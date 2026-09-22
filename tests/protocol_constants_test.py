# -*- coding: UTF-8 -*-

'''
Module
    test_protocol_constants.py
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
    Unit tests for ProtocolConstants and TransportConstants dataclasses and DI wiring.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.communication.stream_config import StreamConfig
from idecobot.core.model.communication.stream_progress import StreamProgress
from idecobot.core.model.communication.stream_state import StreamState
from idecobot.infrastructure.communication.protocol.mycobot_protocol_codec import (
    MyCobotProtocolCodec,
)
from idecobot.infrastructure.communication.protocol.protocol_codec_factory import (
    ProtocolCodecFactory,
)
from idecobot.infrastructure.communication.streamer.controller_factory import (
    ControllerFactory,
)
from idecobot.infrastructure.communication.streamer.mycobot_controller import (
    MyCobotController,
)
from idecobot.infrastructure.communication.transport.mock_serial_transport import (
    MockSerialTransport,
)
from idecobot.infrastructure.communication.transport.serial_transport import (
    SerialTransport,
)
from idecobot.infrastructure.communication.transport.transport_constants import (
    TransportConstants,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestProtocolConstants(TestCase):
    '''
        Validates protocol constants, transport constants, and pure DI injection.

        It defines:

            :methods:
                | test_protocol_constants_immutability - Verifies frozen dataclass immutability.
                | test_protocol_constants_defaults - Verifies default header, footer, and cmd IDs.
                | test_transport_constants_immutability - Verifies transport constants immutability.
                | test_transport_constants_values - Verifies standard serial parameters.
                | test_serial_transport_di - Verifies pure DI of TransportConstants into SerialTransport.
                | test_mock_serial_transport_di - Verifies DI into MockSerialTransport.
                | test_controller_mock_interaction - Verifies Controller query flow with MockTransport.
                | test_stream_config - Verifies StreamConfig attributes and immutability.
    '''

    def test_protocol_constants_immutability(self) -> None:
        '''
            Verifies that ProtocolConstants instances cannot be mutated.
        '''
        constants = ProtocolConstants()
        with self.assertRaises(FrozenInstanceError):
            setattr(constants, 'cmd_power_on', 0x99)

    def test_protocol_constants_defaults(self) -> None:
        '''
            Verifies default values in ProtocolConstants.
        '''
        constants = ProtocolConstants()
        self.assertEqual(constants.header_byte_1, 0xFE)
        self.assertEqual(constants.header_byte_2, 0xFE)
        self.assertEqual(constants.footer_byte, 0xFA)
        self.assertEqual(constants.cmd_power_on, 0x10)
        self.assertEqual(constants.cmd_release_servos, 0x13)
        self.assertEqual(constants.cmd_get_angles, 0x20)
        self.assertEqual(constants.cmd_send_angles, 0x22)
        self.assertEqual(constants.cmd_send_coords, 0x25)
        self.assertEqual(constants.cmd_set_gripper, 0x66)
        self.assertEqual(constants.cmd_nop, 0x00)
        self.assertAlmostEqual(constants.angle_scale_factor, 100.0)
        self.assertEqual(constants.format_angles_command, '>6hB')
        self.assertEqual(constants.format_coords_command, '>6hBB')
        self.assertEqual(constants.format_gripper_command, '>BB')
        self.assertEqual(constants.format_joints_payload, '>6h')

    def test_transport_constants_immutability(self) -> None:
        '''
            Verifies that TransportConstants instances cannot be mutated.
        '''
        constants = TransportConstants()
        with self.assertRaises(FrozenInstanceError):
            setattr(constants, 'default_baudrate', 9600)

    def test_transport_constants_values(self) -> None:
        '''
            Verifies standard serial transport default values.
        '''
        constants = TransportConstants()
        self.assertEqual(constants.default_port, '/dev/ttyUSB0')
        self.assertEqual(constants.default_baudrate, 115200)
        self.assertIn(115200, constants.standard_baudrates)
        self.assertEqual(constants.empty_payload, b'')
        self.assertEqual(constants.zero_bytes_written, 0)

    def test_serial_transport_di(self) -> None:
        '''
            Verifies pure DI injection of TransportConstants into SerialTransport.
        '''
        constants = TransportConstants(default_port='/dev/custom_port', default_baudrate=57600)
        transport = SerialTransport(constants=constants)
        self.assertEqual(getattr(transport, '_port'), '/dev/custom_port')
        self.assertEqual(getattr(transport, '_baudrate'), 57600)

    def test_mock_serial_transport_di(self) -> None:
        '''
            Verifies pure DI injection into MockSerialTransport.
        '''
        transport_constants = TransportConstants()
        protocol_constants = ProtocolConstants()
        mock = MockSerialTransport(
            transport_constants=transport_constants,
            protocol_constants=protocol_constants
        )
        self.assertFalse(mock.is_open())
        self.assertTrue(mock.open())
        self.assertTrue(mock.is_open())
        mock.close()
        self.assertFalse(mock.is_open())

    def test_controller_mock_interaction(self) -> None:
        '''
            Verifies controller query flow with mock transport and protocol codec.
        '''
        transport_constants = TransportConstants()
        protocol_constants = ProtocolConstants()
        mock = MockSerialTransport(
            transport_constants=transport_constants,
            protocol_constants=protocol_constants
        )
        codec = ProtocolCodecFactory.create(constants=protocol_constants)
        controller = ControllerFactory.create(
            transport=mock,
            codec=codec,
            constants=protocol_constants
        )
        self.assertTrue(controller.connect('/dev/dummy', 115200))
        angles = controller.read_angles()
        self.assertIsNotNone(angles)
        if angles is not None:
            self.assertEqual(len(angles), 6)
            for a in angles:
                self.assertAlmostEqual(a, 0.0)
        controller.disconnect()
        self.assertFalse(controller.is_connected())

    def test_stream_config(self) -> None:
        '''
            Verifies StreamConfig attributes and immutability.
        '''
        config = StreamConfig(playback_rate=1.5)
        self.assertEqual(config.playback_rate, 1.5)
        with self.assertRaises(FrozenInstanceError):
            setattr(config, 'playback_rate', 2.0)

    def test_stream_progress(self) -> None:
        '''
            Verifies StreamProgress pure data structure attributes and immutability.
        '''
        progress = StreamProgress(
            state=StreamState.STREAMING,
            current_step=3,
            total_steps=10,
            command_name='move_joints',
            progress_percent=30.0
        )
        self.assertEqual(progress.state, StreamState.STREAMING)
        self.assertEqual(progress.current_step, 3)
        self.assertEqual(progress.total_steps, 10)
        self.assertEqual(progress.command_name, 'move_joints')
        self.assertEqual(progress.progress_percent, 30.0)
        with self.assertRaises(FrozenInstanceError):
            setattr(progress, 'current_step', 4)


if __name__ == '__main__':
    main()
