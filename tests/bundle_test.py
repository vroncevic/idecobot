# -*- coding: UTF-8 -*-

'''
Module
    test_bundle.py
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
    Unit tests for IDECobotBundleFactory composition and component wiring.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.setup.bundle import IDECobotBundle
from idecobot.setup.factory import IDECobotBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIDECobotBundleFactory(TestCase):
    '''
        Test cases for IDECobotBundleFactory root composition and dependency wiring.

        It defines:

            :methods:
                | test_bundle_creation - Tests complete assembly of bundle.
                | test_bundle_components_initialized - Tests all core services are operational.
                | test_bundle_dictionary_export - Tests bundle serialization to dictionary.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Tests factory produces a valid IDECobotBundle.
        '''
        bundle: IDECobotBundle = IDECobotBundleFactory.create_bundle()
        self.assertIsNotNone(bundle)
        self.assertIsNotNone(bundle.base)
        self.assertIsNotNone(bundle.service)
        self.assertIsNotNone(bundle.gui)
        self.assertIsNotNone(bundle.streamer)
        self.assertIsNotNone(bundle.cli)

    def test_bundle_components_initialized(self) -> None:
        '''
            Tests that service and CLI are properly initialized.
        '''
        bundle: IDECobotBundle = IDECobotBundleFactory.create_bundle()
        self.assertTrue(bundle.service.is_initialized())
        self.assertTrue(bundle.cli.is_initialized())

    def test_bundle_dictionary_export(self) -> None:
        '''
            Tests bundle to_dict conversion.
        '''
        bundle: IDECobotBundle = IDECobotBundleFactory.create_bundle()
        b_dict = bundle.to_dict()
        self.assertIn('base', b_dict)
        self.assertIn('service', b_dict)
        self.assertIn('gui', b_dict)
        self.assertIn('streamer', b_dict)
        self.assertIn('cli', b_dict)


if __name__ == '__main__':
    main()
