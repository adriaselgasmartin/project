import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from graph import *
from test_graph import CreateGraph_1, CreateGraph_2
from node import Node
from path import Reachability, FindShortestPath, PlotPath
from airSpace import AirSpace
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
current_graph = None
design_frame = None  # Esto va fuera de cualquier función


def show_example_graph():
    global current_graph
    current_graph = CreateGraph_1()
    ax.clear()
    Plot(current_graph, ax)
    ax.grid(True)
    canvas.draw()


def show_invented_graph():
    global current_graph
    current_graph = CreateGraph_2()
    ax.clear()
    Plot(current_graph, ax)
    ax.grid(True)
    canvas.draw()


def load_graph_from_file():
    global current_graph
    file_path = filedialog.askopenfilename(title="Select graph file", filetypes=[("Text Files", "*.txt")])
    if file_path:
        g = LoadGraphFromFile(file_path)
        if g is not None:
            current_graph = g
            ax.clear()
            Plot(current_graph, ax)
            ax.grid(True)
            canvas.draw()
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
    ax.clear()
    Plot(current_graph, ax)
    ax.grid(True)
    canvas.draw()


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
        ax.clear()
        Plot(current_graph, ax)
        ax.grid(True)
        canvas.draw()


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
        ax.clear()
        Plot(current_graph, ax)
        ax.grid(True)
        canvas.draw()


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
    global current_graph, design_frame

    # Cerrar diseño anterior si existe
    if design_frame and design_frame.winfo_exists():
        design_frame.destroy()

    current_graph = Graph()

    design_frame = tk.Frame(root, name="design_frame", bd=2, relief=tk.RIDGE)
    design_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    title_label = tk.Label(design_frame, text="Design Graph", font=("Arial", 14, "bold"))
    title_label.pack(pady=5)

    canvas = tk.Canvas(design_frame, width=500, height=500, bg="white")
    canvas.pack()

    node_positions = {}
    selected_node = None

    def on_click(event):
        nonlocal selected_node
        x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        for name, (nx, ny) in node_positions.items():
            if abs(nx - x) < 10 and abs(ny - y) < 10:
                selected_node = name
                return
        name = simpledialog.askstring("Node Name", "Enter name:", parent=root)
        if name:
            node = Node(name, x, y)
            if AddNode(current_graph, node):
                node_positions[name] = (x, y)
                redraw()

    def on_drag(event):
        nonlocal selected_node
        if selected_node:
            x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
            node_positions[selected_node] = (x, y)
            for node in current_graph.nodes:
                if node.name == selected_node:
                    node.x = x
                    node.y = y
            redraw()

    def on_release(event):
        nonlocal selected_node
        selected_node = None

    def redraw():
        canvas.delete("all")
        for seg in current_graph.segments:
            if seg.origin.name in node_positions and seg.destination.name in node_positions:
                x1, y1 = node_positions[seg.origin.name]
                x2, y2 = node_positions[seg.destination.name]
                canvas.create_line(x1, y1, x2, y2, fill="red")
        for name, (x, y) in node_positions.items():
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
            canvas.create_text(x + 10, y, text=name, fill="blue")

    def add_segment_design():
        origin = simpledialog.askstring("Input", "Enter origin node name:", parent=root)
        destination = simpledialog.askstring("Input", "Enter destination node name:", parent=root)
        if origin and destination:
            if AddSegment(current_graph, (origin, destination), origin, destination):
                redraw()

    def save():
        save_graph()
        messagebox.showinfo("Saved", "Graph saved successfully.", parent=root)

    def close_design():
        design_frame.destroy()
        # Redibujar el gráfico principal si existe
        if current_graph and current_graph.nodes:
            ax.clear()
            Plot(current_graph, ax)
            ax.grid(True)
            canvas.draw()

    btn_frame = tk.Frame(design_frame)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Add Segment", command=add_segment_design).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Save Graph", command=save).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Close Design", command=close_design).pack(side=tk.LEFT, padx=5)

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)


def show_reachability():
    global current_graph
    reach = []
    ax.clear()

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

    for node in current_graph.nodes:
        ax.plot(node.x, node.y, 'o', markersize=5, markerfacecolor='lightgray', markeredgecolor='gray')
        ax.text(node.x, node.y, f' {node.name}', color='gray', fontsize=9)

    for node in current_graph.nodes:
        if node.name == name:
            ax.plot(node.x, node.y, 'bo')
        elif node in reachable:
            reach.append(node)
            ax.plot(node.x, node.y, 'go')

    for seg in current_graph.segments:
        if (seg.origin.name == name and seg.destination in reachable) or (seg.origin in reachable and seg.destination in reachable):
            ax.plot([seg.origin.x, seg.destination.x], [seg.origin.y, seg.destination.y], 'r-')

    ax.grid(True)
    canvas.draw()

def show_shortest_path():
    global current_graph
    ax.clear()
    ax.grid(True)
    canvas.draw()

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
        PlotPath(current_graph, path.nodes, ax=ax)  # Asegúrate que PlotPath acepte ax como parámetro
        canvas.draw()


def load_catalunya_data():
    air = AirSpace()
    global zona
    zona= "Catalunya"
    try:
        air.load_nav_points("Nav.txt")
        air.load_nav_segments("Seg.txt")
        air.load_airports("Aer.txt")
        messagebox.showinfo("Datos cargados", "Datos de Catalunya cargados correctamente.")
        return air
    except Exception as e:
        messagebox.showerror("Error al cargar", str(e))

        return None

def load_espanya_data():
    air = AirSpace()
    global zona
    zona= "España"
    try:
        air.load_nav_points("ESP_NAV.txt")
        air.load_nav_segments("ESP_SEG.txt")
        air.load_airports("ESP_AER.txt")
        messagebox.showinfo("Datos cargados", "Datos de España cargados correctamente.")
        return air
    except Exception as e:
        messagebox.showerror("Error al cargar", str(e))

        return None

def load_europa_data():
    air = AirSpace()
    global zona
    zona ="Europa"
    try:
        air.load_nav_points("EU_NAV.txt")
        air.load_nav_segments("EU_SEG.txt")
        air.load_airports("EU_AER.txt")
        messagebox.showinfo("Datos cargados", "Datos de Europa cargados correctamente.")
        return air
    except Exception as e:
        messagebox.showerror("Error al cargar", str(e))
        return None

def plot_airspace(airspace: AirSpace):
    ax.clear()  # Limpia antes de dibujar, no después
    id_to_point = {np.number: np for np in airspace.nav_points}

    for np in airspace.nav_points:
        ax.plot(np.longitude, np.latitude, 'co')
        ax.text(np.longitude, np.latitude, np.name, fontsize=5)

    for seg in airspace.nav_segments:
        if seg.origin_number in id_to_point and seg.destination_number in id_to_point:
            origin = id_to_point[seg.origin_number]
            dest = id_to_point[seg.destination_number]
            dx = dest.longitude - origin.longitude
            dy = dest.latitude - origin.latitude
            ax.arrow(origin.longitude, origin.latitude, dx, dy,
                     length_includes_head=True, head_width=0.07, head_length=0.07, color='c')

    fig.suptitle(f"Airspace - {zona}", fontsize=16)
    ax.set_title(f"{airspace}", fontsize=12)
    ax.grid(True)
    canvas.draw()


def cargar_y_mostrarcat():
    global airspace
    global current_graph
    airspace = load_catalunya_data()
    current_graph = airspace_to_graph(airspace)
    if airspace:
        plot_airspace(airspace)

def cargar_y_mostraresp():
    global airspace
    global current_graph
    airspace = load_espanya_data()
    current_graph = airspace_to_graph(airspace)
    if airspace:
        plot_airspace(airspace)

def cargar_y_mostrareu():
    global airspace
    global current_graph
    airspace = load_europa_data()
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
            AddSegment(g,(id_to_node[seg.origin_number].name,id_to_node[seg.destination_number]), id_to_node[seg.origin_number].name, id_to_node[seg.destination_number].name)

    return g

def export_to_kml():
    global airspace
    if not airspace:
        messagebox.showwarning("Advertencia", "No hay datos de espacio aéreo cargados.")
        return

    kml_path = filedialog.asksaveasfilename(
        defaultextension=".kml",
        filetypes=[("Google Earth KML", "*.kml")],
        title="Guardar como archivo KML"
    )

    if not kml_path:
        return

    try:
        with open(kml_path, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            f.write('<Document>\n')
            f.write(f'  <name>Airspace - {zona}</name>\n')

            # Puntos de navegación
            for np in airspace.nav_points:
                f.write('  <Placemark>\n')
                f.write(f'    <name>{np.name}</name>\n')
                f.write('    <Point>\n')
                f.write(f'      <coordinates>{np.longitude},{np.latitude},0</coordinates>\n')
                f.write('    </Point>\n')
                f.write('  </Placemark>\n')

            # Segmentos de navegación
            id_to_point = {p.number: p for p in airspace.nav_points}
            for seg in airspace.nav_segments:
                if seg.origin_number in id_to_point and seg.destination_number in id_to_point:
                    origin = id_to_point[seg.origin_number]
                    dest = id_to_point[seg.destination_number]
                    f.write('  <Placemark>\n')
                    f.write('    <LineString>\n')
                    f.write('      <coordinates>\n')
                    f.write(f'        {origin.longitude},{origin.latitude},0 {dest.longitude},{dest.latitude},0\n')
                    f.write('      </coordinates>\n')
                    f.write('    </LineString>\n')
                    f.write('  </Placemark>\n')

            f.write('</Document>\n')
            f.write('</kml>\n')

        messagebox.showinfo("Éxito", f"KML exportado a {kml_path}")
    except Exception as e:
        messagebox.showerror("Error al exportar", str(e))

root = tk.Tk()
root.title("Graph Editor v3")
root.geometry("1200x700")

# Layout frames
left_frame = tk.Frame(root, width=300)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Matplotlib figure embedded in Tkinter
fig = Figure(figsize=(6, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Botons al panell esquerre
botons = [
    ("Show Example Graph", show_example_graph),
    ("Show Invented Graph", show_invented_graph),
    ("Load Graph from File", load_graph_from_file),
    ("Save Graph to File", save_graph),
    ("Add Node", add_node),
    ("Add Segment", add_segment),
    ("Delete Node", delete_node),
    ("Design Graph Interactively", design_graph),
    ("Show Neighbors of a Node", show_node_neighbors),
    ("Show Reachability", show_reachability),
    ("Show Shortest Path", show_shortest_path),
    ("Load CAT Airspace data", cargar_y_mostrarcat),
    ("Load ESP Airspace data", cargar_y_mostraresp),
    ("Load EU Airspace data", cargar_y_mostrareu),
    ("Exportar a Google Earth (KML)", export_to_kml),
    ("Quit", root.quit)
]

for text, cmd in botons:
    b = tk.Button(left_frame, text=text, width=30, command=cmd)
    b.pack(padx=5, pady=3, anchor='n')

root.mainloop()
