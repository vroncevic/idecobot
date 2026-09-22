# -*- coding: UTF-8 -*-

'''
Module
    connection_constants.py
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
    Defines ConnectionConstants frozen dataclass for ConnectionPanel widget.
'''

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class ConnectionConstants:
    '''
        Constants for serial port connection panel styles, layout, presets, and widget states.

        It defines:

            :attributes:
                | port_width - Text column width of the port combobox.
                | baud_width - Text column width of the baudrate combobox.
                | refresh_width - Text character width of the refresh button.
                | connect_width - Text character width of the connect/disconnect button.
                | frame_padx - Horizontal padding of the header frame.
                | frame_pady - Vertical padding of the header frame.
                | title_padx - Horizontal padding tuple for section title label.
                | label_padx - Horizontal padding tuple for descriptor labels.
                | port_padx - Horizontal padding tuple for port combobox.
                | refresh_padx - Horizontal padding tuple for refresh button.
                | baud_padx - Horizontal padding tuple for baudrate combobox.
                | connect_padx - Horizontal padding tuple for connect toggle button.
                | status_padx - Horizontal padding tuple for connection status indicator.
                | default_baudrate - Baseline transmission baudrate string.
                | baudrates - Tuple of available transmission baudrate presets.
                | title_text - Section title label string.
                | port_label_text - Port label text string.
                | baud_label_text - Baudrate label text string.
                | refresh_symbol - Unicode glyph for refresh button.
                | connect_text - Text for connect action button.
                | disconnect_text - Text for disconnect action button.
                | status_connected_text - Text indicator for connected state.
                | status_disconnected_text - Text indicator for disconnected state.
                | state_normal - Tkinter normal widget state string.
                | state_readonly - Tkinter readonly widget state string.
                | state_disabled - Tkinter disabled widget state string.
                | style_button - Standard Ttk button style identifier.
                | style_accent_button - Accent Ttk button style identifier.
                | style_danger_button - Danger Ttk button style identifier.
    '''

    port_width: int = 16
    baud_width: int = 8
    refresh_width: int = 3
    connect_width: int = 10
    frame_padx: int = 6
    frame_pady: int = 4
    title_padx: tuple[int, int] = (0, 6)
    label_padx: tuple[int, int] = (2, 2)
    port_padx: tuple[int, int] = (0, 4)
    refresh_padx: tuple[int, int] = (0, 6)
    baud_padx: tuple[int, int] = (0, 6)
    connect_padx: tuple[int, int] = (0, 6)
    status_padx: tuple[int, int] = (2, 0)
    default_baudrate: str = '115200'
    baudrates: tuple[str, ...] = ('9600', '19200', '57600', '115200', '1000000')
    title_text: str = 'COMMUNICATION:'
    port_label_text: str = 'Port:'
    baud_label_text: str = 'Baud:'
    refresh_symbol: str = '⟳'
    connect_text: str = 'Connect'
    disconnect_text: str = 'Disconnect'
    status_connected_text: str = '● Connected'
    status_disconnected_text: str = '● Disconnected'
    state_normal: Literal['normal'] = 'normal'
    state_readonly: Literal['readonly'] = 'readonly'
    state_disabled: Literal['disabled'] = 'disabled'
    style_button: str = 'TButton'
    style_accent_button: str = 'Accent.TButton'
    style_danger_button: str = 'Danger.TButton'
