"""Requires numpy and scipy"""

from graph import Graph
import numpy as np
from numpy.linalg import matrix_rank
import random


class RigidityChecker(Graph):

    def __init__(self, graph_dict, dimension):
        """Graph must be in the correct form for Graph class"""
        super().__init__(graph_dict)
        self.dimension = dimension
        self.independent = False
        self.rigid = False

    def dimension_increase(self):
        self.dimension += 1

    def dimension_decrease(self):
        self.dimension -= 1

    def random_placement(self):
        placement = np.zeros((self.number_of_vertices(), self.dimension))

        for v in self.vertex_set():
            for k in range(self.dimension):
                placement[v][k] = random.randint(0, 100 * self.number_of_vertices())
        return placement

    def random_rigidity_matrix(self):
        rigidity_matrix = np.zeros((self.number_of_edges(), self.dimension * self.number_of_vertices()))
        placement = self.random_placement()
        for e in self.edge_list():
            for v in self.vertex_set():
                if v == min(e):
                    for k in range(self.dimension):
                        rigidity_matrix[self.edge_list().index(e)][self.dimension * v + k] = \
                            placement[v][k] - placement[max(e)][k]
                elif v == max(e):
                    for k in range(self.dimension):
                        rigidity_matrix[self.edge_list().index(e)][self.dimension * v + k] = \
                            -rigidity_matrix[self.edge_list().index(e)][self.dimension * min(e) + k]
        return rigidity_matrix

    def rank_check(self, matrix):
        if matrix_rank(matrix) == self.number_of_edges():
            self.independent = True
        else:
            self.independent = False
        if matrix_rank(matrix) == self.dimension * self.number_of_vertices() - \
                (self.dimension * (self.dimension + 1) / 2):
            self.rigid = True
        else:
            self.rigid = False

    def rigidity_check(self):
        self.rank_check(self.random_rigidity_matrix())
        print("")
        n = self.number_of_vertices()
        m = self.number_of_edges()
        if n < self.dimension + 1:
            if 2 * m == n * (n - 1):
                print(f"Graph is minimally rigid in dimension {self.dimension}.")
            else:
                print(f"Graph is independent and flexible in dimension {self.dimension}.")
        elif (self.independent is True) and (self.rigid is True):
            print(f"Graph is minimally rigid in dimension {self.dimension}.")
        elif (self.independent is True) and (self.rigid is False):
            print(f"Graph is independent and flexible in dimension {self.dimension}.")
        elif (self.independent is False) and (self.rigid is True):
            print(f"Graph is dependent and rigid in dimension {self.dimension}.")
        elif (self.independent is False) and (self.rigid is False):
            print(f"Graph is dependent and flexible in dimension {self.dimension}. Rerun to double check.")
