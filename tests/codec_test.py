# -*- coding: UTF-8 -*-

'''
Module
    test_codec.py
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
    Unit tests for MyCobotProtocolCodec packet encoding and decoding.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.infrastructure.communication.protocol.mycobot_protocol_codec import MyCobotProtocolCodec

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMyCobotProtocolCodec(TestCase):
    '''
        Test cases for MyCobot binary packet serialization and parsing.

        It defines:

            :methods:
                | test_encode_frame_structure - Tests framing with 0xFE 0xFE and footer 0xFA.
                | test_encode_decode_angles - Tests joint angle pack and unpack roundtrip.
                | test_encode_decode_coords - Tests Cartesian coordinates pack and unpack.
                | test_gripper_encoding - Tests tool gripper command frame encoding.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.constants = ProtocolConstants()
        self.codec = MyCobotProtocolCodec(constants=self.constants)

    def test_encode_frame_structure(self) -> None:
        '''
            Tests packet framing headers and footers.
        '''
        frame: MyCobotFrame = self.codec.pack_power()
        raw = frame.to_bytes()
        self.assertEqual(raw[0], 0xFE)
        self.assertEqual(raw[1], 0xFE)
        self.assertEqual(raw[2], 2)  # len = 1 (cmd) + 0 (payload) + 1 (footer)
        self.assertEqual(raw[3], 0x10)
        self.assertEqual(raw[4], 0xFA)

    def test_encode_decode_angles(self) -> None:
        '''
            Tests encoding and decoding of joint angles.
        '''
        original_angles = [10.5, -20.0, 45.25, 0.0, -90.0, 120.0]
        frame: MyCobotFrame = self.codec.pack_angles(original_angles, speed=50)
        raw = frame.to_bytes()
        self.assertEqual(raw[0], 0xFE)
        self.assertEqual(raw[1], 0xFE)
        self.assertEqual(raw[3], 0x22)

        payload = frame.payload
        decoded = self.codec.unpack_angles(payload)
        for orig, dec in zip(original_angles, decoded):
            self.assertAlmostEqual(orig, dec, delta=0.02)

    def test_encode_decode_coords(self) -> None:
        '''
            Tests encoding and decoding of Cartesian coordinates.
        '''
        original_coords = [150.0, -100.5, 200.25, 0.0, 90.0, -45.0]
        frame: MyCobotFrame = self.codec.pack_coords(original_coords, speed=40, mode=0)
        raw = frame.to_bytes()
        self.assertEqual(raw[0], 0xFE)
        self.assertEqual(raw[1], 0xFE)
        self.assertEqual(raw[3], 0x25)

        payload = frame.payload
        decoded = self.codec.unpack_coords(payload)
        for orig, dec in zip(original_coords, decoded):
            self.assertAlmostEqual(orig, dec, delta=0.02)

    def test_gripper_encoding(self) -> None:
        '''
            Tests tool gripper packet generation.
        '''
        grip_frame: MyCobotFrame = self.codec.pack_gripper(1, 30)
        raw = grip_frame.to_bytes()
        self.assertEqual(raw[3], 0x66)
        self.assertEqual(raw[4], 1)
        self.assertEqual(raw[5], 30)


if __name__ == '__main__':
    main()
