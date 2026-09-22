# -*- coding: UTF-8 -*-

'''
Module
    mycobot_controller.py
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
    Defines MyCobotController composite facade delegating to connection, actuator, and telemetry.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.service.communication.itransport import ITransport
from idecobot.infrastructure.communication.streamer.iconnection_manager import IConnectionManager
from idecobot.infrastructure.communication.streamer.irobot_actuator import IRobotActuator
from idecobot.infrastructure.communication.streamer.irobot_telemetry import IRobotTelemetry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotController:
    '''
        Composite robot controller orchestrating connection, actuation, and telemetry.

        It defines:

            :attributes:
                | _connection - Injected IConnectionManager session manager.
                | _actuator - Injected IRobotActuator command executor.
                | _telemetry - Injected IRobotTelemetry query reader.
            :methods:
                | __init__ - Initializes controller facade with injected components.
                | connect - Connects to manipulator communications port.
                | disconnect - Disconnects active hardware link.
                | is_connected - Checks if controller is actively linked.
                | send_angles - Transmits joint angle target frame.
                | send_coords - Transmits Cartesian coordinate target frame.
                | set_gripper - Commands end-effector gripper state.
                | power - Toggles power on or releases servos.
                | home - Commands robot to zero home joint state.
                | read_angles - Queries current joint angles.
                | get_transport - Returns the underlying communication transport.
                | get_version - Returns controller version string.
    '''

    _connection: IConnectionManager
    _actuator: IRobotActuator
    _telemetry: IRobotTelemetry

    def __init__(
        self,
        connection: IConnectionManager,
        actuator: IRobotActuator,
        telemetry: IRobotTelemetry
    ) -> None:
        '''
            Initializes controller facade with injected components.

            :param connection: Injected IConnectionManager instance.
            :param actuator: Injected IRobotActuator instance.
            :param telemetry: Injected IRobotTelemetry instance.
            :exceptions: None.
        '''
        self._connection = connection
        self._actuator = actuator
        self._telemetry = telemetry

    def connect(self, port: str, baudrate: int = 115200) -> bool:
        '''
            Connects to manipulator communications port.

            :param port: Device port path or address.
            :param baudrate: Transmission baud rate.
            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._connection.connect(port, baudrate)

    def disconnect(self) -> None:
        '''
            Disconnects active hardware link.

            :exceptions: None.
        '''
        self._connection.disconnect()

    def is_connected(self) -> bool:
        '''
            Checks if controller is actively linked.

            :return: True if open and active, False otherwise.
            :exceptions: None.
        '''
        return self._connection.is_connected()

    def send_angles(self, angles: Sequence[float], speed: int) -> bool:
        '''
            Commands joint positioning.

            :param angles: Sequence of 6 joint angles in degrees.
            :param speed: Operating velocity percentage.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        return self._actuator.send_angles(angles, speed)

    def send_coords(
        self,
        coords: Sequence[float],
        speed: int,
        mode: int = 0
    ) -> bool:
        '''
            Commands Cartesian tool positioning.

            :param coords: Sequence of 6 values [X, Y, Z, Rx, Ry, Rz].
            :param speed: Operating velocity percentage.
            :param mode: Interpolation mode (0=linear, 1=angular).
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        return self._actuator.send_coords(coords, speed, mode)

    def set_gripper(self, state: int, speed: int) -> bool:
        '''
            Commands end-effector gripper state.

            :param state: Gripper state (1=grip, 0=release).
            :param speed: Operating velocity percentage.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        return self._actuator.set_gripper(state, speed)

    def power(self, on: bool) -> bool:
        '''
            Toggles servo power on or release.

            :param on: True to power on, False to release servos.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        return self._actuator.power(on)

    def home(self, speed: int) -> bool:
        '''
            Moves manipulator to zero home position.

            :param speed: Movement velocity percentage.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        return self._actuator.home(speed)

    def read_angles(self) -> Sequence[float] | None:
        '''
            Queries current joint angles from hardware.

            :return: Sequence of 6 angles in degrees, or None if unavailable.
            :exceptions: None.
        '''
        return self._telemetry.read_angles()

    def get_transport(self) -> ITransport:
        '''
            Returns the underlying communication transport.

            :return: Injected ITransport channel instance.
            :exceptions: None.
        '''
        return self._connection.get_transport()

    def get_version(self) -> str:
        '''
            Returns controller version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
