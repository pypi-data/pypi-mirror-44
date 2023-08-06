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

import abc

from . import neighborhood


class Rule:
    """ Base class for evolution rules.
        This class has to be inherited if the cellular automaton is supposed to have any effect.
    """

    def __init__(self, neighborhood_: neighborhood.Neighborhood):
        self._neighborhood = neighborhood_

    def _get_neighbor_by_relative_coordinate(self, neighbours, rel_coordinate):
        return neighbours[self._neighborhood.get_id_of_neighbor_from_relative_coordinate(rel_coordinate)]

    @abc.abstractmethod
    def evolve_cell(self, last_cell_state, neighbors_last_states):
        """ Calculates and sets new state of 'cell'.
        A cells evolution will only be called if it or at least one of its neighbors has changed last evolution_step.
        :param last_cell_state:         The cells state previous to the evolution step.
        :param neighbors_last_states:   The cells neighbors current states.
        :return: New state.             The state after this evolution step
        """
        return last_cell_state

    @abc.abstractmethod
    def init_state(self, cell_coordinate):
        """ Will be called to initialize a cells state.
        :param cell_coordinate: Cells coordinate.
        :return: Iterable that represents the initial cell state
                 Has to be compatible with 'multiprocessing.sharedctype.RawArray' when using multi processing.
        """
        return [0]

    @abc.abstractmethod
    def get_state_draw_color(self, current_state):
        """ Return the draw color for the current state """
        return [0, 0, 0]
