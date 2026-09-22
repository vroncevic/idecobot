# -*- coding: UTF-8 -*-

'''
Module
    jog_panel_factory.py
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
    Defines JogPanelFactory responsible for assembling JogPanel and its subpanel collaborators.
'''

from __future__ import annotations

from tkinter import Frame, TOP, X

from idecobot.infrastructure.gui.jog.cartesian_constants import CartesianConstants
from idecobot.infrastructure.gui.jog.cartesian_panel import CartesianPanel
from idecobot.infrastructure.gui.jog.jog_constants import JogConstants
from idecobot.infrastructure.gui.jog.jog_coordinator import JogCoordinator
from idecobot.infrastructure.gui.jog.jog_panel import JogPanel
from idecobot.infrastructure.gui.jog.joint_constants import JointConstants
from idecobot.infrastructure.gui.jog.joint_panel import JointPanel
from idecobot.infrastructure.gui.jog.step_constants import StepConstants
from idecobot.infrastructure.gui.jog.step_panel import StepPanel
from idecobot.infrastructure.gui.jog.tool_constants import ToolConstants
from idecobot.infrastructure.gui.jog.tool_panel import ToolPanel
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogPanelFactory:
    '''
        Factory class assembling JogPanel composite view and wiring child subpanels.

        It defines:

            :methods:
                | create_jog_panel - Constructs container frame, subpanels, and JogPanel.
    '''

    @classmethod
    def create_jog_panel(
        cls,
        parent: Frame,
        coordinator: JogCoordinator,
        palette: ColorPalette,
        constants: JogConstants
    ) -> JogPanel:
        '''
            Constructs and wires the JogPanel composite view with all child subpanels.

            :param parent: Parent container Frame.
            :param coordinator: Injected JogCoordinator handling motion and kinematics.
            :param palette: Injected ColorPalette design tokens.
            :param constants: Injected JogConstants layout and operational configuration.
            :return: Fully assembled JogPanel instance.
            :exceptions: None.
        '''
        frame: Frame = Frame(
            parent,
            bg=palette.bg_dark,
            padx=constants.outer_padx,
            pady=constants.outer_pady
        )
        frame.pack(fill=X, side=TOP)

        step_constants: StepConstants = StepConstants()
        joint_constants: JointConstants = JointConstants()
        cart_constants: CartesianConstants = CartesianConstants()
        tool_constants: ToolConstants = ToolConstants()

        step_panel: StepPanel = StepPanel(frame, palette, step_constants)

        def handle_joint_jog(joint_id: int, sign: float) -> None:
            step: float = step_panel.get_step()
            speed: int = step_panel.get_speed()

            if coordinator.jog_joint(joint_id, sign, step, speed):
                joint_panel.update_angles(coordinator.get_angles())

        def handle_cart_jog(axis: str, sign: float) -> None:
            step: float = step_panel.get_step()
            speed: int = step_panel.get_speed()

            if coordinator.jog_cartesian(axis, sign, step, speed):
                cart_panel.update_coords(coordinator.get_coords())

        def handle_gripper(state: int) -> None:
            speed: int = step_panel.get_speed()

            if coordinator.actuate_gripper(state, speed):
                label: str = (
                    constants.state_gripped
                    if state == constants.grip_action_grip
                    else constants.state_released
                )
                tool_panel.set_gripper_state(label)

        def handle_power(on: bool) -> None:
            coordinator.toggle_power(on)

        def handle_home() -> None:
            speed: int = step_panel.get_speed()

            if coordinator.home(speed):
                coordinator.reset_positions()
                joint_panel.update_angles(coordinator.get_angles())
                cart_panel.update_coords(coordinator.get_coords())

        joint_panel: JointPanel = JointPanel(
            frame, handle_joint_jog, palette, joint_constants
        )
        cart_panel: CartesianPanel = CartesianPanel(
            frame, handle_cart_jog, palette, cart_constants
        )
        tool_panel: ToolPanel = ToolPanel(
            frame,
            handle_gripper,
            handle_power,
            handle_home,
            palette,
            tool_constants
        )

        return JogPanel(
            frame=frame,
            coordinator=coordinator,
            step_panel=step_panel,
            joint_panel=joint_panel,
            cart_panel=cart_panel,
            tool_panel=tool_panel
        )

