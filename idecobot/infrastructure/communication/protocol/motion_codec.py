# -*- coding: UTF-8 -*-

'''
Module
    motion_codec.py
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
    Defines MotionCodec packing and unpacking joint angles and Cartesian coordinates.
'''

from __future__ import annotations

from collections.abc import Sequence
from struct import pack, unpack

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCodec:
    '''
        Encodes and decodes robot kinematic motion parameters to/from binary payloads.

        It defines:

            :attributes:
                | _constants - Injected ProtocolConstants low-level framing parameters.
            :methods:
                | __init__ - Initializes motion codec with protocol constants.
                | pack_angles - Assembles SEND_ANGLES binary frame from joint angles.
                | pack_coords - Assembles SEND_COORDS binary frame from Cartesian coordinates.
                | unpack_angles - Decodes raw response payload into joint angles tuple.
                | unpack_coords - Decodes raw response payload into Cartesian coordinates tuple.
                | get_version - Returns motion codec component version string.
    '''

    _constants: ProtocolConstants

    def __init__(self, constants: ProtocolConstants) -> None:
        '''
            Initializes MotionCodec with protocol constants.

            :param constants: Injected ProtocolConstants instance.
            :exceptions: None.
        '''
        self._constants = constants

    def pack_angles(self, angles: Sequence[float], speed: int) -> MyCobotFrame:
        '''
            Assembles SEND_ANGLES binary frame.

            :param angles: Sequence of 6 joint angles in degrees.
            :param speed: Operating velocity percentage (1-100).
            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''
        scaled: list[int] = [
            int(round(a * self._constants.angle_scale_factor)) for a in angles[:6]
        ]

        while len(scaled) < 6:
            scaled.append(0)

        payload: bytes = pack(
            self._constants.format_angles_command,
            scaled[0], scaled[1], scaled[2],
            scaled[3], scaled[4], scaled[5],
            speed & self._constants.byte_mask
        )

        return MyCobotFrame(
            self._constants.cmd_send_angles,
            payload,
            self._constants.default_frame_delay
        )

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
        scaled: list[int] = [
            int(round(c * self._constants.coord_scale_factor)) if i < 3
            else int(round(c * self._constants.angle_scale_factor))
            for i, c in enumerate(coords[:6])
        ]

        while len(scaled) < 6:
            scaled.append(0)

        payload: bytes = pack(
            self._constants.format_coords_command,
            scaled[0], scaled[1], scaled[2],
            scaled[3], scaled[4], scaled[5],
            speed & self._constants.byte_mask,
            mode & self._constants.byte_mask
        )

        return MyCobotFrame(
            self._constants.cmd_send_coords,
            payload,
            self._constants.default_frame_delay
        )

    def unpack_angles(
        self,
        payload: bytes
    ) -> tuple[float, float, float, float, float, float] | None:
        '''
            Decodes raw response payload into joint angles.

            :param payload: Binary response bytes from robot.
            :return: Tuple of 6 angles in degrees, or None if invalid.
            :exceptions: None.
        '''
        if len(payload) < self._constants.min_angles_response_len:
            return None

        raw_vals: tuple[int, ...] = unpack(
            self._constants.format_joints_payload,
            payload[:self._constants.min_angles_response_len]
        )
        factor: float = self._constants.angle_scale_factor

        return (
            raw_vals[0] / factor,
            raw_vals[1] / factor,
            raw_vals[2] / factor,
            raw_vals[3] / factor,
            raw_vals[4] / factor,
            raw_vals[5] / factor
        )

    def unpack_coords(
        self,
        payload: bytes
    ) -> tuple[float, float, float, float, float, float] | None:
        '''
            Decodes raw response payload into coordinates.

            :param payload: Binary response bytes from robot.
            :return: Tuple of 6 coordinates [X, Y, Z, Rx, Ry, Rz], or None if invalid.
            :exceptions: None.
        '''
        if len(payload) < self._constants.min_angles_response_len:
            return None

        raw_vals: tuple[int, ...] = unpack(
            self._constants.format_joints_payload,
            payload[:self._constants.min_angles_response_len]
        )
        coord_factor: float = self._constants.coord_scale_factor
        angle_factor: float = self._constants.angle_scale_factor

        return (
            raw_vals[0] / coord_factor,
            raw_vals[1] / coord_factor,
            raw_vals[2] / coord_factor,
            raw_vals[3] / angle_factor,
            raw_vals[4] / angle_factor,
            raw_vals[5] / angle_factor
        )

    def get_version(self) -> str:
        '''
            Returns the motion codec component version string.

            :return: The component version string.
            :exceptions: None.
        '''
        return __version__
