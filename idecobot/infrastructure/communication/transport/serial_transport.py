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

from idecobot.core.model.communication.serial_defaults import SerialDefaults

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialTransport:
    '''
        Physical serial port communications channel using PySerial.

        It defines:

            :attributes:
                | _defaults - Injected SerialDefaults configuration settings.
                | _port - Serial port device path string.
                | _baudrate - Communication speed in bits per second.
                | _timeout - Read timeout duration in seconds.
                | _serial - Internal active PySerial connection handle.
            :methods:
                | __init__ - Initializes serial transport configuration.
                | open - Connects to specified serial port.
                | close - Closes active connection.
                | write - Transmits bytes to device.
                | read - Reads requested byte count from device.
                | is_open - Checks if port is connected.
                | flush - Flushes communication buffers.
    '''

    _defaults: SerialDefaults
    _port: str
    _baudrate: int
    _timeout: float
    _serial: Serial | None

    def __init__(self, defaults: SerialDefaults) -> None:
        '''
            Initializes serial transport configuration.

            :param defaults: Injected SerialDefaults configuration instance.
            :exceptions: None.
        '''
        self._defaults = defaults
        self._port = defaults.default_port
        self._baudrate = defaults.default_baudrate
        self._timeout = defaults.default_timeout
        self._serial = None

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
            return self._defaults.zero_bytes_written
        try:
            return self._serial.write(data)

        except (SerialException, OSError):
            return self._defaults.zero_bytes_written

    def read(self, size: int = 1) -> bytes:
        '''
            Reads requested byte count from device.

            :param size: Number of bytes to read.
            :return: Received bytes sequence.
            :exceptions: None.
        '''
        if self._serial is None or not self._serial.is_open:
            return self._defaults.empty_payload
        try:
            return self._serial.read(size)

        except (SerialException, OSError):
            return self._defaults.empty_payload

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
