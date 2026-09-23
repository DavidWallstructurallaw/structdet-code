"""C01 passive command-line entry point."""

import argparse
import json
import sys

from . import __version__
from .errors import StudyError
from .reporting import markdown
from .study import inspect_study


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="structdet-code")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "inspect"):
        command = commands.add_parser(name)
        command.add_argument("--study", required=True)
        if name == "inspect":
            command.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        result = inspect_study(args.study)
    except StudyError as exc:
        print(json.dumps({"status": "invalid", "code": exc.code}), file=sys.stderr)
        return 2
    if args.command == "validate":
        print(json.dumps({"status": "valid_records", "study_id": result["study_id"],
                          "substantive_validation_performed": False}))
    elif args.format == "markdown":
        print(markdown(result), end="")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
