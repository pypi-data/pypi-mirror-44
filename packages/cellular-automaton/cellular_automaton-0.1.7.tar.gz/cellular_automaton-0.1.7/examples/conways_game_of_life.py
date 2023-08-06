#!/usr/bin/env python3
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

import random
from cellular_automaton import *


ALIVE = [1.0]
DEAD = [0]


class ConwaysRule(Rule):
    random_seed = random.seed(13)

    def init_state(self, cell_coordinate):
        rand = random.randrange(0, 16, 1)
        init = max(.0, float(rand - 14))
        return [init]

    def evolve_cell(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state
        alive_neighbours = self.__count_alive_neighbours(neighbors_last_states)
        if last_cell_state == DEAD and alive_neighbours == 3:
            new_cell_state = ALIVE
        if last_cell_state == ALIVE and alive_neighbours < 2:
            new_cell_state = DEAD
        if last_cell_state == ALIVE and 1 < alive_neighbours < 4:
            new_cell_state = ALIVE
        if last_cell_state == ALIVE and alive_neighbours > 3:
            new_cell_state = DEAD
        return new_cell_state

    @staticmethod
    def __count_alive_neighbours(neighbours):
        an = []
        for n in neighbours:
            if n == ALIVE:
                an.append(1)
        return len(an)

    def get_state_draw_color(self, current_state):
        return [255 if current_state[0] else 0, 0, 0]


if __name__ == "__main__":
    neighborhood = MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    ca = CAFactory.make_multi_process_cellular_automaton(dimension=[100, 100],
                                                         neighborhood=neighborhood,
                                                         rule=ConwaysRule,
                                                         processes=4)
    ca_window = CAWindow(cellular_automaton=ca, evolution_steps_per_draw=1)
