# -*- coding: UTF-8 -*-

'''
Module
    imycobot_controller.py
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
    Defines structural interface protocol for interactive robot manual jog and command dispatch.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMyCobotController(Protocol):
    '''
        Defines structural interface protocol for direct interactive robot control.

        It defines:

            :methods:
                | connect - Connects to manipulator serial communications port.
                | disconnect - Disconnects active hardware link.
                | is_connected - Checks if controller is actively linked.
                | send_angles - Commands joint positioning.
                | send_coords - Commands Cartesian tool positioning.
                | set_gripper - Commands end-effector gripper state.
                | power - Toggles servo power on or release.
                | home - Moves manipulator to zero home position.
                | read_angles - Queries current joint angles from hardware.
                | get_version - Returns controller component version string.
    '''

    def connect(self, port: str, baudrate: int = 115200) -> bool:
        '''
            Connects to manipulator serial communications port.

            :param port: Serial device port path or descriptor.
            :param baudrate: Transmission baud rate (default 115200).
            :return: True if successfully connected, False otherwise.
        '''

    def disconnect(self) -> None:
        '''
            Disconnects active hardware link.
        '''

    def is_connected(self) -> bool:
        '''
            Checks if controller is actively linked.

            :return: True if linked and active, False otherwise.
        '''

    def send_angles(self, angles: Sequence[float], speed: int) -> bool:
        '''
            Commands joint positioning.

            :param angles: Sequence of 6 joint angles in degrees.
            :param speed: Operating velocity percentage (1-100).
            :return: True if successfully transmitted, False otherwise.
        '''

    def send_coords(self, coords: Sequence[float], speed: int, mode: int = 0) -> bool:
        '''
            Commands Cartesian tool positioning.

            :param coords: Sequence of 6 values [X, Y, Z, Rx, Ry, Rz].
            :param speed: Operating velocity percentage (1-100).
            :param mode: Interpolation mode (0=linear, 1=angular).
            :return: True if successfully transmitted, False otherwise.
        '''

    def set_gripper(self, state: int, speed: int) -> bool:
        '''
            Commands end-effector gripper state.

            :param state: Gripper state (1=grip, 0=release).
            :param speed: Operating velocity percentage.
            :return: True if successfully transmitted, False otherwise.
        '''

    def power(self, on: bool) -> bool:
        '''
            Toggles servo power on or release.

            :param on: True to power on servos, False to release all servos.
            :return: True if command transmitted, False otherwise.
        '''

    def home(self, speed: int) -> bool:
        '''
            Moves manipulator to zero home position.

            :param speed: Movement velocity percentage.
            :return: True if command transmitted, False otherwise.
        '''

    def read_angles(self) -> Sequence[float] | None:
        '''
            Queries current joint angles from hardware.

            :return: Sequence of 6 angles in degrees, or None if unavailable.
        '''

    def get_version(self) -> str:
        '''
            Returns controller component version string.

            :return: Component version string.
        '''

