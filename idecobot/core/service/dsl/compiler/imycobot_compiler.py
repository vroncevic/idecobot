# -*- coding: UTF-8 -*-

'''
Module
    imycobot_compiler.py
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
    Defines structural interface protocol for the myCobot DSL compiler.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMyCobotCompiler(Protocol):
    '''
        Defines structural interface protocol for compiling AST into serial frames.

        It defines:

            :methods:
                | compile - Translates MyCobotProgram AST into sequence of MyCobotFrames.
                | compile_instruction - Compiles a single AST instruction into serial frames.
                | get_version - Returns the compiler component version string.
    '''

    def compile(self, program: MyCobotProgram) -> Sequence[MyCobotFrame]:
        '''
            Translates MyCobotProgram AST into sequence of MyCobotFrames.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of compiled binary MyCobotFrame objects.
        '''

    def compile_instruction(self, instruction: MyCobotInstruction) -> Sequence[MyCobotFrame]:
        '''
            Compiles a single AST instruction into serial frames.

            :param instruction: Single MyCobotInstruction node.
            :return: Sequence of compiled binary MyCobotFrame objects.
        '''

    def get_version(self) -> str:
        '''
            Returns the compiler component version string.

            :return: The component version string.
            :exceptions: None.
        '''
