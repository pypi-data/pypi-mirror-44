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

from multiprocessing.sharedctypes import RawArray, RawValue
from ctypes import c_float, c_bool


class CellState:
    """
        This is the base class for all cell states.
        When using the cellular automaton display, inherit this class and implement get_state_draw_color.
    """

    _state_save_slot_count = 2

    def __init__(self, initial_state=(0., ), draw_first_state=True):
        self._state_slots = [list(initial_state) for i in range(self.__class__._state_save_slot_count)]
        self._active = [False for i in range(self.__class__._state_save_slot_count)]
        self._active[0] = True
        self._dirty = draw_first_state

    def is_active(self, current_evolution_step):
        """ Returns the active status for the requested evolution_step
        :param current_evolution_step: The evolution_step of interest.
        :return: True if the cell or one of its neighbours changed in the last evolution step.
        """
        return self._active[self._calculate_slot(current_evolution_step)]

    def set_active_for_next_evolution_step(self, current_evolution_step):
        """ Sets the cell active for the next evolution_step, so it will be evolved.
        :param current_evolution_step: The current evolution_step index.
        """
        self._active[self._calculate_slot(current_evolution_step + 1)] = True

    def is_set_for_redraw(self):
        """ States if this state should be redrawn.
        :return: True if state changed since last call of 'was_redrawn'.
        """
        return self._dirty

    def was_redrawn(self):
        """ Remove the state from redraw cycle until next state change """
        self._dirty = False

    def get_state_of_last_evolution_step(self, current_evolution_step):
        return self.get_state_of_evolution_step(current_evolution_step - 1)

    def get_state_of_evolution_step(self, evolution_step):
        """ Returns the state of the evolution_step.
        :param evolution_step:  Uses the evolution_step index, to differ between concurrent states.
        :return The state of the requested evolution_step.
        """
        return self._state_slots[self._calculate_slot(evolution_step)]

    def set_state_of_evolution_step(self, new_state, evolution_step):
        """ Sets the new state for the evolution_step.
        :param new_state:  The new state to set.
        :param evolution_step:  The evolution_step index, to differ between concurrent states.
        :return True if the state really changed.
        :raises IndexError: If the state length changed.
        """
        changed = self._set_new_state_if_valid(new_state, evolution_step)
        self._dirty |= changed
        self._active[self._calculate_slot(evolution_step)] = False
        return changed

    def _set_new_state_if_valid(self, new_state, evolution_step):
        current_state = self.get_state_of_evolution_step(evolution_step)
        if len(new_state) != len(current_state):
            raise IndexError("State length may not change!")

        self.__change_current_state_values(current_state, new_state)
        return self.__did_state_change(evolution_step)

    @staticmethod
    def __change_current_state_values(current_state, new_state):
        for i, ns in enumerate(new_state):
            if current_state[i] != ns:
                current_state[i] = ns

    def __did_state_change(self, evolution_step):
        for a, b in zip(self.get_state_of_evolution_step(evolution_step),
                        self.get_state_of_last_evolution_step(evolution_step)):
            if a != b:
                return True
        return False

    def get_state_draw_color(self, evolution_step):
        """ When implemented should return the color representing the requested state.
        :param evolution_step: Requested evolution_step.
        :return: Color of the state as rgb tuple
        """
        raise NotImplementedError

    @classmethod
    def _calculate_slot(cls, evolution_step):
        return evolution_step % cls._state_save_slot_count


class SynchronousCellState(CellState):
    """ CellState version using shared values for multi processing purpose. """

    def __init__(self, initial_state=(0., ), draw_first_state=True):
        super().__init__(initial_state, draw_first_state)
        self._state_slots = [RawArray(c_float, initial_state) for i in range(self.__class__._state_save_slot_count)]
        self._active = [RawValue(c_bool, False) for i in range(self.__class__._state_save_slot_count)]
        self._active[0].value = True
        self._dirty = RawValue(c_bool, draw_first_state)

    def set_active_for_next_evolution_step(self, current_evolution_step):
        self._active[self._calculate_slot(current_evolution_step + 1)].value = True

    def is_set_for_redraw(self):
        return self._dirty.value

    def was_redrawn(self):
        self._dirty.value = False

    def set_state_of_evolution_step(self, new_state, evolution_step):
        changed = self._set_new_state_if_valid(new_state, evolution_step)
        self._dirty.value |= changed
        self._active[self._calculate_slot(evolution_step)].value = False
        return changed
