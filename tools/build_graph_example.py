"""Build the designed graph comparison from project-owned reference strings.

Developer utility with no input arguments. Only the four reviewed graph rule
references and their presentation variants are executed. User files, studies,
providers, commands and plugins are never accepted as executable inputs.
"""

from copy import deepcopy
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from structdet_code.analysis import analyze_source
from structdet_code.comparison import comparison_document
from structdet_code.graph_rules import FIFO, RULES
from structdet_code.io import digest
from structdet_code.study import SCHEMA, load_study, task_pack
from structdet_code.workflow import encoded

DEST = ROOT / "examples/graph"


def distance_oracle(node_count, edges, start):
    """Independent finite oracle using all-pairs intermediate-vertex closure."""
    matrix = [[None] * node_count for _ in range(node_count)]
    for vertex in range(node_count):
        matrix[vertex][vertex] = 0
    for source, target in edges:
        if source != target:
            matrix[source][target] = 1
    for middle in range(node_count):
        for source in range(node_count):
            if matrix[source][middle] is None:
                continue
            for target in range(node_count):
                if matrix[middle][target] is not None:
                    value = matrix[source][middle] + matrix[middle][target]
                    if matrix[source][target] is None or value < matrix[source][target]:
                        matrix[source][target] = value
    return matrix[start]


def graph_inputs():
    return [
        {"node_count": 1, "edges": [], "start": 0},
        {"node_count": 1, "edges": [[0, 0]], "start": 0},
        {"node_count": 4, "edges": [], "start": 2},
        {"node_count": 4, "edges": [[0, 1], [1, 2], [2, 3]], "start": 0},
        {"node_count": 6, "edges": [[4, 5], [3, 4], [2, 3], [1, 2], [0, 1]], "start": 0},
        {"node_count": 5, "edges": [[0, 1], [0, 2], [1, 3], [2, 4]], "start": 0},
        {"node_count": 4, "edges": [[0, 1], [1, 2], [2, 0]], "start": 1},
        {"node_count": 4, "edges": [[0, 0], [0, 1], [0, 1], [1, 2], [2, 2]], "start": 0},
        {"node_count": 4, "edges": [[0, 1], [1, 2]], "start": 3},
        {"node_count": 6, "edges": [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [0, 5], [5, 4]], "start": 0},
    ]


def _write(path, value):
    path.write_bytes(encoded(value))


def build_example(destination):
    """Write only known fixture material. Destination is never an execution input."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    pack, pack_sha = task_pack("unit-graph-distances")
    suite = {"schema_version": "structdet-code.graph-suite/0.1", "oracle_id": "unit-distance-properties/0.1",
             "cases": [{"id": f"T{index:02}", "input": value} for index, value in enumerate(graph_inputs(), 1)]}
    suite_sha = digest(encoded(suite))
    references = {rule_id: source for rule_id, _, _, source in RULES}
    settlement = references["dist-minimum-settlement/1"]
    fixtures = {
        "left": [FIFO, FIFO.replace("frontier", "pending").replace("current", "active"),
                 settlement, references["dist-complete-edge-passes/1"]],
        "right": [FIFO, references["dist-fifo-step-defect/1"],
                  '# Designed presentation variant, with the same FIFO mechanism.\n' + FIFO, settlement],
    }
    studies = {}
    execution_details = []
    for side, sources in fixtures.items():
        folder = destination / side
        (folder / "sources").mkdir(parents=True, exist_ok=True)
        _write(folder / "suite.json", suite)
        study = {"schema_version": SCHEMA, "study_id": "graph-fixture-" + side,
                 "data_role": "fixture", "evidence_policy": "static_or_reviewed",
                 "task": {key: pack[key] for key in ("pack_id", "pack_version", "resolution_id")},
                 "configurations": [{"id": "C-fixture", "model": "fixture-condition-" + side,
                                     "prompt": "Stipulated common fixture prompt; no model was called.",
                                     "settings": {"fixture_only": True},
                                     "selection_rule": "Designed project fixtures at explicitly declared collection positions."}],
                 "artifacts": [], "assignments": [], "suites": [
                     {"id": "S-graph", "path": "suite.json", "sha256": suite_sha, "oracle_id": suite["oracle_id"]}],
                 "receipts": [], "runs": [], "revisions": [], "feedback": [], "selection": []}
        study["task"]["pack_sha256"] = pack_sha
        for index, source in enumerate(sources, 1):
            artifact, assignment, run, revision, receipt = (f"{prefix}{index:03}" for prefix in ("A", "M", "R", "V", "T"))
            raw = source.encode("utf-8")
            relative = f"sources/program_{index:02}.py"
            (folder / relative).write_bytes(raw)
            analysis = analyze_source(source, pack["pack_id"])
            study["artifacts"].append({"id": artifact, "path": relative, "sha256": digest(raw),
                                       "language": "python", "entry_point": pack["entry_point"],
                                       "origin": "project_fixture", "capture_status": "complete"})
            study["assignments"].append({"id": assignment, "artifact_id": artifact,
                                         "source_sha256": digest(raw), "pack_sha256": pack_sha, "revision": 1,
                                         "status": "accepted", "basis": "static_rule", "class_id": analysis["class_id"],
                                         "reason": None, "reviewer_ref": None, "evidence": analysis["evidence"],
                                         "rule_id": analysis["rule_id"]})
            namespace = {}
            exec(compile(source, "<project-owned-graph-fixture>", "exec"), namespace)
            outcomes = []
            for case in suite["cases"]:
                graph = case["input"]
                argument = deepcopy(graph["edges"])
                value = namespace["shortest_distances"](graph["node_count"], argument, graph["start"])
                checks = {"plain_distance_list": type(value) is list and len(value) == graph["node_count"]
                          and all(v is None or type(v) is int and v >= 0 for v in value),
                          "new_list": value is not argument and all(value is not edge for edge in argument),
                          "minimum_hop_distances": value == distance_oracle(**graph),
                          "input_unchanged": argument == graph["edges"]}
                outcomes.append({"case_id": case["id"], "checks": checks, "passed": all(checks.values())})
            passed = sum(outcome["passed"] for outcome in outcomes)
            study["receipts"].append({"id": receipt, "revision_id": revision, "artifact_id": artifact,
                                      "source_sha256": digest(raw), "suite_id": "S-graph", "suite_sha256": suite_sha,
                                      "environment": {"python": platform.python_version(), "platform": platform.system(),
                                                      "runner": "tools/build_graph_example.py:unit-distance-properties/0.1"},
                                      "status": "passed" if passed == len(outcomes) else "failed",
                                      "attempted": len(outcomes), "completed": len(outcomes), "passed": passed,
                                      "conformance": "passed", "visibility": "withheld",
                                      "execution_basis": "project_fixture_execution"})
            study["runs"].append({"id": run, "configuration_id": "C-fixture", "root_group_id": "G-project-fixtures",
                                  "stop_reason": "unknown", "endpoint_revision_id": revision})
            study["revisions"].append({"id": revision, "run_id": run, "ordinal": 0, "artifact_id": artifact,
                                       "parents": [], "missing_parents": [], "kind": "snapshot", "feedback_ids": []})
            study["selection"].append({"revision_id": revision, "assignment_id": assignment, "receipt_id": receipt})
            execution_details.append({"side": side, "revision_id": revision, "source_sha256": digest(raw),
                                      "suite_sha256": suite_sha, "outcomes": outcomes})
        _write(folder / "study.json", study)
        studies[side] = load_study(folder / "study.json")
    design = comparison_document(*studies["left"], *studies["right"])
    design.update(comparison_id="graph-designed-prefix", varied_field="model", prefix_size=4,
                  protocol_ref="Designed fixture protocol. Slot identities and equal one-attempt budgets are stipulated; no model calls.")
    for side, positions in (("left", (1, 2, 3, 4)), ("right", (1, 2, 4, 5))):
        design[side]["planned_positions"] = max(positions)
        design[side]["budget_per_slot"] = {"unit": "attempts", "limit": 1}
        for slot, position in zip(design[side]["slots"], positions):
            slot["position"] = position
    design["right"]["slots"].insert(2, {"position": 3, "revision_id": None})
    _write(destination / "comparison.json", design)
    _write(destination / "execution_details.json", execution_details)


if __name__ == "__main__":
    if len(sys.argv) != 1:
        raise SystemExit("This project-fixture utility takes no arguments.")
    build_example(DEST)
    print("Built two designed graph studies; 80 project-owned finite case executions.")
