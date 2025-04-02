import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from graph import Graph, LoadGraphFromFile, SaveGraphToFile, AddNode, AddSegment, RemoveNode, Plot, PlotNode
from test_graph import CreateGraph_1, CreateGraph_2
from node import Node

# Global variable to hold the current graph.
current_graph = None


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
    if name is None or name.strip() == "":
        return
    try:
        x = float(simpledialog.askstring("Input", "Enter x coordinate:"))
        y = float(simpledialog.askstring("Input", "Enter y coordinate:"))
    except Exception as e:
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
    seg_name = simpledialog.askstring("Input", "Enter segment name:")
    origin = simpledialog.askstring("Input", "Enter origin node name:")
    destination = simpledialog.askstring("Input", "Enter destination node name:")
    if seg_name and origin and destination:
        if AddSegment(current_graph, seg_name, origin, destination):
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


# A simple interactive design interface.
def design_graph():
    global current_graph
    # Create a new graph for design.
    current_graph = Graph()

    design_win = tk.Toplevel(root)
    design_win.title("Design Graph")

    canvas = tk.Canvas(design_win, width=500, height=500, bg="white")
    canvas.pack()

    # Store node positions (canvas coordinates) in a dictionary keyed by node name.
    node_positions = {}

    def canvas_click(event):
        # On click, ask for a node name and add it to the graph.
        name = simpledialog.askstring("Input", "Enter node name:", parent=design_win)
        if name:
            # For simplicity, we use the canvas coordinates as graph coordinates.
            x, y = event.x, event.y
            node = Node(name, x, y)
            if AddNode(current_graph, node):
                node_positions[name] = (x, y)
                # Draw the node on the canvas.
                canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
                canvas.create_text(x + 10, y, text=name, fill="blue")
            else:
                messagebox.showwarning("Warning", "Node already exists.", parent=design_win)

    def add_segment_design():
        # Ask for origin and destination from the user.
        origin = simpledialog.askstring("Input", "Enter origin node name:", parent=design_win)
        destination = simpledialog.askstring("Input", "Enter destination node name:", parent=design_win)
        seg_name = simpledialog.askstring("Input", "Enter segment name:", parent=design_win)
        if origin and destination and seg_name:
            if AddSegment(current_graph, seg_name, origin, destination):
                # Draw a line between the nodes on the canvas.
                if origin in node_positions and destination in node_positions:
                    x1, y1 = node_positions[origin]
                    x2, y2 = node_positions[destination]
                    canvas.create_line(x1, y1, x2, y2, fill="red")
                else:
                    messagebox.showwarning("Warning", "Node positions not found.", parent=design_win)
            else:
                messagebox.showerror("Error", "Failed to add segment. Check node names.", parent=design_win)

    btn_add_seg = tk.Button(design_win, text="Add Segment", command=add_segment_design)
    btn_add_seg.pack(side=tk.LEFT, padx=5, pady=5)

    btn_save = tk.Button(design_win, text="Save Graph", command=lambda: save_graph())
    btn_save.pack(side=tk.LEFT, padx=5, pady=5)

    canvas.bind("<Button-1>", canvas_click)


# Main GUI window.
root = tk.Tk()
root.title("Graph Editor")

btn_example = tk.Button(root, text="Show Example Graph", width=30, command=show_example_graph)
btn_example.pack(padx=5, pady=5)

btn_invented = tk.Button(root, text="Show Invented Graph", width=30, command=show_invented_graph)
btn_invented.pack(padx=5, pady=5)

btn_load = tk.Button(root, text="Load Graph from File", width=30, command=load_graph_from_file)
btn_load.pack(padx=5, pady=5)

btn_show_neighbors = tk.Button(root, text="Show Neighbors of a Node", width=30, command=show_node_neighbors)
btn_show_neighbors.pack(padx=5, pady=5)

btn_add_node = tk.Button(root, text="Add Node", width=30, command=add_node)
btn_add_node.pack(padx=5, pady=5)

btn_add_seg = tk.Button(root, text="Add Segment", width=30, command=add_segment)
btn_add_seg.pack(padx=5, pady=5)

btn_delete_node = tk.Button(root, text="Delete Node", width=30, command=delete_node)
btn_delete_node.pack(padx=5, pady=5)

btn_design = tk.Button(root, text="Design Graph Interactively", width=30, command=design_graph)
btn_design.pack(padx=5, pady=5)

btn_save = tk.Button(root, text="Save Graph to File", width=30, command=save_graph)
btn_save.pack(padx=5, pady=5)

btn_quit = tk.Button(root, text="Quit", width=30, command=root.quit)
btn_quit.pack(padx=5, pady=5)

root.mainloop()
