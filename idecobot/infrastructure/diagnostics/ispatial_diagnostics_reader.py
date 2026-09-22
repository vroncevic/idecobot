# -*- coding: UTF-8 -*-

'''
Module
    ispatial_diagnostics_reader.py
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
    Defines structural interface protocol for Cartesian coordinates and serial link probing.
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
class ISpatialDiagnosticsReader(Protocol):
    '''
    Defines structural interface protocol for Cartesian coordinates and serial link probing.

    It defines:

        :methods:
            | read_coords - Queries and formats current tool center point Cartesian coordinates.
            | probe_link - Tests hardware responsiveness and link connectivity.
            | get_version - Returns component version string.
    '''

    def read_coords(self) -> str:
        '''
        Queries and formats current tool center point Cartesian coordinates.

        :return: Formatted diagnostics string.
        '''

    def probe_link(self) -> str:
        '''
        Tests hardware responsiveness and link connectivity.

        :return: Connection health status string.
        '''

    def get_version(self) -> str:
        '''
        Returns component version string.

        :return: Version string.
        '''
