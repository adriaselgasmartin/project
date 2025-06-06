from segment import Segment
from node import Node
import math
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

def AddNode (g,n):       #esta funcion revisa si n ya pertenece a la lista g
    if n in g.nodes:
        return False
    else:
        g.nodes.append(n)
        return True


def AddSegment(g, trajecte, nameOriginNode, nameDestinationNode):

    origin = None
    destination = None


    for node in g.nodes:
        if node.name == nameOriginNode:
            origin = node
        if node.name == nameDestinationNode:
            destination = node


    if origin is None or destination is None:
        return False


    seg_name = f"S_{nameOriginNode}_{nameDestinationNode}"


    new_segment = Segment(seg_name, origin, destination)
    g.segments.append(new_segment)

    if hasattr(origin, "neighbors"):
        origin.neighbors.append(destination)
    else:
        origin.neighbors = [destination]

    return True

def GetClosest(g, x, y):
    if not g.nodes:
        return None

    closest_node = None
    min_distance = float('inf')

    # Recorre tots els nodes i calcula la distància a la posició (x, y)
    for node in g.nodes:
        distance = math.sqrt((node.x - x) ** 2 + (node.y - y) ** 2)   #formula del modulo de un vector
        if distance < min_distance:
            min_distance = distance
            closest_node = node

    return closest_node

def Plot(graph, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    for node in graph.nodes:
        ax.plot(node.x, node.y, 'bo')
        ax.text(node.x, node.y, f" {node.name}", fontsize=8)
    for seg in graph.segments:
        ax.arrow(seg.origin.x, seg.origin.y, seg.destination.x - seg.origin.x, seg.destination.y - seg.origin.y,
                 length_includes_head=True, head_width=0.5, head_length=0.5, color='k')



def PlotNode(g, nameOrigin):

    origin = None
    for node in g.nodes:
        if node.name == nameOrigin:
            origin = node
            break

    if origin is None:
        return False

    # Si el node d'origen té atribut 'neighbours', els obtenim, sino es considera com a buida.
    neighbors = origin.neighbors if hasattr(origin, "neighbors") else []

    # Dibuixa tots els nodes amb colors segons la seva relació amb el node d'origen
    for node in g.nodes:
        if node == origin:
            # Node d'origen en blau
            plt.plot(node.x, node.y, 'bo')
            plt.text(node.x, node.y, f' {node.name}', color='blue', fontsize=9)
        elif node in neighbors:
            # Veïns en verd
            plt.plot(node.x, node.y, 'go')
            plt.text(node.x, node.y, f' {node.name}', color='green', fontsize=9)
        else:
            # Resta de nodes en gris (marcador petit gris amb fons gris clar)
            plt.plot(node.x, node.y, 'o', markersize=5, markerfacecolor='gray', markeredgecolor='gray')
            plt.text(node.x, node.y, f' {node.name}', color='gray', fontsize=9)

    # Dibuixa els segments que uneixen el node d'origen amb els seus veïns en vermell
    for seg in g.segments:
        if seg.origin == origin and seg.destination in neighbors:
            plt.plot([seg.origin.x, seg.destination.x],
                     [seg.origin.y, seg.destination.y], 'r-')
            mid_x = (seg.origin.x + seg.destination.x) / 2.0
            mid_y = (seg.origin.y + seg.destination.y) / 2.0
            plt.text(mid_x, mid_y, f'{seg.cost:.2f}', color='red', fontsize=9, ha='center', va='center')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Graph Plot for Node {origin.name}')
    plt.grid(True)
    plt.show()
    return True




def LoadGraphFromFile(data):
    g = Graph()
    with open(data, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(';')
            if parts[0].upper() == "NODE":
                if len(parts) != 5:
                    print(f"Error de format en línia de node: {line}")
                    continue
                name = parts[1]
                try:
                    x = float(parts[2])
                    y = float(parts[3])
                    type = str(parts[4])
                except ValueError:
                    print(f"Error de conversió en línia: {line}")
                    continue
                node = Node(name, x, y, type)
                AddNode(g, node)
            elif parts[0].upper() == "SEGMENT":
                if len(parts) != 4:
                    print(f"Error de format en línia de segment: {line}")
                    continue
                trajecte = parts[1]
                origin_name = parts[2]
                destination_name = parts[3]
                AddSegment(g, trajecte, origin_name, destination_name)
    return g

def RemoveNode(g, nodeName):
    node_to_remove = None
    for node in g.nodes:
        if node.name == nodeName:
            node_to_remove = node
            break
    if node_to_remove is None:
        return False
    g.nodes.remove(node_to_remove)
    g.segments = [seg for seg in g.segments if seg.origin != node_to_remove and seg.destination != node_to_remove]
    for node in g.nodes:
        if node_to_remove in node.neighbors:
            node.neighbors.remove(node_to_remove)
    return True

def SaveGraphToFile(g, filename):

    try:
        with open(filename, "w") as f:
            for node in g.nodes:
                f.write("N,{},{},{}\n".format(node.name, node.x, node.y))
            for seg in g.segments:
                f.write("S,{},{},{}\n".format(seg.name, seg.origin.name, seg.destination.name))
                return True
    except Exception as e:
        print("Error saving graph to file:", e)
        return False

def ReachableNodes(g, originNode):
    origin = None
    destination = None
    for node in g.nodes:
        if node.name == originNode:
            origin=node

    if origin is None:
        return False

    if hasattr(origin, "neighbors"):
        origin.neighbors.append(destination)
    else:
        origin.neighbors = [destination]



