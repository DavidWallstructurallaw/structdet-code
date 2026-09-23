"""Self-contained passive analysis snapshots, checked against installed code."""

from importlib.resources import files
import json
import os
from pathlib import Path
import platform
import tempfile

from . import __version__
from .comparison import compare_studies, comparison_markdown
from .errors import StudyError, require
from .evidence import MAX_RESULT, _hash
from .io import InputDirectory, MAX_JSON, MAX_SOURCE, digest, json_bytes, relative_path
from .reporting import markdown
from .study import fields, integer, records, inspect_study
from .trace import analyze_trace
from .trace_reporting import trace_markdown
from .workflow import _write_new, encoded

SCHEMA = "structdet-code.snapshot/0.1"
MAX_FILES = 512
MAX_BUNDLE = 25_165_824
METHOD = "exact-passive-analysis/0.1"


def software_identity():
    """Hash installed analysis/renderer/rule code and task data, never bundle code."""
    root = files("structdet_code")
    resources = [(p.name, p) for p in root.iterdir() if p.name.endswith(".py")]
    resources += [("tasks/" + p.name, p) for p in root.joinpath("tasks").iterdir()
                  if p.name.endswith(".json")]
    return {"version": __version__, "method": METHOD,
            "python": platform.python_version(), "implementation": platform.python_implementation(),
            "platform": platform.system(),
            "files": {name: digest(path.read_bytes()) for name, path in sorted(resources)}}


def _arguments(action, arguments):
    require(isinstance(action, str) and action in {"inspect", "trace", "compare"}, "unsupported_snapshot_action")
    if action == "inspect":
        fields(arguments, "study", "evidence")
    elif action == "trace":
        fields(arguments, "study", "design evidence")
    else:
        fields(arguments, "left right", "design")
    require(all(isinstance(value, str) and bool(value) for value in arguments.values()),
            "invalid_snapshot_argument")


def _json_result(result):
    data = (json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode()
    require(len(data) <= MAX_RESULT, "snapshot_result_size_limit")
    return data


def render_result(action, result):
    return {"inspect": markdown, "trace": trace_markdown, "compare": comparison_markdown}[action](result)


def _run(action, arguments, root):
    args = {key: root / relative_path(value) for key, value in arguments.items()}
    if action == "inspect":
        result = inspect_study(args["study"], args.get("evidence"))
    elif action == "trace":
        result = analyze_trace(args["study"], args.get("design"), args.get("evidence"))
    else:
        result = compare_studies(args["left"], args["right"], args.get("design"))
    raw, rendered = _json_result(result), render_result(action, result).encode()
    require(len(rendered) <= MAX_RESULT, "snapshot_report_size_limit")
    return result, raw, rendered


def _add(captured, path, data):
    relative_path(path)
    if path in captured:
        require(captured[path] == data, "snapshot_input_changed_during_capture")
    captured[path] = data
    require(len(captured) <= MAX_FILES and sum(map(len, captured.values())) <= MAX_BUNDLE,
            "snapshot_bundle_limit")


def _capture(action, arguments):
    _arguments(action, arguments)
    captured, bound = {}, {}
    for key, supplied in sorted(arguments.items()):
        path = Path(supplied).absolute()
        prefix = "inputs/" + key + "/"
        bound[key] = prefix + path.name
        with InputDirectory(path.parent) as directory:
            raw = directory.read(path.name, MAX_JSON)
            _add(captured, bound[key], raw)
            value = json_bytes(raw)
            # Minimal bounded discovery; the copied input gets full validation
            # before any persistent output is created.
            if key in {"study", "left", "right"}:
                require(isinstance(value, dict), "object_required")
                for section, maximum, limit in (("artifacts", 128, MAX_SOURCE), ("suites", 16, MAX_JSON)):
                    for item in records(value.get(section), maximum).values():
                        require("path" in item, "unexpected_or_missing_field")
                        relative_path(item["path"])
                        _add(captured, prefix + item["path"], directory.read(item["path"], limit))
            elif key == "evidence":
                require(isinstance(value, dict), "object_required")
                for item in records(value.get("materials"), 64).values():
                    require("path" in item, "unexpected_or_missing_field")
                    if item["path"] is not None:
                        relative_path(item["path"])
                        _add(captured, prefix + item["path"], directory.read(item["path"], MAX_SOURCE))
    return captured, bound


def _write_payloads(root, payloads):
    paths = {relative_path(name) for name in payloads}
    require(not any(parent in paths for path in paths for parent in path.parents),
            "snapshot_path_collision")
    for relative, raw in sorted(payloads.items()):
        destination = root / relative_path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        _write_new(destination, raw)


def create_snapshot(action, arguments, output):
    captured, bound = _capture(action, arguments)
    identity = software_identity()
    with tempfile.TemporaryDirectory(prefix="structdet-snapshot-") as temporary:
        root = Path(temporary)
        _write_payloads(root, captured)
        _, raw, rendered = _run(action, bound, root)
    require(software_identity() == identity, "software_changed_during_analysis")
    _add(captured, "result.json", raw)
    _add(captured, "result.md", rendered)
    manifest = {"schema_version": SCHEMA, "action": action, "arguments": bound,
                "software": identity, "files": [
                    {"path": name, "sha256": digest(data), "bytes": len(data)}
                    for name, data in sorted(captured.items())]}
    manifest_raw = encoded(manifest)
    require(len(manifest_raw) + sum(map(len, captured.values())) <= MAX_BUNDLE, "snapshot_bundle_limit")
    destination = Path(output).absolute()
    with InputDirectory(destination.parent) as parent:
        try:
            os.mkdir(destination.name, mode=0o700, dir_fd=parent.fd)
        except FileExistsError as exc:
            raise StudyError("output_already_exists") from exc
    # Writes are exclusive. Failed writes leave a detectable incomplete bundle,
    # never a reported successful snapshot.
    _write_payloads(destination, captured)
    _write_new(destination / "snapshot.json", manifest_raw)
    return {"status": "snapshot_created", "action": action, "files": len(captured),
            "manifest_sha256": digest(manifest_raw), "result_sha256": digest(raw),
            "candidate_execution_performed": False,
            "contains_private_inputs": True}


def replay_snapshot(bundle):
    with InputDirectory(Path(bundle).absolute(), total_limit=MAX_BUNDLE) as directory:
        manifest_raw = directory.read("snapshot.json", MAX_JSON)
        manifest = json_bytes(manifest_raw)
        fields(manifest, "schema_version action arguments software files")
        require(manifest["schema_version"] == SCHEMA, "unsupported_snapshot_schema")
        _arguments(manifest["action"], manifest["arguments"])
        require(manifest["software"] == software_identity(), "replay_software_mismatch")
        require(isinstance(manifest["files"], list) and len(manifest["files"]) <= MAX_FILES,
                "snapshot_file_limit")
        captured = {}
        for entry in manifest["files"]:
            fields(entry, "path sha256 bytes")
            path = relative_path(entry["path"])
            require(path.parts[0] == "inputs" or entry["path"] in {"result.json", "result.md"},
                    "unexpected_snapshot_file")
            require(entry["path"] not in captured, "duplicate_snapshot_file")
            _hash(entry["sha256"])
            limit = MAX_RESULT if entry["path"] in {"result.json", "result.md"} else MAX_JSON
            integer(entry["bytes"], 0, limit)
            raw = directory.read(entry["path"], limit)
            require(len(raw) == entry["bytes"] and digest(raw) == entry["sha256"],
                    "replay_file_binding_mismatch")
            captured[entry["path"]] = raw
        require({"result.json", "result.md"} <= captured.keys(), "snapshot_result_missing")
        for value in manifest["arguments"].values():
            require(relative_path(value).parts[0] == "inputs" and value in captured,
                    "snapshot_argument_not_captured")
    # Reanalyze only listed, captured passive inputs in a private working area.
    # Neither paths nor unlisted files in the original bundle can add a validator.
    with tempfile.TemporaryDirectory(prefix="structdet-replay-") as temporary:
        root = Path(temporary)
        _write_payloads(root, {key: value for key, value in captured.items() if key.startswith("inputs/")})
        result, raw, rendered = _run(manifest["action"], manifest["arguments"], root)
    require(software_identity() == manifest["software"], "software_changed_during_analysis")
    require(raw == captured["result.json"] and rendered == captured["result.md"],
            "replay_result_mismatch")
    return {"status": "replay_verified", "action": manifest["action"],
            "manifest_sha256": digest(manifest_raw), "result_sha256": digest(raw),
            "candidate_execution_performed": False, "external_calls_performed": False,
            "authenticity_established": False, "result": result}
