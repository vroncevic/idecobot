# -*- coding: UTF-8 -*-

'''
Module
    imycobot_protocol_codec.py
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
    Defines structural interface protocol for binary serial protocol encoding and decoding.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMyCobotProtocolCodec(Protocol):
    '''
        Defines structural interface protocol for encoding and decoding binary robot frames.

        It defines:

            :methods:
                | encode_frame - Formats a MyCobotFrame into wire-ready binary packet.
                | format_hex - Formats binary encoded frame as space-separated hexadecimal string.
                | extract_response_payload - Extracts validated payload from raw response bytes.
                | pack_angles - Assembles SEND_ANGLES binary frame.
                | pack_coords - Assembles SEND_COORDS binary frame.
                | pack_gripper - Assembles SET_GRIPPER binary frame.
                | pack_relax - Assembles RELEASE_SERVOS binary frame.
                | pack_power - Assembles POWER_ON binary frame.
                | pack_get_angles - Assembles GET_ANGLES query frame.
                | unpack_angles - Decodes raw response payload into joint angles.
                | unpack_coords - Decodes raw response payload into coordinates.
                | get_version - Returns protocol codec component version string.
    '''

    def encode_frame(self, frame: MyCobotFrame) -> bytes:
        '''
            Formats a MyCobotFrame into wire-ready binary packet.

            :param frame: Frame containing command ID and payload.
            :return: Serialized binary packet ready for transmission.
        '''

    def format_hex(self, frame: MyCobotFrame) -> str:
        '''
            Formats binary encoded frame as space-separated hexadecimal string.

            :param frame: MyCobotFrame instance.
            :return: Hexadecimal string representation.
        '''

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
        '''


    def pack_angles(self, angles: Sequence[float], speed: int) -> MyCobotFrame:
        '''
            Assembles SEND_ANGLES binary frame.

            :param angles: Sequence of 6 joint angles in degrees.
            :param speed: Operating velocity percentage (1-100).
            :return: Serialized MyCobotFrame instance.
        '''

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
        '''

    def pack_gripper(self, state: int, speed: int) -> MyCobotFrame:
        '''
            Assembles SET_GRIPPER binary frame.

            :param state: Gripper state (1=grip, 0=release).
            :param speed: Operating velocity percentage.
            :return: Serialized MyCobotFrame instance.
        '''

    def pack_relax(self) -> MyCobotFrame:
        '''
            Assembles RELEASE_SERVOS binary frame.

            :return: Serialized MyCobotFrame instance.
        '''

    def pack_power(self) -> MyCobotFrame:
        '''
            Assembles POWER_ON binary frame.

            :return: Serialized MyCobotFrame instance.
        '''

    def pack_get_angles(self) -> MyCobotFrame:
        '''
            Assembles GET_ANGLES query frame.

            :return: Serialized MyCobotFrame instance.
        '''

    def unpack_angles(
        self,
        payload: bytes
    ) -> tuple[float, float, float, float, float, float] | None:
        '''
            Decodes raw response payload into joint angles.

            :param payload: Binary response bytes from robot.
            :return: Tuple of 6 angles in degrees, or None if invalid.
        '''

    def unpack_coords(
        self,
        payload: bytes
    ) -> tuple[float, float, float, float, float, float] | None:
        '''
            Decodes raw response payload into coordinates.

            :param payload: Binary response bytes from robot.
            :return: Tuple of 6 coordinates [X, Y, Z, Rx, Ry, Rz], or None if invalid.
        '''

    def get_version(self) -> str:
        '''
            Returns the protocol codec component version string.

            :return: Component version string.
        '''

