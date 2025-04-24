from graph import *
from node import Node
import os

g=None
def CreateGraph_1():
    g = Graph()
    AddNode(g, Node("A", 1, 20))
    AddNode(g, Node("B", 8, 17))
    AddNode(g, Node("C", 15, 20))
    AddNode(g, Node("D", 18, 15))
    AddNode(g, Node("E", 2, 4))
    AddNode(g, Node("F", 6, 5))
    AddNode(g, Node("G", 12, 12))
    AddNode(g, Node("H", 10, 3))
    AddNode(g, Node("I", 19, 1))
    AddNode(g, Node("J", 13, 5))
    AddNode(g, Node("K", 3, 15))
    AddNode(g, Node("L", 4, 10))
    AddSegment(g, "AB", "A", "B")
    AddSegment(g, "AE", "A", "E")
    AddSegment(g, "AK", "A", "K")
    AddSegment(g, "BA", "B", "A")
    AddSegment(g, "BC", "B", "C")
    AddSegment(g, "BF", "B", "F")
    AddSegment(g, "BK", "B", "K")
    AddSegment(g, "BG", "B", "G")
    AddSegment(g, "CD", "C", "D")
    AddSegment(g, "CG", "C", "G")
    AddSegment(g, "DG", "D", "G")
    AddSegment(g, "DH", "D", "H")
    AddSegment(g, "DI", "D", "I")
    AddSegment(g, "EF", "E", "F")
    AddSegment(g, "FL", "F", "L")
    AddSegment(g, "GB", "G", "B")
    AddSegment(g, "GF", "G", "F")
    AddSegment(g, "GH", "G", "H")
    AddSegment(g, "ID", "I", "D")
    AddSegment(g, "IJ", "I", "J")
    AddSegment(g, "JI", "J", "I")
    AddSegment(g, "KA", "K", "A")
    AddSegment(g, "KL", "K", "L")
    AddSegment(g, "LK", "L", "K")
    AddSegment(g, "LF", "L", "F")
    return g



def CreateGraph_2():
    G = Graph()
    AddNode(G, Node("P", 0, 0))
    AddNode(G, Node("Q", 10, 0))
    AddNode(G, Node("R", 5, 10))
    AddSegment(G, "PQ", "P", "Q")
    AddSegment(G, "QR", "Q", "R")
    AddSegment(G, "PR", "P", "R")
    return G

def test_file_loading():
    print("Testing file loading...")
    fileName = "data.txt"
    G_loaded = LoadGraphFromFile(fileName)
    if G_loaded:
        Plot(G_loaded)
    else:
        print("Error loading graph from file.")
    os.remove(fileName)


if __name__ == "__main__":
    print("Probando el grafo...")
    G = CreateGraph_1()
    Plot(G)
    PlotNode(G, "C")
    n = GetClosest(G, 15, 5)
    print(n.name)  # La respuesta debe ser J
    n = GetClosest(G, 8, 19)
    print(n.name)  # La respuesta debe ser B
    test_file_loading()
