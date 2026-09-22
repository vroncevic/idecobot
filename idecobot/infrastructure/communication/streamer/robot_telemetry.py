# -*- coding: UTF-8 -*-

'''
Module
    robot_telemetry.py
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
    Implements robot hardware status query and joint angles telemetry reading.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.service.communication.itransport import ITransport
from idecobot.infrastructure.communication.protocol.imycobot_protocol_codec import IMyCobotProtocolCodec

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RobotTelemetry:
    '''
        Queries telemetry data and hardware responsiveness from manipulator.

        It defines:

            :methods:
                | __init__ - Initializes telemetry reader with transport, codec, and constants.
                | read_angles - Queries current joint angles from hardware.
                | ping - Verifies robot hardware responsiveness.
                | get_version - Returns robot telemetry component version string.
    '''

    _prefix_len: int = 4

    def __init__(
        self,
        transport: ITransport,
        codec: IMyCobotProtocolCodec,
        constants: ProtocolConstants
    ) -> None:
        '''
            Initializes telemetry reader with transport, codec, and constants.

            :param transport: Injected ITransport channel instance.
            :param codec: Injected IMyCobotProtocolCodec frame encoder/decoder.
            :param constants: Injected ProtocolConstants framing parameters.
            :exceptions: None.
        '''
        self._transport: ITransport = transport
        self._codec: IMyCobotProtocolCodec = codec
        self._constants: ProtocolConstants = constants

    def read_angles(self) -> Sequence[float] | None:
        '''
            Queries current joint angles from hardware.

            :return: Sequence of 6 angles in degrees, or None if unavailable.
            :exceptions: None.
        '''
        if not self._transport.is_open():
            return None

        query_frame: MyCobotFrame = self._codec.pack_get_angles()
        raw_bytes: bytes = self._codec.encode_frame(query_frame)

        if self._transport.write(raw_bytes) != len(raw_bytes):
            return None

        resp: bytes = self._transport.read(self._constants.full_angles_response_len)
        payload: bytes | None = self._codec.extract_response_payload(
            resp,
            self._constants.min_angles_frame_len,
            self._prefix_len,
            self._constants.min_angles_response_len
        )

        if payload is None:
            return None

        return self._codec.unpack_angles(payload)

    def ping(self) -> bool:
        '''
            Verifies robot hardware responsiveness.

            :return: True if hardware responds to query, False otherwise.
            :exceptions: None.
        '''
        return self.read_angles() is not None

    def get_version(self) -> str:
        '''
            Returns robot telemetry component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
