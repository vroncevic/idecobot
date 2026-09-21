# -*- coding: UTF-8 -*-

'''
Module
    mycobot_program.py
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
    Defines MyCobotProgram immutable container for parsed AST instructions.
'''

from __future__ import annotations

from dataclasses import dataclass

from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MyCobotProgram:
    '''
        Represents a validated sequence of AST instructions in the myCobot DSL.

        It defines:

            :attributes:
                | instructions - Immutable tuple of MyCobotInstruction nodes.
            :methods:
                | count - Returns the total number of instructions.
                | to_text - Serializes program back into formatted DSL source text.
                | to_dict - Serializes program to dictionary representation.
    '''

    instructions: tuple[MyCobotInstruction, ...] = ()

    @property
    def count(self) -> int:
        '''
            Returns the total count of instructions.

            :return: Total number of instructions in program.
            :exceptions: None.
        '''
        return len(self.instructions)

    def to_text(self) -> str:
        '''
            Serializes program instructions back into formatted DSL source text.

            :return: Formatted multiline source script text.
            :exceptions: None.
        '''
        return '\n'.join(
            inst.raw_text if inst.raw_text else str(inst.command_type.value)
            for inst in self.instructions
        )

    def to_dict(self) -> dict[str, object]:
        '''
            Serializes program to dictionary representation.

            :return: Dictionary representation of program.
            :exceptions: None.
        '''
        return {
            'count': len(self.instructions),
            'instructions': [
                {
                    'command_type': inst.command_type.value,
                    'line_number': inst.line_number,
                    'parameters': dict(inst.parameters),
                    'raw_text': inst.raw_text,
                }
                for inst in self.instructions
            ],
        }
