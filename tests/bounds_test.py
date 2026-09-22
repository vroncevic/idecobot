# -*- coding: UTF-8 -*-

'''
Module
    bounds_test.py
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
    Unit tests for decomposed MyCobotBounds pure data model and KinematicValidator.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from idecobot.core.model.kinematics.joint_bounds import JointBounds
from idecobot.core.model.kinematics.joint_limit import JointLimit
from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds
from idecobot.core.model.kinematics.spatial_bounds import SpatialBounds
from idecobot.core.model.kinematics.speed_bounds import SpeedBounds
from idecobot.core.model.kinematics.trajectory_bounds import TrajectoryBounds
from idecobot.core.service.kinematics.kinematic_validator import KinematicValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMyCobotBounds(TestCase):
    '''
        Test cases for decomposed MyCobotBounds pure data models and KinematicValidator checks.

        It defines:

            :methods:
                | setUp - Sets up test fixture with decomposed bounds and validator.
                | test_bounds_attributes - Tests pure dataclass attributes.
                | test_bounds_immutability - Verifies frozen instance immutability.
                | test_joint_range_checks - Tests angular range enforcement.
                | test_invalid_joint_id - Tests out-of-range joint index handling.
                | test_speed_and_z_checks - Tests speed and Z coordinate safety.
                | test_reach_safe - Tests 3D Cartesian reach envelope checks.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with decomposed bounds and validator.
        '''
        self.joints = JointBounds(
            j1=JointLimit(min_deg=-165.0, max_deg=165.0),
            j2=JointLimit(min_deg=-165.0, max_deg=165.0),
            j3=JointLimit(min_deg=-165.0, max_deg=165.0),
            j4=JointLimit(min_deg=-165.0, max_deg=165.0),
            j5=JointLimit(min_deg=-165.0, max_deg=165.0),
            j6=JointLimit(min_deg=-175.0, max_deg=175.0)
        )
        self.spatial = SpatialBounds(max_reach_mm=285.0, min_z_mm=-10.0)
        self.speed = SpeedBounds(min_speed=1, max_speed=100, default_speed=30)
        self.trajectory = TrajectoryBounds(max_jerk_deg=60.0)
        self.bounds = MyCobotBounds(
            joints=self.joints,
            spatial=self.spatial,
            speed=self.speed,
            trajectory=self.trajectory
        )
        self.validator = KinematicValidator(bounds=self.bounds)

    def test_bounds_attributes(self) -> None:
        '''
            Tests pure dataclass attributes on decomposed MyCobotBounds.
        '''
        self.assertEqual(self.bounds.joints.j1.min_deg, -165.0)
        self.assertEqual(self.bounds.joints.j1.max_deg, 165.0)
        self.assertEqual(self.bounds.joints.j6.min_deg, -175.0)
        self.assertEqual(self.bounds.joints.j6.max_deg, 175.0)
        self.assertEqual(self.bounds.spatial.max_reach_mm, 285.0)
        self.assertEqual(self.bounds.spatial.min_z_mm, -10.0)
        self.assertEqual(self.bounds.trajectory.max_jerk_deg, 60.0)
        self.assertEqual(self.bounds.speed.min_speed, 1)
        self.assertEqual(self.bounds.speed.max_speed, 100)
        self.assertEqual(self.bounds.speed.default_speed, 30)

    def test_bounds_immutability(self) -> None:
        '''
            Verifies MyCobotBounds and submodels are immutable and frozen.
        '''
        with self.assertRaises(FrozenInstanceError):
            setattr(self.bounds.speed, 'default_speed', 50)
        with self.assertRaises(FrozenInstanceError):
            setattr(self.bounds, 'speed', self.speed)

    def test_joint_range_checks(self) -> None:
        '''
            Tests valid and invalid angles for all joints via KinematicValidator.
        '''
        for j_id in range(1, 6):
            self.assertTrue(self.validator.is_joint_in_range(j_id, 0.0))
            self.assertTrue(self.validator.is_joint_in_range(j_id, 165.0))
            self.assertTrue(self.validator.is_joint_in_range(j_id, -165.0))
            self.assertFalse(self.validator.is_joint_in_range(j_id, 166.0))
            self.assertFalse(self.validator.is_joint_in_range(j_id, -166.0))

        self.assertTrue(self.validator.is_joint_in_range(6, 175.0))
        self.assertTrue(self.validator.is_joint_in_range(6, -175.0))
        self.assertFalse(self.validator.is_joint_in_range(6, 176.0))

    def test_invalid_joint_id(self) -> None:
        '''
            Tests joint index validation handles out-of-range IDs cleanly.
        '''
        self.assertFalse(self.validator.is_joint_in_range(0, 0.0))
        self.assertFalse(self.validator.is_joint_in_range(7, 0.0))
        self.assertFalse(self.validator.is_joint_in_range(-1, 0.0))

    def test_speed_and_z_checks(self) -> None:
        '''
            Tests speed percentage and Z table penetration validation.
        '''
        self.assertTrue(self.validator.is_speed_in_range(1))
        self.assertTrue(self.validator.is_speed_in_range(50))
        self.assertTrue(self.validator.is_speed_in_range(100))
        self.assertFalse(self.validator.is_speed_in_range(0))
        self.assertFalse(self.validator.is_speed_in_range(101))

        self.assertTrue(self.validator.is_z_safe(0.0))
        self.assertTrue(self.validator.is_z_safe(-10.0))
        self.assertTrue(self.validator.is_z_safe(200.0))
        self.assertFalse(self.validator.is_z_safe(-10.1))

    def test_reach_safe(self) -> None:
        '''
            Tests 3D spherical reach envelope boundary checks.
        '''
        self.assertTrue(self.validator.is_reach_safe(0.0, 0.0, 0.0))
        self.assertTrue(self.validator.is_reach_safe(200.0, 0.0, 0.0))
        self.assertTrue(self.validator.is_reach_safe(285.0, 0.0, 0.0))
        self.assertFalse(self.validator.is_reach_safe(285.1, 0.0, 0.0))
        self.assertFalse(self.validator.is_reach_safe(200.0, 200.0, 100.0))


if __name__ == '__main__':
    main()
