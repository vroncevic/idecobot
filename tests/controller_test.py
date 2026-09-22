# -*- coding: UTF-8 -*-

'''
Module
    controller_test.py
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
    Unit tests for MyCobot controller components, facade, and factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.service.communication.imycobot_controller import (
    IMyCobotController
)
from idecobot.infrastructure.communication.protocol.mycobot_protocol_codec import (
    MyCobotProtocolCodec
)
from idecobot.infrastructure.communication.protocol.protocol_codec_factory import (
    ProtocolCodecFactory
)
from idecobot.infrastructure.communication.streamer.connection_manager import (
    ConnectionManager
)
from idecobot.infrastructure.communication.streamer.controller_factory import (
    ControllerFactory
)
from idecobot.infrastructure.communication.streamer.iconnection_manager import (
    IConnectionManager
)
from idecobot.infrastructure.communication.streamer.icontroller_factory import (
    IControllerFactory
)
from idecobot.infrastructure.communication.streamer.irobot_actuator import (
    IRobotActuator
)
from idecobot.infrastructure.communication.streamer.irobot_telemetry import (
    IRobotTelemetry
)
from idecobot.infrastructure.communication.streamer.mycobot_controller import (
    MyCobotController
)
from idecobot.infrastructure.communication.streamer.robot_actuator import (
    RobotActuator
)
from idecobot.infrastructure.communication.streamer.robot_telemetry import (
    RobotTelemetry
)
from idecobot.infrastructure.communication.transport.mock_serial_transport import (
    MockSerialTransport
)
from idecobot.infrastructure.communication.transport.transport_constants import (
    TransportConstants
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMyCobotController(TestCase):
    '''
        Test cases for decomposed robot controller components and composite facade.

        It defines:

            :methods:
                | setUp - Initializes fixtures for transport, codec, and controller.
                | test_connection_manager - Tests connection lifecycle operations.
                | test_robot_actuator - Tests movement, gripper, power, and home commands.
                | test_robot_telemetry - Tests telemetry reading and ping queries.
                | test_controller_facade_delegation - Tests full facade delegation.
                | test_protocol_conformance - Verifies structural Protocol compliance.
                | test_version_methods - Verifies get_version across all components.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.
        '''
        self.transport_constants: TransportConstants = TransportConstants()
        self.protocol_constants: ProtocolConstants = ProtocolConstants()
        self.mock_transport: MockSerialTransport = MockSerialTransport(
            transport_constants=self.transport_constants,
            protocol_constants=self.protocol_constants
        )
        self.codec: MyCobotProtocolCodec = ProtocolCodecFactory.create(
            constants=self.protocol_constants
        )
        self.controller: MyCobotController = ControllerFactory.create(
            transport=self.mock_transport,
            codec=self.codec,
            constants=self.protocol_constants
        )

    def test_connection_manager(self) -> None:
        '''
            Tests connection lifecycle operations.
        '''
        conn = ConnectionManager(transport=self.mock_transport)
        self.assertFalse(conn.is_connected())
        self.assertEqual(conn.get_transport(), self.mock_transport)
        self.assertTrue(conn.connect('/dev/dummy', 115200))
        self.assertTrue(conn.is_connected())
        conn.disconnect()
        self.assertFalse(conn.is_connected())

    def test_robot_actuator(self) -> None:
        '''
            Tests movement, gripper, power, and home commands.
        '''
        actuator = RobotActuator(transport=self.mock_transport, codec=self.codec)
        self.assertFalse(actuator.send_angles([0.0] * 6, speed=50))

        self.mock_transport.open()
        self.assertTrue(actuator.send_angles([10.0, -20.0, 30.0, 0.0, 0.0, 0.0], speed=50))
        self.assertTrue(actuator.send_coords([100.0, 100.0, 100.0, 0.0, 0.0, 0.0], speed=40))
        self.assertTrue(actuator.set_gripper(state=1, speed=30))
        self.assertTrue(actuator.power(on=True))
        self.assertTrue(actuator.power(on=False))
        self.assertTrue(actuator.home(speed=80))

    def test_robot_telemetry(self) -> None:
        '''
            Tests telemetry reading and ping queries.
        '''
        telemetry = RobotTelemetry(
            transport=self.mock_transport,
            codec=self.codec,
            constants=self.protocol_constants
        )
        self.assertIsNone(telemetry.read_angles())
        self.assertFalse(telemetry.ping())

        self.mock_transport.open()
        angles = telemetry.read_angles()
        self.assertIsNotNone(angles)
        if angles is not None:
            self.assertEqual(len(angles), 6)
        self.assertTrue(telemetry.ping())

    def test_controller_facade_delegation(self) -> None:
        '''
            Tests full facade delegation.
        '''
        self.assertEqual(self.controller.get_transport(), self.mock_transport)
        self.assertTrue(self.controller.connect('/dev/ttyUSB0', 115200))
        self.assertTrue(self.controller.is_connected())
        self.assertTrue(self.controller.send_angles([0.0] * 6, speed=30))
        self.assertTrue(self.controller.send_coords([150.0, 0.0, 200.0, 0.0, 90.0, 0.0], speed=40))
        self.assertTrue(self.controller.set_gripper(state=0, speed=20))
        self.assertTrue(self.controller.power(on=True))
        self.assertTrue(self.controller.home(speed=50))

        angles = self.controller.read_angles()
        self.assertIsNotNone(angles)
        self.controller.disconnect()
        self.assertFalse(self.controller.is_connected())

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural Protocol compliance.
        '''
        conn = ConnectionManager(transport=self.mock_transport)
        actuator = RobotActuator(transport=self.mock_transport, codec=self.codec)
        telemetry = RobotTelemetry(
            transport=self.mock_transport,
            codec=self.codec,
            constants=self.protocol_constants
        )
        factory = ControllerFactory()

        self.assertIsInstance(conn, IConnectionManager)
        self.assertIsInstance(actuator, IRobotActuator)
        self.assertIsInstance(telemetry, IRobotTelemetry)
        self.assertIsInstance(factory, IControllerFactory)
        self.assertIsInstance(self.controller, IMyCobotController)

    def test_version_methods(self) -> None:
        '''
            Verifies get_version across all components.
        '''
        conn = ConnectionManager(transport=self.mock_transport)
        actuator = RobotActuator(transport=self.mock_transport, codec=self.codec)
        telemetry = RobotTelemetry(
            transport=self.mock_transport,
            codec=self.codec,
            constants=self.protocol_constants
        )

        self.assertEqual(conn.get_version(), '1.0.3')
        self.assertEqual(actuator.get_version(), '1.0.3')
        self.assertEqual(telemetry.get_version(), '1.0.3')
        self.assertEqual(self.controller.get_version(), '1.0.3')
        self.assertEqual(ControllerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
