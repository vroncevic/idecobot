# -*- coding: UTF-8 -*-

'''
Module
    imycobot_parser.py
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
    Defines structural interface protocol for the myCobot DSL parser.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.token.mycobot_token import MyCobotToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMyCobotParser(Protocol):
    '''
        Defines structural interface protocol for parsing myCobot DSL tokens into AST.

        It defines:

            :methods:
                | parse - Parses token sequence and raw source lines into AST program.
                | parse_statement - Parses a single statement token sequence into an AST instruction.
    '''

    def parse(
        self,
        tokens: Sequence[MyCobotToken],
        raw_lines: Sequence[str]
    ) -> MyCobotProgram:
        '''
            Parses token sequence and raw source lines into AST program.

            :param tokens: Sequence of lexical tokens.
            :param raw_lines: Original raw source text lines.
            :return: Validated AST MyCobotProgram instance.
        '''

    def parse_statement(
        self,
        stmt_tokens: Sequence[MyCobotToken],
        raw_lines: Sequence[str]
    ) -> MyCobotInstruction | None:
        '''
            Parses a single statement token sequence into an AST instruction.

            :param stmt_tokens: Tokens belonging to a single statement.
            :param raw_lines: Original raw source text lines.
            :return: Parsed MyCobotInstruction node or None if empty.
        '''
