# test_graph.py

import os
from graph import LoadGraphFromFile, Plot, PlotNode
from node import Node  # Assegura't que la classe Node està definida en node.py


def main():
    # Defineix el nom del fitxer sample
    sample_filename = "sample_graph.txt"

    # Dades sample per al graf:
    sample_data = """
# Exemple de fitxer per carregar un graf
NODE;A;0;0
NODE;B;3;4
NODE;C;6;8
NODE;D;2;7
SEGMENT;A;B
SEGMENT;B;C
SEGMENT;A;D
    """

    # Escriu les dades sample al fitxer
    with open(sample_filename, "w") as f:
        f.write(sample_data.strip())

    # Carrega el graf des del fitxer
    g = LoadGraphFromFile(sample_filename)

    # Mostra els nodes carregats
    print("Nodes carregats:")
    for node in g.nodes:
        print(f"{node.name}: ({node.x}, {node.y})")

    # Mostra els segments carregats
    print("\nSegments carregats:")
    for seg in g.segments:
        print(f"{seg.name}: {seg.origin.name} -> {seg.destination.name}, cost = {seg.cost:.2f}")

    # Visualitza el graf complet
    Plot(g)

    # Visualitza el subgraf per al node "A"
    PlotNode(g, "A")

    # Neteja el fitxer sample
    os.remove(sample_filename)


if __name__ == '__main__':
    main()
