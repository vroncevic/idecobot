# -*- coding: UTF-8 -*-

'''
Module
    iservo_diagnostics_reader.py
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
    Defines structural interface protocol for querying servo voltages and power re-engagement.
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
class IServoDiagnosticsReader(Protocol):
    '''
    Defines structural interface protocol for servo power and voltage diagnostics.

    It defines:

        :methods:
            | read_voltages - Queries and formats operating voltages for all joint servos.
            | power_on - Transmits power on command to re-enable servo torque.
            | get_version - Returns component version string.
    '''

    def read_voltages(self) -> str:
        '''
        Queries and formats operating voltages for all joint servos.

        :return: Formatted diagnostics string with low-voltage warnings.
        '''

    def power_on(self) -> str:
        '''
        Transmits power on command to re-enable servo torque.

        :return: Status confirmation message.
        '''

    def get_version(self) -> str:
        '''
        Returns component version string.

        :return: Version string.
        '''
