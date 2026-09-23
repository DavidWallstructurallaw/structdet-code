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
from structdet_code.evidence import prepare_evidence
from structdet_code.io import digest
from structdet_code.reporting import markdown
from structdet_code.study import inspect_study
from structdet_code.trace import analyze_trace
from structdet_code.trace_reporting import trace_markdown
from structdet_code.workflow import encoded

ROOT = Path(__file__).resolve().parents[1]
FAILED = ["T04", "T05", "T06", "T07", "T08", "T10"]


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "example"
        shutil.copytree(ROOT / "examples/interventions", self.root)
        self.study_path = self.root / "study.json"
        self.design_path = self.root / "design.json"
        self.evidence_path = self.root / "evidence.json"
        self.study = json.loads(self.study_path.read_bytes())
        self.design = json.loads(self.design_path.read_bytes())
        self.evidence = json.loads(self.evidence_path.read_bytes())

    def save(self):
        raw = encoded(self.study)
        self.study_path.write_bytes(raw)
        self.design["study_sha256"] = self.evidence["study_sha256"] = digest(raw)
        self.design_path.write_bytes(encoded(self.design))
        self.evidence_path.write_bytes(encoded(self.evidence))

    def analyze(self):
        self.save()
        return analyze_trace(self.study_path, self.design_path, self.evidence_path)

    def error(self, code, call=None):
        with self.assertRaises(StudyError) as raised:
            (call or self.analyze)()
        self.assertEqual(raised.exception.code, code)

    def event(self, key):
        return next(e for e in self.evidence["interventions"] if e["id"] == key)

    def test_reappearance_copy_claim_and_withheld_content_are_separate(self):
        result = self.analyze()
        events = {e["id"]: e for e in result["evidence"]["interventions"]}
        self.assertEqual(len(events), 9)
        reference, withheld = events["I1-reference"], events["I2-withheld"]
        for e in (reference, withheld, events["I2-alternate"]):
            self.assertEqual((e["prior_class"], e["subsequent_class"]), ("DIST-FIFO", "DIST-RELAX"))
            self.assertEqual(e["selected_path_relation"], "observed_again")
            self.assertFalse(e["causal_effect_estimated"])
            self.assertFalse(e["autonomous_discovery_established"])
            self.assertEqual(e["external_recovery_rate"]["status"], "not_estimated")
        self.assertEqual(reference["reuse_claim"], "copied")
        self.assertEqual(reference["exact_material_matches"], ["reference"])
        self.assertTrue(reference["agent_visible_association"])
        self.assertEqual(withheld["exact_material_matches"], ["reference"])
        self.assertFalse(withheld["agent_visible_association"])
        self.assertEqual([r["usage"]["generation_records"] for r in result["trajectories"]], [1, 1])
        self.assertEqual([len(r["revisions"]) for r in result["trajectories"]], [3, 3])

    def test_different_mechanisms_can_have_identical_failed_inputs(self):
        result = self.analyze()["evidence"]["failure_profiles"]
        pair = next(p for p in result["pairs"] if (p["left"], p["right"]) == ("P-E-I2-V0", "P-E-I2-V1"))
        self.assertEqual(pair["both_failed"], FAILED)
        self.assertEqual(pair["left_failed_right_passed"], [])
        self.assertEqual(pair["right_failed_left_passed"], [])
        self.assertFalse(pair["same_source_bytes"])
        self.assertTrue(pair["same_run"])
        self.assertFalse(pair["failure_independence_established"])
        self.assertTrue(pair["complete_suite_both"])
        self.assertEqual(pair["both_completed"], 10)
        fixed = next(p for p in result["pairs"] if (p["left"], p["right"]) == ("P-E-I2-V1", "P-E-I2-V2"))
        self.assertEqual(fixed["left_failed_right_passed"], FAILED)
        self.assertEqual(fixed["both_failed"], [])

    def test_partial_outcomes_compare_only_jointly_completed_cases(self):
        profile = next(p for p in self.evidence["failure_profiles"] if p["receipt_id"] == "E-I2-V1")
        for o in profile["outcomes"]:
            if o["id"] == "T04":
                o["status"] = "not_completed"
            if o["id"] == "T05":
                o["status"] = "not_attempted"
        receipt = next(r for r in self.study["receipts"] if r["id"] == "E-I2-V1")
        receipt.update(status="timeout", attempted=9, completed=8)
        pair = next(p for p in self.analyze()["evidence"]["failure_profiles"]["pairs"]
                    if (p["left"], p["right"]) == ("P-E-I2-V0", "P-E-I2-V1"))
        self.assertEqual(pair["both_completed"], 8)
        self.assertFalse(pair["complete_suite_both"])
        self.assertEqual(pair["left_failures_other_unobserved"], ["T04", "T05"])
        self.assertEqual(pair["left_failed_right_passed"], [])
        self.assertEqual(pair["both_failed"], ["T06", "T07", "T08", "T10"])

    def test_distinct_failures_require_an_observed_pass_on_the_other_side(self):
        profile = next(p for p in self.evidence["failure_profiles"] if p["receipt_id"] == "E-I2-V1")
        for row in profile["outcomes"]:
            if row["id"] == "T04":
                row["status"] = "passed"
            if row["id"] == "T01":
                row["status"] = "failed"
        pair = next(p for p in self.analyze()["evidence"]["failure_profiles"]["pairs"]
                    if (p["left"], p["right"]) == ("P-E-I2-V0", "P-E-I2-V1"))
        self.assertEqual(pair["left_failed_right_passed"], ["T04"])
        self.assertEqual(pair["right_failed_left_passed"], ["T01"])
        self.assertEqual(pair["both_failed"], ["T05", "T06", "T07", "T08", "T10"])

    def test_scope_and_unknown_visibility_block_failure_pairing(self):
        original = deepcopy(self.study)
        for field, value in (("visibility", "feedback"), ("visibility", "unknown"),
                             ("execution_basis", "external_report"), ("environment", {"python": "other", "platform": "Linux", "runner": "other"})):
            with self.subTest(field=field, value=value):
                self.study = deepcopy(original)
                receipt = next(r for r in self.study["receipts"] if r["id"] == "E-I2-V1")
                receipt[field] = value
                profiles = self.analyze()["evidence"]["failure_profiles"]
                self.assertEqual(len(profiles["profiles"]), 4)
                pair = next(p for p in profiles["pairs"] if (p["left"], p["right"]) == ("P-E-I2-V0", "P-E-I2-V1"))
                self.assertEqual(pair["status"], "unavailable")
                self.assertNotIn("both_failed", pair)

    def test_profile_case_roster_counts_duplicates_and_bounds(self):
        original = deepcopy(self.evidence)
        changes = [
            (lambda d: d["failure_profiles"][0]["outcomes"].pop(), "profile_case_roster_mismatch"),
            (lambda d: d["failure_profiles"][0]["outcomes"][0].update(status="failed"), "profile_receipt_counts_mismatch"),
            (lambda d: d["failure_profiles"][0]["outcomes"][0].update(status="maybe"), "invalid_enum"),
            (lambda d: d["failure_profiles"].append({**d["failure_profiles"][0], "id": "Duplicate"}), "duplicate_profile_receipt"),
            (lambda d: d["failure_profiles"][0].update(receipt_id="absent"), "profile_receipt_missing"),
            (lambda d: d.update(failure_profiles=[d["failure_profiles"][0]] * 33), "record_count_limit"),
        ]
        for change, code in changes:
            with self.subTest(code=code):
                self.evidence = deepcopy(original)
                change(self.evidence)
                self.error(code)

    def test_intervention_ancestry_order_and_missing_refs_rejected(self):
        original = deepcopy(self.evidence)
        changes = [
            ({"after_revision_id": "I2-V1"}, "intervention_not_between_ancestors"),
            ({"after_revision_id": "I1-V2"}, "intervention_not_between_ancestors"),
            ({"before_revision_id": "I2-V2"}, "intervention_run_mismatch"),
            ({"order": 2}, "duplicate_intervention_order"),
            ({"order": True}, "invalid_integer"),
            ({"material_ids": ["missing"]}, "intervention_material_missing"),
            ({"after_revision_id": None}, "intervention_start_requires_root_prompt"),
            ({"kind": "other", "reuse_claim": "copied"}, "reuse_claim_without_reference"),
        ]
        for change, code in changes:
            with self.subTest(code=code):
                self.evidence = deepcopy(original)
                self.event("I1-reference").update(change)
                self.error(code)
        self.evidence = deepcopy(original)
        self.event("I1-test0")["order"] = 20
        self.error("intervention_order_conflicts_with_revisions")

    def test_feedback_cannot_be_promoted_or_hidden_by_sidecar(self):
        self.event("I1-test0")["visibility"] = "withheld"
        self.error("intervention_visibility_conflict")
        self.event("I1-test0").update(visibility="visible", feedback_ids=["F-I2-V0"])
        self.error("intervention_feedback_binding_mismatch")
        self.event("I1-test0")["feedback_ids"] = []
        self.error("test_intervention_needs_feedback")

    def test_unknown_material_and_independence_claim_remain_unverified(self):
        material = next(m for m in self.evidence["materials"] if m["id"] == "reference")
        material.update(path=None, sha256=None, source_ref=None, independence_claim="claimed_independent")
        result = self.analyze()["evidence"]
        public = next(m for m in result["materials"] if m["id"] == "reference")
        self.assertFalse(public["bytes_captured"])
        self.assertFalse(public["independence_verified"])
        event = next(e for e in result["interventions"] if e["id"] == "I1-reference")
        self.assertEqual(event["material_bytes_unavailable"], ["reference"])
        self.assertEqual(event["exact_material_matches"], [])
        self.assertEqual(event["reuse_claim"], "copied")

    def test_path_exclusion_and_unresolved_classes_are_not_discoveries(self):
        self.design["runs"][0]["path"] = None
        result = self.analyze()
        event = next(e for e in result["evidence"]["interventions"] if e["id"] == "I1-reference")
        self.assertEqual(event["selected_path_relation"], "outside_selected_path")
        self.assertFalse(event["agent_visible_association"])
        self.design["runs"][0]["path"] = ["I1-V0", "I1-V1", "I1-V2"]
        next(a for a in self.design["assessments"] if a["revision_id"] == "I1-V2")["assignment_id"] = None
        event = next(e for e in self.analyze()["evidence"]["interventions"] if e["id"] == "I1-reference")
        self.assertEqual(event["selected_path_relation"], "unresolved_assignment")
        self.assertIsNone(event["subsequent_class"])

    def test_static_receipt_selection_is_disclosed(self):
        self.save()
        result = inspect_study(self.study_path, self.evidence_path)
        selected = [p["receipt_id"] for p in result["evidence"]["failure_profiles"]["profiles"] if p["selected_for_analysis"]]
        self.assertEqual(selected, ["E-I2-V2"])
        self.assertIn("Finite failure profiles", markdown(result))
        self.assertTrue(all(e["selected_path_relation"] == "not_traced" for e in result["evidence"]["interventions"]))

    def test_material_tamper_symlinks_and_passive_private_content(self):
        path = self.root / "materials/reference.py"
        raw = path.read_bytes()
        path.write_bytes(raw + b"\n")
        self.error("material_digest_mismatch")
        path.unlink()
        path.symlink_to(self.root / "sources/relax_good.py")
        self.error("payload_unavailable_or_unsafe")
        path.unlink()
        marker = self.root / "EXECUTED"
        private = f"PRIVATE_PROMPT_SENTINEL\nopen({str(marker)!r}, 'w').write('unsafe')\n".encode()
        path.write_bytes(private)
        next(m for m in self.evidence["materials"] if m["id"] == "reference")["sha256"] = digest(private)
        result = self.analyze()
        self.assertFalse(marker.exists())
        self.assertNotIn("PRIVATE_PROMPT_SENTINEL", json.dumps(result) + trace_markdown(result))
        self.assertNotIn(str(marker), json.dumps(result))

    def test_stale_schema_unknown_hooks_and_output_limit(self):
        original = deepcopy(self.evidence)
        self.evidence["schema_version"] = "future"
        self.error("unsupported_evidence_schema")
        self.evidence = deepcopy(original)
        self.evidence["plugin"] = "execute-this"
        self.error("unexpected_or_missing_field")
        self.evidence = deepcopy(original)
        self.save()
        self.study["study_id"] = "corrected"
        self.study_path.write_bytes(encoded(self.study))
        self.error("evidence_study_binding_mismatch", lambda: inspect_study(self.study_path, self.evidence_path))
        with patch("structdet_code.evidence.MAX_RESULT", 100):
            self.error("analysis_result_size_limit")

    def test_template_stays_empty_and_does_not_overwrite(self):
        output = self.root / "blank.json"
        prepare_evidence(self.study_path, output)
        blank = json.loads(output.read_bytes())
        self.assertEqual([blank[k] for k in ("materials", "interventions", "failure_profiles")], [[], [], []])
        self.error("output_already_exists", lambda: prepare_evidence(self.study_path, output))
        result = inspect_study(self.study_path, output)
        self.assertEqual(result["evidence"]["interventions"], [])

    def test_cli_json_markdown_and_invalid_evidence(self):
        args = ["trace", "--study", str(self.study_path), "--design", str(self.design_path),
                "--evidence", str(self.evidence_path)]
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(main(args), 0)
        expected = json.loads(out.getvalue())
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(main(args + ["--format", "markdown"]), 0)
        self.assertEqual(out.getvalue(), trace_markdown(expected))
        self.assertIn("observed_again", out.getvalue())
        self.evidence_path.write_text('{"schema_version": "wrong"}')
        with redirect_stdout(io.StringIO()), redirect_stderr(err):
            self.assertEqual(main(args), 2)
        self.assertNotIn("Traceback", err.getvalue())


if __name__ == "__main__":
    unittest.main()
