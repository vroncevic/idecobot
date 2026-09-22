# -*- coding: UTF-8 -*-

'''
Module
    power_command_compiler.py
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
    Defines PowerCommandCompiler compiling POWER statements into binary protocol frames.
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


class PowerCommandCompiler:
    '''
        Compiles POWER statements into POWER_ON binary frames.

        It defines:

            :attributes:
                | _constants - Injected ProtocolConstants low-level framing parameters.
            :methods:
                | __init__ - Initializes compiler with protocol constants.
                | can_compile - Verifies if instruction command type is POWER.
                | compile - Compiles POWER instruction into POWER_ON frame.
                | get_version - Returns the compiler component version string.
    '''

    _constants: ProtocolConstants

    def __init__(self, constants: ProtocolConstants) -> None:
        '''
            Initializes PowerCommandCompiler with protocol constants.

            :param constants: Injected ProtocolConstants instance.
            :exceptions: None.
        '''
        self._constants = constants

    def can_compile(self, command_type: MyCobotCommandType) -> bool:
        '''
            Verifies if instruction command type is POWER.

            :param command_type: MyCobotCommandType enum value.
            :return: True if command type is POWER, False otherwise.
            :exceptions: None.
        '''
        return command_type == MyCobotCommandType.POWER

    def compile(
        self,
        instruction: MyCobotInstruction,
        context: CompilerContext
    ) -> Sequence[MyCobotFrame]:
        '''
            Compiles POWER instruction into POWER_ON binary frame.

            :param instruction: Parsed POWER AST instruction node.
            :param context: Active compilation context tracking arm state.
            :return: Sequence containing single POWER_ON frame.
            :exceptions: None.
        '''
        return (
            MyCobotFrame(
                self._constants.cmd_power_on,
                b'',
                self._constants.servo_delay
            ),
        )

    def get_version(self) -> str:
        '''
            Returns the compiler component version string.

            :return: The component version string.
            :exceptions: None.
        '''
        return __version__
