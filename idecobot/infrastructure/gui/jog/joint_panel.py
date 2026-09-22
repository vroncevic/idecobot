# -*- coding: UTF-8 -*-

'''
Module
    joint_panel.py
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
    Defines JointPanel widget for single-joint manual motion controls.
'''

from __future__ import annotations

from collections.abc import Callable, Sequence
from tkinter import BOTH, CENTER, Frame, LEFT, W, X
from tkinter.ttk import Button, Label

from idecobot.infrastructure.gui.jog.joint_constants import JointConstants
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointPanel:
    '''
        Subpanel providing incremental +/- jog buttons and angle displays for 6 joints.

        It defines:

            :attributes:
                | _palette - Injected ColorPalette design tokens.
                | _constants - Injected JointConstants configuration.
                | _frame - Container Frame widget.
                | _on_jog - Jog callback function.
                | _labels - Mapping of joint index to angle readout Label widgets.
            :methods:
                | __init__ - Initializes joint jog controls.
                | create_joint_row - Builds a single joint jog row with controls and readout.
                | get_frame - Returns container Frame.
                | update_angles - Updates displayed joint angle readouts.
                | constants - Property returning injected JointConstants.
                | get_version - Returns Joint panel version string.
    '''

    _palette: ColorPalette
    _constants: JointConstants
    _frame: Frame
    _on_jog: Callable[[int, float], None]
    _labels: dict[int, Label]

    def __init__(
        self,
        parent: Frame,
        on_jog: Callable[[int, float], None],
        palette: ColorPalette,
        constants: JointConstants
    ) -> None:
        '''
            Initializes joint jog controls.

            :param parent: Parent Frame widget.
            :param on_jog: Callback (joint_id: int, sign: float) -> None.
            :param palette: Injected ColorPalette color design tokens.
            :param constants: Injected JointConstants configuration.
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
        self._on_jog = on_jog
        self._labels = {}

        lbl_title: Label = Label(
            self._frame,
            text=self._constants.title_text,
            style=self._constants.style_header
        )
        lbl_title.pack(anchor=W, pady=self._constants.pad_title_y)

        for j_id in range(self._constants.min_joint_id, self._constants.max_joint_id + 1):
            self.create_joint_row(j_id)

    def create_joint_row(self, j_id: int) -> None:
        '''
            Builds a single joint jog row with label, minus button, readout, plus button.

            :param j_id: Joint index from 1 to 6.
            :exceptions: None.
        '''
        row: Frame = Frame(self._frame, bg=self._palette.bg_card)
        row.pack(fill=X, pady=self._constants.row_pady)

        name_lbl: Label = Label(
            row,
            text=f'J{j_id}:',
            width=self._constants.label_width,
            style=self._constants.style_label
        )
        name_lbl.pack(side=LEFT)

        btn_minus: Button = Button(
            row,
            text=self._constants.btn_minus_text,
            width=self._constants.step_btn_width + 1,
            command=lambda: self._on_jog(j_id, self._constants.sign_minus)
        )
        btn_minus.pack(side=LEFT, padx=self._constants.btn_padx)

        unit_str: str = self._constants.unit_deg
        val_lbl: Label = Label(
            row,
            text=self._constants.default_readout,
            width=self._constants.val_width,
            style=self._constants.style_status,
            anchor=CENTER
        )
        val_lbl.pack(side=LEFT, padx=self._constants.btn_padx)
        self._labels[j_id] = val_lbl

        btn_plus: Button = Button(
            row,
            text=self._constants.btn_plus_text,
            width=self._constants.step_btn_width + 1,
            command=lambda: self._on_jog(j_id, self._constants.sign_plus)
        )
        btn_plus.pack(side=LEFT, padx=self._constants.btn_padx)

    def get_frame(self) -> Frame:
        '''
            Returns container Frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def update_angles(self, angles: Sequence[float]) -> None:
        '''
            Updates displayed joint angle readouts.

            :param angles: Sequence of 6 joint angles in degrees.
            :exceptions: None.
        '''
        for idx, angle in enumerate(angles):
            j_id: int = idx + 1

            if j_id in self._labels:
                self._labels[j_id].config(text=f'{angle:.1f}{self._constants.unit_deg}')

    @property
    def constants(self) -> JointConstants:
        '''
            Returns injected JointConstants.

            :return: JointConstants instance.
        '''
        return self._constants

    def get_version(self) -> str:
        '''
            Returns Joint panel version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
