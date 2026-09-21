# -*- coding: UTF-8 -*-

'''
Module
    mycobot_instruction.py
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
    Defines MyCobotInstruction immutable data model representing an AST command node.
'''

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MyCobotInstruction:
    '''
        Represents an individual parsed instruction node in the myCobot AST.

        It defines:

            :attributes:
                | command_type - Type of command (HOME, RELAX, SPEED, MOVE, etc.).
                | line_number - Source 1-indexed line number.
                | parameters - Dictionary mapping axis/parameter names to numeric values.
                | raw_text - Original raw text line from source.
    '''

    command_type: MyCobotCommandType
    line_number: int
    parameters: Mapping[str, float]
    raw_text: str
