"""Regenerate the project-owned C01 fixture and its actual finite test receipts.

Developer utility only. It executes this project's seven named reviewed files.
It has no user-supplied candidate, manifest, command, plugin, or path argument.
Production inspection never invokes this utility.
"""

from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from structdet_code.study import SCHEMA, task_pack

DEST = ROOT / "examples/minimal"
SOURCE_NAMES = ("insertion_inplace", "insertion", "insertion_renamed", "merge",
                "selection", "opaque", "claimed_merge")
LABELS = ("SORT-INS", "SORT-INS", "SORT-INS", "SORT-MERGE", "SORT-SEL", None, "SORT-MERGE")
NOTES = (
    "The next incoming value is placed into the growing ordered prefix. Reusing the input list is a separate interface defect.",
    "The outer frontier grows a sorted prefix; shifts place the incoming value before the next iteration.",
    "Renamed variables preserve prefix growth and incoming-value placement.",
    "Position-based subproblems form ordered runs, then frontiers determine the merged output.",
    "Each iteration rescans the entire remaining region to obtain its next minimum.",
    "Opaque ordering delegation is unresolved for mechanism and violates the task's permitted operations.",
    "Deliberately untrusted model-style proposal based on a misleading docstring. This is not an admitted label.",
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(name, value):
    (DEST / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main():
    require_no_args = len(sys.argv) == 1
    if not require_no_args:
        raise SystemExit("This project-fixture utility takes no arguments.")
    pack, pack_sha = task_pack()
    inputs = [[], [0], [2, 1], [1, 1], [4095, 0, 256, 255],
              [7, 1, 6, 2, 5, 3, 4, 0], [3, 1, 3, 0, 2, 0, 2, 1],
              [256, 1, 4095, 255, 16, 0, 257, 4094],
              [0, 1, 2, 3, 7, 6, 5, 4], list(range(31, -1, -1))]
    suite = {"schema_version": "structdet-code.sort-suite/0.1", "oracle_id": "sort-properties/0.1",
             "cases": [{"id": f"T{i:02d}", "input": value} for i, value in enumerate(inputs)]}
    write_json("suite.json", suite)
    suite_sha = sha((DEST / "suite.json").read_bytes())
    artifacts, assignments, functions = [], [], {}
    for i, name in enumerate(SOURCE_NAMES):
        path = DEST / "sources" / f"{name}.py"
        raw = path.read_bytes()
        artifact_id = f"A{i + 1}"
        artifacts.append({"id": artifact_id, "path": f"sources/{name}.py", "sha256": sha(raw),
                          "language": "python", "entry_point": "sort_values",
                          "origin": "project_fixture", "capture_status": "complete"})
        status = "unresolved" if name == "opaque" else "proposed" if name == "claimed_merge" else "accepted"
        assignments.append({
            "id": f"M{i + 1}", "artifact_id": artifact_id, "source_sha256": sha(raw),
            "pack_sha256": pack_sha, "revision": 1, "status": status,
            "basis": "model_assisted" if name == "claimed_merge" else "fixture",
            "class_id": LABELS[i], "reason": "opaque_dependency" if name == "opaque"
            else "not_reviewed" if name == "claimed_merge" else None,
            "reviewer_ref": None,
            "evidence": [{"start_line": 1, "end_line": len(raw.decode().splitlines()), "note": NOTES[i]}],
        })
        spec = importlib.util.spec_from_file_location(f"c01_owned_{name}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        functions[artifact_id] = module.sort_values
    runs, revisions = [], []
    starts = ("A1", "A2", "A3", "A4", "A5", "A6", "A7")
    for i, artifact_id in enumerate(starts, 1):
        endpoint = "R1V2" if i == 1 else "R4V1" if i == 4 else f"R{i}V0"
        runs.append({"id": f"R{i}", "configuration_id": "C-fixture", "root_group_id": "G-project-fixtures",
                     "stop_reason": "failure" if i == 6 else "success", "endpoint_revision_id": endpoint})
        revisions.append({"id": f"R{i}V0", "run_id": f"R{i}", "ordinal": 0,
                          "artifact_id": artifact_id, "parents": [], "missing_parents": [],
                          "kind": "generation", "feedback_ids": []})
    revisions.extend([
        {"id": "R1V1", "run_id": "R1", "ordinal": 1, "artifact_id": "A2", "parents": ["R1V0"],
         "missing_parents": [], "kind": "edit", "feedback_ids": ["F-input-copy"]},
        {"id": "R1V2", "run_id": "R1", "ordinal": 2, "artifact_id": "A2", "parents": ["R1V1"],
         "missing_parents": [], "kind": "no_op", "feedback_ids": ["F-retest"]},
        {"id": "R4V1", "run_id": "R4", "ordinal": 1, "artifact_id": "A5", "parents": ["R4V0"],
         "missing_parents": [], "kind": "edit", "feedback_ids": ["F-alternative"]},
    ])
    receipts, execution_details = [], []
    artifact_map = {a["id"]: a for a in artifacts}
    for revision in revisions:
        outcomes = []
        for case in suite["cases"]:
            argument = list(case["input"])
            before = list(argument)
            result = functions[revision["artifact_id"]](argument)
            checks = {
                "new_plain_list": type(result) is list and result is not argument,
                "plain_integers": all(type(v) is int for v in result),
                "same_multiplicities": Counter(result) == Counter(before),
                "nondecreasing": all(a <= b for a, b in zip(result, result[1:])),
                "input_unchanged": argument == before,
            }
            outcomes.append({"case_id": case["id"], "checks": checks, "passed": all(checks.values())})
        passed = sum(outcome["passed"] for outcome in outcomes)
        receipts.append({
            "id": "T-" + revision["id"], "revision_id": revision["id"],
            "artifact_id": revision["artifact_id"], "source_sha256": artifact_map[revision["artifact_id"]]["sha256"],
            "suite_id": "S-small", "suite_sha256": suite_sha,
            "environment": {"python": platform.python_version(), "platform": platform.system(),
                            "runner": "tools/build_c01_fixture.py:sort-properties/0.1"},
            "status": "passed" if passed == len(inputs) else "failed", "attempted": len(inputs),
            "completed": len(inputs), "passed": passed,
            "conformance": "failed" if revision["artifact_id"] == "A6" else "passed",
            "visibility": "feedback", "execution_basis": "project_fixture_execution",
        })
        execution_details.append({"revision_id": revision["id"], "source_sha256": artifact_map[revision["artifact_id"]]["sha256"],
                                  "suite_sha256": suite_sha, "outcomes": outcomes})
    study = {
        "schema_version": SCHEMA, "study_id": "c01-owned-sorting", "data_role": "fixture", "evidence_policy": "fixture_only",
        "task": {"pack_id": pack["pack_id"], "pack_version": pack["pack_version"],
                 "resolution_id": pack["resolution_id"], "pack_sha256": pack_sha},
        "configurations": [{"id": "C-fixture", "model": None, "prompt": None, "settings": None,
                            "selection_rule": "Designed fixture; select the explicitly named initial revision of each run."}],
        "artifacts": artifacts, "assignments": assignments,
        "suites": [{"id": "S-small", "path": "suite.json", "sha256": suite_sha, "oracle_id": "sort-properties/0.1"}],
        "receipts": receipts, "runs": runs, "revisions": revisions,
        "feedback": [
            {"id": "F-input-copy", "revision_id": "R1V0", "kind": "test", "receipt_id": "T-R1V0", "visible_to_agent": True},
            {"id": "F-retest", "revision_id": "R1V1", "kind": "test", "receipt_id": "T-R1V1", "visible_to_agent": True},
            {"id": "F-alternative", "revision_id": "R4V0", "kind": "human", "receipt_id": None, "visible_to_agent": True},
        ],
        "selection": [{"revision_id": f"R{i}V0", "assignment_id": f"M{i}", "receipt_id": f"T-R{i}V0"} for i in range(1, 8)],
    }
    write_json("study.json", study)
    write_json("execution_details.json", {"data_role": "fixture", "independent_validation": False,
                                         "suite_sha256": suite_sha, "records": execution_details})
    # Derived by hand before invoking any product metric function.
    write_json("expected.json", {
        "selected_observations": 7, "accepted": 5, "proposed": 1, "unresolved": 1,
        "all_counts": {"SORT-INS": 3, "SORT-MERGE": 1, "SORT-SEL": 1},
        "all_sci": [11, 25], "valid_counts": {"SORT-INS": 2, "SORT-MERGE": 1, "SORT-SEL": 1},
        "valid_sci": [3, 8], "qualified_valid_selected": 5,
        "recorded_runs": 7, "recorded_revisions": 10, "no_op_revisions": 1,
    })
    print(json.dumps({"fixture_sources": len(artifacts), "revision_receipts": len(receipts),
                      "finite_test_executions": len(inputs) * len(receipts), "model_calls": 0}))


if __name__ == "__main__":
    main()
