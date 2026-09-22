# -*- coding: UTF-8 -*-

'''
Module
    diagnostics_coordinator.py
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
    Coordinates specialized diagnostic readers into unified facade.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.service.communication.imycobot_controller import IMyCobotController
from idecobot.infrastructure.diagnostics.ijoint_diagnostics_reader import IJointDiagnosticsReader
from idecobot.infrastructure.diagnostics.iservo_diagnostics_reader import IServoDiagnosticsReader
from idecobot.infrastructure.diagnostics.ispatial_diagnostics_reader import ISpatialDiagnosticsReader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DiagnosticsCoordinator:
    '''
    Coordinates specialized diagnostic readers into unified facade.

    It defines:

        :attributes:
            | _joint_reader - Injected IJointDiagnosticsReader.
            | _servo_reader - Injected IServoDiagnosticsReader.
            | _spatial_reader - Injected ISpatialDiagnosticsReader.
            | _controller - Injected IMyCobotController.
        :methods:
            | __init__ - Initializes diagnostics coordinator.
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

    _joint_reader: IJointDiagnosticsReader
    _servo_reader: IServoDiagnosticsReader
    _spatial_reader: ISpatialDiagnosticsReader
    _controller: IMyCobotController

    def __init__(
        self,
        joint_reader: IJointDiagnosticsReader,
        servo_reader: IServoDiagnosticsReader,
        spatial_reader: ISpatialDiagnosticsReader,
        controller: IMyCobotController
    ) -> None:
        '''
        Initializes diagnostics coordinator with injected readers.

        :param joint_reader: Injected IJointDiagnosticsReader.
        :param servo_reader: Injected IServoDiagnosticsReader.
        :param spatial_reader: Injected ISpatialDiagnosticsReader.
        :param controller: Injected IMyCobotController.
        '''
        self._joint_reader = joint_reader
        self._servo_reader = servo_reader
        self._spatial_reader = spatial_reader
        self._controller = controller

    def get_startup_summary(self) -> Sequence[str]:
        '''
        Returns sequence of baseline telemetry strings on connect.

        :return: Sequence of formatted telemetry lines.
        '''
        return (
            self._spatial_reader.probe_link(),
            self._joint_reader.read_angles(),
            self._spatial_reader.read_coords(),
            self._joint_reader.read_temperatures(),
            self._servo_reader.read_voltages()
        )

    def diagnose_angles(self) -> str:
        '''
        Queries and formats current joint angles.

        :return: Formatted status string.
        '''
        return self._joint_reader.read_angles()

    def diagnose_coords(self) -> str:
        '''
        Queries and formats current Cartesian coordinates.

        :return: Formatted status string.
        '''
        return self._spatial_reader.read_coords()

    def diagnose_temperatures(self) -> str:
        '''
        Queries and formats current servo motor temperatures.

        :return: Formatted status string.
        '''
        return self._joint_reader.read_temperatures()

    def diagnose_voltages(self) -> str:
        '''
        Queries and formats operating voltages.

        :return: Formatted status string.
        '''
        return self._servo_reader.read_voltages()

    def diagnose_link(self) -> str:
        '''
        Verifies hardware communication responsiveness.

        :return: Formatted status string.
        '''
        return self._spatial_reader.probe_link()

    def re_enable_power(self) -> str:
        '''
        Re-enables power to all robot servos.

        :return: Formatted status string.
        '''
        return self._servo_reader.power_on()

    def release_servos(self) -> str:
        '''
        Releases servo torque for manual lead-through.

        :return: Formatted status string.
        '''
        self._controller.power(False)

        return 'ℹ [DIAG] Servos released (manual lead-through active).'

    def get_version(self) -> str:
        '''
        Returns component version string.

        :return: Version string.
        '''
        return __version__
