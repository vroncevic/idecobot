# -*- coding: UTF-8 -*-

'''
Module
    cartesian_constants.py
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
    Defines CartesianConstants frozen dataclass for CartesianPanel.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class CartesianConstants:
    '''
        Constants for Cartesian subpanel layout, styles, and axes descriptors.

        It defines:

            :attributes:
                | frame_padx - Horizontal padding of Cartesian subpanel frame.
                | frame_pady - Vertical padding of Cartesian subpanel frame.
                | outer_padx - Outer container horizontal padding.
                | row_pady - Vertical padding between Cartesian jog rows.
                | title_text - Header label text for Cartesian jog subpanel.
                | label_width - Character width of axis descriptor labels.
                | val_width - Character width of coordinate readout labels.
                | step_btn_width - Character width of increment/decrement buttons.
                | btn_minus_text - Text for minus decrement button.
                | btn_plus_text - Text for plus increment button.
                | axes - Ordered sequence of 6 Cartesian axis symbols (X, Y, Z, Rx, Ry, Rz).
                | style_header - Ttk style identifier for header label.
                | style_label - Ttk style identifier for standard axis label.
                | style_status - Ttk style identifier for coordinate readout label.
                | pad_title_y - Vertical padding tuple for panel header.
                | btn_padx - Horizontal padding for +/- jog buttons.
                | linear_axes - Set of linear Cartesian axes for millimeter unit checks.
                | sign_minus - Direction sign factor for decrement jog.
                | sign_plus - Direction sign factor for increment jog.
                | unit_mm - Millimeter unit string symbol.
                | unit_deg - Degree unit string symbol.
    '''

    frame_padx: int = 8
    frame_pady: int = 4
    outer_padx: int = 4
    row_pady: int = 1
    title_text: str = 'Cartesian Jog (X-Rz)'
    label_width: int = 3
    val_width: int = 7
    step_btn_width: int = 2
    btn_minus_text: str = '-'
    btn_plus_text: str = '+'
    axes: tuple[str, ...] = ('X', 'Y', 'Z', 'Rx', 'Ry', 'Rz')
    style_header: str = 'Header.TLabel'
    style_label: str = 'TLabel'
    style_status: str = 'Status.TLabel'
    pad_title_y: tuple[int, int] = (0, 4)
    btn_padx: int = 2
    linear_axes: frozenset[str] = frozenset({'X', 'Y', 'Z'})
    sign_minus: float = -1.0
    sign_plus: float = 1.0
    unit_mm: str = 'mm'
    unit_deg: str = '°'

