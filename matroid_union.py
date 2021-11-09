from graph import Graph, DirectedGraph
from rigidity_checker import RigidityChecker


class MatroidUnion:

    def __init__(self, graph_dict):
        self.graph = Graph(graph_dict)

        tree_dict = {}
        laman_dict = {}
        for vertex in self.graph.adjacency_list:
            tree_dict[vertex] = set()
            laman_dict[vertex] = set()
        self.tree = RigidityChecker(tree_dict, 1)
        self.laman = RigidityChecker(laman_dict, 2)

        # As edges are not hashable, we will need a directory for later.
        self.edge_directory = {}
        edge_list = self.graph.edge_list()
        _ = 0
        for edge in edge_list:
            self.edge_directory[_] = edge
            _ += 1

        # The direct graph D used in the algorithm.
        d_dict = {}
        for edge_number in self.edge_directory:
            d_dict[edge_number] = set()
        self.d_graph = DirectedGraph(d_dict)

    def get_edge_number(self, edge):
        """Obtain a key from edge_directory corresponding to the inputted edge."""
        for key in self.edge_directory:
            if self.edge_directory[key] == edge:
                return key

    def clear_d_graph(self):
        """Clear the edges of self.d_graph."""
        edge_list = self.d_graph.edge_list()
        for edge in edge_list:
            self.d_graph.delete_edge(edge)

    def check_edge_pair_laman(self, edge_in, edge_out):
        self.laman.add_edge(edge_in)
        self.laman.delete_edge(edge_out)
        self.laman.independence_update()
        if self.laman.independent is True:
            source = self.get_edge_number(edge_out)
            sink = self.get_edge_number(edge_in)
            self.d_graph.add_edge([source, sink])
        self.laman.add_edge(edge_out)
        self.laman.delete_edge(edge_in)

    def check_edge_pair_tree(self, edge_in, edge_out):
        self.tree.add_edge(edge_in)
        self.tree.delete_edge(edge_out)
        self.tree.independence_update()
        if self.tree.independent is True:
            source = self.get_edge_number(edge_out)
            sink = self.get_edge_number(edge_in)
            self.d_graph.add_edge([source, sink])
        self.tree.add_edge(edge_out)
        self.tree.delete_edge(edge_in)


# Test code, ignore
# check = MatroidUnion({0: {1}, 1: {0,2}, 2: {1}})
#
# check.laman.add_edge({0,1})
# print("Laman graph", check.laman.adjacency_list)
# print("edge directory", check.edge_directory)
# print("d graph", check.d_graph.adjacency_list)
# check.check_edge_pair_laman({1,2},{0,1})
# print("d graph", check.d_graph.adjacency_list)
# check.clear_d_graph()
# print("d graph after clearing", check.d_graph.adjacency_list)