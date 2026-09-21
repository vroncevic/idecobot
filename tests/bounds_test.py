# -*- coding: UTF-8 -*-

'''
Module
    test_bounds.py
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
    Unit tests for MyCobotBounds domain model.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMyCobotBounds(TestCase):
    '''
        Test cases for MyCobotBounds physical limit checks.

        It defines:

            :methods:
                | test_default_values - Tests default bounds parameters.
                | test_joint_range_checks - Tests angular range enforcement.
                | test_invalid_joint_id - Tests out-of-range joint index handling.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.bounds = MyCobotBounds()

    def test_default_values(self) -> None:
        '''
            Tests default boundary limits.
        '''
        self.assertEqual(self.bounds.j1_min_deg, -165.0)
        self.assertEqual(self.bounds.j1_max_deg, 165.0)
        self.assertEqual(self.bounds.j6_min_deg, -175.0)
        self.assertEqual(self.bounds.j6_max_deg, 175.0)
        self.assertEqual(self.bounds.max_reach_mm, 285.0)
        self.assertEqual(self.bounds.min_z_mm, -10.0)

    def test_joint_range_checks(self) -> None:
        '''
            Tests valid and invalid angles for all joints.
        '''
        for j_id in range(1, 6):
            self.assertTrue(self.bounds.is_joint_in_range(j_id, 0.0))
            self.assertTrue(self.bounds.is_joint_in_range(j_id, 165.0))
            self.assertTrue(self.bounds.is_joint_in_range(j_id, -165.0))
            self.assertFalse(self.bounds.is_joint_in_range(j_id, 166.0))
            self.assertFalse(self.bounds.is_joint_in_range(j_id, -166.0))

        self.assertTrue(self.bounds.is_joint_in_range(6, 175.0))
        self.assertTrue(self.bounds.is_joint_in_range(6, -175.0))
        self.assertFalse(self.bounds.is_joint_in_range(6, 176.0))

    def test_invalid_joint_id(self) -> None:
        '''
            Tests checking bounds for non-existent joint id.
        '''
        self.assertFalse(self.bounds.is_joint_in_range(0, 0.0))
        self.assertFalse(self.bounds.is_joint_in_range(7, 0.0))

    def test_speed_and_z_checks(self) -> None:
        '''
            Tests speed percentage and vertical table safety checks.
        '''
        self.assertTrue(self.bounds.is_speed_in_range(1))
        self.assertTrue(self.bounds.is_speed_in_range(50))
        self.assertTrue(self.bounds.is_speed_in_range(100))
        self.assertFalse(self.bounds.is_speed_in_range(0))
        self.assertFalse(self.bounds.is_speed_in_range(101))

        self.assertTrue(self.bounds.is_z_safe(0.0))
        self.assertTrue(self.bounds.is_z_safe(-10.0))
        self.assertFalse(self.bounds.is_z_safe(-10.1))

    def test_from_dict_defaults(self) -> None:
        '''
            Verifies MyCobotBounds.from_dict fallback to defaults on empty dict.
        '''
        bounds = MyCobotBounds.from_dict({})
        self.assertEqual(bounds.j1_min_deg, -165.0)
        self.assertEqual(bounds.j1_max_deg, 165.0)
        self.assertEqual(bounds.j6_min_deg, -175.0)
        self.assertEqual(bounds.j6_max_deg, 175.0)
        self.assertEqual(bounds.max_reach_mm, 285.0)
        self.assertEqual(bounds.min_z_mm, -10.0)
        self.assertEqual(bounds.max_jerk_deg, 60.0)
        self.assertEqual(bounds.min_speed, 1)
        self.assertEqual(bounds.max_speed, 100)
        self.assertEqual(bounds.default_speed, 30)

    def test_from_dict_custom(self) -> None:
        '''
            Verifies MyCobotBounds.from_dict overrides specific fields when provided.
        '''
        custom_data: dict[str, object] = {
            'j1_min_deg': -120.0,
            'j1_max_deg': 120.0,
            'max_reach_mm': 250.0,
            'min_z_mm': 0.0,
            'default_speed': 20
        }
        bounds = MyCobotBounds.from_dict(custom_data)
        self.assertAlmostEqual(bounds.j1_min_deg, -120.0)
        self.assertAlmostEqual(bounds.j1_max_deg, 120.0)
        self.assertAlmostEqual(bounds.max_reach_mm, 250.0)
        self.assertAlmostEqual(bounds.min_z_mm, 0.0)
        self.assertEqual(bounds.default_speed, 20)
        self.assertEqual(bounds.j2_min_deg, -165.0)
        self.assertEqual(bounds.j6_max_deg, 175.0)


if __name__ == '__main__':
    main()
