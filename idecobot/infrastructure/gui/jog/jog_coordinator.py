# -*- coding: UTF-8 -*-

'''
Module
    jog_coordinator.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    idecobot is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    idecobot is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines JogCoordinator managing manual jog state, kinematic validation, and robot dispatch.
'''

from __future__ import annotations

from collections.abc import Callable

from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds
from idecobot.core.service.communication.imycobot_controller import IMyCobotController
from idecobot.infrastructure.gui.jog.jog_constants import JogConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogCoordinator:
    '''
        Coordinates manual jog state, safety boundary enforcement, and hardware dispatch.

        It defines:

            :attributes:
                | _controller - Injected robot communication controller.
                | _bounds - Injected kinematic bounds model.
                | _constants - Injected JogConstants configuration.
                | _on_log - Optional logging callback.
                | _current_angles - Tracked 6 joint angles in degrees.
                | _current_coords - Tracked Cartesian coordinates [x, y, z, rx, ry, rz].
            :methods:
                | __init__ - Initializes jog coordinator with controller and bounds.
                | get_angles - Returns tracked joint angles list.
                | get_coords - Returns tracked Cartesian coordinates list.
                | reset_positions - Resets internal tracked positions to default baseline.
                | jog_joint - Calculates joint delta, verifies bounds, and dispatches command.
                | jog_cartesian - Calculates Cartesian delta, checks reach/floor, and dispatches.
                | actuate_gripper - Sends gripper actuation command to robot.
                | toggle_power - Sends servo power toggle command to robot.
                | home - Dispatches zero homing command to robot.
    '''

    _controller: IMyCobotController
    _bounds: MyCobotBounds
    _constants: JogConstants
    _on_log: Callable[[str], None] | None
    _current_angles: list[float]
    _current_coords: list[float]

    def __init__(
        self,
        controller: IMyCobotController,
        bounds: MyCobotBounds,
        constants: JogConstants,
        on_log: Callable[[str], None] | None = None
    ) -> None:
        '''
            Initializes jog coordinator.

            :param controller: Injected robot communication controller.
            :param bounds: Injected kinematic bounds model.
            :param constants: Injected JogConstants configuration.
            :param on_log: Optional logging callback.
            :exceptions: None.
        '''
        self._controller = controller
        self._bounds = bounds
        self._constants = constants
        self._on_log = on_log
        self._current_angles = list(constants.default_angles)
        self._current_coords = list(constants.default_coords)

    def get_angles(self) -> list[float]:
        '''
            Returns current tracked joint angles.

            :return: List of 6 joint angles in degrees.
            :exceptions: None.
        '''
        return list(self._current_angles)

    def get_coords(self) -> list[float]:
        '''
            Returns current tracked Cartesian coordinates.

            :return: List of Cartesian coordinates [x, y, z, rx, ry, rz].
            :exceptions: None.
        '''
        return list(self._current_coords)

    def reset_positions(self) -> None:
        '''
            Resets tracked joint angles and Cartesian coordinates to defaults.

            :exceptions: None.
        '''
        self._current_angles = list(self._constants.default_angles)
        self._current_coords = list(self._constants.default_coords)

    def _log(self, msg: str) -> None:
        '''
            Helper invoking optional logging callback.

            :param msg: Message string to log.
            :exceptions: None.
        '''
        if self._on_log is not None:
            self._on_log(msg)

    def jog_joint(self, joint_id: int, sign: float, step: float, speed: int) -> bool:
        '''
            Handles joint jog delta calculation, bounds check, and command dispatch.

            :param joint_id: Joint index from 1 to 6.
            :param sign: Direction factor (+1.0 or -1.0).
            :param step: Jog step delta in degrees.
            :param speed: Operating speed percentage.
            :return: True if command succeeded, False otherwise.
            :exceptions: None.
        '''
        idx: int = joint_id - 1
        new_angle: float = self._current_angles[idx] + (sign * step)

        if not self._bounds.is_joint_in_range(joint_id, new_angle):
            self._log(f'⚠️ Jog refused: J{joint_id} angle {new_angle:.1f}° exceeds kinematic bounds!')
            return False

        self._current_angles[idx] = round(new_angle, self._constants.round_precision)
        success: bool = self._controller.send_angles(self._current_angles, speed)

        if success:
            self._log(f'Jog J{joint_id}: {self._current_angles[idx]:.1f}° (speed={speed}%)')
        else:
            self._log(f'❌ Jog command failed for joint J{joint_id}')
        return success

    def _is_cartesian_safe(self, axis: str, new_val: float) -> bool:
        '''
            Validates Cartesian reach radius and ground floor safety.

            :param axis: Axis name string.
            :param new_val: Proposed coordinate value.
            :return: True if safe, False if boundary violation detected.
            :exceptions: None.
        '''
        r: float = (
            (new_val if axis == 'X' else self._current_coords[0]) ** 2 +
            (new_val if axis == 'Y' else self._current_coords[1]) ** 2 +
            (new_val if axis == 'Z' else self._current_coords[2]) ** 2
        ) ** 0.5
        if r > self._bounds.max_reach_mm:
            self._log(f'⚠️ Jog refused: reach {r:.1f}mm exceeds safe radius!')
            return False
        if axis == 'Z' and not self._bounds.is_z_safe(new_val):
            self._log(f'⚠️ Jog refused: Z={new_val:.1f}mm below minimum safe floor!')
            return False
        return True

    def jog_cartesian(self, axis: str, sign: float, step: float, speed: int) -> bool:
        '''
            Handles Cartesian axis jog delta calculation and dispatch.

            :param axis: Axis name string.
            :param sign: Direction factor (+1.0 or -1.0).
            :param step: Jog step delta in mm or degrees.
            :param speed: Operating speed percentage.
            :return: True if command succeeded, False otherwise.
            :exceptions: None.
        '''
        idx: int = self._constants.axis_map[axis]
        new_val: float = self._current_coords[idx] + (sign * step)

        if axis in self._constants.linear_axes and not self._is_cartesian_safe(axis, new_val):
            return False

        self._current_coords[idx] = round(new_val, self._constants.round_precision)
        success: bool = self._controller.send_coords(self._current_coords, speed)

        if success:
            self._log(f'Jog {axis}: {self._current_coords[idx]:.1f} (speed={speed}%)')
        else:
            self._log(f'❌ Jog command failed for axis {axis}')
        return success

    def actuate_gripper(self, state: int, speed: int) -> bool:
        '''
            Actuates tool gripper.

            :param state: 1 for grip, 0 for release.
            :param speed: Gripper speed percentage.
            :return: True if command succeeded, False otherwise.
            :exceptions: None.
        '''
        action: str = self._constants.action_grip if state == 1 else self._constants.action_release
        success: bool = self._controller.set_gripper(state, speed)

        if success:
            self._log(f'Tool: {action} (speed={speed}%)')
        else:
            self._log(f'❌ Tool command failed: {action}')
        return success

    def toggle_power(self, on: bool) -> bool:
        '''
            Toggles servo power on or relax.

            :param on: True to power on, False to relax.
            :return: True if command succeeded, False otherwise.
            :exceptions: None.
        '''
        success: bool = self._controller.power(on)
        action: str = self._constants.action_power_on if on else self._constants.action_relax

        if success:
            self._log(f'Servos: {action}')
        else:
            self._log(f'❌ Failed to send {action}')
        return success

    def home(self, speed: int) -> bool:
        '''
            Dispatches homing command to reset manipulator arm to zero angles.

            :param speed: Motion speed percentage.
            :return: True if command succeeded, False otherwise.
            :exceptions: None.
        '''
        home_angles: list[float] = list(self._constants.default_angles)
        success: bool = self._controller.send_angles(home_angles, speed)

        if success:
            self.reset_positions()
            self._log(f'Manipulator homed to 0° (speed={speed}%)')
        else:
            self._log('❌ Failed to home manipulator')
        return success
