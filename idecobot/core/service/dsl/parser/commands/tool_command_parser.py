# -*- coding: UTF-8 -*-

'''
Module
    tool_command_parser.py
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
    Defines ToolCommandParser parsing TOOL statements.
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
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolCommandParser:
    '''
        Parses TOOL statements into AST instruction nodes.

        It defines:

            :attributes:
                | COMMAND_NAME - Command keyword identifier string ('TOOL').
                | _grammar - Injected DslGrammarConstants grammar specification.
            :methods:
                | __init__ - Initializes parser with grammar constants.
                | can_parse - Checks if command is TOOL.
                | parse - Parses TOOL tokens.
    '''

    COMMAND_NAME: ClassVar[str] = 'TOOL'

    _grammar: DslGrammarConstants

    def __init__(self, grammar: DslGrammarConstants) -> None:
        '''
            Initializes ToolCommandParser with grammar constants.

            :param grammar: Injected DslGrammarConstants instance.
            :exceptions: None.
        '''
        self._grammar = grammar

    def can_parse(self, command_name: str) -> bool:
        '''
            Checks if command is TOOL.

            :param command_name: Command keyword string.
            :return: True if command is TOOL, False otherwise.
            :exceptions: None.
        '''
        return command_name == self.COMMAND_NAME

    def parse(
        self,
        tokens: Sequence[MyCobotToken],
        line_number: int,
        raw_text: str
    ) -> MyCobotInstruction:
        '''
            Parses TOOL tokens into MyCobotInstruction.

            :param tokens: Sequence of tokens in statement.
            :param line_number: Source line number.
            :param raw_text: Raw statement text.
            :return: MyCobotInstruction instance.
            :exceptions:
                | ValueError: Invalid syntax or unrecognized tool action.
        '''
        if len(tokens) < 2:
            raise ValueError(
                f'Line {line_number}: TOOL command expects action GRIP or RELEASE.'
            )

        action: str = tokens[1].value.upper()

        if action not in self._grammar.tool_actions:
            raise ValueError(
                f'Line {line_number}: Invalid tool action "{action}". Expected GRIP or RELEASE.'
            )

        speed: float = self._grammar.default_tool_speed
        idx: int = 2

        while idx < len(tokens):
            if (
                tokens[idx].token_type == MyCobotTokenType.IDENTIFIER
                and tokens[idx].value.upper() == self._grammar.cmd_speed
                and idx + 2 < len(tokens)
                and tokens[idx + 1].token_type == MyCobotTokenType.COLON
                and tokens[idx + 2].token_type == MyCobotTokenType.NUMBER
            ):
                speed = float(tokens[idx + 2].value)
                idx += 3
            else:
                idx += 1

        return MyCobotInstruction(
            command_type=MyCobotCommandType.TOOL,
            line_number=line_number,
            parameters={
                self._grammar.param_action: action,
                self._grammar.param_speed: speed
            },
            raw_text=raw_text
        )
