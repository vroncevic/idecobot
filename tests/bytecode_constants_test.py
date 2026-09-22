# -*- coding: UTF-8 -*-

'''
Module
    bytecode_constants_test.py
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
    Unit tests for BytecodeConstants dataclass and table column alignment tokens.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from idecobot.infrastructure.gui.log.bytecode_constants import BytecodeConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBytecodeConstants(TestCase):
    '''
        Test cases verifying BytecodeConstants defaults, column alignment, and immutability.

        It defines:

            :methods:
                | setUp - Initializes BytecodeConstants instance.
                | test_default_values - Verifies standard widget attributes and defaults.
                | test_column_alignment - Verifies that header DELAY matches data row offset.
                | test_immutability - Verifies FrozenInstanceError on modification attempt.
    '''

    def setUp(self) -> None:
        '''
            Sets up BytecodeConstants instance before each test.
        '''
        self.constants: BytecodeConstants = BytecodeConstants()

    def test_default_values(self) -> None:
        '''
            Verifies standard widget attributes and defaults.
        '''
        self.assertEqual(self.constants.state_normal, 'normal')
        self.assertEqual(self.constants.state_disabled, 'disabled')
        self.assertEqual(self.constants.wrap_none, 'none')
        self.assertEqual(self.constants.border_width, 0)
        self.assertEqual(self.constants.col_step_width, 6)
        self.assertEqual(self.constants.col_cmd_width, 6)
        self.assertEqual(self.constants.col_hex_width, 54)
        self.assertEqual(self.constants.divider_length, 74)

    def test_column_alignment(self) -> None:
        '''
            Verifies that header DELAY column index matches data row DELAY start index.
        '''
        header: str = self.constants.header_template
        header_delay_idx: int = header.index('DELAY')

        # Simulate standard 17-byte MyCobot frame (50 hex chars)
        step_num: int = 1
        cmd_hex: str = '0x22'
        hex_frame_17b: str = 'FE FE 0F 22 00 00 00 00 00 00 00 00 00 00 00 00 1E FA'
        delay_str: str = '2.00s'
        row_17b: str = (
            f'{step_num:<{self.constants.col_step_width}} '
            f'{cmd_hex:<{self.constants.col_cmd_width}} '
            f'{hex_frame_17b:<{self.constants.col_hex_width}} '
            f'{delay_str}\n'
        )
        row_17b_delay_idx: int = row_17b.index(delay_str)

        # Simulate short 5-byte MyCobot frame (14 hex chars)
        hex_frame_5b: str = 'FE FE 02 10 FA'
        row_5b: str = (
            f'{step_num:<{self.constants.col_step_width}} '
            f'{cmd_hex:<{self.constants.col_cmd_width}} '
            f'{hex_frame_5b:<{self.constants.col_hex_width}} '
            f'{delay_str}\n'
        )
        row_5b_delay_idx: int = row_5b.index(delay_str)

        self.assertEqual(header_delay_idx, 69)
        self.assertEqual(row_17b_delay_idx, 69)
        self.assertEqual(row_5b_delay_idx, 69)
        self.assertEqual(header_delay_idx, row_17b_delay_idx)
        self.assertEqual(header_delay_idx, row_5b_delay_idx)

    def test_immutability(self) -> None:
        '''
            Verifies FrozenInstanceError when attempting to modify attributes.
        '''
        with self.assertRaises(FrozenInstanceError):
            self.constants.col_hex_width = 80


if __name__ == '__main__':
    main()
