def shortest_distances(node_count, edges, start):
    neighbors = [[] for vertex in range(node_count)]
    for source, target in edges:
        neighbors[source].append(target)
    distances = [None] * node_count
    settled = [False] * node_count
    distances[start] = 0
    for step in range(node_count):
        best = None
        for vertex in range(node_count):
            if not settled[vertex] and distances[vertex] is not None:
                if best is None or distances[vertex] < distances[best]:
                    best = vertex
        if best is None:
            break
        settled[best] = True
        for neighbor in neighbors[best]:
            candidate = distances[best] + 1
            if distances[neighbor] is None or candidate < distances[neighbor]:
                distances[neighbor] = candidate
    return distances
