# -*- coding: UTF-8 -*-

'''
Module
    toolbar.py
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
    Defines Toolbar widget implementing quick-action controls.
'''

from __future__ import annotations

from tkinter import Frame
from tkinter.ttk import Button

from idecobot.core.model.communication.stream_state import StreamState
from idecobot.infrastructure.gui.toolbar.toolbar_constants import ToolbarConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Toolbar:
    '''
        Quick-action execution toolbar providing Run, Pause, Stop, Home, and Relax controls.

        It defines:

            :attributes:
                | _frame - Injected container Frame widget.
                | _btn_run - Injected Run stream button.
                | _btn_pause - Injected Pause stream button.
                | _btn_stop - Injected Stop stream button.
                | _btn_home - Injected Home manipulator button.
                | _btn_relax - Injected Relax servos button.
                | _btn_clear_log - Injected Clear log button.
                | _constants - Injected ToolbarConstants configuration.
            :methods:
                | __init__ - Initializes toolbar buttons and callbacks.
                | get_frame - Returns container Frame.
                | update_stream_state - Updates button enabled/disabled states.
                | set_connected - Updates controls based on connection state.
                | constants - Property returning injected ToolbarConstants.
    '''

    _frame: Frame
    _btn_run: Button
    _btn_pause: Button
    _btn_stop: Button
    _btn_home: Button
    _btn_relax: Button
    _btn_clear_log: Button
    _constants: ToolbarConstants

    def __init__(
        self,
        frame: Frame,
        btn_run: Button,
        btn_pause: Button,
        btn_stop: Button,
        btn_home: Button,
        btn_relax: Button,
        btn_clear_log: Button,
        constants: ToolbarConstants
    ) -> None:
        '''
            Initializes toolbar with injected buttons and constants.

            :param frame: Container Tkinter Frame.
            :param btn_run: Injected Run stream button.
            :param btn_pause: Injected Pause stream button.
            :param btn_stop: Injected Stop stream button.
            :param btn_home: Injected Home manipulator button.
            :param btn_relax: Injected Relax servos button.
            :param btn_clear_log: Injected Clear log button.
            :param constants: Injected ToolbarConstants configuration.
            :exceptions: None.
        '''
        self._frame = frame
        self._btn_run = btn_run
        self._btn_pause = btn_pause
        self._btn_stop = btn_stop
        self._btn_home = btn_home
        self._btn_relax = btn_relax
        self._btn_clear_log = btn_clear_log
        self._constants = constants

    def get_frame(self) -> Frame:
        '''
            Returns the container frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def update_stream_state(self, state: StreamState) -> None:
        '''
            Updates button states according to active streaming lifecycle.

            :param state: Active StreamState.
            :exceptions: None.
        '''
        match state:
            case StreamState.STREAMING:
                self._btn_run.state([self._constants.state_disabled])
                self._btn_pause.state([self._constants.state_enabled])
                self._btn_stop.state([self._constants.state_enabled])
            case StreamState.PAUSED:
                self._btn_run.state([self._constants.state_disabled])
                self._btn_pause.state([self._constants.state_enabled])
                self._btn_stop.state([self._constants.state_enabled])
            case _:
                self._btn_run.state([self._constants.state_enabled])
                self._btn_pause.state([self._constants.state_disabled])
                self._btn_stop.state([self._constants.state_disabled])

    def set_connected(self, connected: bool) -> None:
        '''
            Updates controls based on connection state.

            :param connected: True if connected, False otherwise.
            :exceptions: None.
        '''
        if connected:
            self._btn_run.state([self._constants.state_enabled])
            self._btn_home.state([self._constants.state_enabled])
            self._btn_relax.state([self._constants.state_enabled])
        else:
            self._btn_run.state([self._constants.state_disabled])
            self._btn_pause.state([self._constants.state_disabled])
            self._btn_stop.state([self._constants.state_disabled])

    @property
    def constants(self) -> ToolbarConstants:
        '''
            Returns injected ToolbarConstants.

            :return: ToolbarConstants instance.
        '''
        return self._constants
