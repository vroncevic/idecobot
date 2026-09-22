# -*- coding: UTF-8 -*-

'''
Module
    test_dsl_grammar_constants.py
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
    Unit tests for DslGrammarConstants dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from idecobot.core.model.dsl.token.dsl_grammar_constants import DslGrammarConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslGrammarConstants(TestCase):
    '''
        Test cases for DslGrammarConstants immutability and default definitions.

        It defines:

            :methods:
                | test_immutability - Verifies that constants cannot be modified.
                | test_commands - Verifies command set and keywords.
                | test_tool_actions - Verifies tool action definitions.
                | test_axes - Verifies joint and Cartesian axes.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.grammar = DslGrammarConstants()

    def test_immutability(self) -> None:
        '''
            Verifies that DslGrammarConstants instances cannot be mutated.
        '''
        with self.assertRaises(FrozenInstanceError):
            setattr(self.grammar, 'cmd_home', 'HOMING')

    def test_commands(self) -> None:
        '''
            Verifies command keyword constants and set membership.
        '''
        self.assertEqual(self.grammar.cmd_home, 'HOME')
        self.assertEqual(self.grammar.cmd_relax, 'RELAX')
        self.assertEqual(self.grammar.cmd_power, 'POWER')
        self.assertEqual(self.grammar.cmd_speed, 'SPEED')
        self.assertEqual(self.grammar.cmd_wait, 'WAIT')
        self.assertEqual(self.grammar.cmd_tool, 'TOOL')
        self.assertEqual(self.grammar.cmd_move, 'MOVE')
        self.assertIn('MOVE', self.grammar.commands)
        self.assertIn('HOME', self.grammar.commands)
        self.assertEqual(len(self.grammar.commands), 7)

    def test_tool_actions(self) -> None:
        '''
            Verifies tool action keywords and presets.
        '''
        self.assertEqual(self.grammar.action_grip, 'GRIP')
        self.assertEqual(self.grammar.action_release, 'RELEASE')
        self.assertIn('GRIP', self.grammar.tool_actions)
        self.assertIn('RELEASE', self.grammar.tool_actions)
        self.assertEqual(self.grammar.default_tool_speed, 50.0)

    def test_axes(self) -> None:
        '''
            Verifies joint and Cartesian axes sets.
        '''
        self.assertEqual(len(self.grammar.joint_axes), 6)
        self.assertIn('J1', self.grammar.joint_axes)
        self.assertIn('J6', self.grammar.joint_axes)
        self.assertEqual(len(self.grammar.cartesian_axes), 6)
        self.assertIn('X', self.grammar.cartesian_axes)
        self.assertIn('RZ', self.grammar.cartesian_axes)
        self.assertEqual(
            self.grammar.cartesian_coords,
            ('x', 'y', 'z', 'rx', 'ry', 'rz')
        )


if __name__ == '__main__':
    main()
