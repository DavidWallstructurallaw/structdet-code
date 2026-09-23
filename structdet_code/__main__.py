"""Passive inspection and explicit source/review preparation commands."""

import argparse
import json
import sys

from . import __version__
from .errors import StudyError
from .comparison import compare_studies, comparison_markdown, prepare_comparison
from .reporting import markdown
from .study import inspect_study
from .workflow import apply_review, prepare_review, prepare_sources


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="structdet-code")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "inspect"):
        command = commands.add_parser(name)
        command.add_argument("--study", required=True)
        if name == "inspect":
            command.add_argument("--format", choices=("json", "markdown"), default="json")
    prepare = commands.add_parser("prepare", help="Copy an explicit local source collection into a new study")
    prepare.add_argument("--sources", required=True)
    prepare.add_argument("--include", action="append", help="Relative .py path; repeat for explicit nested selections")
    prepare.add_argument("--output", required=True)
    prepare.add_argument("--study-id", default="local-collection")
    prepare.add_argument("--data-role", choices=("fixture", "descriptive"), default="descriptive")
    prepare.add_argument("--task", choices=("sorting-bounded", "unit-graph-distances"), default="sorting-bounded")
    review = commands.add_parser("review-template", help="Create a blank, source-bound decision template")
    review.add_argument("--study", required=True)
    review.add_argument("--output", required=True)
    apply = commands.add_parser("apply-review", help="Append supplied decisions into a new study manifest")
    apply.add_argument("--study", required=True)
    apply.add_argument("--review", required=True)
    apply.add_argument("--output", required=True)
    for name in ("comparison-template", "compare"):
        command = commands.add_parser(name)
        command.add_argument("--left", required=True)
        command.add_argument("--right", required=True)
        if name == "comparison-template":
            command.add_argument("--output", required=True)
        else:
            command.add_argument("--design")
            command.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare_sources(args.sources, args.output, args.study_id, args.data_role, args.include, args.task)
        elif args.command == "review-template":
            result = prepare_review(args.study, args.output)
        elif args.command == "apply-review":
            result = apply_review(args.study, args.review, args.output)
        elif args.command == "comparison-template":
            result = prepare_comparison(args.left, args.right, args.output)
        elif args.command == "compare":
            result = compare_studies(args.left, args.right, args.design)
        else:
            result = inspect_study(args.study)
    except StudyError as exc:
        print(json.dumps({"status": "invalid", "code": exc.code}), file=sys.stderr)
        return 2
    except OSError:
        print(json.dumps({"status": "invalid", "code": "io_operation_failed"}), file=sys.stderr)
        return 2
    if args.command == "validate":
        print(json.dumps({"status": "valid_records", "study_id": result["study_id"],
                          "substantive_validation_performed": False}))
    elif args.command == "inspect" and args.format == "markdown":
        print(markdown(result), end="")
    elif args.command == "compare" and args.format == "markdown":
        print(comparison_markdown(result), end="")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
