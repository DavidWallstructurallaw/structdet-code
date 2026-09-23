from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from structdet_code.__main__ import main
from structdet_code.comparison import compare_studies, comparison_markdown, prepare_comparison
from structdet_code.errors import StudyError
from structdet_code.io import digest
from structdet_code.workflow import encoded

ROOT = Path(__file__).resolve().parents[1]


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "graph"
        shutil.copytree(ROOT / "examples/graph", self.root)
        self.left = self.root / "left/study.json"
        self.right = self.root / "right/study.json"
        self.design_path = self.root / "comparison.json"
        self.design = json.loads(self.design_path.read_bytes())

    def compare(self):
        self.design_path.write_bytes(encoded(self.design))
        return compare_studies(self.left, self.right, self.design_path)

    def save_study(self, side, study):
        path = self.root / side / "study.json"
        raw = encoded(study)
        path.write_bytes(raw)
        self.design[side]["study_sha256"] = digest(raw)

    def study(self, side):
        return json.loads((self.root / side / "study.json").read_bytes())

    def test_exact_prefix_oracle_retains_missing_failed_and_excluded_later_slots(self):
        result = self.compare()
        self.assertEqual(result["status"], "compatible_descriptive")
        left, right = result["left"], result["right"]
        self.assertEqual(left["prefix_population"]["views"]["classified_all"]["class_counts"],
                         {"DIST-FIFO": 2, "DIST-RELAX": 1, "DIST-SETTLE": 1})
        self.assertEqual(right["missing_positions"], [3])
        self.assertEqual(right["excluded_later_selected"], [{"position": 5, "revision_id": "V004"}])
        self.assertEqual([row["position"] for row in right["prefix_observations"]], [1, 2, 4])
        self.assertEqual(right["configuration_inventory"]["observed"], 4)
        population = right["prefix_population"]
        self.assertEqual(population["views"]["classified_all"]["class_counts"], {"DIST-FIFO": 3})
        self.assertEqual(population["views"]["classified_valid"]["class_counts"], {"DIST-FIFO": 2})
        self.assertEqual(population["validity_states"], {"failed": 1, "passed_under_supplied_scope": 2})
        self.assertEqual(population["observed_pass_fraction"]["value"], 2 / 3)
        self.assertEqual(population["observed_pass_coverage_requested"]["value"], 1 / 2)
        self.assertEqual(population["classification_coverage_requested"]["value"], 3 / 4)
        for view in ("classified_all", "classified_valid"):
            delta = result["contrasts"][view]["right_minus_left"]
            self.assertEqual(delta["observed_support"], -2)
            self.assertEqual(delta["sci"], {"numerator": 5, "denominator": 8, "value": 0.625})
            self.assertEqual(delta["gini_simpson"]["numerator"], -5)
        self.assertEqual(len(result["shared_prefix_source_sha256"]), 1)
        self.assertEqual(population["declared_root_groups"], {"G-project-fixtures": 3})
        self.assertFalse(result["candidate_execution_performed"])
        self.assertFalse(result["causal_effect_estimated"])

    def test_template_and_no_design_leave_unknowns_without_inferred_order(self):
        output = self.root / "blank.json"
        prepare_comparison(self.left, self.right, output)
        template = json.loads(output.read_bytes())
        for side in ("left", "right"):
            self.assertIsNone(template[side]["planned_positions"])
            self.assertIsNone(template[side]["budget_per_slot"])
            self.assertTrue(all(slot["position"] is None for slot in template[side]["slots"]))
        self.assertIsNone(template["protocol_ref"])
        self.assertIsNone(template["varied_field"])
        result = compare_studies(self.left, self.right)
        self.assertEqual(result["status"], "descriptive_only")
        self.assertIsNone(result["left"]["prefix_population"])
        self.assertEqual(result["left"]["configuration_inventory"]["observed"], 4)
        self.assertIsNone(result["contrasts"]["classified_all"]["right_minus_left"])
        with self.assertRaisesRegex(StudyError, "output_already_exists"):
            prepare_comparison(self.left, self.right, output)

    def test_missing_accounting_and_unmapped_selected_never_trigger_backfill(self):
        original = deepcopy(self.design)
        modifications = [
            (lambda d: d["right"]["slots"].pop(2), "right:prefix_positions_unaccounted"),
            (lambda d: d["right"]["slots"].pop(4), "right:selected_revisions_unmapped"),
            (lambda d: d["right"]["slots"][0].update(position=None), "right:slot_positions_unknown"),
            (lambda d: d.update(prefix_size=5), "left:prefix_exceeds_planned_positions"),
        ]
        for change, reason in modifications:
            self.design = deepcopy(original)
            change(self.design)
            result = self.compare()
            self.assertIn(reason, result["compatibility_reasons"])
            self.assertEqual(result["contrasts"]["classified_all"]["status"], "unavailable")

    def test_slot_identity_bounds_and_foreign_revisions_are_rejected(self):
        original = deepcopy(self.design)
        modifications = [
            (lambda d: d["right"]["slots"][1].update(position=1), "duplicate_comparison_position"),
            (lambda d: d["right"]["slots"][1].update(revision_id="V001"), "duplicate_comparison_revision"),
            (lambda d: d["right"]["slots"][1].update(revision_id="missing"), "comparison_revision_not_selected_in_configuration"),
            (lambda d: d["right"]["slots"][1].update(position=6), "slot_outside_planned_positions"),
            (lambda d: d["right"]["slots"][1].update(position=True), "invalid_integer"),
            (lambda d: d.update(prefix_size=129), "invalid_integer"),
            (lambda d: d["right"].update(slots=[{"position": None, "revision_id": None}] * 257), "comparison_slot_limit"),
        ]
        for change, code in modifications:
            self.design = deepcopy(original)
            change(self.design)
            with self.subTest(code=code), self.assertRaisesRegex(StudyError, code):
                self.compare()

    def test_changed_study_or_pack_binding_cannot_reuse_design(self):
        self.left.write_bytes(self.left.read_bytes() + b"\n")
        with self.assertRaisesRegex(StudyError, "comparison_study_binding_mismatch"):
            self.compare()
        study = self.study("left")
        study["task"]["pack_sha256"] = "0" * 64
        self.save_study("left", study)
        with self.assertRaisesRegex(StudyError, "unsupported_or_changed_task_frame"):
            self.compare()

    def test_unknown_or_different_budget_and_protocol_block_deltas(self):
        original = deepcopy(self.design)
        modifications = [
            (lambda d: d["right"].update(budget_per_slot=None), "right:budget_unknown"),
            (lambda d: d["right"]["budget_per_slot"].update(limit=2), "budget_mismatch"),
            (lambda d: d["right"]["budget_per_slot"].update(unit="model_calls"), "budget_mismatch"),
            (lambda d: d.update(protocol_ref=None), "collection_protocol_unknown"),
            (lambda d: d.update(varied_field=None), "varied_field_unknown"),
        ]
        for change, reason in modifications:
            self.design = deepcopy(original)
            change(self.design)
            result = self.compare()
            self.assertIn(reason, result["compatibility_reasons"])
            self.assertEqual(result["contrasts"]["classified_all"]["status"], "unavailable")

    def test_condition_controls_require_known_values_and_one_changed_field(self):
        original = self.study("right")
        changes = [("prompt", "different", "control_mismatch:prompt"),
                   ("settings", {"fixture_only": False}, "control_mismatch:settings"),
                   ("selection_rule", "different", "control_mismatch:selection_rule"),
                   ("model", "fixture-condition-left", "varied_field_unchanged"),
                   ("model", None, "right:model_unknown")]
        for field, value, reason in changes:
            study = deepcopy(original)
            study["configurations"][0][field] = value
            self.save_study("right", study)
            result = self.compare()
            self.assertIn(reason, result["compatibility_reasons"])
        left = self.study("left")
        left["configurations"][0]["settings"] = None
        right = deepcopy(original)
        right["configurations"][0]["settings"] = None
        self.save_study("left", left)
        self.save_study("right", right)
        result = self.compare()
        self.assertIn("left:settings_unknown", result["compatibility_reasons"])
        self.assertIn("right:settings_unknown", result["compatibility_reasons"])

    def test_task_and_material_mismatch_are_separate_inventories(self):
        result = compare_studies(ROOT / "examples/static/study.json", self.right)
        self.assertIn("task_mismatch", result["compatibility_reasons"])
        self.assertEqual(result["contrasts"]["classified_all"]["status"], "unavailable")
        right = self.study("right")
        right["data_role"] = "descriptive"
        for receipt in right["receipts"]:
            receipt["execution_basis"] = "external_report"
        self.save_study("right", right)
        self.assertIn("data_role_mismatch", self.compare()["compatibility_reasons"])

    def test_same_comparison_workflow_supports_sorting_populations(self):
        for side in ("left", "right"):
            folder = self.root / ("sorting-" + side)
            shutil.copytree(ROOT / "examples/static", folder)
            path = folder / "study.json"
            study = json.loads(path.read_bytes())
            study["configurations"][0].update(model="fixture-" + side, prompt="common", settings={})
            path.write_bytes(encoded(study))
        self.left = self.root / "sorting-left/study.json"
        self.right = self.root / "sorting-right/study.json"
        template_path = self.root / "sorting-comparison.json"
        prepare_comparison(self.left, self.right, template_path)
        self.design = json.loads(template_path.read_bytes())
        self.design.update(varied_field="model", protocol_ref="Stipulated fixture protocol", prefix_size=7)
        for side in ("left", "right"):
            self.design[side].update(planned_positions=7, budget_per_slot={"unit": "attempts", "limit": 1})
            for index, slot in enumerate(self.design[side]["slots"], 1):
                slot["position"] = index
        result = self.compare()
        self.assertEqual(result["status"], "compatible_descriptive")
        contrast = result["contrasts"]["classified_all"]
        self.assertEqual((contrast["left_population"], contrast["right_population"]), (6, 6))
        self.assertEqual(contrast["right_minus_left"]["sci"]["numerator"], 0)
        self.assertEqual(result["contrasts"]["classified_valid"]["status"], "unavailable")

    def test_configuration_filter_requires_matching_selected_revisions(self):
        study = self.study("right")
        extra = {**study["configurations"][0], "id": "C-extra"}
        study["configurations"].append(extra)
        study["runs"][3]["configuration_id"] = "C-extra"
        self.save_study("right", study)
        with self.assertRaisesRegex(StudyError, "comparison_revision_not_selected_in_configuration"):
            self.compare()
        self.design["right"]["slots"].pop()
        result = self.compare()
        self.assertEqual(result["status"], "compatible_descriptive")
        self.assertEqual(result["right"]["study_selected_count"], 4)
        self.assertEqual(result["right"]["configuration_inventory"]["observed"], 3)

    def test_missing_receipt_blocks_valid_comparison_only(self):
        study = self.study("right")
        study["selection"][0]["receipt_id"] = None
        self.save_study("right", study)
        result = self.compare()
        self.assertEqual(result["contrasts"]["classified_all"]["status"], "available")
        self.assertIn("observed_test_receipts_missing", result["contrasts"]["classified_valid"]["reasons"])
        self.assertEqual(result["right"]["observed_without_receipt"], 1)

    def test_changed_suite_or_environment_blocks_valid_comparison_only(self):
        original = self.study("right")
        for mutation in ("environment", "basis", "suite"):
            study = deepcopy(original)
            if mutation == "suite":
                path = self.root / "right/suite.json"
                suite = json.loads(path.read_bytes())
                suite["cases"][0]["input"]["edges"] = [[0, 0]]
                raw = encoded(suite)
                path.write_bytes(raw)
                study["suites"][0]["sha256"] = digest(raw)
                for receipt in study["receipts"]:
                    receipt["suite_sha256"] = digest(raw)
            elif mutation == "basis":
                for receipt in study["receipts"]:
                    receipt["execution_basis"] = "external_report"
            else:
                study["receipts"][0]["environment"]["runner"] = "different-runner"
            self.save_study("right", study)
            result = self.compare()
            self.assertEqual(result["contrasts"]["classified_all"]["status"], "available")
            self.assertIn("test_scope_unknown_mixed_or_changed", result["contrasts"]["classified_valid"]["reasons"])

    def test_partial_and_timeout_results_stay_undetermined(self):
        study = self.study("right")
        study["receipts"][0].update(status="partial", attempted=10, completed=3, passed=3)
        study["receipts"][2].update(status="timeout", attempted=10, completed=0, passed=0)
        self.save_study("right", study)
        result = self.compare()
        self.assertEqual(result["right"]["prefix_population"]["validity_states"], {"failed": 1, "undetermined": 2})
        self.assertIn("empty_classified_population", result["contrasts"]["classified_valid"]["reasons"])
        self.assertEqual(result["contrasts"]["classified_all"]["status"], "available")

    def test_unresolved_and_proposed_labels_reduce_coverage_without_becoming_classes(self):
        study = self.study("right")
        study["assignments"][0].update(status="unresolved", class_id=None, reason="hybrid", evidence=[], rule_id=None)
        study["assignments"][1].update(status="proposed", basis="model_assisted", reason="not_reviewed", rule_id=None)
        self.save_study("right", study)
        result = self.compare()
        population = result["right"]["prefix_population"]
        self.assertEqual(population["views"]["classified_all"]["class_counts"], {"DIST-FIFO": 1})
        self.assertEqual(population["classification_coverage_observed"]["value"], 1 / 3)
        self.assertEqual(population["classification_coverage_requested"]["value"], 1 / 4)
        self.assertEqual(population["unadmitted_reasons"], {"hybrid": 1, "not_reviewed": 1})

    def test_empty_observed_prefix_is_explicit_and_deltas_are_unavailable(self):
        self.design["right"].update(planned_positions=8)
        self.design["right"]["slots"] = ([{"position": p, "revision_id": None} for p in range(1, 5)]
            + [{"position": p + 4, "revision_id": f"V{p:03}"} for p in range(1, 5)])
        result = self.compare()
        population = result["right"]["prefix_population"]
        self.assertEqual(population["observed"], 0)
        self.assertEqual(population["views"]["classified_all"]["observed_support"], 0)
        self.assertIsNone(population["views"]["classified_all"]["sci"]["value"])
        self.assertIn("empty_classified_population", result["contrasts"]["classified_all"]["reasons"])
        self.assertEqual(result["right"]["missing_positions"], [1, 2, 3, 4])

    def test_order_of_json_rows_does_not_replace_explicit_collection_positions(self):
        expected = self.compare()
        self.design["right"]["slots"].reverse()
        self.design["left"]["slots"].reverse()
        actual = self.compare()
        self.assertEqual(actual["contrasts"], expected["contrasts"])
        self.assertEqual(actual["right"]["prefix_observations"], expected["right"]["prefix_observations"])

    def test_reports_keep_sensitive_condition_strings_out_and_render_exact_operands(self):
        for side in ("left", "right"):
            study = self.study(side)
            study["configurations"][0]["prompt"] = "PRIVATE_PROMPT_9372"
            study["configurations"][0]["settings"] = {"private": "PRIVATE_SETTING_9372"}
            self.save_study(side, study)
        self.design["protocol_ref"] = "PRIVATE_PROTOCOL_9372"
        result = self.compare()
        rendered = comparison_markdown(result)
        for secret in ("PRIVATE_PROMPT_9372", "PRIVATE_SETTING_9372", "PRIVATE_PROTOCOL_9372"):
            self.assertNotIn(secret, json.dumps(result) + rendered)
        self.assertIn("SCI delta=5/8", rendered)
        self.assertIn("Gini-Simpson delta=-5/8", rendered)
        self.assertIn("left n=4, right n=3", rendered)
        self.assertIn("left n=4, right n=2", rendered)
        self.assertIn("3 / 4 | 3 | 1 | 3 | 2", rendered)

    def test_cli_json_markdown_invalid_design_and_unsafe_paths(self):
        args = ["compare", "--left", str(self.left), "--right", str(self.right), "--design", str(self.design_path)]
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(args), 0)
        result = json.loads(output.getvalue())
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(args + ["--format", "markdown"]), 0)
        self.assertEqual(output.getvalue(), comparison_markdown(result))
        self.design_path.write_text('{"schema_version":"one","schema_version":"two"}')
        output = io.StringIO()
        with redirect_stderr(output):
            self.assertEqual(main(args), 2)
        self.assertEqual(json.loads(output.getvalue())["code"], "duplicate_json_key")
        self.design_path.unlink()
        self.design_path.symlink_to(self.left)
        with self.assertRaisesRegex(StudyError, "payload_unavailable_or_unsafe"):
            compare_studies(self.left, self.right, self.design_path)

    def test_design_unknown_fields_do_not_enable_executable_extensions(self):
        marker = self.root / "must-not-exist"
        self.design["runner"] = f"open({str(marker)!r}, 'w').write('wrong')"
        with self.assertRaisesRegex(StudyError, "unexpected_or_missing_field"):
            self.compare()
        self.assertFalse(marker.exists())
