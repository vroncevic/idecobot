# -*- coding: UTF-8 -*-

'''
Module
    idiagnostics_menu_handler.py
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
    Defines structural interface protocol IDiagnosticsMenuHandler for robot diagnostics actions.
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
class IDiagnosticsMenuHandler(Protocol):
    '''
    Structural interface protocol for diagnostics menu actions and logging.

    It defines:

        :methods:
            | diagnose_link - Probes hardware link responsiveness.
            | diagnose_angles - Queries and logs joint angles telemetry.
            | diagnose_coords - Queries and logs Cartesian coordinates telemetry.
            | diagnose_temperatures - Queries and logs servo motor temperatures.
            | diagnose_voltages - Queries and logs servo operating voltages.
            | diagnose_power_on - Re-enables power to all servos.
            | diagnose_release_servos - Releases servo torque for lead-through.
            | run_startup_diagnostics - Queries and logs baseline telemetry upon connection.
            | get_version - Returns protocol version string.
    '''

    def diagnose_link(self) -> None:
        '''
        Probes hardware link responsiveness.
        '''

    def diagnose_angles(self) -> None:
        '''
        Queries and logs joint angles telemetry.
        '''

    def diagnose_coords(self) -> None:
        '''
        Queries and logs Cartesian coordinates telemetry.
        '''

    def diagnose_temperatures(self) -> None:
        '''
        Queries and logs servo motor temperatures.
        '''

    def diagnose_voltages(self) -> None:
        '''
        Queries and logs servo operating voltages.
        '''

    def diagnose_power_on(self) -> None:
        '''
        Re-enables power to all servos.
        '''

    def diagnose_release_servos(self) -> None:
        '''
        Releases servo torque for lead-through.
        '''

    def run_startup_diagnostics(self) -> None:
        '''
        Queries and logs baseline telemetry upon connection.
        '''

    def get_version(self) -> str:
        '''
        Returns protocol version string.

        :return: Version string.
        '''
