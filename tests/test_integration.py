import json
from pathlib import Path
import tempfile
import unittest

from structdet_code.comparison import compare_studies, prepare_comparison
from structdet_code.errors import StudyError
from structdet_code.evidence import prepare_evidence
from structdet_code.replay import create_snapshot, replay_snapshot
from structdet_code.study import inspect_study, load_study
from structdet_code.trace import analyze_trace, prepare_trace
from structdet_code.workflow import apply_review, encoded, prepare_sources
from tools.run_demonstrations import run_demonstrations

ROOT = Path(__file__).resolve().parents[1]


class IntegrationTests(unittest.TestCase):
    def test_six_demonstrations_and_all_exact_replays(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "demos"
            summary = run_demonstrations(root)
            rows = {row["demonstration"]: row for row in summary["demonstrations"]}
            self.assertEqual(set(rows), {"surface", "mechanisms", "concentration", "stable", "attrition", "interventions"})
            self.assertTrue(all(row["replay_status"] == "replay_verified" for row in rows.values()))
            self.assertEqual(rows["surface"]["views"]["classified_all"]["class_counts"],
                             {"SORT-INS": 4, "SORT-MERGE": 1, "SORT-SEL": 1})
            concentration, stable = rows["concentration"]["checkpoints"], rows["stable"]["checkpoints"]
            self.assertEqual([p["support"] for p in concentration], [3, 2, 1])
            self.assertEqual([(p["sci"]["numerator"], p["sci"]["denominator"]) for p in concentration],
                             [(7, 18), (5, 9), (1, 1)])
            self.assertEqual([p["support"] for p in stable], [3, 3, 3])
            self.assertEqual([p["passing"]["numerator"] for p in stable], [2, 4, 6])
            self.assertEqual([p["observed"] for p in rows["attrition"]["checkpoints"]], [5, 2, 2])
            self.assertEqual(rows["attrition"]["matched_run_ids"], ["A3", "A4"])
            self.assertEqual(rows["interventions"]["intervention_count"], 9)
            self.assertEqual(rows["interventions"]["profile_count"], 4)
            self.assertFalse(summary["candidate_execution_performed"])
            self.assertEqual(summary["model_calls"], 0)

    def test_correction_invalidates_dependents_and_preserves_historical_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            study_dir = root / "study"
            prepare_sources(ROOT / "examples/minimal/sources", study_dir, data_role="fixture")
            old_path = study_dir / "study.json"
            original_study, original = load_study(old_path)
            trace_path, evidence_path = study_dir / "trace.json", study_dir / "evidence.json"
            prepare_trace(old_path, trace_path)
            prepare_evidence(old_path, evidence_path)
            comparison = study_dir / "comparison.json"
            prepare_comparison(old_path, old_path, comparison)
            snapshot = root / "historical"
            create_snapshot("trace", {"study": str(old_path), "design": str(trace_path),
                                      "evidence": str(evidence_path)}, snapshot)
            review_path = study_dir / "review.json"
            review = json.loads(review_path.read_bytes())
            artifact_id = next(row["artifact_id"] for row in original["selected_observations"]
                               if row["assignment_status"] == "accepted")
            entry = next(row for row in review["entries"] if row["artifact_id"] == artifact_id)
            entry.update(decision="unresolved", basis="human_review", class_id=None,
                         reason="insufficient_evidence", reviewer_ref="reviewer:correction",
                         evidence=[], note="Withdraw supplied admission pending further review.")
            review_path.write_bytes(encoded(review))
            new_path = study_dir / "corrected.json"
            receipt = apply_review(old_path, review_path, new_path)
            updated_study, updated = load_study(new_path)
            self.assertEqual(updated["views"]["classified_all"]["population_size"],
                             original["views"]["classified_all"]["population_size"] - 1)
            self.assertEqual(updated_study["revisions"], original_study["revisions"])
            self.assertEqual(updated_study["artifacts"], original_study["artifacts"])
            self.assertEqual(updated_study["assignments"][:-1], original_study["assignments"])
            self.assertEqual(receipt["dependent_bindings"]["previous_study_sha256"], original["study_sha256"])
            self.assertEqual(receipt["dependent_bindings"]["new_study_sha256"], updated["study_sha256"])
            checks = [
                (lambda: analyze_trace(new_path, trace_path), "trace_study_binding_mismatch"),
                (lambda: inspect_study(new_path, evidence_path), "evidence_study_binding_mismatch"),
                (lambda: compare_studies(new_path, old_path, comparison), "comparison_study_binding_mismatch"),
            ]
            for call, code in checks:
                with self.subTest(code=code), self.assertRaises(StudyError) as raised:
                    call()
                self.assertEqual(raised.exception.code, code)
            replayed = replay_snapshot(snapshot)
            self.assertEqual(replayed["status"], "replay_verified")
            self.assertEqual(replayed["result"]["study_sha256"], original["study_sha256"])
            new_design = study_dir / "corrected-trace.json"
            new_evidence = study_dir / "corrected-evidence.json"
            prepare_trace(new_path, new_design)
            prepare_evidence(new_path, new_evidence)
            corrected = analyze_trace(new_path, new_design, new_evidence)
            rows = [row for run in corrected["trajectories"] for row in run["revisions"]]
            target = next(row for row in rows if row["artifact_id"] == artifact_id)
            self.assertEqual(target["assignment_status"], "unresolved")
            self.assertEqual(len(rows), len(original_study["revisions"]))
            self.assertEqual(corrected["cohorts"]["status"], "not_requested")
            current_snapshot = root / "corrected-snapshot"
            create_snapshot("trace", {"study": str(new_path), "design": str(new_design),
                                      "evidence": str(new_evidence)}, current_snapshot)
            self.assertEqual(replay_snapshot(current_snapshot)["result"]["study_sha256"], updated["study_sha256"])


if __name__ == "__main__":
    unittest.main()
