# -*- coding: UTF-8 -*-

'''
Module
    mycobot_bounds.py
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
    Defines MyCobotBounds domain model for 6-DOF robotic manipulator physical limits.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MyCobotBounds:
    '''
        Defines physical mechanical and kinematic boundaries for myCobot 280.

        It defines:

            :attributes:
                | j1_min_deg - Minimum angle limit for Joint 1 in degrees.
                | j1_max_deg - Maximum angle limit for Joint 1 in degrees.
                | j2_min_deg - Minimum angle limit for Joint 2 in degrees.
                | j2_max_deg - Maximum angle limit for Joint 2 in degrees.
                | j3_min_deg - Minimum angle limit for Joint 3 in degrees.
                | j3_max_deg - Maximum angle limit for Joint 3 in degrees.
                | j4_min_deg - Minimum angle limit for Joint 4 in degrees.
                | j4_max_deg - Maximum angle limit for Joint 4 in degrees.
                | j5_min_deg - Minimum angle limit for Joint 5 in degrees.
                | j5_max_deg - Maximum angle limit for Joint 5 in degrees.
                | j6_min_deg - Minimum angle limit for Joint 6 in degrees.
                | j6_max_deg - Maximum angle limit for Joint 6 in degrees.
                | max_reach_mm - Maximum spherical reach radius in millimeters.
                | min_z_mm - Minimum vertical table safety threshold in millimeters.
                | max_jerk_deg - Maximum single step angular jump warning threshold in degrees.
                | min_speed - Minimum allowable operating speed percentage.
                | max_speed - Maximum allowable operating speed percentage.
                | default_speed - Default operating speed percentage.
            :methods:
                | from_dict - Constructs bounds from dictionary with default fallbacks.
                | is_joint_in_range - Verifies if a given joint angle is within bounds.
                | is_speed_in_range - Verifies if speed percentage is within allowed limits.
                | is_z_safe - Verifies if vertical coordinate satisfies table safety threshold.
    '''

    j1_min_deg: float = -165.0
    j1_max_deg: float = 165.0
    j2_min_deg: float = -165.0
    j2_max_deg: float = 165.0
    j3_min_deg: float = -165.0
    j3_max_deg: float = 165.0
    j4_min_deg: float = -165.0
    j4_max_deg: float = 165.0
    j5_min_deg: float = -165.0
    j5_max_deg: float = 165.0
    j6_min_deg: float = -175.0
    j6_max_deg: float = 175.0
    max_reach_mm: float = 285.0
    min_z_mm: float = -10.0
    max_jerk_deg: float = 60.0
    min_speed: int = 1
    max_speed: int = 100
    default_speed: int = 30

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> MyCobotBounds:
        '''
            Constructs MyCobotBounds from dictionary with default fallbacks.

            :param data: Dictionary containing mechanical boundary parameters.
            :return: Constructed MyCobotBounds instance.
            :exceptions: None.
        '''
        return cls(
            j1_min_deg=float(data.get('j1_min_deg', -165.0)),
            j1_max_deg=float(data.get('j1_max_deg', 165.0)),
            j2_min_deg=float(data.get('j2_min_deg', -165.0)),
            j2_max_deg=float(data.get('j2_max_deg', 165.0)),
            j3_min_deg=float(data.get('j3_min_deg', -165.0)),
            j3_max_deg=float(data.get('j3_max_deg', 165.0)),
            j4_min_deg=float(data.get('j4_min_deg', -165.0)),
            j4_max_deg=float(data.get('j4_max_deg', 165.0)),
            j5_min_deg=float(data.get('j5_min_deg', -165.0)),
            j5_max_deg=float(data.get('j5_max_deg', 165.0)),
            j6_min_deg=float(data.get('j6_min_deg', -175.0)),
            j6_max_deg=float(data.get('j6_max_deg', 175.0)),
            max_reach_mm=float(data.get('max_reach_mm', 285.0)),
            min_z_mm=float(data.get('min_z_mm', -10.0)),
            max_jerk_deg=float(data.get('max_jerk_deg', 60.0)),
            min_speed=int(data.get('min_speed', 1)),
            max_speed=int(data.get('max_speed', 100)),
            default_speed=int(data.get('default_speed', 30))
        )

    def is_joint_in_range(self, joint_id: int, angle: float) -> bool:
        '''
            Verifies if a given joint angle is within mechanical limits.

            :param joint_id: Joint index from 1 to 6.
            :param angle: Target angle in degrees.
            :return: True if within range, False otherwise.
            :exceptions: None.
        '''
        match joint_id:
            case 1:
                return self.j1_min_deg <= angle <= self.j1_max_deg
            case 2:
                return self.j2_min_deg <= angle <= self.j2_max_deg
            case 3:
                return self.j3_min_deg <= angle <= self.j3_max_deg
            case 4:
                return self.j4_min_deg <= angle <= self.j4_max_deg
            case 5:
                return self.j5_min_deg <= angle <= self.j5_max_deg
            case 6:
                return self.j6_min_deg <= angle <= self.j6_max_deg
            case _:
                return False

    def is_speed_in_range(self, speed: int) -> bool:
        '''
            Verifies if a given speed percentage is within allowed limits.

            :param speed: Speed percentage integer.
            :return: True if within bounds, False otherwise.
            :exceptions: None.
        '''
        return self.min_speed <= speed <= self.max_speed

    def is_z_safe(self, z_mm: float) -> bool:
        '''
            Verifies if vertical coordinate satisfies table safety threshold.

            :param z_mm: Vertical height coordinate in millimeters.
            :return: True if above safety limit, False otherwise.
            :exceptions: None.
        '''
        return z_mm >= self.min_z_mm
