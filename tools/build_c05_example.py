"""Regenerate the fixed owned intervention example, never execute input files."""

from copy import deepcopy
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from structdet_code.evidence import evidence_document
from structdet_code.graph_rules import RULES
from structdet_code.io import digest
from structdet_code.study import SCHEMA, load_study, task_pack
from structdet_code.trace import trace_document
from structdet_code.workflow import encoded
from tools.build_graph_example import distance_oracle, graph_inputs


def build_example(destination):
    destination = Path(destination)
    (destination / "sources").mkdir(parents=True, exist_ok=True)
    (destination / "materials").mkdir(exist_ok=True)
    rules = {key: source for key, _, _, source in RULES}
    programs = {
        "fifo_good": ("DIST-FIFO", rules["dist-fifo-first-discovery/1"]),
        "fifo_bad": ("DIST-FIFO", rules["dist-fifo-step-defect/1"]),
        "relax_good": ("DIST-RELAX", rules["dist-complete-edge-passes/1"]),
        "relax_bad": ("DIST-RELAX", rules["dist-complete-edge-passes/1"].replace(
            "distances[source] + 1", "distances[source] + 2")),
    }
    histories = {"I1": ["relax_good", "fifo_good", "relax_good"],
                 "I2": ["relax_bad", "fifo_bad", "relax_good"]}
    task, pack_sha = task_pack("unit-graph-distances")
    suite = {"schema_version": "structdet-code.graph-suite/0.1", "oracle_id": "unit-distance-properties/0.1",
             "cases": [{"id": f"T{index:02}", "input": graph} for index, graph in enumerate(graph_inputs(), 1)]}
    suite_raw = encoded(suite)
    (destination / "suite.json").write_bytes(suite_raw)
    study = {"schema_version": SCHEMA, "study_id": "owned-intervention-example",
             "data_role": "fixture", "evidence_policy": "fixture_only",
             "task": {key: task[key] for key in ("pack_id", "pack_version", "resolution_id")},
             "configurations": [{"id": "fixture", "model": "project-owned-no-model-calls",
                                 "prompt": "Return minimum hop distances for a directed unit graph.",
                                 "settings": {"material": "designed_fixture", "sampling_performed": False},
                                 "selection_rule": "Complete declared paths at ordinals 0, 1, 2."}],
             "artifacts": [], "assignments": [], "suites": [
                 {"id": "suite", "path": "suite.json", "sha256": digest(suite_raw), "oracle_id": suite["oracle_id"]}],
             "receipts": [], "runs": [], "revisions": [], "feedback": [], "selection": []}
    study["task"]["pack_sha256"] = pack_sha
    functions, artifacts, details = {}, {}, []
    for name, (cls, source) in programs.items():
        raw = source.encode()
        (destination / "sources" / (name + ".py")).write_bytes(raw)
        artifact = {"id": name, "path": "sources/" + name + ".py", "sha256": digest(raw),
                    "language": "python", "entry_point": task["entry_point"],
                    "origin": "project_fixture", "capture_status": "complete"}
        study["artifacts"].append(artifact)
        artifacts[name] = artifact
        study["assignments"].append({
            "id": "M-" + name, "artifact_id": name, "source_sha256": digest(raw), "pack_sha256": pack_sha,
            "revision": 1, "status": "accepted", "basis": "fixture", "class_id": cls,
            "reason": None, "reviewer_ref": None,
            "evidence": [{"start_line": 1, "end_line": len(source.splitlines()),
                          "note": "Reviewed owned propagation schedule; increment defect retains the mechanism."}]})
        namespace = {}
        exec(compile(source, "<owned-c05-reference>", "exec"), namespace)
        functions[name] = namespace["shortest_distances"]
    for run, names in histories.items():
        study["runs"].append({"id": run, "configuration_id": "fixture", "root_group_id": "G-owned-fixtures",
                              "stop_reason": "budget", "endpoint_revision_id": run + "-V2"})
        for ordinal, name in enumerate(names):
            revision = f"{run}-V{ordinal}"
            parent = f"{run}-V{ordinal-1}" if ordinal else None
            study["revisions"].append({"id": revision, "run_id": run, "ordinal": ordinal,
                                      "artifact_id": name, "parents": [parent] if parent else [],
                                      "missing_parents": [], "kind": "edit" if parent else "generation",
                                      "feedback_ids": ["F-" + parent] if parent else []})
            for prefix, visibility in (("E-", "withheld"), ("T-", "feedback")):
                if prefix == "T-" and ordinal == 2:
                    continue
                outcomes = []
                for case in suite["cases"]:
                    graph = case["input"]
                    edges = deepcopy(graph["edges"])
                    output = functions[name](graph["node_count"], edges, graph["start"])
                    checks = {
                        "plain_distance_list": type(output) is list and len(output) == graph["node_count"]
                        and all(v is None or type(v) is int and v >= 0 for v in output),
                        "new_list": output is not edges and all(output is not edge for edge in edges),
                        "minimum_hop_distances": output == distance_oracle(**graph),
                        "input_unchanged": edges == graph["edges"]}
                    outcomes.append({"case_id": case["id"], "passed": all(checks.values()), "checks": checks})
                passed = sum(o["passed"] for o in outcomes)
                receipt_id = prefix + revision
                study["receipts"].append({
                    "id": receipt_id, "revision_id": revision, "artifact_id": name,
                    "source_sha256": artifacts[name]["sha256"], "suite_id": "suite",
                    "suite_sha256": digest(suite_raw),
                    "environment": {"python": platform.python_version(), "platform": platform.system(),
                                    "runner": "tools/build_c05_example.py:unit-distance-properties/0.1"},
                    "status": "passed" if passed == len(outcomes) else "failed",
                    "attempted": len(outcomes), "completed": len(outcomes), "passed": passed,
                    "conformance": "passed", "visibility": visibility, "execution_basis": "project_fixture_execution"})
                details.append({"receipt_id": receipt_id, "source_sha256": artifacts[name]["sha256"],
                                "suite_sha256": digest(suite_raw), "outcomes": outcomes})
            if ordinal < 2:
                study["feedback"].append({"id": "F-" + revision, "revision_id": revision, "kind": "test",
                                          "receipt_id": "T-" + revision, "visible_to_agent": True})
        study["selection"].append({"revision_id": run + "-V2", "assignment_id": "M-" + names[-1],
                                    "receipt_id": "E-" + run + "-V2"})
    (destination / "study.json").write_bytes(encoded(study))
    (destination / "execution_details.json").write_bytes(encoded({
        "role": "owned_finite_execution_with_stipulated_histories_and_exposure",
        "model_calls": 0, "case_executions": sum(len(d["outcomes"]) for d in details), "receipts": details}))
    study, result = load_study(destination / "study.json")
    design = trace_document(study, result)
    design.update(trace_id="intervention-and-reappearance", checkpoints=[0, 1, 2],
                  protocol_ref="Designed fixed-budget histories; ordered sidecar marks supplied exposure and reuse.")
    for run in design["runs"]:
        run.update(stop_ordinal=2, budget={"max_revision_ordinal": 2, "max_test_case_attempts": 50})
    for assessment in design["assessments"]:
        assessment["receipt_id"] = "E-" + assessment["revision_id"]
    (destination / "design.json").write_bytes(encoded(design))
    evidence = evidence_document(result)
    content = {
        "task": ("instruction", study["configurations"][0]["prompt"] + "\n"),
        "alternate": ("instruction", "Use a different propagation mechanism than the current FIFO implementation.\n"),
        "reference": ("reference_code", programs["relax_good"][1]),
    }
    for key, (kind, source) in content.items():
        name = "materials/" + key + (".py" if kind == "reference_code" else ".txt")
        raw = source.encode()
        (destination / name).write_bytes(raw)
        evidence["materials"].append({"id": key, "path": name, "sha256": digest(raw), "kind": kind,
                                      "origin": "project_fixture", "source_ref": "owned-example:" + key,
                                      "independence_claim": "shared_origin"})
    for run in histories:
        def event(suffix, after, before, order, kind, material_ids, feedback_ids, visibility="visible", reuse="none"):
            evidence["interventions"].append({
                "id": run + "-" + suffix, "run_id": run, "after_revision_id": after,
                "before_revision_id": before, "order": order, "kind": kind,
                "material_ids": material_ids, "feedback_ids": feedback_ids,
                "visibility": visibility, "reuse_claim": reuse})
        event("prompt", None, run + "-V0", 1, "baseline_prompt", ["task"], [])
        for ordinal in (0, 1):
            event("test" + str(ordinal), f"{run}-V{ordinal}", f"{run}-V{ordinal+1}", ordinal + 2,
                  "test_feedback", [], [f"F-{run}-V{ordinal}"])
        if run == "I1":
            event("reference", run + "-V1", run + "-V2", 4, "reference_material", ["reference"], [], reuse="copied")
        else:
            event("alternate", run + "-V1", run + "-V2", 4, "alternative_strategy", ["alternate"], [], reuse="unknown")
            event("withheld", run + "-V1", run + "-V2", 5, "reference_material", ["reference"], [],
                  visibility="withheld", reuse="unknown")
    for detail in details:
        if detail["receipt_id"] in {"E-I1-V0", "E-I2-V0", "E-I2-V1", "E-I2-V2"}:
            evidence["failure_profiles"].append({
                "id": "P-" + detail["receipt_id"], "receipt_id": detail["receipt_id"],
                "outcomes": [{"id": o["case_id"], "status": "passed" if o["passed"] else "failed"}
                             for o in detail["outcomes"]]})
    (destination / "evidence.json").write_bytes(encoded(evidence))
    return {"runs": len(study["runs"]), "revisions": len(study["revisions"]),
            "receipts": len(details), "finite_case_executions": sum(len(d["outcomes"]) for d in details)}


if __name__ == "__main__":
    print(build_example(ROOT / "examples/interventions"))
