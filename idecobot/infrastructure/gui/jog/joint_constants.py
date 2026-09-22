# -*- coding: UTF-8 -*-

'''
Module
    joint_constants.py
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
    Defines JointConstants frozen dataclass for JointPanel.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class JointConstants:
    '''
        Constants for Joint jog subpanel layout, styles, and joint descriptors.

        It defines:

            :attributes:
                | frame_padx - Horizontal padding of joint subpanel frame.
                | frame_pady - Vertical padding of joint subpanel frame.
                | outer_padx - Outer container horizontal padding.
                | row_pady - Vertical padding between joint jog rows.
                | title_text - Header label text for joint jog subpanel.
                | label_width - Character width of joint descriptor labels.
                | val_width - Character width of angle readout labels.
                | step_btn_width - Character width of increment/decrement buttons.
                | btn_minus_text - Text for minus decrement button.
                | btn_plus_text - Text for plus increment button.
                | style_header - Ttk style identifier for header label.
                | style_label - Ttk style identifier for joint name label.
                | style_status - Ttk style identifier for angle readout label.
                | pad_title_y - Vertical padding tuple for panel header.
                | btn_padx - Horizontal padding for +/- jog buttons.
                | default_readout - Baseline zero angle readout string.
                | min_joint_id - Minimum 1-based joint identifier.
                | max_joint_id - Maximum 1-based joint identifier.
                | sign_minus - Direction sign factor for decrement jog.
                | sign_plus - Direction sign factor for increment jog.
                | unit_deg - Degree unit string symbol.
    '''

    frame_padx: int = 8
    frame_pady: int = 4
    outer_padx: int = 4
    row_pady: int = 1
    title_text: str = 'Joint Jog (J1-J6)'
    label_width: int = 3
    val_width: int = 7
    step_btn_width: int = 2
    btn_minus_text: str = '-'
    btn_plus_text: str = '+'
    style_header: str = 'Header.TLabel'
    style_label: str = 'TLabel'
    style_status: str = 'Status.TLabel'
    pad_title_y: tuple[int, int] = (0, 4)
    btn_padx: int = 2
    default_readout: str = '0.0°'
    min_joint_id: int = 1
    max_joint_id: int = 6
    sign_minus: float = -1.0
    sign_plus: float = 1.0
    unit_deg: str = '°'

