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

import itertools

from typing import Type

from . import Neighborhood, Rule
from .automaton import CellularAutomatonProcessor, CellularAutomatonMultiProcessor
from .cell import Cell
from .state import CellularAutomatonState
from .cell_state import CellState, SynchronousCellState


class CAFactory:
    """ This factory provides an easy way to create cellular automatons with single or multi processing. """

    @staticmethod
    def make_single_process_cellular_automaton(dimension,
                                               neighborhood: Neighborhood,
                                               rule: Type[Rule]):

        ca = CAFactory._make_cellular_automaton_state(dimension, neighborhood, CellState, rule)
        return CellularAutomatonProcessor(ca)

    @staticmethod
    def _make_cellular_automaton_state(dimension, neighborhood, state_class, rule_class):
        rule = rule_class(neighborhood)
        cell_states = CAFactory._make_cell_states(state_class, rule, dimension)
        cells = CAFactory._make_cells(cell_states, neighborhood, dimension)
        return CellularAutomatonState(cells, dimension, rule)

    @staticmethod
    def make_multi_process_cellular_automaton(dimension,
                                              neighborhood: Neighborhood,
                                              rule: Type[Rule],
                                              processes: int):
        if processes < 1:
            raise ValueError("At least one process is necessary")
        elif processes == 1:
            return CAFactory.make_single_process_cellular_automaton(dimension, neighborhood, rule)
        else:
            ca = CAFactory._make_cellular_automaton_state(dimension, neighborhood, SynchronousCellState, rule)
            return CellularAutomatonMultiProcessor(ca, processes)

    @staticmethod
    def _make_cell_states(state_class, rule, dimension):
        cell_states = {}
        for c in itertools.product(*[range(d) for d in dimension]):
            coordinate = tuple(c)
            cell_states[coordinate] = state_class(rule.init_state(coordinate))
        return cell_states

    @staticmethod
    def _make_cells(cell_states, neighborhood, dimension):
        cells = {}
        for coordinate, cell_state in cell_states.items():
            n_coordinates = neighborhood.calculate_cell_neighbor_coordinates(coordinate, dimension)
            neighbor_states = tuple([cell_states[tuple(nc)] for nc in n_coordinates])
            cells[coordinate] = Cell(cell_state, neighbor_states)
        return cells


