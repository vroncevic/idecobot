# -*- coding: UTF-8 -*-

'''
Module
    studio_command_executor.py
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
    Defines StudioCommandExecutor class for launching the IDE GUI.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar

from ats_utilities.utils.reflection import to_str

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.command.icommand_definition import ICommandDefinition
from idecobot.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StudioCommandExecutor:
    '''
        Command executor strategy for launching idecobot Motion Studio and DSL Editor GUI.

        It defines:

            :attributes:
                | PARAM_FILE - Parameter name key for file option ('file').
                | PARAM_PORT - Parameter name key for port option ('port').
                | definition - The command CLI metadata definition.
                | gui - The GUI presentation adapter instance.
            :methods:
                | __init__ - Initializes the studio command executor with injected abstractions.
                | execute - Executes the studio command.
                | get_definition - Returns the command definition metadata.
                | __str__ - Returns string representation.
    '''

    PARAM_FILE: ClassVar[str] = 'file'
    PARAM_PORT: ClassVar[str] = 'port'

    definition: ICommandDefinition
    gui: IGUI

    def __init__(self, definition: ICommandDefinition, gui: IGUI) -> None:
        '''
            Initializes the command executor with injected abstractions.

            :param definition: Injected ICommandDefinition metadata.
            :param gui: Injected IGUI presentation adapter.
            :exceptions: None.
        '''
        self.definition = definition
        self.gui = gui

    def execute(self, *, params: Mapping[str, object], service: IService) -> Mapping[str, object]:
        '''
            Executes the studio subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: Injected core IService facade.
            :return: Mapping containing execution returncode and output.
            :exceptions: None.
        '''
        if not self.gui.is_initialized() or not service.is_initialized():
            return {
                'returncode': 1,
                'stdout': '',
                'stderr': 'studio_command_executor::execute - gui or service not initialized'
            }

        try:
            file_path: object = params.get(self.PARAM_FILE)

            if file_path is not None and isinstance(file_path, str) and file_path:
                self.gui.load_file(file_path)

            port: object = params.get(self.PARAM_PORT)

            if port is not None and isinstance(port, str) and port:
                self.gui.connect_port(port)

            self.gui.start()
            return {'returncode': 0, 'stdout': 'Studio closed successfully', 'stderr': ''}

        except (RuntimeError, ValueError, OSError) as exc:
            return {'returncode': 1, 'stdout': '', 'stderr': f'studio_command_executor::execute - {exc}'}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self.definition

    def __str__(self) -> str:
        '''
            Returns string representation.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
