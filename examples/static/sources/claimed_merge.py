def sort_values(values):
    """Claim: merge sort. The label must not establish membership."""
    result = list(values)
    for boundary in range(1, len(result)):
        value = result[boundary]
        slot = boundary - 1
        while slot >= 0 and result[slot] > value:
            result[slot + 1] = result[slot]
            slot -= 1
        result[slot + 1] = value
    return result
