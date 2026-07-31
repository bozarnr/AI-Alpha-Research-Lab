import unittest

from ai_alpha_lab.demo import synthetic_panel
from ai_alpha_lab.expressions import FormulaContract, FormulaError, evaluate_formula
from ai_alpha_lab.loop import CandidateRecord, rejection_gallery, summarize_loop
from ai_alpha_lab.research import PromotionGate, evaluate_candidate


class FormulaSafetyTests(unittest.TestCase):
    def setUp(self):
        self.panel = synthetic_panel()
        self.contract = FormulaContract(frozenset({"close", "amount", "returns"}))

    def test_formula_uses_past_data_only(self):
        output = evaluate_formula("rank(delta(amount, 3))", self.panel, self.contract)
        self.assertEqual(len(output), len(self.panel))
        self.assertTrue(output.isna().any())

    def test_future_field_is_rejected(self):
        with self.assertRaises(FormulaError):
            evaluate_formula("forward_return", self.panel, self.contract)

    def test_unsorted_panel_is_rejected(self):
        with self.assertRaises(FormulaError):
            evaluate_formula("rank(amount)", self.panel.sample(frac=1, random_state=1), self.contract)

    def test_demo_candidate_is_not_promoted(self):
        result = evaluate_candidate(
            "rank(delta(amount, 3)) - rank(mean(returns, 5))",
            self.panel,
            split_date="2024-03-15",
            gate=PromotionGate(min_oos_rank_ic=0.05, max_turnover=0.60),
        )
        self.assertFalse(result["promoted"])

    def test_costs_reduce_reported_net_return(self):
        result = evaluate_candidate(
            "rank(delta(amount, 3))",
            self.panel,
            split_date="2024-03-15",
            gate=PromotionGate(transaction_cost_bps=30),
        )
        self.assertLessEqual(result["oos_net_return"], result["oos_gross_return"])

    def test_rejection_gallery_sorts_best_rejected_candidates_first(self):
        records = [
            CandidateRecord("rank(amount)", 0.01, -0.001, 0.7, False, "too costly"),
            CandidateRecord("rank(close)", 0.03, -0.002, 0.8, False, "too costly"),
            CandidateRecord("rank(returns)", 0.06, 0.001, 0.4, True, "passed"),
        ]

        summary = summarize_loop(records)
        gallery = rejection_gallery(records, limit=1)

        self.assertEqual(summary.promoted_candidates, 1)
        self.assertEqual(summary.rejection_reasons, {"too costly": 2})
        self.assertEqual(gallery[0]["formula"], "rank(close)")


if __name__ == "__main__":
    unittest.main()
