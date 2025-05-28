from graph import Graph
import math
import matplotlib.pyplot as plt

class Path:
    def __init__(self, nodes=None, cost=0.0):
        self.nodes = list(nodes) if nodes else []
        self.cost = cost

    def last_node(self):
        return self.nodes[-1] if self.nodes else None


def AddNodeToPath(path, node, graph):
    prev = path.last_node()
    added_cost = 0.0
    if prev:
        seg = next((s for s in graph.segments if s.origin == prev and s.destination == node), None)
        if seg is not None:
            added_cost = seg.cost
    return Path(path.nodes + [node], path.cost + added_cost)


def ContainsNode(path, node):
    return node in path.nodes


def CostToNode(path, node, graph):
    if node in path.nodes:
        idx = path.nodes.index(node)
        total = 0.0
        for i in range(idx):
            origin = path.nodes[i]
            dest = path.nodes[i+1]
            seg = next((s for s in graph.segments if s.origin == origin and s.destination == dest), None)
            if seg is not None:
                total += seg.cost
        return total
    return -1


def PlotPath(graph, path, ax):
    if not path:
        return

    for node in graph.nodes:
        ax.plot(node.x, node.y, 'ko', markersize=5)
        ax.text(node.x, node.y, f' {node.name}', fontsize=8)

    for seg in graph.segments:
        ax.plot([seg.origin.x, seg.destination.x], [seg.origin.y, seg.destination.y], 'gray')

    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        ax.plot([a.x, b.x], [a.y, b.y], 'r-', linewidth=2)

    for p in path:
        ax.plot(p.x, p.y, 'go', markersize=6)

    ax.set_title(f'Shortest Path: {path[0].name} -> {path[-1].name}')
    ax.grid(True)



def Reachability(graph, nodeName):
    start = next((n for n in graph.nodes if n.name == nodeName), None)
    if start is None:
        return []
    visited = {start}
    stack = [start]
    reachable = []
    while stack:
        current = stack.pop()
        neighbors = getattr(current, 'neighbors', [])
        for nb in neighbors:
            if nb not in visited:
                visited.add(nb)
                reachable.append(nb)
                stack.append(nb)
    return reachable


def FindShortestPath(graph, originName, destinationName):
    origin = next((n for n in graph.nodes if n.name == originName), None)
    dest = next((n for n in graph.nodes if n.name == destinationName), None)
    if origin is None or dest is None:
        return None
    open_paths = []
    start_path = Path([origin], cost=0.0)
    open_paths.append((heuristic(origin, dest), start_path))
    closed = set()
    while open_paths:
        open_paths.sort(key=lambda x: x[0])
        est, path = open_paths.pop(0)
        last = path.last_node()
        if last == dest:
            return path
        closed.add(last)
        for nb in getattr(last, 'neighbors', []):
            if nb in path.nodes:
                continue
            seg = next((s for s in graph.segments if s.origin == last and s.destination == nb), None)
            if seg is None:
                continue
            new_cost = path.cost + seg.cost
            new_path = Path(path.nodes + [nb], new_cost)
            if nb in closed:
                continue
            open_paths = [(e,p) for e,p in open_paths if not (p.last_node() == nb and p.cost > new_cost)]
            open_paths.append((new_cost + heuristic(nb, dest), new_path))
    return None


def heuristic(n1, n2):
    return math.hypot(n2.x - n1.x, n2.y - n1.y)