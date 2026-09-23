from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from fractions import Fraction
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from structdet_code.__main__ import main
from structdet_code.errors import StudyError
from structdet_code.graph_rules import FIFO
from structdet_code.io import digest
from structdet_code.study import load_study
from structdet_code.trace import analyze_trace, prepare_trace, trace_document
from structdet_code.trace_reporting import trace_markdown
from structdet_code.workflow import encoded, prepare_sources

ROOT = Path(__file__).resolve().parents[1]


class TraceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "trace"
        shutil.copytree(ROOT / "examples/trace", self.root)
        self.study_path = self.root / "study.json"
        self.design_path = self.root / "design.json"
        self.study = json.loads(self.study_path.read_bytes())
        self.design = json.loads((self.root / "concentration.json").read_bytes())

    def save_study(self):
        raw = encoded(self.study)
        self.study_path.write_bytes(raw)
        self.design["study_sha256"] = digest(raw)

    def analyze(self):
        self.design_path.write_bytes(encoded(self.design))
        return analyze_trace(self.study_path, self.design_path)

    def assert_code(self, code, call=None):
        with self.assertRaises(StudyError) as raised:
            (call or self.analyze)()
        self.assertEqual(raised.exception.code, code)

    def row(self, revision_id):
        return next(row for row in self.study["revisions"] if row["id"] == revision_id)

    def assessment(self, revision_id):
        return next(row for row in self.design["assessments"] if row["revision_id"] == revision_id)

    def trace_run(self, run_id):
        return next(row for row in self.design["runs"] if row["run_id"] == run_id)

    def only_runs(self, identities):
        selected = set(identities)
        revisions = {row["id"] for row in self.study["revisions"] if row["run_id"] in selected}
        self.design["runs"] = [row for row in self.design["runs"] if row["run_id"] in selected]
        self.design["assessments"] = [row for row in self.design["assessments"] if row["revision_id"] in revisions]

    def set_artifact(self, revision_id, artifact_id):
        artifact = next(row for row in self.study["artifacts"] if row["id"] == artifact_id)
        self.row(revision_id)["artifact_id"] = artifact_id
        self.assessment(revision_id)["assignment_id"] = "M-" + artifact_id
        for receipt in self.study["receipts"]:
            if receipt["revision_id"] == revision_id:
                receipt.update(artifact_id=artifact_id, source_sha256=artifact["sha256"])
        for selection in self.study["selection"]:
            if selection["revision_id"] == revision_id:
                selection["assignment_id"] = "M-" + artifact_id
        artifacts = {row["id"]: row for row in self.study["artifacts"]}
        revisions = {row["id"]: row for row in self.study["revisions"]}
        for row in self.study["revisions"]:
            if row["kind"] in {"edit", "no_op"} and not row["missing_parents"]:
                parent = revisions[row["parents"][0]]
                same = artifacts[row["artifact_id"]]["sha256"] == artifacts[parent["artifact_id"]]["sha256"]
                row["kind"] = "no_op" if same else "edit"

    def test_six_run_exact_oracle_keeps_all_and_valid_cross_tabs(self):
        result = self.analyze()
        points = result["cohorts"]["checkpoints"]
        self.assertEqual(result["cohorts"]["status"], "compatible_descriptive")
        self.assertEqual(result["cohorts"]["matched_run_ids"], ["C1", "C2", "C3", "C4", "C5", "C6"])
        expected_all = [{"DIST-FIFO": 3, "DIST-SETTLE": 2, "DIST-RELAX": 1},
                        {"DIST-FIFO": 4, "DIST-SETTLE": 2}, {"DIST-FIFO": 6}]
        expected_valid = [{"DIST-FIFO": 2}, {"DIST-FIFO": 3, "DIST-SETTLE": 1}, {"DIST-FIFO": 6}]
        for point, counts, valid, sci, passed in zip(points, expected_all, expected_valid,
                [Fraction(7, 18), Fraction(5, 9), Fraction(1)], [2, 4, 6]):
            for cohort in ("available", "matched"):
                population = point[cohort]
                metrics = population["views"]["classified_all"]
                self.assertEqual(metrics["class_counts"], counts)
                self.assertEqual(Fraction(metrics["sci"]["numerator"], metrics["sci"]["denominator"]), sci)
                self.assertEqual(population["views"]["classified_valid"]["class_counts"], valid)
                self.assertEqual(population["observed_pass_fraction"], {"numerator": passed, "denominator": 6, "value": passed / 6})
                self.assertEqual(population["classification_coverage_observed"]["value"], 1)
        changes = result["cohorts"]["changes"]["matched"]
        self.assertEqual([c["views"]["classified_all"]["later_minus_earlier"]["sci"]["value"] for c in changes], [1 / 6, 4 / 9])
        for change in changes:
            self.assertEqual(change["joint"]["status"], "available")
            self.assertEqual(change["joint"]["finite_pass_direction"], "rising")
            self.assertEqual(change["joint"]["support_direction"], "falling")
            self.assertEqual(change["joint"]["concentration_direction"], "rising")
        self.assertEqual(result["cohorts"]["path_transition_states"]["mechanism_switch"], 3)
        self.assertEqual(sum(row["count"] for row in result["cohorts"]["path_transition_counts"]), 12)
        self.assertEqual(changes[0]["observed_set_changes"]["classified_all"]["no_longer_observed"], ["DIST-RELAX"])
        self.assertFalse(result["candidate_execution_performed"])
        self.assertEqual(result["structural_half_life"]["status"], "not_applicable")

    def test_correctness_can_rise_with_stable_support_and_concentration(self):
        self.design = json.loads((self.root / "stable.json").read_bytes())
        result = self.analyze()
        for change in result["cohorts"]["changes"]["matched"]:
            self.assertEqual(change["joint"], {"status": "available", "reasons": [], "finite_pass_direction": "rising",
                                               "support_direction": "stable", "concentration_direction": "stable"})
            self.assertEqual(change["views"]["classified_all"]["later_minus_earlier"]["sci"]["numerator"], 0)

    def test_attrition_does_not_forward_fill_or_become_matched_mechanism_loss(self):
        self.design = json.loads((self.root / "attrition.json").read_bytes())
        result = self.analyze()
        self.assertEqual(result["roster"]["explicitly_unrecorded_runs"], ["A6"])
        cohort = result["cohorts"]
        self.assertEqual(cohort["matched_run_ids"], ["A3", "A4"])
        self.assertEqual([p["available"]["observed"] for p in cohort["checkpoints"]], [5, 2, 2])
        later = cohort["checkpoints"][1]
        self.assertEqual(later["availability_states"], {"observed": 2, "run_unrecorded": 1, "stopped_success": 2, "stopped_timeout": 1})
        self.assertEqual(later["risk_set"]["known_stopped_before"], ["A1", "A2", "A5"])
        self.assertEqual(later["risk_set"]["known_reached"], ["A3", "A4"])
        self.assertEqual(later["risk_set"]["reach_unknown"], ["A6"])
        available = cohort["changes"]["available"][0]
        self.assertIn("cohort_membership_changed", available["joint"]["reasons"])
        self.assertEqual(available["observed_set_changes"]["classified_all"]["status"], "inventory_only")
        matched = cohort["changes"]["matched"][0]
        self.assertEqual(matched["joint"]["finite_pass_direction"], "rising")
        self.assertEqual(matched["joint"]["support_direction"], "stable")
        self.assertEqual(matched["views"]["classified_all"]["later_minus_earlier"]["observed_support"], 0)
        self.assertEqual(cohort["checkpoints"][0]["matched"]["views"]["classified_valid"]["sci"]["status"], "undefined")

    def test_test_only_repetition_and_no_op_do_not_add_generations(self):
        result = self.analyze()
        first = result["trajectories"][0]
        self.assertEqual(first["usage"]["recorded_revisions"], 3)
        self.assertEqual(first["usage"]["generation_records"], 1)
        self.assertEqual(first["usage"]["no_op_revisions"], 2)
        self.assertEqual(first["usage"]["test_receipts"], 6)
        self.assertEqual(first["usage"]["test_case_attempts"], 60)
        self.assertEqual(len(first["revisions"][-1]["test_observations"]), 2)
        self.assertEqual(first["transition_states"], {"unchanged_source_and_mechanism": 2})
        self.assertEqual(result["cohorts"]["checkpoints"][2]["matched"]["observed"], 6)

    def test_template_uses_explicit_endpoint_and_never_picks_best_receipt(self):
        path = self.root / "template.json"
        prepare_trace(self.study_path, path)
        template = json.loads(path.read_bytes())
        self.assertIsNone(template["configuration_id"])
        self.assertIsNone(template["protocol_ref"])
        self.assertEqual(template["checkpoints"], [])
        self.assertTrue(all(run["budget"] is None and run["stop_ordinal"] is None for run in template["runs"]))
        # Non-endpoint C3-V0 has two receipts with different exposure scopes.
        row = next(row for row in template["assessments"] if row["revision_id"] == "C3-V0")
        self.assertIsNone(row["receipt_id"])
        endpoint = next(row for row in template["assessments"] if row["revision_id"] == "C1-V2")
        self.assertEqual(endpoint["receipt_id"], "E-C1-V2")
        self.assert_code("output_already_exists", lambda: prepare_trace(self.study_path, path))
        automatic = analyze_trace(self.study_path)
        self.assertEqual(len(automatic["trajectories"]), 17)
        self.assertEqual(automatic["cohorts"]["status"], "not_requested")

    def test_single_run_has_trajectory_without_concentration_series(self):
        self.only_runs(["C4"])
        result = self.analyze()
        self.assertEqual(result["trajectories"][0]["transition_states"]["mechanism_switch"], 1)
        for point in result["cohorts"]["checkpoints"]:
            metrics = point["available"]["views"]["classified_all"]
            self.assertEqual(metrics["observed_support"], 1)
            self.assertEqual(metrics["sci"]["status"], "not_applicable")
            self.assertIsNone(metrics["sci"]["value"])
        self.assertTrue(all(change["joint"]["status"] == "insufficient_comparable_evidence"
                            for change in result["cohorts"]["changes"]["matched"]))

    def test_unresolved_assessment_is_not_a_switch_or_new_mechanism(self):
        self.assessment("C3-V1")["assignment_id"] = None
        result = self.analyze()
        run = next(run for run in result["trajectories"] if run["run_id"] == "C3")
        self.assertEqual(run["transition_states"], {"unresolved_assignment": 2})
        population = result["cohorts"]["checkpoints"][1]["matched"]
        self.assertEqual(population["observed"], 6)
        self.assertEqual(population["views"]["classified_all"]["population_size"], 5)
        self.assertEqual(population["unadmitted_reasons"], {"not_reviewed": 1})
        for change in result["cohorts"]["changes"]["matched"]:
            self.assertIn("mechanism_coverage_incomplete", change["joint"]["reasons"])
            self.assertEqual(change["views"]["classified_all"]["status"], "unavailable")

    def test_final_receipt_cannot_certify_earlier_identical_bytes(self):
        self.assessment("C1-V0")["receipt_id"] = "E-C1-V2"
        self.assert_code("selection_receipt_wrong_revision")

    def test_changed_or_unknown_test_scope_blocks_joint_but_keeps_mechanism_change(self):
        original = deepcopy(self.study)
        for key, value in (("environment", {"python": "3.12", "platform": "Other", "runner": "changed"}),
                           ("visibility", "feedback"), ("visibility", "unknown"), ("execution_basis", "external_report")):
            self.study = deepcopy(original)
            next(r for r in self.study["receipts"] if r["id"] == "E-C1-V1")[key] = value
            self.save_study()
            result = self.analyze()
            first = result["cohorts"]["changes"]["matched"][0]
            self.assertEqual(first["views"]["classified_all"]["status"], "available")
            self.assertEqual(first["views"]["classified_valid"]["status"], "unavailable")
            self.assertEqual(first["joint"]["status"], "insufficient_comparable_evidence")

    def test_changed_suite_stays_a_different_longitudinal_measure(self):
        suite = json.loads((self.root / "suite.json").read_bytes())
        suite["cases"][0]["input"]["edges"] = [[0, 0]]
        raw = encoded(suite)
        (self.root / "other-suite.json").write_bytes(raw)
        self.study["suites"].append({"id": "other", "path": "other-suite.json", "sha256": digest(raw), "oracle_id": suite["oracle_id"]})
        for receipt in self.study["receipts"]:
            if receipt["revision_id"].startswith("C") and receipt["revision_id"].endswith("V1"):
                receipt.update(suite_id="other", suite_sha256=digest(raw))
        self.save_study()
        result = self.analyze()
        self.assertTrue(all("test_scope_unknown_mixed_or_changed" in change["joint"]["reasons"]
                            for change in result["cohorts"]["changes"]["matched"]))

    def test_missing_and_partial_receipts_never_become_failed_or_passing_inferences(self):
        self.assessment("C1-V1")["receipt_id"] = None
        receipt = next(r for r in self.study["receipts"] if r["id"] == "E-C2-V1")
        receipt.update(status="partial", attempted=10, completed=1, passed=1)
        self.save_study()
        result = self.analyze()
        states = result["cohorts"]["checkpoints"][1]["matched"]["validity_states"]
        self.assertEqual(states, {"failed": 2, "not_assessed": 1, "passed_under_supplied_scope": 2, "undetermined": 1})
        change = result["cohorts"]["changes"]["matched"][0]
        self.assertIn("validity_incomplete", change["finite_pass_change"]["reasons"])
        self.assertIn("test_receipts_missing", change["joint"]["reasons"])

    def test_explicit_branch_path_excludes_sibling_and_merge_is_not_an_ordinary_switch(self):
        self.only_runs(["C1"])
        self.set_artifact("C1-V1", "settle_good")
        branch = {"id": "C1-branch", "run_id": "C1", "ordinal": 2, "artifact_id": "relax_good",
                  "parents": ["C1-V0"], "missing_parents": [], "kind": "edit", "feedback_ids": []}
        self.row("C1-V2").update(ordinal=3, kind="merge", parents=["C1-V1", "C1-branch"])
        self.study["revisions"].append(branch)
        self.design["assessments"].append({"revision_id": "C1-branch", "assignment_id": "M-relax_good", "receipt_id": None})
        self.trace_run("C1").update(stop_ordinal=3, budget={"max_revision_ordinal": 3, "max_test_case_attempts": 60})
        self.design["checkpoints"] = [0, 1, 2, 3]
        self.save_study()
        result = self.analyze()
        run = result["trajectories"][0]
        self.assertEqual(run["excluded_revision_ids"], ["C1-branch"])
        self.assertEqual(run["transition_states"], {"mechanism_switch": 1, "merge_parent_comparison": 1})
        self.assertEqual(result["cohorts"]["checkpoints"][2]["cells"][0]["state"], "branch_excluded")
        study, inspection = load_study(self.study_path)
        template = trace_document(study, inspection)
        self.assertIsNone(next(run for run in template["runs"] if run["run_id"] == "C1")["path"])
        self.trace_run("C1")["path"] = ["C1-V0", "C1-V1", "C1-branch", "C1-V2"]
        self.assert_code("trace_path_not_parent_linked")

    def test_missing_ordinal_is_not_renumbered_or_filled(self):
        self.only_runs(["C3"])
        self.row("C3-V1")["ordinal"] = 3
        self.row("C3-V2")["ordinal"] = 4
        self.trace_run("C3").update(stop_ordinal=4, budget={"max_revision_ordinal": 4, "max_test_case_attempts": 60})
        self.design["checkpoints"] = [0, 1, 3, 4]
        self.save_study()
        result = self.analyze()
        run = result["trajectories"][0]
        self.assertEqual(run["ordinal_gaps"], [{"after": 0, "before": 3}])
        self.assertEqual(run["path_transitions"][0]["state"], "ordinal_gap")
        self.assertEqual(result["cohorts"]["checkpoints"][1]["cells"][0]["state"], "missing_revision")
        self.assertEqual(result["cohorts"]["matched_run_ids"], [])
        self.assertEqual([row["ordinal"] for row in run["revisions"]], [0, 3, 4])

    def test_missing_parent_does_not_establish_a_mechanism_switch(self):
        self.only_runs(["C3"])
        self.row("C3-V1").update(parents=["lost-parent"], missing_parents=["lost-parent"], feedback_ids=[])
        self.save_study()
        result = self.analyze()
        first = result["trajectories"][0]["path_transitions"][0]
        self.assertEqual(first["state"], "missing_lineage")
        self.assertTrue(first["source_changed"])
        self.assertNotIn("mechanism_switch", result["trajectories"][0]["transition_states"])

    def test_equal_class_histograms_preserve_different_order_and_reappearance(self):
        self.only_runs(["C1"])
        self.set_artifact("C1-V1", "settle_good")
        self.save_study()
        first = self.analyze()["trajectories"][0]
        self.assertEqual(first["transition_states"], {"mechanism_switch": 2})
        self.assertTrue(first["mechanism_visitation"][-1]["observed_again_after_other_class"])
        self.set_artifact("C1-V1", "fifo_good")
        self.set_artifact("C1-V2", "settle_good")
        self.save_study()
        second = self.analyze()["trajectories"][0]
        self.assertEqual(Counter(row["class_id"] for row in first["mechanism_visitation"]),
                         Counter(row["class_id"] for row in second["mechanism_visitation"]))
        self.assertEqual(second["transition_states"], {"mechanism_switch": 1, "unchanged_source_and_mechanism": 1})
        self.assertFalse(second["mechanism_visitation"][-1]["observed_again_after_other_class"])

    def test_group_reappearance_is_observed_again_without_recovery_score(self):
        self.only_runs(["C1", "C2"])
        for run in ("C1", "C2"):
            self.set_artifact(run + "-V1", "settle_good")
        self.save_study()
        result = self.analyze()
        changes = result["cohorts"]["changes"]["matched"]
        self.assertEqual(changes[0]["observed_set_changes"]["classified_all"]["first_observed"], ["DIST-SETTLE"])
        self.assertEqual(changes[1]["observed_set_changes"]["classified_all"]["observed_again"], ["DIST-FIFO"])
        self.assertEqual(changes[1]["observed_set_changes"]["classified_all"]["first_observed"], [])
        self.assertEqual(result["external_recovery_rate"]["status"], "not_estimated")

    def test_unknown_stop_time_is_not_inferred_from_selected_endpoint(self):
        self.design = json.loads((self.root / "attrition.json").read_bytes())
        self.trace_run("A1")["stop_ordinal"] = None
        result = self.analyze()
        point = result["cohorts"]["checkpoints"][1]
        cell = next(row for row in point["cells"] if row["run_id"] == "A1")
        self.assertEqual(cell["state"], "stop_time_unknown")
        self.assertIn("A1", point["risk_set"]["reach_unknown"])
        self.assertNotIn("A1", point["risk_set"]["known_stopped_before"])

    def test_matched_budget_check_uses_the_actual_matched_runs(self):
        self.design = json.loads((self.root / "attrition.json").read_bytes())
        self.trace_run("A1")["budget"] = None
        result = self.analyze()
        self.assertIn("run_budget_unknown", result["cohorts"]["reasons"])
        self.assertEqual(result["cohorts"]["changes"]["matched"][0]["joint"]["status"], "available")
        self.assertEqual(result["cohorts"]["changes"]["available"][0]["joint"]["status"], "insufficient_comparable_evidence")

    def test_budget_unknown_mismatch_excess_and_protocol_preserve_inventory_only(self):
        original = deepcopy(self.design)
        mutations = [
            (lambda: self.trace_run("C1").update(budget=None), "run_budget_unknown"),
            (lambda: self.trace_run("C1")["budget"].update(max_test_case_attempts=61), "run_budget_mismatch"),
            (lambda: self.trace_run("C1")["budget"].update(max_test_case_attempts=59), "recorded_budget_exceeded"),
            (lambda: self.design.update(protocol_ref=None), "collection_protocol_unknown"),
            (lambda: self.design.update(checkpoints=[0, 1, 3]), "checkpoint_exceeds_revision_budget"),
        ]
        for mutation, reason in mutations:
            self.design = deepcopy(original)
            mutation()
            result = self.analyze()
            self.assertIn(reason, result["cohorts"]["reasons"])
            self.assertEqual(result["cohorts"]["changes"]["available"][0]["views"]["classified_all"]["status"], "unavailable")
            self.assertEqual(result["cohorts"]["checkpoints"][0]["available"]["observed"], 6)

    def test_multiple_configurations_cannot_enter_one_cohort(self):
        self.design["configuration_id"] = None
        result = self.analyze()
        self.assertEqual(result["cohorts"]["status"], "unavailable")
        self.assertEqual(result["cohorts"]["checkpoints"], [])
        self.design["configuration_id"] = "stable"
        self.assert_code("trace_run_configuration_mismatch")

    def test_reclassification_changes_evidence_without_new_generation_and_stale_labels_fail(self):
        original = next(row for row in self.study["assignments"] if row["artifact_id"] == "fifo_good")
        new = {**deepcopy(original), "id": "M-correction", "revision": 2, "status": "unresolved",
               "class_id": None, "reason": "review_disagreement", "evidence": []}
        self.study["assignments"].append(new)
        for selection in self.study["selection"]:
            if selection["assignment_id"] == original["id"]:
                selection["assignment_id"] = new["id"]
        self.save_study()
        self.assert_code("stale_assignment_selected")
        for row in self.design["assessments"]:
            if row["assignment_id"] == original["id"]:
                row["assignment_id"] = new["id"]
        result = self.analyze()
        self.assertEqual(sum(run["usage"]["generation_records"] for run in result["trajectories"]), 6)
        self.assertEqual(result["cohorts"]["checkpoints"][2]["available"]["views"]["classified_all"]["population_size"], 0)
        self.assertEqual(len(self.study["assignments"]), 7)

    def test_identical_source_with_incompatible_hard_labels_cannot_be_a_switch(self):
        original = deepcopy(next(row for row in self.study["artifacts"] if row["id"] == "fifo_good"))
        original["id"] = "same_bytes_other_label"
        self.study["artifacts"].append(original)
        assignment = deepcopy(next(row for row in self.study["assignments"] if row["artifact_id"] == "fifo_good"))
        assignment.update(id="M-same_bytes_other_label", artifact_id="same_bytes_other_label", class_id="DIST-SETTLE")
        self.study["assignments"].append(assignment)
        self.set_artifact("C1-V1", "same_bytes_other_label")
        self.save_study()
        self.assert_code("trace_conflicting_classes_for_same_source")

    def test_feedback_requires_correct_revision_ancestry_and_visibility(self):
        original = deepcopy(self.study)
        self.row("C1-V1")["feedback_ids"] = ["F-C2-V0"]
        self.save_study()
        self.assert_code("feedback_not_available_to_revision")
        self.study = original
        event = next(row for row in self.study["feedback"] if row["id"] == "F-C1-V0")
        event["receipt_id"] = "E-C1-V0"
        self.save_study()
        self.assert_code("feedback_exposes_withheld_or_unknown_receipt")

    def test_bindings_bounds_and_nonchronological_fields_are_checked(self):
        original = deepcopy(self.design)
        mutations = [
            (lambda d: d.update(study_sha256="0" * 64), "trace_study_binding_mismatch"),
            (lambda d: d.update(clock="recursive_training_generation"), "unsupported_trace_clock"),
            (lambda d: d.update(checkpoints=[0, 2, 1]), "trace_checkpoints_not_strictly_increasing"),
            (lambda d: d.update(checkpoints=[0, 0]), "trace_checkpoints_not_strictly_increasing"),
            (lambda d: d.update(checkpoints=[True]), "invalid_integer"),
            (lambda d: d.update(checkpoints=list(range(33))), "trace_checkpoint_limit"),
            (lambda d: d["runs"][0].update(stop_ordinal=1), "trace_stop_precedes_recorded_revision"),
            (lambda d: d["runs"][0].update(missing=True), "trace_run_declared_missing_but_present"),
            (lambda d: d["runs"][0].update(run_id="unknown_run"), "trace_run_not_recorded"),
            (lambda d: d["runs"][0].update(path=["C1-V1", "C1-V2"]), "trace_path_omits_known_ancestor"),
            (lambda d: d["runs"][0].update(path=["C1-V0"]), "trace_path_endpoint_mismatch"),
            (lambda d: d["assessments"].pop(), "trace_assessments_incomplete"),
            (lambda d: d["assessments"].append(deepcopy(d["assessments"][0])), "duplicate_trace_assessment"),
            (lambda d: d.update(runner="execute candidates"), "unexpected_or_missing_field"),
        ]
        for mutation, code in mutations:
            self.design = deepcopy(original)
            mutation(self.design)
            with self.subTest(code=code):
                self.assert_code(code)

    def test_unknown_path_keeps_all_source_records_without_selecting_a_branch(self):
        self.trace_run("C1")["path"] = None
        result = self.analyze()
        run = result["trajectories"][0]
        self.assertEqual(len(run["revisions"]), 3)
        self.assertEqual(run["path_transitions"], [])
        self.assertTrue(all(row["on_selected_path"] is None for row in run["revisions"]))
        self.assertNotIn("C1", result["cohorts"]["matched_run_ids"])
        for point in result["cohorts"]["checkpoints"]:
            self.assertEqual(next(cell for cell in point["cells"] if cell["run_id"] == "C1")["state"], "path_unknown")

    def test_all_missing_roster_is_an_explicit_empty_population(self):
        self.design["runs"] = [{"run_id": "not-captured", "missing": True, "path": None, "stop_ordinal": None,
                                "budget": {"max_revision_ordinal": 2, "max_test_case_attempts": 60}}]
        self.design["assessments"] = []
        result = self.analyze()
        for point in result["cohorts"]["checkpoints"]:
            view = point["available"]["views"]["classified_all"]
            self.assertEqual(view["observed_support"], 0)
            self.assertIsNone(view["sci"]["value"])
        self.assertTrue(all(c["views"]["classified_all"]["later_minus_earlier"] is None
                            for c in result["cohorts"]["changes"]["available"]))

    def test_cli_json_markdown_parity_and_bounded_error(self):
        self.design_path.write_bytes(encoded(self.design))
        args = ["trace", "--study", str(self.study_path), "--design", str(self.design_path)]
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(args), 0)
        result = json.loads(output.getvalue())
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(args + ["--format", "markdown"]), 0)
        self.assertEqual(output.getvalue(), trace_markdown(result))
        self.assertIn("SCI delta=1/6", output.getvalue())
        self.assertIn("finite passing rising; support falling; concentration rising", output.getvalue())
        self.assertIn("7/18", output.getvalue())
        self.design_path.write_text('{"schema_version":"one","schema_version":"two"}')
        output = io.StringIO()
        with redirect_stderr(output):
            self.assertEqual(main(args), 2)
        self.assertEqual(json.loads(output.getvalue())["code"], "duplicate_json_key")

    def test_passive_input_sensitive_text_symlinks_and_output_limits(self):
        sources = self.root / "canary"
        sources.mkdir()
        marker = self.root / "must-not-exist"
        source = f"open({str(marker)!r}, 'w').write('PRIVATE_CODE_TEXT')\n" + FIFO
        (sources / "program.py").write_text(source)
        destination = self.root / "prepared"
        prepare_sources(sources, destination, pack_id="unit-graph-distances")
        passive = analyze_trace(destination / "study.json")
        self.assertFalse(marker.exists())
        self.assertNotIn("PRIVATE_CODE_TEXT", json.dumps(passive))
        config = next(row for row in self.study["configurations"] if row["id"] == "concentration")
        config.update(model="PRIVATE_MODEL", prompt="PRIVATE_PROMPT", settings={"secret": "PRIVATE_SETTINGS"})
        self.design["protocol_ref"] = "PRIVATE_PROTOCOL"
        self.save_study()
        result = self.analyze()
        text = json.dumps(result) + trace_markdown(result)
        for secret in ("PRIVATE_MODEL", "PRIVATE_PROMPT", "PRIVATE_SETTINGS", "PRIVATE_PROTOCOL"):
            self.assertNotIn(secret, text)
        with patch("structdet_code.trace.MAX_RESULT", 10):
            self.assert_code("trace_result_size_limit")
        self.design_path.unlink()
        self.design_path.symlink_to(self.study_path)
        self.assert_code("payload_unavailable_or_unsafe", lambda: analyze_trace(self.study_path, self.design_path))

    def test_sorting_uses_the_same_trace_path_with_known_source_only_changes(self):
        result = analyze_trace(ROOT / "examples/minimal/study.json")
        first = result["trajectories"][0]
        self.assertEqual(result["task"]["pack_id"], "sorting-bounded")
        self.assertEqual(first["transition_states"], {"source_change_same_mechanism": 1, "unchanged_source_and_mechanism": 1})
        self.assertEqual(first["revisions"][0]["validity"], "failed")
        self.assertEqual(first["revisions"][1]["validity"], "passed_under_supplied_scope")
        self.assertEqual(first["usage"]["generation_records"], 1)

    def test_json_record_order_does_not_rewrite_revision_time(self):
        expected = self.analyze()
        self.design["runs"].reverse()
        self.design["assessments"].reverse()
        self.study["revisions"].reverse()
        self.study["receipts"].reverse()
        self.study["runs"].reverse()
        self.save_study()
        result = self.analyze()
        self.assertEqual(result["trajectories"], expected["trajectories"])
        self.assertEqual(result["cohorts"], expected["cohorts"])
