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

from cellular_automaton.cellular_automaton.cell_state import SynchronousCellState
import unittest


class TestCellState(unittest.TestCase):
    def setUp(self):
        self.cell_state = SynchronousCellState(initial_state=(0,), draw_first_state=False)

    def test_get_state_with_overflow(self):
        self.cell_state.set_state_of_evolution_step(new_state=(1,), evolution_step=0)
        self.assertEqual(tuple(self.cell_state.get_state_of_evolution_step(2)), (1,))

    def test_set_state_with_overflow(self):
        self.cell_state.set_state_of_evolution_step(new_state=(1,), evolution_step=3)
        self.assertEqual(tuple(self.cell_state.get_state_of_evolution_step(1)), (1,))

    def test_set_state_does_not_effect_all_slots(self):
        self.cell_state.set_state_of_evolution_step(new_state=(1,), evolution_step=0)
        self.assertEqual(tuple(self.cell_state.get_state_of_evolution_step(1)), (0,))

    def test_redraw_state_on_change(self):
        self.cell_state.set_state_of_evolution_step(new_state=(1,), evolution_step=0)
        self.assertTrue(self.cell_state.is_set_for_redraw())

    def test_redraw_state_on_nochange(self):
        self.cell_state.set_state_of_evolution_step(new_state=(0,), evolution_step=0)
        self.assertFalse(self.cell_state.is_set_for_redraw())

    def test_active_state_after_set(self):
        self.cell_state.set_state_of_evolution_step(new_state=(1,), evolution_step=0)
        self.assertFalse(self.cell_state.is_active(0))
        self.assertFalse(self.cell_state.is_active(1))

    def test_set_active_for_next_evolution_step(self):
        self.cell_state.set_state_of_evolution_step(new_state=(1,), evolution_step=0)
        self.cell_state.set_active_for_next_evolution_step(0)
        self.assertFalse(self.cell_state.is_active(0))
        self.assertTrue(self.cell_state.is_active(1))

    def test_new_state_length(self):
        self.assertRaises(IndexError, self.__set_state_with_new_length)

    def __set_state_with_new_length(self):
        return self.cell_state.set_state_of_evolution_step(new_state=(1, 1), evolution_step=0)

    def test_redraw_flag(self):
        self.cell_state = SynchronousCellState(initial_state=(0,), draw_first_state=True)
        self.assertTrue(self.cell_state.is_set_for_redraw())
        self.cell_state.was_redrawn()
        self.assertFalse(self.cell_state.is_set_for_redraw())


if __name__ == '__main__':
    unittest.main()
