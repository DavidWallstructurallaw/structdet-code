from fractions import Fraction
import unittest

from structdet_code.errors import StudyError
from structdet_code.metrics import count_metrics


class CountTests(unittest.TestCase):
    def test_independent_exact_oracles(self):
        cases = [({"a": 3, "b": 2, "c": 1}, 6, 3, Fraction(7, 18)),
                 ({"a": 4, "b": 2}, 6, 2, Fraction(5, 9)),
                 ({"a": 6}, 6, 1, Fraction(1)),
                 ({"a": 8, "b": 6, "c": 3, "d": 2, "e": 1}, 20, 5, Fraction(57, 200)),
                 ({"a": 1, "b": 1}, 2, 2, Fraction(1, 2))]
        for counts, n, support, sci in cases:
            with self.subTest(counts=counts):
                result = count_metrics(counts, n)
                self.assertEqual(result["observed_support"], support)
                self.assertEqual(Fraction(result["sci"]["numerator"], result["sci"]["denominator"]), sci)
                self.assertEqual(Fraction(result["gini_simpson"]["numerator"], result["gini_simpson"]["denominator"]), 1 - sci)

    def test_empty_population_preserves_undefined_sci(self):
        result = count_metrics({"a": 0}, 0)
        self.assertEqual(result["observed_support"], 0)
        self.assertIsNone(result["sci"]["value"])
        self.assertEqual(result["sci"]["status"], "undefined")

    def test_invalid_denominators_and_counts_are_rejected(self):
        for counts, n in [({"a": 2}, 3), ({"a": True}, 1), ({"a": -1}, -1),
                          ({"a": 1.0}, 1), ({"a": 1}, True), ({"": 1}, 1),
                          ({"a": 1}, None)]:
            with self.subTest(counts=counts, n=n), self.assertRaises(StudyError):
                count_metrics(counts, n)

    def test_zero_class_and_label_permutation_do_not_change_sci(self):
        a = count_metrics({"a": 2, "b": 1, "zero": 0}, 3)
        b = count_metrics({"other": 1, "name": 2}, 3)
        self.assertEqual(a["sci"], b["sci"])
        self.assertEqual(a["observed_support"], b["observed_support"])


if __name__ == "__main__":
    unittest.main()
