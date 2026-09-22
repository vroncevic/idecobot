# -*- coding: UTF-8 -*-

'''
Module
    mycobot_protocol_codec.py
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
    Defines MyCobotProtocolCodec composite facade delegating to focused protocol components.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.infrastructure.communication.protocol.imotion_codec import IMotionCodec
from idecobot.infrastructure.communication.protocol.iprotocol_framer import IProtocolFramer
from idecobot.infrastructure.communication.protocol.isystem_codec import ISystemCodec
from idecobot.infrastructure.communication.protocol.itool_codec import IToolCodec

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotProtocolCodec:
    '''
        Composite facade encoding and decoding binary frames for Elephant Robotics myCobot manipulator.

        It defines:

            :attributes:
                | _framer - Injected IProtocolFramer wire framing component.
                | _motion - Injected IMotionCodec kinematics packing component.
                | _tool - Injected IToolCodec gripper and end-effector component.
                | _system - Injected ISystemCodec power and query component.
            :methods:
                | __init__ - Initializes facade with injected protocol components.
                | framer - Property returning injected IProtocolFramer.
                | encode_frame - Encodes MyCobotFrame into complete binary packet.
                | format_hex - Formats binary frame as uppercase hex string.
                | pack_angles - Assembles SEND_ANGLES binary frame.
                | pack_coords - Assembles SEND_COORDS binary frame.
                | pack_gripper - Assembles SET_GRIPPER binary frame.
                | pack_relax - Assembles RELEASE_SERVOS binary frame.
                | pack_power - Assembles POWER_ON binary frame.
                | pack_get_angles - Assembles GET_ANGLES query frame.
                | unpack_angles - Decodes raw response payload into joint angles.
                | unpack_coords - Decodes raw response payload into coordinates.
                | get_version - Returns protocol codec version string.
    '''

    def __init__(
        self,
        framer: IProtocolFramer,
        motion: IMotionCodec,
        tool: IToolCodec,
        system: ISystemCodec
    ) -> None:
        '''
            Initializes facade with injected protocol components.

            :param framer: Injected protocol framer component.
            :param motion: Injected motion codec component.
            :param tool: Injected tool codec component.
            :param system: Injected system codec component.
            :exceptions: None.
        '''
        self._framer: IProtocolFramer = framer
        self._motion: IMotionCodec = motion
        self._tool: IToolCodec = tool
        self._system: ISystemCodec = system

    @property
    def framer(self) -> IProtocolFramer:
        '''
            Returns injected protocol framer.

            :return: Injected IProtocolFramer instance.
        '''
        return self._framer

    def encode_frame(self, frame: MyCobotFrame) -> bytes:
        '''
            Serializes MyCobotFrame into full binary packet with header, length, cmd ID, and footer.

            :param frame: Injected MyCobotFrame data model.
            :return: Complete serialized binary packet as bytes.
            :exceptions: None.
        '''
        return self._framer.encode_frame(frame)

    def format_hex(self, frame: MyCobotFrame) -> str:
        '''
            Formats binary frame as uppercase space-separated hex string.

            :param frame: Injected MyCobotFrame data model.
            :return: Hexadecimal representation string.
            :exceptions: None.
        '''
        return self._framer.format_hex(frame)

    def extract_response_payload(
        self,
        raw_bytes: bytes,
        min_frame_len: int,
        prefix_len: int,
        payload_len: int
    ) -> bytes | None:
        '''
            Extracts validated payload from robot raw response bytes.

            :param raw_bytes: Raw bytes received from robot.
            :param min_frame_len: Minimum acceptable length for frame.
            :param prefix_len: Header length prefix offset.
            :param payload_len: Expected length of payload.
            :return: Validated payload bytes, or None if invalid.
            :exceptions: None.
        '''
        return self._framer.extract_response_payload(
            raw_bytes, min_frame_len, prefix_len, payload_len
        )

    def pack_angles(self, angles: Sequence[float], speed: int) -> MyCobotFrame:
        '''
            Assembles SEND_ANGLES binary frame.

            :param angles: Sequence of 6 joint angles in degrees.
            :param speed: Operating velocity percentage (1-100).
            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''
        return self._motion.pack_angles(angles, speed)

    def pack_coords(
        self,
        coords: Sequence[float],
        speed: int,
        mode: int = 0
    ) -> MyCobotFrame:
        '''
            Assembles SEND_COORDS binary frame.

            :param coords: Sequence of 6 Cartesian values [X, Y, Z, Rx, Ry, Rz].
            :param speed: Operating velocity percentage (1-100).
            :param mode: Coordinate mode (0=linear, 1=angular).
            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''
        return self._motion.pack_coords(coords, speed, mode)

    def pack_gripper(self, state: int, speed: int) -> MyCobotFrame:
        '''
            Assembles SET_GRIPPER binary frame.

            :param state: Gripper state (1=grip, 0=release).
            :param speed: Operating velocity percentage.
            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''
        return self._tool.pack_gripper(state, speed)

    def pack_relax(self) -> MyCobotFrame:
        '''
            Assembles RELEASE_SERVOS binary frame.

            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''
        return self._system.pack_relax()

    def pack_power(self) -> MyCobotFrame:
        '''
            Assembles POWER_ON binary frame.

            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''
        return self._system.pack_power()

    def pack_get_angles(self) -> MyCobotFrame:
        '''
            Assembles GET_ANGLES query frame.

            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''
        return self._system.pack_get_angles()

    def unpack_angles(self, payload: bytes) -> tuple[float, float, float, float, float, float] | None:
        '''
            Decodes raw response payload into joint angles.

            :param payload: Binary response bytes from robot.
            :return: Tuple of 6 angles in degrees, or None if invalid.
            :exceptions: None.
        '''
        return self._motion.unpack_angles(payload)

    def unpack_coords(self, payload: bytes) -> tuple[float, float, float, float, float, float] | None:
        '''
            Decodes raw response payload into coordinates.

            :param payload: Binary response bytes from robot.
            :return: Tuple of 6 coordinates [X, Y, Z, Rx, Ry, Rz], or None if invalid.
            :exceptions: None.
        '''
        return self._motion.unpack_coords(payload)

    def get_version(self) -> str:
        '''
            Returns the protocol codec component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
