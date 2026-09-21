# -*- coding: UTF-8 -*-

'''
Module
    console_constants.py
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
    Defines ConsoleConstants frozen dataclass for SerialConsole widget.
'''

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class ConsoleConstants:
    '''
        Constants for serial console text styling, tags, and prefixes.

        It defines:

            :attributes:
                | tag_time - Text tag identifier for timestamps.
                | tag_tx - Text tag identifier for transmit log lines.
                | tag_rx - Text tag identifier for receive log lines.
                | tag_err - Text tag identifier for error log lines.
                | tag_warn - Text tag identifier for warning log lines.
                | tag_info - Text tag identifier for standard informational lines.
                | font_weight_bold - Font weight descriptor.
                | state_normal - Tkinter normal widget state.
                | state_disabled - Tkinter disabled widget state.
                | wrap_none - Tkinter no line wrapping.
                | index_start - Text widget start index string.
                | prefix_tx - Prefix pattern identifying transmitted data.
                | prefix_rx - Prefix pattern identifying received data.
                | keyword_err - Substring identifying error entries.
                | keyword_warn - Substring identifying warning entries.
                | time_format - Datetime string formatting directive.
                | time_slice_end - Number of characters to take from formatted time.
                | pad_text_x - Horizontal padding inside text widget.
                | pad_text_y - Vertical padding inside text widget.
                | border_width - Text widget border width.
    '''

    tag_time: str = 'tag_time'
    tag_tx: str = 'tag_tx'
    tag_rx: str = 'tag_rx'
    tag_err: str = 'tag_err'
    tag_warn: str = 'tag_warn'
    tag_info: str = 'tag_info'
    font_weight_bold: str = 'bold'
    state_normal: Literal['normal'] = 'normal'
    state_disabled: Literal['disabled'] = 'disabled'
    wrap_none: Literal['none'] = 'none'
    index_start: str = '1.0'
    prefix_tx: str = 'TX:'
    prefix_rx: str = 'RX:'
    keyword_err: str = 'ERR'
    keyword_warn: str = 'WARN'
    time_format: str = '%H:%M:%S.%f'
    time_slice_end: int = 12
    pad_text_x: int = 6
    pad_text_y: int = 4
    border_width: int = 0
