# -*- coding: UTF-8 -*-

'''
Module
    imycobot_dsl_service.py
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
    Defines structural interface protocol for the unified myCobot DSL service.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.diagnostic.mycobot_diagnostic import MyCobotDiagnostic
from idecobot.core.model.dsl.token.mycobot_token import MyCobotToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMyCobotDslService(Protocol):
    '''
        Defines structural interface protocol for tokenizing, parsing, linting, and compiling DSL.

        It defines:

            :methods:
                | tokenize - Converts raw DSL script into lexical token sequence.
                | parse - Parses script text into AST program.
                | lint - Evaluates AST program against semantic rules.
                | compile - Translates AST program into binary protocol frames.
                | validate - End-to-end parse and lint returning AST and diagnostics.
                | get_version - Returns protocol version string.
    '''

    def tokenize(self, source: str) -> Sequence[MyCobotToken]:
        '''
            Converts raw DSL script into lexical token sequence.

            :param source: Raw DSL source code string.
            :return: Sequence of lexical tokens.
        '''

    def parse(self, source: str) -> MyCobotProgram:
        '''
            Parses script text into AST program.

            :param source: Raw DSL source code string.
            :return: Parsed MyCobotProgram AST instance.
        '''

    def lint(self, program: MyCobotProgram) -> Sequence[MyCobotDiagnostic]:
        '''
            Evaluates AST program against semantic rules.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of detected diagnostics.
        '''

    def compile(self, program: MyCobotProgram) -> Sequence[MyCobotFrame]:
        '''
            Translates AST program into binary protocol frames.

            :param program: Parsed MyCobotProgram AST instance.
            :return: Sequence of compiled MyCobotFrame objects.
        '''

    def validate(self, source: str) -> tuple[MyCobotProgram | None, Sequence[MyCobotDiagnostic]]:
        '''
            End-to-end parse and lint returning AST and diagnostics.

            :param source: Raw DSL source code string.
            :return: Tuple of optional program AST and sequence of diagnostics.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
        '''

