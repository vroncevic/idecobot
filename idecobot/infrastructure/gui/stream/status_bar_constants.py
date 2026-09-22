# -*- coding: UTF-8 -*-

'''
Module
    status_bar_constants.py
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
    Defines StatusBarConstants frozen dataclass for StatusBar widget.
'''

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class StatusBarConstants:
    '''
        Constants for streaming telemetry status bar layout, styling, and default text.

        It defines:

            :attributes:
                | height - Pixel height of the fixed-height status bar container.
                | progressbar_length - Pixel length of the execution progress bar.
                | bg_idle - Background color during IDLE / READY state.
                | bg_streaming - Background color during active motion streaming.
                | bg_paused - Background color when motion streaming is paused.
                | bg_error - Background color on error state.
                | fg_text - Primary white text foreground color.
                | fg_secondary - Secondary light gray text foreground color.
                | font_state - Typography tuple for lifecycle state indicator.
                | font_text - Typography tuple for step, command, and message readouts.
                | text_ready - Text displayed during idle/ready status.
                | mode_determinate - Progressbar operation mode string.
                | text_default_step - Baseline step count readout string.
                | text_default_cmd - Baseline command name readout string.
                | text_empty - Empty string placeholder.
                | pad_progress_x - Horizontal padding for progress bar.
                | pad_progress_y - Vertical padding for progress bar.
                | pad_state_x - Horizontal padding for state indicator label.
                | pad_text_x - Horizontal padding for telemetry labels.
                | default_progress_val - Initial progress bar numerical percentage value.
    '''

    height: int = 24
    progressbar_length: int = 180
    bg_idle: str = '#007ACC'
    bg_streaming: str = '#16825D'
    bg_paused: str = '#D7BA7D'
    bg_error: str = '#A80000'
    fg_text: str = '#FFFFFF'
    fg_secondary: str = '#E7E7E7'
    font_state: tuple[str, int, str] = ('DejaVu Sans', 8, 'bold')
    font_text: tuple[str, int] = ('DejaVu Sans', 8)
    text_ready: str = 'READY'
    mode_determinate: Literal['determinate', 'indeterminate'] = 'determinate'
    text_default_step: str = 'Step: 0/0'
    text_default_cmd: str = 'Command: -'
    text_empty: str = ''
    pad_progress_x: int = 8
    pad_progress_y: int = 2
    pad_state_x: int = 8
    pad_text_x: int = 6
    default_progress_val: float = 0.0
