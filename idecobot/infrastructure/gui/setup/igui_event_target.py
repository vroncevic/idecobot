# -*- coding: UTF-8 -*-

'''
Module
    igui_event_target.py
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
    Defines structural interface protocol for receiving GUI mediated interaction events.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IGUIEventTarget(Protocol):
    '''
        Defines structural interface protocol for handling GUI user interaction events.

        It defines:

            :methods:
                | connect_port - Dispatches serial communication port connection.
                | disconnect_port - Dispatches serial communication port disconnection.
                | run_stream - Dispatches trajectory streaming execution.
                | pause_stream - Dispatches trajectory streaming pause.
                | stop_stream - Dispatches trajectory streaming stop.
                | append_log - Dispatches log entry emission.
                | on_bytecode - Dispatches compiled bytecode frame sequence.
                | get_version - Returns event target interface version string.
    '''

    def connect_port(self, port: str, baud: int = 115200) -> bool:
        '''
            Connects to specified serial communication port.

            :param port: Serial device path string.
            :param baud: Communication baudrate.
            :return: True if connected successfully, False otherwise.
        '''

    def disconnect_port(self) -> None:
        '''
            Disconnects from active serial communication port.
        '''

    def run_stream(self) -> None:
        '''
            Initiates robot trajectory streaming.
        '''

    def pause_stream(self) -> None:
        '''
            Pauses active robot trajectory streaming.
        '''

    def stop_stream(self) -> None:
        '''
            Stops active robot trajectory streaming.
        '''

    def append_log(self, message: str) -> None:
        '''
            Emits a log message to the active monitor.

            :param message: Formatted log message text.
        '''

    def on_bytecode(self, frames: Sequence[MyCobotFrame]) -> None:
        '''
            Receives compiled robot bytecode frame sequence.

            :param frames: Sequence of compiled MyCobotFrame instances.
        '''

    def get_version(self) -> str:
        '''
            Returns event target interface version string.

            :return: Component version string.
        '''
