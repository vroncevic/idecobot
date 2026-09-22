# -*- coding: UTF-8 -*-

'''
Module
    spatial_diagnostics_reader.py
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
    Implements SpatialDiagnosticsReader querying Cartesian coords and link responsiveness.
'''

from __future__ import annotations

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.service.communication.itransport import ITransport
from idecobot.infrastructure.communication.protocol.imycobot_protocol_codec import IMyCobotProtocolCodec
from idecobot.infrastructure.diagnostics.diagnostics_constants import DiagnosticsConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SpatialDiagnosticsReader:
    '''
    Queries Cartesian tool coordinates and verifies hardware link connectivity.

    It defines:

        :attributes:
            | _transport - Injected ITransport communications channel.
            | _codec - Injected IMyCobotProtocolCodec frame encoder/decoder.
            | _constants - Injected DiagnosticsConstants configuration.
            | _proto - Injected ProtocolConstants framing values.
        :methods:
            | __init__ - Initializes spatial diagnostics reader.
            | read_coords - Queries and formats current tool center point Cartesian coordinates.
            | probe_link - Tests hardware responsiveness and link connectivity.
            | get_version - Returns component version string.
    '''

    _transport: ITransport
    _codec: IMyCobotProtocolCodec
    _constants: DiagnosticsConstants
    _proto: ProtocolConstants

    def __init__(
        self,
        transport: ITransport,
        codec: IMyCobotProtocolCodec,
        constants: DiagnosticsConstants,
        proto: ProtocolConstants
    ) -> None:
        '''
        Initializes spatial diagnostics reader with injected dependencies.

        :param transport: Injected ITransport communications channel.
        :param codec: Injected IMyCobotProtocolCodec frame encoder/decoder.
        :param constants: Injected DiagnosticsConstants configuration.
        :param proto: Injected ProtocolConstants framing values.
        '''
        self._transport = transport
        self._codec = codec
        self._constants = constants
        self._proto = proto

    def read_coords(self) -> str:
        '''
        Queries and formats current tool center point Cartesian coordinates.

        :return: Formatted diagnostics string.
        '''
        if not self._transport.is_open():
            return self._constants.msg_not_connected

        frame: MyCobotFrame = MyCobotFrame(self._proto.cmd_get_coords, b'', 0.05)
        raw_cmd: bytes = self._codec.encode_frame(frame)
        self._transport.flush()
        self._transport.write(raw_cmd)

        raw_resp: bytes = self._transport.read(self._proto.full_angles_response_len)
        payload: bytes | None = self._codec.extract_response_payload(
            raw_resp,
            self._proto.min_angles_frame_len,
            self._constants.prefix_len,
            self._proto.min_angles_response_len
        )

        if payload is None:
            return '❌ [DIAG] Failed to read Cartesian coordinates (no response).'

        coords = self._codec.unpack_coords(payload)

        if coords is None:
            return '❌ [DIAG] Invalid Cartesian coordinate payload format.'

        return (
            f'ℹ [DIAG] Cartesian Coords: X={coords[0]:.1f}mm, Y={coords[1]:.1f}mm, '
            f'Z={coords[2]:.1f}mm, Rx={coords[3]:.1f}°, Ry={coords[4]:.1f}°, Rz={coords[5]:.1f}°'
        )

    def probe_link(self) -> str:
        '''
        Tests hardware responsiveness and link connectivity.

        :return: Connection health status string.
        '''
        if not self._transport.is_open():
            return self._constants.msg_not_connected

        frame: MyCobotFrame = MyCobotFrame(self._proto.cmd_get_angles, b'', 0.05)
        raw_cmd: bytes = self._codec.encode_frame(frame)
        self._transport.flush()
        self._transport.write(raw_cmd)

        raw_resp: bytes = self._transport.read(self._proto.full_angles_response_len)
        payload: bytes | None = self._codec.extract_response_payload(
            raw_resp,
            self._proto.min_angles_frame_len,
            self._constants.prefix_len,
            self._proto.min_angles_response_len
        )

        if payload is None:
            return self._constants.msg_link_offline

        return self._constants.msg_link_online

    def get_version(self) -> str:
        '''
        Returns component version string.

        :return: Version string.
        '''
        return __version__
