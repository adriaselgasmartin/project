from graph import *
from node import Node


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
    AddSegment(g, "Bg", "B", "g")
    AddSegment(g, "CD", "C", "D")
    AddSegment(g, "Cg", "C", "g")
    AddSegment(g, "Dg", "D", "g")
    AddSegment(g, "DH", "D", "H")
    AddSegment(g, "DI", "D", "I")
    AddSegment(g, "EF", "E", "F")
    AddSegment(g, "FL", "F", "L")
    AddSegment(g, "gB", "g", "B")
    AddSegment(g, "gF", "g", "F")
    AddSegment(g, "gH", "g", "H")
    AddSegment(g, "ID", "I", "D")
    AddSegment(g, "IJ", "I", "J")
    AddSegment(g, "JI", "J", "I")
    AddSegment(g, "KA", "K", "A")
    AddSegment(g, "KL", "K", "L")
    AddSegment(g, "LK", "L", "K")
    AddSegment(g, "LF", "L", "F")
    return g


print("Probando el grafo...")
g = CreateGraph_1()
Plot(g)
PlotNode(g, "C")
n = GetClosest(g, 15, 5)
print(n.name)  # La respuesta debe ser J
n = GetClosest(g, 8, 19)
print(n.name)  # La respuesta debe ser B