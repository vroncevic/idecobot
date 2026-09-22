# -*- coding: UTF-8 -*-

'''
Module
    step_constants.py
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
    Defines StepConstants frozen dataclass for StepPanel.
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
class StepConstants:
    '''
        Constants for step and speed dropdown selector layout, presets, and styles.

        It defines:

            :attributes:
                | frame_padx - Horizontal padding of the panel frame.
                | frame_pady - Vertical padding of the panel frame.
                | outer_padx - Outer container horizontal padding.
                | title_text - Section header title string.
                | label_step - Label text for step size selection.
                | label_speed - Label text for operating speed selection.
                | combo_width - Character width of step and speed comboboxes.
                | default_step_str - Baseline step increment string.
                | default_speed_str - Baseline operating speed percentage string.
                | default_step - Baseline step increment numerical value.
                | default_speed - Baseline operating speed percentage numerical value.
                | step_presets - Sequence of selectable step delta strings in degrees or mm.
                | speed_presets - Sequence of selectable speed percentage strings.
                | style_header - Ttk style identifier for header label.
                | style_label - Ttk style identifier for selector labels.
                | state_readonly - Ttk combobox readonly state string.
                | pad_title_y - Vertical padding tuple for panel header.
                | pad_step_y - Vertical padding tuple for step dropdown combobox.
    '''

    frame_padx: int = 8
    frame_pady: int = 4
    outer_padx: int = 4
    title_text: str = 'Jog Config'
    label_step: str = 'Step (deg/mm):'
    label_speed: str = 'Speed (%):'
    combo_width: int = 8
    default_step_str: str = '5.0'
    default_speed_str: str = '30'
    default_step: float = 5.0
    default_speed: int = 30
    step_presets: tuple[str, ...] = ('1.0', '5.0', '10.0', '20.0', '45.0')
    speed_presets: tuple[str, ...] = ('10', '20', '30', '50', '80', '100')
    style_header: str = 'Header.TLabel'
    style_label: str = 'TLabel'
    state_readonly: str = 'readonly'
    pad_title_y: tuple[int, int] = (0, 4)
    pad_step_y: tuple[int, int] = (0, 6)
