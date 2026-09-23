"""Build fixed, project-owned revision examples with actual finite test receipts.

Histories, conditions, stopping and budgets are stipulated software fixtures.
Only the reviewed graph references and their explicit increment defects execute.
The command takes no candidate, study, provider, plugin or shell argument.
"""

from copy import deepcopy
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from structdet_code.graph_rules import RULES
from structdet_code.io import digest
from structdet_code.study import SCHEMA, load_study, task_pack
from structdet_code.trace import trace_document
from structdet_code.workflow import encoded
from tools.build_graph_example import distance_oracle, graph_inputs

DEST = ROOT / "examples/trace"


def build_example(destination):
    destination = Path(destination)
    (destination / "sources").mkdir(parents=True, exist_ok=True)
    references = {key: source for key, _, _, source in RULES}
    programs = {
        "fifo_good": ("DIST-FIFO", references["dist-fifo-first-discovery/1"]),
        "fifo_bad": ("DIST-FIFO", references["dist-fifo-step-defect/1"]),
        "settle_good": ("DIST-SETTLE", references["dist-minimum-settlement/1"]),
        "settle_bad": ("DIST-SETTLE", references["dist-minimum-settlement/1"].replace("distances[best] + 1", "distances[best] + 2")),
        "relax_good": ("DIST-RELAX", references["dist-complete-edge-passes/1"]),
        "relax_bad": ("DIST-RELAX", references["dist-complete-edge-passes/1"].replace("distances[source] + 1", "distances[source] + 2")),
    }
    scenarios = {
        "concentration": [
            ("C1", ["fifo_good", "fifo_good", "fifo_good"], "budget", 2),
            ("C2", ["fifo_good", "fifo_good", "fifo_good"], "budget", 2),
            ("C3", ["fifo_bad", "fifo_good", "fifo_good"], "budget", 2),
            ("C4", ["settle_bad", "settle_good", "fifo_good"], "budget", 2),
            ("C5", ["settle_bad", "settle_bad", "fifo_good"], "budget", 2),
            ("C6", ["relax_bad", "fifo_bad", "fifo_good"], "budget", 2),
        ],
        "stable": [
            ("S1", ["fifo_good", "fifo_good", "fifo_good"], "budget", 2),
            ("S2", ["fifo_good", "fifo_good", "fifo_good"], "budget", 2),
            ("S3", ["fifo_bad", "fifo_good", "fifo_good"], "budget", 2),
            ("S4", ["settle_bad", "settle_good", "settle_good"], "budget", 2),
            ("S5", ["settle_bad", "settle_bad", "settle_good"], "budget", 2),
            ("S6", ["relax_bad", "relax_bad", "relax_good"], "budget", 2),
        ],
        "attrition": [
            ("A1", ["settle_good"], "success", 0),
            ("A2", ["relax_good"], "success", 0),
            ("A3", ["fifo_bad", "fifo_good", "fifo_good"], "budget", 2),
            ("A4", ["fifo_bad", "fifo_good", "fifo_good"], "budget", 2),
            ("A5", ["fifo_bad"], "timeout", 0),
        ],
    }
    pack, pack_sha = task_pack("unit-graph-distances")
    suite = {"schema_version": "structdet-code.graph-suite/0.1", "oracle_id": "unit-distance-properties/0.1",
             "cases": [{"id": f"T{index:02}", "input": graph} for index, graph in enumerate(graph_inputs(), 1)]}
    suite_bytes = encoded(suite)
    (destination / "suite.json").write_bytes(suite_bytes)
    suite_sha = digest(suite_bytes)
    study = {"schema_version": SCHEMA, "study_id": "owned-revision-examples", "data_role": "fixture",
             "evidence_policy": "fixture_only", "task": {key: pack[key] for key in ("pack_id", "pack_version", "resolution_id")},
             "configurations": [{"id": name, "model": "project-owned-fixture-no-model-calls",
                                 "prompt": "Stipulated task and repair context for a designed software example.",
                                 "settings": {"material": "designed_fixture", "sampling_performed": False},
                                 "selection_rule": "Declared paths at exact code-revision ordinals; retain missing and stopped runs."}
                                for name in scenarios],
             "artifacts": [], "assignments": [], "suites": [{"id": "suite", "path": "suite.json",
                                                                "sha256": suite_sha, "oracle_id": suite["oracle_id"]}],
             "receipts": [], "runs": [], "revisions": [], "feedback": [], "selection": []}
    study["task"]["pack_sha256"] = pack_sha
    functions, artifact_map = {}, {}
    for name, (cls, source) in programs.items():
        raw = source.encode()
        (destination / "sources" / (name + ".py")).write_bytes(raw)
        artifact = {"id": name, "path": "sources/" + name + ".py", "sha256": digest(raw),
                    "language": "python", "entry_point": pack["entry_point"],
                    "origin": "project_fixture", "capture_status": "complete"}
        study["artifacts"].append(artifact)
        artifact_map[name] = artifact
        study["assignments"].append({"id": "M-" + name, "artifact_id": name, "source_sha256": digest(raw),
                                     "pack_sha256": pack_sha, "revision": 1, "status": "accepted", "basis": "fixture",
                                     "class_id": cls, "reason": None, "reviewer_ref": None,
                                     "evidence": [{"start_line": 1, "end_line": len(source.splitlines()),
                                                   "note": "Designed fixture assignment to " + cls + "; increment defects retain the same propagation schedule."}]})
        namespace = {}
        exec(compile(source, "<project-owned-trace-reference>", "exec"), namespace)
        functions[name] = namespace["shortest_distances"]
    details = []

    def execute(revision, artifact_id, receipt_id, visibility):
        outcomes = []
        for case in suite["cases"]:
            graph = case["input"]
            edges = deepcopy(graph["edges"])
            value = functions[artifact_id](graph["node_count"], edges, graph["start"])
            checks = {"plain_distance_list": type(value) is list and len(value) == graph["node_count"]
                      and all(v is None or type(v) is int and v >= 0 for v in value),
                      "new_list": value is not edges and all(value is not edge for edge in edges),
                      "minimum_hop_distances": value == distance_oracle(**graph),
                      "input_unchanged": edges == graph["edges"]}
            outcomes.append({"case_id": case["id"], "checks": checks, "passed": all(checks.values())})
        passed = sum(item["passed"] for item in outcomes)
        study["receipts"].append({"id": receipt_id, "revision_id": revision, "artifact_id": artifact_id,
                                  "source_sha256": artifact_map[artifact_id]["sha256"], "suite_id": "suite", "suite_sha256": suite_sha,
                                  "environment": {"python": platform.python_version(), "platform": platform.system(),
                                                  "runner": "tools/build_trace_example.py:unit-distance-properties/0.1"},
                                  "status": "passed" if passed == len(outcomes) else "failed",
                                  "attempted": len(outcomes), "completed": len(outcomes), "passed": passed,
                                  "conformance": "passed", "visibility": visibility,
                                  "execution_basis": "project_fixture_execution"})
        details.append({"receipt_id": receipt_id, "revision_id": revision,
                        "source_sha256": artifact_map[artifact_id]["sha256"], "suite_sha256": suite_sha,
                        "outcomes": outcomes})

    assessments, stops = [], {}
    for configuration, histories in scenarios.items():
        for run, names, stop, stop_ordinal in histories:
            stops[run] = stop_ordinal
            endpoint = f"{run}-V{len(names) - 1}"
            study["runs"].append({"id": run, "configuration_id": configuration, "root_group_id": "G-owned-fixtures",
                                  "stop_reason": stop, "endpoint_revision_id": endpoint})
            for ordinal, name in enumerate(names):
                revision = f"{run}-V{ordinal}"
                parent = f"{run}-V{ordinal - 1}"
                kind = "generation" if ordinal == 0 else "no_op" if names[ordinal - 1] == name else "edit"
                study["revisions"].append({"id": revision, "run_id": run, "ordinal": ordinal, "artifact_id": name,
                                           "parents": [parent] if ordinal else [], "missing_parents": [], "kind": kind,
                                           "feedback_ids": ["F-" + parent] if ordinal else []})
                execute(revision, name, "E-" + revision, "withheld")
                assessments.append({"revision_id": revision, "assignment_id": "M-" + name, "receipt_id": "E-" + revision})
                if ordinal < len(names) - 1:
                    execute(revision, name, "T-" + revision, "feedback")
                    study["feedback"].append({"id": "F-" + revision, "revision_id": revision, "kind": "test",
                                              "receipt_id": "T-" + revision, "visible_to_agent": True})
            study["selection"].append({"revision_id": endpoint, "assignment_id": "M-" + names[-1], "receipt_id": "E-" + endpoint})
    # Another finite test of the same final bytes adds evidence, not a revision.
    execute("C1-V2", "fifo_good", "retest-C1-V2", "withheld")
    (destination / "study.json").write_bytes(encoded(study))
    _, inspection = load_study(destination / "study.json")
    for configuration, histories in scenarios.items():
        run_ids = {run for run, _, _, _ in histories}
        design = trace_document(study, inspection)
        design.update(trace_id="fixture-" + configuration, configuration_id=configuration,
                      protocol_ref="Designed exact-ordinal fixture protocol; histories and equal budgets stipulated; zero model calls.",
                      checkpoints=[0, 1, 2])
        design["runs"] = [run for run in design["runs"] if run["run_id"] in run_ids]
        design["assessments"] = [item for item in assessments if item["revision_id"].split("-")[0] in run_ids]
        for run in design["runs"]:
            run.update(stop_ordinal=stops[run["run_id"]], budget={"max_revision_ordinal": 2, "max_test_case_attempts": 60})
        if configuration == "attrition":
            design["runs"].append({"run_id": "A6", "missing": True, "path": None, "stop_ordinal": None,
                                   "budget": {"max_revision_ordinal": 2, "max_test_case_attempts": 60}})
        (destination / (configuration + ".json")).write_bytes(encoded(design))
    (destination / "execution_details.json").write_bytes(encoded(details))
    return {"source_files": len(programs), "runs": len(study["runs"]), "revisions": len(study["revisions"]),
            "test_receipts": len(study["receipts"]), "finite_case_executions": sum(len(item["outcomes"]) for item in details)}


if __name__ == "__main__":
    if len(sys.argv) != 1:
        raise SystemExit("This fixed project-fixture utility takes no arguments.")
    print(build_example(DEST))
