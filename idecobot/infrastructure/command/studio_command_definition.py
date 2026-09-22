# -*- coding: UTF-8 -*-

'''
Module
    studio_command_definition.py
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
    Defines StudioCommandDefinition class for CLI studio subcommand metadata.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from ats_utilities.option.command.data import OptionData
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StudioCommandDefinition:
    '''
        CLI subcommand metadata definition for idecobot Motion Studio and DSL Editor.

        It defines:

            :attributes:
                | COMMAND_NAME - CLI subcommand name identifier ('studio').
                | OPTION_FILE - Option flag for script file path ('--file').
                | OPTION_PORT - Option flag for serial port ('--port').
                | OPTION_VERBOSE - Option flag for verbose logging ('--verbose').
            :methods:
                | name - Returns the command name.
                | help_text - Returns the command help text.
                | options - Returns the sequence of command options.
                | __str__ - Returns the command definition as string representation.
    '''

    COMMAND_NAME: ClassVar[str] = 'studio'
    OPTION_FILE: ClassVar[str] = '--file'
    OPTION_PORT: ClassVar[str] = '--port'
    OPTION_VERBOSE: ClassVar[str] = '--verbose'

    @property
    def name(self) -> str:
        '''
            Returns the command name.

            :return: The command name.
            :exceptions: None.
        '''
        return self.COMMAND_NAME

    @property
    def help_text(self) -> str:
        '''
            Returns the command help text.

            :return: The command help text.
            :exceptions: None.
        '''
        return 'Run idecobot Motion Studio and DSL Editor graphical interface'

    @property
    def options(self) -> Sequence[OptionData]:
        '''
            Returns the command options.

            :return: Sequence of command options.
            :exceptions: None.
        '''
        return [
            OptionData(
                name=self.OPTION_FILE,
                help_text='Path to initial .cobot DSL script file',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name=self.OPTION_PORT,
                help_text='Serial communications port path or descriptor',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name=self.OPTION_VERBOSE,
                help_text='Enable verbose logging output',
                action='store_true',
                default=False,
                required=False,
                choices=None,
                nargs=None
            )
        ]

    def __str__(self) -> str:
        '''
            Returns the command definition as string representation.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
