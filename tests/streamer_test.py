# -*- coding: UTF-8 -*-

'''
Module
    streamer_test.py
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
    Unit tests for MyCobot streamer and streamer factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.model.communication.stream_config import StreamConfig
from idecobot.core.model.communication.stream_state import StreamState
from idecobot.infrastructure.communication.transport.transport_constants import (
    TransportConstants
)
from idecobot.core.service.communication.imycobot_streamer import (
    IMyCobotStreamer
)
from idecobot.infrastructure.communication.protocol.protocol_framer import (
    ProtocolFramer
)
from idecobot.infrastructure.communication.streamer.istreamer_factory import (
    IStreamerFactory
)
from idecobot.infrastructure.communication.streamer.mycobot_streamer import (
    MyCobotStreamer
)
from idecobot.infrastructure.communication.streamer.streamer_factory import (
    StreamerFactory
)
from idecobot.infrastructure.communication.transport.mock_serial_transport import (
    MockSerialTransport
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMyCobotStreamer(TestCase):
    '''
        Tests for StreamerFactory and MyCobotStreamer components.

        It defines:

            :methods:
                | setUp - Initializes mock transport and protocol framer.
                | test_streamer_factory_protocol - Verifies IStreamerFactory protocol conformance.
                | test_streamer_protocol - Verifies IMyCobotStreamer protocol conformance.
                | test_streamer_versions - Verifies get_version returns __version__.
                | test_transmit_frame - Tests single frame transmission over transport.
                | test_streaming_lifecycle - Tests stream, pause, resume, and stop controls.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.
        '''
        self.transport_constants: TransportConstants = TransportConstants()
        self.protocol_constants: ProtocolConstants = ProtocolConstants()
        self.transport: MockSerialTransport = MockSerialTransport(
            transport_constants=self.transport_constants,
            protocol_constants=self.protocol_constants
        )
        self.transport.open()
        self.framer: ProtocolFramer = ProtocolFramer(constants=self.protocol_constants)
        self.streamer: MyCobotStreamer = StreamerFactory.create(
            transport=self.transport,
            framer=self.framer
        )

    def test_streamer_factory_protocol(self) -> None:
        '''
            Verifies StreamerFactory conforms structurally to IStreamerFactory.
        '''
        self.assertIsInstance(StreamerFactory, IStreamerFactory)

    def test_streamer_protocol(self) -> None:
        '''
            Verifies MyCobotStreamer conforms structurally to IMyCobotStreamer.
        '''
        self.assertIsInstance(self.streamer, IMyCobotStreamer)

    def test_streamer_versions(self) -> None:
        '''
            Verifies get_version implementations return string version matching __version__.
        '''
        self.assertEqual(StreamerFactory.get_version(), '1.0.3')
        self.assertEqual(self.streamer.get_version(), '1.0.3')

    def test_transmit_frame(self) -> None:
        '''
            Tests transmitting a single frame writes wire bytes to transport.
        '''
        frame: MyCobotFrame = MyCobotFrame(
            cmd_id=self.protocol_constants.cmd_power_on,
            payload=bytes([1]),
            delay_after_sec=0.0
        )
        self.streamer.transmit_frame(frame, delay_scale=1.0)
        history: tuple[bytes, ...] = self.transport.get_history()
        self.assertTrue(len(history) > 0)

    def test_streaming_lifecycle(self) -> None:
        '''
            Tests streaming start, progress, and control operations.
        '''
        frame: MyCobotFrame = MyCobotFrame(
            cmd_id=self.protocol_constants.cmd_power_on,
            payload=bytes([1]),
            delay_after_sec=0.001
        )
        config: StreamConfig = StreamConfig(playback_rate=1.0)
        started: bool = self.streamer.stream([frame], config=config)
        self.assertTrue(started)

        self.streamer.pause()
        self.streamer.resume()
        self.streamer.stop()
        self.assertEqual(self.streamer.get_state(), StreamState.STOPPED)


if __name__ == '__main__':
    main()
