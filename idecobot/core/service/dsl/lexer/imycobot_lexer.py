# -*- coding: UTF-8 -*-

'''
Module
    imycobot_lexer.py
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
    Defines structural interface protocol for the myCobot DSL lexical analyzer.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

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
class IMyCobotLexer(Protocol):
    '''
        Defines protocol IMyCobotLexer for tokenizing DSL source strings.

        It defines:

            :methods:
                | tokenize - Tokenizes source text into sequence of tokens.
                | tokenize_line - Tokenizes a single line of DSL source code.
                | get_version - Returns protocol version string.
    '''

    def tokenize(self, source: str) -> Sequence[MyCobotToken]:
        '''
            Tokenizes source text into sequence of tokens.

            :param source: Raw DSL source code string.
            :return: Sequence of tokenized symbols.
        '''

    def tokenize_line(self, line: str, line_number: int = 1) -> Sequence[MyCobotToken]:
        '''
            Tokenizes a single line of DSL source code.

            :param line: Single raw DSL text line.
            :param line_number: 1-indexed line number for token location tracking.
            :return: Sequence of tokenized symbols for the line.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
        '''

