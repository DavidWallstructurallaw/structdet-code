"""Explicit source preparation and bound, append-only review import.

All candidate material remains passive. New outputs are created exclusively;
existing files, source bundles and review history are never overwritten.
"""

import copy
import json
import os
from pathlib import Path

from .analysis import analyze_source
from .errors import StudyError, require
from .io import InputDirectory, MAX_JSON, MAX_SOURCE, MAX_TOTAL, digest, json_bytes
from .study import SCHEMA, _inspect, fields, identifier, load_study, task_pack

REVIEW_SCHEMA = "structdet-code.review/0.1"


def encoded(value) -> bytes:
    data = (json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")
    require(len(data) <= MAX_JSON, "json_size_limit")
    return data


def _write_new(path: Path, data: bytes):
    """Use a held no-follow parent descriptor and refuse existing output names."""
    with InputDirectory(path.parent) as parent:
        try:
            fd = os.open(path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o600, dir_fd=parent.fd)
        except FileExistsError as exc:
            raise StudyError("output_already_exists") from exc
        except OSError as exc:
            raise StudyError("output_unavailable") from exc
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
        except OSError as exc:
            # A partial output is retained, never silently reported as success.
            raise StudyError("output_write_failed_partial_file_retained") from exc


def review_document(study, result):
    current = {}
    for item in study["assignments"]:
        previous = current.get(item["artifact_id"])
        if previous is None or item["revision"] > previous["revision"]:
            current[item["artifact_id"]] = item
    analyses = {row["artifact_id"]: row for row in result["source_analysis"]}
    entries = []
    for artifact in study["artifacts"]:
        prior = current.get(artifact["id"])
        analysis = analyses[artifact["id"]]
        entries.append({
            "artifact_id": artifact["id"], "source_sha256": artifact["sha256"],
            "current_assignment_id": prior["id"] if prior else None,
            "suggested_class_id": analysis["class_id"],
            "decision": None, "basis": "unknown", "class_id": None, "reason": None,
            "reviewer_ref": None, "evidence": [], "note": None,
        })
    return {"schema_version": REVIEW_SCHEMA, "study_sha256": result["study_sha256"],
            "pack_sha256": study["task"]["pack_sha256"], "entries": entries}


def prepare_sources(source_root, output, study_id="local-collection", data_role="descriptive", include=None):
    identifier(study_id)
    require(data_role in {"fixture", "descriptive"}, "invalid_data_role")
    root, destination = Path(source_root).absolute(), Path(output).absolute()
    require(not destination.exists() and not destination.is_symlink(), "output_already_exists")
    captured = []
    with InputDirectory(root) as directory:
        if include is None:
            names = []
            with os.scandir(directory.fd) as entries:
                for index, entry in enumerate(entries):
                    require(index < 4096, "directory_entry_limit")
                    if entry.name.endswith(".py"):
                        names.append(entry.name)
                        require(len(names) <= 128, "source_collection_size")
            names.sort()
        else:
            names = include
        require(isinstance(names, list) and 0 < len(names) <= 128, "source_collection_size")
        require(all(isinstance(name, str) for name in names), "python_source_required")
        require(len(set(names)) == len(names), "duplicate_source_path")
        for name in names:
            require(isinstance(name, str) and name.endswith(".py"), "python_source_required")
            data = directory.read(name, MAX_SOURCE)
            try:
                source = data.decode("utf-8")
            except UnicodeError as exc:
                raise StudyError("source_requires_utf8") from exc
            captured.append((name, data, analyze_source(source)))
    pack, pack_sha = task_pack()
    study = {
        "schema_version": SCHEMA, "study_id": study_id, "data_role": data_role,
        "evidence_policy": "static_or_reviewed",
        "task": {key: pack[key] for key in ("pack_id", "pack_version", "resolution_id")},
        "configurations": [{"id": "collection", "model": None, "prompt": None, "settings": None,
                            "selection_rule": "One supplied standalone slot per selected source path; origins and independence unknown."}],
        "artifacts": [], "assignments": [], "suites": [], "receipts": [],
        "runs": [], "revisions": [], "feedback": [], "selection": [],
    }
    study["task"]["pack_sha256"] = pack_sha
    for index, (name, data, analysis) in enumerate(captured, 1):
        artifact_id, assignment_id, run_id, revision_id = (f"{prefix}{index:03}" for prefix in ("A", "M", "R", "V"))
        study["artifacts"].append({"id": artifact_id, "path": "sources/" + name, "sha256": digest(data),
                                   "language": "python", "entry_point": pack["entry_point"],
                                   "origin": "project_fixture" if data_role == "fixture" else "supplied",
                                   "capture_status": "complete"})
        study["assignments"].append({
            "id": assignment_id, "artifact_id": artifact_id, "source_sha256": digest(data),
            "pack_sha256": pack_sha, "revision": 1,
            "status": "accepted" if analysis["status"] == "recognized" else "unresolved",
            "basis": "static_rule", "class_id": analysis["class_id"], "reason": analysis["reason"],
            "reviewer_ref": None, "evidence": analysis["evidence"], "rule_id": analysis["rule_id"],
        })
        study["runs"].append({"id": run_id, "configuration_id": "collection", "root_group_id": None,
                               "stop_reason": "unknown", "endpoint_revision_id": None})
        study["revisions"].append({"id": revision_id, "run_id": run_id, "ordinal": 0,
                                   "artifact_id": artifact_id, "parents": [], "missing_parents": [],
                                   "kind": "snapshot", "feedback_ids": []})
        study["selection"].append({"revision_id": revision_id, "assignment_id": assignment_id, "receipt_id": None})
    manifest = encoded(study)
    require(len(manifest) + sum(len(data) for _, data, _ in captured) <= MAX_TOTAL,
            "total_input_size_limit")
    # Validate and construct all outputs against the exact captured bytes before
    # creating an output directory. This avoids re-reading changing input files.
    payloads = {"sources/" + name: data for name, data, _ in captured}

    class CapturedDirectory:
        def read(self, relative, limit):
            data = payloads[relative]
            require(len(data) <= limit, "payload_size_limit")
            return data

    result = _inspect(study, CapturedDirectory(), digest(manifest))
    review = encoded(review_document(study, result))
    try:
        destination.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise StudyError("output_already_exists") from exc
    except OSError as exc:
        raise StudyError("output_directory_unavailable") from exc
    for relative, data in payloads.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        _write_new(target, data)
    _write_new(destination / "study.json", manifest)
    _write_new(destination / "review.json", review)
    return {"status": "prepared", "study_path": str(destination / "study.json"),
            "review_path": str(destination / "review.json"), "source_count": len(captured),
            "classification_coverage": result["ledger"]["classification_coverage"],
            "candidate_execution_performed": False, "test_receipts_created": 0}


def prepare_review(study_path, output):
    study, result = load_study(study_path)
    destination = Path(output).absolute()
    _write_new(destination, encoded(review_document(study, result)))
    return {"status": "review_prepared", "review_path": str(destination),
            "decisions_filled": 0, "source_count": len(study["artifacts"])}


def apply_review(study_path, review_path, output):
    source, review_file, destination = (Path(p).absolute() for p in (study_path, review_path, output))
    require(destination.parent == source.parent, "review_output_must_share_study_directory")
    require(not destination.exists() and not destination.is_symlink(), "output_already_exists")
    study, result = load_study(source)
    require(study["evidence_policy"] in {"reviewed_import", "static_or_reviewed"}, "review_policy_required")
    with InputDirectory(review_file.parent) as directory:
        review = json_bytes(directory.read(review_file.name, MAX_JSON))
    fields(review, "schema_version study_sha256 pack_sha256 entries")
    require(review["schema_version"] == REVIEW_SCHEMA, "unsupported_review_schema")
    require(review["study_sha256"] == result["study_sha256"], "stale_review_study")
    require(review["pack_sha256"] == study["task"]["pack_sha256"], "review_frame_mismatch")
    require(isinstance(review["entries"], list) and len(review["entries"]) <= 128, "review_count_limit")
    expected = {e["artifact_id"]: e for e in review_document(study, result)["entries"]}
    new = copy.deepcopy(study)
    seen, added, ids = set(), 0, {item["id"] for item in new["assignments"]}
    for entry in review["entries"]:
        fields(entry, "artifact_id source_sha256 current_assignment_id suggested_class_id "
               "decision basis class_id reason reviewer_ref evidence note")
        identifier(entry["artifact_id"])
        key = entry["artifact_id"]
        require(key in expected and key not in seen, "unknown_or_duplicate_review_artifact")
        seen.add(key)
        require(all(entry[k] == expected[key][k] for k in
                    ("source_sha256", "current_assignment_id", "suggested_class_id")), "stale_review_binding")
        if entry["decision"] is None:
            require(all(entry[k] == expected[key][k] for k in
                        ("basis", "class_id", "reason", "reviewer_ref", "evidence", "note")), "review_decision_missing")
            continue
        require(isinstance(entry["basis"], str)
                and entry["basis"] in {"human_review", "model_assisted", "unknown"}, "invalid_review_basis")
        counter = 1
        while f"review-{counter:04}" in ids:
            counter += 1
        assignment_id = f"review-{counter:04}"
        ids.add(assignment_id)
        revision = 1 + max((a["revision"] for a in study["assignments"] if a["artifact_id"] == key), default=0)
        assignment = {"id": assignment_id, "artifact_id": key, "source_sha256": entry["source_sha256"],
                      "pack_sha256": review["pack_sha256"], "revision": revision,
                      "status": entry["decision"], "basis": entry["basis"], "class_id": entry["class_id"],
                      "reason": entry["reason"], "reviewer_ref": entry["reviewer_ref"], "evidence": entry["evidence"]}
        if entry["note"] is not None:
            assignment["note"] = entry["note"]
        new["assignments"].append(assignment)
        revisions = {r["id"]: r for r in new["revisions"]}
        for selected in new["selection"]:
            if revisions[selected["revision_id"]]["artifact_id"] == key:
                selected["assignment_id"] = assignment_id
        added += 1
    require(added > 0, "no_review_decisions")
    payload = encoded(new)
    with InputDirectory(source.parent) as directory:
        updated = _inspect(new, directory, digest(payload))
    _write_new(destination, payload)
    return {"status": "review_applied", "study_path": str(destination), "assignments_appended": added,
            "prior_assignments_preserved": len(study["assignments"]),
            "classification_coverage": updated["ledger"]["classification_coverage"],
            "substantive_validation_performed": False}
