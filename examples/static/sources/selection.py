def sort_values(values):
    remaining = list(values)
    result = []
    while remaining:
        selected = 0
        for index in range(1, len(remaining)):
            if remaining[index] < remaining[selected]:
                selected = index
        result.append(remaining.pop(selected))
    return result
