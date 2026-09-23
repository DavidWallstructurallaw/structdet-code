def shortest_distances(node_count, edges, start):
    distances = [None] * node_count
    distances[start] = 0
    for step in range(node_count - 1):
        changed = False
        for source, target in edges:
            if distances[source] is not None:
                candidate = distances[source] + 2
                if distances[target] is None or candidate < distances[target]:
                    distances[target] = candidate
                    changed = True
        if not changed:
            break
    return distances
