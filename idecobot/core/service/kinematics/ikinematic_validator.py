# -*- coding: UTF-8 -*-

'''
Module
    ikinematic_validator.py
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
    Defines structural interface protocol for robotic kinematics validation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IKinematicValidator(Protocol):
    '''
        Defines protocol IKinematicValidator for robot boundary validation.

        It defines:

            :methods:
                | is_joint_in_range - Verifies if a given joint angle is within mechanical limits.
                | is_speed_in_range - Verifies if speed percentage is within allowed limits.
                | is_z_safe - Verifies if vertical coordinate satisfies table safety threshold.
                | is_reach_safe - Verifies if Cartesian coordinates satisfy maximum radial reach.
                | get_version - Returns protocol version string.
    '''

    def is_joint_in_range(self, joint_id: int, angle: float) -> bool:
        '''
            Verifies if a given joint angle is within mechanical limits.

            :param joint_id: Joint index from 1 to 6.
            :param angle: Target angle in degrees.
            :return: True if within range, False otherwise.
            :exceptions: None.
        '''

    def is_speed_in_range(self, speed: int) -> bool:
        '''
            Verifies if a given speed percentage is within allowed limits.

            :param speed: Speed percentage integer.
            :return: True if within bounds, False otherwise.
            :exceptions: None.
        '''

    def is_z_safe(self, z_mm: float) -> bool:
        '''
            Verifies if vertical coordinate satisfies table safety threshold.

            :param z_mm: Vertical height coordinate in millimeters.
            :return: True if above safety limit, False otherwise.
            :exceptions: None.
        '''

    def is_reach_safe(self, x: float, y: float, z: float) -> bool:
        '''
            Verifies if 3D Cartesian coordinates are within maximum radial reach.

            :param x: X coordinate in millimeters.
            :param y: Y coordinate in millimeters.
            :param z: Z coordinate in millimeters.
            :return: True if reach distance is within limit, False otherwise.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
        '''

