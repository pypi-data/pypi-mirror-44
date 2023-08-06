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

import time
import operator

from . import automaton


class _Rect:
    def __init__(self, left=0, top=0, width=0, height=0, rect=None, pos=None, size=None):
        if rect is not None and (pos is not None or size is not None):
            raise ValueError("define either rect OR position and size OR left, top, width and height")
        if not (left == top == width == height == 0) and not(rect == pos == size is None):
            raise ValueError("define either rect OR position and size OR left, top, width and height")

        self.__direct_initialisation(height, left, top, width)
        self.__pos_and_size_initialisation(pos, size)
        self.__rect_initialisation(rect)

    def __rect_initialisation(self, rect):
        if rect is not None:
            self.__direct_initialisation(rect[1][1], rect[0][0], rect[0][1], rect[1][0])

    def __pos_and_size_initialisation(self, pos, size):
        if pos is not None:
            self.left = pos[0]
            self.top = pos[1]

        if size is not None:
            self.width = size[0]
            self.height = size[1]

    def __direct_initialisation(self, height, left, top, width):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def get_rect_tuple(self):
        return (self.left, self.top), (self.width, self.height)


class DrawEngine(object):
    def __init__(self, window_size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global pygame
        import pygame
        pygame.init()
        pygame.display.set_caption("Cellular Automaton")
        self.__screen = pygame.display.set_mode(window_size)
        self.__font = pygame.font.SysFont("monospace", 15)

        self._width = window_size[0]
        self._height = window_size[1]

    def write_text(self, pos, text, color=(0, 255, 0)):
        label = self.__font.render(text, 1, color)
        update_rect = self.__screen.blit(label, pos)
        DrawEngine.update_rectangles(update_rect)

    def fill_surface_with_color(self, rect, color=(0, 0, 0)):
        return self.__screen.fill(color, rect)

    @staticmethod
    def update_rectangles(rectangles):
        pygame.display.update(rectangles)

    @staticmethod
    def is_active():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True


class _CASurface:
    def __init__(self,
                 grid_rect,
                 cellular_automaton: automaton.CellularAutomatonProcessor,
                 draw_engine,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cellular_automaton = cellular_automaton
        self.__rect = grid_rect
        self.__cell_size = self._calculate_cell_display_size()
        self.__draw_engine = draw_engine

    def _calculate_cell_display_size(self):
        grid_dimension = self._cellular_automaton.get_dimension()
        return [self.__rect.width / grid_dimension[0], self.__rect.height / grid_dimension[1]]

    def redraw_cellular_automaton(self):
        """ Redraws those cells which changed their state since last redraw. """
        self.__draw_engine.update_rectangles(list(self.__redraw_dirty_cells()))

    def __redraw_dirty_cells(self):
        for coordinate, cell in self._cellular_automaton.get_cells().items():
            if cell.is_set_for_redraw():
                yield from self.__redraw_cell(cell, coordinate)

    def __redraw_cell(self, cell, coordinate):
        cell_color = self.__get_cell_color(cell)
        cell_pos = self._calculate_cell_position_in_the_grid(coordinate)
        surface_pos = self._calculate_cell_position_on_screen(cell_pos)
        cell.was_redrawn()
        yield self._draw_cell_surface(surface_pos, cell_color)

    def __get_cell_color(self, cell):
        return self._cellular_automaton.get_current_rule().get_state_draw_color(
            cell.get_current_state(self._cellular_automaton.get_current_evolution_step()))

    def _calculate_cell_position_in_the_grid(self, coordinate):
        return list(map(operator.mul, self.__cell_size, coordinate))

    def _calculate_cell_position_on_screen(self, cell_pos):
        return [self.__rect.left + cell_pos[0], self.__rect.top + cell_pos[1]]

    def _draw_cell_surface(self, surface_pos, cell_color):
        return self.__draw_engine.fill_surface_with_color((surface_pos, self.__cell_size), cell_color)


class CAWindow(DrawEngine):
    def __init__(self, cellular_automaton: automaton.CellularAutomatonProcessor,
                 evolution_steps_per_draw=1,
                 window_size=(1000, 800),
                 *args, **kwargs):
        super().__init__(window_size=window_size, *args, **kwargs)
        self._ca = cellular_automaton
        self.ca_display = _CASurface(_Rect(pos=(0, 30), size=(window_size[0], window_size[1] - 30)),
                                     self._ca,
                                     self)

        self.__loop_evolution_and_redraw_of_automaton(evolution_steps_per_draw=evolution_steps_per_draw)

    def __loop_evolution_and_redraw_of_automaton(self, evolution_steps_per_draw):
        while super().is_active():
            time_ca_start = time.time()
            self._ca.evolve_x_times(evolution_steps_per_draw)
            time_ca_end = time.time()
            self.ca_display.redraw_cellular_automaton()
            time_ds_end = time.time()
            self.__print_process_duration(time_ca_end, time_ca_start, time_ds_end)

    def __print_process_duration(self, time_ca_end, time_ca_start, time_ds_end):
        super().fill_surface_with_color(_Rect(size=(self._width, 30)).get_rect_tuple())
        super().write_text((10, 5), "CA: " + "{0:.4f}".format(time_ca_end - time_ca_start) + "s")
        super().write_text((310, 5), "Display: " + "{0:.4f}".format(time_ds_end - time_ca_end) + "s")
        super().write_text((660, 5), "Step: " + str(self._ca.get_current_evolution_step()))
