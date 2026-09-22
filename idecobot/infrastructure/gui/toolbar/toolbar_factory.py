# -*- coding: UTF-8 -*-

'''
Module
    toolbar_factory.py
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
    Defines ToolbarFactory responsible for assembling Toolbar controls.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import Frame, LEFT, Tk, TOP, VERTICAL, X, Y
from tkinter.ttk import Button, Separator

from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.toolbar.toolbar import Toolbar
from idecobot.infrastructure.gui.toolbar.toolbar_constants import ToolbarConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarFactory:
    '''
        Factory class assembling Toolbar composite view and wiring quick-action buttons.

        It defines:

            :methods:
                | create_toolbar - Constructs container frame, buttons, separators, and Toolbar.
    '''

    @classmethod
    def create_toolbar(
        cls,
        parent: Frame | Tk,
        on_run: Callable[[], None],
        on_pause: Callable[[], None],
        on_stop: Callable[[], None],
        on_home: Callable[[], None],
        on_relax: Callable[[], None],
        on_clear_log: Callable[[], None],
        palette: ColorPalette,
        constants: ToolbarConstants
    ) -> Toolbar:
        '''
            Constructs and wires the Toolbar quick-action buttons and separators.

            :param parent: Parent Tkinter Frame or Tk container.
            :param on_run: Callback triggering script streaming.
            :param on_pause: Callback pausing active streaming.
            :param on_stop: Callback stopping active streaming.
            :param on_home: Callback homing arm.
            :param on_relax: Callback releasing arm servos.
            :param on_clear_log: Callback clearing log console.
            :param palette: Injected ColorPalette color tokens.
            :param constants: Injected ToolbarConstants configuration.
            :return: Fully assembled Toolbar instance.
            :exceptions: None.
        '''
        frame: Frame = Frame(
            parent,
            bg=palette.bg_card,
            padx=constants.frame_padx,
            pady=constants.frame_pady
        )
        frame.pack(fill=X, side=TOP)

        btn_run: Button = Button(
            frame,
            text=constants.text_stream,
            style=constants.style_run_btn,
            command=on_run
        )
        btn_run.pack(side=LEFT, padx=constants.btn_padx)

        btn_pause: Button = Button(
            frame,
            text=constants.text_pause,
            command=on_pause
        )
        btn_pause.pack(side=LEFT, padx=constants.btn_padx)

        btn_stop: Button = Button(
            frame,
            text=constants.text_stop,
            style=constants.style_stop_btn,
            command=on_stop
        )
        btn_stop.pack(side=LEFT, padx=constants.btn_padx)

        sep1: Separator = Separator(frame, orient=VERTICAL)
        sep1.pack(side=LEFT, fill=Y, padx=constants.sep_padx, pady=constants.sep_pady)

        btn_home: Button = Button(
            frame,
            text=constants.text_home,
            style=constants.style_home_btn,
            command=on_home
        )
        btn_home.pack(side=LEFT, padx=constants.btn_padx)

        btn_relax: Button = Button(
            frame,
            text=constants.text_relax,
            command=on_relax
        )
        btn_relax.pack(side=LEFT, padx=constants.btn_padx)

        sep2: Separator = Separator(frame, orient=VERTICAL)
        sep2.pack(side=LEFT, fill=Y, padx=constants.sep_padx, pady=constants.sep_pady)

        btn_clear_log: Button = Button(
            frame,
            text=constants.text_clear_log,
            command=on_clear_log
        )
        btn_clear_log.pack(side=LEFT, padx=constants.btn_padx)

        return Toolbar(
            frame=frame,
            btn_run=btn_run,
            btn_pause=btn_pause,
            btn_stop=btn_stop,
            btn_home=btn_home,
            btn_relax=btn_relax,
            btn_clear_log=btn_clear_log,
            constants=constants
        )
