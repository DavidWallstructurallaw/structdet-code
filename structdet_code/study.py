"""C01 input contract, exact bindings, and finite selected-population inspection.

This module validates supplied records. It does not execute candidates, decide
algorithm membership, authenticate reviewers, or qualify a longitudinal study.
"""

from collections import Counter, defaultdict
from importlib.resources import files
from pathlib import Path
import re

from . import __version__
from .errors import StudyError, require
from .io import InputDirectory, MAX_JSON, MAX_SOURCE, digest, json_bytes
from .metrics import count_metrics

SCHEMA = "structdet-code.study/0.1"
REASONS = {"insufficient_evidence", "unsupported_syntax", "opaque_dependency",
           "unresolved_reachability", "hybrid", "schema_gap", "review_disagreement",
           "not_reviewed"}


def fields(obj, required: str, optional: str = "") -> None:
    require(isinstance(obj, dict), "object_required")
    needed, allowed = set(required.split()), set((required + " " + optional).split())
    require(needed <= obj.keys() and obj.keys() <= allowed, "unexpected_or_missing_field")


def identifier(value) -> None:
    require(isinstance(value, str)
            and re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{0,63}", value) is not None,
            "invalid_identifier")


def integer(value, low=0, high=1_000_000) -> None:
    require(type(value) is int and low <= value <= high, "invalid_integer")


def text(value, nullable=False) -> None:
    require((nullable and value is None) or (isinstance(value, str) and 0 < len(value) <= 4096),
            "invalid_text")


def enum(value, choices) -> None:
    require(isinstance(value, str) and value in choices, "invalid_enum")


def refs(value) -> None:
    require(isinstance(value, list) and len(value) <= 512, "invalid_reference_list")
    for item in value:
        identifier(item)
    require(len(value) == len(set(value)), "duplicate_reference")


def records(value, maximum=512) -> dict:
    require(isinstance(value, list) and len(value) <= maximum, "record_count_limit")
    result = {}
    for item in value:
        require(isinstance(item, dict) and "id" in item, "record_id_required")
        identifier(item["id"])
        require(item["id"] not in result, "duplicate_record_id")
        result[item["id"]] = item
    return result


def task_pack() -> tuple[dict, str]:
    data = files("structdet_code").joinpath("tasks/sorting.json").read_bytes()
    return json_bytes(data), digest(data)


def inspect_study(path: str | Path) -> dict:
    path = Path(path).absolute()
    with InputDirectory(path.parent) as directory:
        raw = directory.read(path.name, MAX_JSON)
        return _inspect(json_bytes(raw), directory, digest(raw))


def _inspect(study: dict, directory: InputDirectory, study_sha: str) -> dict:
    fields(study, "schema_version study_id data_role evidence_policy task configurations "
           "artifacts assignments suites receipts runs revisions feedback selection")
    require(study["schema_version"] == SCHEMA, "unsupported_schema")
    identifier(study["study_id"])
    enum(study["data_role"], {"fixture", "descriptive"})
    enum(study["evidence_policy"], {"fixture_only", "reviewed_import"})
    require((study["data_role"] == "fixture") == (study["evidence_policy"] == "fixture_only"),
            "role_policy_mismatch")
    pack, pack_sha = task_pack()
    fields(study["task"], "pack_id pack_version resolution_id pack_sha256")
    require(study["task"] == {
        "pack_id": pack["pack_id"], "pack_version": pack["pack_version"],
        "resolution_id": pack["resolution_id"], "pack_sha256": pack_sha,
    }, "unsupported_or_changed_task_frame")
    classes = {item["id"] for item in pack["classes"]}
    configurations = records(study["configurations"], 32)
    for item in configurations.values():
        fields(item, "id model prompt settings selection_rule")
        text(item["model"], nullable=True)
        text(item["prompt"], nullable=True)
        require(item["settings"] is None or isinstance(item["settings"], dict), "invalid_settings")
        text(item["selection_rule"], nullable=True)

    artifacts = records(study["artifacts"], 128)
    sources = {}
    for item in artifacts.values():
        fields(item, "id path sha256 language entry_point origin capture_status")
        enum(item["language"], {"python"})
        require(item["entry_point"] == pack["entry_point"], "unsupported_entry_point")
        enum(item["origin"], {"project_fixture", "model_generated", "supplied", "unknown"})
        enum(item["capture_status"], {"complete", "partial", "unknown"})
        data = directory.read(item["path"], MAX_SOURCE)
        require(item["sha256"] == digest(data), "source_digest_mismatch")
        try:
            sources[item["id"]] = data.decode("utf-8")
        except UnicodeError as exc:
            raise StudyError("source_requires_utf8") from exc

    assignments = records(study["assignments"])
    versions = defaultdict(dict)
    for item in assignments.values():
        fields(item, "id artifact_id source_sha256 pack_sha256 revision status basis class_id "
               "reason reviewer_ref evidence", "note rule_id")
        identifier(item["artifact_id"])
        require(item["artifact_id"] in artifacts, "assignment_artifact_missing")
        artifact = artifacts[item["artifact_id"]]
        require(item["source_sha256"] == artifact["sha256"], "assignment_source_mismatch")
        require(item["pack_sha256"] == pack_sha, "assignment_frame_mismatch")
        integer(item["revision"], 1)
        prior = versions[item["artifact_id"]]
        require(item["revision"] not in prior, "ambiguous_assignment_revision")
        prior[item["revision"]] = item["id"]
        enum(item["status"], {"accepted", "proposed", "unresolved", "conflicted"})
        enum(item["basis"], {"fixture", "human_review", "model_assisted", "static_rule", "unknown"})
        text(item["reviewer_ref"], nullable=True)
        if "note" in item:
            text(item["note"])
        if "rule_id" in item:
            text(item["rule_id"], nullable=True)
        if item["class_id"] is not None:
            identifier(item["class_id"])
            require(item["class_id"] in classes, "class_outside_frame")
        require(isinstance(item["evidence"], list) and len(item["evidence"]) <= 32,
                "invalid_source_evidence")
        for anchor in item["evidence"]:
            fields(anchor, "start_line end_line note")
            integer(anchor["start_line"], 1)
            integer(anchor["end_line"], anchor["start_line"])
            require(anchor["end_line"] <= len(sources[item["artifact_id"]].splitlines()),
                    "source_anchor_out_of_range")
            text(anchor["note"])
        if item["status"] == "accepted":
            require(item["class_id"] is not None and item["reason"] is None
                    and bool(item["evidence"]), "accepted_assignment_lacks_evidence")
            require(artifact["capture_status"] == "complete", "accepted_partial_source")
            allowed_basis = "fixture" if study["evidence_policy"] == "fixture_only" else "human_review"
            require(item["basis"] == allowed_basis, "assignment_basis_not_admissible")
            if allowed_basis == "human_review":
                require(item["reviewer_ref"] is not None, "reviewer_reference_required")
        else:
            enum(item["reason"], REASONS)
            if item["status"] in {"unresolved", "conflicted"}:
                require(item["class_id"] is None, "unresolved_hard_label")

    suites = records(study["suites"], 16)
    suite_sizes = {}
    for item in suites.values():
        fields(item, "id path sha256 oracle_id")
        data = directory.read(item["path"], MAX_JSON)
        require(item["sha256"] == digest(data), "suite_digest_mismatch")
        suite = json_bytes(data)
        fields(suite, "schema_version oracle_id cases")
        require(suite["schema_version"] == "structdet-code.sort-suite/0.1"
                and item["oracle_id"] == suite["oracle_id"] == "sort-properties/0.1",
                "unsupported_suite_oracle")
        cases = records(suite["cases"], 10000)
        require(bool(cases), "empty_test_suite")
        for case in cases.values():
            fields(case, "id input")
            require(isinstance(case["input"], list) and len(case["input"]) <= 256,
                    "test_input_outside_domain")
            for value in case["input"]:
                integer(value, 0, 4095)
        suite_sizes[item["id"]] = len(cases)

    runs = records(study["runs"], 128)
    for item in runs.values():
        fields(item, "id configuration_id root_group_id stop_reason endpoint_revision_id")
        identifier(item["configuration_id"])
        require(item["configuration_id"] in configurations, "configuration_missing")
        if item["root_group_id"] is not None:
            identifier(item["root_group_id"])
        enum(item["stop_reason"], {"success", "failure", "budget", "timeout", "running", "unknown"})
        if item["endpoint_revision_id"] is not None:
            identifier(item["endpoint_revision_id"])

    revisions = records(study["revisions"])
    by_run = defaultdict(list)
    for item in revisions.values():
        fields(item, "id run_id ordinal artifact_id parents missing_parents kind feedback_ids")
        identifier(item["run_id"])
        identifier(item["artifact_id"])
        require(item["run_id"] in runs and item["artifact_id"] in artifacts,
                "revision_run_or_artifact_missing")
        integer(item["ordinal"])
        enum(item["kind"], {"generation", "edit", "no_op", "merge"})
        refs(item["parents"])
        refs(item["missing_parents"])
        refs(item["feedback_ids"])
        require(set(item["missing_parents"]) <= set(item["parents"]), "invalid_missing_parents")
        for parent_id in item["parents"]:
            if parent_id in item["missing_parents"]:
                require(parent_id not in revisions, "parent_declared_missing_but_present")
                continue
            require(parent_id in revisions, "undeclared_missing_parent")
            parent = revisions[parent_id]
            # Parent shape is checked when its own record is visited.
            require(parent.get("run_id") == item["run_id"], "cross_run_parent")
            integer(parent.get("ordinal"))
            require(parent["ordinal"] < item["ordinal"], "parent_order_violation")
        if item["kind"] == "generation":
            require(not item["parents"], "generation_has_parent")
        elif item["kind"] == "merge":
            require(len(item["parents"]) >= 2, "merge_needs_parents")
        else:
            require(len(item["parents"]) == 1, "revision_needs_one_parent")
            if not item["missing_parents"]:
                parent = revisions[item["parents"][0]]
                identifier(parent.get("artifact_id"))
                require(parent.get("artifact_id") in artifacts, "parent_artifact_missing")
                same = (artifacts[parent["artifact_id"]]["sha256"]
                        == artifacts[item["artifact_id"]]["sha256"])
                require(same == (item["kind"] == "no_op"), "revision_change_kind_mismatch")
        by_run[item["run_id"]].append(item)
    for run in runs.values():
        history = by_run[run["id"]]
        require(bool(history), "run_has_no_recorded_revision")
        require(len({r["ordinal"] for r in history}) == len(history), "duplicate_revision_ordinal")
        require(sum(r["kind"] == "generation" for r in history) <= 1, "multiple_run_roots")
        endpoint = run["endpoint_revision_id"]
        require(endpoint is None or (endpoint in revisions
                and revisions[endpoint]["run_id"] == run["id"]), "invalid_run_endpoint")

    receipts = records(study["receipts"], 1024)
    for item in receipts.values():
        fields(item, "id revision_id artifact_id source_sha256 suite_id suite_sha256 "
               "environment status attempted completed passed conformance visibility execution_basis")
        for key in ("revision_id", "artifact_id", "suite_id"):
            identifier(item[key])
        require(item["revision_id"] in revisions and item["artifact_id"] in artifacts
                and item["suite_id"] in suites, "receipt_reference_missing")
        require(revisions[item["revision_id"]]["artifact_id"] == item["artifact_id"]
                and artifacts[item["artifact_id"]]["sha256"] == item["source_sha256"],
                "receipt_source_binding_mismatch")
        require(suites[item["suite_id"]]["sha256"] == item["suite_sha256"],
                "receipt_suite_binding_mismatch")
        fields(item["environment"], "python platform runner")
        for value in item["environment"].values():
            text(value)
        enum(item["status"], {"passed", "failed", "partial", "timeout", "error"})
        enum(item["conformance"], {"passed", "failed", "unknown"})
        enum(item["visibility"], {"feedback", "withheld", "unknown"})
        enum(item["execution_basis"], {"project_fixture_execution", "fixture_stipulated", "external_report"})
        require(study["data_role"] == "fixture" or item["execution_basis"] == "external_report",
                "fixture_receipt_in_real_study")
        integer(item["attempted"], 0, suite_sizes[item["suite_id"]])
        integer(item["completed"], 0, item["attempted"])
        integer(item["passed"], 0, item["completed"])
        if item["status"] == "passed":
            require(item["passed"] == item["completed"] == item["attempted"]
                    == suite_sizes[item["suite_id"]], "incomplete_passing_receipt")
        if item["status"] == "failed":
            require(item["passed"] < item["completed"], "failure_without_failed_case")

    feedback = records(study["feedback"], 1024)
    for item in feedback.values():
        fields(item, "id revision_id kind receipt_id visible_to_agent")
        identifier(item["revision_id"])
        require(item["revision_id"] in revisions, "feedback_revision_missing")
        enum(item["kind"], {"test", "build", "lint", "human", "model"})
        require(type(item["visible_to_agent"]) is bool, "invalid_feedback_visibility")
        if item["receipt_id"] is not None:
            identifier(item["receipt_id"])
            require(item["receipt_id"] in receipts, "feedback_receipt_missing")
            receipt = receipts[item["receipt_id"]]
            require(receipt["revision_id"] == item["revision_id"], "feedback_receipt_wrong_revision")
            require(not item["visible_to_agent"] or receipt["visibility"] == "feedback",
                    "feedback_exposes_withheld_or_unknown_receipt")
    ancestors = {}
    for item in sorted(revisions.values(), key=lambda r: (r["ordinal"], r["id"])):
        lineage = set(item["parents"])
        for parent_id in item["parents"]:
            lineage.update(ancestors.get(parent_id, ()))
        ancestors[item["id"]] = lineage
        for feedback_id in item["feedback_ids"]:
            require(feedback_id in feedback, "received_feedback_missing")
            event = feedback[feedback_id]
            require(event["visible_to_agent"] and event["revision_id"] in lineage,
                    "feedback_not_available_to_revision")

    require(isinstance(study["selection"], list) and len(study["selection"]) <= 128,
            "selection_limit")
    selected, selected_runs = [], set()
    all_counts, valid_counts = Counter(), Counter()
    statuses, validity, reasons = Counter(), Counter(), Counter()
    for item in study["selection"]:
        fields(item, "revision_id assignment_id receipt_id")
        identifier(item["revision_id"])
        require(item["revision_id"] in revisions, "selection_revision_missing")
        revision = revisions[item["revision_id"]]
        require(revision["run_id"] not in selected_runs, "multiple_selected_revisions_per_run")
        selected_runs.add(revision["run_id"])
        artifact_id = revision["artifact_id"]
        assignment = None
        if item["assignment_id"] is not None:
            identifier(item["assignment_id"])
            require(item["assignment_id"] in assignments, "selection_assignment_missing")
            assignment = assignments[item["assignment_id"]]
            require(assignment["artifact_id"] == artifact_id, "selection_assignment_wrong_artifact")
            require(assignment["revision"] == max(versions[artifact_id]), "stale_assignment_selected")
        receipt, valid_state = None, "not_assessed"
        if item["receipt_id"] is not None:
            identifier(item["receipt_id"])
            require(item["receipt_id"] in receipts, "selection_receipt_missing")
            receipt = receipts[item["receipt_id"]]
            require(receipt["revision_id"] == revision["id"], "selection_receipt_wrong_revision")
            if receipt["status"] == "failed" or receipt["conformance"] == "failed":
                valid_state = "failed"
            elif receipt["status"] == "passed" and receipt["conformance"] == "passed":
                valid_state = "passed_under_supplied_scope"
            else:
                valid_state = "undetermined"
        state = assignment["status"] if assignment else "not_reviewed"
        statuses[state] += 1
        validity[valid_state] += 1
        if assignment and state == "accepted":
            all_counts[assignment["class_id"]] += 1
            if valid_state == "passed_under_supplied_scope":
                valid_counts[assignment["class_id"]] += 1
        else:
            reasons[assignment["reason"] if assignment else "not_reviewed"] += 1
        selected.append({
            "revision_id": revision["id"], "run_id": revision["run_id"],
            "artifact_id": artifact_id, "source_sha256": artifacts[artifact_id]["sha256"],
            "assignment_id": item["assignment_id"], "assignment_status": state,
            "proposed_or_accepted_class": assignment["class_id"] if assignment else None,
            "reason": assignment["reason"] if assignment else "not_reviewed",
            "source_anchors": [{"start_line": e["start_line"], "end_line": e["end_line"]}
                               for e in assignment["evidence"]] if assignment else [],
            "receipt_id": item["receipt_id"], "validity": valid_state,
            "suite_id": receipt["suite_id"] if receipt else None,
            "test_status": receipt["status"] if receipt else "not_assessed",
        })
    histories = []
    for run in runs.values():
        history = sorted(by_run[run["id"]], key=lambda r: r["ordinal"])
        histories.append({
            "run_id": run["id"], "configuration_id": run["configuration_id"],
            "root_group_id": run["root_group_id"], "stop_reason": run["stop_reason"],
            "endpoint_revision_id": run["endpoint_revision_id"],
            "ordinal_gaps": [{"after": a["ordinal"], "before": b["ordinal"]}
                             for a, b in zip(history, history[1:]) if b["ordinal"] > a["ordinal"] + 1],
            "revisions": [{key: r[key] for key in ("id", "ordinal", "artifact_id", "parents",
                           "missing_parents", "kind", "feedback_ids")} for r in history],
        })
    return {
        "result_schema": "structdet-code.inspection/0.1", "software_version": __version__,
        "study_id": study["study_id"], "study_sha256": study_sha, "task": study["task"],
        "data_role": study["data_role"], "evidence_policy": study["evidence_policy"],
        "record_inspection_complete": True, "substantive_validation_performed": False,
        "candidate_execution_performed": False, "mechanism_recognition_performed": False,
        "claim_scope": "fixture_arithmetic" if study["data_role"] == "fixture" else "supplied_review_records_only",
        "ledger": {
            "recorded_runs": len(runs), "recorded_revisions": len(revisions),
            "generation_records": sum(r["kind"] == "generation" for r in revisions.values()),
            "no_op_revisions": sum(r["kind"] == "no_op" for r in revisions.values()),
            "source_records": len(artifacts), "unique_source_bytes": len({a["sha256"] for a in artifacts.values()}),
            "test_receipts": len(receipts), "selected_observations": len(selected),
            "selected_unique_source_bytes": len({s["source_sha256"] for s in selected}),
            "assignment_states": dict(sorted(statuses.items())), "validity_states": dict(sorted(validity.items())),
            "unadmitted_reasons": dict(sorted(reasons.items())),
        },
        "views": {"classified_all": count_metrics(all_counts, sum(all_counts.values())),
                  "classified_valid": count_metrics(valid_counts, sum(valid_counts.values()))},
        "selected_observations": selected, "recorded_histories": histories,
        "limitations": ["Record checks do not authenticate reviews, provenance or test execution.",
                        "Mechanism labels are supplied; automatic recognition starts in C02.",
                        "Finite test passing is limited to the named suite and supplied conformance review.",
                        "C01 preserves revision links; cohort convergence analysis is scheduled for C04."],
    }
