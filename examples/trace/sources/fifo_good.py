def shortest_distances(node_count, edges, start):
    neighbors = [[] for vertex in range(node_count)]
    for source, target in edges:
        neighbors[source].append(target)
    distances = [None] * node_count
    distances[start] = 0
    frontier = [start]
    head = 0
    while head < len(frontier):
        current = frontier[head]
        head += 1
        for neighbor in neighbors[current]:
            if distances[neighbor] is None:
                distances[neighbor] = distances[current] + 1
                frontier.append(neighbor)
    return distances
