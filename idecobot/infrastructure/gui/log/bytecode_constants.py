# -*- coding: UTF-8 -*-

'''
Module
    bytecode_constants.py
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
    Defines BytecodeConstants frozen dataclass for BytecodePreview widget.
'''

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class BytecodeConstants:
    '''
        Constants for bytecode preview table formatting and widget states.

        It defines:

            :attributes:
                | state_normal - Tkinter normal widget state.
                | state_disabled - Tkinter disabled widget state.
                | wrap_none - Tkinter no line wrapping.
                | index_start - Text widget start index string.
                | border_width - Text widget border width.
                | pad_text_x - Horizontal padding inside text widget.
                | pad_text_y - Vertical padding inside text widget.
                | header_template - Formatted header title string.
                | divider_char - Separator line character.
                | divider_length - Number of separator characters.
    '''

    state_normal: Literal['normal'] = 'normal'
    state_disabled: Literal['disabled'] = 'disabled'
    wrap_none: Literal['none'] = 'none'
    index_start: str = '1.0'
    border_width: int = 0
    pad_text_x: int = 6
    pad_text_y: int = 4
    header_template: str = 'STEP   CMD    HEX FRAME                                DELAY\n'
    divider_char: str = '-'
    divider_length: int = 65
