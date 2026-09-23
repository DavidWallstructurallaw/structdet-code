"""Readable rendering of the canonical inspection result."""


def markdown(result: dict) -> str:
    ledger = result["ledger"]
    lines = ["# StructDet Code inspection", "", f"Study: `{result['study_id']}`",
             f"Material: `{result['data_role']}`. Claim scope: `{result['claim_scope']}`.", "",
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
              "Validity: " + ", ".join(f"{k}={v}" for k, v in ledger["validity_states"].items()) + ".", "",
              "## Selected records", "", "| Revision | Assignment | Mechanism label | Validity |",
              "| --- | --- | --- | --- |"]
    for row in result["selected_observations"]:
        lines.append(f"| {row['revision_id']} | {row['assignment_status']} "
                     f"| {row['proposed_or_accepted_class'] or 'unresolved'} | {row['validity']} |")
    lines += ["", "## What this result supports", "",
              "The two distributions summarize explicitly selected observations with admitted supplied labels. "
              "Proposed and unresolved labels contribute to coverage accounting only. "
              "The valid view additionally requires a complete passing receipt and supplied passing conformance review.", ""]
    lines += ["- " + limitation for limitation in result["limitations"]]
    return "\n".join(lines) + "\n"
