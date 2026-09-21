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
    Unit tests for ProtocolConstants and SerialDefaults dataclasses and DI wiring.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.communication.serial_defaults import SerialDefaults
from idecobot.infrastructure.communication.protocol.mycobot_protocol_codec import (
    MyCobotProtocolCodec,
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

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestProtocolConstants(TestCase):
    '''
        Validates protocol constants, serial defaults, and pure DI injection.

        It defines:

            :methods:
                | test_protocol_constants_immutability - Verifies frozen dataclass immutability.
                | test_protocol_constants_defaults - Verifies default header, footer, and cmd IDs.
                | test_serial_defaults_immutability - Verifies serial defaults immutability.
                | test_serial_defaults_values - Verifies standard serial parameters.
                | test_serial_transport_di - Verifies pure DI of SerialDefaults into SerialTransport.
                | test_mock_serial_transport_di - Verifies DI into MockSerialTransport.
                | test_controller_mock_interaction - Verifies Controller query flow with MockTransport.
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

    def test_serial_defaults_immutability(self) -> None:
        '''
            Verifies that SerialDefaults instances cannot be mutated.
        '''
        defaults = SerialDefaults()
        with self.assertRaises(FrozenInstanceError):
            setattr(defaults, 'default_baudrate', 9600)

    def test_serial_defaults_values(self) -> None:
        '''
            Verifies standard serial default values.
        '''
        defaults = SerialDefaults()
        self.assertEqual(defaults.default_port, '/dev/ttyUSB0')
        self.assertEqual(defaults.default_baudrate, 115200)
        self.assertIn(115200, defaults.standard_baudrates)
        self.assertEqual(defaults.empty_payload, b'')
        self.assertEqual(defaults.zero_bytes_written, 0)

    def test_serial_transport_di(self) -> None:
        '''
            Verifies pure DI injection of SerialDefaults into SerialTransport.
        '''
        defaults = SerialDefaults(default_port='/dev/custom_port', default_baudrate=57600)
        transport = SerialTransport(defaults=defaults)
        self.assertEqual(transport._port, '/dev/custom_port')
        self.assertEqual(transport._baudrate, 57600)

    def test_mock_serial_transport_di(self) -> None:
        '''
            Verifies pure DI injection into MockSerialTransport.
        '''
        defaults = SerialDefaults()
        constants = ProtocolConstants()
        mock = MockSerialTransport(defaults=defaults, constants=constants)
        self.assertFalse(mock.is_open())
        self.assertTrue(mock.open())
        self.assertTrue(mock.is_open())
        mock.close()
        self.assertFalse(mock.is_open())

    def test_controller_mock_interaction(self) -> None:
        '''
            Verifies controller query flow with mock transport and protocol codec.
        '''
        defaults = SerialDefaults()
        constants = ProtocolConstants()
        mock = MockSerialTransport(defaults=defaults, constants=constants)
        codec = MyCobotProtocolCodec(constants=constants)
        controller = MyCobotController(
            transport=mock,
            codec=codec,
            constants=constants
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


if __name__ == '__main__':
    main()
