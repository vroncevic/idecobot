# -*- coding: UTF-8 -*-

'''
Module
    jog_panel.py
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
    Defines JogPanel top manual control composite view holding jog subpanels.
'''

from __future__ import annotations

from tkinter import Frame

from idecobot.infrastructure.gui.jog.cartesian_panel import CartesianPanel
from idecobot.infrastructure.gui.jog.jog_coordinator import JogCoordinator
from idecobot.infrastructure.gui.jog.joint_panel import JointPanel
from idecobot.infrastructure.gui.jog.step_panel import StepPanel
from idecobot.infrastructure.gui.jog.tool_panel import ToolPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogPanel:
    '''
        Top manual control view holding joint, Cartesian, step selector, and tool subpanels.

        It defines:

            :attributes:
                | _frame - Injected outer container Frame widget.
                | _coordinator - Injected JogCoordinator managing motion state.
                | _step_panel - Injected StepPanel subpanel.
                | _joint_panel - Injected JointPanel subpanel.
                | _cart_panel - Injected CartesianPanel subpanel.
                | _tool_panel - Injected ToolPanel subpanel.
            :methods:
                | __init__ - Initializes JogPanel with injected collaborators.
                | get_frame - Returns container Frame.
                | reset_positions - Resets tracked joint angles and Cartesian coordinates.
                | coordinator - Property returning injected JogCoordinator.
                | step_panel - Property returning injected StepPanel.
                | joint_panel - Property returning injected JointPanel.
                | cart_panel - Property returning injected CartesianPanel.
                | tool_panel - Property returning injected ToolPanel.
    '''

    _frame: Frame
    _coordinator: JogCoordinator
    _step_panel: StepPanel
    _joint_panel: JointPanel
    _cart_panel: CartesianPanel
    _tool_panel: ToolPanel

    def __init__(
        self,
        frame: Frame,
        coordinator: JogCoordinator,
        step_panel: StepPanel,
        joint_panel: JointPanel,
        cart_panel: CartesianPanel,
        tool_panel: ToolPanel
    ) -> None:
        '''
            Initializes JogPanel composite view with strictly injected dependencies.

            :param frame: Injected outer container Frame widget.
            :param coordinator: Injected JogCoordinator instance.
            :param step_panel: Injected StepPanel instance.
            :param joint_panel: Injected JointPanel instance.
            :param cart_panel: Injected CartesianPanel instance.
            :param tool_panel: Injected ToolPanel instance.
            :exceptions: None.
        '''
        self._frame = frame
        self._coordinator = coordinator
        self._step_panel = step_panel
        self._joint_panel = joint_panel
        self._cart_panel = cart_panel
        self._tool_panel = tool_panel

    def get_frame(self) -> Frame:
        '''
            Returns the container frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def reset_positions(self) -> None:
        '''
            Resets tracked positions on coordinator and synchronizes child display panels.

            :exceptions: None.
        '''
        self._coordinator.reset_positions()
        self._joint_panel.update_angles(self._coordinator.get_angles())
        self._cart_panel.update_coords(self._coordinator.get_coords())

    @property
    def coordinator(self) -> JogCoordinator:
        '''
            Returns injected JogCoordinator.

            :return: JogCoordinator instance.
        '''
        return self._coordinator

    @property
    def step_panel(self) -> StepPanel:
        '''
            Returns injected StepPanel.

            :return: StepPanel instance.
        '''
        return self._step_panel

    @property
    def joint_panel(self) -> JointPanel:
        '''
            Returns injected JointPanel.

            :return: JointPanel instance.
        '''
        return self._joint_panel

    @property
    def cart_panel(self) -> CartesianPanel:
        '''
            Returns injected CartesianPanel.

            :return: CartesianPanel instance.
        '''
        return self._cart_panel

    @property
    def tool_panel(self) -> ToolPanel:
        '''
            Returns injected ToolPanel.

            :return: ToolPanel instance.
        '''
        return self._tool_panel
