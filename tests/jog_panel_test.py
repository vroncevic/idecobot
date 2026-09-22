# -*- coding: UTF-8 -*-

'''
Module
    jog_panel_test.py
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
    Unit tests for JogPanelFactory, JogPanel, and ToolPanel GUI callbacks.
'''

from __future__ import annotations

from tkinter import Frame, Tk
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
from idecobot.infrastructure.gui.jog.jog_panel import JogPanel
from idecobot.infrastructure.gui.jog.jog_panel_factory import JogPanelFactory
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockController:
    '''
    Mock robot controller tracking gripper and motion states.
    '''

    def __init__(self) -> None:
        self.gripper_state: int | None = None
        self.last_speed: int = 0
        self.power_state: bool = False
        self.home_called: bool = False

    def send_angles(self, angles: list[float], speed: int) -> bool:
        '''
        Simulates angle transmission.
        '''
        self.last_angles: list[float] = list(angles)
        self.last_speed = speed
        return True

    def send_coords(self, coords: list[float], speed: int) -> bool:
        '''
        Simulates Cartesian coordinate transmission.
        '''
        self.last_speed = speed
        return True

    def set_gripper(self, state: int, speed: int) -> bool:
        '''
        Simulates gripper actuation.
        '''
        self.gripper_state = state
        self.last_speed = speed
        return True

    def power(self, on: bool) -> bool:
        '''
        Simulates power toggle.
        '''
        self.power_state = on
        return True

    def home(self, speed: int) -> bool:
        '''
        Simulates zero homing.
        '''
        self.home_called = True
        self.last_speed = speed
        return True

    def is_connected(self) -> bool:
        '''
        Returns connection status.
        '''
        return True

    def get_angles(self) -> list[float]:
        '''
        Returns default joint angles.
        '''
        return [0.0] * 6

    def get_coords(self) -> list[float]:
        '''
        Returns default coordinates.
        '''
        return [0.0] * 6

    def stop(self) -> bool:
        '''
        Simulates emergency stop.
        '''
        return True


class TestJogPanelFactory(TestCase):
    '''
    Unit tests for JogPanelFactory assembly and ToolPanel callbacks.

    It defines:

        :methods:
            | setUp - Initializes Tk window, coordinator, and palette.
            | tearDown - Destroys Tk window.
            | test_jog_panel_creation - Verifies panel assembly.
            | test_gripper_actions - Verifies grip and release buttons execute without AttributeError.
            | test_power_and_home_actions - Verifies power toggle and homing callbacks.
    '''

    def setUp(self) -> None:
        '''
        Sets up test fixture before each test.
        '''
        self.root: Tk = Tk()
        self.root.withdraw()
        self.parent: Frame = Frame(self.root)
        self.parent.pack()

        self.controller: MockController = MockController()
        bounds: MyCobotBounds = MyCobotBounds(
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
        validator: KinematicValidator = KinematicValidator(bounds=bounds)
        self.constants: JogConstants = JogConstants()
        self.coordinator: JogCoordinator = JogCoordinator(
            controller=self.controller,
            validator=validator,
            constants=self.constants,
            on_log=lambda msg: None
        )
        self.palette: ColorPalette = ColorPalette()

    def tearDown(self) -> None:
        '''
        Cleans up Tk root window after each test.
        '''
        self.root.destroy()

    def test_jog_panel_creation(self) -> None:
        '''
        Verifies JogPanelFactory constructs JogPanel with all child components.
        '''
        panel: JogPanel = JogPanelFactory.create_jog_panel(
            parent=self.parent,
            coordinator=self.coordinator,
            palette=self.palette,
            constants=self.constants
        )
        self.assertIsNotNone(panel)
        self.assertIsNotNone(panel.get_frame())
        self.assertIsNotNone(panel.coordinator)
        self.assertIsNotNone(panel.step_panel)
        self.assertIsNotNone(panel.joint_panel)
        self.assertIsNotNone(panel.cart_panel)
        self.assertIsNotNone(panel.tool_panel)

    def test_gripper_actions(self) -> None:
        '''
        Verifies gripper Grip and Release buttons actuate controller and update status.
        '''
        panel: JogPanel = JogPanelFactory.create_jog_panel(
            parent=self.parent,
            coordinator=self.coordinator,
            palette=self.palette,
            constants=self.constants
        )

        tool_panel_frame = panel.tool_panel.get_frame()
        # Find grip and release buttons in tool panel child widgets
        buttons = []
        for child in tool_panel_frame.winfo_children():
            if isinstance(child, Frame):
                for subchild in child.winfo_children():
                    if hasattr(subchild, 'invoke'):
                        buttons.append(subchild)

        grip_btn = None
        release_btn = None
        for btn in buttons:
            text = btn.cget('text')
            if text == self.constants.btn_grip_text:
                grip_btn = btn
            elif text == self.constants.btn_release_text:
                release_btn = btn

        self.assertIsNotNone(grip_btn, 'Grip button should exist')
        self.assertIsNotNone(release_btn, 'Release button should exist')

        # Test Release actuation (simulating user clicking Release button)
        release_btn.invoke()
        self.assertEqual(self.controller.gripper_state, 0)

        # Test Grip actuation (simulating user clicking Grip button)
        grip_btn.invoke()
        self.assertEqual(self.controller.gripper_state, 1)

    def test_power_and_home_actions(self) -> None:
        '''
        Verifies power on, relax, and home button invocations.
        '''
        panel: JogPanel = JogPanelFactory.create_jog_panel(
            parent=self.parent,
            coordinator=self.coordinator,
            palette=self.palette,
            constants=self.constants
        )

        tool_panel_frame = panel.tool_panel.get_frame()
        buttons = []
        for child in tool_panel_frame.winfo_children():
            if hasattr(child, 'invoke'):
                buttons.append(child)
            elif isinstance(child, Frame):
                for subchild in child.winfo_children():
                    if hasattr(subchild, 'invoke'):
                        buttons.append(subchild)

        pwr_btn = None
        rlx_btn = None
        home_btn = None
        for btn in buttons:
            text = btn.cget('text')
            if text == self.constants.btn_power_on_text:
                pwr_btn = btn
            elif text == self.constants.btn_relax_text:
                rlx_btn = btn
            elif text == self.constants.btn_home_text:
                home_btn = btn

        self.assertIsNotNone(pwr_btn)
        self.assertIsNotNone(rlx_btn)
        self.assertIsNotNone(home_btn)

        pwr_btn.invoke()
        self.assertTrue(self.controller.power_state)

        rlx_btn.invoke()
        self.assertFalse(self.controller.power_state)

        home_btn.invoke()
        self.assertEqual(self.controller.last_angles, [0.0] * 6)


if __name__ == '__main__':
    main()
