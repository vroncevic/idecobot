# -*- coding: UTF-8 -*-

'''
Module
    workspace_constants_test.py
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
    Unit tests for WorkspaceConstants configuration dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from os.path import exists
from unittest import TestCase, main

from idecobot.infrastructure.storage.workspace_constants import WorkspaceConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceConstants(TestCase):
    '''
        Test cases verifying WorkspaceConstants defaults and immutability.

        It defines:

            :methods:
                | setUp - Initializes WorkspaceConstants instance.
                | test_default_values - Verifies standard workspace dir, archive path, and extension.
                | test_archive_exists - Verifies bundled examples.tgz exists at resolved path.
                | test_immutability - Verifies FrozenInstanceError on modification attempt.
    '''

    def setUp(self) -> None:
        '''
            Sets up WorkspaceConstants instance before each test.
        '''
        self.constants: WorkspaceConstants = WorkspaceConstants()

    def test_default_values(self) -> None:
        '''
            Verifies standard workspace dir, archive path, and extension.
        '''
        self.assertEqual(self.constants.workspace_dir, '~/.idecobot/workspace')
        self.assertEqual(self.constants.archive_mode, 'r:gz')
        self.assertEqual(self.constants.file_extension, '.cobot')

    def test_archive_exists(self) -> None:
        '''
            Verifies bundled examples.tgz exists at resolved path.
        '''
        self.assertTrue(exists(self.constants.archive_path))

    def test_immutability(self) -> None:
        '''
            Verifies FrozenInstanceError on modification attempt.
        '''
        with self.assertRaises(FrozenInstanceError):
            self.constants.workspace_dir = '/tmp/other'


if __name__ == '__main__':
    main()
