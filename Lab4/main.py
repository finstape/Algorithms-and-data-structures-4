import threading
import networkx as nx
import customtkinter as ctk


# Function tree algorithm
class Minimum_Tree_Traversal:
    def __init__(self, graph_editor):
        self.graph_editor = graph_editor
        self.edges = graph_editor.edges
        self.graph = graph_editor.graph
        self.traversal = []
        self.used = []
        self.result = ""

    # DFS algo finding cycle
    def dfs_cycle(self, v, p=-1):
        self.used[v] = True
        for u in self.graph.neighbors(v):
            if not self.used[u]:
                self.dfs_cycle(u, v)
            elif u != p:
                self.result = "Граф содержит цикл -- не дерево!"
                break

    # DFS algo increment quantity
    def dfs_increment(self, v):
        self.used[v] = True
        for u in self.graph.neighbors(v):
            if not self.used[u]:
                self.graph.nodes[v]["quantity"] += self.dfs_increment(u)

        return self.graph.nodes[v]["quantity"] + 1 if self.graph.nodes[v]["label"] == "Treasure" else self.graph.nodes[v]["quantity"]

    # DFS algo
    def dfs(self, v):
        self.used[v] = True

        if self.graph.nodes[v]["quantity"] == 0:
            if self.graph.nodes[v]["label"] == "Treasure":
                self.traversal.append(v)
            return

        self.traversal.append(v)
        for u in self.graph.neighbors(v):
            if not self.used[u]:
                self.dfs(u)
                if self.traversal[-1] != v:
                    self.traversal.append(v)

    # Algorithm
    def algorithm(self):
        self.used = [False for _ in range(self.graph.number_of_nodes())]
        self.dfs_cycle(0)

        if self.result != "":
            return self.result

        if sum(list([1 if x else 0 for x in self.used])) != self.graph.number_of_nodes():
            return "Граф несвязный -- не дерево!"

        self.used = [False for _ in range(self.graph.number_of_nodes())]
        self.graph.nodes[0]["quantity"] += self.dfs_increment(0)

        self.used = [False for _ in range(self.graph.number_of_nodes())]
        self.dfs(0)

        result = f"Длина: {len(self.traversal) - 1}\n\n"
        for i in range(len(self.traversal) - 1):
            result += f'{self.traversal[i]} -> {self.traversal[i + 1]}\n'
        return result


# Class for editing a graph on a canvas
class GraphEditor(ctk.CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_left_click)
        self.bind("<Button-3>", self.on_right_click)
        self.bind("<Button-2>", self.on_middle_click)
        self.vertices = []
        self.edges = []
        self.selected_vertex = None
        self.graph = nx.DiGraph()

    # Function to handle left-click events on the canvas
    def on_left_click(self, event):
        x, y = event.x, event.y
        self.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue", tags="vertex")
        self.create_text(x, y, text=str(len(self.graph)), fill="white", tags="vertex_text")
        self.vertices.append((x, y))
        self.graph.add_node(len(self.graph), label="Room", quantity=0)

    # Function to handle middle-click events on the canvas (mouse wheel click)
    def on_middle_click(self, event):
        x, y = event.x, event.y
        vertex = self.get_clicked_vertex(x, y)
        if vertex is not None:
            vx, vy = self.vertices[vertex]
            self.create_oval(vx - 10, vy - 10, vx + 10, vy + 10, fill="gold", tags="vertex")
            self.create_text(vx, vy, text=f"{vertex}", fill="black", tags="vertex_text")
            nx.set_node_attributes(self.graph, {vertex: {"label": "Treasure", "quantity": 0}})

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
                self.create_line(sx, sy, ex, ey, width=2)
                self.edges.append((self.selected_vertex, vertex))
                self.edges.append((vertex, self.selected_vertex))
                self.graph.add_edge(self.selected_vertex, vertex)
                self.graph.add_edge(vertex, self.selected_vertex)
                self.selected_vertex = None

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
        self.title("Минимальное время, чтобы собрать все яблоки на дереве")
        self.geometry("720x520")
        self.frame1 = None
        self.frame2 = None
        self.clear_button = None
        self.answer_label = None
        self.graph_editor = None
        self.output_text = None
        self.process_button = None
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
        self.answer_label.pack(side="top", padx=10, fill=ctk.BOTH)

        self.output_text = ctk.CTkTextbox(self.frame1, height=370, width=150)
        self.output_text.pack(side="top", padx=10)
        self.output_text.bind("<KeyPress>", self.prevent_typing)

        self.frame2 = ctk.CTkFrame(self)
        self.frame2.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.graph_editor = GraphEditor(self.frame2, width=600, height=600, bg="grey")
        self.graph_editor.pack(side="top", padx=10, pady=10)

    # Function to prevent typing in the output textbox
    def prevent_typing(self, event):
        return "break"

    # Function to clear the output textbox and the graph on the canvas
    def clear_output(self):
        self.graph_editor.clear_graph()
        self.output_text.delete("1.0", ctk.END)

    # Function to run a process in a separate thread
    def threading_run(self):
        t = threading.Thread(target=self.run_process)
        t.start()

    # Function to run a process in the main thread
    def run_process(self):
        self.output_text.delete("1.0", ctk.END)
        self.after(10, self.start_process)

    # Function to start a process
    def start_process(self):
        traversal = Minimum_Tree_Traversal(self.graph_editor)
        result = traversal.algorithm()
        self.output_text.insert(ctk.END, result)


# Main block to run the GUI application
if __name__ == "__main__":
    gui = Interface()
    gui.mainloop()
