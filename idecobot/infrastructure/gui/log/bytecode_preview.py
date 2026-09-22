# -*- coding: UTF-8 -*-

'''
Module
    bytecode_preview.py
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
    Defines BytecodePreview widget displaying compiled binary frame sequences.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import BOTH, END, RIGHT, Y, Frame, Scrollbar, Text

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.infrastructure.communication.protocol.iprotocol_framer import IProtocolFramer
from idecobot.infrastructure.gui.log.bytecode_constants import BytecodeConstants
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


class BytecodePreview:
    '''
        Read-only hex frame inspector rendering compiled protocol payloads.

        It defines:

            :attributes:
                | _palette - Injected ColorPalette color tokens.
                | _fonts - Injected FontConfig typography tokens.
                | _constants - Injected BytecodeConstants configuration.
                | _framer - Injected IProtocolFramer protocol encoder.
                | _frame - Container Frame widget.
                | _text - Read-only Text display area.
            :methods:
                | __init__ - Initializes bytecode preview layout.
                | get_frame - Returns container Frame.
                | set_frames - Renders compiled frame sequence into formatted hex table.
                | clear - Clears hex preview area.
                | get_version - Returns preview component version.
                | constants - Property returning injected BytecodeConstants.
    '''

    _palette: ColorPalette
    _fonts: FontConfig
    _constants: BytecodeConstants
    _framer: IProtocolFramer
    _frame: Frame
    _text: Text

    def __init__(
        self,
        parent: Frame,
        palette: ColorPalette,
        fonts: FontConfig,
        constants: BytecodeConstants,
        framer: IProtocolFramer
    ) -> None:
        '''
            Initializes preview text area with injected constants and framer.

            :param parent: Parent Frame widget.
            :param palette: Injected ColorPalette color design tokens.
            :param fonts: Injected FontConfig typography tokens.
            :param constants: Injected BytecodeConstants configuration.
            :param framer: Injected IProtocolFramer protocol encoder.
            :exceptions: None.
        '''
        self._palette = palette
        self._fonts = fonts
        self._constants = constants
        self._framer = framer

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

    def get_frame(self) -> Frame:
        '''
            Returns container Frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def set_frames(self, frames: Sequence[MyCobotFrame]) -> None:
        '''
            Renders compiled frame sequence into formatted hex table.

            :param frames: Sequence of compiled MyCobotFrame instances.
            :exceptions: None.
        '''
        self._text.config(state=self._constants.state_normal)
        self._text.delete(self._constants.index_start, END)
        divider: str = self._constants.divider_char * self._constants.divider_length + '\n'
        self._text.insert(END, self._constants.header_template)
        self._text.insert(END, divider)

        for idx, frame in enumerate(frames):
            step_num: int = idx + 1
            cmd_hex: str = f'0x{frame.cmd_id:02X}'
            frame_hex: str = self._framer.format_hex(frame)
            delay_str: str = f'{frame.delay_after_sec:.2f}s'
            line: str = (
                f'{step_num:<{self._constants.col_step_width}} '
                f'{cmd_hex:<{self._constants.col_cmd_width}} '
                f'{frame_hex:<{self._constants.col_hex_width}} '
                f'{delay_str}\n'
            )
            self._text.insert(END, line)

        self._text.config(state=self._constants.state_disabled)

    def clear(self) -> None:
        '''
            Clears hex preview area.

            :exceptions: None.
        '''
        self._text.config(state=self._constants.state_normal)
        self._text.delete(self._constants.index_start, END)
        self._text.config(state=self._constants.state_disabled)

    def get_version(self) -> str:
        '''
            Returns component implementation version.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

    @property
    def constants(self) -> BytecodeConstants:
        '''
            Returns injected BytecodeConstants.

            :return: BytecodeConstants instance.
        '''
        return self._constants
