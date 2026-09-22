# -*- coding: UTF-8 -*-

'''
Module
    bundle_options_validator_test.py
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
    Unit tests for IDECobotBundleOptionsValidator.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions import ATSTypeError, ATSValueError

from idecobot.setup.opt_validator import IDECobotBundleOptionsValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIDECobotBundleOptionsValidator(TestCase):
    '''
    Test cases for IDECobotBundleOptionsValidator option structure verification.

    It defines:

        :methods:
            | test_validate_valid_empty - Tests validation of empty options mapping.
            | test_validate_valid_populated - Tests validation of correctly typed options.
            | test_validate_none - Tests ATSValueError raised when options is None.
            | test_validate_not_mapping - Tests ATSTypeError raised when options is not Mapping.
            | test_validate_invalid_option_type - Tests ATSTypeError on mismatched option type.
            | test_is_valid_true - Tests is_valid returns True for conforming options.
            | test_is_valid_false - Tests is_valid returns False on non-conforming options.
    '''

    def test_validate_valid_empty(self) -> None:
        '''
        Tests validation of empty options mapping.
        '''
        IDECobotBundleOptionsValidator.validate({})

    def test_validate_valid_populated(self) -> None:
        '''
        Tests validation of correctly typed options.
        '''
        options = {
            'port': '/dev/ttyACM0',
            'baudrate': 115200,
            'info_file': '/path/to/info.yaml',
            'file_path': '/path/to/script.cobot',
            'robot_config': '/path/to/robot.json'
        }
        IDECobotBundleOptionsValidator.validate(options)

    def test_validate_none(self) -> None:
        '''
        Tests ATSValueError raised when options is None.
        '''
        with self.assertRaises(ATSValueError):
            IDECobotBundleOptionsValidator.validate(None)  # type: ignore[arg-type]

    def test_validate_not_mapping(self) -> None:
        '''
        Tests ATSTypeError raised when options is not Mapping.
        '''
        with self.assertRaises(ATSTypeError):
            IDECobotBundleOptionsValidator.validate(['not', 'a', 'dict'])  # type: ignore[arg-type]

    def test_validate_invalid_option_type(self) -> None:
        '''
        Tests ATSTypeError on mismatched option type.
        '''
        with self.assertRaises(ATSTypeError):
            IDECobotBundleOptionsValidator.validate({'baudrate': 'not_an_int'})  # type: ignore[dict-item]

    def test_is_valid_true(self) -> None:
        '''
        Tests is_valid returns True for conforming options.
        '''
        self.assertTrue(IDECobotBundleOptionsValidator.is_valid({'port': '/dev/ttyUSB0'}))

    def test_is_valid_false(self) -> None:
        '''
        Tests is_valid returns False on non-conforming options.
        '''
        self.assertFalse(IDECobotBundleOptionsValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(IDECobotBundleOptionsValidator.is_valid({'baudrate': 'invalid'}))  # type: ignore[dict-item]


if __name__ == '__main__':
    main()
