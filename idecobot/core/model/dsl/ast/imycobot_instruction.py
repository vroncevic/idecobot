# -*- coding: UTF-8 -*-

'''
Module
    imycobot_instruction.py
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
    Defines structural interface protocol for an AST instruction node.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMyCobotInstruction(Protocol):
    '''
        Defines protocol IMyCobotInstruction with property accessors.

        It defines:

            :methods:
                | command_type - Returns the command type of the instruction.
                | line_number - Returns the source line number of the instruction.
                | parameters - Returns the parameter mapping of the instruction.
                | raw_text - Returns the raw text string of the instruction.
    '''

    @property
    def command_type(self) -> MyCobotCommandType:
        '''
            Returns the command type of the instruction.

            :return: The MyCobotCommandType enum value.
        '''

    @property
    def line_number(self) -> int:
        '''
            Returns the source line number of the instruction.

            :return: 1-indexed line number integer.
        '''

    @property
    def parameters(self) -> Mapping[str, float]:
        '''
            Returns the parameter mapping of the instruction.

            :return: Mapping of parameter name to float value.
        '''

    @property
    def raw_text(self) -> str:
        '''
            Returns the raw text string of the instruction.

            :return: Source text line representation.
        '''
