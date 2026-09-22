# -*- coding: UTF-8 -*-

'''
Module
    bounds_loader.py
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
    Defines BoundsLoader for loading and assembling robot kinematic boundaries from config.
'''

from __future__ import annotations

from json import loads
from os.path import abspath, dirname, exists, join

from idecobot.core.model.kinematics.joint_bounds import JointBounds
from idecobot.core.model.kinematics.joint_limit import JointLimit
from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds
from idecobot.core.model.kinematics.spatial_bounds import SpatialBounds
from idecobot.core.model.kinematics.speed_bounds import SpeedBounds
from idecobot.core.model.kinematics.trajectory_bounds import TrajectoryBounds
from idecobot.setup.keys import IDECobotBundleKeys
from idecobot.setup.options import IDECobotBundleOptions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BoundsLoader:
    '''
        Loads and constructs MyCobotBounds domain model from JSON geometry configuration.

        It defines:

            :attributes:
                | _default_geometry_file - Default path to robot geometry configuration file.
            :methods:
                | get_default_config_path - Returns default path to geometry configuration.
                | load - Loads geometry JSON and constructs composed MyCobotBounds.
    '''

    _default_geometry_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'mycobot_geometry.json'
    )

    @classmethod
    def get_default_config_path(cls) -> str:
        '''
            Returns default file path to robot geometry configuration.

            :return: Absolute path to default geometry config file.
            :exceptions: None.
        '''
        return cls._default_geometry_file

    @classmethod
    def load(cls, options: IDECobotBundleOptions | None = None) -> MyCobotBounds:
        '''
            Loads geometry configuration file and constructs MyCobotBounds domain model.

            :param options: Optional bundle configuration options containing robot config path.
            :return: Fully initialized MyCobotBounds domain model.
            :exceptions: None.
        '''
        config_path: str = cls._default_geometry_file

        if options and IDECobotBundleKeys.OPTION_ROBOT_CONFIG in options:
            config_path = str(options[IDECobotBundleKeys.OPTION_ROBOT_CONFIG])

        data: dict[str, object] = {}

        if exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as handle:
                    data = loads(handle.read())

            except (OSError, ValueError):
                data = {}

        joints: JointBounds = JointBounds(
            j1=JointLimit(
                min_deg=float(data.get('j1_min_deg', -165.0)),
                max_deg=float(data.get('j1_max_deg', 165.0))
            ),
            j2=JointLimit(
                min_deg=float(data.get('j2_min_deg', -165.0)),
                max_deg=float(data.get('j2_max_deg', 165.0))
            ),
            j3=JointLimit(
                min_deg=float(data.get('j3_min_deg', -165.0)),
                max_deg=float(data.get('j3_max_deg', 165.0))
            ),
            j4=JointLimit(
                min_deg=float(data.get('j4_min_deg', -165.0)),
                max_deg=float(data.get('j4_max_deg', 165.0))
            ),
            j5=JointLimit(
                min_deg=float(data.get('j5_min_deg', -165.0)),
                max_deg=float(data.get('j5_max_deg', 165.0))
            ),
            j6=JointLimit(
                min_deg=float(data.get('j6_min_deg', -175.0)),
                max_deg=float(data.get('j6_max_deg', 175.0))
            )
        )
        spatial: SpatialBounds = SpatialBounds(
            max_reach_mm=float(data.get('max_reach_mm', 285.0)),
            min_z_mm=float(data.get('min_z_mm', -10.0))
        )
        speed: SpeedBounds = SpeedBounds(
            min_speed=int(data.get('min_speed', 1)),
            max_speed=int(data.get('max_speed', 100)),
            default_speed=int(data.get('default_speed', 30))
        )
        trajectory: TrajectoryBounds = TrajectoryBounds(
            max_jerk_deg=float(data.get('max_jerk_deg', 60.0))
        )

        return MyCobotBounds(
            joints=joints,
            spatial=spatial,
            speed=speed,
            trajectory=trajectory
        )
