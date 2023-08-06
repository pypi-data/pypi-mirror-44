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
sys.path.append('..')

from cellular_automaton.cellular_automaton.cell import Cell
from cellular_automaton.cellular_automaton.cell_state import CellState
import unittest


class TestCellState(unittest.TestCase):
    def setUp(self):
        self.neighbors = [CellState() for x in range(5)]
        for neighbor in self.neighbors:
            neighbor.set_state_of_evolution_step((0, ), 0)
        self.cell = Cell(CellState(), self.neighbors)

    def cell_and_neighbors_active(self, evolution_step):
        self.neighbors.append(self.cell._state)
        all_active = True
        for state in self.neighbors:
            if not state.is_active(evolution_step):
                all_active = False
        return all_active

    def test_evolve_activation(self):
        self.cell.evolve_if_ready((lambda a, b: (1,)), 0)
        all_active = self.cell_and_neighbors_active(1)
        self.assertTrue(all_active)

    def test_evolve_activation_on_no_change(self):
        self.cell.evolve_if_ready((lambda a, b: (0,)), 0)
        all_active = self.cell_and_neighbors_active(1)
        self.assertFalse(all_active)


if __name__ == '__main__':
    unittest.main()
