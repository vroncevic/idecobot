# -*- coding: UTF-8 -*-

'''
Module
    bundle_validator_test.py
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
    Unit tests for IDECobotBundleValidator.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.exceptions import ATSTypeError, ATSValueError

from idecobot.core.service.communication.imycobot_streamer import IMyCobotStreamer
from idecobot.core.service.iservice import IService
from idecobot.infrastructure.cli.icli import ICLI
from idecobot.infrastructure.gui.igui import IGUI
from idecobot.setup.bundle import IDECobotBundle
from idecobot.setup.validator import IDECobotBundleValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIDECobotBundleValidator(TestCase):
    '''
    Test cases for IDECobotBundleValidator instance verification.

    It defines:

        :attributes:
            | _bundle - Valid IDECobotBundle fixture.
        :methods:
            | setUp - Initializes mock bundle before each test execution.
            | test_validate_valid - Tests validation of conforming bundle.
            | test_validate_none - Tests ATSValueError raised when bundle is None.
            | test_validate_not_bundle - Tests ATSTypeError raised when not an IDECobotBundle.
            | test_validate_none_attribute - Tests ATSValueError when attribute is None.
            | test_validate_invalid_attribute_type - Tests ATSTypeError on mismatched attribute.
            | test_is_valid_true - Tests is_valid returns True on conforming bundle.
            | test_is_valid_false - Tests is_valid returns False on non-conforming bundle.
    '''

    _bundle: IDECobotBundle

    def setUp(self) -> None:
        '''
        Initializes mock bundle before each test execution.
        '''
        self._bundle = IDECobotBundle(
            base=MagicMock(spec=BaseBundle),
            service=MagicMock(spec=IService),
            gui=MagicMock(spec=IGUI),
            streamer=MagicMock(spec=IMyCobotStreamer),
            cli=MagicMock(spec=ICLI)
        )

    def test_validate_valid(self) -> None:
        '''
        Tests validation of conforming bundle.
        '''
        IDECobotBundleValidator.validate(self._bundle)

    def test_validate_none(self) -> None:
        '''
        Tests ATSValueError raised when bundle is None.
        '''
        with self.assertRaises(ATSValueError):
            IDECobotBundleValidator.validate(None)  # type: ignore[arg-type]

    def test_validate_not_bundle(self) -> None:
        '''
        Tests ATSTypeError raised when not an IDECobotBundle.
        '''
        with self.assertRaises(ATSTypeError):
            IDECobotBundleValidator.validate('not_a_bundle')  # type: ignore[arg-type]

    def test_validate_none_attribute(self) -> None:
        '''
        Tests ATSValueError when attribute is None.
        '''
        bad_bundle = IDECobotBundle(
            base=MagicMock(spec=BaseBundle),
            service=MagicMock(spec=IService),
            gui=MagicMock(spec=IGUI),
            streamer=MagicMock(spec=IMyCobotStreamer),
            cli=None  # type: ignore[arg-type]
        )
        with self.assertRaises(ATSValueError):
            IDECobotBundleValidator.validate(bad_bundle)

    def test_validate_invalid_attribute_type(self) -> None:
        '''
        Tests ATSTypeError on mismatched attribute.
        '''
        bad_bundle = IDECobotBundle(
            base=MagicMock(spec=BaseBundle),
            service=MagicMock(spec=IService),
            gui=MagicMock(spec=IGUI),
            streamer=MagicMock(spec=IMyCobotStreamer),
            cli=123  # type: ignore[arg-type]
        )
        with self.assertRaises(ATSTypeError):
            IDECobotBundleValidator.validate(bad_bundle)

    def test_is_valid_true(self) -> None:
        '''
        Tests is_valid returns True on conforming bundle.
        '''
        self.assertTrue(IDECobotBundleValidator.is_valid(self._bundle))

    def test_is_valid_false(self) -> None:
        '''
        Tests is_valid returns False on non-conforming bundle.
        '''
        self.assertFalse(IDECobotBundleValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(IDECobotBundleValidator.is_valid('bad'))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
