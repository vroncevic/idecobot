# -*- coding: UTF-8 -*-

'''
Module
    imycobot_program.py
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
    Defines structural interface protocol for an AST program container.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.dsl.ast.imycobot_instruction import IMyCobotInstruction

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMyCobotProgram(Protocol):
    '''
        Defines protocol IMyCobotProgram representing a complete AST program.

        It defines:

            :methods:
                | instructions - Returns the ordered sequence of AST instructions.
                | count - Returns the total count of instructions.
                | to_text - Serializes program back into formatted DSL source text.
                | to_dict - Serializes program to dictionary representation.
    '''

    @property
    def instructions(self) -> Sequence[IMyCobotInstruction]:
        '''
            Returns the ordered sequence of AST instructions.

            :return: Sequence of IMyCobotInstruction nodes.
        '''

    @property
    def count(self) -> int:
        '''
            Returns the total count of instructions.

            :return: Total number of instructions in program.
        '''

    def to_text(self) -> str:
        '''
            Serializes program instructions back into formatted DSL source text.

            :return: Formatted multiline source script text.
        '''

    def to_dict(self) -> dict[str, object]:
        '''
            Serializes program to dictionary representation.

            :return: Dictionary representation of program.
        '''
