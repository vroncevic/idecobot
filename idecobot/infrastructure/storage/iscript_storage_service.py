# -*- coding: UTF-8 -*-

'''
Module
    iscript_storage_service.py
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
    Defines structural interface protocol for loading and saving DSL .cobot scripts.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScriptStorageService(Protocol):
    '''
        Defines structural interface protocol for script file storage.

        It defines:

            :methods:
                | load_script - Reads script text content from file.
                | save_script - Writes script text content to file.
                | validate_extension - Verifies file has .cobot extension.
    '''

    def load_script(self, file_path: str) -> str:
        '''
            Reads script text content from file.

            :param file_path: Absolute or relative path to .cobot script file.
            :return: Script source code string.
        '''

    def save_script(self, file_path: str, content: str) -> bool:
        '''
            Writes script text content to file.

            :param file_path: Absolute or relative path to .cobot script file.
            :param content: Script source code text to persist.
            :return: True if saved successfully, False otherwise.
        '''

    def validate_extension(self, file_path: str) -> bool:
        '''
            Verifies file has .cobot extension.

            :param file_path: Path string to check.
            :return: True if ends with .cobot, False otherwise.
        '''

    def get_version(self) -> str:
        '''
            Returns storage protocol version string.

            :return: Component version string.
        '''
