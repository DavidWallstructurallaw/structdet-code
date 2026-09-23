def shortest_distances(node_count, edges, start):
    neighbors = [[] for vertex in range(node_count)]
    for source, target in edges:
        neighbors[source].append(target)
    distances = [None] * node_count
    distances[start] = 0
    pending = [start]
    head = 0
    while head < len(pending):
        active = pending[head]
        head += 1
        for neighbor in neighbors[active]:
            if distances[neighbor] is None:
                distances[neighbor] = distances[active] + 1
                pending.append(neighbor)
    return distances
