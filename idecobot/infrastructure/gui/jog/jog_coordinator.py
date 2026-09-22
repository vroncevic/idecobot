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

from idecobot.core.service.communication.imycobot_controller import IMyCobotController
from idecobot.core.service.kinematics.ikinematic_validator import IKinematicValidator
from idecobot.infrastructure.gui.jog.jog_constants import JogConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
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
                | _on_log - Injected logging callback.
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
                | get_version - Returns jog coordinator version string.
    '''

    _controller: IMyCobotController
    _validator: IKinematicValidator
    _constants: JogConstants
    _on_log: Callable[[str], None]
    _current_angles: list[float]
    _current_coords: list[float]

    def __init__(
        self,
        controller: IMyCobotController,
        validator: IKinematicValidator,
        constants: JogConstants,
        on_log: Callable[[str], None]
    ) -> None:
        '''
            Initializes jog coordinator.

            :param controller: Injected robot communication controller.
            :param validator: Injected kinematic validator service.
            :param constants: Injected JogConstants configuration.
            :param on_log: Injected logging callback.
            :exceptions: None.
        '''
        self._controller = controller
        self._validator = validator
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

        if not self._validator.is_joint_in_range(joint_id, new_angle):
            self._on_log(f'⚠️ Jog refused: J{joint_id} angle {new_angle:.1f}° exceeds kinematic bounds!')
            return False

        self._current_angles[idx] = round(new_angle, self._constants.round_precision)
        success: bool = self._controller.send_angles(self._current_angles, speed)

        if success:
            self._on_log(f'Jog J{joint_id}: {self._current_angles[idx]:.1f}° (speed={speed}%)')
        else:
            self._on_log(f'❌ Jog command failed for joint J{joint_id}')
        return success

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

        if axis in self._constants.linear_axes:
            tx: float = new_val if axis == 'X' else self._current_coords[0]
            ty: float = new_val if axis == 'Y' else self._current_coords[1]
            tz: float = new_val if axis == 'Z' else self._current_coords[2]

            if not self._validator.is_reach_safe(tx, ty, tz):
                r: float = (tx ** 2 + ty ** 2 + tz ** 2) ** 0.5
                self._on_log(f'⚠️ Jog refused: reach {r:.1f}mm exceeds safe radius!')
                return False

            if axis == 'Z' and not self._validator.is_z_safe(new_val):
                self._on_log(f'⚠️ Jog refused: Z={new_val:.1f}mm below minimum safe floor!')
                return False

        self._current_coords[idx] = round(new_val, self._constants.round_precision)
        success: bool = self._controller.send_coords(self._current_coords, speed)

        if success:
            self._on_log(f'Jog {axis}: {self._current_coords[idx]:.1f} (speed={speed}%)')
        else:
            self._on_log(f'❌ Jog command failed for axis {axis}')
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
            self._on_log(f'Tool: {action} (speed={speed}%)')
        else:
            self._on_log(f'❌ Tool command failed: {action}')
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
            self._on_log(f'Servos: {action}')
        else:
            self._on_log(f'❌ Failed to send {action}')
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
            self._on_log(f'Manipulator homed to 0° (speed={speed}%)')
        else:
            self._on_log('❌ Failed to home manipulator')

        return success

    def get_version(self) -> str:
        '''
            Returns jog coordinator implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
