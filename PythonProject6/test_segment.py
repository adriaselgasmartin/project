from segment import Segment
from node import Node

node1= Node("node1", 0, 0)
node2= Node("node2", 3, 4)
node3= Node("node1", 1, 1)

seg1= Segment("seg1", node1, node2)
seg2= Segment("seg2", node2, node3)

print("Segment 1:")
print("Name:", seg1.name)
print("Origin:", seg1.origin.__dict__)
print("Destination:", seg1.destination.__dict__)
print("Cost:", seg1.cost)

print("\nSegment 2:")
print("Name:", seg2.name)
print("Origin:", seg2.origin.__dict__)
print("Destination:", seg2.destination.__dict__)
print("Cost:", seg2.cost)