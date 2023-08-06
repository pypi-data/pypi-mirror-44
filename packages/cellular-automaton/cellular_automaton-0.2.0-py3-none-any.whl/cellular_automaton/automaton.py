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

import multiprocessing

from multiprocessing.sharedctypes import RawValue
from ctypes import c_int


class CellularAutomatonProcessor:
    """ This class is responsible for the evolution of the cells. """

    def __init__(self, cellular_automaton):
        self._ca = cellular_automaton

    def evolve_x_times(self, x):
        """ Evolve all cells x times.
        :param x: The number of evolution steps processed with the call of this method.
        """
        for x in range(x):
            self.evolve()

    def evolve(self):
        """ Evolve all cells """
        self._ca.current_evolution_step += 1
        i = self._ca.current_evolution_step
        r = self._ca.evolution_rule.evolve_cell
        list(map(lambda c: c.evolve_if_ready(r, i), tuple(self._ca.cells.values())))

    def get_dimension(self):
        return self._ca.dimension

    def get_cells(self):
        return self._ca.cells

    def get_current_evolution_step(self):
        return self._ca.current_evolution_step

    def get_current_rule(self):
        return self._ca.evolution_rule


class CellularAutomatonMultiProcessor(CellularAutomatonProcessor):
    """ This is a variant of CellularAutomatonProcessor that uses multi processing.
        The evolution of the cells will be outsourced to new processes.

        WARNING:
        This variant has high memory use!
        The inter process communication overhead can make this variant slower than single processing!
    """

    def __init__(self, cellular_automaton, process_count: int = 2):
        multiprocessing.freeze_support()
        if process_count < 1:
            raise ValueError

        super().__init__(cellular_automaton)

        self.evolve_range = range(len(self._ca.cells))
        self._ca.current_evolution_step = RawValue(c_int, self._ca.current_evolution_step)
        self.__init_processes(process_count)

    def __init_processes(self, process_count):
        self.pool = multiprocessing.Pool(processes=process_count,
                                         initializer=_init_process,
                                         initargs=(tuple(self._ca.cells.values()),
                                                   self._ca.evolution_rule,
                                                   self._ca.current_evolution_step))

    def evolve(self):
        self._ca.current_evolution_step.value += 1
        self.pool.map(_process_routine, self.evolve_range)

    def get_current_evolution_step(self):
        return self._ca.current_evolution_step.value


global_cells = None
global_rule = None
global_evolution_step = None


def _init_process(cells, rule, index):
    global global_rule, global_cells, global_evolution_step
    global_cells = cells
    global_rule = rule
    global_evolution_step = index


def _process_routine(i):
    global_cells[i].evolve_if_ready(global_rule.evolve_cell, global_evolution_step.value)
