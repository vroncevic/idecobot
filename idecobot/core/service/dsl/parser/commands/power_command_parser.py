# -*- coding: UTF-8 -*-

'''
Module
    power_command_parser.py
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
    Defines PowerCommandParser parsing POWER statements.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from idecobot.core.model.dsl.ast.mycobot_command_type import MyCobotCommandType
from idecobot.core.model.dsl.ast.mycobot_instruction import MyCobotInstruction
from idecobot.core.model.dsl.token.mycobot_token import MyCobotToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PowerCommandParser:
    '''
        Parses POWER statements into AST instruction nodes.

        It defines:

            :attributes:
                | COMMAND_NAME - Command keyword identifier string ('POWER').
            :methods:
                | can_parse - Checks if command is POWER.
                | parse - Parses POWER tokens.
    '''

    COMMAND_NAME: ClassVar[str] = 'POWER'

    def can_parse(self, command_name: str) -> bool:
        '''
            Checks if command is POWER.

            :param command_name: Command keyword string.
            :return: True if command is POWER, False otherwise.
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
            Parses POWER tokens into MyCobotInstruction.

            :param tokens: Sequence of tokens in statement.
            :param line_number: Source line number.
            :param raw_text: Raw statement text.
            :return: MyCobotInstruction instance.
            :exceptions: None.
        '''
        _ = tokens

        return MyCobotInstruction(
            command_type=MyCobotCommandType.POWER,
            line_number=line_number,
            parameters={},
            raw_text=raw_text
        )
