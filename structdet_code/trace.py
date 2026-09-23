"""Passive revision trajectories and exact-ordinal run cohorts.

The study owns artifacts, parent links and evidence. A small bound design owns
the run roster, selected paths, checkpoints and supplied budget/stop context.
No program is run, absent revision is filled, or training clock is inferred.
"""

from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path

from . import __version__
from .comparison import _fingerprint, _fraction, _population
from .errors import require
from .io import InputDirectory, MAX_JSON, digest, json_bytes
from .study import fields, identifier, integer, load_study, refs, selected_observation, text
from .workflow import _write_new, encoded

SCHEMA = "structdet-code.trace/0.1"
SELECTION = "declared-path-exact-ordinal/0.1"
TERMINAL = {"success", "failure", "budget", "timeout"}
MAX_CHECKPOINTS = 32
MAX_RESULT = 4_194_304


def _maps(study, inspection):
    context = {key: {item["id"]: item for item in study[key]}
               for key in ("revisions", "artifacts", "assignments", "receipts")}
    context["latest"] = {}
    for item in study["assignments"]:
        context["latest"][item["artifact_id"]] = max(
            item["revision"], context["latest"].get(item["artifact_id"], 0))
    context["analyses"] = {item["artifact_id"]: item for item in inspection["source_analysis"]}
    context["policy"] = study["evidence_policy"]
    return context


def _unambiguous_path(run, history):
    """Follow an explicitly selected endpoint, or a complete unique linear chain."""
    by_id = {item["id"]: item for item in history}
    endpoint = run["endpoint_revision_id"]
    if endpoint is None:
        ordered = sorted(history, key=lambda item: item["ordinal"])
        if (ordered[0]["parents"] or any(right["parents"] != [left["id"]]
                for left, right in zip(ordered, ordered[1:]))):
            return None
        return [item["id"] for item in ordered]
    path, current = [], by_id[endpoint]
    while True:
        path.append(current["id"])
        if not current["parents"] or all(parent in current["missing_parents"] for parent in current["parents"]):
            return list(reversed(path))
        if len(current["parents"]) != 1:
            return None
        current = by_id[current["parents"][0]]


def trace_document(study, inspection):
    context = _maps(study, inspection)
    by_run, by_revision = defaultdict(list), defaultdict(list)
    for revision in study["revisions"]:
        by_run[revision["run_id"]].append(revision)
    for receipt in study["receipts"]:
        by_revision[receipt["revision_id"]].append(receipt["id"])
    chosen = {item["revision_id"]: item for item in study["selection"]}
    latest = {item["artifact_id"]: item["id"] for item in study["assignments"]
              if item["revision"] == context["latest"][item["artifact_id"]]}
    configurations = {run["configuration_id"] for run in study["runs"]}
    assessments = []
    for revision in sorted(study["revisions"], key=lambda item: (item["run_id"], item["ordinal"])):
        receipt_ids = by_revision[revision["id"]]
        receipt = (chosen[revision["id"]]["receipt_id"] if revision["id"] in chosen else
                   receipt_ids[0] if len(receipt_ids) == 1 else None)
        assessments.append({"revision_id": revision["id"],
                            "assignment_id": latest.get(revision["artifact_id"]), "receipt_id": receipt})
    return {"schema_version": SCHEMA, "trace_id": "revision-trace",
            "study_sha256": inspection["study_sha256"],
            "configuration_id": next(iter(configurations)) if len(configurations) == 1 else None,
            "protocol_ref": None, "clock": "revision_ordinal", "selection_rule": SELECTION,
            "checkpoints": [],
            "runs": [{"run_id": run["id"], "missing": False,
                      "path": _unambiguous_path(run, by_run[run["id"]]),
                      "stop_ordinal": None, "budget": None} for run in study["runs"]],
            "assessments": assessments}


def prepare_trace(study_path, output):
    study, inspection = load_study(study_path)
    document = trace_document(study, inspection)
    _write_new(Path(output).absolute(), encoded(document))
    return {"status": "trace_template_created", "schema_version": SCHEMA,
            "candidate_execution_performed": False}


def _scope(receipt, suites):
    if receipt is None:
        return None
    value = {"suite_sha256": receipt["suite_sha256"],
             "oracle_id": suites[receipt["suite_id"]]["oracle_id"],
             "environment_sha256": _fingerprint(receipt["environment"]),
             "execution_basis": receipt["execution_basis"], "visibility": receipt["visibility"]}
    return {"scope_sha256": _fingerprint(value), **value}


def _class(row):
    return row["proposed_or_accepted_class"] if row["assignment_status"] == "accepted" else None


def _edge(left, right):
    a, b = _class(left), _class(right)
    same = left["source_sha256"] == right["source_sha256"]
    if left["revision_id"] not in right["parents"]:
        state = "missing_lineage"
    elif right["kind"] == "merge":
        state = "merge_parent_comparison"
    elif right["ordinal"] != left["ordinal"] + 1:
        state = "ordinal_gap"
    elif a is None or b is None:
        state = "unresolved_assignment"
    elif same:
        state = "unchanged_source_and_mechanism"
    elif a == b:
        state = "source_change_same_mechanism"
    else:
        state = "mechanism_switch"
    return {"from_revision": left["revision_id"], "to_revision": right["revision_id"],
            "from_ordinal": left["ordinal"], "to_ordinal": right["ordinal"],
            "from_class": a, "to_class": b, "source_changed": not same, "state": state,
            "test_scope_changed": left["test_scope"] != right["test_scope"],
            "received_feedback_ids": right["feedback_ids"]}


def _validate(study, inspection, design):
    fields(design, "schema_version trace_id study_sha256 configuration_id protocol_ref clock selection_rule checkpoints runs assessments")
    require(design["schema_version"] == SCHEMA, "unsupported_trace_schema")
    identifier(design["trace_id"])
    require(design["study_sha256"] == inspection["study_sha256"], "trace_study_binding_mismatch")
    require(design["clock"] == "revision_ordinal", "unsupported_trace_clock")
    require(design["selection_rule"] == SELECTION, "unsupported_trace_selection")
    text(design["protocol_ref"], nullable=True)
    config_id = design["configuration_id"]
    configurations = {item["id"]: item for item in study["configurations"]}
    if config_id is not None:
        identifier(config_id)
        require(config_id in configurations, "trace_configuration_missing")
    checkpoints = design["checkpoints"]
    require(isinstance(checkpoints, list) and len(checkpoints) <= MAX_CHECKPOINTS, "trace_checkpoint_limit")
    for value in checkpoints:
        integer(value)
    require(checkpoints == sorted(set(checkpoints)), "trace_checkpoints_not_strictly_increasing")
    require(isinstance(design["runs"], list) and len(design["runs"]) <= 128, "trace_run_limit")
    runs = {item["id"]: item for item in study["runs"]}
    revisions = {item["id"]: item for item in study["revisions"]}
    by_run = defaultdict(list)
    for revision in study["revisions"]:
        by_run[revision["run_id"]].append(revision)
    roster = {}
    for item in design["runs"]:
        fields(item, "run_id missing path stop_ordinal budget")
        run_id = item["run_id"]
        identifier(run_id)
        require(run_id not in roster, "duplicate_trace_run")
        require(type(item["missing"]) is bool, "invalid_missing_run_flag")
        roster[run_id] = item
        budget = item["budget"]
        if budget is not None:
            fields(budget, "max_revision_ordinal max_test_case_attempts")
            for key, value in budget.items():
                if value is not None:
                    integer(value, 0, 1_000_000 if key == "max_revision_ordinal" else 1_000_000_000)
        if item["missing"]:
            require(run_id not in runs, "trace_run_declared_missing_but_present")
            require(item["path"] is None and item["stop_ordinal"] is None,
                    "missing_run_has_path_or_stop")
            continue
        require(run_id in runs, "trace_run_not_recorded")
        run = runs[run_id]
        require(config_id is None or run["configuration_id"] == config_id, "trace_run_configuration_mismatch")
        if item["stop_ordinal"] is not None:
            integer(item["stop_ordinal"])
            require(run["stop_reason"] in TERMINAL, "trace_stop_without_terminal_reason")
            require(item["stop_ordinal"] >= max(r["ordinal"] for r in by_run[run_id]),
                    "trace_stop_precedes_recorded_revision")
        path = item["path"]
        if path is None:
            continue
        refs(path)
        require(bool(path), "empty_recorded_trace_path")
        require(all(key in revisions and revisions[key]["run_id"] == run_id for key in path),
                "trace_path_revision_missing_or_foreign")
        require(run["endpoint_revision_id"] is None or path[-1] == run["endpoint_revision_id"],
                "trace_path_endpoint_mismatch")
        first = revisions[path[0]]
        require(set(first["parents"]) <= set(first["missing_parents"]), "trace_path_omits_known_ancestor")
        for left, right in zip(path, path[1:]):
            a, b = revisions[left], revisions[right]
            require(a["ordinal"] < b["ordinal"], "trace_path_order_violation")
            # A supplied continuation across a missing direct parent is retained
            # as unresolved lineage. Known sibling jumps and skipped known
            # intermediate revisions cannot masquerade as a selected path.
            require(left in b["parents"] or bool(b["missing_parents"]), "trace_path_not_parent_linked")
    context = _maps(study, inspection)
    require(isinstance(design["assessments"], list) and len(design["assessments"]) <= 512,
            "trace_assessment_limit")
    wanted = {r["id"] for r in study["revisions"] if r["run_id"] in roster}
    rows, classes_by_source = {}, {}
    suites = {item["id"]: item for item in study["suites"]}
    for item in design["assessments"]:
        row = selected_observation(item, **context)
        key = row["revision_id"]
        require(key in wanted, "trace_assessment_outside_roster")
        require(key not in rows, "duplicate_trace_assessment")
        revision = revisions[key]
        run = runs[row["run_id"]]
        receipt = context["receipts"].get(row["receipt_id"])
        row.update(ordinal=revision["ordinal"], kind=revision["kind"], parents=revision["parents"],
                   missing_parents=revision["missing_parents"], feedback_ids=revision["feedback_ids"],
                   root_group_id=run["root_group_id"], artifact_origin=context["artifacts"][row["artifact_id"]]["origin"],
                   test_scope=_scope(receipt, suites))
        if _class(row) is not None:
            previous = classes_by_source.setdefault(row["source_sha256"], _class(row))
            require(previous == _class(row), "trace_conflicting_classes_for_same_source")
        rows[key] = row
    require(rows.keys() == wanted, "trace_assessments_incomplete")
    return roster, rows, configurations.get(config_id)


def _trajectories(study, roster, rows):
    runs = {item["id"]: item for item in study["runs"]}
    suites = {item["id"]: item for item in study["suites"]}
    by_run, receipts, feedback = defaultdict(list), defaultdict(list), defaultdict(list)
    for row in rows.values():
        by_run[row["run_id"]].append(row)
    for receipt in study["receipts"]:
        receipts[receipt["revision_id"]].append(receipt)
    consumers = defaultdict(list)
    for revision in study["revisions"]:
        for key in revision["feedback_ids"]:
            consumers[key].append(revision["id"])
    for event in study["feedback"]:
        feedback[event["revision_id"]].append({**event, "received_by": sorted(consumers[event["id"]])})
    result = []
    for run_id, design in sorted(roster.items()):
        if design["missing"]:
            result.append({"run_id": run_id, "status": "unrecorded", "budget": design["budget"],
                           "stop_ordinal": None, "stop_reason": "unknown", "revisions": [],
                           "selected_path": None, "path_transitions": [], "excluded_revision_ids": []})
            continue
        run = runs[run_id]
        history = sorted(by_run[run_id], key=lambda r: r["ordinal"])
        path = design["path"]
        chosen = set(path or [])
        transitions = [_edge(rows[a], rows[b]) for a, b in zip(path or [], (path or [])[1:])]
        matrix = Counter((edge["from_class"], edge["to_class"]) for edge in transitions
                         if edge["state"] in {"mechanism_switch", "source_change_same_mechanism", "unchanged_source_and_mechanism"})
        visits, seen, last_class = [], set(), None
        for key in path or []:
            cls = _class(rows[key])
            visits.append({"revision_id": key, "ordinal": rows[key]["ordinal"], "class_id": cls,
                           "first_observed": cls is not None and cls not in seen,
                           "observed_again_after_other_class": cls is not None and cls in seen and last_class not in (None, cls)})
            if cls is not None:
                seen.add(cls)
                last_class = cls
        observations, attempts, completed = [], 0, 0
        for row in history:
            test_records = []
            for receipt in sorted(receipts[row["revision_id"]], key=lambda r: r["id"]):
                attempts += receipt["attempted"]
                completed += receipt["completed"]
                test_records.append({key: receipt[key] for key in
                                     ("id", "status", "attempted", "completed", "passed", "conformance", "visibility")}
                                    | {"test_scope": _scope(receipt, suites), "selected": receipt["id"] == row["receipt_id"]})
            observations.append({**row, "on_selected_path": row["revision_id"] in chosen if path is not None else None,
                                 "test_observations": test_records,
                                 "feedback_examining_revision": sorted(feedback[row["revision_id"]], key=lambda e: e["id"])})
        budget, exceeded = design["budget"], []
        if budget is not None:
            reached = max(history[-1]["ordinal"], design["stop_ordinal"] or 0)
            if budget["max_revision_ordinal"] is not None and reached > budget["max_revision_ordinal"]:
                exceeded.append("revision_ordinal_limit")
            if budget["max_test_case_attempts"] is not None and attempts > budget["max_test_case_attempts"]:
                exceeded.append("test_case_attempt_limit")
        result.append({"run_id": run_id, "status": "recorded", "configuration_id": run["configuration_id"],
                       "root_group_id": run["root_group_id"], "stop_reason": run["stop_reason"],
                       "stop_ordinal": design["stop_ordinal"], "endpoint_revision_id": run["endpoint_revision_id"],
                       "budget": budget, "recorded_budget_excess": exceeded,
                       "usage": {"recorded_revisions": len(history), "maximum_ordinal": history[-1]["ordinal"],
                                 "generation_records": sum(row["kind"] == "generation" for row in history),
                                 "no_op_revisions": sum(row["kind"] == "no_op" for row in history),
                                 "test_receipts": sum(len(receipts[row["revision_id"]]) for row in history),
                                 "test_case_attempts": attempts, "completed_test_cases": completed},
                       "selected_path": path,
                       "excluded_revision_ids": [row["revision_id"] for row in history if row["revision_id"] not in chosen] if path is not None else [],
                       "revisions": observations, "path_transitions": transitions, "mechanism_visitation": visits,
                       "transition_states": dict(sorted(Counter(edge["state"] for edge in transitions).items())),
                       "transition_counts": [{"from_class": a, "to_class": b, "count": count}
                                             for (a, b), count in sorted(matrix.items())],
                       "ordinal_gaps": [{"after": a["ordinal"], "before": b["ordinal"]}
                                        for a, b in zip(history, history[1:]) if b["ordinal"] > a["ordinal"] + 1]})
    return result


def _checkpoint_state(run, ordinal):
    if run["status"] == "unrecorded":
        return "run_unrecorded", None
    if run["stop_ordinal"] is not None and run["stop_ordinal"] < ordinal:
        return "stopped_" + run["stop_reason"], None
    if run["selected_path"] is None:
        return "path_unknown", None
    for row in run["revisions"]:
        if row["ordinal"] == ordinal:
            return ("observed", row) if row["on_selected_path"] else ("branch_excluded", None)
    if ordinal > run["usage"]["maximum_ordinal"]:
        return ("stop_time_unknown" if run["stop_reason"] in TERMINAL and run["stop_ordinal"] is None
                else "not_recorded_at_checkpoint"), None
    return "missing_revision", None


def _snapshot(rows, requested):
    result = _population(rows, requested)
    result["run_ids"] = sorted(row["run_id"] for row in rows)
    result["revision_ids"] = [row["revision_id"] for row in sorted(rows, key=lambda r: r["run_id"])]
    for view in result["views"].values():
        if view["population_size"] == 1:
            view["qualifiers"].append("single_admitted_observation")
            for key in ("sci", "gini_simpson"):
                view[key] = {"status": "not_applicable", "reason": "single_admitted_observation",
                             "value": None, "numerator": None, "denominator": None}
    return result


def _delta(a, b):
    difference = Fraction(b["numerator"], b["denominator"]) - Fraction(a["numerator"], a["denominator"])
    return _fraction(difference.numerator, difference.denominator)


def _numeric_contrast(left, right, reasons):
    reasons = list(reasons)
    if left["population_size"] < 2 or right["population_size"] < 2:
        reasons.append("fewer_than_two_admitted_runs")
    if reasons:
        return {"status": "unavailable", "reasons": sorted(set(reasons)), "later_minus_earlier": None}
    return {"status": "available", "reasons": [],
            "earlier_population": left["population_size"], "later_population": right["population_size"],
            "later_minus_earlier": {"observed_support": right["observed_support"] - left["observed_support"],
                                    "sci": _delta(left["sci"], right["sci"]),
                                    "gini_simpson": _delta(left["gini_simpson"], right["gini_simpson"])}}


def _set_change(previous, current, seen, reasons):
    before, after = set(previous["class_counts"]), set(current["class_counts"])
    retained, entered = before & after, after - before
    return {"status": "inventory_only" if reasons else "comparable_observed_sets",
            "qualifiers": sorted(set(reasons)), "reference_classes": sorted(before), "current_classes": sorted(after),
            "retained": sorted(retained), "no_longer_observed": sorted(before - after),
            "new_since_previous": sorted(entered), "first_observed": sorted(after - seen),
            "observed_again": sorted(entered & seen),
            "retention_fraction": _fraction(len(retained), len(before))}


def _scope_reasons(rows):
    reasons = []
    scopes = [row["test_scope"] for row in rows]
    if any(scope is None for scope in scopes):
        reasons.append("test_receipts_missing")
    if any(scope is not None and scope["visibility"] == "unknown" for scope in scopes):
        reasons.append("test_visibility_unknown")
    if len({scope["scope_sha256"] for scope in scopes if scope is not None}) != 1:
        reasons.append("test_scope_unknown_mixed_or_changed")
    if any(row["validity"] in {"not_assessed", "undetermined"} for row in rows):
        reasons.append("validity_incomplete")
    return reasons


def _direction(value):
    return "rising" if value > 0 else "falling" if value < 0 else "stable"


def _changes(checkpoints, rows_at, context_reasons):
    changes, seen = [], {view: set() for view in ("classified_all", "classified_valid")}
    for previous, current in zip(checkpoints, checkpoints[1:]):
        left_rows, right_rows = rows_at[previous["ordinal"]], rows_at[current["ordinal"]]
        left, right = previous["population"], current["population"]
        reasons = list(context_reasons)
        if left["run_ids"] != right["run_ids"]:
            reasons.append("cohort_membership_changed")
        if any(row["assignment_status"] != "accepted" for row in left_rows + right_rows):
            reasons.append("mechanism_coverage_incomplete")
        if len(left_rows) < 2 or len(right_rows) < 2:
            reasons.append("fewer_than_two_observed_runs")
        test_reasons = _scope_reasons(left_rows + right_rows)
        views, sets = {}, {}
        for view in seen:
            a, b = left["views"][view], right["views"][view]
            seen[view].update(a["class_counts"])
            view_reasons = reasons + (test_reasons if view == "classified_valid" else [])
            views[view] = _numeric_contrast(a, b, view_reasons)
            sets[view] = _set_change(a, b, seen[view], view_reasons)
            seen[view].update(b["class_counts"])
        pass_reasons = list(context_reasons) + test_reasons
        if left["run_ids"] != right["run_ids"]:
            pass_reasons.append("cohort_membership_changed")
        if len(left_rows) < 2 or len(right_rows) < 2:
            pass_reasons.append("fewer_than_two_observed_runs")
        pass_delta = None if pass_reasons else _delta(left["observed_pass_fraction"], right["observed_pass_fraction"])
        joint_reasons = sorted(set(reasons + test_reasons))
        joint = {"status": "insufficient_comparable_evidence" if joint_reasons else "available",
                 "reasons": joint_reasons, "finite_pass_direction": None, "support_direction": None,
                 "concentration_direction": None}
        if not joint_reasons:
            delta = views["classified_all"]["later_minus_earlier"]
            joint.update(finite_pass_direction=_direction(pass_delta["numerator"]),
                         support_direction=_direction(delta["observed_support"]),
                         concentration_direction=_direction(delta["sci"]["numerator"]))
        changes.append({"from_ordinal": previous["ordinal"], "to_ordinal": current["ordinal"],
                        "earlier_run_ids": left["run_ids"], "later_run_ids": right["run_ids"],
                        "views": views, "observed_set_changes": sets,
                        "finite_pass_change": {"status": "unavailable" if pass_reasons else "available",
                                               "reasons": sorted(set(pass_reasons)), "later_minus_earlier": pass_delta,
                                               "earlier": left["observed_pass_fraction"], "later": right["observed_pass_fraction"]},
                        "joint": joint})
    return changes


def _budget_reasons(trajectories, last_ordinal):
    reasons = []
    budgets = []
    for run in trajectories:
        budget = run["budget"]
        if budget is None or any(value is None for value in budget.values()):
            reasons.append("run_budget_unknown")
        else:
            budgets.append(_fingerprint(budget))
            if last_ordinal > budget["max_revision_ordinal"]:
                reasons.append("checkpoint_exceeds_revision_budget")
        if run.get("recorded_budget_excess"):
            reasons.append("recorded_budget_exceeded")
    if len(set(budgets)) > 1:
        reasons.append("run_budget_mismatch")
    return reasons


def _cohorts(design, trajectories, config):
    ordinals = design["checkpoints"]
    if not ordinals or config is None:
        return {"status": "not_requested" if not ordinals else "unavailable",
                "reasons": ["checkpoints_not_selected"] if not ordinals else ["configuration_unknown"],
                "matched_run_ids": [], "checkpoints": [], "changes": {"available": [], "matched": []}}
    common_reasons = []
    if design["protocol_ref"] is None:
        common_reasons.append("collection_protocol_unknown")
    for key in ("model", "prompt", "settings", "selection_rule"):
        if config[key] is None:
            common_reasons.append(key + "_unknown")
    context_reasons = common_reasons + _budget_reasons(trajectories, ordinals[-1])
    cells, rows_at = {}, {}
    for ordinal in ordinals:
        cells[ordinal], rows_at[ordinal] = [], []
        for run in trajectories:
            state, row = _checkpoint_state(run, ordinal)
            cells[ordinal].append({"run_id": run["run_id"], "state": state,
                                   "revision_id": row["revision_id"] if row else None})
            if row is not None:
                rows_at[ordinal].append(row)
    matched = set.intersection(*({row["run_id"] for row in rows_at[ordinal]} for ordinal in ordinals))
    matched_rows = {ordinal: [row for row in rows_at[ordinal] if row["run_id"] in matched] for ordinal in ordinals}
    checkpoints = []
    for ordinal in ordinals:
        stopped, reached, unknown = [], [], []
        for run in trajectories:
            if run["stop_ordinal"] is not None and run["stop_ordinal"] < ordinal:
                stopped.append(run["run_id"])
            elif run["status"] == "recorded" and (run["usage"]["maximum_ordinal"] >= ordinal
                    or run["stop_ordinal"] is not None and run["stop_ordinal"] >= ordinal):
                reached.append(run["run_id"])
            else:
                unknown.append(run["run_id"])
        checkpoints.append({"ordinal": ordinal, "cells": cells[ordinal],
                            "availability_states": dict(sorted(Counter(cell["state"] for cell in cells[ordinal]).items())),
                            "risk_set": {"roster_size": len(trajectories), "known_stopped_before": stopped,
                                         "known_reached": reached, "reach_unknown": unknown,
                                         "not_known_stopped": sorted(set(reached + unknown))},
                            "available": _snapshot(rows_at[ordinal], len(trajectories)),
                            "matched": _snapshot(matched_rows[ordinal], len(matched))})
    changes = {}
    for view, populations in (("available", rows_at), ("matched", matched_rows)):
        projected = [{"ordinal": point["ordinal"], "population": point[view]} for point in checkpoints]
        members = {row["run_id"] for population in populations.values() for row in population}
        scope_reasons = common_reasons + _budget_reasons(
            [run for run in trajectories if run["run_id"] in members], ordinals[-1])
        changes[view] = _changes(projected, populations, scope_reasons)
    transition_states, transition_counts = Counter(), Counter()
    for run in trajectories:
        transition_states.update(run.get("transition_states", {}))
        for row in run.get("transition_counts", []):
            transition_counts[(row["from_class"], row["to_class"])] += row["count"]
    return {"status": "compatible_descriptive" if not context_reasons else "descriptive_only",
            "reasons": sorted(set(context_reasons)), "matched_run_ids": sorted(matched),
            "matched_exclusions": [{"run_id": run["run_id"],
                                    "missing_at": [ordinal for ordinal in ordinals if not any(
                                        row["run_id"] == run["run_id"] for row in rows_at[ordinal])]}
                                   for run in trajectories if run["run_id"] not in matched],
            "checkpoints": checkpoints, "changes": changes,
            "transition_scope": "whole_declared_paths",
            "path_transition_states": dict(sorted(transition_states.items())),
            "path_transition_counts": [{"from_class": a, "to_class": b, "count": count}
                                       for (a, b), count in sorted(transition_counts.items())]}


def analyze_trace(study_path, design_path=None):
    study, inspection = load_study(study_path)
    design_sha = None
    if design_path is None:
        design = trace_document(study, inspection)
    else:
        path = Path(design_path).absolute()
        with InputDirectory(path.parent) as directory:
            raw = directory.read(path.name, MAX_JSON)
        design, design_sha = json_bytes(raw), digest(raw)
    roster, rows, config = _validate(study, inspection, design)
    trajectories = _trajectories(study, roster, rows)
    result = {"result_schema": "structdet-code.trace-result/0.1", "software_version": __version__,
              "trace_id": design["trace_id"], "study_id": study["study_id"],
              "study_sha256": inspection["study_sha256"], "design_sha256": design_sha,
              "task": study["task"], "data_role": study["data_role"], "evidence_policy": study["evidence_policy"],
              "clock": design["clock"], "selection_rule": design["selection_rule"],
              "configuration_id": design["configuration_id"], "protocol_sha256": _fingerprint(design["protocol_ref"]),
              "condition_fingerprints": {key: _fingerprint(config[key]) if config else None
                                         for key in ("model", "prompt", "settings", "selection_rule")},
              "candidate_execution_performed": False, "provenance_authenticated": False,
              "substantive_validation_performed": False, "causal_effect_estimated": False,
              "roster": {"planned_runs": len(roster), "recorded_runs": sum(not run["missing"] for run in roster.values()),
                         "explicitly_unrecorded_runs": sorted(key for key, run in roster.items() if run["missing"]),
                         "study_runs_outside_roster": sorted(run["id"] for run in study["runs"] if run["id"] not in roster),
                         "recorded_stop_reasons": dict(sorted(Counter(run["stop_reason"] for run in trajectories
                                                                        if run["status"] == "recorded").items()))},
              "trajectories": trajectories, "cohorts": _cohorts(design, trajectories, config),
              "structural_half_life": {"status": "not_applicable", "reason": "revision_clock_is_not_recursive_training"},
              "external_recovery_rate": {"status": "not_estimated", "reason": "observed_reappearance_does_not_establish_external_recovery"},
              "limitations": [
                  "Trajectories retain actual revision ordinals; test-only evidence and assignment versions add no code generations.",
                  "Selected paths are supplied branch decisions. Missing ancestry and ordinal gaps do not become supported adjacent switches.",
                  "Checkpoint selection is exact: no stopped endpoint, absent revision or passing receipt is carried forward.",
                  "Available cases can change with stopping and missingness; matched cases retain the same observed runs at every selected checkpoint.",
                  "Matched observation membership does not remove success-dependent selection or establish independent samples.",
                  "Numeric trends require known compatible context and complete mechanism coverage; finite-pass trends also require a common known test scope.",
                  "A single admitted observation has no population concentration result in trace output.",
                  "Supplied budget, stopping, feedback and execution records are not authenticated; absent events remain unknown.",
                  "Observed sets and reappearance concern these records, with no inference of general capacity loss, external recovery or causal effects.",
              ]}
    require(len(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False).encode()) <= MAX_RESULT,
            "trace_result_size_limit")
    return result
