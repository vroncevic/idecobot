# -*- coding: UTF-8 -*-

'''
Module
    diagnostics_menu_handler.py
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
    Dispatches diagnostic queries and commands to coordinator and logs formatted output.
'''

from __future__ import annotations

from collections.abc import Callable

from idecobot.infrastructure.diagnostics.idiagnostics_coordinator import IDiagnosticsCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DiagnosticsMenuHandler:
    '''
    Dispatches diagnostic queries and commands to coordinator and logs formatted output.

    It defines:

        :attributes:
            | _diagnostics - Injected IDiagnosticsCoordinator.
            | _on_log - Callback for logging message string.
        :methods:
            | __init__ - Initializes diagnostics menu handler with injected coordinator and log callback.
            | diagnose_link - Probes hardware link responsiveness.
            | diagnose_angles - Queries and logs joint angles telemetry.
            | diagnose_coords - Queries and logs Cartesian coordinates telemetry.
            | diagnose_temperatures - Queries and logs servo motor temperatures.
            | diagnose_voltages - Queries and logs servo operating voltages.
            | diagnose_power_on - Re-enables power to all servos.
            | diagnose_release_servos - Releases servo torque for lead-through.
            | run_startup_diagnostics - Queries and logs baseline telemetry upon connection.
            | get_version - Returns handler version string.
    '''

    _diagnostics: IDiagnosticsCoordinator
    _on_log: Callable[[str], None]

    def __init__(
        self,
        diagnostics: IDiagnosticsCoordinator,
        on_log: Callable[[str], None]
    ) -> None:
        '''
        Initializes diagnostics menu handler with injected coordinator and log callback.

        :param diagnostics: Injected IDiagnosticsCoordinator.
        :param on_log: Callback for logging message string.
        '''
        self._diagnostics = diagnostics
        self._on_log = on_log

    def diagnose_link(self) -> None:
        '''
        Probes hardware link responsiveness.
        '''
        self._on_log(self._diagnostics.diagnose_link())

    def diagnose_angles(self) -> None:
        '''
        Queries and logs joint angles telemetry.
        '''
        self._on_log(self._diagnostics.diagnose_angles())

    def diagnose_coords(self) -> None:
        '''
        Queries and logs Cartesian coordinates telemetry.
        '''
        self._on_log(self._diagnostics.diagnose_coords())

    def diagnose_temperatures(self) -> None:
        '''
        Queries and logs servo motor temperatures.
        '''
        self._on_log(self._diagnostics.diagnose_temperatures())

    def diagnose_voltages(self) -> None:
        '''
        Queries and logs servo operating voltages.
        '''
        self._on_log(self._diagnostics.diagnose_voltages())

    def diagnose_power_on(self) -> None:
        '''
        Re-enables power to all servos.
        '''
        self._on_log(self._diagnostics.re_enable_power())

    def diagnose_release_servos(self) -> None:
        '''
        Releases servo torque for lead-through.
        '''
        self._on_log(self._diagnostics.release_servos())

    def run_startup_diagnostics(self) -> None:
        '''
        Queries and logs baseline telemetry upon connection.
        '''
        for line in self._diagnostics.get_startup_summary():
            self._on_log(line)

    def get_version(self) -> str:
        '''
        Returns handler version string.

        :return: Version string.
        '''
        return __version__
