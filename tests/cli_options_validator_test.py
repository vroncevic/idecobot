# -*- coding: UTF-8 -*-

'''
Module
    cli_options_validator_test.py
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
    Unit tests for CLIBundleOptionsValidator.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator
from idecobot.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundleOptionsValidator(TestCase):
    '''
    Test cases for CLIBundleOptionsValidator options validation.

    It defines:

        :attributes:
            | _valid_options - Populated valid options dictionary fixture.
        :methods:
            | setUp - Initializes fixtures before each test execution.
            | test_validate_valid - Tests validation of conforming options.
            | test_validate_none - Tests ATSValueError raised when options is None.
            | test_validate_not_mapping - Tests ATSTypeError raised when not a Mapping.
            | test_validate_missing_option - Tests ATSValueError when required option missing.
            | test_validate_invalid_type - Tests ATSTypeError on mismatched option type.
            | test_is_valid_true - Tests is_valid returns True on conforming options.
            | test_is_valid_false - Tests is_valid returns False on non-conforming options.
    '''

    _valid_options: dict[str, object]

    def setUp(self) -> None:
        '''
        Initializes fixtures before each test execution.
        '''
        self._valid_options = {
            'service': MagicMock(spec=IService),
            'parser': MagicMock(spec=IOptionManager),
            'gui': MagicMock(spec=IGUI)
        }

    def test_validate_valid(self) -> None:
        '''
        Tests validation of conforming options.
        '''
        CLIBundleOptionsValidator.validate(self._valid_options)

    def test_validate_none(self) -> None:
        '''
        Tests ATSValueError raised when options is None.
        '''
        with self.assertRaises(ATSValueError):
            CLIBundleOptionsValidator.validate(None)  # type: ignore[arg-type]

    def test_validate_not_mapping(self) -> None:
        '''
        Tests ATSTypeError raised when not a Mapping.
        '''
        with self.assertRaises(ATSTypeError):
            CLIBundleOptionsValidator.validate(['bad', 'type'])  # type: ignore[arg-type]

    def test_validate_missing_option(self) -> None:
        '''
        Tests ATSValueError when required option missing.
        '''
        incomplete: dict[str, object] = {
            'service': MagicMock(spec=IService),
            'parser': MagicMock(spec=IOptionManager)
            # missing 'gui'
        }
        with self.assertRaises(ATSValueError):
            CLIBundleOptionsValidator.validate(incomplete)

    def test_validate_invalid_type(self) -> None:
        '''
        Tests ATSTypeError on mismatched option type.
        '''
        bad_type = {
            'service': MagicMock(spec=IService),
            'parser': MagicMock(spec=IOptionManager),
            'gui': 'not_an_igui'
        }
        with self.assertRaises(ATSTypeError):
            CLIBundleOptionsValidator.validate(bad_type)

    def test_is_valid_true(self) -> None:
        '''
        Tests is_valid returns True on conforming options.
        '''
        self.assertTrue(CLIBundleOptionsValidator.is_valid(self._valid_options))

    def test_is_valid_false(self) -> None:
        '''
        Tests is_valid returns False on non-conforming options.
        '''
        self.assertFalse(CLIBundleOptionsValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(CLIBundleOptionsValidator.is_valid({}))


if __name__ == '__main__':
    main()
