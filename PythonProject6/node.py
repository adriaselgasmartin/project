import math

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.neighbors = []

def AddNeighbour (n1, n2):

    if n2 in n1.neighbors:
        return False
    else:
        n1.neighbors.append(n2)
        return True

def Distance (n1, n2):

    return math.sqrt((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2)