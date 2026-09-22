# -*- coding: UTF-8 -*-

'''
Module
    log_panel.py
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
    Defines LogPanel bottom tabbed pane combining SerialConsole and BytecodePreview.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import Frame
from tkinter.ttk import Notebook

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.infrastructure.gui.log.bytecode_preview import BytecodePreview
from idecobot.infrastructure.gui.log.log_constants import LogConstants
from idecobot.infrastructure.gui.log.serial_console import SerialConsole

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LogPanel:
    '''
        Bottom pane containing tabbed views for serial communication logs and bytecode inspection.

        It defines:

            :attributes:
                | _frame - Injected outer container Frame widget.
                | _notebook - Injected tabbed notebook container widget.
                | _console - Injected SerialConsole instance.
                | _bytecode - Injected BytecodePreview instance.
                | _constants - Injected LogConstants configuration.
            :methods:
                | __init__ - Initializes LogPanel with injected collaborators.
                | get_frame - Returns container Frame.
                | append_log - Appends entry to serial console.
                | set_bytecode - Updates bytecode preview tab and selects it.
                | clear - Clears console and bytecode.
                | console - Property returning injected SerialConsole.
                | bytecode - Property returning injected BytecodePreview.
                | notebook - Property returning injected Notebook.
                | constants - Property returning injected LogConstants.
    '''

    _frame: Frame
    _notebook: Notebook
    _console: SerialConsole
    _bytecode: BytecodePreview
    _constants: LogConstants

    def __init__(
        self,
        frame: Frame,
        notebook: Notebook,
        console: SerialConsole,
        bytecode: BytecodePreview,
        constants: LogConstants
    ) -> None:
        '''
            Initializes bottom tabbed logging panel with strictly injected dependencies.

            :param frame: Injected outer container Frame widget.
            :param notebook: Injected Notebook widget.
            :param console: Injected SerialConsole instance.
            :param bytecode: Injected BytecodePreview instance.
            :param constants: Injected LogConstants configuration.
            :exceptions: None.
        '''
        self._frame = frame
        self._notebook = notebook
        self._console = console
        self._bytecode = bytecode
        self._constants = constants

    def get_frame(self) -> Frame:
        '''
            Returns container Frame.

            :return: Tkinter Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def append_log(self, message: str) -> None:
        '''
            Appends message to serial monitor console tab.

            :param message: Message line string.
            :exceptions: None.
        '''
        self._console.append_log(message)

    def set_bytecode(self, frames: Sequence[MyCobotFrame]) -> None:
        '''
            Updates bytecode preview tab with compiled frames and switches active tab.

            :param frames: Sequence of MyCobotFrame instances.
            :exceptions: None.
        '''
        self._bytecode.set_frames(frames)
        self._notebook.select(self._constants.tab_index_bytecode)

    def clear(self) -> None:
        '''
            Clears both console logs and bytecode preview.

            :exceptions: None.
        '''
        self._console.clear()
        self._bytecode.clear()

    @property
    def console(self) -> SerialConsole:
        '''
            Returns injected SerialConsole.

            :return: SerialConsole instance.
        '''
        return self._console

    @property
    def bytecode(self) -> BytecodePreview:
        '''
            Returns injected BytecodePreview.

            :return: BytecodePreview instance.
        '''
        return self._bytecode

    @property
    def notebook(self) -> Notebook:
        '''
            Returns injected Notebook.

            :return: Notebook instance.
        '''
        return self._notebook

    @property
    def constants(self) -> LogConstants:
        '''
            Returns injected LogConstants.

            :return: LogConstants instance.
        '''
        return self._constants
