import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from structdet_code.errors import StudyError
from structdet_code.io import digest, json_bytes
from structdet_code.reporting import markdown
from structdet_code.study import inspect_study

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples/minimal"


class StudyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "study"
        shutil.copytree(FIXTURE, self.root, ignore=shutil.ignore_patterns("__pycache__"))
        self.path = self.root / "study.json"
        self.study = json.loads(self.path.read_text())

    def inspect(self):
        self.path.write_text(json.dumps(self.study))
        return inspect_study(self.path)

    def invalid(self, code=None):
        with self.assertRaises(StudyError) as raised:
            self.inspect()
        if code:
            self.assertEqual(raised.exception.code, code)

    def test_fixture_joint_views_match_independent_oracle(self):
        result = self.inspect()
        oracle = json.loads((self.root / "expected.json").read_text())
        self.assertEqual(result["ledger"]["selected_observations"], oracle["selected_observations"])
        for view, prefix in (("classified_all", "all"), ("classified_valid", "valid")):
            self.assertEqual(result["views"][view]["class_counts"], oracle[prefix + "_counts"])
            sci = result["views"][view]["sci"]
            self.assertEqual([sci["numerator"], sci["denominator"]], oracle[prefix + "_sci"])
        self.assertEqual(result["ledger"]["validity_states"]["passed_under_supplied_scope"], 5)
        self.assertEqual(result["ledger"]["assignment_states"], {"accepted": 5, "proposed": 1, "unresolved": 1})
        self.assertFalse(result["candidate_execution_performed"])

    def test_fix_changes_validity_without_creating_a_new_mechanism(self):
        self.study["selection"][0] = {"revision_id": "R1V1", "assignment_id": "M2", "receipt_id": "T-R1V1"}
        result = self.inspect()
        self.assertEqual(result["views"]["classified_valid"]["population_size"], 5)
        self.assertEqual(result["views"]["classified_all"]["sci"]["numerator"], 11)
        self.assertEqual(result["ledger"]["selected_observations"], 7)
        self.study["selection"][0] = {"revision_id": "R1V2", "assignment_id": "M2", "receipt_id": "T-R1V2"}
        repeated = self.inspect()
        self.assertEqual(result["views"], repeated["views"])
        self.assertEqual(repeated["ledger"]["no_op_revisions"], 1)
        self.assertEqual(repeated["ledger"]["selected_unique_source_bytes"], 6)

    def test_multiple_snapshots_of_one_run_cannot_inflate_selected_population(self):
        self.study["selection"].append({"revision_id": "R1V1", "assignment_id": "M2", "receipt_id": "T-R1V1"})
        self.invalid("multiple_selected_revisions_per_run")

    def test_model_proposal_cannot_become_an_accepted_assignment_by_status_alone(self):
        row = self.study["assignments"][-1]
        row.update(status="accepted", reason=None)
        self.invalid("assignment_basis_not_admissible")

    def test_fixture_cannot_be_relabelled_as_reviewed_empirical_data(self):
        self.study.update(data_role="descriptive", evidence_policy="reviewed_import")
        self.invalid("assignment_basis_not_admissible")

    def test_reviewed_import_is_record_qualified_without_claiming_independence(self):
        self.study.update(data_role="descriptive", evidence_policy="reviewed_import")
        for row in self.study["assignments"]:
            if row["status"] == "accepted":
                row.update(basis="human_review", reviewer_ref="supplied-reviewer-reference")
        for row in self.study["receipts"]:
            row["execution_basis"] = "external_report"
        result = self.inspect()
        self.assertEqual(result["claim_scope"], "supplied_review_records_only")
        self.assertFalse(result["substantive_validation_performed"])

    def test_unknown_and_empty_classified_population_stay_explicit(self):
        for row in self.study["assignments"]:
            row.update(status="unresolved", class_id=None, reason="schema_gap")
        result = self.inspect()
        self.assertEqual(result["ledger"]["selected_observations"], 7)
        self.assertEqual(result["views"]["classified_all"]["observed_support"], 0)
        self.assertEqual(result["views"]["classified_all"]["sci"]["status"], "undefined")
        self.assertEqual(result["ledger"]["unadmitted_reasons"], {"schema_gap": 7})

    def test_stale_source_and_assignment_bindings_are_rejected(self):
        self.study["assignments"][0]["source_sha256"] = "0" * 64
        self.invalid("assignment_source_mismatch")
        self.study = json.loads((FIXTURE / "study.json").read_text())
        source = self.root / "sources/insertion.py"
        source.write_text(source.read_text() + "\n# changed\n")
        self.invalid("source_digest_mismatch")

    def test_reclassification_requires_explicit_current_assignment_selection(self):
        new = copy.deepcopy(self.study["assignments"][1])
        new.update(id="M2-correction", revision=2, status="unresolved", class_id=None, reason="review_disagreement")
        self.study["assignments"].append(new)
        self.invalid("stale_assignment_selected")
        self.study["selection"][1]["assignment_id"] = new["id"]
        result = self.inspect()
        self.assertEqual(result["views"]["classified_all"]["population_size"], 4)
        self.assertEqual(result["ledger"]["selected_observations"], 7)

    def test_receipt_for_same_bytes_at_later_revision_cannot_certify_earlier_revision(self):
        self.study["selection"][0] = {"revision_id": "R1V1", "assignment_id": "M2", "receipt_id": "T-R1V2"}
        self.invalid("selection_receipt_wrong_revision")

    def test_changed_suite_and_incomplete_passing_receipts_are_rejected(self):
        self.study["receipts"][1]["suite_sha256"] = "0" * 64
        self.invalid("receipt_suite_binding_mismatch")
        self.study["receipts"][1]["suite_sha256"] = self.study["suites"][0]["sha256"]
        self.study["receipts"][1].update(attempted=3, completed=3, passed=3)
        self.invalid("incomplete_passing_receipt")

    def test_noop_and_parent_chronology_are_checked(self):
        self.study["revisions"][-2]["kind"] = "edit"
        self.invalid("revision_change_kind_mismatch")
        self.study["revisions"][-2]["kind"] = "no_op"
        self.study["revisions"][0]["parents"] = ["R1V2"]
        self.invalid("parent_order_violation")

    def test_feedback_cannot_cross_revision_or_withheld_boundary(self):
        self.study["feedback"][0]["receipt_id"] = "T-R1V1"
        self.invalid("feedback_receipt_wrong_revision")
        self.study["feedback"][0]["receipt_id"] = "T-R1V0"
        self.study["receipts"][0]["visibility"] = "withheld"
        self.invalid("feedback_exposes_withheld_or_unknown_receipt")

    def test_explicit_missing_history_preserves_actual_ordinals(self):
        self.study["revisions"][-3].update(ordinal=5, parents=["lost-parent"], missing_parents=["lost-parent"], feedback_ids=[])
        self.study["revisions"][-2]["ordinal"] = 8
        result = self.inspect()
        history = result["recorded_histories"][0]
        self.assertEqual([r["ordinal"] for r in history["revisions"]], [0, 5, 8])
        self.assertEqual(history["revisions"][1]["missing_parents"], ["lost-parent"])
        self.assertEqual(history["ordinal_gaps"], [{"after": 0, "before": 5}, {"after": 5, "before": 8}])
        self.assertEqual(result["ledger"]["selected_observations"], 7)

    def test_unsafe_paths_symlinks_and_executable_hooks_are_rejected(self):
        original = self.study["artifacts"][0]["path"]
        for unsafe in ("../outside.py", "/tmp/outside.py", "sources/../x.py", "sources\\x.py", "./sources/x.py"):
            with self.subTest(path=unsafe):
                self.study["artifacts"][0]["path"] = unsafe
                self.invalid("unsafe_path")
        self.study["artifacts"][0]["path"] = original
        candidate = self.root / original
        target = self.root / "outside.py"
        candidate.rename(target)
        candidate.symlink_to(target)
        self.invalid("payload_unavailable_or_unsafe")
        self.study["validator_command"] = "echo should-never-execute"
        self.invalid("unexpected_or_missing_field")

    def test_candidate_side_effect_is_never_executed_during_inspection(self):
        marker = self.root / "executed.txt"
        candidate = self.root / self.study["artifacts"][-1]["path"]
        candidate.write_text(f"open({str(marker)!r}, 'w').write('unexpected execution')\n")
        sha = digest(candidate.read_bytes())
        self.study["artifacts"][-1]["sha256"] = sha
        assignment = self.study["assignments"][-1]
        assignment.update(source_sha256=sha, status="unresolved", class_id=None, reason="unsupported_syntax")
        assignment["evidence"] = []
        for receipt in self.study["receipts"]:
            if receipt["artifact_id"] == "A7":
                receipt["source_sha256"] = sha
        self.inspect()
        self.assertFalse(marker.exists())

    def test_partial_source_cannot_have_an_accepted_assignment(self):
        self.study["artifacts"][0]["capture_status"] = "partial"
        self.invalid("accepted_partial_source")

    def test_duplicate_json_keys_nonfinite_numbers_and_excess_depth_fail(self):
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":1e999}', b'[' * 26 + b'0' + b']' * 26):
            with self.subTest(raw=raw), self.assertRaises(StudyError):
                json_bytes(raw)

    def test_cli_and_markdown_use_the_same_canonical_values(self):
        result = self.inspect()
        rendered = markdown(result)
        self.assertIn("| classified_all | 5 | 3 | 11/25 | 14/25 |", rendered)
        command = [sys.executable, "-m", "structdet_code", "inspect", "--study", str(self.path)]
        ran = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(ran.stdout)["views"], result["views"])
        self.study["task"]["pack_version"] = "different"
        self.path.write_text(json.dumps(self.study))
        ran = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(ran.returncode, 2)
        self.assertEqual(json.loads(ran.stderr)["code"], "unsupported_or_changed_task_frame")
        self.assertNotIn("Traceback", ran.stderr)


if __name__ == "__main__":
    unittest.main()
