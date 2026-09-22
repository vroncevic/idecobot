# -*- coding: UTF-8 -*-

'''
Module
    diagnostics_constants.py
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
    Defines DiagnosticsConstants dataclass for hardware diagnostic thresholds and messages.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class DiagnosticsConstants:
    '''
    Immutable configuration parameters and status tokens for hardware diagnostics.

    It defines:

        :attributes:
            | temp_warn_threshold - Temperature in Celsius triggering overheat warning (50).
            | voltage_warn_threshold - Voltage triggering low voltage warning (6.8).
            | prefix_len - Prefix length for Elephant Robotics framing (4).
            | read_timeout - Serial read response timeout in seconds (0.5).
            | msg_not_connected - Warning message when serial port is disconnected.
            | msg_power_on_sent - Confirmation message after re-engaging servos.
            | msg_relax_sent - Confirmation message after relaxing servos.
            | msg_link_online - Status message when robot replies to probe.
            | msg_link_offline - Status message when robot fails to reply.
    '''

    temp_warn_threshold: int = 50
    voltage_warn_threshold: float = 6.8
    prefix_len: int = 4
    read_timeout: float = 0.5
    msg_not_connected: str = (
        '❌ [DIAG] Robot is not connected! Please connect via toolbar first.'
    )
    msg_power_on_sent: str = 'ℹ [DIAG] Power On frame sent. Servos re-engaged.'
    msg_relax_sent: str = 'ℹ [DIAG] Servos released (manual lead-through active).'
    msg_link_online: str = 'ℹ [DIAG] Controller Link: ONLINE (115200 baud, responsive)'
    msg_link_offline: str = '❌ [DIAG] Controller Link: OFFLINE (Hardware probe failed)'
