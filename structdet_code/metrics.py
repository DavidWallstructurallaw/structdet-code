"""Exact descriptive arithmetic over an already admitted hard-label population.

Method: empirical-class-counts/0.1. No classification, execution, smoothing,
sample independence, or population-capacity estimate is implied.
"""

from collections.abc import Mapping
from fractions import Fraction
import re

from .errors import require


def _ratio(value: Fraction | None) -> dict:
    if value is None:
        return {"status": "undefined", "reason": "empty_classified_population",
                "value": None, "numerator": None, "denominator": None}
    return {"status": "available", "reason": None, "value": float(value),
            "numerator": value.numerator, "denominator": value.denominator}


def count_metrics(counts: Mapping[str, int], population_size: int) -> dict:
    """Summarize nonnegative class counts whose sum equals the supplied n."""
    require(isinstance(counts, Mapping) and len(counts) <= 4096, "invalid_count_table")
    require(type(population_size) is int and population_size >= 0
            and population_size.bit_length() <= 4096, "invalid_population_size")
    require(all(isinstance(k, str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{0,63}", k)
                and type(v) is int and v >= 0 and v.bit_length() <= 4096
                for k, v in counts.items()), "invalid_count_table")
    require(sum(counts.values()) == population_size, "count_conservation_failed")
    sci = (Fraction(sum(v * v for v in counts.values()), population_size ** 2)
           if population_size else None)
    return {
        "method": "empirical-class-counts/0.1",
        "population_size": population_size,
        "class_counts": dict(sorted(counts.items())),
        "observed_support": sum(v > 0 for v in counts.values()),
        "qualifiers": [] if population_size else ["empty_classified_population"],
        "sci": _ratio(sci),
        "gini_simpson": _ratio(1 - sci if sci is not None else None),
        "uncertainty": "not_estimated",
    }
