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

        # The set F used in algorithm loop.
        self.F = []

    def run_program(self):
        repeat = True
        all_edges = self.graph.edge_list()
        while repeat is True:
            repeat = False
            self.clear_d_graph()
            laman_edges = self.laman.edge_list()
            tree_edges = self.tree.edge_list()
            not_laman_edges = [edge for edge in all_edges if edge not in laman_edges]
            not_tree_edges = [edge for edge in all_edges if edge not in tree_edges]
            if laman_edges:
                if not_tree_edges:
                    for edge_out in laman_edges:
                        for edge_in in not_tree_edges:
                            self.check_edge_pair_laman(edge_in, edge_out)
            if tree_edges:
                if not_laman_edges:
                    for edge_out in tree_edges:
                        for edge_in in not_laman_edges:
                            self.check_edge_pair_tree(edge_in, edge_out)
            self.generate_f_set()
            for edge in self.F:
                if edge not in laman_edges:
                    if edge not in tree_edges:
                        if self.check_edge_single_laman(edge) is True:
                            self.laman.add_edge(edge)
                            repeat = True
                            break
                        elif self.check_edge_single_tree(edge) is True:
                            self.tree.add_edge(edge)
                            repeat = True
                            break
        print("(2,3)-tight graph edges are: ", self.laman.edge_list())
        print("Tree edges are: ", self.tree.edge_list())

    def generate_f_set(self):
        self.F = []
        all_edge = self.graph.edge_list()
        laman_edge = self.laman.edge_list()
        tree_edge = self.tree.edge_list()
        for edge in all_edge:
            if edge in laman_edge:
                if edge in tree_edge:
                    continue
                elif self.check_edge_single_tree(edge) is True:
                    self.F.append(edge)
                    continue
                else:
                    continue
            if edge in tree_edge:
                if self.check_edge_single_laman(edge) is True:
                    self.F.append(edge)
                    continue
                else:
                    continue
            if self.check_edge_single_laman(edge) is True:
                self.F.append(edge)
                continue
            if self.check_edge_single_tree(edge) is True:
                self.F.append(edge)
                continue

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

    def check_edge_single_laman(self, edge):
        self.laman.add_edge(edge)
        self.laman.independence_update()
        if self.laman.independent is True:
            self.laman.delete_edge(edge)
            return True
        else:
            self.laman.delete_edge(edge)
            return False

    def check_edge_single_tree(self, edge):
        self.tree.add_edge(edge)
        self.tree.independence_update()
        if self.tree.independent is True:
            self.tree.delete_edge(edge)
            return True
        else:
            self.tree.delete_edge(edge)
            return False


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
