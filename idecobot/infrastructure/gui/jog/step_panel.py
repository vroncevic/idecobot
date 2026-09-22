# -*- coding: UTF-8 -*-

'''
Module
    step_panel.py
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
    Defines StepPanel widget for configuring step increment and motion speed.
'''

from __future__ import annotations

from tkinter import Frame, LEFT, W, Y
from tkinter.ttk import Combobox, Label

from idecobot.infrastructure.gui.jog.step_constants import StepConstants
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StepPanel:
    '''
        Subpanel allowing the operator to configure jog step increments and motion speed.

        It defines:

            :attributes:
                | _palette - Injected ColorPalette design tokens.
                | _constants - Injected StepConstants configuration.
                | _frame - Tkinter container Frame.
                | _cb_step - Step increment dropdown.
                | _cb_speed - Operating speed dropdown.
            :methods:
                | __init__ - Initializes step and speed dropdown controls.
                | get_frame - Returns container Frame.
                | get_step - Returns selected step increment value.
                | get_speed - Returns selected operating speed percentage.
                | constants - Property returning injected StepConstants.
    '''

    _palette: ColorPalette
    _constants: StepConstants
    _frame: Frame
    _cb_step: Combobox
    _cb_speed: Combobox

    def __init__(
        self,
        parent: Frame,
        palette: ColorPalette,
        constants: StepConstants
    ) -> None:
        '''
            Initializes step selector panel layout.

            :param parent: Parent Frame widget.
            :param palette: Injected ColorPalette color design tokens.
            :param constants: Injected StepConstants configuration.
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
        self._frame.pack(side=LEFT, fill=Y, padx=self._constants.outer_padx)

        lbl_title: Label = Label(
            self._frame,
            text=self._constants.title_text,
            style=self._constants.style_header
        )
        lbl_title.pack(anchor=W, pady=self._constants.pad_title_y)

        lbl_step: Label = Label(
            self._frame,
            text=self._constants.label_step,
            style=self._constants.style_label
        )
        lbl_step.pack(anchor=W)

        self._cb_step = Combobox(
            self._frame,
            values=list(self._constants.step_presets),
            width=self._constants.combo_width,
            state=self._constants.state_readonly
        )
        self._cb_step.set(self._constants.default_step_str)
        self._cb_step.pack(anchor=W, pady=self._constants.pad_step_y)

        lbl_speed: Label = Label(
            self._frame,
            text=self._constants.label_speed,
            style=self._constants.style_label
        )
        lbl_speed.pack(anchor=W)

        self._cb_speed = Combobox(
            self._frame,
            values=list(self._constants.speed_presets),
            width=self._constants.combo_width,
            state=self._constants.state_readonly
        )
        self._cb_speed.set(self._constants.default_speed_str)
        self._cb_speed.pack(anchor=W)

    def get_frame(self) -> Frame:
        '''
            Returns the container frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def get_step(self) -> float:
        '''
            Returns the currently selected step size in mm / degrees.

            :return: Step size as float.
            :exceptions: None.
        '''
        try:
            return float(self._cb_step.get())

        except (ValueError, TypeError):
            return self._constants.default_step

    def get_speed(self) -> int:
        '''
            Returns the currently selected speed percentage.

            :return: Speed percentage integer (1-100).
            :exceptions: None.
        '''
        try:
            val_str: str = self._cb_speed.get().replace('%', '').strip()

            return max(1, min(100, int(val_str)))

        except (ValueError, TypeError):
            return self._constants.default_speed

    @property
    def constants(self) -> StepConstants:
        '''
            Returns injected StepConstants.

            :return: StepConstants instance.
        '''
        return self._constants
