# -*- coding: UTF-8 -*-

'''
Module
    transport_constants.py
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
    Defines TransportConstants configuration dataclass for serial transport infrastructure.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class TransportConstants:
    '''
        Default configuration constants for serial transport infrastructure.

        It defines:

            :attributes:
                | default_port - Default hardware serial port path string.
                | default_baudrate - Default communication baudrate.
                | standard_baudrates - Tuple of standard serial baudrates.
                | default_timeout - Default serial read timeout in seconds.
                | default_read_size - Default chunk size in bytes for single read operation.
                | empty_payload - Empty byte sequence constant.
                | zero_bytes_written - Zero byte count write indicator.
    '''

    default_port: str = '/dev/ttyUSB0'
    default_baudrate: int = 115200
    standard_baudrates: tuple[int, ...] = (9600, 19200, 57600, 115200, 1000000)
    default_timeout: float = 0.5
    default_read_size: int = 1
    empty_payload: bytes = b''
    zero_bytes_written: int = 0
