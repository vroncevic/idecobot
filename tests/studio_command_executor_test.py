# -*- coding: UTF-8 -*-

'''
Module
    studio_command_executor_test.py
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
    Unit tests for StudioCommandExecutor strategy launching Motion Studio GUI.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.command.studio_command_definition import StudioCommandDefinition
from idecobot.infrastructure.command.studio_command_executor import StudioCommandExecutor
from idecobot.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStudioCommandExecutor(TestCase):
    '''
    Test cases for StudioCommandExecutor CLI execution lifecycle.

    It defines:

        :attributes:
            | _definition - Injected StudioCommandDefinition instance.
            | _gui_mock - Mock of IGUI presentation adapter.
            | _service_mock - Mock of core IService facade.
            | _executor - StudioCommandExecutor instance under test.
        :methods:
            | setUp - Initializes fixtures before each test execution.
            | test_execute_uninitialized_gui - Tests execution when GUI is not initialized.
            | test_execute_uninitialized_service - Tests execution when service is not initialized.
            | test_execute_success_minimal - Tests studio execution with default arguments.
            | test_execute_with_file - Tests loading script file upon execution.
            | test_execute_with_port - Tests connecting port upon execution.
            | test_execute_with_file_and_port - Tests passing both file and port arguments.
            | test_execute_with_ignored_empty_params - Tests empty/invalid param handling.
            | test_execute_runtime_error_handled - Tests handling RuntimeError during start.
            | test_execute_value_error_handled - Tests handling ValueError during load.
            | test_execute_os_error_handled - Tests handling OSError during port connect.
            | test_get_definition - Tests retrieval of injected command definition.
            | test_to_string - Tests string representation of executor.
    '''

    _definition: StudioCommandDefinition
    _gui_mock: MagicMock
    _service_mock: MagicMock
    _executor: StudioCommandExecutor

    def setUp(self) -> None:
        '''
        Initializes fixtures before each test execution.
        '''
        self._definition = StudioCommandDefinition()
        self._gui_mock = MagicMock(spec=IGUI)
        self._service_mock = MagicMock(spec=IService)
        self._gui_mock.is_initialized.return_value = True
        self._service_mock.is_initialized.return_value = True
        self._executor = StudioCommandExecutor(self._definition, self._gui_mock)

    def test_execute_uninitialized_gui(self) -> None:
        '''
        Tests execution when GUI is not initialized.
        '''
        self._gui_mock.is_initialized.return_value = False
        res = self._executor.execute(params={}, service=self._service_mock)
        self.assertEqual(res['returncode'], 1)
        self.assertIn('not initialized', str(res['stderr']))

    def test_execute_uninitialized_service(self) -> None:
        '''
        Tests execution when service is not initialized.
        '''
        self._service_mock.is_initialized.return_value = False
        res = self._executor.execute(params={}, service=self._service_mock)
        self.assertEqual(res['returncode'], 1)
        self.assertIn('not initialized', str(res['stderr']))

    def test_execute_success_minimal(self) -> None:
        '''
        Tests studio execution with default arguments.
        '''
        res = self._executor.execute(params={}, service=self._service_mock)
        self.assertEqual(res['returncode'], 0)
        self.assertIn('successfully', str(res['stdout']))
        self._gui_mock.start.assert_called_once()

    def test_execute_with_file(self) -> None:
        '''
        Tests loading script file upon execution.
        '''
        res = self._executor.execute(
            params={'file': '/path/to/demo.cobot'},
            service=self._service_mock
        )
        self.assertEqual(res['returncode'], 0)
        self._gui_mock.load_file.assert_called_once_with('/path/to/demo.cobot')
        self._gui_mock.start.assert_called_once()

    def test_execute_with_port(self) -> None:
        '''
        Tests connecting port upon execution.
        '''
        res = self._executor.execute(
            params={'port': '/dev/ttyACM0'},
            service=self._service_mock
        )
        self.assertEqual(res['returncode'], 0)
        self._gui_mock.connect_port.assert_called_once_with('/dev/ttyACM0')
        self._gui_mock.start.assert_called_once()

    def test_execute_with_file_and_port(self) -> None:
        '''
        Tests passing both file and port arguments.
        '''
        res = self._executor.execute(
            params={'file': '/path/to/demo.cobot', 'port': '/dev/ttyUSB0'},
            service=self._service_mock
        )
        self.assertEqual(res['returncode'], 0)
        self._gui_mock.load_file.assert_called_once_with('/path/to/demo.cobot')
        self._gui_mock.connect_port.assert_called_once_with('/dev/ttyUSB0')
        self._gui_mock.start.assert_called_once()

    def test_execute_with_ignored_empty_params(self) -> None:
        '''
        Tests empty/invalid param handling.
        '''
        res = self._executor.execute(
            params={'file': '', 'port': None},
            service=self._service_mock
        )
        self.assertEqual(res['returncode'], 0)
        self._gui_mock.load_file.assert_not_called()
        self._gui_mock.connect_port.assert_not_called()
        self._gui_mock.start.assert_called_once()

    def test_execute_runtime_error_handled(self) -> None:
        '''
        Tests handling RuntimeError during start.
        '''
        self._gui_mock.start.side_effect = RuntimeError('Window failed to launch')
        res = self._executor.execute(params={}, service=self._service_mock)
        self.assertEqual(res['returncode'], 1)
        self.assertIn('Window failed to launch', str(res['stderr']))

    def test_execute_value_error_handled(self) -> None:
        '''
        Tests handling ValueError during load.
        '''
        self._gui_mock.load_file.side_effect = ValueError('Corrupted script format')
        res = self._executor.execute(
            params={'file': 'bad.cobot'},
            service=self._service_mock
        )
        self.assertEqual(res['returncode'], 1)
        self.assertIn('Corrupted script format', str(res['stderr']))

    def test_execute_os_error_handled(self) -> None:
        '''
        Tests handling OSError during port connect.
        '''
        self._gui_mock.connect_port.side_effect = OSError('Port busy')
        res = self._executor.execute(
            params={'port': '/dev/ttyUSB0'},
            service=self._service_mock
        )
        self.assertEqual(res['returncode'], 1)
        self.assertIn('Port busy', str(res['stderr']))

    def test_get_definition(self) -> None:
        '''
        Tests retrieval of injected command definition.
        '''
        self.assertIs(self._executor.get_definition(), self._definition)

    def test_to_string(self) -> None:
        '''
        Tests string representation of executor.
        '''
        desc: str = str(self._executor)
        self.assertIsInstance(desc, str)
        self.assertTrue(len(desc) > 0)


if __name__ == '__main__':
    main()
