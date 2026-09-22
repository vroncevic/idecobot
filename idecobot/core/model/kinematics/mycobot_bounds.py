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
    Defines MyCobotBounds immutable domain model composed of kinematic boundary data.
'''

from __future__ import annotations

from dataclasses import dataclass

from idecobot.core.model.kinematics.joint_bounds import JointBounds
from idecobot.core.model.kinematics.spatial_bounds import SpatialBounds
from idecobot.core.model.kinematics.speed_bounds import SpeedBounds
from idecobot.core.model.kinematics.trajectory_bounds import TrajectoryBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MyCobotBounds:
    '''
        Defines physical mechanical and kinematic boundary data for myCobot 280.

        It defines:

            :attributes:
                | joints - Angular boundaries for all 6 joints.
                | spatial - Cartesian spatial boundary limits.
                | speed - Operating speed boundary limits.
                | trajectory - Trajectory and motion smoothness limits.
    '''

    joints: JointBounds
    spatial: SpatialBounds
    speed: SpeedBounds
    trajectory: TrajectoryBounds
