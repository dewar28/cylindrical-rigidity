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

    def independence_update(self):
        self.rank_check(self.random_rigidity_matrix())
