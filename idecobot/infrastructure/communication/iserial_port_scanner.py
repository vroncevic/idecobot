# -*- coding: UTF-8 -*-

'''
Module
    iserial_port_scanner.py
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
    Defines structural interface protocol for serial hardware port discovery.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISerialPortScanner(Protocol):
    '''
        Defines structural interface protocol for scanning available serial ports.

        It defines:

            :methods:
                | scan_ports - Returns available system serial port descriptors.
                | is_port_available - Verifies whether a specific serial port is detected.
    '''

    def scan_ports(self) -> Sequence[str]:
        '''
            Returns available system serial port descriptors.

            :return: Sequence of port path strings.
        '''

    def is_port_available(self, port: str) -> bool:
        '''
            Verifies whether a specific serial port is currently detected.

            :param port: Device path or COM port name to verify.
            :return: True if port is detected, False otherwise.
        '''

    def get_version(self) -> str:
        '''
            Returns scanner protocol version string.

            :return: Component version string.
        '''
