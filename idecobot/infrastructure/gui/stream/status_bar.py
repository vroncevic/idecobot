# -*- coding: UTF-8 -*-

'''
Module
    status_bar.py
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
    Defines StatusBar widget for runtime execution telemetry and progress reporting.
'''

from __future__ import annotations

from tkinter import Frame, HORIZONTAL, Label, LEFT, RIGHT
from tkinter.ttk import Progressbar

from idecobot.core.model.communication.stream_progress import StreamProgress
from idecobot.core.model.communication.stream_state import StreamState
from idecobot.infrastructure.gui.stream.status_bar_constants import StatusBarConstants
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.theme.font_config import FontConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StatusBar:
    '''
        Bottom telemetry status bar displaying streamer state, progress bar, and step details.

        It defines:

            :attributes:
                | _palette - Injected ColorPalette design tokens.
                | _fonts - Injected FontConfig typography tokens.
                | _constants - Injected StatusBarConstants configuration.
                | frame - The container Frame widget.
            :methods:
                | __init__ - Initializes the streaming status bar.
                | update_progress - Updates the telemetry widgets with new StreamProgress data.
                | set_message - Displays a general status message.
                | reset - Resets status bar to default idle state.
                | constants - Property returning injected StatusBarConstants.
    '''

    _palette: ColorPalette
    _fonts: FontConfig
    _constants: StatusBarConstants
    frame: Frame
    _state_label: Label
    _step_label: Label
    _cmd_label: Label
    _msg_label: Label
    _progressbar: Progressbar

    def __init__(
        self,
        parent: Frame,
        palette: ColorPalette,
        fonts: FontConfig,
        constants: StatusBarConstants
    ) -> None:
        '''
            Initializes the streaming status bar.

            :param parent: Parent Tkinter Frame.
            :param palette: Injected ColorPalette color design tokens.
            :param fonts: Injected FontConfig typography tokens.
            :param constants: Injected StatusBarConstants configuration.
            :exceptions: None.
        '''
        self._palette = palette
        self._fonts = fonts
        self._constants = constants

        self.frame = Frame(parent, bg=self._constants.bg_idle, height=self._constants.height)
        self.frame.pack_propagate(False)

        self._state_label = Label(
            self.frame,
            text=self._constants.text_ready,
            bg=self._constants.bg_idle,
            fg=self._constants.fg_text,
            font=self._constants.font_state,
            padx=self._constants.pad_state_x
        )
        self._state_label.pack(side=LEFT)

        self._step_label = Label(
            self.frame,
            text=self._constants.text_default_step,
            bg=self._constants.bg_idle,
            fg=self._constants.fg_secondary,
            font=self._constants.font_text,
            padx=self._constants.pad_text_x
        )
        self._step_label.pack(side=LEFT)

        self._cmd_label = Label(
            self.frame,
            text=self._constants.text_default_cmd,
            bg=self._constants.bg_idle,
            fg=self._constants.fg_secondary,
            font=self._constants.font_text,
            padx=self._constants.pad_text_x
        )
        self._cmd_label.pack(side=LEFT)

        self._msg_label = Label(
            self.frame,
            text=self._constants.text_empty,
            bg=self._constants.bg_idle,
            fg=self._constants.fg_secondary,
            font=self._constants.font_text,
            padx=self._constants.pad_text_x
        )
        self._msg_label.pack(side=LEFT)

        self._progressbar = Progressbar(
            self.frame,
            orient=HORIZONTAL,
            mode=self._constants.mode_determinate,
            length=self._constants.progressbar_length
        )
        self._progressbar.pack(
            side=RIGHT,
            padx=self._constants.pad_progress_x,
            pady=self._constants.pad_progress_y
        )

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Updates the telemetry widgets with new StreamProgress data.

            :param progress: The current streaming progress telemetry.
            :exceptions: None.
        '''
        state_str: str = progress.state.name
        self._state_label.config(text=state_str)

        if progress.state == StreamState.STREAMING:
            self._state_label.config(bg=self._constants.bg_streaming)
            self.frame.config(bg=self._constants.bg_streaming)
        elif progress.state == StreamState.PAUSED:
            self._state_label.config(bg=self._constants.bg_paused)
            self.frame.config(bg=self._constants.bg_paused)
        elif progress.state == StreamState.ERROR:
            self._state_label.config(bg=self._constants.bg_error)
            self.frame.config(bg=self._constants.bg_error)
        else:
            self._state_label.config(bg=self._constants.bg_idle)
            self.frame.config(bg=self._constants.bg_idle)

        self._step_label.config(text=f'Step: {progress.current_step}/{progress.total_steps}')
        self._cmd_label.config(text=f'Command: {progress.command_name or "-"}')
        self._progressbar['value'] = progress.progress_percent

    def set_message(self, message: str) -> None:
        '''
            Displays a general status message.

            :param message: Status message string.
            :exceptions: None.
        '''
        self._msg_label.config(text=message)

    def reset(self) -> None:
        '''
            Resets status bar to default idle state.

            :exceptions: None.
        '''
        self.frame.config(bg=self._constants.bg_idle)
        self._state_label.config(text=self._constants.text_ready, bg=self._constants.bg_idle)
        self._step_label.config(text=self._constants.text_default_step)
        self._cmd_label.config(text=self._constants.text_default_cmd)
        self._msg_label.config(text=self._constants.text_empty)
        self._progressbar['value'] = self._constants.default_progress_val

    @property
    def constants(self) -> StatusBarConstants:
        '''
            Returns injected StatusBarConstants.

            :return: StatusBarConstants instance.
        '''
        return self._constants
