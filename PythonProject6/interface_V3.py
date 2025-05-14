import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from graph import Graph, LoadGraphFromFile, SaveGraphToFile, AddNode, AddSegment, RemoveNode, Plot, PlotNode
from test_graph import CreateGraph_1, CreateGraph_2
from node import Node
from path import Reachability, FindShortestPath, PlotPath
from airSpace import AirSpace
from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport
import matplotlib.pyplot as plt
current_graph = None

def load_catalunya_data():
    air = AirSpace()
    try:
        air.load_nav_points("Nav.txt")
        air.load_nav_segments("Seg.txt")
        air.load_airports("Aer.txt")
        messagebox.showinfo("Datos cargados", "Datos de Catalunya cargados correctamente.")
        return air
    except Exception as e:
        messagebox.showerror("Error al cargar", str(e))
        return None

def plot_airspace(airspace: AirSpace):
    fig, ax = plt.subplots()
    id_to_point = {np.number: np for np in airspace.nav_points}


    for np in airspace.nav_points:
        ax.plot(np.longitude, np.latitude, 'ko')
        ax.text(np.longitude, np.latitude, np.name, fontsize=6)


    for seg in airspace.nav_segments:
        if seg.origin_number in id_to_point and seg.destination_number in id_to_point:
            origin = id_to_point[seg.origin_number]
            dest = id_to_point[seg.destination_number]
            dx = dest.longitude - origin.longitude
            dy = dest.latitude - origin.latitude
            plt.arrow(origin.longitude, origin.latitude, dx, dy,length_includes_head=True, head_width=0.07, head_length=0.07, color='c')

    ax.set_title("Airspace - Catalunya")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True)
    plt.show()
airspace = None  # Variable global

def cargar_y_mostrar():
    global airspace
    global current_graph
    airspace = load_catalunya_data()
    current_graph = airspace_to_graph(airspace)
    if airspace:
        plot_airspace(airspace)


def airspace_to_graph(airspace: AirSpace) -> Graph:
    g = Graph()
    id_to_node = {}

    for navpoint in airspace.nav_points:
        node = Node(navpoint.name, navpoint.longitude, navpoint.latitude)
        AddNode(g, node)
        id_to_node[navpoint.number] = node

    for seg in airspace.nav_segments:
        if seg.origin_number in id_to_node and seg.destination_number in id_to_node:
            AddSegment(g, id_to_node[seg.origin_number].name, id_to_node[seg.destination_number].name)

    return g

def show_example_graph():
    global current_graph
    current_graph = CreateGraph_1()
    Plot(current_graph)


def show_invented_graph():
    global current_graph
    current_graph = CreateGraph_2()
    Plot(current_graph)


def load_graph_from_file():
    global current_graph
    file_path = filedialog.askopenfilename(title="Select graph file", filetypes=[("Text Files", "*.txt")])
    if file_path:
        g = LoadGraphFromFile(file_path)
        if g is not None:
            current_graph = g
            Plot(current_graph)
        else:
            messagebox.showerror("Error", "Failed to load graph.")


def show_node_neighbors():
    global current_graph
    global airspace
    if current_graph is None:
        messagebox.showwarning("Warning", "No graph loaded.")
        return
    node_name = simpledialog.askstring("Input", "Enter node name:")
    if node_name:
        if not PlotNode(current_graph, node_name):
            messagebox.showerror("Error", "Node not found.")


def add_node():
    global current_graph
    if current_graph is None:
        messagebox.showwarning("Warning", "No graph loaded.")
        return
    name = simpledialog.askstring("Input", "Enter node name:")
    if not name:
        return
    try:
        x = float(simpledialog.askstring("Input", "Enter x coordinate:"))
        y = float(simpledialog.askstring("Input", "Enter y coordinate:"))
    except Exception:
        messagebox.showerror("Error", "Invalid coordinates.")
        return
    node = Node(name, x, y)
    if AddNode(current_graph, node):
        messagebox.showinfo("Success", "Node added.")
    else:
        messagebox.showwarning("Warning", "Node already exists.")
    Plot(current_graph)


def add_segment():
    global current_graph
    if current_graph is None:
        messagebox.showwarning("Warning", "No graph loaded.")
        return
    origin = simpledialog.askstring("Input", "Enter origin node name:")
    destination = simpledialog.askstring("Input", "Enter destination node name:")
    if origin and destination:
        if AddSegment(current_graph, origin, origin, destination):
            messagebox.showinfo("Success", "Segment added.")
        else:
            messagebox.showerror("Error", "Failed to add segment. Check node names.")
        Plot(current_graph)


def delete_node():
    global current_graph
    if current_graph is None:
        messagebox.showwarning("Warning", "No graph loaded.")
        return
    node_name = simpledialog.askstring("Input", "Enter node name to delete:")
    if node_name:
        if RemoveNode(current_graph, node_name):
            messagebox.showinfo("Success", "Node and related segments deleted.")
        else:
            messagebox.showerror("Error", "Node not found.")
        Plot(current_graph)


def save_graph():
    global current_graph
    if current_graph is None:
        messagebox.showwarning("Warning", "No graph loaded.")
        return
    file_path = filedialog.asksaveasfilename(title="Save graph", defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        if SaveGraphToFile(current_graph, file_path):
            messagebox.showinfo("Success", "Graph saved.")
        else:
            messagebox.showerror("Error", "Failed to save graph.")


def design_graph():
    global current_graph
    current_graph = Graph()

    design_win = tk.Toplevel(root)
    design_win.title("Design Graph")

    canvas = tk.Canvas(design_win, width=500, height=500, bg="white")
    canvas.pack()

    node_positions = {}

    def canvas_click(event):
        name = simpledialog.askstring("Input", "Enter node name:", parent=design_win)
        if name:
            x, y = event.x, event.y
            node = Node(name, x, y)
            if AddNode(current_graph, node):
                node_positions[name] = (x, y)
                canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")
                canvas.create_text(x+10, y, text=name, fill="blue")
            else:
                messagebox.showwarning("Warning", "Node already exists.", parent=design_win)

    def add_segment_design():
        origin = simpledialog.askstring("Input", "Enter origin node name:", parent=design_win)
        destination = simpledialog.askstring("Input", "Enter destination node name:", parent=design_win)
        if origin and destination:
            if AddSegment(current_graph, origin, origin, destination):
                if origin in node_positions and destination in node_positions:
                    x1, y1 = node_positions[origin]
                    x2, y2 = node_positions[destination]
                    canvas.create_line(x1, y1, x2, y2, fill="red")
                else:
                    messagebox.showwarning("Warning", "Node positions not found.", parent=design_win)
            else:
                messagebox.showerror("Error", "Failed to add segment.", parent=design_win)

    btn_add_seg = tk.Button(design_win, text="Add Segment", command=add_segment_design)
    btn_add_seg.pack(side=tk.LEFT, padx=5, pady=5)

    btn_save = tk.Button(design_win, text="Save Graph", command=save_graph)
    btn_save.pack(side=tk.LEFT, padx=5, pady=5)

    canvas.bind("<Button-1>", canvas_click)


def show_reachability():
    global current_graph
    if current_graph is None:
        messagebox.showwarning("Warning", "No graph loaded.")
        return
    name = simpledialog.askstring("Input", "Enter origin node for reachability:")
    if not name:
        return
    reachable = Reachability(current_graph, name)
    if not reachable:
        messagebox.showinfo("Reachability", f"No nodes reachable from {name}.")
        return

    import matplotlib.pyplot as plt
    for node in current_graph.nodes:
        if node.name == name:
            plt.plot(node.x, node.y, 'bo')
        elif node in reachable:
            plt.plot(node.x, node.y, 'go')
        else:
            plt.plot(node.x, node.y, 'o', markersize=4, markerfacecolor='none', markeredgecolor='none')
        plt.text(node.x, node.y, f' {node.name}', color='black')
    for seg in current_graph.segments:
        if seg.origin.name == name and seg.destination in reachable or (seg.origin in reachable and seg.destination in reachable):
            plt.plot([seg.origin.x, seg.destination.x], [seg.origin.y, seg.destination.y], 'r-')
    plt.title(f'Reachable from {name}')
    plt.grid(True)
    plt.show()


def show_shortest_path():
    global current_graph
    if current_graph is None:
        messagebox.showwarning("Warning", "No graph loaded.")
        return
    origin = simpledialog.askstring("Input", "Enter origin node for shortest path:")
    destination = simpledialog.askstring("Input", "Enter destination node for shortest path:")
    if not origin or not destination:
        return
    path = FindShortestPath(current_graph, origin, destination)
    if not path:
        messagebox.showinfo("Shortest Path", f"No path from {origin} to {destination}.")
    else:
        PlotPath(current_graph, path)

# Main GUI window
root = tk.Tk()
root.title("Graph Editor v3")

btn_example = tk.Button(root, text="Show Example Graph", width=30, command=show_example_graph)
btn_example.pack(padx=5, pady=5)

btn_invented = tk.Button(root, text="Show Invented Graph", width=30, command=show_invented_graph)
btn_invented.pack(padx=5, pady=5)

btn_load = tk.Button(root, text="Load Graph from File", width=30, command=load_graph_from_file)
btn_load.pack(padx=5, pady=5)

btn_neighbors = tk.Button(root, text="Show Neighbors of a Node", width=30, command=show_node_neighbors)
btn_neighbors.pack(padx=5, pady=5)

btn_reach = tk.Button(root, text="Show Reachability", width=30, command=show_reachability)
btn_reach.pack(padx=5, pady=5)

btn_shortest = tk.Button(root, text="Show Shortest Path", width=30, command=show_shortest_path)
btn_shortest.pack(padx=5, pady=5)

btn_add_node = tk.Button(root, text="Add Node", width=30, command=add_node)
btn_add_node.pack(padx=5, pady=5)

btn_add_seg = tk.Button(root, text="Add Segment", width=30, command=add_segment)
btn_add_seg.pack(padx=5, pady=5)

btn_delete = tk.Button(root, text="Delete Node", width=30, command=delete_node)
btn_delete.pack(padx=5, pady=5)

btn_design = tk.Button(root, text="Design Graph Interactively", width=30, command=design_graph)
btn_design.pack(padx=5, pady=5)

btn_save = tk.Button(root, text="Save Graph to File", width=30, command=save_graph)
btn_save.pack(padx=5, pady=5)

btn_cargar = tk.Button(root, text="Load Airspace data", width=30, command=cargar_y_mostrar)
btn_cargar.pack(pady=5)

btn_quit = tk.Button(root, text="Quit", width=30, command=root.quit)
btn_quit.pack(padx=5, pady=5)





root.mainloop()
