def sort_values(values):
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
