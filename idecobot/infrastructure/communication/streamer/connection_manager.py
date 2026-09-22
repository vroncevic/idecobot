# -*- coding: UTF-8 -*-

'''
Module
    connection_manager.py
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
    Implements robot connection session lifecycle management without reflection.
'''

from __future__ import annotations

from idecobot.core.service.communication.itransport import ITransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionManager:
    '''
        Manages communication transport lifecycle and connection sessions.

        It defines:

            :methods:
                | __init__ - Initializes connection manager with injected transport channel.
                | connect - Configures and opens transport communication link.
                | disconnect - Closes active hardware transport channel.
                | is_connected - Checks whether transport channel is actively connected.
                | get_transport - Returns the underlying transport instance.
                | get_version - Returns connection manager component version string.
    '''

    def __init__(self, transport: ITransport) -> None:
        '''
            Initializes connection manager with injected transport.

            :param transport: Injected ITransport channel instance.
            :exceptions: None.
        '''
        self._transport: ITransport = transport

    def connect(self, port: str, baudrate: int = 115200) -> bool:
        '''
            Configures and opens transport communication link.

            :param port: Device path or address.
            :param baudrate: Transmission baud rate (default 115200).
            :return: True if successfully connected, False otherwise.
            :exceptions: None.
        '''
        self._transport.configure(port, baudrate)

        return self._transport.open()

    def disconnect(self) -> None:
        '''
            Closes active hardware transport channel.

            :exceptions: None.
        '''
        self._transport.close()

    def is_connected(self) -> bool:
        '''
            Checks whether transport channel is actively connected.

            :return: True if active and open, False otherwise.
            :exceptions: None.
        '''
        return self._transport.is_open()

    def get_transport(self) -> ITransport:
        '''
            Returns the underlying transport instance.

            :return: Injected ITransport channel instance.
            :exceptions: None.
        '''
        return self._transport

    def get_version(self) -> str:
        '''
            Returns connection manager component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
