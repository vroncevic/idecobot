# -*- coding: UTF-8 -*-

'''
Module
    servo_diagnostics_reader.py
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
    Implements ServoDiagnosticsReader querying servo voltages and re-engaging power.
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


class ServoDiagnosticsReader:
    '''
    Queries servo supply voltages and dispatches power on commands.

    It defines:

        :attributes:
            | _transport - Injected ITransport communications channel.
            | _codec - Injected IMyCobotProtocolCodec frame encoder/decoder.
            | _constants - Injected DiagnosticsConstants configuration.
            | _proto - Injected ProtocolConstants framing values.
        :methods:
            | __init__ - Initializes servo diagnostics reader.
            | read_voltages - Queries and formats operating voltages for all joint servos.
            | power_on - Transmits power on command to re-enable servo torque.
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
        Initializes servo diagnostics reader with injected dependencies.

        :param transport: Injected ITransport communications channel.
        :param codec: Injected IMyCobotProtocolCodec frame encoder/decoder.
        :param constants: Injected DiagnosticsConstants configuration.
        :param proto: Injected ProtocolConstants framing values.
        '''
        self._transport = transport
        self._codec = codec
        self._constants = constants
        self._proto = proto

    def read_voltages(self) -> str:
        '''
        Queries and formats operating voltages for all joint servos.

        :return: Formatted diagnostics string with low-voltage warnings.
        '''
        if not self._transport.is_open():
            return self._constants.msg_not_connected

        frame: MyCobotFrame = MyCobotFrame(self._proto.cmd_get_servo_voltages, b'', 0.05)
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
            return '❌ [DIAG] Failed to read servo voltages (no response).'

        volts: list[float] = [b / 10.0 for b in payload[:6]]
        has_low_v: bool = any(v < self._constants.voltage_warn_threshold for v in volts)
        prefix: str = '⚠️ [WARN]' if has_low_v else 'ℹ [DIAG]'

        items: list[str] = [
            f'J{i + 1}={v:.1f}V{" (⚠️ LOW!)" if v < self._constants.voltage_warn_threshold else ""}'
            for i, v in enumerate(volts)
        ]

        return f'{prefix} Servo Voltages: {", ".join(items)}'

    def power_on(self) -> str:
        '''
        Transmits power on command to re-enable servo torque.

        :return: Status confirmation message.
        '''
        if not self._transport.is_open():
            return self._constants.msg_not_connected

        frame: MyCobotFrame = self._codec.pack_power()
        raw_cmd: bytes = self._codec.encode_frame(frame)
        self._transport.write(raw_cmd)

        return self._constants.msg_power_on_sent

    def get_version(self) -> str:
        '''
        Returns component version string.

        :return: Version string.
        '''
        return __version__
