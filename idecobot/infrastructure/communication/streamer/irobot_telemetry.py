# -*- coding: UTF-8 -*-

'''
Module
    irobot_telemetry.py
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
    Defines structural interface protocol for querying robot telemetry and hardware status.
'''

from __future__ import annotations

from collections.abc import Sequence
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
class IRobotTelemetry(Protocol):
    '''
        Defines structural interface protocol for robot hardware state queries.

        It defines:

            :methods:
                | read_angles - Queries current joint angles from hardware.
                | ping - Verifies robot hardware responsiveness.
                | get_version - Returns robot telemetry component version string.
    '''

    def read_angles(self) -> Sequence[float] | None:
        '''
            Queries current joint angles from hardware.

            :return: Sequence of 6 angles in degrees, or None if unavailable.
        '''

    def ping(self) -> bool:
        '''
            Verifies robot hardware responsiveness.

            :return: True if hardware responds to query, False otherwise.
        '''

    def get_version(self) -> str:
        '''
            Returns robot telemetry component version string.

            :return: Component version string.
        '''
