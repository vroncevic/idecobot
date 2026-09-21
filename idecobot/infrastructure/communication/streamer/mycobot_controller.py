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
    Defines MyCobotController implementing interactive robot control and manual jog commands.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.service.communication.itransport import ITransport
from idecobot.infrastructure.communication.protocol.imycobot_protocol_codec import (
    IMyCobotProtocolCodec,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotController:
    '''
        Interactive robot controller dispatching manual jog and direct hardware commands.

        It defines:

            :attributes:
                | _transport - Injected ITransport communications channel.
                | _codec - Injected IMyCobotProtocolCodec frame encoder/decoder.
                | _constants - Injected ProtocolConstants protocol parameters.
            :methods:
                | __init__ - Initializes controller with injected abstractions.
                | connect - Opens communication transport.
                | disconnect - Closes communication transport.
                | is_connected - Checks if transport is active.
                | send_angles - Transmits joint angle target frame.
                | send_coords - Transmits Cartesian coordinate target frame.
                | set_gripper - Commands end-effector gripper state.
                | power - Toggles power on or releases servos.
                | home - Commands robot to zero home joint state.
                | read_angles - Queries current joint angles.
                | _send_frame - Helper writing frame bytes to transport.
    '''

    _transport: ITransport
    _codec: IMyCobotProtocolCodec
    _constants: ProtocolConstants

    def __init__(
        self,
        transport: ITransport,
        codec: IMyCobotProtocolCodec,
        constants: ProtocolConstants
    ) -> None:
        '''
            Initializes controller with injected abstractions.

            :param transport: Injected ITransport channel.
            :param codec: Injected IMyCobotProtocolCodec codec.
            :param constants: Injected ProtocolConstants parameters.
            :exceptions: None.
        '''
        self._transport = transport
        self._codec = codec
        self._constants = constants

    def connect(self, port: str, baudrate: int = 115200) -> bool:
        '''
            Connects to manipulator serial communications port.

            :param port: Serial device port path.
            :param baudrate: Transmission baud rate.
            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        if hasattr(self._transport, '_port'):
            setattr(self._transport, '_port', port)

        if hasattr(self._transport, '_baudrate'):
            setattr(self._transport, '_baudrate', baudrate)

        return self._transport.open()

    def disconnect(self) -> None:
        '''
            Disconnects active hardware link.

            :exceptions: None.
        '''
        self._transport.close()

    def is_connected(self) -> bool:
        '''
            Checks if controller is actively linked.

            :return: True if open and active, False otherwise.
            :exceptions: None.
        '''
        return self._transport.is_open()

    def _send_frame(self, frame: MyCobotFrame) -> bool:
        '''
            Helper transmitting serialized frame bytes.

            :param frame: MyCobotFrame to send.
            :return: True if written successfully, False otherwise.
            :exceptions: None.
        '''
        if not self._transport.is_open():
            return False

        raw_bytes: bytes = frame.to_bytes()
        written: int = self._transport.write(raw_bytes)

        return written == len(raw_bytes)

    def send_angles(self, angles: Sequence[float], speed: int) -> bool:
        '''
            Commands joint positioning.

            :param angles: Sequence of 6 joint angles in degrees.
            :param speed: Operating velocity percentage.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        frame: MyCobotFrame = self._codec.pack_angles(angles, speed)

        return self._send_frame(frame)

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
        frame: MyCobotFrame = self._codec.pack_coords(coords, speed, mode)

        return self._send_frame(frame)

    def set_gripper(self, state: int, speed: int) -> bool:
        '''
            Commands end-effector gripper state.

            :param state: Gripper state (1=grip, 0=release).
            :param speed: Operating velocity percentage.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        frame: MyCobotFrame = self._codec.pack_gripper(state, speed)

        return self._send_frame(frame)

    def power(self, on: bool) -> bool:
        '''
            Toggles servo power on or release.

            :param on: True to power on, False to release servos.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        frame: MyCobotFrame = self._codec.pack_power() if on else self._codec.pack_relax()

        return self._send_frame(frame)

    def home(self, speed: int) -> bool:
        '''
            Moves manipulator to zero home position.

            :param speed: Movement velocity percentage.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        frame: MyCobotFrame = self._codec.pack_angles([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], speed)

        return self._send_frame(frame)

    def read_angles(self) -> Sequence[float] | None:
        '''
            Queries current joint angles from hardware.

            :return: Sequence of 6 angles in degrees, or None if unavailable.
            :exceptions: None.
        '''
        if not self._transport.is_open():
            return None

        query_frame: MyCobotFrame = self._codec.pack_get_angles()

        if not self._send_frame(query_frame):
            return None

        resp: bytes = self._transport.read(self._constants.full_angles_response_len)
        prefix_len: int = 4
        payload_end: int = (
            prefix_len + self._constants.min_angles_response_len
        )

        if (
            len(resp) >= self._constants.min_angles_frame_len
            and resp[0] == self._constants.header_byte_1
            and resp[1] == self._constants.header_byte_2
        ):
            payload: bytes = resp[prefix_len:payload_end]
            return self._codec.unpack_angles(payload)

        return None
