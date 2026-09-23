"""Project-owned reference programs for narrowly scoped sorting rules.

These strings are parsed as data by the recognizer, never imported or executed
by the product. Tests may execute these reviewed, project-owned references.
Changing an operative reference requires a new rule ID. See docs/C02.md.
"""

SCOPE = "sorting-whole-module-alpha-ast/1"

INSERTION = '''def sort_values(values):
    out = list(values)
    for index in range(1, len(out)):
        incoming = out[index]
        position = index - 1
        while position >= 0 and out[position] > incoming:
            out[position + 1] = out[position]
            position -= 1
        out[position + 1] = incoming
    return out
'''

# id, class, descriptor explanation, complete reference source
RULES = (
    ("sort-adj-sweep/1", "SORT-ADJ",
     "Repeated adjacent comparisons and swaps order a shrinking prefix.",
     '''def sort_values(values):
    out = list(values)
    for end in range(len(out) - 1, 0, -1):
        for index in range(end):
            if out[index] > out[index + 1]:
                out[index], out[index + 1] = out[index + 1], out[index]
    return out
'''),
    ("sort-ins-shift-copy/1", "SORT-INS",
     "Each incoming value is placed in an ordered prefix by shifting larger values.",
     INSERTION),
    ("sort-ins-shift-alias/1", "SORT-INS",
     "Prefix insertion is recognizable despite reusing the caller's input list.",
     INSERTION.replace("out = list(values)", "out = values")),
    ("sort-sel-extract/1", "SORT-SEL",
     "A full scan selects the next minimum from the remaining unordered values.",
     '''def sort_values(values):
    remaining = list(values)
    result = []
    while remaining:
        selected = 0
        for index in range(1, len(remaining)):
            if remaining[index] < remaining[selected]:
                selected = index
        result.append(remaining.pop(selected))
    return result
'''),
    ("sort-merge-halves/1", "SORT-MERGE",
     "Recursively ordered halves are combined through advancing head comparisons.",
     '''def sort_values(values):
    if len(values) < 2:
        return list(values)
    midpoint = len(values) // 2
    left = sort_values(values[:midpoint])
    right = sort_values(values[midpoint:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
'''),
    ("sort-pivot-three-way/1", "SORT-PIVOT",
     "Values are partitioned around a pivot; strict partitions are recursively ordered.",
     '''def sort_values(values):
    if len(values) < 2:
        return list(values)
    pivot = values[0]
    lower = []
    equal = []
    upper = []
    for value in values:
        if value < pivot:
            lower.append(value)
        elif value > pivot:
            upper.append(value)
        else:
            equal.append(value)
    return sort_values(lower) + equal + sort_values(upper)
'''),
    ("sort-heap-max-extract/1", "SORT-HEAP",
     "A binary max-heap is restored by sift-down and its maximum repeatedly extracted.",
     '''def sort_values(values):
    out = list(values)
    def sift(root, stop):
        while 2 * root + 1 < stop:
            child = 2 * root + 1
            if child + 1 < stop and out[child] < out[child + 1]:
                child += 1
            if out[root] >= out[child]:
                break
            out[root], out[child] = out[child], out[root]
            root = child
    for start in range(len(out) // 2 - 1, -1, -1):
        sift(start, len(out))
    for end in range(len(out) - 1, 0, -1):
        out[0], out[end] = out[end], out[0]
        sift(0, end)
    return out
'''),
    ("sort-count-full-key/1", "SORT-COUNT",
     "Full integer keys address occurrence counts, then increasing keys reconstruct output.",
     '''def sort_values(values):
    counts = [0] * 4096
    for value in values:
        counts[value] += 1
    result = []
    for key in range(4096):
        result.extend([key] * counts[key])
    return result
'''),
    ("sort-radix-lsd16/1", "SORT-RADIX",
     "Three stable base-16 digit passes reconstruct order for keys in 0..4095.",
     '''def sort_values(values):
    out = list(values)
    place = 1
    for step in range(3):
        buckets = [[] for bucket in range(16)]
        for value in out:
            buckets[(value // place) % 16].append(value)
        out = []
        for bucket in buckets:
            out.extend(bucket)
        place *= 16
    return out
'''),
)
