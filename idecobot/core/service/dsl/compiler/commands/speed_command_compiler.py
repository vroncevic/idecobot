# -*- coding: UTF-8 -*-

'''
Module
    speed_command_compiler.py
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
    Defines SpeedCommandCompiler handling SPEED statements during compilation.
'''

from __future__ import annotations

from collections.abc import Sequence

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


class SpeedCommandCompiler:
    '''
        Handles SPEED statements updating the active velocity in compiler context.

        It defines:

            :attributes:
                | _default_speed - Baseline fallback velocity percentage.
            :methods:
                | __init__ - Initializes compiler with default velocity percentage.
                | can_compile - Verifies if instruction command type is SPEED.
                | compile - Updates active speed in context without emitting frames.
                | get_version - Returns the compiler component version string.
    '''

    _default_speed: int

    def __init__(self, default_speed: int) -> None:
        '''
            Initializes SpeedCommandCompiler with baseline velocity.

            :param default_speed: Baseline velocity percentage (1-100).
            :exceptions: None.
        '''
        self._default_speed = default_speed

    def can_compile(self, command_type: MyCobotCommandType) -> bool:
        '''
            Verifies if instruction command type is SPEED.

            :param command_type: MyCobotCommandType enum value.
            :return: True if command type is SPEED, False otherwise.
            :exceptions: None.
        '''
        return command_type == MyCobotCommandType.SPEED

    def compile(
        self,
        instruction: MyCobotInstruction,
        context: CompilerContext
    ) -> Sequence[MyCobotFrame]:
        '''
            Updates active velocity percentage in context without emitting frames.

            :param instruction: Parsed SPEED AST instruction node.
            :param context: Active compilation context tracking arm state.
            :return: Empty sequence since SPEED does not emit serial frames.
            :exceptions: None.
        '''
        context.speed = int(instruction.parameters.get('value', self._default_speed))
        return ()

    def get_version(self) -> str:
        '''
            Returns the compiler component version string.

            :return: The component version string.
            :exceptions: None.
        '''
        return __version__
