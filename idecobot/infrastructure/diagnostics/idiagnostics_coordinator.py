# -*- coding: UTF-8 -*-

'''
Module
    idiagnostics_coordinator.py
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
    Defines structural interface protocol orchestrating high-level robot diagnostics.
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
class IDiagnosticsCoordinator(Protocol):
    '''
    Defines structural interface protocol orchestrating high-level robot diagnostics.

    It defines:

        :methods:
            | get_startup_summary - Returns sequence of baseline telemetry strings on connect.
            | diagnose_angles - Queries and formats current joint angles.
            | diagnose_coords - Queries and formats current Cartesian coordinates.
            | diagnose_temperatures - Queries and formats current servo motor temperatures.
            | diagnose_voltages - Queries and formats operating voltages.
            | diagnose_link - Verifies hardware communication responsiveness.
            | re_enable_power - Re-enables power to all robot servos.
            | release_servos - Releases servo torque for manual lead-through.
            | get_version - Returns component version string.
    '''

    def get_startup_summary(self) -> Sequence[str]:
        '''
        Returns sequence of baseline telemetry strings on connect.

        :return: Sequence of formatted telemetry lines.
        '''

    def diagnose_angles(self) -> str:
        '''
        Queries and formats current joint angles.

        :return: Formatted status string.
        '''

    def diagnose_coords(self) -> str:
        '''
        Queries and formats current Cartesian coordinates.

        :return: Formatted status string.
        '''

    def diagnose_temperatures(self) -> str:
        '''
        Queries and formats current servo motor temperatures.

        :return: Formatted status string.
        '''

    def diagnose_voltages(self) -> str:
        '''
        Queries and formats operating voltages.

        :return: Formatted status string.
        '''

    def diagnose_link(self) -> str:
        '''
        Verifies hardware communication responsiveness.

        :return: Formatted status string.
        '''

    def re_enable_power(self) -> str:
        '''
        Re-enables power to all robot servos.

        :return: Formatted status string.
        '''

    def release_servos(self) -> str:
        '''
        Releases servo torque for manual lead-through.

        :return: Formatted status string.
        '''

    def get_version(self) -> str:
        '''
        Returns component version string.

        :return: Version string.
        '''
