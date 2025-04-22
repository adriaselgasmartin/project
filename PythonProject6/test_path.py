if __name__ == '__main__':
    from graph import Graph, AddNode, AddSegment
    from path import Reachability, FindShortestPath, PlotPath
    from node import Node

    G = Graph()
    AddNode(G, Node('A', 0, 0))
    AddNode(G, Node('B', 5, 0))
    AddNode(G, Node('C', 5, 5))
    AddNode(G, Node('D', 0, 5))
    AddSegment(G, 'AB', 'A', 'B')
    AddSegment(G, 'BC', 'B', 'C')
    AddSegment(G, 'CD', 'C', 'D')
    AddSegment(G, 'DA', 'D', 'A')

    # Test Reachability
    r = Reachability(G, 'A')
    print(sorted([n.name for n in r]))  # expect ['B','C','D']

    # Test Shortest Path
    p = FindShortestPath(G, 'A', 'C')
    if p:
        print([n.name for n in p.nodes], p.cost)  # expect ['A','B','C']
        PlotPath(G, p)
    else:
        print('No path found')