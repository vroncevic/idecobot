# -*- coding: UTF-8 -*-

'''
Module
    move_command_parser.py
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
    Defines MoveCommandParser parsing MOVE joint and cartesian statements.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.model.dsl.token.dsl_grammar_constants import DslGrammarConstants
from idecobot.core.model.dsl.token.mycobot_token import MyCobotToken
from idecobot.core.model.dsl.token.mycobot_token_type import MyCobotTokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MoveCommandParser:
    '''
        Parses MOVE statements into AST instruction nodes.

        It defines:

            :attributes:
                | COMMAND_NAME - Command keyword identifier string ('MOVE').
                | _grammar - Injected DslGrammarConstants grammar specification.
            :methods:
                | __init__ - Initializes parser with grammar constants.
                | can_parse - Checks if command is MOVE.
                | extract_pairs - Extracts key-value pairs from token stream.
                | determine_type - Determines instruction type from parsed keys.
                | parse - Parses MOVE tokens into MyCobotInstruction.
                | get_version - Returns parser version string.
    '''

    COMMAND_NAME: ClassVar[str] = 'MOVE'

    _grammar: DslGrammarConstants

    def __init__(self, grammar: DslGrammarConstants) -> None:
        '''
            Initializes MoveCommandParser with grammar constants.

            :param grammar: Injected DslGrammarConstants instance.
            :exceptions: None.
        '''
        self._grammar = grammar

    def can_parse(self, command_name: str) -> bool:
        '''
            Checks if command is MOVE.

            :param command_name: Command keyword string.
            :return: True if command is MOVE, False otherwise.
            :exceptions: None.
        '''
        return command_name == self.COMMAND_NAME

    def extract_pairs(
        self,
        tokens: Sequence[MyCobotToken],
        line_number: int
    ) -> dict[str, float]:
        '''
            Extracts key-value pairs from tokens following the command.

            :param tokens: Sequence of tokens in statement.
            :param line_number: Source line number for error reporting.
            :return: Dictionary of parsed lowercase parameters.
            :exceptions:
                | ValueError: Invalid syntax or missing numerical value.
        '''
        params: dict[str, float] = {}
        idx: int = 1

        while idx < len(tokens):
            tok: MyCobotToken = tokens[idx]

            if tok.token_type != MyCobotTokenType.IDENTIFIER:
                idx += 1
                continue

            key: str = tok.value.upper()

            if idx + 2 >= len(tokens) or tokens[idx + 1].token_type != MyCobotTokenType.COLON:
                raise ValueError(
                    f'Line {line_number}: Expected ":" after axis identifier "{key}".'
                )

            val_tok: MyCobotToken = tokens[idx + 2]

            if val_tok.token_type != MyCobotTokenType.NUMBER:
                raise ValueError(
                    f'Line {line_number}: Expected numerical value for axis "{key}".'
                )

            params[key.lower()] = float(val_tok.value)
            idx += 3

        return params

    def determine_type(
        self,
        params: dict[str, float],
        line_number: int
    ) -> MyCobotCommandType:
        '''
            Determines command type (MOVE_JOINTS or MOVE_COORDS) from keys.

            :param params: Extracted parameter dictionary.
            :param line_number: Source line number for error reporting.
            :return: MyCobotCommandType enum value.
            :exceptions:
                | ValueError: Conflicting or missing coordinate parameters.
        '''
        keys: set[str] = {k.upper() for k in params.keys()}
        has_joints: bool = bool(keys & self._grammar.joint_axes)
        has_cart: bool = bool(keys & self._grammar.cartesian_axes)

        if has_joints and has_cart:
            raise ValueError(
                f'Line {line_number}: Cannot mix joint and cartesian coordinates.'
            )

        if has_joints:
            return MyCobotCommandType.MOVE_JOINTS

        if has_cart:
            return MyCobotCommandType.MOVE_COORDS

        raise ValueError(
            f'Line {line_number}: MOVE command requires at least one coordinate.'
        )

    def parse(
        self,
        tokens: Sequence[MyCobotToken],
        line_number: int,
        raw_text: str
    ) -> MyCobotInstruction:
        '''
            Parses MOVE tokens into MyCobotInstruction.

            :param tokens: Sequence of tokens in statement.
            :param line_number: Source line number.
            :param raw_text: Raw statement text.
            :return: MyCobotInstruction instance.
            :exceptions:
                | ValueError: Invalid syntax or conflicting coordinates.
        '''
        params: dict[str, float] = self.extract_pairs(tokens, line_number)
        cmd_type: MyCobotCommandType = self.determine_type(params, line_number)

        return MyCobotInstruction(
            command_type=cmd_type,
            line_number=line_number,
            parameters=params,
            raw_text=raw_text
        )

    def get_version(self) -> str:
        '''
            Returns parser version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
