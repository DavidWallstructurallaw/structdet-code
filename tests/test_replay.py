from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from structdet_code.__main__ import main
from structdet_code.errors import StudyError
from structdet_code.io import digest
from structdet_code.replay import create_snapshot, replay_snapshot, software_identity
from structdet_code.workflow import encoded, prepare_sources

ROOT = Path(__file__).resolve().parents[1]


class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bundle = self.root / "bundle"
        self.args = {"study": str(ROOT / "examples/interventions/study.json"),
                     "design": str(ROOT / "examples/interventions/design.json"),
                     "evidence": str(ROOT / "examples/interventions/evidence.json")}

    def create(self):
        return create_snapshot("trace", self.args, self.bundle)

    def error(self, code, call=None):
        with self.assertRaises(StudyError) as raised:
            (call or (lambda: replay_snapshot(self.bundle)))()
        self.assertEqual(raised.exception.code, code)

    def manifest(self):
        return json.loads((self.bundle / "snapshot.json").read_bytes())

    def save_manifest(self, document):
        (self.bundle / "snapshot.json").write_bytes(encoded(document))

    def rebind_file(self, name, raw):
        (self.bundle / name).write_bytes(raw)
        manifest = self.manifest()
        item = next(i for i in manifest["files"] if i["path"] == name)
        item.update(sha256=digest(raw), bytes=len(raw))
        self.save_manifest(manifest)

    def test_all_three_actions_recompute_exact_json_and_markdown(self):
        cases = [
            ("inspect", {"study": str(ROOT / "examples/static/study.json")}),
            ("compare", {"left": str(ROOT / "examples/graph/left/study.json"),
                         "right": str(ROOT / "examples/graph/right/study.json"),
                         "design": str(ROOT / "examples/graph/comparison.json")}),
            ("trace", self.args),
        ]
        for action, arguments in cases:
            with self.subTest(action=action):
                target = self.root / action
                saved = create_snapshot(action, arguments, target)
                replayed = replay_snapshot(target)
                self.assertEqual(replayed["status"], "replay_verified")
                self.assertEqual(replayed["result_sha256"], saved["result_sha256"])
                self.assertEqual(replayed["result"], json.loads((target / "result.json").read_bytes()))
                self.assertFalse(replayed["candidate_execution_performed"])
                self.assertFalse(replayed["external_calls_performed"])
                self.assertFalse(replayed["authenticity_established"])
                self.assertEqual((target / "snapshot.json").stat().st_mode & 0o777, 0o600)
                self.assertEqual(target.stat().st_mode & 0o777, 0o700)

    def test_relocated_bundle_needs_no_original_sources(self):
        source = self.root / "source"
        shutil.copytree(ROOT / "examples/interventions", source)
        arguments = {k: str(source / Path(v).name) for k, v in self.args.items()}
        create_snapshot("trace", arguments, self.bundle)
        shutil.rmtree(source)
        relocated = self.root / "relocated"
        self.bundle.rename(relocated)
        result = replay_snapshot(relocated)
        self.assertEqual(result["status"], "replay_verified")
        self.assertEqual(result["result"]["evidence"]["interventions"][-1]["visibility"], "withheld")

    def test_byte_change_is_detected_before_recomputation(self):
        self.create()
        target = self.bundle / "inputs/study/sources/fifo_good.py"
        target.write_bytes(target.read_bytes() + b"\n")
        self.error("replay_file_binding_mismatch")

    def test_rehashed_source_still_requires_valid_study_binding(self):
        self.create()
        name = "inputs/study/sources/fifo_good.py"
        self.rebind_file(name, (self.bundle / name).read_bytes() + b"\n")
        self.error("source_digest_mismatch")

    def test_rehashed_outputs_must_equal_new_computation(self):
        self.create()
        original_json = (self.bundle / "result.json").read_bytes()
        value = json.loads(original_json)
        value["cohorts"]["checkpoints"][0]["available"]["observed"] = 99
        self.rebind_file("result.json", encoded(value))
        self.error("replay_result_mismatch")
        self.rebind_file("result.json", original_json)
        self.rebind_file("result.md", (self.bundle / "result.md").read_bytes() + b"Different conclusion.\n")
        self.error("replay_result_mismatch")

    def test_method_runtime_version_and_code_changes_fail_closed(self):
        self.create()
        original = self.manifest()
        for key in ("method", "version", "python", "platform", "implementation"):
            with self.subTest(key=key):
                changed = deepcopy(original)
                changed["software"][key] = "other"
                self.save_manifest(changed)
                self.error("replay_software_mismatch")
        self.save_manifest(original)
        changed = software_identity()
        changed["files"]["metrics.py"] = "0" * 64
        with patch("structdet_code.replay.software_identity", return_value=changed):
            self.error("replay_software_mismatch")

    def test_unknown_commands_fields_and_hooks_are_rejected(self):
        self.create()
        original = self.manifest()
        for action in ("exec", ["trace"], None):
            changed = deepcopy(original)
            changed["action"] = action
            self.save_manifest(changed)
            self.error("unsupported_snapshot_action")
        changed = deepcopy(original)
        changed["arguments"]["validator"] = "some/module.py"
        self.save_manifest(changed)
        self.error("unexpected_or_missing_field")
        self.error("unexpected_or_missing_field", lambda: create_snapshot(
            "inspect", {"study": self.args["study"], "design": self.args["design"]}, self.root / "wrong"))
        self.assertFalse((self.root / "wrong").exists())

    def test_paths_symlinks_and_duplicate_inventory_are_rejected(self):
        self.create()
        original = self.manifest()
        for name in ("../escape", "/tmp/escape", "inputs//bad", "inputs\\bad"):
            changed = deepcopy(original)
            changed["files"][0]["path"] = name
            self.save_manifest(changed)
            self.error("unsafe_path")
        changed = deepcopy(original)
        changed["files"].append(deepcopy(changed["files"][0]))
        self.save_manifest(changed)
        self.error("duplicate_snapshot_file")
        self.save_manifest(original)
        target = self.bundle / "inputs/study/sources/fifo_good.py"
        target.unlink()
        target.symlink_to(ROOT / "examples/interventions/sources/fifo_good.py")
        self.error("payload_unavailable_or_unsafe")

    def test_unlisted_payload_cannot_satisfy_a_study_reference(self):
        self.create()
        manifest = self.manifest()
        manifest["files"] = [f for f in manifest["files"] if f["path"] != "inputs/study/sources/fifo_good.py"]
        self.save_manifest(manifest)
        self.assertTrue((self.bundle / "inputs/study/sources/fifo_good.py").is_file())
        self.error("payload_unavailable_or_unsafe")

    def test_trace_order_and_evidence_are_bound_even_with_same_histogram(self):
        self.create()
        name = "inputs/evidence/evidence.json"
        document = json.loads((self.bundle / name).read_bytes())
        event = next(e for e in document["interventions"] if e["id"] == "I2-withheld")
        event["visibility"] = "unknown"
        self.rebind_file(name, encoded(document))
        self.error("replay_result_mismatch")

    def test_missing_results_malformed_json_and_bounded_files(self):
        self.create()
        original = self.manifest()
        changed = deepcopy(original)
        changed["files"] = [f for f in changed["files"] if f["path"] != "result.md"]
        self.save_manifest(changed)
        self.error("snapshot_result_missing")
        self.save_manifest(original)
        with patch("structdet_code.replay.MAX_FILES", 1):
            self.error("snapshot_file_limit")
        (self.bundle / "snapshot.json").write_text('{"x":1,"x":2}')
        self.error("duplicate_json_key")
        (self.bundle / "snapshot.json").write_text('{"x":NaN}')
        self.error("nonfinite_json_number")
        self.save_manifest(original)
        name = "result.json"
        with (self.bundle / name).open("wb") as stream:
            stream.truncate(4_194_305)
        self.error("payload_size_limit")

    def test_capture_refuses_overwrite_invalid_inputs_and_material_tamper(self):
        self.create()
        original = (self.bundle / "snapshot.json").read_bytes()
        self.error("output_already_exists", self.create)
        self.assertEqual((self.bundle / "snapshot.json").read_bytes(), original)
        bad = self.root / "bad.json"
        bad.write_text('{"artifacts":[{"id":"a","path":null}],"suites":[]}')
        self.error("unsafe_path", lambda: create_snapshot("inspect", {"study": str(bad)}, self.root / "bad-output"))
        self.assertFalse((self.root / "bad-output").exists())
        name = "inputs/evidence/materials/reference.py"
        self.rebind_file(name, (self.bundle / name).read_bytes() + b"\n")
        self.error("material_digest_mismatch")

    def test_candidate_is_passive_in_prepare_snapshot_and_replay(self):
        candidates = self.root / "candidates"
        candidates.mkdir()
        marker = self.root / "EXECUTED"
        source = f"open({str(marker)!r}, 'w').write('unsafe')\ndef sort_values(values):\n    return values\n"
        (candidates / "probe.py").write_text(source)
        prepared = self.root / "prepared"
        prepare_sources(candidates, prepared)
        create_snapshot("inspect", {"study": str(prepared / "study.json")}, self.bundle)
        replay_snapshot(self.bundle)
        self.assertFalse(marker.exists())

    def test_cli_round_trip_and_stable_error_format(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(main(["snapshot", "--action", "trace", "--study", self.args["study"],
                                   "--design", self.args["design"], "--evidence", self.args["evidence"],
                                   "--output", str(self.bundle)]), 0)
        self.assertTrue(json.loads(out.getvalue())["contains_private_inputs"])
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(main(["replay", "--bundle", str(self.bundle), "--format", "markdown"]), 0)
        self.assertTrue(out.getvalue().startswith("Exact offline replay verified."))
        (self.bundle / "snapshot.json").write_text("{}")
        err = io.StringIO()
        with redirect_stderr(err), redirect_stdout(io.StringIO()):
            self.assertEqual(main(["replay", "--bundle", str(self.bundle)]), 2)
        self.assertEqual(json.loads(err.getvalue())["status"], "invalid")
        self.assertNotIn("Traceback", err.getvalue())


if __name__ == "__main__":
    unittest.main()
