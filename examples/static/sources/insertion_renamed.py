def sort_values(values):
    ordered = list(values)
    for frontier in range(1, len(ordered)):
        item = ordered[frontier]
        cursor = frontier - 1
        while cursor >= 0 and ordered[cursor] > item:
            ordered[cursor + 1] = ordered[cursor]
            cursor -= 1
        ordered[cursor + 1] = item
    return ordered
