# -*- coding: UTF-8 -*-

'''
Module
    diagnostics_test.py
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
    Unit tests for diagnostics subsystem readers, coordinator, and factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
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
from idecobot.infrastructure.communication.transport.transport_constants import (
    TransportConstants,
)
from idecobot.infrastructure.diagnostics.diagnostics_constants import DiagnosticsConstants
from idecobot.infrastructure.diagnostics.diagnostics_coordinator import DiagnosticsCoordinator
from idecobot.infrastructure.diagnostics.diagnostics_factory import DiagnosticsFactory
from idecobot.infrastructure.diagnostics.idiagnostics_coordinator import (
    IDiagnosticsCoordinator,
)
from idecobot.infrastructure.diagnostics.ijoint_diagnostics_reader import (
    IJointDiagnosticsReader,
)
from idecobot.infrastructure.diagnostics.iservo_diagnostics_reader import (
    IServoDiagnosticsReader,
)
from idecobot.infrastructure.diagnostics.ispatial_diagnostics_reader import (
    ISpatialDiagnosticsReader,
)
from idecobot.infrastructure.diagnostics.joint_diagnostics_reader import (
    JointDiagnosticsReader,
)
from idecobot.infrastructure.diagnostics.servo_diagnostics_reader import (
    ServoDiagnosticsReader,
)
from idecobot.infrastructure.diagnostics.spatial_diagnostics_reader import (
    SpatialDiagnosticsReader,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDiagnostics(TestCase):
    '''
    Test cases for specialized diagnostic readers, coordinator, and factory.

    It defines:

        :methods:
            | setUp - Initializes fixtures for transport, codec, controller, and readers.
            | test_readers_when_closed - Tests readers behavior when transport closed.
            | test_readers_when_open - Tests readers output when transport open with mock data.
            | test_coordinator_telemetry - Tests coordinator aggregation and startup summary.
            | test_protocol_compliance - Verifies structural Protocol conformance.
            | test_version_methods - Tests version string retrieval across components.
    '''

    def setUp(self) -> None:
        '''
        Initializes fixtures for transport, codec, controller, and readers.
        '''
        self.proto: ProtocolConstants = ProtocolConstants()
        self.diag_const: DiagnosticsConstants = DiagnosticsConstants()
        self.transport: MockSerialTransport = MockSerialTransport(
            transport_constants=TransportConstants(),
            protocol_constants=self.proto
        )
        self.codec: MyCobotProtocolCodec = ProtocolCodecFactory.create(constants=self.proto)
        self.controller: MyCobotController = ControllerFactory.create(
            transport=self.transport,
            codec=self.codec,
            constants=self.proto
        )
        self.joint_reader: JointDiagnosticsReader = JointDiagnosticsReader(
            transport=self.transport,
            codec=self.codec,
            constants=self.diag_const,
            proto=self.proto
        )
        self.servo_reader: ServoDiagnosticsReader = ServoDiagnosticsReader(
            transport=self.transport,
            codec=self.codec,
            constants=self.diag_const,
            proto=self.proto
        )
        self.spatial_reader: SpatialDiagnosticsReader = SpatialDiagnosticsReader(
            transport=self.transport,
            codec=self.codec,
            constants=self.diag_const,
            proto=self.proto
        )
        self.coordinator: DiagnosticsCoordinator = DiagnosticsCoordinator(
            joint_reader=self.joint_reader,
            servo_reader=self.servo_reader,
            spatial_reader=self.spatial_reader,
            controller=self.controller
        )

    def test_readers_when_closed(self) -> None:
        '''
        Tests readers behavior when transport is closed.
        '''
        self.assertIn('not connected', self.joint_reader.read_angles())
        self.assertIn('not connected', self.joint_reader.read_temperatures())
        self.assertIn('not connected', self.servo_reader.read_voltages())
        self.assertIn('not connected', self.servo_reader.power_on())
        self.assertIn('not connected', self.spatial_reader.read_coords())
        self.assertIn('not connected', self.spatial_reader.probe_link())

    def test_readers_when_open(self) -> None:
        '''
        Tests readers output when transport is open with simulated robot data.
        '''
        self.transport.open()
        self.assertIn('Joint Angles', self.joint_reader.read_angles())
        self.assertIn('Servo Temps', self.joint_reader.read_temperatures())
        self.assertIn('Servo Voltages', self.servo_reader.read_voltages())
        self.assertIn('Cartesian Coords', self.spatial_reader.read_coords())
        self.assertIn('responsive', self.spatial_reader.probe_link())

    def test_coordinator_telemetry(self) -> None:
        '''
        Tests coordinator aggregation and startup summary.
        '''
        self.transport.open()
        summary = self.coordinator.get_startup_summary()
        self.assertEqual(len(summary), 5)
        self.assertIn('responsive', self.coordinator.diagnose_link())
        self.assertIn('Joint Angles', self.coordinator.diagnose_angles())
        self.assertIn('Cartesian Coords', self.coordinator.diagnose_coords())
        self.assertIn('Servo Temps', self.coordinator.diagnose_temperatures())
        self.assertIn('Servo Voltages', self.coordinator.diagnose_voltages())
        self.assertIn('Power On frame sent', self.coordinator.re_enable_power())
        self.assertIn('Servos released', self.coordinator.release_servos())

    def test_protocol_compliance(self) -> None:
        '''
        Verifies structural Protocol conformance.
        '''
        self.assertIsInstance(self.joint_reader, IJointDiagnosticsReader)
        self.assertIsInstance(self.servo_reader, IServoDiagnosticsReader)
        self.assertIsInstance(self.spatial_reader, ISpatialDiagnosticsReader)
        self.assertIsInstance(self.coordinator, IDiagnosticsCoordinator)

    def test_version_methods(self) -> None:
        '''
        Tests version string retrieval across all components.
        '''
        self.assertEqual(self.joint_reader.get_version(), '1.0.3')
        self.assertEqual(self.servo_reader.get_version(), '1.0.3')
        self.assertEqual(self.spatial_reader.get_version(), '1.0.3')
        self.assertEqual(self.coordinator.get_version(), '1.0.3')
        self.assertEqual(DiagnosticsFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
