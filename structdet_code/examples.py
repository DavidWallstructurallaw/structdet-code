"""Export owned passive fixtures and run demonstrations from an installed package."""

from importlib.resources import files
from pathlib import Path

from .errors import require
from .replay import create_snapshot, replay_snapshot
from .workflow import _write_new, encoded


def _example_root():
    root = files("structdet_code").joinpath("example_data")
    if root.is_dir():
        return root
    # The same authoritative tree is mapped into example_data by setuptools.
    # This fallback serves an uninstalled source checkout only.
    checkout = Path(__file__).resolve().parents[1]
    require((checkout / "pyproject.toml").is_file() and (checkout / "examples").is_dir(),
            "packaged_examples_unavailable")
    return checkout / "examples"


def _copy_tree(source, destination):
    count = 0
    for entry in sorted(source.iterdir(), key=lambda item: item.name):
        if entry.name.startswith(".") or entry.name == "__pycache__":
            continue
        target = destination / entry.name
        if entry.is_dir():
            target.mkdir(mode=0o700)
            count += _copy_tree(entry, target)
        elif entry.name.endswith((".json", ".py", ".txt")):
            _write_new(target, entry.read_bytes())
            count += 1
    return count


def export_examples(output):
    """Copy installed resources as data; never import or execute fixture programs."""
    source = _example_root()
    output = Path(output).absolute()
    require(not output.exists() and not output.is_symlink(), "output_already_exists")
    output.mkdir(mode=0o700)
    count = _copy_tree(source, output)
    return {"status": "examples_copied", "file_count": count,
            "material": "designed_owned_fixtures", "candidate_execution_performed": False}


def run_demonstrations(output):
    output = Path(output).absolute()
    output.mkdir(mode=0o700)
    export_examples(output / "examples")
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
        captured = create_snapshot(action, {key: str(output / path) for key, path in arguments.items()}, output / name)
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

