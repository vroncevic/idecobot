# -*- coding: UTF-8 -*-

'''
Module
    mycobot_compiler.py
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
    Defines MyCobotCompiler coordinating modular command compilers to generate binary frames.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.service.dsl.compiler.commands.icommand_compiler import ICommandCompiler
from idecobot.core.service.dsl.compiler.compiler_context import CompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotCompiler:
    '''
        Coordinates command compilers to transform AST instructions into binary protocol frames.

        It defines:

            :attributes:
                | _compilers - Sequence of injected ICommandCompiler instances.
                | _default_speed - Baseline velocity percentage.
            :methods:
                | __init__ - Initializes compiler with injected command compilers and baseline velocity.
                | compile - Compiles entire MyCobotProgram into sequence of MyCobotFrames.
                | compile_instruction - Compiles a single AST instruction into serial frames.
                | get_version - Returns compiler component version string.
    '''

    _compilers: tuple[ICommandCompiler, ...]
    _default_speed: int

    def __init__(self, compilers: Sequence[ICommandCompiler], default_speed: int) -> None:
        '''
            Initializes compiler with injected command compilers and motion parameters.

            :param compilers: Sequence of ICommandCompiler implementations.
            :param default_speed: Baseline velocity percentage (1-100).
            :exceptions: None.
        '''
        self._compilers = tuple(compilers)
        self._default_speed = default_speed

    def compile(self, program: MyCobotProgram) -> Sequence[MyCobotFrame]:
        '''
            Translates MyCobotProgram AST into sequence of MyCobotFrames.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of compiled binary MyCobotFrame objects.
            :exceptions: None.
        '''
        context: CompilerContext = CompilerContext(default_speed=self._default_speed)

        for inst in program.instructions:
            for compiler in self._compilers:
                if compiler.can_compile(inst.command_type):
                    for frame in compiler.compile(inst, context):
                        context.add_frame(frame)

                    break

        return tuple(context.frames)

    def compile_instruction(self, instruction: MyCobotInstruction) -> Sequence[MyCobotFrame]:
        '''
            Compiles a single AST instruction into a sequence of binary frames.

            :param instruction: Single MyCobotInstruction node.
            :return: Sequence of compiled MyCobotFrame instances.
            :exceptions: None.
        '''
        return self.compile(MyCobotProgram(instructions=(instruction,)))

    def get_version(self) -> str:
        '''
            Returns the compiler component version string.

            :return: The component version string.
            :exceptions: None.
        '''
        return __version__
