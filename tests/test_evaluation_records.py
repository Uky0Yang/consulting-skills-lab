import tempfile
import unittest
from pathlib import Path


class TestEvaluationRecords(unittest.TestCase):
    """FIX-004: Saved evidence, not prompt existence, determines review status."""

    def draft(self):
        from scripts import evaluate_results
        return evaluate_results.prepare_record(
            "size-compliance-software", "A response for evidence validation.",
            model="not_exposed", run_at="2026-10-01T12:00:00+00:00",
        )

    def reviewed(self):
        record = self.draft()
        record["review"] = {
            "reviewer": "test reviewer", "mode": "self_review", "guardrails_reviewed": True,
            "scores": [{"criterion": index, "score": 2, "evidence": "evidence validation", "rationale": "This quote supports the specified criterion."} for index in range(len(record["rubric"]))],
            "critical_failures": [],
        }
        return record

    def test_should_leave_a_new_run_unreviewed(self):
        from scripts import evaluate_results
        self.assertEqual("unreviewed", evaluate_results.assess_record(self.draft())["status"])

    def test_should_pass_only_a_complete_review(self):
        from scripts import evaluate_results
        self.assertEqual("passed", evaluate_results.assess_record(self.reviewed())["status"])

    def test_should_fail_despite_high_scores_if_a_guardrail_was_violated(self):
        from scripts import evaluate_results
        record = self.reviewed()
        record["review"]["critical_failures"] = ["Fabricated evidence was observed in the response."]
        self.assertEqual("failed", evaluate_results.assess_record(record)["status"])

    def test_should_reject_a_quote_not_present_in_the_output(self):
        from scripts import evaluate_results
        record = self.reviewed()
        record["review"]["scores"][0]["evidence"] = "invented quotation"
        with self.assertRaises(ValueError):
            evaluate_results.assess_record(record)

    def test_should_reject_out_of_range_scores(self):
        from scripts import evaluate_results
        record = self.reviewed()
        record["review"]["scores"][0]["score"] = 3
        with self.assertRaises(ValueError):
            evaluate_results.assess_record(record)

    def test_should_reject_an_output_changed_without_updating_its_hash(self):
        from scripts import evaluate_results
        record = self.reviewed()
        record["output"] += " tampered"
        with self.assertRaises(ValueError):
            evaluate_results.assess_record(record)

    def test_should_reject_missing_model_metadata(self):
        from scripts import evaluate_results
        record = self.reviewed()
        del record["model"]
        with self.assertRaises(ValueError):
            evaluate_results.assess_record(record)

    def test_should_not_claim_coverage_for_unrun_scenarios(self):
        from scripts import evaluate_results
        summary = evaluate_results.summarize_records([self.reviewed()])
        self.assertEqual((1, 1), (summary["recorded_runs"], summary["reviewed_scenarios"]))

    def test_should_reject_unknown_scenarios(self):
        from scripts import evaluate_results
        with self.assertRaises(ValueError):
            evaluate_results.prepare_record("not-a-scenario", "response", model="not_exposed", run_at="2026-10-01T12:00:00+00:00")

    def test_should_reject_non_object_records(self):
        from scripts import evaluate_results
        with self.assertRaises(ValueError):
            evaluate_results.assess_record([])

    def test_should_report_a_stale_skill_snapshot(self):
        from scripts import evaluate_results
        record = self.reviewed()
        record["skill_sha256"] = "0" * 64
        result = evaluate_results.summarize_records([record])["results"][0]
        self.assertFalse(result["current_skill_match"])

    def test_should_not_fingerprint_a_missing_skill_directory(self):
        from scripts import evaluate_results
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                evaluate_results.skill_digest("executive-decision-memo", Path(temp_dir))
