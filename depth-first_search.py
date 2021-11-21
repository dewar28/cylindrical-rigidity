from graph import DirectedGraph

class DepthSearchDigraph(DirectedGraph):

    def __init__(self, graph_dict):
        super().__init__(graph_dict)
        self.stack = []
        self.path = []

    def reset(self):
        self.stack = []
        self.path = []

    def depth_search(self, start_vertex, vertex_set):
        self.reset()
        self.stack.append(start_vertex)