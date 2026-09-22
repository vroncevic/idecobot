# -*- coding: UTF-8 -*-

'''
Module
    mycobot_lexer.py
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
    Defines MyCobotLexer implementation converting source code into token stream.
'''

from __future__ import annotations

from collections.abc import Sequence
from re import compile as re_compile, Pattern
from typing import ClassVar

from idecobot.core.model.dsl.token.dsl_grammar_constants import DslGrammarConstants
from idecobot.core.model.dsl.token.mycobot_token import MyCobotToken
from idecobot.core.model.dsl.token.mycobot_token_type import MyCobotTokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotLexer:
    '''
        Concrete lexical analyzer for myCobot DSL script code.

        It defines:

            :attributes:
                | GROUP_COMMENT - Regex match group name for single-line comments.
                | GROUP_NUMBER - Regex match group name for numeric literals.
                | GROUP_COLON - Regex match group name for colon delimiters.
                | GROUP_IDENT - Regex match group name for alphanumeric identifiers.
                | GROUP_NEWLINE - Regex match group name for newline delimiters.
                | GROUP_SKIP - Regex match group name for whitespace skipped characters.
                | GROUP_MISMATCH - Regex match group name for unexpected characters.
                | _grammar - Injected DslGrammarConstants specification.
                | _re_token - Master regular expression pattern matching symbols.
            :methods:
                | __init__ - Initializes lexer with grammar constants.
                | tokenize - Tokenizes source text into list of tokens.
                | tokenize_line - Tokenizes a single line of DSL source code.
                | get_version - Returns lexer version string.
    '''

    GROUP_COMMENT: ClassVar[str] = 'COMMENT'
    GROUP_NUMBER: ClassVar[str] = 'NUMBER'
    GROUP_COLON: ClassVar[str] = 'COLON'
    GROUP_IDENT: ClassVar[str] = 'IDENT'
    GROUP_NEWLINE: ClassVar[str] = 'NEWLINE'
    GROUP_SKIP: ClassVar[str] = 'SKIP'
    GROUP_MISMATCH: ClassVar[str] = 'MISMATCH'

    _re_token: Pattern[str] = re_compile(
        r'(?P<COMMENT>#[^\r\n]*)'
        r'|(?P<NUMBER>[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)'
        r'|(?P<COLON>:)'
        r'|(?P<IDENT>[A-Za-z_][A-Za-z0-9_]*)'
        r'|(?P<NEWLINE>\r?\n)'
        r'|(?P<SKIP>[ \t]+)'
        r'|(?P<MISMATCH>.)'
    )

    _grammar: DslGrammarConstants

    def __init__(self, grammar: DslGrammarConstants) -> None:
        '''
            Initializes MyCobotLexer with grammar constants.

            :param grammar: Injected DslGrammarConstants instance.
            :exceptions: None.
        '''
        self._grammar = grammar

    def tokenize(self, source: str) -> Sequence[MyCobotToken]:
        '''
            Tokenizes source text into sequence of tokens.

            :param source: Raw DSL source code string.
            :return: Sequence of tokenized symbols.
            :exceptions:
                | ValueError: Invalid syntax or unrecognized token encountered.
        '''
        tokens: list[MyCobotToken] = []
        line_num: int = 1
        line_start: int = 0

        for match in self._re_token.finditer(source):
            kind: str | None = match.lastgroup
            val: str = match.group()
            col: int = match.start() - line_start + 1

            match kind:
                case self.GROUP_NEWLINE:
                    tokens.append(MyCobotToken(MyCobotTokenType.NEWLINE, val, line_num, col))
                    line_num += 1
                    line_start = match.end()
                case self.GROUP_COMMENT:
                    tokens.append(MyCobotToken(MyCobotTokenType.COMMENT, val, line_num, col))
                case self.GROUP_NUMBER:
                    tokens.append(MyCobotToken(MyCobotTokenType.NUMBER, val, line_num, col))
                case self.GROUP_COLON:
                    tokens.append(MyCobotToken(MyCobotTokenType.COLON, val, line_num, col))
                case self.GROUP_IDENT:
                    upper_val: str = val.upper()
                    token_type: MyCobotTokenType = (
                        MyCobotTokenType.COMMAND
                        if upper_val in self._grammar.commands
                        else MyCobotTokenType.IDENTIFIER
                    )
                    tokens.append(MyCobotToken(token_type, upper_val, line_num, col))
                case self.GROUP_SKIP:
                    continue
                case self.GROUP_MISMATCH:
                    raise ValueError(f'Unexpected character {val!r} at line {line_num}, column {col}')

        tokens.append(MyCobotToken(MyCobotTokenType.EOF, '', line_num, 0))

        return tuple(tokens)

    def tokenize_line(self, line: str, line_number: int = 1) -> Sequence[MyCobotToken]:
        '''
            Tokenizes a single line of DSL source code.

            :param line: Single raw DSL text line.
            :param line_number: 1-indexed line number for token location tracking.
            :return: Sequence of tokenized symbols for the line.
            :exceptions:
                | ValueError: Invalid syntax or unrecognized token encountered.
        '''
        tokens: list[MyCobotToken] = []

        for match in self._re_token.finditer(line):
            kind: str | None = match.lastgroup
            val: str = match.group()
            col: int = match.start() + 1

            match kind:
                case self.GROUP_NEWLINE | self.GROUP_SKIP:
                    continue
                case self.GROUP_COMMENT:
                    tokens.append(MyCobotToken(MyCobotTokenType.COMMENT, val, line_number, col))
                case self.GROUP_NUMBER:
                    tokens.append(MyCobotToken(MyCobotTokenType.NUMBER, val, line_number, col))
                case self.GROUP_COLON:
                    tokens.append(MyCobotToken(MyCobotTokenType.COLON, val, line_number, col))
                case self.GROUP_IDENT:
                    upper_val: str = val.upper()
                    token_type: MyCobotTokenType = (
                        MyCobotTokenType.COMMAND
                        if upper_val in self._grammar.commands
                        else MyCobotTokenType.IDENTIFIER
                    )
                    tokens.append(MyCobotToken(token_type, upper_val, line_number, col))
                case self.GROUP_MISMATCH:
                    raise ValueError(f'Unexpected character {val!r} at line {line_number}, column {col}')

        return tuple(tokens)

    def get_version(self) -> str:
        '''
            Returns lexer version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

