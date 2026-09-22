# -*- coding: UTF-8 -*-

'''
Module
    storage_constants.py
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
    Defines StorageConstants immutable dataclass for script file operations.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class StorageConstants:
    '''
        Immutable configuration constants for script file storage and validation.

        It defines:

            :attributes:
                | file_extension - Standard DSL script file extension ('.cobot').
                | backup_extension - Backup file extension ('.bak').
                | file_filter_name - Descriptive label for file dialog filters.
                | filetypes - Tuple of filter pairs for file dialogs.
                | encoding - Text file character encoding ('utf-8').
                | read_mode - File mode for reading operations ('r').
                | write_mode - File mode for writing operations ('w').
    '''

    file_extension: str = '.cobot'
    backup_extension: str = '.bak'
    file_filter_name: str = 'myCobot Scripts'
    filetypes: tuple[tuple[str, str], ...] = (
        ('myCobot Scripts', '*.cobot'),
        ('All Files', '*.*')
    )
    encoding: str = 'utf-8'
    read_mode: str = 'r'
    write_mode: str = 'w'
