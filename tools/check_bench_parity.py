"""Compare finite count arithmetic with an explicitly trusted pinned Bench source.

This developer command imports the supplied trusted source; do not point it at
candidate programs or untrusted repositories. It is not used by passive intake.
"""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
PIN = "0a9dc88deffd4b14264485b161bea06f027f68f5"
HASHES = {
    "structdet_bench/__init__.py": "9c8c3178053045f6272735257126a22f2ad4c4b31f55f4e8dc3d668cf01cef31",
    "structdet_bench/contracts.py": "a9d88b10d13afa0ddc967804d90b9ac48679eaf45e9aed5d5ead16880e93440a",
    "structdet_bench/populations.py": "33d53b4698bfe69f9a2ae7acd5532e349d3db7773a45b7533e7378c3ee9044f1",
    "structdet_bench/records.py": "c34bacbd1f0c7db490b596ff6334e8fe44c3d9425cbcaeb8473a0e99e0620046",
    "structdet_bench/metrics.py": "f4bbe94e755d2870cbf07c4488834aaa29d2adba16270c30f9549b23f4f69ff4",
    "structdet_bench/evidence.py": "bdf8e3f1c7c190dcb0052202e2d90ed8dbf1a5c00826c7b5c784b1f96026fa61",
    "structdet_bench/inventory.py": "c9f03643944d3096aa276bd6bebc52df49cb9b907af254a317a843fb7c72d554",
    "structdet_bench/local_io.py": "2e38fa7a23c398488a6691a47511526dc26c0109ea048bc85baa7bcceabb81f3",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bench-root", required=True, type=Path)
    args = parser.parse_args()
    bench = args.bench_root.resolve()
    for name, expected in HASHES.items():
        if hashlib.sha256((bench / name).read_bytes()).hexdigest() != expected:
            raise SystemExit("Pinned Bench source bytes do not match: " + name)
    sys.path.insert(0, str(bench))
    sys.path.insert(0, str(ROOT))
    from structdet_bench.metrics import count_metrics as upstream
    from structdet_code.metrics import count_metrics
    vectors = [(), (0,), (1,), (6,), (1, 1), (3, 2, 1), (4, 2), (8, 6, 3, 2, 1),
               (0, 2, 1), (0, 0, 0), (100, 1), (7, 3, 1), (10**12, 2, 1)]
    checked = []
    for vector in vectors:
        counts = {f"C{i}": value for i, value in enumerate(vector)}
        n = sum(vector)
        reference, result = upstream(counts, n), count_metrics(counts, n)
        assert reference.results["observed_support_size"].value == result["observed_support"]
        if n:
            sci = reference.results["structural_concentration_index"].exact_ratio
            assert sci == (result["sci"]["numerator"], result["sci"]["denominator"])
            assert 1 - Fraction(*sci) == Fraction(result["gini_simpson"]["numerator"], result["gini_simpson"]["denominator"])
        else:
            assert reference.results["structural_concentration_index"].result_status == result["sci"]["status"] == "undefined"
        checked.append({"counts": counts, "n": n, "support": result["observed_support"],
                        "sci": [result["sci"]["numerator"], result["sci"]["denominator"]]})
    print(json.dumps({"status": "passed", "baseline_commit": PIN,
                      "baseline_metric_definition": "MET-0.2",
                      "code_method": "empirical-class-counts/0.1",
                      "environment": {"python": platform.python_version(), "platform": platform.system()},
                      "scope": "supplied_count_tables_only; no upstream runtime or empirical qualification",
                      "verified_source_hashes": HASHES, "cases": checked}, indent=2))


if __name__ == "__main__":
    main()
