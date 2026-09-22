# -*- coding: UTF-8 -*-

'''
Module
    icommand_compiler.py
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
    Defines structural interface protocol for individual DSL command compilers.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.service.dsl.compiler.compiler_context import CompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICommandCompiler(Protocol):
    '''
        Defines structural interface protocol for compiling specific DSL instructions.

        It defines:

            :methods:
                | can_compile - Checks whether this compiler handles the given command type.
                | compile - Compiles instruction within context and returns emitted frames.
                | get_version - Returns the compiler component version string.
    '''

    def can_compile(self, command_type: MyCobotCommandType) -> bool:
        '''
            Determines if this compiler handles the given command type.

            :param command_type: MyCobotCommandType enum value.
            :return: True if this compiler handles the command, False otherwise.
            :exceptions: None.
        '''

    def compile(self, instruction: MyCobotInstruction, context: CompilerContext) -> Sequence[MyCobotFrame]:
        '''
            Translates instruction into binary frames updating compiler context.

            :param instruction: AST instruction to compile.
            :param context: Active compilation context tracking robot state.
            :return: Sequence of generated MyCobotFrame instances.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the compiler component version string.

            :return: Component version string.
            :exceptions: None.
        '''
