# -*- coding: UTF-8 -*-

'''
Module
    serial_port_scanner.py
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
    Defines SerialPortScanner enumerating hardware COM / TTY serial ports.
'''

from __future__ import annotations

from collections.abc import Sequence
from serial.tools.list_ports import comports

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPortScanner:
    '''
        Discovers serial communication ports connected to host machine.

        It defines:

            :methods:
                | scan_ports - Queries OS for available serial ports.
                | is_port_available - Verifies whether specified serial port is detected.
    '''

    def scan_ports(self) -> Sequence[str]:
        '''
            Queries operating system for active serial communications ports.

            :return: Sorted sequence of device port identifiers.
            :exceptions: None.
        '''
        ports: list[str] = [port_info.device for port_info in comports()]
        ports.sort()

        return tuple(ports)

    def is_port_available(self, port: str) -> bool:
        '''
            Verifies whether specified serial port path is currently detected.

            :param port: Device path or COM port name to verify.
            :return: True if port is detected, False otherwise.
            :exceptions: None.
        '''
        return port in self.scan_ports()
