# -*- coding: UTF-8 -*-

'''
Module
    dsl_service_factory_test.py
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
    Unit tests for DslServiceFactory assembly and component creation.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.dsl.token.dsl_grammar_constants import DslGrammarConstants
from idecobot.core.service.dsl.dsl_service_factory import DslServiceFactory
from idecobot.core.service.dsl.mycobot_dsl_service import MyCobotDslService
from idecobot.core.service.kinematics.kinematic_validator import KinematicValidator
from idecobot.setup.bounds_loader import BoundsLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslServiceFactory(TestCase):
    '''
        Test cases for DslServiceFactory construction and subsystem wiring.

        It defines:

            :methods:
                | test_create_dsl_service - Tests factory builds valid MyCobotDslService.
                | test_get_version - Tests factory version string retrieval.
    '''

    def test_create_dsl_service(self) -> None:
        '''
            Tests factory produces a fully functioning MyCobotDslService.
        '''
        bounds = BoundsLoader.load()
        validator = KinematicValidator(bounds=bounds)
        protocol_constants = ProtocolConstants()
        grammar = DslGrammarConstants()
        service: MyCobotDslService = DslServiceFactory.create(
            bounds=bounds,
            validator=validator,
            protocol_constants=protocol_constants,
            grammar=grammar
        )
        self.assertIsNotNone(service)
        program, diagnostics = service.validate('MOVE J1:0 SPEED:30')
        self.assertIsNotNone(program)
        self.assertEqual(len(diagnostics), 0)

    def test_get_version(self) -> None:
        '''
            Tests retrieval of factory version string.
        '''
        version: str = DslServiceFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
