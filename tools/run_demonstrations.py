"""Run six passive, owned demonstrations and replay every saved analysis."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from structdet_code.errors import StudyError
from structdet_code.replay import create_snapshot, replay_snapshot
from structdet_code.workflow import _write_new, encoded


def run_demonstrations(output):
    output = Path(output).absolute()
    output.mkdir(mode=0o700)
    scenarios = [
        ("surface", "inspect", {"study": "examples/static/study.json"}),
        ("mechanisms", "compare", {"left": "examples/graph/left/study.json",
                                  "right": "examples/graph/right/study.json",
                                  "design": "examples/graph/comparison.json"}),
        *[(name, "trace", {"study": "examples/trace/study.json", "design": f"examples/trace/{name}.json"})
          for name in ("concentration", "stable", "attrition")],
        ("interventions", "trace", {"study": "examples/interventions/study.json",
                                   "design": "examples/interventions/design.json",
                                   "evidence": "examples/interventions/evidence.json"}),
    ]
    rows = []
    for name, action, arguments in scenarios:
        captured = create_snapshot(action, {key: str(ROOT / path) for key, path in arguments.items()}, output / name)
        replayed = replay_snapshot(output / name)
        result = replayed["result"]
        row = {"demonstration": name, "action": action, "replay_status": replayed["status"],
               "result_sha256": captured["result_sha256"], "candidate_execution_performed": False}
        if action == "inspect":
            row["views"] = result["views"]
        elif action == "trace":
            row["checkpoints"] = [
                {"ordinal": p["ordinal"], "observed": p["available"]["observed"],
                 "support": p["available"]["views"]["classified_all"]["observed_support"],
                 "sci": p["available"]["views"]["classified_all"]["sci"],
                 "passing": p["available"]["observed_pass_fraction"]}
                for p in result["cohorts"]["checkpoints"]]
            row["matched_run_ids"] = result["cohorts"]["matched_run_ids"]
            if "evidence" in result:
                row["intervention_count"] = len(result["evidence"]["interventions"])
                row["profile_count"] = len(result["evidence"]["failure_profiles"]["profiles"])
        rows.append(row)
    summary = {"material": "designed_owned_fixtures", "model_calls": 0,
               "candidate_execution_performed": False, "demonstrations": rows}
    _write_new(output / "summary.json", encoded(summary))
    lines = ["# Six StructDet Code demonstrations", "",
             "Passive analysis of owned fixtures. Every saved JSON and Markdown result was exactly replayed.", "",
             "| Demonstration | Analysis | Replay |", "| --- | --- | --- |"]
    lines += [f"| {r['demonstration']} | {r['action']} | {r['replay_status']} |" for r in rows]
    lines += ["", "Each named directory contains result.md, result.json, snapshot.json and its captured passive inputs.",
              "The fixtures do not establish empirical model behavior. No imported candidate or model was run.", ""]
    _write_new(output / "summary.md", "\n".join(lines).encode())
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="New directory for the six fixture snapshots")
    args = parser.parse_args()
    try:
        value = run_demonstrations(args.output)
    except (StudyError, OSError) as exc:
        print(json.dumps({"status": "invalid", "code": getattr(exc, "code", "output_unavailable")}), file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps(value, indent=2))
