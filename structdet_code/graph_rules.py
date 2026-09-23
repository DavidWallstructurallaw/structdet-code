"""Independently written, project-owned graph reference programs, used as data."""

SCOPE = "unit-graph-whole-module-alpha-ast/1"

FIFO = '''def shortest_distances(node_count, edges, start):
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
'''

RULES = (
    ("dist-fifo-first-discovery/1", "DIST-FIFO",
     "FIFO first discovery propagates one edge at a time without re-enqueueing vertices.", FIFO),
    ("dist-fifo-step-defect/1", "DIST-FIFO",
     "FIFO first discovery is recognizable despite the incorrect two-hop increment per edge.",
     FIFO.replace("distances[current] + 1", "distances[current] + 2")),
    ("dist-minimum-settlement/1", "DIST-SETTLE",
     "Each step scans for the smallest finite unsettled distance, finalizes it, then updates outgoing neighbors.",
     '''def shortest_distances(node_count, edges, start):
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
'''),
    ("dist-complete-edge-passes/1", "DIST-RELAX",
     "Complete edge passes repeatedly improve labels, stopping after node_count-1 rounds or a fixed point.",
     '''def shortest_distances(node_count, edges, start):
    distances = [None] * node_count
    distances[start] = 0
    for step in range(node_count - 1):
        changed = False
        for source, target in edges:
            if distances[source] is not None:
                candidate = distances[source] + 1
                if distances[target] is None or candidate < distances[target]:
                    distances[target] = candidate
                    changed = True
        if not changed:
            break
    return distances
'''),
)
