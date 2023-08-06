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


class StarfallRule(Rule):
    """ A basic cellular automaton that just copies one neighbour state so get some motion in the grid. """
    random_seed = random.seed(1000)

    def init_state(self, cell_coordinate):
        rand = random.randrange(0, 101, 1)
        init = max(.0, float(rand - 99))
        return [init]

    def evolve_cell(self, last_cell_state, neighbors_last_states):
        return self._get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, -1))

    def get_state_draw_color(self, current_state):
        return [255 if current_state[0] else 0, 0, 0]


if __name__ == "__main__":
    neighborhood = MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    ca = CAFactory.make_single_process_cellular_automaton(dimension=[100, 100],
                                                          neighborhood=neighborhood,
                                                          rule=StarfallRule)
    ca_window = CAWindow(cellular_automaton=ca, evolution_steps_per_draw=1)
