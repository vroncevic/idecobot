# -*- coding: UTF-8 -*-

'''
Module
    test_storage.py
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
    Unit tests for ScriptStorageService file operations and extension validation.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from unittest import TestCase, main

from idecobot.infrastructure.storage.script_storage_service import ScriptStorageService
from idecobot.infrastructure.storage.storage_constants import StorageConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScriptStorageService(TestCase):
    '''
        Test cases for .cobot script persistence and extension validation.

        It defines:

            :methods:
                | test_extension_validation - Tests .cobot extension checking.
                | test_save_and_load_roundtrip - Tests write and read of script file.
                | test_missing_file_raises - Tests error handling for non-existent file.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture and temporary file path.
        '''
        self.constants = StorageConstants()
        self.storage = ScriptStorageService(constants=self.constants)
        self.temp_file = '/tmp/test_robot_script.cobot'

    def tearDown(self) -> None:
        '''
            Cleans up temporary files.
        '''
        if exists(self.temp_file):
            remove(self.temp_file)

    def test_extension_validation(self) -> None:
        '''
            Tests extension checking.
        '''
        self.assertTrue(self.storage.validate_extension('demo.cobot'))
        self.assertTrue(self.storage.validate_extension('/path/to/demo.COBOT'))
        self.assertFalse(self.storage.validate_extension('demo.arm'))
        self.assertFalse(self.storage.validate_extension('demo.txt'))
        self.assertFalse(self.storage.validate_extension('demo.json'))

    def test_save_and_load_roundtrip(self) -> None:
        '''
            Tests persisting content and reading back.
        '''
        script = 'HOME\nMOVE J1:10 J2:20 SPEED:50'
        success = self.storage.save_script(self.temp_file, script)
        self.assertTrue(success)

        loaded = self.storage.load_script(self.temp_file)
        self.assertEqual(loaded, script)

    def test_missing_file_raises(self) -> None:
        '''
            Tests that reading non-existent file raises FileNotFoundError.
        '''
        with self.assertRaises(FileNotFoundError):
            self.storage.load_script('/tmp/non_existent_file_xyz.cobot')


if __name__ == '__main__':
    main()
