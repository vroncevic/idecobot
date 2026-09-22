# -*- coding: UTF-8 -*-

'''
Module
    ijoint_diagnostics_reader.py
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
    Defines structural interface protocol for querying robot joint angles and temperatures.
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
class IJointDiagnosticsReader(Protocol):
    '''
    Defines structural interface protocol for robot joint diagnostic queries.

    It defines:

        :methods:
            | read_angles - Queries and formats current joint angles (J1-J6).
            | read_temperatures - Queries and formats current servo motor temperatures.
            | get_version - Returns component version string.
    '''

    def read_angles(self) -> str:
        '''
        Queries and formats current joint angles (J1-J6).

        :return: Formatted diagnostics string.
        '''

    def read_temperatures(self) -> str:
        '''
        Queries and formats current servo motor temperatures.

        :return: Formatted diagnostics string with overheat warnings.
        '''

    def get_version(self) -> str:
        '''
        Returns component version string.

        :return: Version string.
        '''
