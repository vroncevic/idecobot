# -*- coding: UTF-8 -*-

'''
Module
    cartesian_panel.py
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
    Defines CartesianPanel widget for Cartesian space motion controls.
'''

from __future__ import annotations

from collections.abc import Callable, Sequence
from tkinter import BOTH, Frame, LEFT, W, X
from tkinter.ttk import Button, Label

from idecobot.infrastructure.gui.jog.cartesian_constants import CartesianConstants
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CartesianPanel:
    '''
        Subpanel providing incremental jog controls for Cartesian position and orientation.

        It defines:

            :attributes:
                | _palette - Injected ColorPalette design tokens.
                | _constants - Injected CartesianConstants configuration.
                | _frame - Container Frame widget.
                | _on_jog - Jog callback function.
                | _labels - Mapping of axis name to coordinate readout Label widgets.
            :methods:
                | __init__ - Initializes Cartesian jog controls.
                | get_frame - Returns container Frame.
                | update_coords - Updates displayed coordinate readouts.
                | constants - Property returning injected CartesianConstants.
    '''

    _palette: ColorPalette
    _constants: CartesianConstants
    _frame: Frame
    _on_jog: Callable[[str, float], None]
    _labels: dict[str, Label]

    def __init__(
        self,
        parent: Frame,
        on_jog: Callable[[str, float], None],
        palette: ColorPalette,
        constants: CartesianConstants
    ) -> None:
        '''
            Initializes Cartesian jog controls.

            :param parent: Parent Frame widget.
            :param on_jog: Callback (axis: str, sign: float) -> None.
            :param palette: Injected ColorPalette color design tokens.
            :param constants: Injected CartesianConstants configuration.
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

        for axis in self._constants.axes:
            self._create_axis_row(axis)

    def _create_axis_row(self, axis: str) -> None:
        '''
            Builds a single axis row with label, minus button, readout, plus button.

            :param axis: Axis name (X, Y, Z, Rx, Ry, Rz).
            :exceptions: None.
        '''
        row: Frame = Frame(self._frame, bg=self._palette.bg_card)
        row.pack(fill=X, pady=self._constants.row_pady)

        name_lbl: Label = Label(
            row,
            text=f'{axis}:',
            width=self._constants.label_width + 1,
            style=self._constants.style_label
        )
        name_lbl.pack(side=LEFT)

        btn_minus: Button = Button(
            row,
            text=self._constants.btn_minus_text,
            width=self._constants.step_btn_width + 1,
            command=lambda: self._on_jog(axis, self._constants.sign_minus)
        )
        btn_minus.pack(side=LEFT, padx=self._constants.btn_padx)

        unit: str = (
            self._constants.unit_mm
            if axis in self._constants.linear_axes
            else self._constants.unit_deg
        )
        val_lbl: Label = Label(
            row,
            text=f'0.0 {unit}',
            width=self._constants.val_width + 3,
            style=self._constants.style_status,
            anchor=W
        )
        val_lbl.pack(side=LEFT, padx=self._constants.btn_padx)
        self._labels[axis] = val_lbl

        btn_plus: Button = Button(
            row,
            text=self._constants.btn_plus_text,
            width=self._constants.step_btn_width + 1,
            command=lambda: self._on_jog(axis, self._constants.sign_plus)
        )
        btn_plus.pack(side=LEFT, padx=self._constants.btn_padx)

    def get_frame(self) -> Frame:
        '''
            Returns container Frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def update_coords(self, coords: Sequence[float]) -> None:
        '''
            Updates displayed Cartesian coordinate readouts.

            :param coords: Sequence of 6 coordinates [x, y, z, rx, ry, rz].
            :exceptions: None.
        '''
        for idx, axis in enumerate(self._constants.axes):
            if idx < len(coords) and axis in self._labels:
                unit: str = (
                    self._constants.unit_mm
                    if axis in self._constants.linear_axes
                    else self._constants.unit_deg
                )
                self._labels[axis].config(text=f'{coords[idx]:.1f} {unit}')

    @property
    def constants(self) -> CartesianConstants:
        '''
            Returns injected CartesianConstants.

            :return: CartesianConstants instance.
        '''
        return self._constants
