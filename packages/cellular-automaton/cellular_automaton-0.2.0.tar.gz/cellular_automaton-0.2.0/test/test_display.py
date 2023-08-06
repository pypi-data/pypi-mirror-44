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
    def init_state(self, cell_coordinate):
        return [1] if cell_coordinate == (1, 1) else [0]

    def evolve_cell(self, last_cell_state, neighbors_last_states):
        return [last_cell_state[0] + 1] if neighbors_last_states else last_cell_state

    def get_state_draw_color(self, current_state):
        return 255, 0, 0


class DrawEngineMock(display.DrawEngine):
    written_texts = 0
    filled_surfaces = 0
    updated_rectangles = 0
    _draws = 0
    _draws_until_end = 1

    def __init__(self, window_size=None, draws_until_end=1):
        super(display.DrawEngine, self).__init__()
        self._width = window_size[0]
        self._height = window_size[1]
        DrawEngineMock.written_texts = 0
        DrawEngineMock.filled_surfaces = 0
        DrawEngineMock.updated_rectangles = 0
        DrawEngineMock._draws = 0

        DrawEngineMock._draws_until_end = draws_until_end

    def write_text(self, pos, text, color=(0, 255, 0)):
        self.written_texts += 1

    def fill_surface_with_color(self, rect, color=(0, 0, 0)):
        self.filled_surfaces += 1

    @staticmethod
    def update_rectangles(rectangles):
        DrawEngineMock.updated_rectangles += len(rectangles)
        DrawEngineMock._draws += 1

    @staticmethod
    def is_active():
        return DrawEngineMock._draws < DrawEngineMock._draws_until_end


class CAWindowMock(CAWindow, DrawEngineMock):
    """ Mocks the window with fake engine. """


class TestDisplay(unittest.TestCase):
    def setUp(self):
        self.ca = CAFactory.make_single_process_cellular_automaton((3, 3), MooreNeighborhood(), TestRule)

    def test_evolution_steps_per_draw(self):
        mock = CAWindowMock(self.ca, evolution_steps_per_draw=10, window_size=(10, 10))
        self.assertEqual(self.ca.get_current_evolution_step(), 10)

    def test_updated_rectangle_count(self):
        mock = CAWindowMock(self.ca, evolution_steps_per_draw=1, window_size=(10, 10), draws_until_end=4)
        self.assertEqual(DrawEngineMock.updated_rectangles, 9 + 3)


if __name__ == '__main__':
    unittest.main()
