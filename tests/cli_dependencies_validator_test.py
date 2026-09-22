# -*- coding: UTF-8 -*-

'''
Module
    cli_dependencies_validator_test.py
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
    Unit tests for CLIBundleDependenciesValidator.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator
from idecobot.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from idecobot.infrastructure.command.command import CommandBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundleDependenciesValidator(TestCase):
    '''
    Test cases for CLIBundleDependenciesValidator dependency verification.

    It defines:

        :attributes:
            | _valid_deps - Conforming CLIBundleDependencies fixture.
        :methods:
            | setUp - Initializes fixtures before each test execution.
            | test_validate_valid - Tests validation of conforming dependencies.
            | test_validate_none - Tests ATSValueError raised when dependencies is None.
            | test_validate_not_mapping - Tests ATSTypeError raised when not a Mapping.
            | test_validate_missing_dependency - Tests ATSValueError when dependency missing.
            | test_validate_invalid_type - Tests ATSTypeError on mismatched dependency type.
            | test_is_valid_true - Tests is_valid returns True on conforming dependencies.
            | test_is_valid_false - Tests is_valid returns False on non-conforming dependencies.
    '''

    _valid_deps: CLIBundleDependencies

    def setUp(self) -> None:
        '''
        Initializes fixtures before each test execution.
        '''
        self._valid_deps = CLIBundleDependencies(
            service=MagicMock(spec=IService),
            parser=MagicMock(spec=IOptionManager),
            commands=[MagicMock(spec=CommandBundle)]
        )

    def test_validate_valid(self) -> None:
        '''
        Tests validation of conforming dependencies.
        '''
        CLIBundleDependenciesValidator.validate(self._valid_deps)

    def test_validate_none(self) -> None:
        '''
        Tests ATSValueError raised when dependencies is None.
        '''
        with self.assertRaises(ATSValueError):
            CLIBundleDependenciesValidator.validate(None)  # type: ignore[arg-type]

    def test_validate_not_mapping(self) -> None:
        '''
        Tests ATSTypeError raised when not a Mapping.
        '''
        with self.assertRaises(ATSTypeError):
            CLIBundleDependenciesValidator.validate(('tuple', 'not', 'mapping'))  # type: ignore[arg-type]

    def test_validate_missing_dependency(self) -> None:
        '''
        Tests ATSValueError when dependency missing.
        '''
        incomplete: dict[str, object] = {
            'service': MagicMock(spec=IService),
            'parser': MagicMock(spec=IOptionManager)
            # missing 'commands'
        }
        with self.assertRaises(ATSValueError):
            CLIBundleDependenciesValidator.validate(incomplete)  # type: ignore[arg-type]

    def test_validate_invalid_type(self) -> None:
        '''
        Tests ATSTypeError on mismatched dependency type.
        '''
        bad_type = {
            'service': MagicMock(spec=IService),
            'parser': MagicMock(spec=IOptionManager),
            'commands': 123  # not a Sequence
        }
        with self.assertRaises(ATSTypeError):
            CLIBundleDependenciesValidator.validate(bad_type)  # type: ignore[arg-type]

    def test_is_valid_true(self) -> None:
        '''
        Tests is_valid returns True on conforming dependencies.
        '''
        self.assertTrue(CLIBundleDependenciesValidator.is_valid(self._valid_deps))

    def test_is_valid_false(self) -> None:
        '''
        Tests is_valid returns False on non-conforming dependencies.
        '''
        self.assertFalse(CLIBundleDependenciesValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(CLIBundleDependenciesValidator.is_valid({}))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
