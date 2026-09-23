"""Readable rendering of the canonical trajectory and cohort result."""


def _number(value):
    if value.get("status") in {"undefined", "not_applicable"}:
        return value["reason"]
    if value["denominator"] == 0:
        return "undefined"
    return f"{value['numerator']}/{value['denominator']}"


def trace_markdown(result):
    cohorts = result["cohorts"]
    roster = result["roster"]
    lines = ["# StructDet Code revision trace", "",
             f"Study: `{result['study_id']}`; trace: `{result['trace_id']}`; material: `{result['data_role']}`.", "",
             f"Task: `{result['task']['pack_id']}`; evidence policy: `{result['evidence_policy']}`.", "",
             f"Clock: `{result['clock']}`; selection: `{result['selection_rule']}`.", "",
             f"Roster: {roster['planned_runs']} runs; {roster['recorded_runs']} recorded. "
             f"Explicitly unrecorded: `{roster['explicitly_unrecorded_runs']}`.", "",
             f"Cohort status: `{cohorts['status']}`; reasons: `{cohorts['reasons']}`.", "",
             f"Matched across every requested checkpoint: `{cohorts['matched_run_ids']}`.", "",
             f"Recorded stopping reasons: `{roster['recorded_stop_reasons']}`. "
             f"Study runs outside this roster: `{roster['study_runs_outside_roster']}`."]
    if cohorts["checkpoints"]:
        lines += ["", "## Checkpoint populations", "",
                  "Available cases retain each recorded observation at that ordinal. Matched cases retain the same run IDs at every selected checkpoint.", "",
                  "| Ordinal | Cohort | Observed / roster | Admitted | Finite passed / observed | Support | SCI | Valid admitted | Valid SCI |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for point in cohorts["checkpoints"]:
            for name in ("available", "matched"):
                population = point[name]
                all_view, valid = population["views"]["classified_all"], population["views"]["classified_valid"]
                lines.append(f"| {point['ordinal']} | {name} | {population['observed']} / {population['requested_slots']} "
                             f"| {all_view['population_size']} | {_number(population['observed_pass_fraction'])} "
                             f"| {all_view['observed_support']} | {_number(all_view['sci'])} "
                             f"| {valid['population_size']} | {_number(valid['sci'])} |")
        lines += ["", "Missing outputs are not failed tests. Single-observation concentration is not applicable.", "",
                  f"Whole declared-path transition states: `{cohorts['path_transition_states']}`; "
                  f"supported adjacent counts: `{cohorts['path_transition_counts']}`.", "",
                  "## Changes and joint outcomes", "",
                  "All numeric differences are later minus earlier, qualified by the recorded cohort and evidence."]
        for cohort, changes in cohorts["changes"].items():
            for change in changes:
                lines += ["", f"### {cohort}: {change['from_ordinal']} to {change['to_ordinal']}", "",
                          f"Earlier runs: `{change['earlier_run_ids']}`; later runs: `{change['later_run_ids']}`.", ""]
                for view, contrast in change["views"].items():
                    if contrast["status"] == "available":
                        delta = contrast["later_minus_earlier"]
                        lines.append(f"- `{view}`: n={contrast['earlier_population']} to {contrast['later_population']}; "
                                     f"support delta={delta['observed_support']}; SCI delta={_number(delta['sci'])}; "
                                     f"Gini-Simpson delta={_number(delta['gini_simpson'])}.")
                    else:
                        lines.append(f"- `{view}`: unavailable; `{contrast['reasons']}`.")
                passed = change["finite_pass_change"]
                lines.append(f"- Finite pass fraction: {_number(passed['earlier'])} to {_number(passed['later'])}; "
                             + (f"delta={_number(passed['later_minus_earlier'])}." if passed["status"] == "available"
                                else f"comparison unavailable; `{passed['reasons']}`."))
                joint = change["joint"]
                if joint["status"] == "available":
                    lines += ["", f"Joint observation: finite passing {joint['finite_pass_direction']}; "
                              f"support {joint['support_direction']}; concentration {joint['concentration_direction']}."]
                else:
                    lines += ["", f"Joint observation: `{joint['status']}`; `{joint['reasons']}`."]
                for view, change_sets in change["observed_set_changes"].items():
                    lines += ["", f"`{view}` sets ({change_sets['status']}): retained `{change_sets['retained']}`; "
                              f"no longer observed `{change_sets['no_longer_observed']}`; "
                              f"first observed `{change_sets['first_observed']}`; observed again `{change_sets['observed_again']}`; "
                              f"retained/reference={_number(change_sets['retention_fraction'])}. "
                              f"Qualifiers: `{change_sets['qualifiers']}`."]
        lines += ["", "## Missingness, risk sets and coverage", ""]
        for point in cohorts["checkpoints"]:
            risk = point["risk_set"]
            lines += [f"### Ordinal {point['ordinal']}", "",
                      f"Availability: `{point['availability_states']}`.", "",
                      f"Known stopped before this ordinal: `{risk['known_stopped_before']}`; "
                      f"known reached: `{risk['known_reached']}`; reach unknown: `{risk['reach_unknown']}`.", "",
                      "| Run | State | Selected revision |", "| --- | --- | --- |"]
            for cell in point["cells"]:
                lines.append(f"| {cell['run_id']} | {cell['state']} | {cell['revision_id'] or 'none'} |")
            for name in ("available", "matched"):
                population = point[name]
                lines += ["", f"{name}: class counts `{population['views']['classified_all']['class_counts']}`; "
                          f"valid counts `{population['views']['classified_valid']['class_counts']}`; "
                          f"validity `{population['validity_states']}`; "
                          f"unadmitted `{population['unadmitted_reasons']}`.", "",
                          f"Classification coverage observed={_number(population['classification_coverage_observed'])}; "
                          f"declared root groups `{population['declared_root_groups']}`; "
                          f"unknown roots={population['unknown_root_groups']}.", ""]
    lines += ["", "## Per-run trajectories", "",
              "Rows follow supplied revision ordinals. Parent links determine lineage; sibling rows alone do not establish a mechanism transition. "
              "Repeated test receipts remain attached to their revision; their within-revision chronological order is unspecified."]
    scopes = {}
    for run in result["trajectories"]:
        lines += ["", f"### Run `{run['run_id']}`", ""]
        if run["status"] == "unrecorded":
            lines += [f"Explicitly unrecorded run. Supplied budget: `{run['budget']}`."]
            continue
        lines += [f"Configuration: `{run['configuration_id']}`; root group: `{run['root_group_id']}`.", "",
                  f"Stop: `{run['stop_reason']}` at supplied ordinal `{run['stop_ordinal']}`; "
                  f"selected endpoint: `{run['endpoint_revision_id']}`.", "",
                  f"Selected path: `{run['selected_path']}`; excluded revisions: `{run['excluded_revision_ids']}`.", "",
                  f"Budget: `{run['budget']}`; recorded usage: `{run['usage']}`; "
                  f"recorded excess: `{run['recorded_budget_excess']}`.", "",
                  "| Ordinal | Revision / kind | Parents | Admitted class / state | Finite validity / receipt | Received feedback |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for row in run["revisions"]:
            cls = row["proposed_or_accepted_class"] if row["assignment_status"] == "accepted" else row["assignment_status"]
            lines.append(f"| {row['ordinal']} | {row['revision_id']} / {row['kind']} | {', '.join(row['parents']) or 'none'} "
                         f"| {cls} | {row['validity']} / {row['receipt_id'] or 'none'} | {', '.join(row['feedback_ids']) or 'none'} |")
        lines += ["", f"Ordinal gaps: `{run['ordinal_gaps']}`; transition states: `{run['transition_states']}`.", "",
                  "Supported adjacent selected-path transition counts: " + f"`{run['transition_counts']}`.", ""]
        for edge in run["path_transitions"]:
            lines.append(f"- {edge['from_revision']} ({edge['from_class']}) to {edge['to_revision']} ({edge['to_class']}): "
                         f"`{edge['state']}`; source changed={edge['source_changed']}; test scope changed={edge['test_scope_changed']}.")
        if run["path_transitions"]:
            lines.append("")
        for row in run["revisions"]:
            spans = ", ".join(dict.fromkeys(f"{a['start_line']}-{a['end_line']}" for a in row["source_anchors"])) or "none"
            lines += [f"`{row['revision_id']}`: artifact `{row['artifact_id']}`, source `{row['source_sha256']}`; "
                      f"assignment `{row['assignment_id']}`, basis `{row['classification_basis']}`, evidence lines {spans}; "
                      f"missing parents `{row['missing_parents']}`.", ""]
            for receipt in row["test_observations"]:
                scope = receipt["test_scope"]
                scopes[scope["scope_sha256"]] = scope
                lines.append(f"- Receipt `{receipt['id']}`: {receipt['status']}; attempted/completed/passed="
                             f"{receipt['attempted']}/{receipt['completed']}/{receipt['passed']}; "
                             f"visibility={receipt['visibility']}; selected={receipt['selected']}; scope `{scope['scope_sha256']}`.")
            for event in row["feedback_examining_revision"]:
                lines.append(f"- Feedback `{event['id']}`: {event['kind']}, receipt `{event['receipt_id']}`, "
                             f"visible={event['visible_to_agent']}, received by `{event['received_by']}`.")
            lines.append("")
    if scopes:
        lines += ["## Test scope identities", "",
                  "| Scope | Suite SHA-256 | Oracle | Environment fingerprint | Basis | Visibility |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for identity, scope in sorted(scopes.items()):
            lines.append(f"| `{identity}` | `{scope['suite_sha256']}` | {scope['oracle_id']} | "
                         f"`{scope['environment_sha256']}` | {scope['execution_basis']} | {scope['visibility']} |")
    lines += ["", "## What this result supports", "",
              "This report describes source-bound revision histories and conditional distributions over the named run roster. "
              "The joint outcomes preserve both finite correctness and mechanism changes, with missing prerequisites beside unavailable comparisons.", "",
              f"Study binding: `{result['study_sha256']}`; design binding: `{result['design_sha256']}`; "
              f"task binding: `{result['task']['pack_sha256']}`.", "",
              f"Structural Half-Life: `{result['structural_half_life']['status']}`. "
              f"External Recovery Rate: `{result['external_recovery_rate']['status']}`.", ""]
    lines += ["- " + item for item in result["limitations"]]
    return "\n".join(lines) + "\n"
