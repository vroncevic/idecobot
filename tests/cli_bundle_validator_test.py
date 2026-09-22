# -*- coding: UTF-8 -*-

'''
Module
    cli_bundle_validator_test.py
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
    Unit tests for CLIBundleValidator.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.cli.setup.bundle import CLIBundle
from idecobot.infrastructure.cli.setup.validator import CLIBundleValidator
from idecobot.infrastructure.command.command import CommandBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundleValidator(TestCase):
    '''
    Test cases for CLIBundleValidator instance verification.

    It defines:

        :attributes:
            | _bundle - Conforming CLIBundle fixture.
        :methods:
            | setUp - Initializes fixtures before each test execution.
            | test_validate_valid - Tests validation of conforming CLIBundle.
            | test_validate_none - Tests ATSValueError raised when bundle is None.
            | test_validate_not_bundle - Tests ATSTypeError raised when not a CLIBundle.
            | test_validate_none_attribute - Tests ATSValueError when attribute is None.
            | test_validate_invalid_attribute_type - Tests ATSTypeError on mismatched attribute.
            | test_is_valid_true - Tests is_valid returns True on conforming bundle.
            | test_is_valid_false - Tests is_valid returns False on non-conforming bundle.
    '''

    _bundle: CLIBundle

    def setUp(self) -> None:
        '''
        Initializes fixtures before each test execution.
        '''
        self._bundle = CLIBundle(
            service=MagicMock(spec=IService),
            parser=MagicMock(spec=IOptionManager),
            commands=[MagicMock(spec=CommandBundle)]
        )

    def test_validate_valid(self) -> None:
        '''
        Tests validation of conforming CLIBundle.
        '''
        CLIBundleValidator.validate(self._bundle)

    def test_validate_none(self) -> None:
        '''
        Tests ATSValueError raised when bundle is None.
        '''
        with self.assertRaises(ATSValueError):
            CLIBundleValidator.validate(None)  # type: ignore[arg-type]

    def test_validate_not_bundle(self) -> None:
        '''
        Tests ATSTypeError raised when not a CLIBundle.
        '''
        with self.assertRaises(ATSTypeError):
            CLIBundleValidator.validate({'not': 'a bundle'})  # type: ignore[arg-type]

    def test_validate_none_attribute(self) -> None:
        '''
        Tests ATSValueError when attribute is None.
        '''
        bad_bundle = CLIBundle(
            service=MagicMock(spec=IService),
            parser=None,  # type: ignore[arg-type]
            commands=[]
        )
        with self.assertRaises(ATSValueError):
            CLIBundleValidator.validate(bad_bundle)

    def test_validate_invalid_attribute_type(self) -> None:
        '''
        Tests ATSTypeError on mismatched attribute.
        '''
        bad_bundle = CLIBundle(
            service=MagicMock(spec=IService),
            parser=123,  # type: ignore[arg-type]
            commands=[]
        )
        with self.assertRaises(ATSTypeError):
            CLIBundleValidator.validate(bad_bundle)

    def test_is_valid_true(self) -> None:
        '''
        Tests is_valid returns True on conforming bundle.
        '''
        self.assertTrue(CLIBundleValidator.is_valid(self._bundle))

    def test_is_valid_false(self) -> None:
        '''
        Tests is_valid returns False on non-conforming bundle.
        '''
        self.assertFalse(CLIBundleValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(CLIBundleValidator.is_valid('bad'))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
