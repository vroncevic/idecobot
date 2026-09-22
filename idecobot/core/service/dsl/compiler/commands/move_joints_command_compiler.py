# -*- coding: UTF-8 -*-

'''
Module
    move_joints_command_compiler.py
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
    Defines MoveJointsCommandCompiler compiling MOVE_JOINTS instructions.
'''

from __future__ import annotations

from collections.abc import Sequence
from struct import pack

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.service.dsl.compiler.compiler_context import CompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MoveJointsCommandCompiler:
    '''
        Compiles MOVE_JOINTS instructions into SEND_ANGLES binary frames.

        It defines:

            :attributes:
                | _constants - Injected ProtocolConstants low-level framing parameters.
                | _default_delay - Frame delay after move completion in seconds.
            :methods:
                | __init__ - Initializes compiler with protocol constants and move delay.
                | can_compile - Verifies if instruction command type is MOVE_JOINTS.
                | compile - Updates context angles and compiles SEND_ANGLES frame.
                | get_version - Returns the compiler component version string.
    '''

    _constants: ProtocolConstants
    _default_delay: float

    def __init__(self, constants: ProtocolConstants, default_delay: float) -> None:
        '''
            Initializes MoveJointsCommandCompiler with protocol constants and delay.

            :param constants: Injected ProtocolConstants instance.
            :param default_delay: Delay in seconds following joint motion.
            :exceptions: None.
        '''
        self._constants = constants
        self._default_delay = default_delay

    def can_compile(self, command_type: MyCobotCommandType) -> bool:
        '''
            Verifies if instruction command type is MOVE_JOINTS.

            :param command_type: MyCobotCommandType enum value.
            :return: True if command type is MOVE_JOINTS, False otherwise.
            :exceptions: None.
        '''
        return command_type == MyCobotCommandType.MOVE_JOINTS

    def compile(
        self,
        instruction: MyCobotInstruction,
        context: CompilerContext
    ) -> Sequence[MyCobotFrame]:
        '''
            Updates context joint angles and compiles SEND_ANGLES frame.

            :param instruction: Parsed MOVE_JOINTS AST instruction node.
            :param context: Active compilation context tracking arm state.
            :return: Sequence containing single SEND_ANGLES frame.
            :exceptions: None.
        '''
        for idx in range(6):
            key: str = f'j{idx + 1}'

            if key in instruction.parameters:
                context.angles[idx] = float(instruction.parameters[key])

        scaled: list[int] = [
            int(round(ang * self._constants.angle_scale_factor))
            for ang in context.angles
        ]
        move_speed: int = int(instruction.parameters.get('speed', context.speed))
        payload: bytes = pack(
            self._constants.format_angles_command,
            scaled[0], scaled[1], scaled[2],
            scaled[3], scaled[4], scaled[5],
            move_speed & self._constants.byte_mask
        )

        return (
            MyCobotFrame(
                self._constants.cmd_send_angles,
                payload,
                self._default_delay
            ),
        )

    def get_version(self) -> str:
        '''
            Returns the compiler component version string.

            :return: The component version string.
            :exceptions: None.
        '''
        return __version__
