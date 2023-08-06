"""
Copyright 2019 Richard Feistenauer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
sys.path.append('../cellular_automaton')

import cellular_automaton as csn
import unittest


class TestNeighborhood(unittest.TestCase):
    @staticmethod
    def check_neighbors(neighborhood, neighborhood_sets, dimension=(3, 3)):
        for neighborhood_set in neighborhood_sets:
            neighbors = neighborhood.calculate_cell_neighbor_coordinates(neighborhood_set[0], dimension)
            if neighborhood_set[1] != neighbors:
                print("\nrel_n:", neighborhood._rel_neighbors)
                print("\nWrong neighbors (expected, real): ", (neighborhood_set[1]), neighbors)
                return False
        return True

    def test_ignore_missing_neighbors(self):
        neighborhood = csn.MooreNeighborhood(csn.EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS)
        n00 = [[0, 0], [[1, 0], [0, 1], [1, 1]]]
        n01 = [[0, 1], [[0, 0], [1, 0], [1, 1], [0, 2], [1, 2]]]
        n11 = [[1, 1], [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1], [0, 2], [1, 2], [2, 2]]]
        n22 = [[2, 2], [[1, 1], [2, 1], [1, 2]]]
        self.assertTrue(self.check_neighbors(neighborhood, [n00, n01, n11, n22]))

    def test_ignore_edge_cells(self):
        neighborhood = csn.MooreNeighborhood(csn.EdgeRule.IGNORE_EDGE_CELLS)
        n00 = [[0, 0], []]
        n01 = [[0, 1], []]
        n20 = [[2, 0], []]
        n11 = [[1, 1], [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1], [0, 2], [1, 2], [2, 2]]]
        n22 = [[2, 2], []]
        self.assertTrue(self.check_neighbors(neighborhood, [n00, n01, n20, n11, n22]))

    def test_cyclic_dimensions(self):
        neighborhood = csn.MooreNeighborhood(csn.EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
        n00 = [[0, 0], [[2, 2], [0, 2], [1, 2], [2, 0], [1, 0], [2, 1], [0, 1], [1, 1]]]
        n11 = [[1, 1], [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1], [0, 2], [1, 2], [2, 2]]]
        n22 = [[2, 2], [[1, 1], [2, 1], [0, 1], [1, 2], [0, 2], [1, 0], [2, 0], [0, 0]]]
        self.assertTrue(self.check_neighbors(neighborhood, [n00, n11, n22]))

    def test_von_neumann_r1(self):
        neighborhood = csn.VonNeumannNeighborhood(csn.EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
        n1 = [[1, 1], [[1, 0], [0, 1], [2, 1], [1, 2]]]
        self.assertTrue(self.check_neighbors(neighborhood, [n1]))

    def test_von_neumann_r2(self):
        neighborhood = csn.VonNeumannNeighborhood(csn.EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS, radius=2)
        n1 = [[2, 2], [[2, 0], [1, 1], [2, 1], [3, 1], [0, 2], [1, 2], [3, 2], [4, 2], [1, 3], [2, 3], [3, 3], [2, 4]]]
        self.assertTrue(self.check_neighbors(neighborhood, [n1], dimension=[5, 5]))

    def test_von_neumann_d3(self):
        neighborhood = csn.VonNeumannNeighborhood(csn.EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS,
                                                  dimension=3)
        n1 = [[1, 1, 1], [[1, 1, 0], [1, 0, 1], [0, 1, 1], [2, 1, 1], [1, 2, 1], [1, 1, 2]]]
        self.assertTrue(self.check_neighbors(neighborhood, [n1], dimension=[3, 3, 3]))

    def test_hexagonal(self):
        neighborhood = csn.RadialNeighborhood(csn.EdgeRule.IGNORE_EDGE_CELLS, radius=2)
        n1 = [[2, 2], [[1, 0], [2, 0], [3, 0],
                       [0, 1], [1, 1], [2, 1], [3, 1], [4, 1],
                       [0, 2], [1, 2], [3, 2], [4, 2],
                       [0, 3], [1, 3], [2, 3], [3, 3], [4, 3],
                       [1, 4], [2, 4], [3, 4]]]
        self.assertTrue(self.check_neighbors(neighborhood, [n1], dimension=[5, 5]))

    def test_hexagonal(self):
        neighborhood = csn.HexagonalNeighborhood(csn.EdgeRule.IGNORE_EDGE_CELLS, radius=2)
        n1 = [[2, 2], [[1, 0], [2, 0], [3, 0],
                       [0, 1], [1, 1], [2, 1], [3, 1],
                       [0, 2], [1, 2], [3, 2], [4, 2],
                       [0, 3], [1, 3], [2, 3], [3, 3],
                       [1, 4], [2, 4], [3, 4]]]
        n2 = [[2, 3], [[1, 1], [2, 1], [3, 1],
                       [1, 2], [2, 2], [3, 2], [4, 2],
                       [0, 3], [1, 3], [3, 3], [4, 3],
                       [1, 4], [2, 4], [3, 4], [4, 4],
                       [1, 5], [2, 5], [3, 5]]]
        self.assertTrue(self.check_neighbors(neighborhood, [n1, n2], dimension=[6, 6]))


if __name__ == '__main__':
    unittest.main()
