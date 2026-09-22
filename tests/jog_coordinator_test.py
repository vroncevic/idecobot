# -*- coding: UTF-8 -*-

'''
Module
    test_jog_coordinator.py
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
    Unit tests for JogCoordinator and JogConstants.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.kinematics.joint_bounds import JointBounds
from idecobot.core.model.kinematics.joint_limit import JointLimit
from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds
from idecobot.core.model.kinematics.spatial_bounds import SpatialBounds
from idecobot.core.model.kinematics.speed_bounds import SpeedBounds
from idecobot.core.model.kinematics.trajectory_bounds import TrajectoryBounds
from idecobot.core.service.kinematics.kinematic_validator import KinematicValidator
from idecobot.infrastructure.gui.jog.jog_constants import JogConstants
from idecobot.infrastructure.gui.jog.jog_coordinator import JogCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockController:
    '''
        Mock controller recording invocations for test verification.
    '''

    def __init__(self) -> None:
        '''
            Initializes mock controller recording states.
        '''
        self.last_angles: list[float] | None = None
        self.last_coords: list[float] | None = None
        self.last_speed: int = 0
        self.power_state: bool = False
        self.gripper_state: int = 0

    def send_angles(self, angles: list[float], speed: int) -> bool:
        '''
            Records angular motion parameters.
        '''
        self.last_angles = list(angles)
        self.last_speed = speed
        return True

    def send_coords(self, coords: list[float], speed: int) -> bool:
        '''
            Records Cartesian coordinate parameters.
        '''
        self.last_coords = list(coords)
        self.last_speed = speed
        return True

    def set_gripper(self, state: int, speed: int) -> bool:
        '''
            Records gripper state and actuation speed.
        '''
        self.gripper_state = state
        self.last_speed = speed
        return True

    def power(self, on: bool) -> bool:
        '''
            Records power switch status.
        '''
        self.power_state = on
        return True

    def home(self, speed: int) -> bool:
        '''
            Records homing motion execution.
        '''
        self.last_speed = speed
        return True

    def is_connected(self) -> bool:
        '''
            Reports simulated connectivity state.
        '''
        return True

    def get_angles(self) -> list[float] | None:
        '''
            Returns simulated current joint angles.
        '''
        return [0.0] * 6

    def get_coords(self) -> list[float] | None:
        '''
            Returns simulated current Cartesian coordinates.
        '''
        return [0.0] * 6

    def stop(self) -> bool:
        '''
            Records motion cancellation command.
        '''
        return True


class TestJogCoordinator(TestCase):
    '''
        Test cases for JogCoordinator motion coordination and boundary safety.

        It defines:

            :methods:
                | test_initial_state - Verifies default angles and coordinates.
                | test_jog_joint_valid - Tests successful joint jogging within limits.
                | test_jog_joint_out_of_bounds - Tests boundary violation rejection.
                | test_jog_cartesian_valid - Tests successful Cartesian axis jogging.
                | test_jog_cartesian_reach_limit - Tests reach violation rejection.
                | test_gripper_and_power - Tests gripper and power commands.
                | test_home_and_reset - Tests zero homing and position resetting.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with coordinator and mock controller.
        '''
        self.controller = MockController()
        self.bounds = MyCobotBounds(
            joints=JointBounds(
                j1=JointLimit(min_deg=-165.0, max_deg=165.0),
                j2=JointLimit(min_deg=-165.0, max_deg=165.0),
                j3=JointLimit(min_deg=-165.0, max_deg=165.0),
                j4=JointLimit(min_deg=-165.0, max_deg=165.0),
                j5=JointLimit(min_deg=-165.0, max_deg=165.0),
                j6=JointLimit(min_deg=-175.0, max_deg=175.0)
            ),
            spatial=SpatialBounds(max_reach_mm=285.0, min_z_mm=-10.0),
            speed=SpeedBounds(min_speed=1, max_speed=100, default_speed=30),
            trajectory=TrajectoryBounds(max_jerk_deg=60.0)
        )
        self.validator = KinematicValidator(bounds=self.bounds)
        self.constants = JogConstants()
        self.logs: list[str] = []
        self.coordinator = JogCoordinator(
            controller=self.controller,
            validator=self.validator,
            constants=self.constants,
            on_log=self.logs.append
        )

    def test_initial_state(self) -> None:
        '''
            Verifies default baseline positions from constants.
        '''
        self.assertEqual(self.coordinator.get_angles(), list(self.constants.default_angles))
        self.assertEqual(self.coordinator.get_coords(), list(self.constants.default_coords))

    def test_jog_joint_valid(self) -> None:
        '''
            Tests valid joint jog within safety limits.
        '''
        success: bool = self.coordinator.jog_joint(joint_id=1, sign=1.0, step=5.0, speed=30)
        self.assertTrue(success)
        self.assertEqual(self.coordinator.get_angles()[0], 5.0)
        self.assertEqual(self.controller.last_angles, [5.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    def test_jog_joint_out_of_bounds(self) -> None:
        '''
            Tests jog rejection when exceeding joint limits.
        '''
        success: bool = self.coordinator.jog_joint(joint_id=1, sign=1.0, step=200.0, speed=30)
        self.assertFalse(success)
        self.assertEqual(self.coordinator.get_angles()[0], 0.0)
        self.assertTrue(any('exceeds kinematic bounds' in msg for msg in self.logs))

    def test_jog_cartesian_valid(self) -> None:
        '''
            Tests valid Cartesian jog command.
        '''
        success: bool = self.coordinator.jog_cartesian(axis='X', sign=1.0, step=10.0, speed=30)
        self.assertTrue(success)
        self.assertEqual(self.coordinator.get_coords()[0], 10.0)

    def test_jog_cartesian_reach_limit(self) -> None:
        '''
            Tests Cartesian jog rejection when exceeding reach limit.
        '''
        success: bool = self.coordinator.jog_cartesian(axis='X', sign=1.0, step=500.0, speed=30)
        self.assertFalse(success)
        self.assertTrue(any('exceeds safe radius' in msg for msg in self.logs))

    def test_gripper_and_power(self) -> None:
        '''
            Tests gripper actuation and servo power toggle.
        '''
        self.assertTrue(self.coordinator.actuate_gripper(state=1, speed=50))
        self.assertEqual(self.controller.gripper_state, 1)

        self.assertTrue(self.coordinator.toggle_power(on=True))
        self.assertTrue(self.controller.power_state)

    def test_home_and_reset(self) -> None:
        '''
            Tests manipulator arm homing and position resetting.
        '''
        self.coordinator.jog_joint(1, 1.0, 20.0, 30)
        self.assertEqual(self.coordinator.get_angles()[0], 20.0)

        self.assertTrue(self.coordinator.home(speed=30))
        self.assertEqual(self.coordinator.get_angles()[0], 0.0)


if __name__ == '__main__':
    main()
