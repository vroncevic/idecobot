# -*- coding: UTF-8 -*-

'''
Module
    mock_serial_transport.py
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
    Defines MockSerialTransport simulating robot responses for offline testing and development.
'''

from __future__ import annotations

from struct import pack

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.infrastructure.communication.transport.transport_constants import (
    TransportConstants,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockSerialTransport:
    '''
        Simulated loopback serial transport for offline development and testing.

        It defines:

            :attributes:
                | _transport_constants - Injected TransportConstants configuration settings.
                | _protocol_constants - Injected ProtocolConstants protocol framing values.
                | _is_open - Connection status flag.
                | _simulated_angles - Virtual joint angle positions in degrees.
                | _rx_buffer - Buffer holding simulated responses to be read.
                | _history - Log of transmitted byte sequences.
            :methods:
                | __init__ - Initializes mock serial transport with default home joint positions.
                | configure - Virtual configuration handler updating target endpoint.
                | open - Opens mock transport.
                | close - Closes mock transport.
                | write - Ingests bytes, updates simulation state, queues responses.
                | read - Reads simulated response bytes.
                | is_open - Returns virtual connection status.
                | flush - Clears buffers.
                | get_history - Returns transmitted byte history.
                | get_version - Returns mock serial transport component version string.
    '''

    _transport_constants: TransportConstants
    _protocol_constants: ProtocolConstants
    _is_open: bool
    _simulated_angles: list[float]
    _rx_buffer: bytearray
    _history: list[bytes]

    def __init__(
        self,
        transport_constants: TransportConstants,
        protocol_constants: ProtocolConstants
    ) -> None:
        '''
            Initializes mock serial transport with default home joint positions.

            :param transport_constants: Injected TransportConstants configuration instance.
            :param protocol_constants: Injected ProtocolConstants protocol parameters.
            :exceptions: None.
        '''
        self._transport_constants = transport_constants
        self._protocol_constants = protocol_constants
        self._is_open = False
        self._simulated_angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self._rx_buffer = bytearray()
        self._history = []

    def configure(self, port: str, baudrate: int) -> None:
        '''
            Virtual configuration handler updating target endpoint.

            :param port: Device path or address.
            :param baudrate: Communication baud rate.
            :exceptions: None.
        '''

    def open(self) -> bool:
        '''
            Opens mock transport.

            :return: Always True for virtual connection.
            :exceptions: None.
        '''
        self._is_open = True
        return True

    def close(self) -> None:
        '''
            Closes mock transport.

            :exceptions: None.
        '''
        self._is_open = False
        self._rx_buffer.clear()

    def write(self, data: bytes) -> int:
        '''
            Ingests bytes, updates simulated robot state, and queues responses.

            :param data: Byte sequence transmitted to simulated robot.
            :return: Number of bytes processed.
            :exceptions: None.
        '''
        if not self._is_open:
            return self._transport_constants.zero_bytes_written

        self._history.append(data)

        min_cmd_len: int = 4
        if (
            len(data) >= min_cmd_len
            and data[0] == self._protocol_constants.header_byte_1
            and data[1] == self._protocol_constants.header_byte_2
        ):
            cmd_id: int = data[3]
            if cmd_id == self._protocol_constants.cmd_get_angles:
                len_byte: int = (
                    self._protocol_constants.min_angles_response_len
                    + self._protocol_constants.length_overhead
                )
                header: bytes = bytes([
                    self._protocol_constants.header_byte_1,
                    self._protocol_constants.header_byte_2,
                    len_byte,
                    self._protocol_constants.cmd_get_angles
                ])
                scaled: list[int] = [
                    int(round(a * self._protocol_constants.angle_scale_factor))
                    for a in self._simulated_angles
                ]
                payload: bytes = pack(
                    self._protocol_constants.format_joints_payload,
                    *scaled
                )
                footer: bytes = bytes([self._protocol_constants.footer_byte])
                self._rx_buffer.extend(header + payload + footer)

        return len(data)

    def read(self, size: int = 1) -> bytes:
        '''
            Reads simulated response bytes.

            :param size: Maximum bytes to read.
            :return: Bytes from simulated RX buffer.
            :exceptions: None.
        '''
        if not self._is_open or not self._rx_buffer:
            return self._transport_constants.empty_payload

        chunk: bytes = bytes(self._rx_buffer[:size])

        del self._rx_buffer[:size]

        return chunk

    def is_open(self) -> bool:
        '''
            Returns virtual connection status.

            :return: True if virtual channel open, False otherwise.
            :exceptions: None.
        '''
        return self._is_open

    def flush(self) -> None:
        '''
            Clears virtual buffers.

            :exceptions: None.
        '''
        self._rx_buffer.clear()

    def get_history(self) -> tuple[bytes, ...]:
        '''
            Returns log of transmitted byte sequences.

            :return: Tuple of raw byte records.
            :exceptions: None.
        '''
        return tuple(self._history)

    def get_version(self) -> str:
        '''
            Returns mock serial transport component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__

