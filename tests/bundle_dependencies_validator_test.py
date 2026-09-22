# -*- coding: UTF-8 -*-

'''
Module
    bundle_dependencies_validator_test.py
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
    Unit tests for IDECobotBundleDependenciesValidator.
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
from idecobot.setup.dep_validator import IDECobotBundleDependenciesValidator
from idecobot.setup.dependencies import IDECobotBundleDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIDECobotBundleDependenciesValidator(TestCase):
    '''
    Test cases for IDECobotBundleDependenciesValidator dependency verification.

    It defines:

        :attributes:
            | _valid_deps - Valid IDECobotBundleDependencies fixture.
        :methods:
            | setUp - Initializes mock dependencies before each test execution.
            | test_validate_valid - Tests validation of conforming dependencies.
            | test_validate_none - Tests ATSValueError raised when dependencies is None.
            | test_validate_not_mapping - Tests ATSTypeError raised when not a Mapping.
            | test_validate_missing_attribute - Tests ATSValueError when dependency missing.
            | test_validate_invalid_type - Tests ATSTypeError when dependency has wrong type.
            | test_is_valid_true - Tests is_valid returns True for conforming dependencies.
            | test_is_valid_false - Tests is_valid returns False on invalid dependencies.
    '''

    _valid_deps: IDECobotBundleDependencies

    def setUp(self) -> None:
        '''
        Initializes mock dependencies before each test execution.
        '''
        self._valid_deps = IDECobotBundleDependencies(
            base=MagicMock(spec=BaseBundle),
            service=MagicMock(spec=IService),
            gui=MagicMock(spec=IGUI),
            streamer=MagicMock(spec=IMyCobotStreamer),
            cli=MagicMock(spec=ICLI)
        )

    def test_validate_valid(self) -> None:
        '''
        Tests validation of conforming dependencies.
        '''
        IDECobotBundleDependenciesValidator.validate(self._valid_deps)

    def test_validate_none(self) -> None:
        '''
        Tests ATSValueError raised when dependencies is None.
        '''
        with self.assertRaises(ATSValueError):
            IDECobotBundleDependenciesValidator.validate(None)  # type: ignore[arg-type]

    def test_validate_not_mapping(self) -> None:
        '''
        Tests ATSTypeError raised when not a Mapping.
        '''
        with self.assertRaises(ATSTypeError):
            IDECobotBundleDependenciesValidator.validate(['not', 'mapping'])  # type: ignore[arg-type]

    def test_validate_missing_attribute(self) -> None:
        '''
        Tests ATSValueError when dependency missing.
        '''
        incomplete: dict[str, object] = {
            'base': MagicMock(spec=BaseBundle),
            'service': MagicMock(spec=IService),
            'gui': MagicMock(spec=IGUI),
            'streamer': MagicMock(spec=IMyCobotStreamer)
            # missing 'cli'
        }
        with self.assertRaises(ATSValueError):
            IDECobotBundleDependenciesValidator.validate(incomplete)  # type: ignore[arg-type]

    def test_validate_invalid_type(self) -> None:
        '''
        Tests ATSTypeError when dependency has wrong type.
        '''
        bad_type_deps: dict[str, object] = {
            'base': MagicMock(spec=BaseBundle),
            'service': MagicMock(spec=IService),
            'gui': MagicMock(spec=IGUI),
            'streamer': MagicMock(spec=IMyCobotStreamer),
            'cli': 'not_an_icli'
        }
        with self.assertRaises(ATSTypeError):
            IDECobotBundleDependenciesValidator.validate(bad_type_deps)  # type: ignore[arg-type]

    def test_is_valid_true(self) -> None:
        '''
        Tests is_valid returns True for conforming dependencies.
        '''
        self.assertTrue(IDECobotBundleDependenciesValidator.is_valid(self._valid_deps))

    def test_is_valid_false(self) -> None:
        '''
        Tests is_valid returns False on invalid dependencies.
        '''
        self.assertFalse(IDECobotBundleDependenciesValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(IDECobotBundleDependenciesValidator.is_valid({}))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
