# -*- coding: UTF-8 -*-

'''
Module
    robot_actuator.py
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
    Implements robot movement and tool actuation dispatching over hardware transport.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.service.communication.itransport import ITransport
from idecobot.infrastructure.communication.protocol.imycobot_protocol_codec import IMyCobotProtocolCodec

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RobotActuator:
    '''
        Dispatches movement, homing, and tool actuation commands to robot hardware.

        It defines:

            :methods:
                | __init__ - Initializes actuator with injected transport and codec.
                | send_frame - Serializes and transmits single frame to robot transport.
                | send_angles - Commands robot joint positioning.
                | send_coords - Commands robot Cartesian tool positioning.
                | set_gripper - Commands end-effector gripper state.
                | power - Toggles servo power on or releases all servos.
                | home - Commands robot to zero home joint state.
                | get_version - Returns robot actuator component version string.
    '''

    def __init__(self, transport: ITransport, codec: IMyCobotProtocolCodec) -> None:
        '''
            Initializes actuator with injected transport and codec.

            :param transport: Injected ITransport channel instance.
            :param codec: Injected IMyCobotProtocolCodec frame encoder.
            :exceptions: None.
        '''
        self._transport: ITransport = transport
        self._codec: IMyCobotProtocolCodec = codec

    def send_frame(self, frame: MyCobotFrame) -> bool:
        '''
            Transmits encoded frame to transport.

            :param frame: Frame model to serialize and send.
            :return: True if completely written, False otherwise.
            :exceptions: None.
        '''
        if not self._transport.is_open():
            return False

        raw_bytes: bytes = self._codec.encode_frame(frame)
        written: int = self._transport.write(raw_bytes)

        return written == len(raw_bytes)

    def send_angles(self, angles: Sequence[float], speed: int) -> bool:
        '''
            Commands robot joint positioning.

            :param angles: Sequence of 6 joint angles in degrees.
            :param speed: Operating velocity percentage (1-100).
            :return: True if successfully transmitted, False otherwise.
            :exceptions: None.
        '''
        return self.send_frame(self._codec.pack_angles(angles, speed))

    def send_coords(
        self,
        coords: Sequence[float],
        speed: int,
        mode: int = 0
    ) -> bool:
        '''
            Commands robot Cartesian tool positioning.

            :param coords: Sequence of 6 values [X, Y, Z, Rx, Ry, Rz].
            :param speed: Operating velocity percentage (1-100).
            :param mode: Interpolation mode (0=linear, 1=angular).
            :return: True if successfully transmitted, False otherwise.
            :exceptions: None.
        '''
        return self.send_frame(self._codec.pack_coords(coords, speed, mode))

    def set_gripper(self, state: int, speed: int) -> bool:
        '''
            Commands end-effector gripper state.

            :param state: Gripper state (1=grip, 0=release).
            :param speed: Operating velocity percentage.
            :return: True if successfully transmitted, False otherwise.
            :exceptions: None.
        '''
        return self.send_frame(self._codec.pack_gripper(state, speed))

    def power(self, on: bool) -> bool:
        '''
            Toggles servo power on or releases all servos.

            :param on: True to power on, False to release servos.
            :return: True if command transmitted, False otherwise.
            :exceptions: None.
        '''
        frame: MyCobotFrame = (
            self._codec.pack_power() if on else self._codec.pack_relax()
        )

        return self.send_frame(frame)

    def home(self, speed: int) -> bool:
        '''
            Commands robot to zero home joint state.

            :param speed: Movement velocity percentage.
            :return: True if command transmitted, False otherwise.
            :exceptions: None.
        '''
        frame: MyCobotFrame = self._codec.pack_angles(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], speed
        )

        return self.send_frame(frame)

    def get_version(self) -> str:
        '''
            Returns robot actuator component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
