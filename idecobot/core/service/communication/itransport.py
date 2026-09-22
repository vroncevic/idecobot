# -*- coding: UTF-8 -*-

'''
Module
    itransport.py
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
    Defines structural interface protocol for byte stream hardware transports.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITransport(Protocol):
    '''
        Defines structural interface protocol for serial/socket communication transports.

        It defines:

            :methods:
                | configure - Configures transport endpoint and baud rate parameters.
                | open - Opens the transport connection.
                | close - Closes the transport connection.
                | write - Transmits byte buffer to transport.
                | read - Reads requested number of bytes from transport.
                | is_open - Checks if transport channel is actively open.
                | flush - Flushes transport write/read buffers.
                | get_version - Returns transport component version string.
    '''

    def configure(self, port: str, baudrate: int) -> None:
        '''
            Configures transport endpoint and baud rate parameters.

            :param port: Device path or host address.
            :param baudrate: Communication baud rate in bps.
        '''

    def open(self) -> bool:
        '''
            Opens the transport connection.

            :return: True if successfully opened, False otherwise.
        '''

    def close(self) -> None:
        '''
            Closes the transport connection.
        '''

    def write(self, data: bytes) -> int:
        '''
            Transmits byte buffer to transport.

            :param data: Byte sequence to transmit.
            :return: Number of bytes successfully written.
        '''

    def read(self, size: int = 1) -> bytes:
        '''
            Reads requested number of bytes from transport.

            :param size: Number of bytes to read.
            :return: Received bytes sequence.
        '''

    def is_open(self) -> bool:
        '''
            Checks if transport channel is actively open.

            :return: True if open, False otherwise.
        '''

    def flush(self) -> None:
        '''
            Flushes transport write and read buffers.
        '''

    def get_version(self) -> str:
        '''
            Returns transport component version string.

            :return: Component version string.
        '''

