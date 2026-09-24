"""Build and qualify owned distributions offline, outside the source checkout.

Requires pip and setuptools >=77.0.3 in the invoking build environment.
The two runtime venvs have no system packages or third-party runtime dependencies.
The source route rebuilds the actual sdist with the installed PEP 517 backend,
then installs that wheel into the second clean venv. Nothing is published.
"""

import argparse
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import venv
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(command, cwd, log, expected=0):
    env = {k: v for k, v in os.environ.items()
           if k not in {"PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP"}}
    result = subprocess.run([str(x) for x in command], cwd=cwd, env=env,
                            capture_output=True, text=True, timeout=120)
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    check(result.returncode == expected,
          f"Command exit {result.returncode}, expected {expected}; see {log}")
    return result


def wheel_payload(path):
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def qualify_runtime(wheel, output, fixture_hashes, expected_version):
    output.mkdir()
    env_dir, work = output / "venv", output / "work"
    venv.EnvBuilder(with_pip=False).create(env_dir)
    work.mkdir()
    python, console = env_dir / "bin/python", env_dir / "bin/structdet-code"
    run([sys.executable, "-I", "-m", "pip", "--isolated", "--python", python,
         "install", "--no-index", "--no-deps", "--no-cache-dir", wheel],
        work, output / "install.log")
    identity = json.loads(run([python, "-I", "-c",
        "import importlib.metadata as m, json, structdet_code as s; "
        "from importlib.resources import files; "
        "print(json.dumps({'module': s.__file__, 'version': s.__version__, "
        "'examples': str(files('structdet_code').joinpath('example_data')), "
        "'packages': {d.metadata['Name']: d.version for d in m.distributions()}}))"],
        work, output / "identity.json").stdout)
    check(Path(identity["module"]).is_relative_to(env_dir), "Imported checkout instead of installation")
    check(Path(identity["examples"]).is_relative_to(env_dir) and Path(identity["examples"]).is_dir(),
          "Installed example resources missing")
    check(identity["packages"] == {"structdet-code": expected_version}, "Runtime is not dependency-free")
    check(identity["version"] == expected_version, "Installed version mismatch")
    checks = ["clean_runtime_import_and_metadata", "installed_example_resources"]
    module_version = run([python, "-I", "-m", "structdet_code", "--version"],
                         work, output / "module-version.txt").stdout.strip()
    console_version = run([console, "--version"], work, output / "console-version.txt").stdout.strip()
    check(module_version == console_version == expected_version, "Entry point version mismatch")
    checks.append("module_and_console_entry_points")
    counter = 0

    def cli(*args, expected=0, markdown=False):
        nonlocal counter
        counter += 1
        result = run([console, *args], work, output / f"command-{counter:02}.log", expected)
        if markdown:
            check(bool(result.stdout.strip()), "Empty Markdown report")
            return result.stdout
        return json.loads(result.stdout if expected == 0 else result.stderr)

    exported = work / "examples"
    exported_result = cli("examples", "--output", exported)
    copied = {p.relative_to(exported).as_posix(): sha(p.read_bytes())
              for p in exported.rglob("*") if p.is_file()}
    check(copied == fixture_hashes and exported_result["file_count"] == len(copied),
          "Installed examples differ from authoritative fixture bytes")
    check(all(p.stat().st_mode & 0o077 == 0 for p in [exported, *exported.rglob("*")]),
          "Example export permissions are not owner-only")
    check(cli("examples", "--output", exported, expected=2)["code"] == "output_already_exists",
          "Export accepted an existing output directory")
    checks += ["all_fixture_bytes_and_permissions", "existing_output_refused"]
    studies = sorted(exported.rglob("study.json"))
    check(len(studies) == 6, "Expected six shipped study manifests")
    for study in studies:
        check(cli("validate", "--study", study)["status"] == "valid_records", "Invalid shipped study")
    checks.append("six_shipped_studies_validate")
    static = exported / "static/study.json"
    inspected = cli("inspect", "--study", static)
    check(inspected["views"]["classified_all"]["class_counts"] ==
          {"SORT-INS": 4, "SORT-MERGE": 1, "SORT-SEL": 1}, "Static count oracle changed")
    cli("inspect", "--study", static, "--format", "markdown", markdown=True)
    checks.append("static_json_and_markdown")
    graph = exported / "graph"
    compared = cli("compare", "--left", graph / "left/study.json", "--right", graph / "right/study.json",
                   "--design", graph / "comparison.json")
    delta = compared["contrasts"]["classified_all"]["right_minus_left"]["sci"]
    check((delta["numerator"], delta["denominator"]) == (5, 8), "Comparison oracle changed")
    cli("comparison-template", "--left", graph / "left/study.json", "--right", graph / "right/study.json",
        "--output", work / "comparison-template.json")
    checks.append("compatible_comparison_and_template")
    intervention = exported / "interventions"
    traced = cli("trace", "--study", intervention / "study.json", "--design", intervention / "design.json",
                 "--evidence", intervention / "evidence.json")
    check(len(traced["evidence"]["interventions"]) == 9, "Intervention records missing")
    check(len(traced["evidence"]["failure_profiles"]["profiles"]) == 4, "Failure profiles missing")
    checks.append("recorded_trace_interventions_and_profiles")
    prepared = work / "prepared"
    cli("prepare", "--sources", exported / "minimal/sources", "--output", prepared, "--data-role", "fixture")
    original = json.loads((prepared / "study.json").read_bytes())
    check(len(original["artifacts"]) == 7 and original["receipts"] == [], "Preparation invented evidence")
    cli("review-template", "--study", prepared / "study.json", "--output", prepared / "decisions.json")
    cli("evidence-template", "--study", prepared / "study.json", "--output", prepared / "evidence.json")
    cli("trace-template", "--study", prepared / "study.json", "--output", prepared / "trace.json")
    decisions = json.loads((prepared / "decisions.json").read_bytes())
    entry = next(row for row in decisions["entries"] if row["suggested_class_id"] is not None)
    entry.update(decision="unresolved", basis="human_review", class_id=None,
                 reason="insufficient_evidence", reviewer_ref="reviewer:fixture-correction",
                 evidence=[], note="Designed withdrawal for installation qualification.")
    write_json(prepared / "decisions.json", decisions)
    cli("apply-review", "--study", prepared / "study.json", "--review", prepared / "decisions.json",
        "--output", prepared / "corrected.json")
    corrected = json.loads((prepared / "corrected.json").read_bytes())
    check(corrected["assignments"][:-1] == original["assignments"], "Prior review history changed")
    check(cli("inspect", "--study", prepared / "corrected.json")["views"]["classified_all"]["population_size"] == 5,
          "Correction did not reduce admitted population")
    check(cli("inspect", "--study", prepared / "corrected.json", "--evidence", prepared / "evidence.json",
              expected=2)["code"] == "evidence_study_binding_mismatch", "Stale evidence binding accepted")
    checks += ["prepare_and_review_correction", "bound_templates_and_stale_evidence_refusal"]
    own = work / "own-sources"
    own.mkdir()
    marker = work / "candidate-must-not-run"
    (own / "opaque.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n",
                                    encoding="utf-8")
    cli("prepare", "--sources", own, "--output", work / "own-study")
    cli("inspect", "--study", work / "own-study/study.json")
    check(not marker.exists(), "Candidate source was executed")
    check(json.loads((work / "own-study/study.json").read_bytes())["data_role"] == "descriptive",
          "Own-source default role changed")
    checks.append("own_input_remains_passive_and_descriptive")
    (work / "malformed.json").write_text('{"broken":', encoding="utf-8")
    error = cli("inspect", "--study", work / "malformed.json", expected=2)
    check(error == {"status": "invalid", "code": "invalid_json"}, "Unbounded or unexpected malformed-input error")
    checks.append("malformed_input_exit_2")
    demos = work / "demos"
    summary = cli("demo", "--output", demos)
    rows = {row["demonstration"]: row for row in summary["demonstrations"]}
    check(set(rows) == {"surface", "mechanisms", "concentration", "stable", "attrition", "interventions"},
          "Missing demonstration")
    check(all(row["replay_status"] == "replay_verified" for row in rows.values()), "Demo replay failed")
    concentration = rows["concentration"]["checkpoints"]
    check([p["support"] for p in concentration] == [3, 2, 1], "Concentration support oracle changed")
    check([(p["sci"]["numerator"], p["sci"]["denominator"]) for p in concentration] ==
          [(7, 18), (5, 9), (1, 1)], "Concentration SCI oracle changed")
    check([p["passing"]["numerator"] for p in concentration] == [2, 4, 6], "Correctness oracle changed")
    check([p["support"] for p in rows["stable"]["checkpoints"]] == [3, 3, 3], "Stable support oracle changed")
    check([p["observed"] for p in rows["attrition"]["checkpoints"]] == [5, 2, 2] and
          rows["attrition"]["matched_run_ids"] == ["A3", "A4"], "Attrition accounting changed")
    checks.append("six_demonstrations_and_joint_outcome_oracles")
    saved = work / "cli-snapshot"
    cli("snapshot", "--action", "inspect", "--study", static, "--output", saved)
    shutil.rmtree(exported)
    shutil.rmtree(demos / "examples")
    moved = work / "moved-interventions"
    shutil.move(demos / "interventions", moved)
    for name in rows:
        bundle = moved if name == "interventions" else demos / name
        replayed = cli("replay", "--bundle", bundle)
        check(replayed["status"] == "replay_verified", "Relocated replay failed")
    check(cli("replay", "--bundle", saved)["status"] == "replay_verified", "CLI snapshot replay failed")
    cli("replay", "--bundle", moved, "--format", "markdown", markdown=True)
    checks.append("fresh_process_replay_without_original_inputs")
    with (moved / "result.md").open("ab") as stream:
        stream.write(b"tampered\n")
    error = cli("replay", "--bundle", moved, expected=2)
    check(error["status"] == "invalid", "Tampered report accepted")
    checks.append("tampered_report_refused")
    return {"status": "passed", "checks": checks, "cli_commands": counter,
            "installed_version": identity["version"], "third_party_runtime_dependencies": [],
            "import_from_venv": True, "cwd_outside_checkout": True,
            "fixture_files": len(copied), "study_manifests": len(studies),
            "demonstration_result_sha256": {name: row["result_sha256"] for name, row in rows.items()},
            "candidate_execution_performed": False, "model_calls": 0}


def qualify(output):
    output = Path(output).resolve()
    check(not output.is_relative_to(ROOT), "Qualification output must be outside the source checkout")
    output.mkdir()
    checkout, dist, rebuilt = output / "build-source", output / "dist", output / "from-sdist"
    checkout.mkdir()
    dist.mkdir()
    rebuilt.mkdir()
    for name in ("README.md", "SPEC.md", "CHANGELOG.md", "LICENSE", "NOTICE", "MANIFEST.in", "pyproject.toml"):
        shutil.copy2(ROOT / name, checkout / name)
    for name in ("structdet_code", "examples", "docs", "tests", "tools", "LICENSES"):
        shutil.copytree(ROOT / name, checkout / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
    run([sys.executable, "-I", "-c", "from setuptools.build_meta import build_sdist, build_wheel; "
         f"build_sdist({str(dist)!r}); build_wheel({str(dist)!r})"], checkout, output / "build.log")
    wheel, sdist = next(dist.glob("*.whl")), next(dist.glob("*.tar.gz"))
    run([sys.executable, "-I", "-m", "pip", "--isolated", "wheel", "--no-index", "--no-deps",
         "--no-build-isolation", "--no-cache-dir", "--wheel-dir", rebuilt, sdist],
        output, output / "sdist-rebuild.log")
    rebuilt_wheel = next(rebuilt.glob("*.whl"))
    payload = wheel_payload(wheel)
    check(payload == wheel_payload(rebuilt_wheel), "Direct and sdist-rebuilt wheel contents differ")
    fixture_hashes = {p.relative_to(ROOT / "examples").as_posix(): sha(p.read_bytes())
                      for p in (ROOT / "examples").rglob("*")
                      if p.is_file() and p.suffix in {".py", ".json", ".txt"}}
    packaged = {name.removeprefix("structdet_code/example_data/"): sha(data)
                for name, data in payload.items() if name.startswith("structdet_code/example_data/")}
    check(packaged == fixture_hashes, "Wheel lost or altered example files")
    for name in ("LICENSE", "NOTICE", "LICENSES/CC-BY-4.0.txt"):
        check(any(key.endswith(".dist-info/licenses/" + name) for key in payload), f"Wheel missing license: {name}")
    with tarfile.open(sdist) as archive:
        names = {str(Path(name).relative_to(Path(name).parts[0])) for name in archive.getnames()}
        check({"README.md", "SPEC.md", "CHANGELOG.md", "docs/INSTALL.md", "docs/RELATED_WORK.md",
               "tools/qualify_distribution.py", "tests/test_integration.py", "LICENSE", "NOTICE"} <= names,
              "Source distribution missing user/developer material")
        check(not any(name.endswith((".pdf", ".pyc", ".whl")) for name in names), "Unexpected source payload")
    import tomllib
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    direct = qualify_runtime(wheel, output / "wheel-runtime", fixture_hashes, project["version"])
    source = qualify_runtime(rebuilt_wheel, output / "sdist-runtime", fixture_hashes, project["version"])
    check(direct["demonstration_result_sha256"] == source["demonstration_result_sha256"],
          "Installed routes produced different results")
    summary = {
        "status": "passed", "version": project["version"],
        "environment": {"system": platform.system(), "machine": platform.machine(),
                        "python": platform.python_version(), "implementation": platform.python_implementation(),
                        "pip": version("pip"), "setuptools": version("setuptools")},
        "build_isolation": False, "package_index_access": False,
        "source_route": "actual sdist -> pip wheel with installed backend -> clean venv install",
        "wheel_member_bytes_identical_after_sdist_rebuild": True,
        "artifacts": [{"path": p.relative_to(output).as_posix(), "bytes": p.stat().st_size,
                       "sha256": sha(p.read_bytes())} for p in (wheel, sdist, rebuilt_wheel)],
        "wheel": direct, "sdist": source,
    }
    write_json(output / "qualification.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="New absolute directory outside this checkout")
    args = parser.parse_args()
    result = qualify(args.output)
    print(json.dumps({"status": result["status"], "version": result["version"],
                      "checks_per_route": len(result["wheel"]["checks"]),
                      "output": str(Path(args.output).resolve())}, indent=2))
