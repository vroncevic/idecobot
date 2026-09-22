# -*- coding: UTF-8 -*-

'''
Module
    mycobot_parser.py
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
    Defines concrete MyCobotParser coordinating modular command parsers.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.model.dsl.ast.mycobot_program import MyCobotProgram
from idecobot.core.model.dsl.token.mycobot_token import MyCobotToken
from idecobot.core.model.dsl.token.mycobot_token_type import MyCobotTokenType
from idecobot.core.service.dsl.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotParser:
    '''
        Coordinates command parsers to transform DSL token streams into AST programs.

        It defines:

            :attributes:
                | _parsers - Tuple of modular command parsers.
            :methods:
                | __init__ - Initializes parser registry.
                | parse - Parses token sequence and lines into MyCobotProgram.
                | parse_statement - Dispatches statement tokens to matching parser.
                | split_lines - Splits tokens into per-statement lists.
                | get_version - Returns parser implementation version string.
    '''

    def __init__(self, parsers: Sequence[ICommandParser]) -> None:
        '''
            Initializes parser with modular command sub-parsers.

            :param parsers: Sequence of ICommandParser implementations.
            :exceptions: None.
        '''
        self._parsers: tuple[ICommandParser, ...] = tuple(parsers)

    def split_lines(self, tokens: Sequence[MyCobotToken]) -> list[list[MyCobotToken]]:
        '''
            Splits token sequence by NEWLINE into statement chunks.

            :param tokens: Full sequence of lexical tokens.
            :return: List of token lists, one per statement line.
            :exceptions: None.
        '''
        lines: list[list[MyCobotToken]] = []
        current: list[MyCobotToken] = []

        for tok in tokens:
            if tok.token_type == MyCobotTokenType.NEWLINE:
                if current:
                    lines.append(current)
                    current = []
            elif tok.token_type not in {MyCobotTokenType.COMMENT, MyCobotTokenType.EOF}:
                current.append(tok)

        if current:
            lines.append(current)

        return lines

    def parse_statement(
        self,
        stmt_tokens: Sequence[MyCobotToken],
        raw_lines: Sequence[str] = ()
    ) -> MyCobotInstruction | None:
        '''
            Dispatches statement tokens to appropriate command parser.

            :param stmt_tokens: Tokens belonging to single statement.
            :param raw_lines: Original raw text lines.
            :return: Instruction node or None if empty.
            :exceptions:
                | ValueError: Unknown command or statement syntax error.
        '''
        if not stmt_tokens:
            return None

        first: MyCobotToken = stmt_tokens[0]

        if first.token_type != MyCobotTokenType.COMMAND:
            raise ValueError(
                f'Line {first.line}: Statement must begin with command keyword, got "{first.value}".'
            )

        cmd_name: str = first.value.upper()
        raw: str = raw_lines[first.line - 1] if first.line <= len(raw_lines) else ''

        for parser in self._parsers:
            if parser.can_parse(cmd_name):
                return parser.parse(stmt_tokens, first.line, raw)

        raise ValueError(f'Line {first.line}: Unrecognized command "{cmd_name}".')

    def parse(
        self,
        tokens: Sequence[MyCobotToken],
        raw_lines: Sequence[str] = ()
    ) -> MyCobotProgram:
        '''
            Parses token sequence and raw source lines into AST program.

            :param tokens: Sequence of lexical tokens.
            :param raw_lines: Original raw source text lines.
            :return: Validated AST MyCobotProgram instance.
            :exceptions:
                | ValueError: Syntax error during statement parsing.
        '''
        grouped_lines: list[list[MyCobotToken]] = self.split_lines(tokens)
        instructions: list[MyCobotInstruction] = []

        for stmt_tokens in grouped_lines:
            inst: MyCobotInstruction | None = self.parse_statement(stmt_tokens, raw_lines)

            if inst is not None:
                instructions.append(inst)

        return MyCobotProgram(instructions=tuple(instructions))

    def get_version(self) -> str:
        '''
            Returns parser implementation version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
