# -*- coding: UTF-8 -*-

'''
Module
    connection_panel.py
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
    Defines ConnectionPanel widget for serial connection controls.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import Frame, Label, StringVar
from tkinter.ttk import Button, Combobox

from idecobot.infrastructure.communication.iserial_port_scanner import ISerialPortScanner
from idecobot.infrastructure.gui.stream.connection_constants import ConnectionConstants
from idecobot.infrastructure.communication.iserial_port_scanner import ISerialPortScanner
from idecobot.infrastructure.gui.stream.connection_constants import ConnectionConstants
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionPanel:
    '''
        GUI panel for discovering, selecting, and toggling serial port connection.

        It defines:

            :attributes:
                | frame - The container Frame widget.
                | scanner - Injected ISerialPortScanner implementation.
                | on_connect - Callback invoked on connection attempt.
                | on_disconnect - Callback invoked on disconnection.
                | _palette - Injected ColorPalette color tokens.
                | _constants - Injected ConnectionConstants configuration.
                | _connected - Boolean flag indicating active serial link.
                | _port_var - Tracking StringVar for selected port.
                | _baud_var - Tracking StringVar for selected baudrate.
                | _port_combo - Injected Combobox for serial port selection.
                | _baud_combo - Injected Combobox for baudrate selection.
                | _conn_btn - Injected Button toggling connection.
                | _status_label - Injected Label displaying connection state.
            :methods:
                | __init__ - Initializes the port connection panel with injected widgets.
                | refresh_ports - Scans system serial ports and updates combobox.
                | get_selected_port - Returns the currently selected port string.
                | get_selected_baudrate - Returns the currently selected baudrate integer.
                | set_connected - Updates the visual connection state and toggle button.
                | set_port - Programmatically selects a specific serial port.
                | toggle_connection - Event handler for Connect / Disconnect button.
                | is_connected - Property indicating active connection state.
                | constants - Property returning injected ConnectionConstants.
    '''

    frame: Frame
    scanner: ISerialPortScanner
    on_connect: Callable[[str, int], bool]
    on_disconnect: Callable[[], None]
    _palette: ColorPalette
    _constants: ConnectionConstants
    _connected: bool
    _port_var: StringVar
    _baud_var: StringVar
    _port_combo: Combobox
    _baud_combo: Combobox
    _conn_btn: Button
    _status_label: Label

    def __init__(
        self,
        frame: Frame,
        scanner: ISerialPortScanner,
        on_connect: Callable[[str, int], bool],
        on_disconnect: Callable[[], None],
        port_var: StringVar,
        baud_var: StringVar,
        port_combo: Combobox,
        baud_combo: Combobox,
        conn_btn: Button,
        status_label: Label,
        palette: ColorPalette,
        constants: ConnectionConstants
    ) -> None:
        '''
            Initializes the port connection panel with injected widgets and dependencies.

            :param frame: Injected container Frame widget.
            :param scanner: Injected serial port scanner interface.
            :param on_connect: Callback returning True on successful connection.
            :param on_disconnect: Callback invoked when disconnected.
            :param port_var: Injected StringVar tracking selected port.
            :param baud_var: Injected StringVar tracking selected baudrate.
            :param port_combo: Injected Combobox for port selection.
            :param baud_combo: Injected Combobox for baudrate selection.
            :param conn_btn: Injected Button toggling connection.
            :param status_label: Injected Label displaying connection status.
            :param palette: Injected ColorPalette color tokens.
            :param constants: Injected ConnectionConstants configuration.
            :exceptions: None.
        '''
        self.frame = frame
        self.scanner = scanner
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self._port_var = port_var
        self._baud_var = baud_var
        self._port_combo = port_combo
        self._baud_combo = baud_combo
        self._conn_btn = conn_btn
        self._status_label = status_label
        self._palette = palette
        self._constants = constants
        self._connected = False

    def refresh_ports(self) -> None:
        '''
            Scans system serial ports and updates the combobox.

            :exceptions: None.
        '''
        ports: list[str] = list(self.scanner.scan_ports())
        self._port_combo['values'] = ports

        if ports and not self._port_var.get():
            self._port_var.set(ports[0])

    def get_selected_port(self) -> str:
        '''
            Returns the currently selected port string.

            :return: Port path string.
            :exceptions: None.
        '''
        return self._port_var.get().strip()

    def get_selected_baudrate(self) -> int:
        '''
            Returns the currently selected baudrate integer.

            :return: Baudrate value.
            :exceptions: None.
        '''
        try:
            return int(self._baud_var.get())

        except ValueError:
            return int(self._constants.default_baudrate)

    def set_connected(self, connected: bool) -> None:
        '''
            Updates the visual connection state and toggle button.

            :param connected: True if connection is active, False otherwise.
            :exceptions: None.
        '''
        self._connected = connected

        if connected:
            self._conn_btn.config(
                text=self._constants.disconnect_text,
                style=self._constants.style_danger_button
            )
            self._status_label.config(
                text=self._constants.status_connected_text,
                fg=self._palette.status_connected
            )
            self._port_combo.config(state=self._constants.state_disabled)
            self._baud_combo.config(state=self._constants.state_disabled)
        else:
            self._conn_btn.config(
                text=self._constants.connect_text,
                style=self._constants.style_accent_button
            )
            self._status_label.config(
                text=self._constants.status_disconnected_text,
                fg=self._palette.status_disconnected
            )
            self._port_combo.config(state=self._constants.state_normal)
            self._baud_combo.config(state=self._constants.state_readonly)

    def set_port(self, port: str) -> None:
        '''
            Programmatically selects a specific serial port.

            :param port: Serial port descriptor string.
            :exceptions: None.
        '''
        self._port_var.set(port)

    def toggle_connection(self) -> None:
        '''
            Event handler for Connect / Disconnect button.

            :exceptions: None.
        '''
        if self._connected:
            self.on_disconnect()
            self.set_connected(False)
        else:
            port: str = self.get_selected_port()
            baud: int = self.get_selected_baudrate()

            if port:
                success: bool = self.on_connect(port, baud)
                self.set_connected(success)

    @property
    def is_connected(self) -> bool:
        '''
            Returns boolean indicating active serial link state.

            :return: True if connected, False otherwise.
        '''
        return self._connected

    @property
    def constants(self) -> ConnectionConstants:
        '''
            Returns injected ConnectionConstants.

            :return: ConnectionConstants instance.
        '''
        return self._constants
