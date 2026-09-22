# -*- coding: UTF-8 -*-

'''
Module
    cli_engine_test.py
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
    Unit tests for CLI class implementing inbound CLI port.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.exceptions import ATSRuntimeError, ATSTypeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.cli.engine import CLI
from idecobot.infrastructure.cli.setup.bundle import CLIBundle
from idecobot.infrastructure.command.command import CommandBundle
from idecobot.infrastructure.command.icommand_definition import ICommandDefinition
from idecobot.infrastructure.command.icommand_executor import ICommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIEngine(TestCase):
    '''
    Test cases for CLI command dispatcher and option processing.

    It defines:

        :attributes:
            | _service_mock - Mock of core IService facade.
            | _parser_mock - Mock of IOptionManager CLI option manager.
            | _def_mock - Mock of ICommandDefinition.
            | _exec_mock - Mock of ICommandExecutor.
            | _bundle - CLIBundle fixture containing injected mocks.
            | _cli - CLI engine instance under test.
        :methods:
            | setUp - Initializes test fixtures before each test execution.
            | test_init_and_register - Tests bundle ingestion and command registration.
            | test_is_initialized - Tests initialization status query.
            | test_run_success - Tests command execution dispatch.
            | test_run_command_not_found - Tests handling unknown command.
            | test_run_runtime_error - Tests handling ATSRuntimeError during parse.
            | test_run_value_error - Tests handling ATSValueError during parse.
            | test_run_type_error - Tests handling ATSTypeError during parse.
            | test_to_string - Tests string representation.
    '''

    _service_mock: MagicMock
    _parser_mock: MagicMock
    _def_mock: MagicMock
    _exec_mock: MagicMock
    _bundle: CLIBundle
    _cli: CLI

    def setUp(self) -> None:
        '''
        Initializes test fixtures before each test execution.
        '''
        self._service_mock = MagicMock(spec=IService)
        self._parser_mock = MagicMock(spec=IOptionManager)
        self._def_mock = MagicMock(spec=ICommandDefinition)
        self._def_mock.name = 'studio'
        self._exec_mock = MagicMock(spec=ICommandExecutor)

        cmd_bundle = CommandBundle(definition=self._def_mock, executor=self._exec_mock)
        self._bundle = CLIBundle(
            service=self._service_mock,
            parser=self._parser_mock,
            commands=[cmd_bundle]
        )
        self._cli = CLI(self._bundle)

    def test_init_and_register(self) -> None:
        '''
        Tests bundle ingestion and command registration.
        '''
        self._parser_mock.register_commands.assert_called_once_with([self._def_mock])

    def test_is_initialized(self) -> None:
        '''
        Tests initialization status query.
        '''
        self.assertTrue(self._cli.is_initialized())

    def test_run_success(self) -> None:
        '''
        Tests command execution dispatch.
        '''
        self._parser_mock.parse_command.return_value = ('studio', {'file': 'sample.cobot'})
        self._exec_mock.execute.return_value = {'returncode': 0, 'stdout': 'ok', 'stderr': ''}

        result = self._cli.run()
        self.assertEqual(result['returncode'], 0)
        self._exec_mock.execute.assert_called_once_with(
            params={'file': 'sample.cobot'},
            service=self._service_mock
        )

    def test_run_command_not_found(self) -> None:
        '''
        Tests handling unknown command.
        '''
        self._parser_mock.parse_command.return_value = ('nonexistent', {})
        result = self._cli.run()
        self.assertEqual(result['returncode'], 1)
        self.assertIn('command not found', str(result['stderr']))

    def test_run_runtime_error(self) -> None:
        '''
        Tests handling ATSRuntimeError during parse.
        '''
        self._parser_mock.parse_command.side_effect = ATSRuntimeError('Parse failure')
        result = self._cli.run()
        self.assertEqual(result['returncode'], 1)
        self.assertIn('Parse failure', str(result['stderr']))

    def test_run_value_error(self) -> None:
        '''
        Tests handling ATSValueError during parse.
        '''
        self._parser_mock.parse_command.side_effect = ATSValueError('Missing value')
        result = self._cli.run()
        self.assertEqual(result['returncode'], 1)
        self.assertIn('Missing value', str(result['stderr']))

    def test_run_type_error(self) -> None:
        '''
        Tests handling ATSTypeError during parse.
        '''
        self._parser_mock.parse_command.side_effect = ATSTypeError('Type mismatch')
        result = self._cli.run()
        self.assertEqual(result['returncode'], 1)
        self.assertIn('Type mismatch', str(result['stderr']))

    def test_to_string(self) -> None:
        '''
        Tests string representation.
        '''
        desc: str = str(self._cli)
        self.assertIsInstance(desc, str)
        self.assertTrue(len(desc) > 0)


if __name__ == '__main__':
    main()
