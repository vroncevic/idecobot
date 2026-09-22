# -*- coding: UTF-8 -*-

'''
Module
    serial_console.py
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
    Defines SerialConsole widget rendering timestamped colored serial activity.
'''

from __future__ import annotations

from datetime import datetime
from tkinter import BOTH, END, RIGHT, Y, Frame, Scrollbar, Text

from idecobot.infrastructure.gui.log.console_constants import ConsoleConstants
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.theme.font_config import FontConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialConsole:
    '''
        Timestamped serial monitor console with color-coded TX, RX, and error lines.

        It defines:

            :attributes:
                | _palette - Injected ColorPalette design tokens.
                | _fonts - Injected FontConfig typography tokens.
                | _constants - Injected ConsoleConstants configuration.
                | _frame - Container Frame widget.
                | _text - Primary scrolling Text log area.
            :methods:
                | __init__ - Initializes console with color tags and scrollbar.
                | get_frame - Returns container Frame.
                | append_log - Appends timestamped line with status styling.
                | clear - Clears all console lines.
                | constants - Property returning injected ConsoleConstants.
    '''

    _palette: ColorPalette
    _fonts: FontConfig
    _constants: ConsoleConstants
    _frame: Frame
    _text: Text

    def __init__(
        self,
        parent: Frame,
        palette: ColorPalette,
        fonts: FontConfig,
        constants: ConsoleConstants
    ) -> None:
        '''
            Initializes console with color tags, scrollbar, and injected constants.

            :param parent: Parent Frame widget.
            :param palette: Injected ColorPalette color design tokens.
            :param fonts: Injected FontConfig typography tokens.
            :param constants: Injected ConsoleConstants configuration.
            :exceptions: None.
        '''
        self._palette = palette
        self._fonts = fonts
        self._constants = constants

        self._frame = Frame(parent, bg=self._palette.bg_canvas)
        self._frame.pack(fill=BOTH, expand=True)

        scrollbar: Scrollbar = Scrollbar(self._frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self._text = Text(
            self._frame,
            bg=self._palette.bg_canvas,
            fg=self._palette.fg_text,
            border=self._constants.border_width,
            padx=self._constants.pad_text_x,
            pady=self._constants.pad_text_y,
            font=self._fonts.status,
            yscrollcommand=scrollbar.set,
            state=self._constants.state_disabled,
            wrap=self._constants.wrap_none
        )
        self._text.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self._text.yview)

        self._text.tag_configure(
            self._constants.tag_time,
            foreground=self._palette.fg_muted
        )
        self._text.tag_configure(
            self._constants.tag_tx,
            foreground=self._palette.accent_green,
            font=(
                self._fonts.family_mono,
                self._fonts.status[1],
                self._constants.font_weight_bold
            )
        )
        self._text.tag_configure(
            self._constants.tag_rx,
            foreground=self._palette.accent_blue,
            font=(
                self._fonts.family_mono,
                self._fonts.status[1],
                self._constants.font_weight_bold
            )
        )
        self._text.tag_configure(
            self._constants.tag_err,
            foreground=self._palette.accent_red,
            font=(
                self._fonts.family_mono,
                self._fonts.status[1],
                self._constants.font_weight_bold
            )
        )
        self._text.tag_configure(
            self._constants.tag_warn,
            foreground=self._palette.accent_yellow
        )
        self._text.tag_configure(
            self._constants.tag_info,
            foreground=self._palette.fg_text
        )

    def get_frame(self) -> Frame:
        '''
            Returns container Frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def append_log(self, message: str) -> None:
        '''
            Appends formatted message line with timestamp and color tag.

            :param message: Log message string.
            :exceptions: None.
        '''
        now_str: str = datetime.now().strftime(
            self._constants.time_format
        )[:self._constants.time_slice_end]

        match message:
            case msg if msg.startswith(self._constants.prefix_tx):
                tag: str = self._constants.tag_tx
            case msg if msg.startswith(self._constants.prefix_rx):
                tag: str = self._constants.tag_rx
            case msg if self._constants.keyword_err in msg:
                tag: str = self._constants.tag_err
            case msg if self._constants.keyword_warn in msg:
                tag: str = self._constants.tag_warn
            case _:
                tag: str = self._constants.tag_info

        self._text.config(state=self._constants.state_normal)
        self._text.insert(END, f'[{now_str}] ', self._constants.tag_time)
        self._text.insert(END, f'{message}\n', tag)
        self._text.see(END)
        self._text.config(state=self._constants.state_disabled)

    def clear(self) -> None:
        '''
            Clears all console output.

            :exceptions: None.
        '''
        self._text.config(state=self._constants.state_normal)
        self._text.delete(self._constants.index_start, END)
        self._text.config(state=self._constants.state_disabled)

    @property
    def constants(self) -> ConsoleConstants:
        '''
            Returns injected ConsoleConstants.

            :return: ConsoleConstants instance.
        '''
        return self._constants
