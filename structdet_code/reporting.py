"""Readable rendering of the canonical inspection result."""


def markdown(result: dict) -> str:
    ledger = result["ledger"]
    lines = ["# StructDet Code inspection", "", f"Study: `{result['study_id']}`",
             f"Material: `{result['data_role']}`. Claim scope: `{result['claim_scope']}`.",
             f"Evidence policy: `{result['evidence_policy']}`.", "",
             f"Selected observations: {ledger['selected_observations']}. "
             f"Recorded runs: {ledger['recorded_runs']}. "
             f"Recorded revisions: {ledger['recorded_revisions']}.", "",
             "| View | Classified n | Mechanisms | SCI | Gini-Simpson |",
             "| --- | ---: | ---: | ---: | ---: |"]
    for name, view in result["views"].items():
        def number(key):
            v = view[key]
            return (f"{v['numerator']}/{v['denominator']}" if v["status"] == "available"
                    else "undefined (empty)")
        lines.append(f"| {name} | {view['population_size']} | {view['observed_support']} "
                     f"| {number('sci')} | {number('gini_simpson')} |")
    lines += ["", "Assignment coverage: " + ", ".join(f"{k}={v}" for k, v in ledger["assignment_states"].items()) + ".",
              "Validity: " + ", ".join(f"{k}={v}" for k, v in ledger["validity_states"].items()) + "."]
    coverage = ledger["classification_coverage"]
    recognition = ledger["recognizer_coverage"]
    lines += [f"Admitted coverage: {coverage['admitted']}/{coverage['selected']} selected observations. "
              f"Rule matches: {recognition['recognized']}/{recognition['sources']} source records.",
              "Admitted bases: " + (", ".join(f"{k}={v}" for k, v in ledger["admitted_bases"].items()) or "none") + ".",
              "Unadmitted reasons: " + (", ".join(f"{k}={v}" for k, v in ledger["unadmitted_reasons"].items()) or "none") + ".", "",
              "## Mechanism distribution", "", "| Mechanism | All admitted | Valid admitted |",
              "| --- | ---: | ---: |"]
    all_counts = result["views"]["classified_all"]["class_counts"]
    valid_counts = result["views"]["classified_valid"]["class_counts"]
    for key in sorted(all_counts):
        lines.append(f"| {key} | {all_counts[key]} | {valid_counts.get(key, 0)} |")
    if not all_counts:
        lines.append("| No admitted mechanisms | 0 | 0 |")
    lines += ["",
              "## Selected records", "", "| Revision | Artifact | Assignment | Basis | Mechanism label | Validity |",
              "| --- | --- | --- | --- | --- | --- |"]
    for row in result["selected_observations"]:
        lines.append(f"| {row['revision_id']} | {row['artifact_id']} | {row['assignment_status']} "
                     f"| {row['classification_basis'] or 'none'} "
                     f"| {row['proposed_or_accepted_class'] or 'unresolved'} | {row['validity']} |")
    lines += ["", "## Static evidence and review needs", "",
              "These observations cover syntax, including potentially inactive code. Only a complete rule match admits a static label.", "",
              "| Artifact | Source SHA-256 | Rule or review reason | Evidence lines |",
              "| --- | --- | --- | --- |"]
    for row in result["source_analysis"]:
        anchors = ", ".join(dict.fromkeys(f"{a['start_line']}-{a['end_line']}" for a in row["evidence"]))
        lines.append(f"| {row['artifact_id']} | `{row['source_sha256']}` "
                     f"| {row['rule_id'] or row['reason']} | {anchors or 'review required'} |")
    lines += ["", "## What this result supports", "",
              "The two distributions summarize explicitly selected observations under the named evidence policy. "
              "Proposed and unresolved labels contribute to coverage accounting only. "
              "The valid view additionally requires a complete passing receipt and supplied passing conformance review.", ""]
    lines += ["- " + limitation for limitation in result["limitations"]]
    return "\n".join(lines) + "\n"
