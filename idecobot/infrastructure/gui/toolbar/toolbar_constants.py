# -*- coding: UTF-8 -*-

'''
Module
    toolbar_constants.py
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
    Defines ToolbarConstants frozen dataclass for Toolbar widget.
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
class ToolbarConstants:
    '''
        Constants for toolbar button styling, layout, labels, and widget state management.

        It defines:

            :attributes:
                | frame_padx - Horizontal padding of the toolbar frame.
                | frame_pady - Vertical padding of the toolbar frame.
                | btn_padx - Horizontal padding between toolbar buttons.
                | sep_padx - Horizontal padding surrounding vertical separators.
                | sep_pady - Vertical padding surrounding vertical separators.
                | text_stream - Label for stream execution button.
                | text_pause - Label for stream pause button.
                | text_stop - Label for stream stop button.
                | text_home - Label for robot homing button.
                | text_relax - Label for relaxing servos button.
                | text_clear_log - Label for log clear button.
                | style_run_btn - Ttk style identifier for run action button.
                | style_stop_btn - Ttk style identifier for stop action button.
                | style_home_btn - Ttk style identifier for home arm action button.
                | state_disabled - Ttk widget state for disabled control.
                | state_enabled - Ttk widget state for active/enabled control.
    '''

    frame_padx: int = 6
    frame_pady: int = 4
    btn_padx: int = 3
    sep_padx: int = 8
    sep_pady: int = 2
    text_stream: str = '▶ Stream'
    text_pause: str = '⏸ Pause'
    text_stop: str = '⏹ Stop'
    text_home: str = '⌂ Home'
    text_relax: str = '🔓 Relax'
    text_clear_log: str = '🗑 Clear Log'
    style_run_btn: str = 'Success.TButton'
    style_stop_btn: str = 'Danger.TButton'
    style_home_btn: str = 'Accent.TButton'
    state_disabled: str = 'disabled'
    state_enabled: str = '!disabled'
