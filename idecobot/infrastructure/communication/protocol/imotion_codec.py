# -*- coding: UTF-8 -*-

'''
Module
    imotion_codec.py
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
    Defines structural interface protocol for joint angle and Cartesian coordinate encoding/decoding.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMotionCodec(Protocol):
    '''
        Defines structural interface protocol for kinematic motion packing and unpacking.

        It defines:

            :methods:
                | pack_angles - Assembles SEND_ANGLES binary frame from joint angles.
                | pack_coords - Assembles SEND_COORDS binary frame from Cartesian coordinates.
                | unpack_angles - Decodes raw response payload into joint angles tuple.
                | unpack_coords - Decodes raw response payload into Cartesian coordinates tuple.
                | get_version - Returns motion codec component version string.
    '''

    def pack_angles(self, angles: Sequence[float], speed: int) -> MyCobotFrame:
        '''
            Assembles SEND_ANGLES binary frame.

            :param angles: Sequence of 6 joint angles in degrees.
            :param speed: Operating velocity percentage (1-100).
            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''

    def pack_coords(self, coords: Sequence[float], speed: int, mode: int = 0) -> MyCobotFrame:
        '''
            Assembles SEND_COORDS binary frame.

            :param coords: Sequence of 6 Cartesian values [X, Y, Z, Rx, Ry, Rz].
            :param speed: Operating velocity percentage (1-100).
            :param mode: Coordinate mode (0=linear, 1=angular).
            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''

    def unpack_angles(self, payload: bytes) -> tuple[float, float, float, float, float, float] | None:
        '''
            Decodes raw response payload into joint angles.

            :param payload: Binary response bytes from robot.
            :return: Tuple of 6 angles in degrees, or None if invalid.
            :exceptions: None.
        '''

    def unpack_coords(self, payload: bytes) -> tuple[float, float, float, float, float, float] | None:
        '''
            Decodes raw response payload into coordinates.

            :param payload: Binary response bytes from robot.
            :return: Tuple of 6 coordinates [X, Y, Z, Rx, Ry, Rz], or None if invalid.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the motion codec component version string.

            :return: Component version string.
            :exceptions: None.
        '''
