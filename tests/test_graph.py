import ast
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import tempfile
import unittest

from structdet_code.analysis import RESERVED, analyze_source
from structdet_code.errors import StudyError
from structdet_code.graph_rules import FIFO, RULES
from structdet_code.io import digest
from structdet_code.study import inspect_study, task_pack
from structdet_code.workflow import apply_review, encoded, prepare_review, prepare_sources
from tools.build_graph_example import distance_oracle

PACK = "unit-graph-distances"
ROOT = Path(__file__).resolve().parents[1]


def renamed(source):
    tree, names = ast.parse(source), {}
    def replacement(value):
        return value if value in RESERVED | {"shortest_distances"} else names.setdefault(value, f"local_{len(names)}")
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
    cases = []
    for rule_id, class_id, _, source in RULES:
        cases += [(rule_id + ":reference", class_id, source),
                  (rule_id + ":renamed", class_id, renamed(source)),
                  (rule_id + ":misleading-comment", class_id,
                   '"""This computes a completely different mechanism."""\n' + source)]
    settle = next(source for _, cls, _, source in RULES if cls == "DIST-SETTLE")
    cases += [
        ("uncovered-fifo-storage", "DIST-FIFO", FIFO.replace("frontier[head]", "frontier.pop(0)").replace("        head += 1\n", "")),
        ("uncovered-fifo-annotation", "DIST-FIFO", FIFO.replace("node_count, edges", "node_count: int, edges")),
        ("uncovered-settlement-local", "DIST-SETTLE", settle.replace("    settled =", "    unused = 0\n    settled =", 1)),
        ("opaque-import", None, "import unknown_solver\n" + FIFO),
        ("opaque-call", None, "def shortest_distances(node_count, edges, start):\n    return unknown_solver(node_count, edges, start)\n"),
        ("inactive", None, FIFO.replace("shortest_distances", "unused") + "def shortest_distances(node_count, edges, start):\n    return []\n"),
        ("hybrid", None, FIFO.replace("shortest_distances", "fifo") + settle.replace(
            "    neighbors =", "    if node_count < 10:\n        return fifo(node_count, edges, start)\n    neighbors =", 1)),
        ("dag-only-single-pass", None, "def shortest_distances(node_count, edges, start):\n    distances = [None] * node_count\n    distances[start] = 0\n    for source, target in edges:\n        if distances[source] is not None:\n            distances[target] = distances[source] + 1\n    return distances\n"),
        ("wrong-entry", None, FIFO.replace("shortest_distances", "shortest_path")),
        ("parse-failure", None, "def shortest_distances(:"),
    ]
    rows = []
    for identity, expected, source in cases:
        result = analyze_source(source, PACK)
        rows.append({"case": identity, "expected_class": expected, "assigned_class": result["class_id"],
                     "assigned": result["status"] == "recognized", "reason": result["reason"]})
    assigned = sum(row["assigned"] for row in rows)
    correct = sum(row["assigned"] and row["expected_class"] == row["assigned_class"] for row in rows)
    return {"material": "designed_project_fixtures", "generalization_evaluated": False,
            "cases": len(rows), "assigned": assigned, "false_assignments": assigned - correct,
            "abstentions": len(rows) - assigned,
            "uncovered_known_mechanism_cases": sum(row["expected_class"] is not None and not row["assigned"] for row in rows),
            "coverage": {"numerator": assigned, "denominator": len(rows)},
            "conditional_accuracy": {"numerator": correct, "denominator": assigned}, "results": rows}


class GraphTests(unittest.TestCase):
    def test_designed_classifier_coverage_and_conditional_accuracy_are_separate(self):
        result = classification_evaluation()
        self.assertEqual((result["cases"], result["assigned"], result["abstentions"]), (22, 12, 10))
        self.assertEqual(result["false_assignments"], 0)
        self.assertEqual(result["uncovered_known_mechanism_cases"], 3)
        self.assertEqual(result["conditional_accuracy"], {"numerator": 12, "denominator": 12})

    def test_three_mechanisms_four_rules_are_task_bound_and_passive(self):
        classes = set()
        for rule, cls, _, source in RULES:
            result = analyze_source(source, PACK)
            self.assertEqual((result["rule_id"], result["class_id"]), (rule, cls))
            self.assertFalse(result["validity_assessed"])
            self.assertFalse(result["candidate_execution_performed"])
            self.assertTrue(result["evidence"])
            self.assertIsNone(analyze_source(source, "sorting-bounded")["class_id"])
            classes.add(cls)
        self.assertEqual(classes, {"DIST-FIFO", "DIST-SETTLE", "DIST-RELAX"})
        for bad in ("weighted-graph", [], None):
            with self.assertRaises(StudyError):
                task_pack(bad)

    def test_owned_references_on_exhaustive_small_graphs_and_boundary_cases(self):
        # Only explicitly reviewed project-owned strings are executed here.
        cases = []
        for n in range(1, 4):
            pairs = list(product(range(n), repeat=2))
            for mask in range(1 << len(pairs)):
                edges = [list(edge) for bit, edge in enumerate(pairs) if mask & (1 << bit)]
                for start in range(n):
                    cases.append((n, edges, start))
        self.assertEqual(len(cases), 1570)
        cases += [(128, [[i, i + 1] for i in range(126, -1, -1)], 0),
                  (128, [list(edge) for edge in product(range(128), repeat=2)], 127),
                  (128, [], 127), (4, [[0, 1], [0, 1], [1, 1], [1, 2], [2, 0]], 0)]
        expected = [distance_oracle(n, edges, start) for n, edges, start in cases]
        defect_failures = 0
        for rule, _, _, source in RULES:
            namespace = {}
            exec(compile(source, "<project-owned-graph-reference>", "exec"), namespace)
            for (n, edges, start), oracle in zip(cases, expected):
                supplied = deepcopy(edges)
                actual = namespace["shortest_distances"](n, supplied, start)
                self.assertIs(type(actual), list)
                self.assertEqual(len(actual), n)
                self.assertTrue(all(v is None or type(v) is int and v >= 0 for v in actual))
                self.assertIsNot(actual, supplied)
                self.assertTrue(all(actual is not edge for edge in supplied))
                self.assertEqual(supplied, edges)
                if rule == "dist-fifo-step-defect/1":
                    defect_failures += actual != oracle
                    oracle = [v * 2 if v is not None else None for v in oracle]
                self.assertEqual(actual, oracle, rule)
        self.assertGreater(defect_failures, 0)

    def test_mutations_and_active_versus_inactive_code_do_not_get_partial_matches(self):
        variants = [FIFO.replace("+ 1", "+ True"), FIFO.replace("distances[start] = 0", "distances[start] = 1"),
                    FIFO.replace("distances[neighbor] is None", "distances[neighbor] is not None"),
                    FIFO.replace("frontier.append(neighbor)", "frontier.append(current)"),
                    FIFO.replace("head += 1", "head -= 1"), FIFO + "\ndef inactive():\n    return None\n",
                    FIFO.replace("    neighbors =", "    if node_count > 50:\n        return other(node_count, edges, start)\n    neighbors =", 1)]
        for source in variants:
            self.assertIsNone(analyze_source(source, PACK)["class_id"])

    def test_graph_prepare_review_and_inspect_use_same_bindings(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "input").mkdir()
            (root / "input/program.py").write_text(FIFO)
            prepare_sources(root / "input", root / "study", pack_id=PACK)
            manifest_path = root / "study/study.json"
            result = inspect_study(manifest_path)
            self.assertEqual(result["views"]["classified_all"]["class_counts"], {"DIST-FIFO": 1})
            self.assertEqual(result["ledger"]["test_receipts"], 0)
            prepare_review(manifest_path, root / "review.json")
            review = json.loads((root / "review.json").read_bytes())
            review["entries"][0].update(decision="accepted", basis="human_review", class_id="DIST-FIFO",
                                        reason=None, reviewer_ref="supplied-reviewer",
                                        evidence=[{"start_line": 1, "end_line": len(FIFO.splitlines()), "note": "FIFO first discovery."}])
            (root / "review.json").write_bytes(encoded(review))
            apply_review(manifest_path, root / "review.json", root / "study/reviewed.json")
            self.assertEqual(inspect_study(root / "study/reviewed.json")["ledger"]["admitted_bases"], {"human_review": 1})

    def test_suite_domain_checks_reject_weighted_edges_bools_and_invalid_vertices(self):
        bad_inputs = [
            {"node_count": 0, "edges": [], "start": 0}, {"node_count": 129, "edges": [], "start": 0},
            {"node_count": True, "edges": [], "start": 0}, {"node_count": 2, "edges": [], "start": 2},
            {"node_count": 2, "edges": [], "start": False}, {"node_count": 2, "edges": [[0, 1, 1]], "start": 0},
            {"node_count": 2, "edges": [[-1, 0]], "start": 0}, {"node_count": 2, "edges": [[0, 2]], "start": 0},
            {"node_count": 2, "edges": [[0, True]], "start": 0}, {"node_count": 2, "edges": [[0, 1]] * 16385, "start": 0},
            {"node_count": 2, "edges": [[0, 1]], "start": 0, "directed": False},
        ]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "input").mkdir()
            (root / "input/program.py").write_text(FIFO)
            prepare_sources(root / "input", root / "study", pack_id=PACK)
            path = root / "study/study.json"
            study = json.loads(path.read_bytes())
            for graph in bad_inputs:
                suite = {"schema_version": "structdet-code.graph-suite/0.1", "oracle_id": "unit-distance-properties/0.1",
                         "cases": [{"id": "T1", "input": graph}]}
                raw = json.dumps(suite).encode()
                (path.parent / "suite.json").write_bytes(raw)
                study["suites"] = [{"id": "S1", "path": "suite.json", "sha256": digest(raw), "oracle_id": suite["oracle_id"]}]
                path.write_bytes(encoded(study))
                with self.subTest(graph=str(graph)[:100]), self.assertRaises(StudyError):
                    inspect_study(path)

    def test_graph_source_with_side_effect_remains_passive(self):
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp) / "side-effect"
            secret = "PRIVATE_GRAPH_SOURCE"
            source = f"open({str(marker)!r}, 'w').write({secret!r})\n" + FIFO
            result = analyze_source(source, PACK)
            self.assertFalse(marker.exists())
            self.assertNotIn(secret, str(result))
            self.assertIsNone(result["class_id"])
