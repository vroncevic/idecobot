# -*- coding: UTF-8 -*-

'''
Module
    log_panel_factory.py
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
    Defines LogPanelFactory responsible for assembling LogPanel and its tabs.
'''

from __future__ import annotations

from tkinter import BOTH, Frame
from tkinter.ttk import Notebook

from idecobot.infrastructure.communication.protocol.iprotocol_framer import IProtocolFramer
from idecobot.infrastructure.gui.log.bytecode_constants import BytecodeConstants
from idecobot.infrastructure.gui.log.bytecode_preview import BytecodePreview
from idecobot.infrastructure.gui.log.console_constants import ConsoleConstants
from idecobot.infrastructure.gui.log.log_constants import LogConstants
from idecobot.infrastructure.gui.log.log_panel import LogPanel
from idecobot.infrastructure.gui.log.serial_console import SerialConsole
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.theme.font_config import FontConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LogPanelFactory:
    '''
        Factory assembling LogPanel composite view, notebook tabs, and child consoles.

        It defines:

            :methods:
                | create_log_panel - Constructs frame, tabs, consoles, and LogPanel.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_log_panel(
        cls,
        parent: Frame,
        palette: ColorPalette,
        fonts: FontConfig,
        constants: LogConstants,
        console_constants: ConsoleConstants,
        bytecode_constants: BytecodeConstants,
        framer: IProtocolFramer
    ) -> LogPanel:
        '''
            Constructs and wires the LogPanel composite view with all child tabs.

            :param parent: Parent container Frame.
            :param palette: Injected ColorPalette color design tokens.
            :param fonts: Injected FontConfig typography tokens.
            :param constants: Injected LogConstants configuration.
            :param console_constants: Injected ConsoleConstants configuration.
            :param bytecode_constants: Injected BytecodeConstants configuration.
            :param framer: Injected IProtocolFramer protocol encoder.
            :return: Fully assembled LogPanel instance.
            :exceptions: None.
        '''
        frame: Frame = Frame(
            parent,
            bg=palette.bg_dark,
            padx=constants.pad_frame_x,
            pady=constants.pad_frame_y
        )
        frame.pack(fill=BOTH, expand=True)

        notebook: Notebook = Notebook(frame)
        notebook.pack(fill=BOTH, expand=True)

        tab_console: Frame = Frame(notebook, bg=palette.bg_canvas)
        console: SerialConsole = SerialConsole(
            tab_console,
            palette,
            fonts,
            constants=console_constants
        )
        notebook.add(tab_console, text=constants.tab_serial)

        tab_bytecode: Frame = Frame(notebook, bg=palette.bg_canvas)
        bytecode: BytecodePreview = BytecodePreview(
            tab_bytecode,
            palette,
            fonts,
            constants=bytecode_constants,
            framer=framer
        )
        notebook.add(tab_bytecode, text=constants.tab_bytecode)

        return LogPanel(
            frame=frame,
            notebook=notebook,
            console=console,
            bytecode=bytecode,
            constants=constants
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
