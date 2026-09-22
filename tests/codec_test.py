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
    Unit tests for MyCobot protocol codec components and factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.infrastructure.communication.protocol.imotion_codec import IMotionCodec
from idecobot.infrastructure.communication.protocol.imycobot_protocol_codec import (
    IMyCobotProtocolCodec
)
from idecobot.infrastructure.communication.protocol.iprotocol_codec_factory import (
    IProtocolCodecFactory
)
from idecobot.infrastructure.communication.protocol.iprotocol_framer import (
    IProtocolFramer
)
from idecobot.infrastructure.communication.protocol.isystem_codec import ISystemCodec
from idecobot.infrastructure.communication.protocol.itool_codec import IToolCodec
from idecobot.infrastructure.communication.protocol.motion_codec import MotionCodec
from idecobot.infrastructure.communication.protocol.mycobot_protocol_codec import (
    MyCobotProtocolCodec
)
from idecobot.infrastructure.communication.protocol.protocol_codec_factory import (
    ProtocolCodecFactory
)
from idecobot.infrastructure.communication.protocol.protocol_framer import (
    ProtocolFramer
)
from idecobot.infrastructure.communication.protocol.system_codec import SystemCodec
from idecobot.infrastructure.communication.protocol.tool_codec import ToolCodec

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMyCobotProtocolCodec(TestCase):
    '''
        Test cases for MyCobot binary packet serialization and component decomposition.

        It defines:

            :methods:
                | setUp - Initializes constants and composite codec fixture.
                | test_encode_frame_structure - Tests framing with 0xFE 0xFE and footer 0xFA.
                | test_encode_decode_angles - Tests joint angle pack and unpack roundtrip.
                | test_encode_decode_coords - Tests Cartesian coordinates pack and unpack.
                | test_gripper_encoding - Tests tool gripper command frame encoding.
                | test_system_commands - Tests relax, power, and get_angles system commands.
                | test_component_isolation - Verifies isolated execution of decomposed components.
                | test_protocol_conformance - Verifies runtime Protocol structural checks.
                | test_version_methods - Verifies get_version returns valid strings.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.constants: ProtocolConstants = ProtocolConstants()
        self.codec: MyCobotProtocolCodec = ProtocolCodecFactory.create(
            constants=self.constants
        )

    def test_encode_frame_structure(self) -> None:
        '''
            Tests packet framing headers and footers.
        '''
        frame: MyCobotFrame = self.codec.pack_power()
        raw: bytes = self.codec.encode_frame(frame)
        self.assertEqual(raw[0], 0xFE)
        self.assertEqual(raw[1], 0xFE)
        self.assertEqual(raw[2], 2)
        self.assertEqual(raw[3], 0x10)
        self.assertEqual(raw[4], 0xFA)
        hex_str: str = self.codec.format_hex(frame)
        self.assertEqual(hex_str, raw.hex(' ').upper())

    def test_encode_decode_angles(self) -> None:
        '''
            Tests encoding and decoding of joint angles.
        '''
        original_angles = [10.5, -20.0, 45.25, 0.0, -90.0, 120.0]
        frame: MyCobotFrame = self.codec.pack_angles(original_angles, speed=50)
        raw: bytes = self.codec.encode_frame(frame)
        self.assertEqual(raw[0], 0xFE)
        self.assertEqual(raw[1], 0xFE)
        self.assertEqual(raw[3], 0x22)

        payload: bytes = frame.payload
        decoded = self.codec.unpack_angles(payload)
        self.assertIsNotNone(decoded)
        if decoded is not None:
            for orig, dec in zip(original_angles, decoded):
                self.assertAlmostEqual(orig, dec, delta=0.02)

    def test_encode_decode_coords(self) -> None:
        '''
            Tests encoding and decoding of Cartesian coordinates.
        '''
        original_coords = [150.0, -100.5, 200.2, 0.0, 90.0, -45.0]
        frame: MyCobotFrame = self.codec.pack_coords(original_coords, speed=40, mode=0)
        raw: bytes = self.codec.encode_frame(frame)
        self.assertEqual(raw[0], 0xFE)
        self.assertEqual(raw[1], 0xFE)
        self.assertEqual(raw[3], 0x25)

        payload: bytes = frame.payload
        decoded = self.codec.unpack_coords(payload)
        self.assertIsNotNone(decoded)
        if decoded is not None:
            for orig, dec in zip(original_coords, decoded):
                self.assertAlmostEqual(orig, dec, delta=0.02)

    def test_gripper_encoding(self) -> None:
        '''
            Tests tool gripper packet generation.
        '''
        grip_frame: MyCobotFrame = self.codec.pack_gripper(1, 30)
        raw: bytes = self.codec.encode_frame(grip_frame)
        self.assertEqual(raw[3], 0x66)
        self.assertEqual(raw[4], 1)
        self.assertEqual(raw[5], 30)

    def test_system_commands(self) -> None:
        '''
            Tests relax, power, and get_angles system commands.
        '''
        relax_frame: MyCobotFrame = self.codec.pack_relax()
        self.assertEqual(relax_frame.cmd_id, self.constants.cmd_release_servos)
        self.assertEqual(relax_frame.payload, b'')

        power_frame: MyCobotFrame = self.codec.pack_power()
        self.assertEqual(power_frame.cmd_id, self.constants.cmd_power_on)
        self.assertEqual(power_frame.payload, b'')

        query_frame: MyCobotFrame = self.codec.pack_get_angles()
        self.assertEqual(query_frame.cmd_id, self.constants.cmd_get_angles)
        self.assertEqual(query_frame.payload, b'')

    def test_component_isolation(self) -> None:
        '''
            Verifies isolated execution of decomposed components.
        '''
        framer = ProtocolFramer(constants=self.constants)
        motion = MotionCodec(constants=self.constants)
        tool = ToolCodec(constants=self.constants)
        system = SystemCodec(constants=self.constants)

        frame = system.pack_power()
        encoded = framer.encode_frame(frame)
        self.assertTrue(encoded.startswith(b'\xfe\xfe'))

        grip = tool.pack_gripper(state=0, speed=20)
        self.assertEqual(grip.cmd_id, self.constants.cmd_set_gripper)

        angles_frame = motion.pack_angles([0.0] * 6, speed=10)
        unpacked = motion.unpack_angles(angles_frame.payload)
        self.assertIsNotNone(unpacked)

        short_unpack = motion.unpack_angles(b'\x00')
        self.assertIsNone(short_unpack)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies runtime Protocol structural checks without inheritance.
        '''
        framer = ProtocolFramer(constants=self.constants)
        motion = MotionCodec(constants=self.constants)
        tool = ToolCodec(constants=self.constants)
        system = SystemCodec(constants=self.constants)
        factory = ProtocolCodecFactory()

        self.assertIsInstance(framer, IProtocolFramer)
        self.assertIsInstance(motion, IMotionCodec)
        self.assertIsInstance(tool, IToolCodec)
        self.assertIsInstance(system, ISystemCodec)
        self.assertIsInstance(self.codec, IMyCobotProtocolCodec)
        self.assertIsInstance(factory, IProtocolCodecFactory)

    def test_version_methods(self) -> None:
        '''
            Verifies get_version returns valid version string across components.
        '''
        framer = ProtocolFramer(constants=self.constants)
        motion = MotionCodec(constants=self.constants)
        tool = ToolCodec(constants=self.constants)
        system = SystemCodec(constants=self.constants)

        self.assertEqual(framer.get_version(), '1.0.3')
        self.assertEqual(motion.get_version(), '1.0.3')
        self.assertEqual(tool.get_version(), '1.0.3')
        self.assertEqual(system.get_version(), '1.0.3')
        self.assertEqual(self.codec.get_version(), '1.0.3')
        self.assertEqual(ProtocolCodecFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
