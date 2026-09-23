import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from structdet_code.errors import StudyError
from structdet_code.reporting import markdown
from structdet_code.rules import INSERTION
from structdet_code.study import inspect_study
from structdet_code.workflow import apply_review, prepare_review, prepare_sources

ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sources = self.root / "input"
        self.sources.mkdir()
        (self.sources / "a.py").write_text(INSERTION)
        (self.sources / "b.py").write_text(INSERTION.replace("list(values)", "values[:]"))
        self.output = self.root / "prepared"

    def prepare(self):
        return prepare_sources(self.sources, self.output, "owned-case", "fixture")

    def assertCode(self, code, call, *args, **kwargs):
        with self.assertRaises(StudyError) as raised:
            call(*args, **kwargs)
        self.assertEqual(raised.exception.code, code)

    def reviewed(self, decision="accepted", basis="human_review", class_id="SORT-INS", reason=None):
        document = json.loads((self.output / "review.json").read_text())
        entry = document["entries"][1]
        entry.update(decision=decision, basis=basis, class_id=class_id, reason=reason,
                     reviewer_ref="fixture-supplied-reviewer", evidence=[{
                         "start_line": 1, "end_line": 10, "note": "Ordered prefix extended by shifting predecessors."}])
        path = self.output / "decisions.json"
        path.write_text(json.dumps(document))
        return document, path

    def test_prepare_has_coverage_no_tests_unknown_origins_and_no_invented_generations(self):
        original = {p.name: p.read_bytes() for p in self.sources.iterdir()}
        outcome = self.prepare()
        self.assertEqual(outcome["source_count"], 2)
        self.assertEqual(outcome["classification_coverage"]["admitted"], 1)
        study = json.loads((self.output / "study.json").read_text())
        result = inspect_study(self.output / "study.json")
        self.assertEqual(result["ledger"]["generation_records"], 0)
        self.assertEqual(result["ledger"]["standalone_snapshot_records"], 2)
        self.assertEqual(result["ledger"]["validity_states"], {"not_assessed": 2})
        self.assertEqual(result["views"]["classified_valid"]["sci"]["status"], "undefined")
        self.assertEqual(study["suites"], [])
        self.assertEqual(study["receipts"], [])
        self.assertIsNone(study["configurations"][0]["model"])
        self.assertTrue(all(r["root_group_id"] is None for r in study["runs"]))
        self.assertEqual(original, {p.name: p.read_bytes() for p in self.sources.iterdir()})
        self.assertIn("Admitted coverage: 1/2", markdown(result))

    def test_default_descriptive_role_never_claims_fixture_execution(self):
        prepare_sources(self.sources, self.output)
        result = inspect_study(self.output / "study.json")
        self.assertEqual(result["data_role"], "descriptive")
        self.assertFalse(result["substantive_validation_performed"])
        self.assertFalse(result["candidate_execution_performed"])

    def test_new_schema_does_not_reinterpret_legacy_records(self):
        self.prepare()
        path = self.output / "study.json"
        study = json.loads(path.read_text())
        self.assertEqual(study["schema_version"], "structdet-code.study/0.2")
        study["schema_version"] = "structdet-code.study/0.1"
        path.write_text(json.dumps(study))
        self.assertCode("static_policy_requires_schema_0_2", inspect_study, path)
        study["evidence_policy"] = "fixture_only"
        for item in study["assignments"]:
            item["basis"] = "fixture"
        path.write_text(json.dumps(study))
        self.assertCode("snapshot_requires_schema_0_2", inspect_study, path)

    def test_malformed_schema_values_are_bounded_input_errors(self):
        self.prepare()
        path = self.output / "study.json"
        original = json.loads(path.read_text())
        for value in ([], {}, None, True, 2):
            changed = copy.deepcopy(original)
            changed["schema_version"] = value
            path.write_text(json.dumps(changed))
            self.assertCode("unsupported_schema", inspect_study, path)

    def test_review_duplicates_hooks_and_missing_decisions_are_rejected(self):
        self.prepare()
        original, path = self.reviewed()
        mutations = [({**original, "command": "run something"}, "unexpected_or_missing_field"),
                     ({**original, "entries": original["entries"] + [original["entries"][1]]}, "unknown_or_duplicate_review_artifact")]
        undecided = copy.deepcopy(original)
        undecided["entries"][1]["decision"] = None
        mutations.append((undecided, "review_decision_missing"))
        invalid_basis = copy.deepcopy(original)
        invalid_basis["entries"][1]["basis"] = ["human_review"]
        mutations.append((invalid_basis, "invalid_review_basis"))
        for value, code in mutations:
            path.write_text(json.dumps(value))
            self.assertCode(code, apply_review, self.output / "study.json", path, self.output / "bad.json")

    def test_correction_review_keeps_sources_and_population_but_invalidates_label(self):
        self.prepare()
        _, path = self.reviewed()
        first = self.output / "reviewed.json"
        apply_review(self.output / "study.json", path, first)
        template = self.output / "correction.json"
        prepare_review(first, template)
        document = json.loads(template.read_text())
        document["entries"][1].update(decision="unresolved", basis="human_review", reason="review_disagreement",
                                      reviewer_ref="fixture-reviewer", note="Earlier assignment withdrawn.")
        template.write_text(json.dumps(document))
        corrected = self.output / "corrected.json"
        apply_review(first, template, corrected)
        current = inspect_study(corrected)
        self.assertEqual(current["ledger"]["selected_observations"], 2)
        self.assertEqual(current["views"]["classified_all"]["population_size"], 1)
        self.assertEqual(len(json.loads(corrected.read_text())["assignments"]), 4)

    def test_identical_bytes_at_two_collection_slots_are_not_deduplicated(self):
        (self.sources / "b.py").write_text(INSERTION)
        self.prepare()
        result = inspect_study(self.output / "study.json")
        self.assertEqual(result["views"]["classified_all"]["population_size"], 2)
        self.assertEqual(result["ledger"]["unique_source_bytes"], 1)

    def test_blank_template_and_noop_review_cannot_manufacture_evidence(self):
        self.prepare()
        study = self.output / "study.json"
        path = self.output / "fresh-review.json"
        prepare_review(study, path)
        self.assertEqual(json.loads(path.read_text()), json.loads((self.output / "review.json").read_text()))
        self.assertCode("no_review_decisions", apply_review, study, path, self.output / "new.json")
        self.assertFalse((self.output / "new.json").exists())

    def test_review_appends_and_preserves_old_assignments_and_inputs(self):
        self.prepare()
        study_path = self.output / "study.json"
        original = study_path.read_bytes()
        _, decisions = self.reviewed()
        outcome = apply_review(study_path, decisions, self.output / "reviewed.json")
        self.assertEqual(outcome["assignments_appended"], 1)
        self.assertEqual(study_path.read_bytes(), original)
        updated = json.loads((self.output / "reviewed.json").read_text())
        self.assertEqual(updated["assignments"][:2], json.loads(original)["assignments"])
        self.assertEqual(updated["assignments"][-1]["revision"], 2)
        result = inspect_study(self.output / "reviewed.json")
        self.assertEqual(result["ledger"]["admitted_bases"], {"human_review": 1, "static_rule": 1})
        self.assertFalse(result["substantive_validation_performed"])

    def test_model_proposals_and_conflicted_reviews_stay_out_of_counts(self):
        for decision, basis, label, reason in (("proposed", "model_assisted", "SORT-INS", "not_reviewed"),
                                                ("conflicted", "human_review", None, "review_disagreement")):
            with self.subTest(decision=decision):
                if not self.output.exists():
                    self.prepare()
                _, decisions = self.reviewed(decision, basis, label, reason)
                target = self.output / f"{decision}.json"
                apply_review(self.output / "study.json", decisions, target)
                self.assertEqual(inspect_study(target)["views"]["classified_all"]["population_size"], 1)

    def test_model_cannot_be_promoted_and_anchors_must_be_real(self):
        self.prepare()
        document, decisions = self.reviewed(basis="model_assisted")
        self.assertCode("assignment_basis_not_admissible", apply_review,
                        self.output / "study.json", decisions, self.output / "bad.json")
        document["entries"][1]["basis"] = "human_review"
        document["entries"][1]["evidence"][0]["end_line"] = 999
        decisions.write_text(json.dumps(document))
        self.assertCode("source_anchor_out_of_range", apply_review,
                        self.output / "study.json", decisions, self.output / "bad.json")

    def test_source_task_study_and_previous_assignment_are_bound(self):
        self.prepare()
        original, path = self.reviewed()
        changes = [("study_sha256", "0" * 64, "stale_review_study"),
                   ("pack_sha256", "0" * 64, "review_frame_mismatch")]
        for field, value, code in changes:
            changed = copy.deepcopy(original)
            changed[field] = value
            path.write_text(json.dumps(changed))
            self.assertCode(code, apply_review, self.output / "study.json", path, self.output / "bad.json")
        for field in ("source_sha256", "current_assignment_id", "suggested_class_id"):
            changed = copy.deepcopy(original)
            changed["entries"][1][field] = "different"
            path.write_text(json.dumps(changed))
            self.assertCode("stale_review_binding", apply_review,
                            self.output / "study.json", path, self.output / "bad.json")
        path.write_text(json.dumps(original))
        (self.output / "sources/b.py").write_text(INSERTION)
        self.assertCode("source_digest_mismatch", apply_review,
                        self.output / "study.json", path, self.output / "bad.json")

    def test_static_rule_claims_are_recomputed_not_trusted(self):
        self.prepare()
        source = self.output / "study.json"
        original = json.loads(source.read_text())
        for key, value in (("rule_id", "imaginary/1"), ("class_id", "SORT-MERGE"),
                           ("evidence", [{"start_line": 1, "end_line": 1, "note": "fabricated"}])):
            changed = copy.deepcopy(original)
            changed["assignments"][0][key] = value
            source.write_text(json.dumps(changed))
            self.assertCode("static_rule_claim_mismatch", inspect_study, source)
        changed = copy.deepcopy(original)
        changed["assignments"][1].update(status="accepted", class_id="SORT-INS", reason=None,
            rule_id="sort-ins-shift-copy/1", evidence=original["assignments"][0]["evidence"])
        source.write_text(json.dumps(changed))
        self.assertCode("static_rule_claim_mismatch", inspect_study, source)

    def test_human_rule_disagreement_requires_an_explicit_conflict(self):
        self.prepare()
        document = json.loads((self.output / "review.json").read_text())
        document["entries"][0].update(decision="accepted", basis="human_review", class_id="SORT-MERGE",
            reviewer_ref="fixture-reviewer", evidence=[{"start_line": 1, "end_line": 10, "note": "Supplied disagreement."}])
        decisions = self.output / "decision.json"
        decisions.write_text(json.dumps(document))
        self.assertCode("review_conflicts_with_static_rule", apply_review,
                        self.output / "study.json", decisions, self.output / "bad.json")
        document["entries"][0].update(decision="conflicted", class_id=None, reason="review_disagreement")
        decisions.write_text(json.dumps(document))
        apply_review(self.output / "study.json", decisions, self.output / "conflicted.json")
        self.assertEqual(inspect_study(self.output / "conflicted.json")["views"]["classified_all"]["population_size"], 0)

    def test_outputs_do_not_overwrite_sources_existing_directories_or_symlinks(self):
        self.assertCode("output_already_exists", prepare_sources, self.sources, self.sources)
        self.prepare()
        self.assertCode("output_already_exists", self.prepare)
        study = self.output / "study.json"
        self.assertCode("output_already_exists", prepare_review, study, study)
        alias = self.root / "alias.json"
        alias.symlink_to(study)
        self.assertCode("output_already_exists", prepare_review, study, alias)
        _, review = self.reviewed()
        self.assertCode("review_output_must_share_study_directory", apply_review, study, review, self.root / "elsewhere.json")

    def test_unsafe_and_symlinked_source_paths_are_rejected(self):
        for name in ("../escape.py", "/absolute.py", "input\\a.py"):
            self.assertCode("unsafe_path", prepare_sources, self.sources, self.output, include=[name])
        link = self.sources / "linked.py"
        link.symlink_to(self.sources / "a.py")
        self.assertCode("payload_unavailable_or_unsafe", prepare_sources, self.sources, self.output)
        self.assertFalse(self.output.exists())

    def test_empty_nested_explicit_and_cumulative_limit_behavior(self):
        empty = self.root / "empty"
        empty.mkdir()
        self.assertCode("source_collection_size", prepare_sources, empty, self.output)
        nested = self.sources / "nested"
        nested.mkdir()
        (nested / "c.py").write_text(INSERTION)
        with patch("structdet_code.workflow.MAX_TOTAL", len(INSERTION) * 2):
            self.assertCode("total_input_size_limit", prepare_sources, self.sources, self.output)
        prepare_sources(self.sources, self.output, include=["nested/c.py"])
        self.assertTrue((self.output / "sources/nested/c.py").is_file())

    def test_source_count_and_default_directory_scan_are_bounded(self):
        for index in range(127):
            (self.sources / f"extra-{index}.py").write_text(INSERTION)
        self.assertCode("source_collection_size", self.prepare)
        large = self.root / "many-entries"
        large.mkdir()
        for index in range(4097):
            (large / str(index)).touch()
        self.assertCode("directory_entry_limit", prepare_sources, large, self.output)

    def test_shipped_static_example_remains_reproducible(self):
        result = inspect_study(ROOT / "examples/static/study.json")
        self.assertEqual(result["ledger"]["classification_coverage"]["admitted"], 6)
        self.assertEqual(result["views"]["classified_all"]["class_counts"],
                         {"SORT-INS": 4, "SORT-MERGE": 1, "SORT-SEL": 1})
        self.assertEqual(result["views"]["classified_all"]["sci"]["numerator"], 1)
        self.assertEqual(result["views"]["classified_all"]["sci"]["denominator"], 2)
        self.assertEqual(result["ledger"]["validity_states"], {"not_assessed": 7})

    def test_prepare_is_passive_even_for_top_level_payloads(self):
        marker = self.root / "never-created"
        (self.sources / "b.py").write_text(f"open({str(marker)!r}, 'w').write('bad')\n" + INSERTION)
        self.prepare()
        self.assertFalse(marker.exists())
        self.assertEqual(inspect_study(self.output / "study.json")["ledger"]["classification_coverage"]["admitted"], 1)

    def test_all_cli_paths_and_bounded_errors(self):
        def run(*args):
            return subprocess.run([sys.executable, "-m", "structdet_code", *map(str, args)],
                                  cwd=ROOT, capture_output=True, text=True, timeout=15)
        prepared = run("prepare", "--sources", self.sources, "--output", self.output, "--data-role", "fixture")
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        study = self.output / "study.json"
        for command in ("validate", "inspect"):
            self.assertEqual(run(command, "--study", study).returncode, 0)
        rendered = run("inspect", "--study", study, "--format", "markdown")
        self.assertIn("Admitted coverage: 1/2", rendered.stdout)
        self.assertEqual(run("review-template", "--study", study, "--output", self.output / "template.json").returncode, 0)
        _, review = self.reviewed()
        applied = run("apply-review", "--study", study, "--review", review, "--output", self.output / "new.json")
        self.assertEqual(applied.returncode, 0, applied.stderr)
        repeated = run("prepare", "--sources", self.sources, "--output", self.output)
        self.assertEqual(repeated.returncode, 2)
        self.assertEqual(json.loads(repeated.stderr)["code"], "output_already_exists")
        self.assertNotIn("Traceback", repeated.stderr)
