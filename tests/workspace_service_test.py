# -*- coding: UTF-8 -*-

'''
Module
    workspace_service_test.py
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
    Unit tests for WorkspaceService managing user workspace directory and archive unpacking.
'''

from __future__ import annotations

from os.path import exists, join
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase, main

from idecobot.infrastructure.storage.iworkspace_service import IWorkspaceService
from idecobot.infrastructure.storage.workspace_constants import WorkspaceConstants
from idecobot.infrastructure.storage.workspace_service import WorkspaceService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceService(TestCase):
    '''
        Test cases verifying WorkspaceService operations and protocol compliance.

        It defines:

            :methods:
                | setUp - Initializes isolated temporary workspace environment.
                | tearDown - Cleans up temporary directory tree.
                | test_protocol_conformance - Verifies runtime Protocol checkability.
                | test_ensure_workspace_creates_and_extracts - Verifies automatic examples extraction.
                | test_list_scripts - Verifies listing of unpacked .cobot files.
                | test_extract_examples_missing_archive - Verifies graceful failure on missing archive.
                | test_version_string - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up isolated temporary workspace environment before each test.
        '''
        self.temp_dir: str = mkdtemp(prefix='idecobot_workspace_test_')
        self.constants: WorkspaceConstants = WorkspaceConstants(
            workspace_dir=self.temp_dir
        )
        self.service: WorkspaceService = WorkspaceService(constants=self.constants)

    def tearDown(self) -> None:
        '''
            Cleans up temporary directory tree after each test.
        '''
        if exists(self.temp_dir):
            rmtree(self.temp_dir, ignore_errors=True)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural subtyping protocol compliance via isinstance.
        '''
        self.assertIsInstance(self.service, IWorkspaceService)

    def test_ensure_workspace_creates_and_extracts(self) -> None:
        '''
            Verifies ensure_workspace extracts all 13 examples into empty workspace.
        '''
        workspace_path: str = self.service.ensure_workspace()
        self.assertEqual(workspace_path, self.temp_dir)
        self.assertTrue(exists(workspace_path))

        scripts: list[str] = self.service.list_scripts()
        self.assertGreaterEqual(len(scripts), 13)
        self.assertIn('01_cmd_power.cobot', scripts)
        self.assertIn('10_routine_pick_and_place.cobot', scripts)

        # Check content of an unpacked script
        with open(join(workspace_path, '01_cmd_power.cobot'), 'r', encoding='utf-8') as f:
            content: str = f.read()
        self.assertIn('POWER', content)

    def test_list_scripts(self) -> None:
        '''
            Verifies list_scripts returns empty list when directory has no scripts.
        '''
        self.assertEqual(self.service.list_scripts(), [])
        self.service.ensure_workspace()
        scripts: list[str] = self.service.list_scripts()
        self.assertIsInstance(scripts, list)
        self.assertTrue(all(s.endswith('.cobot') for s in scripts))

    def test_extract_examples_missing_archive(self) -> None:
        '''
            Verifies extract_examples returns False if archive path does not exist.
        '''
        bad_constants: WorkspaceConstants = WorkspaceConstants(
            workspace_dir=self.temp_dir,
            archive_path='/tmp/non_existent_archive_xyz.tgz'
        )
        bad_service: WorkspaceService = WorkspaceService(constants=bad_constants)
        self.assertFalse(bad_service.extract_examples())

    def test_version_string(self) -> None:
        '''
            Verifies get_version returns valid version string.
        '''
        self.assertEqual(self.service.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
