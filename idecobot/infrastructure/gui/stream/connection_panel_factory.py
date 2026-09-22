# -*- coding: UTF-8 -*-

'''
Module
    connection_panel_factory.py
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
    Defines ConnectionPanelFactory responsible for assembling ConnectionPanel.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import Frame, Label, LEFT, StringVar
from tkinter.ttk import Button, Combobox

from idecobot.infrastructure.communication.iserial_port_scanner import ISerialPortScanner
from idecobot.infrastructure.gui.stream.connection_constants import ConnectionConstants
from idecobot.infrastructure.gui.stream.connection_panel import ConnectionPanel
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


class ConnectionPanelFactory:
    '''
        Factory class assembling ConnectionPanel composite view and wiring port controls.

        It defines:

            :methods:
                | create_connection_panel - Constructs container frame, widgets, and ConnectionPanel.
    '''

    @classmethod
    def create_connection_panel(
        cls,
        parent: Frame,
        scanner: ISerialPortScanner,
        on_connect: Callable[[str, int], bool],
        on_disconnect: Callable[[], None],
        palette: ColorPalette,
        fonts: FontConfig,
        constants: ConnectionConstants
    ) -> ConnectionPanel:
        '''
            Constructs and wires the ConnectionPanel composite view with all child widgets.

            :param parent: Parent container Frame.
            :param scanner: Injected serial port scanner interface.
            :param on_connect: Callback returning True on successful connection.
            :param on_disconnect: Callback invoked on disconnection.
            :param palette: Injected ColorPalette design tokens.
            :param fonts: Injected FontConfig typography tokens.
            :param constants: Injected ConnectionConstants configuration.
            :return: Fully assembled ConnectionPanel instance.
            :exceptions: None.
        '''
        frame: Frame = Frame(
            parent,
            bg=palette.bg_header,
            padx=constants.frame_padx,
            pady=constants.frame_pady
        )

        title_label: Label = Label(
            frame,
            text=constants.title_text,
            bg=palette.bg_header,
            fg=palette.fg_muted,
            font=fonts.title
        )
        title_label.pack(side=LEFT, padx=constants.title_padx)

        port_label: Label = Label(
            frame,
            text=constants.port_label_text,
            bg=palette.bg_header,
            fg=palette.fg_light,
            font=fonts.body
        )
        port_label.pack(side=LEFT, padx=constants.label_padx)

        port_var: StringVar = StringVar()
        port_combo: Combobox = Combobox(
            frame,
            textvariable=port_var,
            width=constants.port_width,
            state=constants.state_normal
        )
        port_combo.pack(side=LEFT, padx=constants.port_padx)

        refresh_btn: Button = Button(
            frame,
            text=constants.refresh_symbol,
            width=constants.refresh_width,
            style=constants.style_button
        )
        refresh_btn.pack(side=LEFT, padx=constants.refresh_padx)

        baud_label: Label = Label(
            frame,
            text=constants.baud_label_text,
            bg=palette.bg_header,
            fg=palette.fg_light,
            font=fonts.body
        )
        baud_label.pack(side=LEFT, padx=constants.label_padx)

        baud_var: StringVar = StringVar(value=constants.default_baudrate)
        baud_combo: Combobox = Combobox(
            frame,
            textvariable=baud_var,
            values=list(constants.baudrates),
            width=constants.baud_width,
            state=constants.state_readonly
        )
        baud_combo.pack(side=LEFT, padx=constants.baud_padx)

        conn_btn: Button = Button(
            frame,
            text=constants.connect_text,
            width=constants.connect_width,
            style=constants.style_accent_button
        )
        conn_btn.pack(side=LEFT, padx=constants.connect_padx)

        status_label: Label = Label(
            frame,
            text=constants.status_disconnected_text,
            bg=palette.bg_header,
            fg=palette.status_disconnected,
            font=fonts.status_bold
        )
        status_label.pack(side=LEFT, padx=constants.status_padx)

        panel: ConnectionPanel = ConnectionPanel(
            frame=frame,
            scanner=scanner,
            on_connect=on_connect,
            on_disconnect=on_disconnect,
            port_var=port_var,
            baud_var=baud_var,
            port_combo=port_combo,
            baud_combo=baud_combo,
            conn_btn=conn_btn,
            status_label=status_label,
            palette=palette,
            constants=constants
        )

        refresh_btn.config(command=panel.refresh_ports)
        conn_btn.config(command=panel.toggle_connection)
        panel.refresh_ports()

        return panel
