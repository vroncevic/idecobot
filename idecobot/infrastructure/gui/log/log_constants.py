# -*- coding: UTF-8 -*-

'''
Module
    log_constants.py
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
    Defines LogConstants frozen dataclass for LogPanel tabbed view.
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
class LogConstants:
    '''
        Constants for log panel notebook tabs and frame padding.

        It defines:

            :attributes:
                | tab_serial - Tab title string for serial monitor console.
                | tab_bytecode - Tab title string for bytecode hex inspector.
                | pad_frame_x - Horizontal padding for outer frame.
                | pad_frame_y - Vertical padding for outer frame.
                | tab_index_bytecode - Numerical tab index of bytecode tab.
    '''

    tab_serial: str = '  Serial Monitor (Log)  '
    tab_bytecode: str = '  Bytecode Preview  '
    pad_frame_x: int = 4
    pad_frame_y: int = 2
    tab_index_bytecode: int = 1
