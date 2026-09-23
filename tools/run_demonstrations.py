"""Run six passive, owned demonstrations and replay every saved analysis."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from structdet_code.errors import StudyError
from structdet_code.examples import run_demonstrations


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="New directory for the six fixture snapshots")
    args = parser.parse_args()
    try:
        value = run_demonstrations(args.output)
    except (StudyError, OSError) as exc:
        print(json.dumps({"status": "invalid", "code": getattr(exc, "code", "output_unavailable")}), file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps(value, indent=2))
