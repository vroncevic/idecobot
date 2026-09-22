# -*- coding: UTF-8 -*-

'''
Module
    studio_command_definition_test.py
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
    Unit tests for StudioCommandDefinition CLI subcommand metadata.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.infrastructure.command.studio_command_definition import StudioCommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStudioCommandDefinition(TestCase):
    '''
    Test cases for StudioCommandDefinition CLI metadata.

    It defines:

        :attributes:
            | _definition - StudioCommandDefinition instance under test.
        :methods:
            | setUp - Initializes test fixture before each test execution.
            | test_name - Tests retrieval of command name.
            | test_help_text - Tests retrieval of command help text.
            | test_options - Tests configured CLI options and flags.
            | test_to_string - Tests string representation.
    '''

    _definition: StudioCommandDefinition

    def setUp(self) -> None:
        '''
        Initializes test fixture before each test execution.
        '''
        self._definition = StudioCommandDefinition()

    def test_name(self) -> None:
        '''
        Tests retrieval of command name.
        '''
        self.assertEqual(self._definition.name, 'studio')

    def test_help_text(self) -> None:
        '''
        Tests retrieval of command help text.
        '''
        self.assertIn('Motion Studio', self._definition.help_text)

    def test_options(self) -> None:
        '''
        Tests configured CLI options and flags.
        '''
        options = self._definition.options
        self.assertEqual(len(options), 3)

        option_names = [opt.name for opt in options]
        self.assertIn('--file', option_names)
        self.assertIn('--port', option_names)
        self.assertIn('--verbose', option_names)

    def test_to_string(self) -> None:
        '''
        Tests string representation.
        '''
        desc: str = str(self._definition)
        self.assertIsInstance(desc, str)
        self.assertTrue(len(desc) > 0)


if __name__ == '__main__':
    main()
