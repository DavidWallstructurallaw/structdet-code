"""Passive, task-bound descriptive comparisons with explicit fixed-prefix slots."""

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

from . import __version__
from .errors import require
from .io import InputDirectory, MAX_JSON, digest, json_bytes
from .metrics import count_metrics
from .study import enum, fields, identifier, integer, load_study, text
from .workflow import _write_new, encoded

SCHEMA = "structdet-code.comparison/0.1"
CONDITIONS = ("model", "prompt", "settings")


def _fingerprint(value):
    if value is None:
        return None
    return digest(json.dumps(value, sort_keys=True, ensure_ascii=True,
                             allow_nan=False, separators=(",", ":")).encode())


def _template_side(study, result):
    runs = {item["id"]: item for item in study["runs"]}
    configurations = {runs[row["run_id"]]["configuration_id"]
                      for row in result["selected_observations"]}
    return {"study_sha256": result["study_sha256"],
            "configuration_id": next(iter(configurations)) if len(configurations) == 1 else None,
            "planned_positions": None, "budget_per_slot": None,
            "slots": [{"position": None, "revision_id": row["revision_id"]}
                      for row in result["selected_observations"]]}


def comparison_document(left, left_result, right, right_result):
    return {"schema_version": SCHEMA, "comparison_id": "condition-comparison",
            "varied_field": None, "protocol_ref": None, "prefix_size": None,
            "selection_rule": "fixed_prefix/0.1",
            "left": _template_side(left, left_result),
            "right": _template_side(right, right_result)}


def prepare_comparison(left_path, right_path, output):
    left, left_result = load_study(left_path)
    right, right_result = load_study(right_path)
    document = comparison_document(left, left_result, right, right_result)
    _write_new(Path(output).absolute(), encoded(document))
    return {"status": "comparison_template_created", "schema_version": SCHEMA,
            "candidate_execution_performed": False}


def _fraction(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "value": numerator / denominator if denominator else None}


def _population(rows, requested=None):
    admitted = [row for row in rows if row["assignment_status"] == "accepted"]
    passed = [row for row in rows if row["validity"] == "passed_under_supplied_scope"]
    valid = [row for row in admitted if row["validity"] == "passed_under_supplied_scope"]
    def view(population):
        return count_metrics(Counter(row["proposed_or_accepted_class"] for row in population),
                             len(population))
    return {"observed": len(rows), "requested_slots": requested,
            "unique_source_bytes": len({row["source_sha256"] for row in rows}),
            "declared_root_groups": dict(sorted(Counter(row["root_group_id"] for row in rows
                                                        if row["root_group_id"] is not None).items())),
            "unknown_root_groups": sum(row["root_group_id"] is None for row in rows),
            "classification_coverage_observed": _fraction(len(admitted), len(rows)),
            "classification_coverage_requested": _fraction(len(admitted), requested) if requested else None,
            "observed_pass_fraction": _fraction(len(passed), len(rows)),
            "observed_pass_coverage_requested": _fraction(len(passed), requested) if requested else None,
            "validity_states": dict(sorted(Counter(row["validity"] for row in rows).items())),
            "assignment_states": dict(sorted(Counter(row["assignment_status"] for row in rows).items())),
            "admitted_bases": dict(sorted(Counter(row["classification_basis"] for row in admitted).items())),
            "unadmitted_reasons": dict(sorted(Counter(row["reason"] for row in rows
                                                       if row["assignment_status"] != "accepted").items())),
            "views": {"classified_all": view(admitted), "classified_valid": view(valid)}}


def _side(study, result, design, prefix):
    fields(design, "study_sha256 configuration_id planned_positions budget_per_slot slots")
    require(design["study_sha256"] == result["study_sha256"], "comparison_study_binding_mismatch")
    configs = {item["id"]: item for item in study["configurations"]}
    config_id = design["configuration_id"]
    if config_id is not None:
        identifier(config_id)
        require(config_id in configs, "comparison_configuration_missing")
    config = configs.get(config_id)
    planned, budget = design["planned_positions"], design["budget_per_slot"]
    if planned is not None:
        integer(planned, 1, 10000)
    if budget is not None:
        fields(budget, "unit limit")
        enum(budget["unit"], {"attempts", "model_calls", "generated_tokens", "wall_seconds"})
        integer(budget["limit"], 1, 1_000_000_000)
    runs = {item["id"]: item for item in study["runs"]}
    revisions = {item["id"]: item for item in study["revisions"]}
    artifacts = {item["id"]: item for item in study["artifacts"]}
    rows = {row["revision_id"]: {**row,
            "root_group_id": runs[row["run_id"]]["root_group_id"],
            "stop_reason": runs[row["run_id"]]["stop_reason"],
            "revision_ordinal": revisions[row["revision_id"]]["ordinal"],
            "artifact_origin": artifacts[row["artifact_id"]]["origin"]}
            for row in result["selected_observations"]
            if config is None or runs[row["run_id"]]["configuration_id"] == config_id}
    slots = design["slots"]
    require(isinstance(slots, list) and len(slots) <= 256, "comparison_slot_limit")
    positioned, mapped = {}, set()
    unknown_position = False
    for slot in slots:
        fields(slot, "position revision_id")
        position, revision = slot["position"], slot["revision_id"]
        if position is None:
            unknown_position = True
        else:
            integer(position, 1, 10000)
            require(planned is None or position <= planned, "slot_outside_planned_positions")
            require(position not in positioned, "duplicate_comparison_position")
            positioned[position] = revision
        if revision is not None:
            identifier(revision)
            require(revision in rows, "comparison_revision_not_selected_in_configuration")
            require(revision not in mapped, "duplicate_comparison_revision")
            mapped.add(revision)
    reasons = []
    if config is None:
        reasons.append("configuration_unknown")
    if planned is None:
        reasons.append("planned_positions_unknown")
    elif prefix is not None and planned < prefix:
        reasons.append("prefix_exceeds_planned_positions")
    if prefix is None:
        reasons.append("prefix_size_unknown")
    if unknown_position:
        reasons.append("slot_positions_unknown")
    if mapped != rows.keys():
        reasons.append("selected_revisions_unmapped")
    if prefix is not None and not set(range(1, prefix + 1)) <= positioned.keys():
        reasons.append("prefix_positions_unaccounted")
    prefix_rows, missing, excluded = [], [], []
    if not reasons:
        for position in range(1, prefix + 1):
            revision = positioned[position]
            if revision is None:
                missing.append(position)
            else:
                prefix_rows.append({"position": position, **rows[revision]})
        excluded = [{"position": position, "revision_id": revision}
                    for position, revision in sorted(positioned.items())
                    if position > prefix and revision is not None]
    scopes, without_receipt = {}, 0
    receipts = {item["id"]: item for item in study["receipts"]}
    suites = {item["id"]: item for item in study["suites"]}
    for row in prefix_rows:
        receipt = receipts.get(row["receipt_id"])
        if receipt is None:
            without_receipt += 1
            continue
        scope = {"suite_sha256": receipt["suite_sha256"],
                 "oracle_id": suites[receipt["suite_id"]]["oracle_id"],
                 "environment_sha256": _fingerprint(receipt["environment"]),
                 "execution_basis": receipt["execution_basis"]}
        scopes[_fingerprint(scope)] = scope
    public = {"study_id": result["study_id"], "study_sha256": result["study_sha256"],
              "task": result["task"], "data_role": result["data_role"],
              "evidence_policy": result["evidence_policy"], "configuration_id": config_id,
              "condition_fingerprints": {key: _fingerprint(config[key]) if config else None
                                         for key in CONDITIONS + ("selection_rule",)},
              "planned_positions": planned, "budget_per_slot": budget,
              "study_selected_count": len(result["selected_observations"]),
              "inventory_scope": "selected_configuration" if config else "all_selected_configurations",
              "configuration_inventory": _population(list(rows.values())),
              "prefix_status": "available" if not reasons else "unavailable",
              "prefix_reasons": reasons, "missing_positions": missing,
              "excluded_later_selected": excluded,
              "prefix_population": _population(prefix_rows, prefix) if not reasons else None,
              "prefix_observations": prefix_rows,
              "test_scopes": [{"scope_sha256": key, **value} for key, value in sorted(scopes.items())],
              "observed_without_receipt": without_receipt if not reasons else None}
    return public, config


def _contrast(left, right, view, reasons):
    reasons = list(reasons)
    if not reasons:
        a = left["prefix_population"]["views"][view]
        b = right["prefix_population"]["views"][view]
        if not a["population_size"] or not b["population_size"]:
            reasons.append("empty_classified_population")
    if reasons:
        return {"status": "unavailable", "reasons": reasons, "right_minus_left": None}
    deltas = {"observed_support": b["observed_support"] - a["observed_support"]}
    for metric in ("sci", "gini_simpson"):
        difference = (Fraction(b[metric]["numerator"], b[metric]["denominator"])
                      - Fraction(a[metric]["numerator"], a[metric]["denominator"]))
        deltas[metric] = _fraction(difference.numerator, difference.denominator)
    return {"status": "available", "reasons": [], "right_minus_left": deltas,
            "left_population": a["population_size"], "right_population": b["population_size"]}


def compare_studies(left_path, right_path, design_path=None):
    left_study, left_result = load_study(left_path)
    right_study, right_result = load_study(right_path)
    design_sha = None
    if design_path is None:
        design = comparison_document(left_study, left_result, right_study, right_result)
    else:
        path = Path(design_path).absolute()
        with InputDirectory(path.parent) as directory:
            data = directory.read(path.name, MAX_JSON)
        design, design_sha = json_bytes(data), digest(data)
    fields(design, "schema_version comparison_id varied_field protocol_ref prefix_size selection_rule left right")
    require(design["schema_version"] == SCHEMA, "unsupported_comparison_schema")
    identifier(design["comparison_id"])
    varied, protocol, prefix = design["varied_field"], design["protocol_ref"], design["prefix_size"]
    if varied is not None:
        enum(varied, CONDITIONS)
    text(protocol, nullable=True)
    if prefix is not None:
        integer(prefix, 1, 128)
    require(design["selection_rule"] == "fixed_prefix/0.1", "unsupported_comparison_selection")
    left, left_config = _side(left_study, left_result, design["left"], prefix)
    right, right_config = _side(right_study, right_result, design["right"], prefix)
    reasons = []
    for key in ("task", "data_role", "evidence_policy"):
        if left[key] != right[key]:
            reasons.append(key + "_mismatch")
    if varied is None:
        reasons.append("varied_field_unknown")
    if protocol is None:
        reasons.append("collection_protocol_unknown")
    for name, side in (("left", left), ("right", right)):
        reasons.extend(name + ":" + reason for reason in side["prefix_reasons"])
        if side["budget_per_slot"] is None:
            reasons.append(name + ":budget_unknown")
        for key, value in side["condition_fingerprints"].items():
            if value is None:
                reasons.append(name + ":" + key + "_unknown")
    if (left["budget_per_slot"] is not None and right["budget_per_slot"] is not None
            and left["budget_per_slot"] != right["budget_per_slot"]):
        reasons.append("budget_mismatch")
    if left_config is not None and right_config is not None:
        for key in CONDITIONS + ("selection_rule",):
            a, b = left["condition_fingerprints"][key], right["condition_fingerprints"][key]
            if a is None or b is None:
                continue
            if key == varied:
                if a == b:
                    reasons.append("varied_field_unchanged")
            elif a != b:
                reasons.append("control_mismatch:" + key)
    validity_reasons = list(reasons)
    if not reasons:
        if left["observed_without_receipt"] or right["observed_without_receipt"]:
            validity_reasons.append("observed_test_receipts_missing")
        if (len(left["test_scopes"]) != 1 or len(right["test_scopes"]) != 1
                or left["test_scopes"] != right["test_scopes"]):
            validity_reasons.append("test_scope_unknown_mixed_or_changed")
    shared = sorted({row["source_sha256"] for row in left["prefix_observations"]}
                    & {row["source_sha256"] for row in right["prefix_observations"]})
    return {"result_schema": "structdet-code.comparison-result/0.1", "software_version": __version__,
            "comparison_id": design["comparison_id"], "design_sha256": design_sha,
            "status": "descriptive_only" if reasons else "compatible_descriptive",
            "compatibility_reasons": reasons, "varied_field": varied,
            "protocol_sha256": _fingerprint(protocol), "selection_rule": design["selection_rule"],
            "prefix_size": prefix, "candidate_execution_performed": False,
            "provenance_authenticated": False, "causal_effect_estimated": False,
            "left": left, "right": right, "shared_prefix_source_sha256": shared,
            "contrasts": {"classified_all": _contrast(left, right, "classified_all", reasons),
                          "classified_valid": _contrast(left, right, "classified_valid", validity_reasons)},
            "limitations": [
                "Condition, budget and slot records are supplied claims; their provenance is not authenticated.",
                "Deltas describe admitted populations under the supplied fixed-prefix design; coverage can differ.",
                "Missing outputs retain their positions; observed failures are kept; later outputs never backfill.",
                "Finite-test comparisons require one common supplied suite, oracle, environment and execution basis.",
                "Source overlap is disclosed; distinct bytes or run IDs do not establish independent samples.",
                "No causal effect, population uncertainty, general model capacity or degradation is estimated.",
            ]}


def comparison_markdown(result):
    """Render only the canonical result; never recompute comparisons in prose."""
    lines = ["# StructDet Code condition comparison", "", f"Status: `{result['status']}`.", "",
             f"Selection: `{result['selection_rule']}`; requested prefix: `{result['prefix_size']}`.", "",
             "All differences below are right minus left. Counts refer to admitted mechanism labels.", "",
             "| Side | Material | Prefix observed / requested | Missing positions | Excluded later | Classified | Finite passed |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for name in ("left", "right"):
        side = result[name]
        population = side["prefix_population"]
        if population is None:
            observed = admitted = passed = "unavailable"
        else:
            observed = f"{population['observed']} / {population['requested_slots']}"
            admitted = str(population["classification_coverage_observed"]["numerator"])
            passed = str(population["observed_pass_fraction"]["numerator"])
        missing = (", ".join(map(str, side["missing_positions"])) or "none") if population else "unknown"
        lines.append(f"| {name}: `{side['study_id']}` | {side['data_role']} | {observed} | {missing} | "
                     f"{len(side['excluded_later_selected']) if population else 'unknown'} | {admitted} | {passed} |")
    if result["compatibility_reasons"]:
        lines += ["", "Comparison prerequisites:", ""]
        lines += [f"- `{reason}`" for reason in result["compatibility_reasons"]]
    for name in ("left", "right"):
        side = result[name]
        lines += ["", f"## {name}: `{side['study_id']}`", "",
                  f"Task: `{side['task']['pack_id']}`; frame: `{side['task']['pack_sha256']}`.", "",
                  f"Study: `{side['study_sha256']}`; configuration: `{side['configuration_id']}`.", "",
                  f"Planned positions: `{side['planned_positions']}`; per-slot budget: `{side['budget_per_slot']}`.", ""]
        population = side["prefix_population"] or side["configuration_inventory"]
        lines += ["Population: " + ("fixed prefix." if side["prefix_population"] else
                  f"inventory ({side['inventory_scope']}); prefix unavailable."), "",
                  f"Validity states: `{population['validity_states']}`; admitted bases: `{population['admitted_bases']}`.", "",
                  f"Unadmitted reasons: `{population['unadmitted_reasons']}`.", "",
                  f"Declared root groups: `{population['declared_root_groups']}`; unknown: {population['unknown_root_groups']}.", ""]
        for view, metrics in population["views"].items():
            sci = metrics["sci"]
            value = f"{sci['numerator']}/{sci['denominator']}" if sci["status"] == "available" else "undefined"
            lines.append(f"- `{view}`: n={metrics['population_size']}; counts `{metrics['class_counts']}`; "
                         f"support={metrics['observed_support']}; SCI={value}.")
        if side["prefix_observations"]:
            lines += ["", "| Position | Revision | Class / state | Validity | Receipt | Source SHA-256 |",
                      "| --- | --- | --- | --- | --- | --- |"]
            for row in side["prefix_observations"]:
                label = row["proposed_or_accepted_class"] if row["assignment_status"] == "accepted" else row["assignment_status"]
                lines.append(f"| {row['position']} | `{row['revision_id']}` | `{label}` | {row['validity']} | "
                             f"`{row['receipt_id']}` | `{row['source_sha256']}` |")
        lines += ["", f"Test scopes: `{side['test_scopes']}`.", "",
                  f"Excluded later selected records: `{side['excluded_later_selected']}`."]
    lines += ["", "## Conditional descriptive differences", ""]
    for view, contrast in result["contrasts"].items():
        if contrast["status"] != "available":
            lines.append(f"- `{view}`: unavailable; `{contrast['reasons']}`.")
        else:
            delta = contrast["right_minus_left"]
            sci = delta["sci"]
            gini = delta["gini_simpson"]
            lines.append(f"- `{view}`: left n={contrast['left_population']}, right n={contrast['right_population']}; "
                         f"support delta={delta['observed_support']}; SCI delta={sci['numerator']}/{sci['denominator']}; "
                         f"Gini-Simpson delta={gini['numerator']}/{gini['denominator']}.")
    lines += ["", f"Shared source digests in the two prefixes: {len(result['shared_prefix_source_sha256'])}.", "",
              "## Limits", ""] + ["- " + item for item in result["limitations"]]
    return "\n".join(lines) + "\n"
