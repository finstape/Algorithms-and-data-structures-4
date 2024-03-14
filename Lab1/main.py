import threading
import networkx as nx
import customtkinter as ctk


# Function Traveling Salesman algorithm
class Traveling_Salesman:
    def __init__(self, graph_editor):
        self.graph_editor = graph_editor
        self.edges = graph_editor.edges
        self.graph = graph_editor.graph
        self.length = float("inf")
        self.traversal = {}

    # Algorithm
    def method_nearest_neighbor(self):
        for node in list(self.graph.nodes):
            visited = [False for _ in list(self.graph.nodes)]
            visited[node] = True
            current_node = node
            traversal = [current_node]

            while len(traversal) < len(list(self.graph.nodes)):
                nearest_neighbor = None
                min_distance = float("inf")

                for neighbor in list(self.graph.neighbors(current_node)):
                    if not visited[neighbor] and self.graph[current_node][neighbor]["weight"] < min_distance:
                        nearest_neighbor = neighbor
                        min_distance = self.graph[current_node][neighbor]["weight"]

                if nearest_neighbor is None:
                    break

                traversal.append(nearest_neighbor)
                visited[nearest_neighbor] = True
                current_node = nearest_neighbor

            if traversal[0] in list(self.graph.neighbors(traversal[-1])) and len(traversal) == len(list(self.graph.nodes)):
                traversal.append(traversal[0])
                total_length = sum(self.graph[traversal[i]][traversal[i + 1]]["weight"] for i in range(len(traversal) - 1))

                if total_length < self.length:
                    self.length = total_length
                    self.traversal = traversal

        result = f"Длина: {self.length}\n\n"
        for i in range(len(self.traversal) - 1):
            result += f'{self.traversal[i]} -> {self.traversal[i + 1]} ({self.graph[self.traversal[i]][self.traversal[i + 1]]["weight"]})\n'
        return result

    # Draw graph with his traversal
    def view(self, canvas):
        canvas.clear_graph()
        for i in range(len(self.traversal) - 1):
            start_vertex = self.traversal[i]
            end_vertex = self.traversal[i + 1]
            start_x, start_y = self.graph_editor.vertices[start_vertex]
            end_x, end_y = self.graph_editor.vertices[end_vertex]
            length = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5
            arrow_offset = 10
            sx = start_x + (end_x - start_x) * (arrow_offset / length)
            sy = start_y + (end_y - start_y) * (arrow_offset / length)
            ex = end_x - (end_x - start_x) * (arrow_offset / length)
            ey = end_y - (end_y - start_y) * (arrow_offset / length)
            canvas.create_line(sx, sy, ex, ey, arrow="last", width=2)

        for vertex, (x, y) in enumerate(self.graph_editor.vertices):
            canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue", tags="vertex")
            canvas.create_text(x, y, text=str(vertex), fill="white", tags="vertex_text")


# Class for editing a graph on a canvas
class GraphEditor(ctk.CTkCanvas):
    def __init__(self, master, interface, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_left_click)
        self.bind("<Button-3>", self.on_right_click)
        self.vertices = []
        self.edges = []
        self.selected_vertex = None
        self.graph = nx.DiGraph()
        self.interface = interface

    # Function to handle left-click events on the canvas
    def on_left_click(self, event):
        x, y = event.x, event.y
        self.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue", tags="vertex")
        self.create_text(x, y, text=str(len(self.graph)), fill="white", tags="vertex_text")
        self.vertices.append((x, y))
        self.graph.add_node(len(self.graph))

    # Function to handle right-click events on the canvas
    def on_right_click(self, event):
        x, y = event.x, event.y
        vertex = self.get_clicked_vertex(x, y)
        if vertex is not None:
            if self.selected_vertex is None:
                self.selected_vertex = vertex
            else:
                start_x, start_y = self.vertices[self.selected_vertex]
                end_x, end_y = self.vertices[vertex]
                length = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5
                if length == 0:
                    return
                arrow_offset = 10
                sx = start_x + (end_x - start_x) * (arrow_offset / length)
                sy = start_y + (end_y - start_y) * (arrow_offset / length)
                ex = end_x - (end_x - start_x) * (arrow_offset / length)
                ey = end_y - (end_y - start_y) * (arrow_offset / length)
                self.create_line(sx, sy, ex, ey, arrow=ctk.LAST, width=2)
                self.edges.append((self.selected_vertex, vertex))
                self.graph.add_edge(self.selected_vertex, vertex, weight=int(length))
                self.selected_vertex = None
                self.interface.populate_edge_table()

    # Function to get the index of a clicked vertex on the canvas
    def get_clicked_vertex(self, x, y):
        for i, (vx, vy) in enumerate(self.vertices):
            if (x - vx) ** 2 + (y - vy) ** 2 <= 100:
                return i
        return None

    # Function to clear the graph on the canvas
    def clear_graph(self):
        self.vertices = []
        self.edges = []
        self.graph.clear()
        self.delete("all")


# Class for the graphical user interface
class Interface(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Решение задачи о коммивояжере с помощью метода ближайшего соседа")
        self.geometry("1100x670")
        self.frame1 = None
        self.frame2 = None
        self.frame3 = None
        self.graph_view = None
        self.clear_button = None
        self.answer_label = None
        self.graph_editor = None
        self.output_text = None
        self.process_button = None
        self.edge_table = {}
        self.create_interface()

    # Function to create the graphical user interface
    def create_interface(self):
        self.frame1 = ctk.CTkFrame(self)
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.process_button = ctk.CTkButton(self.frame1, text="Рассчитать", command=self.threading_run)
        self.process_button.pack(side="top", padx=10, pady=10)

        self.clear_button = ctk.CTkButton(self.frame1, text="Очистить", command=self.clear_output)
        self.clear_button.pack(side="top", padx=10, pady=10)

        self.answer_label = ctk.CTkLabel(self.frame1, text="Ответ:")
        self.answer_label.pack(side="top", padx=10, pady=10, fill=ctk.BOTH)

        self.output_text = ctk.CTkTextbox(self.frame1, height=485, width=150)
        self.output_text.pack(side="top", padx=10, pady=10)
        self.output_text.bind("<KeyPress>", self.prevent_typing)

        self.frame2 = ctk.CTkFrame(self)
        self.frame2.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.graph_editor = GraphEditor(self.frame2, width=600, height=385, bg="grey", interface=self)
        self.graph_editor.pack(side="top", padx=10, pady=10)

        self.graph_view = GraphEditor(self.frame2, width=600, height=385, bg="grey", interface=self)
        self.graph_view.pack(side="top", padx=10, pady=10)
        self.graph_view.bind("<Button-1>", self.prevent_typing)

        self.frame3 = ctk.CTkFrame(self)
        self.frame3.grid(row=0, column=2, padx=10, pady=10, sticky="n")

        for col, header in enumerate(["Вершина 1", "Вершина 2", "Вес"]):
            label = ctk.CTkLabel(self.frame3, text=header)
            label.grid(row=0, column=col, padx=30, pady=5)

        self.populate_edge_table()

    # Function to prevent typing in the output textbox
    def prevent_typing(self, event):
        return "break"

    # Function to clear the output textbox and the graph on the canvas
    def clear_output(self):
        self.graph_editor.clear_graph()
        self.graph_view.clear_graph()
        self.output_text.delete("1.0", ctk.END)
        self.populate_edge_table()

    # Function to populate the edge table with data from the graph
    def populate_edge_table(self):
        if self.edge_table:
            for widgets in self.edge_table.values():
                for widget in widgets:
                    widget.destroy()
            self.edge_table = {}

        sorted_edges = sorted(self.graph_editor.graph.edges(data="weight"))

        for row, (vertex1, vertex2, weight) in enumerate(sorted_edges, start=1):
            entry_vertex1 = ctk.CTkEntry(self.frame3, width=100)
            entry_vertex1.insert(ctk.END, vertex1)
            entry_vertex1.grid(row=row, column=0, padx=10, pady=5)
            entry_vertex1.bind("<KeyPress>", self.prevent_typing)

            entry_vertex2 = ctk.CTkEntry(self.frame3, width=100)
            entry_vertex2.insert(ctk.END, vertex2)
            entry_vertex2.grid(row=row, column=1, padx=10, pady=5)
            entry_vertex2.bind("<KeyPress>", self.prevent_typing)

            entry_weight = ctk.CTkEntry(self.frame3, width=100)
            entry_weight.insert(ctk.END, weight)
            entry_weight.grid(row=row, column=2, padx=10, pady=5)
            entry_weight.bind("<FocusOut>",
                              lambda event, vertex1=vertex1, vertex2=vertex2, entry_weight=entry_weight: self.update_weight(vertex1, vertex2,
                                                                                                                            entry_weight))

            self.edge_table[row] = [entry_vertex1, entry_vertex2, entry_weight]

    # Function to update weights in graph
    def update_weight(self, vertex1, vertex2, entry_weight):
        new_weight = entry_weight.get()
        self.graph_editor.graph[vertex1][vertex2]["weight"] = int(new_weight)

    # Function to run a process in a separate thread
    def threading_run(self):
        t = threading.Thread(target=self.start_process)
        t.start()

    # Placeholder function for starting a process
    def start_process(self):
        self.output_text.delete("1.0", ctk.END)
        self.graph_view.clear_graph()

        salesman = Traveling_Salesman(self.graph_editor)
        salesman.method_nearest_neighbor()
        self.output_text.insert(ctk.END, salesman.method_nearest_neighbor())
        salesman.view(self.graph_view)


# Main block to run the GUI application
if __name__ == "__main__":
    gui = Interface()
    gui.mainloop()
