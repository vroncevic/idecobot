# -*- coding: UTF-8 -*-

'''
Module
    gui_event_handler.py
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
    Defines GUIEventHandler concrete event mediator dispatching user interactions.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GUIEventHandler:
    '''
        Event mediator and callback dispatcher for GUI user interactions.

        It defines:

            :attributes:
                | _target - Active callback delegate handling events.
            :methods:
                | __init__ - Initializes the GUI event handler.
                | set_target - Sets the active callback delegate.
                | connect_port - Dispatches port connection event.
                | disconnect_port - Dispatches port disconnection event.
                | run_stream - Dispatches trajectory streaming execution.
                | pause_stream - Dispatches trajectory streaming pause.
                | stop_stream - Dispatches trajectory streaming stop.
                | append_log - Dispatches formatted log emission.
                | on_bytecode - Dispatches compiled bytecode frame sequence.
    '''

    _target: object | None

    def __init__(self) -> None:
        '''
            Initializes the GUI event handler.

            :exceptions: None.
        '''
        self._target = None

    def set_target(self, target: object) -> None:
        '''
            Sets the active callback delegate.

            :param target: Active callback delegate handling events.
            :exceptions: None.
        '''
        self._target = target

    def connect_port(self, port: str, baud: int = 115200) -> bool:
        '''
            Dispatches port connection event.

            :param port: Serial device path string.
            :param baud: Communication baudrate.
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''
        if self._target is not None and hasattr(self._target, 'connect_port'):
            return bool(self._target.connect_port(port, baud))

        return False

    def disconnect_port(self) -> None:
        '''
            Dispatches port disconnection event.

            :exceptions: None.
        '''
        if self._target is not None and hasattr(self._target, 'disconnect_port'):
            self._target.disconnect_port()

    def run_stream(self) -> None:
        '''
            Dispatches trajectory streaming execution.

            :exceptions: None.
        '''
        if self._target is not None and hasattr(self._target, 'run_stream'):
            self._target.run_stream()

    def pause_stream(self) -> None:
        '''
            Dispatches trajectory streaming pause.

            :exceptions: None.
        '''
        if self._target is not None and hasattr(self._target, 'pause_stream'):
            self._target.pause_stream()

    def stop_stream(self) -> None:
        '''
            Dispatches trajectory streaming stop.

            :exceptions: None.
        '''
        if self._target is not None and hasattr(self._target, 'stop_stream'):
            self._target.stop_stream()

    def append_log(self, message: str) -> None:
        '''
            Dispatches formatted log emission.

            :param message: Log message string.
            :exceptions: None.
        '''
        if self._target is not None and hasattr(self._target, 'append_log'):
            self._target.append_log(message)

    def on_bytecode(self, frames: Sequence[MyCobotFrame]) -> None:
        '''
            Dispatches compiled bytecode frame sequence.

            :param frames: Compiled robot command frames.
            :exceptions: None.
        '''
        if self._target is not None and hasattr(self._target, 'on_bytecode'):
            self._target.on_bytecode(frames)
