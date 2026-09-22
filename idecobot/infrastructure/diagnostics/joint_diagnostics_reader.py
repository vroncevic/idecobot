# -*- coding: UTF-8 -*-

'''
Module
    joint_diagnostics_reader.py
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
    Implements JointDiagnosticsReader querying joint angles and servo temperatures.
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


class JointDiagnosticsReader:
    '''
    Queries and formats joint angles and motor temperatures from robot.

    It defines:

        :attributes:
            | _transport - Injected ITransport communications channel.
            | _codec - Injected IMyCobotProtocolCodec frame encoder/decoder.
            | _constants - Injected DiagnosticsConstants configuration.
            | _proto - Injected ProtocolConstants framing values.
        :methods:
            | __init__ - Initializes joint diagnostics reader.
            | read_angles - Queries current joint angles (J1-J6).
            | read_temperatures - Queries current servo motor temperatures.
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
        Initializes joint diagnostics reader with injected dependencies.

        :param transport: Injected ITransport communications channel.
        :param codec: Injected IMyCobotProtocolCodec frame encoder/decoder.
        :param constants: Injected DiagnosticsConstants configuration.
        :param proto: Injected ProtocolConstants framing values.
        '''
        self._transport = transport
        self._codec = codec
        self._constants = constants
        self._proto = proto

    def read_angles(self) -> str:
        '''
        Queries and formats current joint angles (J1-J6).

        :return: Formatted diagnostics string.
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
            return '❌ [DIAG] Failed to read joint angles (no response).'

        angles = self._codec.unpack_angles(payload)

        if angles is None:
            return '❌ [DIAG] Invalid joint angle payload format.'

        return (
            f'ℹ [DIAG] Joint Angles: J1={angles[0]:.2f}°, J2={angles[1]:.2f}°, '
            f'J3={angles[2]:.2f}°, J4={angles[3]:.2f}°, J5={angles[4]:.2f}°, J6={angles[5]:.2f}°'
        )

    def read_temperatures(self) -> str:
        '''
        Queries and formats current servo motor temperatures.

        :return: Formatted diagnostics string with overheat warnings.
        '''
        if not self._transport.is_open():
            return self._constants.msg_not_connected

        frame: MyCobotFrame = MyCobotFrame(self._proto.cmd_get_servo_temps, b'', 0.05)
        raw_cmd: bytes = self._codec.encode_frame(frame)
        self._transport.flush()
        self._transport.write(raw_cmd)

        raw_resp: bytes = self._transport.read(self._proto.full_servos_response_len)
        payload: bytes | None = self._codec.extract_response_payload(
            raw_resp,
            self._proto.full_servos_response_len - 1,
            self._constants.prefix_len,
            self._proto.min_servos_response_len
        )

        if payload is None or len(payload) < 6:
            return '❌ [DIAG] Failed to read servo temperatures (no response).'

        temps: list[int] = list(payload[:6])
        has_overheat: bool = any(t >= self._constants.temp_warn_threshold for t in temps)
        prefix: str = '⚠️ [WARN]' if has_overheat else 'ℹ [DIAG]'

        items: list[str] = [
            f'J{i + 1}={t}°C{" (⚠️ OVERHEAT!)" if t >= self._constants.temp_warn_threshold else ""}'
            for i, t in enumerate(temps)
        ]

        return f'{prefix} Servo Temps: {", ".join(items)}'

    def get_version(self) -> str:
        '''
        Returns component version string.

        :return: Version string.
        '''
        return __version__
