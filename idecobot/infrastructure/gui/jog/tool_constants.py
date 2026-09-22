# -*- coding: UTF-8 -*-

'''
Module
    tool_constants.py
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
    Defines ToolConstants frozen dataclass for ToolPanel.
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
class ToolConstants:
    '''
        Constants for Tool and servo subpanel layout, styles, and action identifiers.

        It defines:

            :attributes:
                | frame_padx - Horizontal padding of tool subpanel frame.
                | frame_pady - Vertical padding of tool subpanel frame.
                | outer_padx - Outer container horizontal padding.
                | tool_btn_width - Character width of tool action buttons.
                | title_text - Header label text for tool and servo subpanel.
                | label_gripper - Label text for gripper control section.
                | label_servo_state - Label text for servo state control section.
                | btn_grip_text - Text for grip button.
                | btn_release_text - Text for release button.
                | btn_power_on_text - Text for power on button.
                | btn_relax_text - Text for relax button.
                | btn_home_text - Text for zero home button.
                | text_gripper_idle - Default idle gripper state text.
                | style_header - Ttk style identifier for header label.
                | style_label - Ttk style identifier for standard labels.
                | style_status - Ttk style identifier for gripper status text.
                | style_accent_btn - Ttk style identifier for accent action button.
                | style_success_btn - Ttk style identifier for success action button.
                | style_danger_btn - Ttk style identifier for danger action button.
                | pad_title_y - Vertical padding tuple for panel header.
                | pad_row_y - Vertical padding for button rows.
                | pad_state_y - Vertical padding tuple for state label.
                | pad_home_y - Vertical padding for zero home button.
                | pad_btn_x - Horizontal padding between buttons.
                | grip_action_grip - Integer action code for gripper close.
                | grip_action_release - Integer action code for gripper open.
    '''

    frame_padx: int = 8
    frame_pady: int = 4
    outer_padx: int = 4
    tool_btn_width: int = 8
    title_text: str = 'Tool & Servo'
    label_gripper: str = 'Gripper:'
    label_servo_state: str = 'Servo State:'
    btn_grip_text: str = 'Grip'
    btn_release_text: str = 'Release'
    btn_power_on_text: str = '⚡ Power On'
    btn_relax_text: str = '🔓 Relax'
    btn_home_text: str = '⌂ Zero Home'
    text_gripper_idle: str = 'State: Idle'
    style_header: str = 'Header.TLabel'
    style_label: str = 'TLabel'
    style_status: str = 'Status.TLabel'
    style_accent_btn: str = 'Accent.TButton'
    style_success_btn: str = 'Success.TButton'
    style_danger_btn: str = 'Danger.TButton'
    pad_title_y: tuple[int, int] = (0, 4)
    pad_row_y: int = 2
    pad_state_y: tuple[int, int] = (2, 6)
    pad_home_y: int = 4
    pad_btn_x: int = 2
    grip_action_grip: int = 1
    grip_action_release: int = 0

