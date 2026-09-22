# -*- coding: UTF-8 -*-

'''
Module
    kinematic_validator.py
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
    Defines KinematicValidator implementing robot mechanical boundary validation.
'''

from __future__ import annotations

from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class KinematicValidator:
    '''
        Validates robot kinematics and Cartesian parameters against physical boundaries.

        It defines:

            :attributes:
                | _bounds - Injected MyCobotBounds physical boundaries data model.
                | _joint_limits - Precomputed tuple of min/max angles for joints 1 to 6.
            :methods:
                | __init__ - Initializes kinematic validator with boundary model.
                | is_joint_in_range - Verifies if a given joint angle is within mechanical limits.
                | is_speed_in_range - Verifies if speed percentage is within allowed limits.
                | is_z_safe - Verifies if vertical coordinate satisfies table safety threshold.
                | is_reach_safe - Verifies if Cartesian coordinates satisfy maximum radial reach.
                | get_version - Returns validator version string.
    '''

    _bounds: MyCobotBounds
    _joint_limits: tuple[tuple[float, float], ...]

    def __init__(self, bounds: MyCobotBounds) -> None:
        '''
            Initializes validator with injected boundary constraints.

            :param bounds: Injected MyCobotBounds data structure.
            :exceptions: None.
        '''
        self._bounds = bounds
        self._joint_limits = (
            (bounds.joints.j1.min_deg, bounds.joints.j1.max_deg),
            (bounds.joints.j2.min_deg, bounds.joints.j2.max_deg),
            (bounds.joints.j3.min_deg, bounds.joints.j3.max_deg),
            (bounds.joints.j4.min_deg, bounds.joints.j4.max_deg),
            (bounds.joints.j5.min_deg, bounds.joints.j5.max_deg),
            (bounds.joints.j6.min_deg, bounds.joints.j6.max_deg)
        )

    def is_joint_in_range(self, joint_id: int, angle: float) -> bool:
        '''
            Verifies if a given joint angle is within mechanical limits.

            :param joint_id: Joint index from 1 to 6.
            :param angle: Target angle in degrees.
            :return: True if within range, False otherwise.
            :exceptions: None.
        '''
        if not 1 <= joint_id <= 6:
            return False

        min_deg, max_deg = self._joint_limits[joint_id - 1]

        return min_deg <= angle <= max_deg

    def is_speed_in_range(self, speed: int) -> bool:
        '''
            Verifies if a given speed percentage is within allowed limits.

            :param speed: Speed percentage integer.
            :return: True if within bounds, False otherwise.
            :exceptions: None.
        '''
        return self._bounds.speed.min_speed <= speed <= self._bounds.speed.max_speed

    def is_z_safe(self, z_mm: float) -> bool:
        '''
            Verifies if vertical coordinate satisfies table safety threshold.

            :param z_mm: Vertical height coordinate in millimeters.
            :return: True if above safety limit, False otherwise.
            :exceptions: None.
        '''
        return z_mm >= self._bounds.spatial.min_z_mm

    def is_reach_safe(self, x: float, y: float, z: float) -> bool:
        '''
            Verifies if 3D Cartesian coordinates are within maximum radial reach.

            :param x: X coordinate in millimeters.
            :param y: Y coordinate in millimeters.
            :param z: Z coordinate in millimeters.
            :return: True if reach distance is within limit, False otherwise.
            :exceptions: None.
        '''
        return (x ** 2 + y ** 2 + z ** 2) ** 0.5 <= self._bounds.spatial.max_reach_mm

    def get_version(self) -> str:
        '''
            Returns validator version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

