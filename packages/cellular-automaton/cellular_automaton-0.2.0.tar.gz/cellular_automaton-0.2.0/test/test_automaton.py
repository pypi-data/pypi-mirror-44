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
import unittest


class TestRule(Rule):
    def evolve_cell(self, last_cell_state, neighbors_last_states):
        return [last_cell_state[0] + 1]

    def init_state(self, cell_coordinate):
        return [0]

    def get_state_draw_color(self, current_state):
        return [0, 0, 0]


class TestCellState(unittest.TestCase):
    def setUp(self):
        self.neighborhood = MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
        self.processor = CAFactory.make_single_process_cellular_automaton([3, 3],
                                                                          self.neighborhood,
                                                                          TestRule)

    def test_single_process_evolution_steps(self):
        self.processor.evolve_x_times(5)
        self.assertEqual(self.processor.get_current_evolution_step(), 5)

    def test_multi_process_evolution_steps(self):
        self.__create_multi_process_automaton()
        self.multi_processor.evolve_x_times(5)
        self.assertEqual(self.multi_processor.get_current_evolution_step(), 5)

    def __create_multi_process_automaton(self):
        self.multi_processor = CAFactory.make_multi_process_cellular_automaton([3, 3],
                                                                               self.neighborhood,
                                                                               TestRule,
                                                                               processes=2)

    def test_single_process_evolution_calls(self):
        self.processor.evolve_x_times(5)
        step = self.processor.get_current_evolution_step()
        cell = self.processor.get_cells()[(1, 1)].get_current_state(step)[0]
        self.assertEqual(cell, 4)

    def test_multi_process_evolution_calls(self):
        self.__create_multi_process_automaton()
        self.multi_processor.evolve_x_times(5)
        step = self.multi_processor.get_current_evolution_step()
        cell = self.multi_processor.get_cells()[(1, 1)].get_current_state(step)[0]
        self.assertEqual(cell, 4)


if __name__ == '__main__':
    unittest.main()
