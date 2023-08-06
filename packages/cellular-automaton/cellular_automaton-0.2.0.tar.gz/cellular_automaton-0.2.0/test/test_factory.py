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

from cellular_automaton import *
from cellular_automaton.cellular_automaton.cell_state import CellState
from cellular_automaton.cellular_automaton.state import CellularAutomatonState
import unittest
import mock


class TestFac(CAFactory):
    @staticmethod
    def make_cell_states(state_class, rule_, dimension):
        return CAFactory._make_cell_states(state_class, rule_, dimension)

    @staticmethod
    def make_cells(cells, neighborhood_, dimension):
        return CAFactory._make_cells(cells, neighborhood_, dimension)

    @staticmethod
    def make_cellular_automaton_state(dimension, neighborhood_, state_class, rule):
        return TestFac._make_cellular_automaton_state(dimension, neighborhood_, state_class, rule)


class TestRule(Rule):
    def evolve_cell(self, last_cell_state, neighbors_last_states):
        return last_cell_state

    def init_state(self, cell_coordinate):
        return [1]

    def get_state_draw_color(self, current_state):
        return [0, 0, 0]


class TestCAFactory(unittest.TestCase):
    def setUp(self):
        self._neighborhood = MooreNeighborhood(EdgeRule.IGNORE_EDGE_CELLS)

    def test_make_ca_calls_correct_methods(self):
        with mock.patch.object(CAFactory, '_make_cell_states', return_value={1: True}) as m1:
            with mock.patch.object(CAFactory, '_make_cells') as m2:
                TestFac.make_cellular_automaton_state([10], self._neighborhood, CellState, Rule)
                m1.assert_called_once()
                m2.assert_called_once_with({1: True}, self._neighborhood, [10])

    def test_make_ca_returns_correct_values(self):
        with mock.patch.object(CAFactory, '_make_cell_states', return_value={1: True}):
            with mock.patch.object(CAFactory, '_make_cells', return_value={1: True}):
                ca = TestFac.make_cellular_automaton_state([10], self._neighborhood, CellState, Rule)
                self.assertIsInstance(ca, CellularAutomatonState)
                self.assertEqual(tuple(ca.cells.values()), (True, ))

    def test_make_cells(self):
        cell_states = self.__create_cell_states()
        cells = TestFac.make_cells(cell_states, self._neighborhood, [3, 3])
        neighbours_of_mid = self.__cast_cells_to_list_and_remove_center_cell(cell_states)
        self.assertEqual(set(cells[(1, 1)]._neighbor_states), set(neighbours_of_mid))

    @staticmethod
    def __cast_cells_to_list_and_remove_center_cell(cell_states):
        neighbours_of_mid = list(cell_states.values())
        neighbours_of_mid.remove(neighbours_of_mid[4])
        return neighbours_of_mid

    @staticmethod
    def __create_cell_states():
        cell_states = {}
        for x in range(3):
            for y in range(3):
                cell_states[(x, y)] = CellState([x * y], False)
        return cell_states

    def test_1dimension_coordinates(self):
        c = TestFac.make_cell_states(CellState, Rule(self._neighborhood), [3])
        self.assertEqual(list(c.keys()), [(0,), (1,), (2,)])

    def test_2dimension_coordinates(self):
        c = TestFac.make_cell_states(CellState, Rule(self._neighborhood), [2, 2])
        self.assertEqual(list(c.keys()), [(0, 0), (0, 1), (1, 0), (1, 1)])

    def test_3dimension_coordinates(self):
        c = TestFac.make_cell_states(CellState, Rule(self._neighborhood), [2, 2, 2])
        self.assertEqual(list(c.keys()), [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
                                          (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)])


if __name__ == '__main__':
    unittest.main()
