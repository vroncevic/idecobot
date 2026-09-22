# -*- coding: UTF-8 -*-

'''
Module
    script_storage_service.py
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
    Defines ScriptStorageService implementing persistence and loading of .cobot scripts.
'''

from __future__ import annotations

from os.path import exists, splitext

from idecobot.infrastructure.storage.storage_constants import StorageConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScriptStorageService:
    '''
        Handles persistence, reading, and validation of robot DSL .cobot script files.

        It defines:

            :attributes:
                | _constants - Injected StorageConstants configuration.
            :methods:
                | __init__ - Initializes storage service with injected constants.
                | constants - Returns injected StorageConstants instance.
                | load_script - Reads script text content from file.
                | save_script - Writes script text content to file.
                | validate_extension - Verifies file has .cobot extension.
    '''

    _constants: StorageConstants

    def __init__(self, constants: StorageConstants) -> None:
        '''
            Initializes ScriptStorageService with configuration constants.

            :param constants: Injected StorageConstants instance.
            :exceptions: None.
        '''
        self._constants = constants

    @property
    def constants(self) -> StorageConstants:
        '''
            Returns the injected storage configuration constants.

            :return: StorageConstants instance.
            :exceptions: None.
        '''
        return self._constants

    def validate_extension(self, file_path: str) -> bool:
        '''
            Verifies file has .cobot extension.

            :param file_path: Path string to check.
            :return: True if ends with .cobot, False otherwise.
            :exceptions: None.
        '''
        _, ext = splitext(file_path)

        return ext.lower() == self._constants.file_extension

    def load_script(self, file_path: str) -> str:
        '''
            Reads script text content from file.

            :param file_path: Absolute or relative path to .cobot script file.
            :return: Script source code string.
            :exceptions:
                | FileNotFoundError: Specified file does not exist.
                | ValueError: Invalid file extension.
        '''
        if not exists(file_path):
            raise FileNotFoundError(f'Script file not found: {file_path}')

        if not self.validate_extension(file_path):
            raise ValueError(
                f'Expected {self._constants.file_extension} file, got: {file_path}'
            )

        with open(file_path, self._constants.read_mode, encoding=self._constants.encoding) as handle:
            return handle.read()

    def save_script(self, file_path: str, content: str) -> bool:
        '''
            Writes script text content to file.

            :param file_path: Absolute or relative path to .cobot script file.
            :param content: Script source code text to persist.
            :return: True if saved successfully, False otherwise.
            :exceptions: None.
        '''
        try:
            target_path: str = file_path

            if not self.validate_extension(target_path):
                target_path = f'{target_path}{self._constants.file_extension}'

            with open(target_path, self._constants.write_mode, encoding=self._constants.encoding) as handle:
                handle.write(content)

            return True

        except (OSError, IOError):
            return False

    def get_version(self) -> str:
        '''
            Returns storage implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

