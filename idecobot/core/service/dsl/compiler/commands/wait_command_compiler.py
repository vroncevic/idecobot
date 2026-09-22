# -*- coding: UTF-8 -*-

'''
Module
    wait_command_compiler.py
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
    Defines WaitCommandCompiler compiling WAIT statements into frame delays or NOP frames.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.service.dsl.compiler.compiler_context import CompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaitCommandCompiler:
    '''
        Compiles WAIT statements by extending preceding frame delay or emitting NOP frames.

        It defines:

            :attributes:
                | _constants - Injected ProtocolConstants low-level framing parameters.
            :methods:
                | __init__ - Initializes compiler with protocol constants.
                | can_compile - Verifies if instruction command type is WAIT.
                | compile - Extends preceding frame delay or emits NOP frame.
                | get_version - Returns the compiler component version string.
    '''

    _constants: ProtocolConstants

    def __init__(self, constants: ProtocolConstants) -> None:
        '''
            Initializes WaitCommandCompiler with protocol constants.

            :param constants: Injected ProtocolConstants instance.
            :exceptions: None.
        '''
        self._constants = constants

    def can_compile(self, command_type: MyCobotCommandType) -> bool:
        '''
            Verifies if instruction command type is WAIT.

            :param command_type: MyCobotCommandType enum value.
            :return: True if command type is WAIT, False otherwise.
            :exceptions: None.
        '''
        return command_type == MyCobotCommandType.WAIT

    def compile(
        self,
        instruction: MyCobotInstruction,
        context: CompilerContext
    ) -> Sequence[MyCobotFrame]:
        '''
            Extends preceding frame delay or generates NOP frame when context is empty.

            :param instruction: Parsed WAIT AST instruction node.
            :param context: Active compilation context tracking arm state.
            :return: Empty sequence if merged into preceding frame, or sequence with NOP frame.
            :exceptions: None.
        '''
        wait_sec: float = float(instruction.parameters.get('seconds', 0.0))

        if not context.add_delay_to_last_frame(wait_sec):
            return (
                MyCobotFrame(
                    self._constants.cmd_nop,
                    b'',
                    wait_sec
                ),
            )

        return ()

    def get_version(self) -> str:
        '''
            Returns the compiler component version string.

            :return: The component version string.
            :exceptions: None.
        '''
        return __version__
