# -*- coding: UTF-8 -*-

'''
Module
    test_storage_constants.py
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
    Unit tests for StorageConstants immutable configuration model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from idecobot.infrastructure.storage.storage_constants import StorageConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStorageConstants(TestCase):
    '''
        Test cases verifying StorageConstants defaults and immutability.

        It defines:

            :methods:
                | setUp - Initializes StorageConstants instance.
                | test_default_values - Verifies standard .cobot extension and modes.
                | test_immutability - Verifies FrozenInstanceError on modification attempt.
                | test_filetypes_filter - Verifies dialog filetypes structure.
    '''

    def setUp(self) -> None:
        '''
            Sets up StorageConstants instance before each test.
        '''
        self.constants: StorageConstants = StorageConstants()

    def test_default_values(self) -> None:
        '''
            Verifies standard .cobot extension and file encoding.
        '''
        self.assertEqual(self.constants.file_extension, '.cobot')
        self.assertEqual(self.constants.backup_extension, '.bak')
        self.assertEqual(self.constants.encoding, 'utf-8')
        self.assertEqual(self.constants.read_mode, 'r')
        self.assertEqual(self.constants.write_mode, 'w')

    def test_immutability(self) -> None:
        '''
            Verifies FrozenInstanceError when attempting attribute mutation.
        '''
        with self.assertRaises(FrozenInstanceError):
            setattr(self.constants, 'file_extension', '.other')

    def test_filetypes_filter(self) -> None:
        '''
            Verifies file dialog type filters.
        '''
        self.assertIn(('myCobot Scripts', '*.cobot'), self.constants.filetypes)
        self.assertIn(('All Files', '*.*'), self.constants.filetypes)


if __name__ == '__main__':
    main()
