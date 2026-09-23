"""Bounded passive AST observations and exact scoped reference recognition.

No source is compiled to executable code or imported. Whole-module equality
retains operators, constants, binding-name equality, calls and statement order.
Only formatting/comments, leading docstrings and bijective non-reserved name
changes are ignored. Partial feature matches never create an admitted label.
"""

import ast
import builtins
from functools import lru_cache
import io
import tokenize

from .io import digest
from .errors import require
from .rules import RULES, SCOPE
from .graph_rules import RULES as GRAPH_RULES, SCOPE as GRAPH_SCOPE

MAX_PARSE_BYTES = 65_536
MAX_TOKENS = 4096
MAX_NODES = 4096
MAX_DEPTH = 64
MAX_FINDINGS = 32
RESERVED = frozenset(dir(builtins)) | {"sort_values"}
ORDINARY_CALLS = {"list", "len", "range", "enumerate", "min", "max", "abs"}
ORDINARY_METHODS = {"append", "extend", "pop", "copy"}


class _ParseLimit(Exception):
    pass


def _body(statements):
    if (statements and isinstance(statements[0], ast.Expr)
            and isinstance(statements[0].value, ast.Constant)
            and isinstance(statements[0].value.value, str)):
        return statements[1:]
    return statements


def _parse(source):
    if len(source.encode("utf-8")) > MAX_PARSE_BYTES:
        raise _ParseLimit
    nesting = 0
    for index, token in enumerate(tokenize.generate_tokens(io.StringIO(source).readline)):
        if index >= MAX_TOKENS:
            raise _ParseLimit
        if token.type == tokenize.OP:
            if token.string in {"(", "[", "{"}:
                nesting += 1
            elif token.string in {")", "]", "}"}:
                nesting -= 1
            if nesting > MAX_DEPTH:
                raise _ParseLimit
    tree = ast.parse(source, mode="exec", feature_version=(3, 12))
    pending, nodes, depth = [(tree, 0)], [], 0
    while pending:
        node, level = pending.pop()
        nodes.append(node)
        depth = max(depth, level)
        if len(nodes) > MAX_NODES or level > MAX_DEPTH:
            raise _ParseLimit
        pending.extend((child, level + 1) for child in ast.iter_child_nodes(node))
    return tree, nodes, depth


def _canonical(tree, entry_point="sort_values"):
    names = {}
    reserved = frozenset(dir(builtins)) | {entry_point}

    def name(value):
        if value in reserved:
            return ("reserved", value)
        return ("symbol", names.setdefault(value, len(names)))

    def visit(value):
        if isinstance(value, ast.AST):
            pairs = []
            for key, child in ast.iter_fields(value):
                if ((isinstance(value, ast.Name) and key == "id")
                        or (isinstance(value, ast.FunctionDef) and key == "name")
                        or (isinstance(value, ast.arg) and key == "arg")):
                    child = name(child)
                elif key == "body" and isinstance(value, (ast.Module, ast.FunctionDef)):
                    child = _body(child)
                pairs.append((key, visit(child)))
            return (type(value).__name__, tuple(pairs))
        if isinstance(value, (list, tuple)):
            return tuple(visit(v) for v in value)
        # Preserve constant type as well as value: True must not equal 1.
        return (type(value).__name__, value)

    return visit(tree)


def _rule_set(pack_id):
    require(isinstance(pack_id, str), "unsupported_task_pack")
    if pack_id == "sorting-bounded":
        return RULES, SCOPE, "sort_values", "sorting-static/1"
    if pack_id == "unit-graph-distances":
        return GRAPH_RULES, GRAPH_SCOPE, "shortest_distances", "unit-graph-static/1"
    require(False, "unsupported_task_pack")


@lru_cache(maxsize=2)
def _references(pack_id):
    references = []
    rules, _, entry, _ = _rule_set(pack_id)
    for rule_id, class_id, explanation, source in rules:
        tree, _, _ = _parse(source)
        references.append((_canonical(tree, entry), rule_id, class_id, explanation))
    return references


def _anchor(node, note):
    return {"start_line": node.lineno, "end_line": node.end_lineno, "note": note}


def analyze_source(source: str, pack_id="sorting-bounded") -> dict:
    """Return observations and a rule result; do not assess functional validity."""
    _, scope, entry_point, analyzer_id = _rule_set(pack_id)
    result = {
        "analyzer_id": analyzer_id, "scope": scope,
        "source_sha256": digest(source.encode("utf-8")),
        "parse_status": "unexamined", "status": "unresolved", "class_id": None,
        "rule_id": None, "reason": "insufficient_evidence", "evidence": [],
        "observations": {}, "findings": [], "findings_omitted": 0,
        "candidate_execution_performed": False, "validity_assessed": False,
    }
    try:
        tree, nodes, depth = _parse(source)
    except (_ParseLimit, RecursionError, MemoryError):
        result.update(parse_status="resource_limited", reason="unsupported_syntax")
        return result
    except (SyntaxError, ValueError, tokenize.TokenError, UnicodeError):
        result.update(parse_status="invalid_syntax", reason="unsupported_syntax")
        return result
    result["parse_status"] = "parsed"
    functions = [n for n in nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    calls = [n for n in nodes if isinstance(n, ast.Call)]
    loops = [n for n in nodes if isinstance(n, (ast.For, ast.While, ast.AsyncFor))]
    comparisons = [n for n in nodes if isinstance(n, ast.Compare)]
    writes = [n for n in nodes if isinstance(n, ast.Subscript) and isinstance(n.ctx, ast.Store)]
    imports = [n for n in nodes if isinstance(n, (ast.Import, ast.ImportFrom))]
    definitions = {n.name for n in functions}
    opaque = []
    for call in calls:
        if isinstance(call.func, ast.Name):
            if call.func.id not in definitions | ORDINARY_CALLS:
                opaque.append(call)
        elif not isinstance(call.func, ast.Attribute) or call.func.attr not in ORDINARY_METHODS:
            opaque.append(call)
    findings = []
    for group, label in ((functions, "function_definition"), (loops, "loop"),
                         (comparisons, "comparison"), (writes, "subscript_write"),
                         (calls, "call_site"), (imports, "import"), (opaque, "unresolved_call")):
        findings.extend({"kind": label, "start_line": n.lineno, "end_line": n.end_lineno}
                        for n in group)
    findings.sort(key=lambda f: (f["start_line"], f["end_line"], f["kind"]))
    result["findings"] = findings[:MAX_FINDINGS]
    result["findings_omitted"] = max(0, len(findings) - MAX_FINDINGS)
    result["observations"] = {
        "ast_nodes": len(nodes), "ast_depth": depth, "functions": len(functions),
        "loops": len(loops), "comparisons": len(comparisons), "calls": len(calls),
        "subscript_writes": len(writes), "imports": len(imports),
        "unresolved_call_sites": len(opaque),
        "top_level_nondefinition_statements": sum(not isinstance(n, ast.FunctionDef) for n in _body(tree.body)),
        "reachability": "not_established_by_observations",
    }
    if imports or opaque:
        result["reason"] = "opaque_dependency"
        return result
    fingerprint = _canonical(tree, entry_point)
    matches = [r for r in _references(pack_id) if r[0] == fingerprint]
    if len(matches) == 1:
        _, rule_id, class_id, explanation = matches[0]
        entry = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == entry_point)
        evidence = [_anchor(entry, explanation)]
        operative = sorted(loops + comparisons + writes, key=lambda n: (n.lineno, n.end_lineno))
        for node in operative[:7]:
            evidence.append(_anchor(node, "Operative structure retained by the complete rule match."))
        result.update(status="recognized", class_id=class_id, rule_id=rule_id,
                      reason=None, evidence=evidence)
        result["observations"]["reachability"] = "within_exact_reference_scope"
    elif len(matches) > 1:
        result["reason"] = "review_disagreement"
    return result
