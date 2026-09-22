# -*- coding: UTF-8 -*-

'''
Module
    igui_event_handler.py
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
    Defines IGUIEventHandler structural protocol for GUI event delegate callbacks.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IGUIEventHandler(Protocol):
    '''
        Protocol defining callbacks and actions handled by the GUI event delegate.

        It defines:

            :methods:
                | connect_port - Connects to specified serial port with given baudrate.
                | disconnect_port - Disconnects currently active serial connection.
                | run_stream - Initiates compilation and trajectory streaming.
                | pause_stream - Pauses active trajectory streaming.
                | stop_stream - Halts active trajectory streaming.
                | append_log - Emits formatted log message to serial monitor console.
                | on_bytecode - Receives and renders compiled frame sequence.
    '''

    def connect_port(self, port: str, baud: int = 115200) -> bool:
        '''
            Connects to specified serial port with given baudrate.

            :param port: Serial device path string.
            :param baud: Communication baudrate.
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''

    def disconnect_port(self) -> None:
        '''
            Disconnects currently active serial connection.

            :exceptions: None.
        '''

    def run_stream(self) -> None:
        '''
            Initiates compilation and trajectory streaming.

            :exceptions: None.
        '''

    def pause_stream(self) -> None:
        '''
            Pauses active trajectory streaming.

            :exceptions: None.
        '''

    def stop_stream(self) -> None:
        '''
            Halts active trajectory streaming.

            :exceptions: None.
        '''

    def append_log(self, message: str) -> None:
        '''
            Emits formatted log message to serial monitor console.

            :param message: Log message string.
            :exceptions: None.
        '''

    def on_bytecode(self, frames: Sequence[MyCobotFrame]) -> None:
        '''
            Receives and renders compiled frame sequence.

            :param frames: Compiled robot command frames.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns event handler protocol version string.

            :return: Component version string.
        '''
