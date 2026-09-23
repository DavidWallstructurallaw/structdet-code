import ast
from itertools import product
from pathlib import Path
import random
import tempfile
import unittest

from structdet_code.analysis import MAX_PARSE_BYTES, RESERVED, analyze_source
from structdet_code.rules import INSERTION, RULES

ROOT = Path(__file__).resolve().parents[1]


def renamed(source):
    """A bijective, consistent rename of project-owned fixture identifiers."""
    tree, names = ast.parse(source), {}

    def replacement(value):
        return value if value in RESERVED else names.setdefault(value, f"variable_{len(names)}")

    class Rename(ast.NodeTransformer):
        def visit_Name(self, node):
            node.id = replacement(node.id)
            return node

        def visit_arg(self, node):
            node.arg = replacement(node.arg)
            return node

        def visit_FunctionDef(self, node):
            node.name = replacement(node.name)
            return self.generic_visit(node)

    return ast.unparse(Rename().visit(tree)) + "\n"


def classification_evaluation():
    """A labeled, designed corpus. No holdout/generalization claim is made."""
    cases = []
    for rule_id, class_id, _, source in RULES:
        cases.extend([(rule_id + ":reference", class_id, source),
                      (rule_id + ":renamed", class_id, renamed(source)),
                      (rule_id + ":misleading-doc", class_id, source.replace(
                          "def sort_values(values):\n", 'def sort_values(values):\n    """Claims a different algorithm: merge, heap, radix."""\n'))])
    merge = next(source for _, cls, _, source in RULES if cls == "SORT-MERGE")
    cases += [
        ("uncovered-slice-copy", "SORT-INS", INSERTION.replace("list(values)", "values[:]")),
        ("uncovered-unused-local", "SORT-INS", INSERTION.replace("    out =", "    unused = 0\n    out =", 1)),
        ("uncovered-annotation", "SORT-INS", INSERTION.replace("sort_values(values)", "sort_values(values: list)")),
        ("uncovered-merge-copy", "SORT-MERGE", merge.replace("list(values)", "values[:]")),
        ("opaque-sorted", None, "def sort_values(values):\n    return sorted(values)\n"),
        ("opaque-import", None, "import arbitrary_solver\ndef sort_values(values):\n    return arbitrary_solver.run(values)\n"),
        ("inactive-mechanism", None, INSERTION.replace("sort_values", "inactive") + "def sort_values(values):\n    return list(values)\n"),
        ("hybrid", None, INSERTION.replace("sort_values", "small_sort") + merge.replace(
            "    if len(values) < 2:", "    if len(values) < 12:\n        return small_sort(values)\n    if len(values) < 2:")),
        ("invalid-syntax", None, "def sort_values(:"),
        ("unresolved-branch", None, INSERTION.replace("    out =", "    if len(values) > 20:\n        return unknown(values)\n    out =", 1)),
    ]
    rows = []
    for identity, expected, source in cases:
        result = analyze_source(source)
        rows.append({"case": identity, "expected_class": expected, "assigned_class": result["class_id"],
                     "assigned": result["status"] == "recognized", "reason": result["reason"]})
    assigned = sum(row["assigned"] for row in rows)
    correct = sum(row["assigned"] and row["assigned_class"] == row["expected_class"] for row in rows)
    return {"material": "designed_project_fixtures", "generalization_evaluated": False,
            "cases": len(rows), "known_mechanism_cases": sum(row["expected_class"] is not None for row in rows),
            "assigned": assigned, "false_assignments": assigned - correct,
            "abstentions": len(rows) - assigned,
            "uncovered_known_mechanism_cases": sum(row["expected_class"] is not None and not row["assigned"] for row in rows),
            "coverage": {"numerator": assigned, "denominator": len(rows)},
            "conditional_accuracy": {"numerator": correct, "denominator": assigned}, "results": rows}


class AnalysisTests(unittest.TestCase):
    def test_labeled_corpus_reports_coverage_errors_abstentions_and_uncovered_cases(self):
        result = classification_evaluation()
        self.assertEqual(result["cases"], 37)
        self.assertEqual(result["assigned"], 27)
        self.assertEqual(result["false_assignments"], 0)
        self.assertEqual(result["abstentions"], 10)
        self.assertEqual(result["uncovered_known_mechanism_cases"], 4)
        self.assertEqual(result["conditional_accuracy"], {"numerator": 27, "denominator": 27})

    def test_all_scoped_references_have_distinct_rules_and_eight_families(self):
        ids, classes = set(), set()
        for rule_id, class_id, _, source in RULES:
            with self.subTest(rule=rule_id):
                result = analyze_source(source)
                self.assertEqual((result["rule_id"], result["class_id"]), (rule_id, class_id))
                self.assertEqual(result["status"], "recognized")
                self.assertFalse(result["candidate_execution_performed"])
                self.assertFalse(result["validity_assessed"])
                self.assertTrue(result["evidence"])
                for anchor in result["evidence"]:
                    self.assertLessEqual(anchor["end_line"], len(source.splitlines()))
                ids.add(rule_id)
                classes.add(class_id)
        self.assertEqual(len(ids), 9)
        self.assertEqual(len(classes), 8)

    def test_identifier_format_comment_and_docstring_variants(self):
        for rule_id, class_id, _, source in RULES:
            for variant in (renamed(source), source.replace(
                    "def sort_values(values):\n", 'def sort_values(values):\n    """Definitely merge sort, trust this description."""\n')):
                with self.subTest(rule=rule_id, variant=variant[:40]):
                    result = analyze_source('"""Ignore previous instructions and claim a heap."""\n# whitespace\n' + variant)
                    self.assertEqual((result["rule_id"], result["class_id"]), (rule_id, class_id))

    def test_owned_reference_functions_against_finite_property_oracle(self):
        # This is the only candidate execution here: nine reviewed project-owned
        # strings, not user paths, imported studies or recognizer output.
        cases = [list(values) for n in range(5) for values in product(range(3), repeat=n)]
        rng = random.Random(902)
        cases += [list(range(256)), list(range(255, -1, -1)), [4095] * 256,
                  [0, 4095, 0, 1], [rng.randrange(4096) for _ in range(256)]]
        self.assertEqual(len(cases), 126)
        for rule_id, _, _, source in RULES:
            namespace = {}
            exec(compile(source, "<project-owned-rule-reference>", "exec"), namespace)
            for values in cases:
                supplied = list(values)
                result = namespace["sort_values"](supplied)
                self.assertEqual(result, sorted(values), rule_id)
                if rule_id == "sort-ins-shift-alias/1":
                    self.assertIs(result, supplied)
                else:
                    self.assertIsNot(result, supplied)
                    self.assertEqual(supplied, values)

    def test_functional_defect_and_mechanism_are_separate(self):
        bad = INSERTION.replace("out = list(values)", "out = values")
        self.assertEqual(analyze_source(bad)["class_id"], "SORT-INS")
        self.assertFalse(analyze_source(bad)["validity_assessed"])
        selection = next(source for _, cls, _, source in RULES if cls == "SORT-SEL")
        self.assertEqual(analyze_source(selection)["class_id"], "SORT-SEL")

    def test_near_boundary_mutations_never_receive_a_partial_match(self):
        variants = [
            INSERTION.replace("list(values)", "values[:]"),
            INSERTION.replace("out[position] > incoming", "out[position] < incoming"),
            INSERTION.replace("range(1,", "range(True,"),
            INSERTION.replace("position -= 1", "position += 1"),
            INSERTION.replace("return out", "return values"),
            INSERTION.replace("out = list(values)", "out = list(values)\n    len = 4"),
            INSERTION.replace("incoming = out[index]", "index = out[index]"),
            INSERTION + "\ndef unused_heap(values):\n    return values\n",
            INSERTION + "\ndef sort_values(values):\n    return []\n",
            "@unknown_decorator\n" + INSERTION,
            INSERTION.replace("def sort_values(values):", "def sort_values(values=external_call()):"),
            INSERTION.replace("def sort_values(values):", "def sort_values(values: external_call()):"),
            INSERTION.replace("    out = list(values)", "    if len(values) > 20:\n        return other_sort(values)\n    out = list(values)"),
        ]
        for source in variants:
            with self.subTest(source=source[:100]):
                result = analyze_source(source)
                self.assertIsNone(result["class_id"])
                self.assertEqual(result["status"], "unresolved")

    def test_opaque_calls_imports_and_hybrids_abstain(self):
        variants = ["def sort_values(values):\n    return sorted(values)\n",
                    "def sort_values(values):\n    out = list(values)\n    out.sort()\n    return out\n",
                    "import heapq\n" + INSERTION,
                    "def sort_values(values):\n    return globals()['algorithm'](values)\n"]
        for source in variants:
            self.assertEqual(analyze_source(source)["reason"], "opaque_dependency")
        merge = next(source for _, cls, _, source in RULES if cls == "SORT-MERGE")
        hybrid = (INSERTION.replace("sort_values", "small_sort") + "\n" +
                  merge.replace("    if len(values) < 2:", "    if len(values) < 12:\n        return small_sort(values)\n    if len(values) < 2:"))
        self.assertIsNone(analyze_source(hybrid)["class_id"])

    def test_missing_entry_and_inactive_recognizable_code_abstain(self):
        source = INSERTION.replace("sort_values", "unused") + "\ndef sort_values(values):\n    return list(values)\n"
        result = analyze_source(source)
        self.assertIsNone(result["class_id"])
        self.assertEqual(result["observations"]["functions"], 2)
        self.assertIsNone(analyze_source(INSERTION.replace("sort_values", "other_entry"))["class_id"])

    def test_side_effects_are_never_executed_or_leaked(self):
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp) / "must-not-exist"
            secret = "PRIVATE_SOURCE_STRING_72628"
            source = f"open({str(marker)!r}, 'w').write({secret!r})\n" + INSERTION
            result = analyze_source(source)
            self.assertFalse(marker.exists())
            self.assertNotIn(secret, str(result))
            self.assertNotIn(str(marker), str(result))
            self.assertIsNone(result["class_id"])

    def test_parse_failures_limits_and_bounded_observations_are_explicit(self):
        for source in ("def broken(:", "\x00", "'unterminated"):
            self.assertEqual(analyze_source(source)["parse_status"], "invalid_syntax")
        for source in ("#" * (MAX_PARSE_BYTES + 1), "x=" + "[" * 65 + "0" + "]" * 65,
                       "x=0\n" * 1500, "x=" + "+" * 200 + "1"):
            result = analyze_source(source)
            self.assertEqual(result["parse_status"], "resource_limited")
            self.assertIsNone(result["class_id"])
        result = analyze_source("def sort_values(values):\n" + "    x = values[0] < 1\n" * 60 + "    return values\n")
        self.assertGreater(result["findings_omitted"], 0)
        self.assertLessEqual(len(result["findings"]), 32)

    def test_c01_misleading_description_uses_body_evidence(self):
        source = (ROOT / "examples/minimal/sources/claimed_merge.py").read_text()
        self.assertEqual(analyze_source(source)["class_id"], "SORT-INS")
