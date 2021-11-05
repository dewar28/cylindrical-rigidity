class Graph:
    """Entries should be dictionaries. Keys should be numbers 1,...,n and values should be subsets of 1,...,n.
    Graphs will be simple graphs.
    Dictionary will be made symmetric."""

    @staticmethod
    def make_dict_symmetric(graph_dict):
        """For making graphs simple"""
        for vertex in graph_dict:
            for neighbour in graph_dict[vertex]:
                graph_dict[neighbour].add(vertex)
            if vertex in graph_dict[vertex]:
                graph_dict[vertex].remove(vertex)

    def __init__(self, graph_dict):
        if graph_dict is None:
            graph_dict = {}
        Graph.make_dict_symmetric(graph_dict)
        self.adjacency_list = graph_dict

    def vertex_set(self):
        """Obtains vertices as a set."""
        vertices = set()
        for i in self.adjacency_list:
            vertices.add(i)
        return vertices

    def edge_list(self):
        """Obtains of list edges, each represented as a set."""
        edges = []
        for vertex in self.adjacency_list:
            for neighbour in self.adjacency_list[vertex]:
                if vertex < neighbour:
                    edges.append({vertex, neighbour})
        return edges

    def number_of_edges(self):
        return len(self.edge_list())

    def number_of_vertices(self):
        return len(self.vertex_set())

    def add_vertex(self):
        """Adds an extra vertex."""
        if self.vertex_set():
            max_vertex = max(self.vertex_set())
            self.adjacency_list[max_vertex + 1] = set()
        else:
            self.adjacency_list[0] = set()

    def add_edge(self, edge):
        """Adds an edge of the form {i,j}.
        Edge will be rejected if endpoints are not in the graph."""
        for i in edge:
            for j in edge:
                if i != j:
                    self.adjacency_list[i].add(j)

    def delete_edge(self, edge):
        """Deletes an edge of the form {i,j}.
        Edge will be rejected if endpoints are not in the graph."""
        for i in edge:
            for j in edge:
                if i != j:
                    self.adjacency_list[i].remove(j)


class DirectedGraph:
    """Entries should be dictionaries. Keys should be numbers 1,...,n and values should be subsets of 1,...,n.
    Graphs will be simple digraphs, possibly with loops."""

    def __init__(self, graph_dict):
        if graph_dict is None:
            graph_dict = {}
        self.adjacency_list = graph_dict

    def vertex_set(self):
        """Obtains vertices as a set."""
        vertices = set()
        for i in self.adjacency_list:
            vertices.add(i)
        return vertices

    def edge_list(self):
        """Obtains of list edges, each represented as a list."""
        edges = []
        for vertex in self.adjacency_list:
            for neighbour in self.adjacency_list[vertex]:
                edges.append([vertex, neighbour])
        return edges

    def number_of_edges(self):
        return len(self.edge_list())

    def number_of_vertices(self):
        return len(self.vertex_set())

    def add_vertex(self):
        """Adds an extra vertex."""
        if self.vertex_set():
            max_vertex = max(self.vertex_set())
            self.adjacency_list[max_vertex + 1] = set()
        else:
            self.adjacency_list[0] = set()

    def add_edge(self, edge):
        """Adds an edge of the form [i,j].
        Edge will be rejected if endpoints are not in the graph."""
        self.adjacency_list[edge[0]].add(edge[1])

    def delete_edge(self, edge):
        """Deletes an edge of the form [i,j].
        Edge will be rejected if endpoints are not in the graph."""
        if edge[1] in self.adjacency_list[edge[0]]:
            self.adjacency_list[edge[0]].remove(edge[1])