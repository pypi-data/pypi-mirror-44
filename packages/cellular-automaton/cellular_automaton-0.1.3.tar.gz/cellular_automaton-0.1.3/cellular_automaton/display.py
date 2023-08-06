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

import pygame
import time
import operator

from . import automaton


class _CASurface:
    def __init__(self, grid_rect, cellular_automaton: automaton.CellularAutomatonProcessor, screen):
        self._cellular_automaton = cellular_automaton
        self.__rect = grid_rect
        self.__cell_size = self._calculate_cell_display_size()
        self.__screen = screen

    def _calculate_cell_display_size(self):
        grid_dimension = self._cellular_automaton.get_dimension()
        return [self.__rect.width / grid_dimension[0], self.__rect.height / grid_dimension[1]]

    def redraw_cellular_automaton(self):
        """ Redraws those cells which changed their state since last redraw. """
        update_rectangles = list(self.__redraw_dirty_cells())
        pygame.display.update(update_rectangles)

    def __redraw_dirty_cells(self):
        for coordinate, cell in self._cellular_automaton.get_cells().items():
            if cell.is_set_for_redraw():
                yield from self.__redraw_cell(cell, coordinate)

    def __redraw_cell(self, cell, coordinate):
        cell_color = self.__get_cell_color(cell)
        cell_pos = self._calculate_cell_position_in_the_grid(coordinate)
        surface_pos = self._calculate_cell_position_on_screen(cell_pos)
        cell.was_redrawn()
        yield self._draw_the_cell_to_screen(cell_color, surface_pos)

    def __get_cell_color(self, cell):
        return self._cellular_automaton.get_current_rule().get_state_draw_color(
            cell.get_current_state(self._cellular_automaton.get_current_evolution_step()))

    def _calculate_cell_position_in_the_grid(self, coordinate):
        return list(map(operator.mul, self.__cell_size, coordinate))

    def _calculate_cell_position_on_screen(self, cell_pos):
        return [self.__rect.left + cell_pos[0], self.__rect.top + cell_pos[1]]

    def _draw_the_cell_to_screen(self, cell_color, surface_pos):
        return self.__screen.fill(cell_color, (surface_pos, self.__cell_size))


class CAWindow:
    def __init__(self, cellular_automaton: automaton.CellularAutomatonProcessor,
                 evolution_steps_per_draw=1,
                 window_size=(1000, 800)):
        self._ca = cellular_automaton
        self.__window_size = window_size
        self.__init_pygame()
        self.__loop_evolution_and_redraw_of_automaton(evolution_steps_per_draw=evolution_steps_per_draw)

    def __init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Cellular Automaton")
        self._screen = pygame.display.set_mode(self.__window_size)
        self._font = pygame.font.SysFont("monospace", 15)

        self.ca_display = _CASurface(pygame.Rect(0, 30, self.__window_size[0], self.__window_size[1] - 30),
                                     self._ca,
                                     self._screen)

    def __loop_evolution_and_redraw_of_automaton(self, evolution_steps_per_draw):
        running = True

        while running:
            time_ca_start = time.time()
            self._ca.evolve_x_times(evolution_steps_per_draw)
            time_ca_end = time.time()
            self.ca_display.redraw_cellular_automaton()
            time_ds_end = time.time()
            self.__print_process_duration(time_ca_end, time_ca_start, time_ds_end)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def __print_process_duration(self, time_ca_end, time_ca_start, time_ds_end):
        self._screen.fill([0, 0, 0], ((0, 0), (self.__window_size[0], 30)))
        self.__write_text((10, 5), "CA: " + "{0:.4f}".format(time_ca_end - time_ca_start) + "s")
        self.__write_text((310, 5), "Display: " + "{0:.4f}".format(time_ds_end - time_ca_end) + "s")
        self.__write_text((660, 5), "Step: " + str(self._ca.get_current_evolution_step()))

    def __write_text(self, pos, text, color=(0, 255, 0)):
        label = self._font.render(text, 1, color)
        update_rect = self._screen.blit(label, pos)
        pygame.display.update(update_rect)
