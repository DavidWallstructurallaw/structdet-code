"""Passive intervention records and receipt-bound finite failure profiles."""

from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import re

from .errors import require
from .io import InputDirectory, MAX_JSON, MAX_SOURCE, digest, json_bytes
from .study import enum, fields, identifier, integer, load_study, records, refs, text
from .workflow import _write_new, encoded

SCHEMA = "structdet-code.evidence/0.1"
MAX_RESULT = 4_194_304


def bounded_result(result):
    require(len(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False).encode())
            <= MAX_RESULT, "analysis_result_size_limit")
    return result


def evidence_document(inspection):
    return {"schema_version": SCHEMA, "study_sha256": inspection["study_sha256"],
            "materials": [], "interventions": [], "failure_profiles": []}


def prepare_evidence(study_path, output):
    _, result = load_study(study_path)
    _write_new(Path(output).absolute(), encoded(evidence_document(result)))
    return {"status": "evidence_template_created", "supplied_records": 0,
            "candidate_execution_performed": False}


def _hash(value, nullable=False):
    require(nullable and value is None or isinstance(value, str)
            and re.fullmatch(r"[0-9a-f]{64}", value) is not None, "invalid_sha256")


def _materials(items, directory):
    material_map, public = records(items, 64), {}
    for key, item in material_map.items():
        fields(item, "id path sha256 kind origin source_ref independence_claim")
        enum(item["kind"], {"instruction", "reference_code", "test_feedback", "other"})
        enum(item["origin"], {"external", "project_fixture", "supplied", "unknown"})
        enum(item["independence_claim"], {"unknown", "shared_origin", "claimed_independent"})
        text(item["source_ref"], nullable=True)
        _hash(item["sha256"], nullable=True)
        available = item["path"] is not None
        if available:
            raw = directory.read(item["path"], MAX_SOURCE)
            require(digest(raw) == item["sha256"], "material_digest_mismatch")
        public[key] = {"id": key, "kind": item["kind"], "origin": item["origin"],
                       "sha256": item["sha256"], "bytes_captured": available,
                       "source_ref_sha256": digest(item["source_ref"].encode()) if item["source_ref"] else None,
                       "independence_claim": item["independence_claim"],
                       "independence_verified": False}
    return public


def _interventions(items, study, materials, result):
    events = records(items, 512)
    revisions = {r["id"]: r for r in study["revisions"]}
    feedback = {f["id"]: f for f in study["feedback"]}
    ancestors = {}
    for revision in sorted(revisions.values(), key=lambda r: (r["ordinal"], r["id"])):
        ancestors[revision["id"]] = set(revision["parents"])
        for parent in revision["parents"]:
            ancestors[revision["id"]].update(ancestors.get(parent, ()))
    rows, paths = {}, {}
    for run in result.get("trajectories", []):
        rows.update({row["revision_id"]: row for row in run["revisions"]})
        paths[run["run_id"]] = run["selected_path"]
    orders, by_run, public = set(), defaultdict(list), []
    for item in events.values():
        fields(item, "id run_id after_revision_id before_revision_id order kind material_ids feedback_ids visibility reuse_claim")
        identifier(item["run_id"])
        identifier(item["before_revision_id"])
        require(item["before_revision_id"] in revisions, "intervention_revision_missing")
        before = revisions[item["before_revision_id"]]
        require(before["run_id"] == item["run_id"], "intervention_run_mismatch")
        after_id = item["after_revision_id"]
        if after_id is not None:
            identifier(after_id)
            require(after_id in revisions and revisions[after_id]["run_id"] == item["run_id"]
                    and after_id in ancestors[before["id"]], "intervention_not_between_ancestors")
        integer(item["order"], 1)
        require((item["run_id"], item["order"]) not in orders, "duplicate_intervention_order")
        orders.add((item["run_id"], item["order"]))
        by_run[item["run_id"]].append((item["order"], before["ordinal"]))
        enum(item["kind"], {"baseline_prompt", "alternative_strategy", "test_feedback", "reference_material", "other"})
        if after_id is None:
            require(item["kind"] == "baseline_prompt" and not before["parents"],
                    "intervention_start_requires_root_prompt")
        enum(item["visibility"], {"visible", "withheld", "unknown"})
        enum(item["reuse_claim"], {"copied", "adapted", "none", "unknown"})
        refs(item["material_ids"])
        refs(item["feedback_ids"])
        require(set(item["material_ids"]) <= materials.keys(), "intervention_material_missing")
        if item["reuse_claim"] in {"copied", "adapted"}:
            require(item["kind"] == "reference_material" and bool(item["material_ids"]),
                    "reuse_claim_without_reference")
        for key in item["feedback_ids"]:
            require(key in feedback and feedback[key]["revision_id"] == after_id,
                    "intervention_feedback_binding_mismatch")
            if item["visibility"] == "visible":
                require(feedback[key]["visible_to_agent"] and key in before["feedback_ids"],
                        "intervention_feedback_not_received")
            else:
                require(key not in before["feedback_ids"], "intervention_visibility_conflict")
        if item["kind"] == "test_feedback":
            require(bool(item["feedback_ids"]), "test_intervention_needs_feedback")
            require(all(feedback[key]["kind"] == "test" and feedback[key]["receipt_id"] is not None
                        for key in item["feedback_ids"]), "test_intervention_requires_test_receipts")
        target, prior = rows.get(before["id"]), rows.get(after_id)
        target_class = (target["proposed_or_accepted_class"] if target
                        and target["assignment_status"] == "accepted" else None)
        prior_class = (prior["proposed_or_accepted_class"] if prior
                       and prior["assignment_status"] == "accepted" else None)
        artifact = next(a for a in study["artifacts"] if a["id"] == before["artifact_id"])
        matches = [key for key in item["material_ids"] if materials[key]["bytes_captured"]
                   and materials[key]["kind"] == "reference_code"
                   and materials[key]["sha256"] == artifact["sha256"]]
        path = paths.get(item["run_id"])
        on_path = path is not None and before["id"] in path and (after_id is None or after_id in path)
        relation = "not_traced" if not rows else "outside_selected_path"
        if on_path:
            relation = "unresolved_assignment"
            if target_class is not None and (after_id is None or prior_class is not None):
                seen = {rows[key]["proposed_or_accepted_class"] for key in path[:path.index(before["id"])]
                        if rows[key]["assignment_status"] == "accepted"}
                relation = ("persisted" if target_class == prior_class else
                            "observed_again" if target_class in seen else "first_observed")
        public.append({**item, "after_ordinal": revisions[after_id]["ordinal"] if after_id else None,
                       "before_ordinal": before["ordinal"], "source_sha256": artifact["sha256"],
                       "prior_class": prior_class, "subsequent_class": target_class,
                       "selected_path_relation": relation,
                       "agent_visible_association": item["visibility"] == "visible" and on_path,
                       "exact_material_matches": sorted(matches),
                       "material_bytes_unavailable": sorted(key for key in item["material_ids"]
                                                           if not materials[key]["bytes_captured"]),
                       "causal_effect_estimated": False, "autonomous_discovery_established": False,
                       "external_recovery_rate": {"status": "not_estimated",
                                                 "reason": "recorded_association_is_not_qualified_recovery"}})
    for sequence in by_run.values():
        ordinals = [ordinal for _, ordinal in sorted(sequence)]
        require(ordinals == sorted(ordinals), "intervention_order_conflicts_with_revisions")
    return sorted(public, key=lambda e: (e["run_id"], e["order"]))


def _profiles(items, study, study_path, selected_receipts):
    from .trace import _scope
    profiles = records(items, 32)
    receipts = {r["id"]: r for r in study["receipts"]}
    revisions = {r["id"]: r for r in study["revisions"]}
    suites = {s["id"]: s for s in study["suites"]}
    cases = {}
    needed = set()
    for item in profiles.values():
        fields(item, "id receipt_id outcomes")
        identifier(item["receipt_id"])
        require(item["receipt_id"] in receipts, "profile_receipt_missing")
        needed.add(receipts[item["receipt_id"]]["suite_id"])
    with InputDirectory(Path(study_path).absolute().parent) as directory:
        for key in sorted(needed):
            raw = directory.read(suites[key]["path"], MAX_JSON)
            require(digest(raw) == suites[key]["sha256"], "suite_digest_mismatch")
            cases[key] = set(records(json_bytes(raw)["cases"], 10000))
    public, outcomes_by_id, seen_receipts = [], {}, set()
    for item in profiles.values():
        receipt = receipts[item["receipt_id"]]
        require(receipt["id"] not in seen_receipts, "duplicate_profile_receipt")
        seen_receipts.add(receipt["id"])
        outcomes = records(item["outcomes"], 10000)
        require(outcomes.keys() == cases[receipt["suite_id"]], "profile_case_roster_mismatch")
        for outcome in outcomes.values():
            fields(outcome, "id status")
            enum(outcome["status"], {"passed", "failed", "not_completed", "not_attempted"})
        counts = Counter(o["status"] for o in outcomes.values())
        require(counts["passed"] == receipt["passed"]
                and counts["passed"] + counts["failed"] == receipt["completed"]
                and counts["passed"] + counts["failed"] + counts["not_completed"] == receipt["attempted"],
                "profile_receipt_counts_mismatch")
        outcomes_by_id[item["id"]] = {key: value["status"] for key, value in outcomes.items()}
        public.append({"id": item["id"], "receipt_id": receipt["id"], "revision_id": receipt["revision_id"],
                       "run_id": revisions[receipt["revision_id"]]["run_id"],
                       "source_sha256": receipt["source_sha256"], "test_scope": _scope(receipt, suites),
                       "selected_for_analysis": receipt["id"] in selected_receipts,
                       "receipt_status": receipt["status"], "conformance": receipt["conformance"],
                       "case_count": len(outcomes), "status_counts": dict(sorted(counts.items())),
                       "failed_case_ids": sorted(key for key, o in outcomes.items() if o["status"] == "failed"),
                       "unobserved_case_ids": sorted(key for key, o in outcomes.items()
                                                   if o["status"] in {"not_completed", "not_attempted"})})
    pairs = []
    for left, right in combinations(sorted(public, key=lambda p: p["id"]), 2):
        reasons = []
        if left["test_scope"] != right["test_scope"]:
            reasons.append("test_scope_mismatch")
        if any(p["test_scope"]["visibility"] == "unknown" for p in (left, right)):
            reasons.append("test_visibility_unknown")
        pair = {"left": left["id"], "right": right["id"],
                "status": "unavailable" if reasons else "comparable_finite_cases", "reasons": reasons,
                "same_source_bytes": left["source_sha256"] == right["source_sha256"],
                "same_run": left["run_id"] == right["run_id"], "failure_independence_established": False}
        if not reasons:
            a, b = outcomes_by_id[left["id"]], outcomes_by_id[right["id"]]
            common = {key for key in a if a[key] in {"passed", "failed"} and b[key] in {"passed", "failed"}}
            pair.update({"both_completed": len(common), "suite_cases": len(a),
                         "complete_suite_both": len(common) == len(a),
                         "both_failed": sorted(key for key in common if a[key] == b[key] == "failed"),
                         "left_failed_right_passed": sorted(key for key in common if a[key] == "failed" and b[key] == "passed"),
                         "right_failed_left_passed": sorted(key for key in common if b[key] == "failed" and a[key] == "passed"),
                         "left_failures_other_unobserved": sorted(key for key in a if a[key] == "failed" and key not in common),
                         "right_failures_other_unobserved": sorted(key for key in b if b[key] == "failed" and key not in common)})
        pairs.append(pair)
    return {"profiles": sorted(public, key=lambda p: p["id"]), "pairs": pairs,
            "scope": "explicit_supplied_receipts", "failure_independence_established": False,
            "deployment_reliability_estimated": False}


def analyze_evidence(study, inspection, study_path, evidence_path, result):
    path = Path(evidence_path).absolute()
    with InputDirectory(path.parent) as directory:
        raw = directory.read(path.name, MAX_JSON)
        document = json_bytes(raw)
        fields(document, "schema_version study_sha256 materials interventions failure_profiles")
        require(document["schema_version"] == SCHEMA, "unsupported_evidence_schema")
        require(document["study_sha256"] == inspection["study_sha256"], "evidence_study_binding_mismatch")
        materials = _materials(document["materials"], directory)
    selected = {row["receipt_id"] for row in result.get("selected_observations", [])}
    for run in result.get("trajectories", []):
        selected.update(row["receipt_id"] for row in run["revisions"] if row["on_selected_path"])
    return bounded_result({
        "schema_version": "structdet-code.evidence-result/0.1", "evidence_sha256": digest(raw),
        "materials": [materials[key] for key in sorted(materials)],
        "interventions": _interventions(document["interventions"], study, materials, result),
        "failure_profiles": _profiles(document["failure_profiles"], study, study_path, selected),
        "provenance_authenticated": False, "candidate_execution_performed": False,
        "limitations": [
            "Intervention order, visibility and reuse are supplied records; source independence is not authenticated.",
            "Exact reference-byte matches describe content identity, without proof of how the program was produced.",
            "A mechanism observed after a visible intervention is an association, with no causal or autonomous-discovery claim.",
            "Failure overlap uses the same finite test scope and jointly completed cases; absent outcomes are not successes.",
            "Failure profiles do not establish independent errors, deployment reliability or a preferred candidate.",
        ]})


def evidence_markdown(evidence):
    lines = ["", "## Interventions and supplied evidence", "",
             f"Evidence binding: {evidence['evidence_sha256']}. Material records: {len(evidence['materials'])}.",
             "", "Study configurations describe the original context; these ordered records describe subsequent supplied exposure. "
             "More than one event can precede the same revision, so a subsequent class is not attributed to one event.",
             "", "| Run | Order | After / before revision | Kind / visibility | Mechanism observation | Exact reference matches |",
             "| --- | --- | --- | --- | --- | --- |"]
    for event in evidence["interventions"]:
        lines.append(f"| {event['run_id']} | {event['order']} | {event['after_revision_id']} / {event['before_revision_id']} "
                     f"| {event['kind']} / {event['visibility']} | {event['selected_path_relation']} "
                     f"({event['prior_class']} to {event['subsequent_class']}) | {event['exact_material_matches']} |")
    for event in evidence["interventions"]:
        lines += ["", f"Event {event['id']}: materials {event['material_ids']}; feedback {event['feedback_ids']}; "
                  f"reuse claim {event['reuse_claim']}; agent-visible selected-path association {event['agent_visible_association']}; "
                  f"uncaptured materials {event['material_bytes_unavailable']}. External recovery is not estimated."]
    for material in evidence["materials"]:
        lines += ["", f"Material {material['id']}: {material['kind']}, origin {material['origin']}, "
                  f"bytes captured {material['bytes_captured']}, SHA-256 {material['sha256']}; "
                  f"independence claim {material['independence_claim']} (unverified)."]
    lines += ["", "## Finite failure profiles", "",
              "Profiles describe the explicitly supplied receipts, including any outside the analysis selection.", ""]
    for profile in evidence["failure_profiles"]["profiles"]:
        lines += [f"- {profile['id']}: receipt {profile['receipt_id']}, revision {profile['revision_id']}; "
                  f"selected {profile['selected_for_analysis']}; conformance {profile['conformance']}; "
                  f"failed cases {profile['failed_case_ids']}; unobserved {profile['unobserved_case_ids']}; "
                  f"source {profile['source_sha256']}; scope {profile['test_scope']['scope_sha256']}."]
    lines.append("")
    for pair in evidence["failure_profiles"]["pairs"]:
        if pair["status"] == "unavailable":
            lines += [f"- {pair['left']} / {pair['right']}: unavailable, {pair['reasons']}."]
        else:
            lines += [f"- {pair['left']} / {pair['right']}: completed in both {pair['both_completed']}/{pair['suite_cases']}; "
                      f"both failed {pair['both_failed']}; left failed/right passed {pair['left_failed_right_passed']}; "
                      f"right failed/left passed {pair['right_failed_left_passed']}; "
                      f"failures with other side unobserved {pair['left_failures_other_unobserved']} / {pair['right_failures_other_unobserved']}; "
                      f"same bytes {pair['same_source_bytes']}, same run {pair['same_run']}."]
    lines += ["", "Failure independence and causal effects are not established.", ""]
    lines += ["- " + item for item in evidence["limitations"]]
    return "\n".join(lines) + "\n"
