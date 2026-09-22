# -*- coding: UTF-8 -*-

'''
Module
    tool_panel.py
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
    Defines ToolPanel widget for end effector gripper and servo power controls.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import BOTH, Frame, LEFT, W, X
from tkinter.ttk import Button, Label

from idecobot.infrastructure.gui.jog.tool_constants import ToolConstants
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolPanel:
    '''
        Subpanel controlling the robot gripper, servo power state, and homing.

        It defines:

            :attributes:
                | _palette - Injected ColorPalette design tokens.
                | _constants - Injected ToolConstants configuration.
                | _frame - Container Frame widget.
                | _lbl_gripper_state - Status label displaying current gripper state.
            :methods:
                | __init__ - Initializes tool controls.
                | get_frame - Returns container Frame.
                | set_gripper_state - Updates gripper state label text.
                | constants - Property returning injected ToolConstants.
    '''

    _palette: ColorPalette
    _constants: ToolConstants
    _frame: Frame
    _lbl_gripper_state: Label

    def __init__(
        self,
        parent: Frame,
        on_grip: Callable[[int], None],
        on_power: Callable[[bool], None],
        on_home: Callable[[], None],
        palette: ColorPalette,
        constants: ToolConstants
    ) -> None:
        '''
            Initializes tool jog controls.

            :param parent: Parent Frame widget.
            :param on_grip: Callback (state: int) -> None (1=grip, 0=release).
            :param on_power: Callback (on: bool) -> None.
            :param on_home: Callback () -> None.
            :param palette: Injected ColorPalette color design tokens.
            :param constants: Injected ToolConstants configuration.
            :exceptions: None.
        '''
        self._palette = palette
        self._constants = constants

        self._frame = Frame(
            parent,
            bg=self._palette.bg_card,
            padx=self._constants.frame_padx,
            pady=self._constants.frame_pady
        )
        self._frame.pack(side=LEFT, fill=BOTH, expand=True, padx=self._constants.outer_padx)

        lbl_title: Label = Label(
            self._frame,
            text=self._constants.title_text,
            style=self._constants.style_header
        )
        lbl_title.pack(anchor=W, pady=self._constants.pad_title_y)

        lbl_grip: Label = Label(
            self._frame,
            text=self._constants.label_gripper,
            style=self._constants.style_label
        )
        lbl_grip.pack(anchor=W)

        row_grip: Frame = Frame(self._frame, bg=self._palette.bg_card)
        row_grip.pack(fill=X, pady=self._constants.pad_row_y)

        btn_grip: Button = Button(
            row_grip,
            text=self._constants.btn_grip_text,
            width=self._constants.tool_btn_width,
            style=self._constants.style_accent_btn,
            command=lambda: on_grip(self._constants.grip_action_grip)
        )
        btn_grip.pack(side=LEFT, padx=self._constants.pad_btn_x)

        btn_rel: Button = Button(
            row_grip,
            text=self._constants.btn_release_text,
            width=self._constants.tool_btn_width,
            command=lambda: on_grip(self._constants.grip_action_release)
        )
        btn_rel.pack(side=LEFT, padx=self._constants.pad_btn_x)

        self._lbl_gripper_state = Label(
            self._frame,
            text=self._constants.text_gripper_idle,
            style=self._constants.style_status
        )
        self._lbl_gripper_state.pack(anchor=W, pady=self._constants.pad_state_y)

        lbl_servo: Label = Label(
            self._frame,
            text=self._constants.label_servo_state,
            style=self._constants.style_label
        )
        lbl_servo.pack(anchor=W)

        row_servo: Frame = Frame(self._frame, bg=self._palette.bg_card)
        row_servo.pack(fill=X, pady=self._constants.pad_row_y)

        btn_pwr: Button = Button(
            row_servo,
            text=self._constants.btn_power_on_text,
            width=self._constants.tool_btn_width,
            style=self._constants.style_success_btn,
            command=lambda: on_power(True)
        )
        btn_pwr.pack(side=LEFT, padx=self._constants.pad_btn_x)

        btn_rlx: Button = Button(
            row_servo,
            text=self._constants.btn_relax_text,
            width=self._constants.tool_btn_width,
            style=self._constants.style_danger_btn,
            command=lambda: on_power(False)
        )
        btn_rlx.pack(side=LEFT, padx=self._constants.pad_btn_x)

        btn_home: Button = Button(
            self._frame,
            text=self._constants.btn_home_text,
            command=on_home
        )
        btn_home.pack(fill=X, pady=self._constants.pad_home_y)

    def get_frame(self) -> Frame:
        '''
            Returns container Frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def set_gripper_state(self, state_text: str) -> None:
        '''
            Updates gripper status text display.

            :param state_text: State description string.
            :exceptions: None.
        '''
        self._lbl_gripper_state.config(text=state_text)

    @property
    def constants(self) -> ToolConstants:
        '''
            Returns injected ToolConstants.

            :return: ToolConstants instance.
        '''
        return self._constants
