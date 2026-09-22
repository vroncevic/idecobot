# -*- coding: UTF-8 -*-

'''
Module
    serial_transport.py
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
    Defines SerialTransport implementing physical UART serial connection.
'''

from __future__ import annotations

from serial import Serial, SerialException

from idecobot.infrastructure.communication.transport.transport_constants import TransportConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialTransport:
    '''
        Physical serial port communications channel using PySerial.

        It defines:

            :attributes:
                | _constants - Injected TransportConstants configuration settings.
                | _port - Serial port device path string.
                | _baudrate - Communication speed in bits per second.
                | _timeout - Read timeout duration in seconds.
                | _serial - Internal active PySerial connection handle.
            :methods:
                | __init__ - Initializes serial transport configuration.
                | configure - Configures target serial port and baud rate.
                | open - Connects to specified serial port.
                | close - Closes active connection.
                | write - Transmits bytes to device.
                | read - Reads requested byte count from device.
                | is_open - Checks if port is connected.
                | flush - Flushes communication buffers.
                | get_version - Returns serial transport component version string.
    '''

    _constants: TransportConstants
    _port: str
    _baudrate: int
    _timeout: float
    _serial: Serial | None

    def __init__(self, constants: TransportConstants) -> None:
        '''
            Initializes serial transport configuration.

            :param constants: Injected TransportConstants configuration instance.
            :exceptions: None.
        '''
        self._constants = constants
        self._port = constants.default_port
        self._baudrate = constants.default_baudrate
        self._timeout = constants.default_timeout
        self._serial = None

    def configure(self, port: str, baudrate: int) -> None:
        '''
            Configures target serial port and baud rate.

            :param port: Device path for serial communication.
            :param baudrate: Communication baud rate in bps.
            :exceptions: None.
        '''
        self._port = port
        self._baudrate = baudrate

    def open(self) -> bool:
        '''
            Opens the physical serial port connection.

            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''
        try:
            self._serial = Serial(
                port=self._port,
                baudrate=self._baudrate,
                timeout=self._timeout
            )
            return self._serial.is_open

        except (SerialException, OSError):
            self._serial = None
            return False

    def close(self) -> None:
        '''
            Closes active serial connection.

            :exceptions: None.
        '''
        if self._serial is not None and self._serial.is_open:
            try:
                self._serial.close()

            except (SerialException, OSError):
                pass
        self._serial = None

    def write(self, data: bytes) -> int:
        '''
            Transmits bytes to device.

            :param data: Byte sequence to write.
            :return: Number of bytes written.
            :exceptions: None.
        '''
        if self._serial is None or not self._serial.is_open:
            return self._constants.zero_bytes_written
        try:
            return self._serial.write(data)

        except (SerialException, OSError):
            return self._constants.zero_bytes_written

    def read(self, size: int = 1) -> bytes:
        '''
            Reads requested byte count from device.

            :param size: Number of bytes to read.
            :return: Received bytes sequence.
            :exceptions: None.
        '''
        if self._serial is None or not self._serial.is_open:
            return self._constants.empty_payload
        try:
            return self._serial.read(size)

        except (SerialException, OSError):
            return self._constants.empty_payload

    def is_open(self) -> bool:
        '''
            Checks if port is connected.

            :return: True if open, False otherwise.
            :exceptions: None.
        '''
        return self._serial is not None and self._serial.is_open

    def flush(self) -> None:
        '''
            Flushes serial communication buffers.

            :exceptions: None.
        '''
        if self._serial is not None and self._serial.is_open:
            try:
                self._serial.flush()

            except (SerialException, OSError):
                pass

    def get_version(self) -> str:
        '''
            Returns serial transport component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__

