# -*- coding: UTF-8 -*-

'''
Module
    bounds_loader_test.py
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
    Unit tests for BoundsLoader geometry configuration loading.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds
from idecobot.setup.bounds_loader import BoundsLoader
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


class TestBoundsLoader(TestCase):
    '''
        Test cases for BoundsLoader configuration reading and domain assembly.

        It defines:

            :methods:
                | test_default_load - Tests loading from default configuration file.
                | test_get_default_config_path - Tests retrieval of default configuration path.
                | test_missing_config_fallback - Tests fallback to safe default boundaries.
    '''

    def test_default_load(self) -> None:
        '''
            Tests loading boundaries from default geometry configuration.
        '''
        bounds: MyCobotBounds = BoundsLoader.load()
        self.assertIsNotNone(bounds)
        self.assertEqual(bounds.joints.j1.min_deg, -165.0)
        self.assertEqual(bounds.joints.j1.max_deg, 165.0)
        self.assertEqual(bounds.joints.j6.min_deg, -175.0)
        self.assertEqual(bounds.joints.j6.max_deg, 175.0)
        self.assertEqual(bounds.spatial.max_reach_mm, 285.0)
        self.assertEqual(bounds.spatial.min_z_mm, -10.0)
        self.assertEqual(bounds.speed.min_speed, 1)
        self.assertEqual(bounds.speed.max_speed, 100)
        self.assertEqual(bounds.speed.default_speed, 30)
        self.assertEqual(bounds.trajectory.max_jerk_deg, 60.0)

    def test_get_default_config_path(self) -> None:
        '''
            Tests retrieval of default configuration path string.
        '''
        path: str = BoundsLoader.get_default_config_path()
        self.assertTrue(path.endswith('mycobot_geometry.json'))

    def test_missing_config_fallback(self) -> None:
        '''
            Tests fallback values when configuration file path does not exist.
        '''
        options: IDECobotBundleOptions = {
            IDECobotBundleKeys.OPTION_ROBOT_CONFIG: '/non/existent/path.json'
        }
        bounds: MyCobotBounds = BoundsLoader.load(options=options)
        self.assertIsNotNone(bounds)
        self.assertEqual(bounds.speed.default_speed, 30)


if __name__ == '__main__':
    main()
