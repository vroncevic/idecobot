# -*- coding: UTF-8 -*-

'''
Module
    color_palette.py
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
    Defines ColorPalette dataclass holding design token hex colors for idecobot UI.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ColorPalette:
    '''
        Immutable design tokens holding color hex codes for the user interface.

        It defines:

            :attributes:
                | bg_dark - Deep dark background (main window / outer frames).
                | bg_card - Card / container background.
                | bg_canvas - High contrast canvas / terminal background.
                | bg_header - Header panel background.
                | fg_text - Primary body text color.
                | fg_muted - Muted / secondary label text color.
                | fg_light - Light label / highlight text color.
                | fg_white - Pure white text color.
                | accent_blue - Primary action / selection blue.
                | accent_green - Success / connected green.
                | accent_red - Danger / disconnected red.
                | accent_yellow - Warning yellow.
                | accent_cyan - Secondary cyan highlight.
                | border - Panel border / separator line color.
                | status_connected - Connection indicator active color.
                | status_disconnected - Connection indicator inactive color.
                | btn_bg - Normal button background color.
                | btn_pressed - Pressed button background color.
                | btn_active - Hover/active button background color.
                | btn_disabled - Disabled button background color.
                | btn_fg_disabled - Disabled button foreground color.
                | tab_inactive - Inactive notebook tab background.
    '''

    bg_dark: str = '#1e2227'
    bg_card: str = '#282c34'
    bg_canvas: str = '#181a1f'
    bg_header: str = '#252526'
    fg_text: str = '#abb2bf'
    fg_muted: str = '#858585'
    fg_light: str = '#CCCCCC'
    fg_white: str = '#ffffff'
    accent_blue: str = '#61afef'
    accent_green: str = '#98c379'
    accent_red: str = '#e06c75'
    accent_yellow: str = '#e5c07b'
    accent_cyan: str = '#56b6c2'
    border: str = '#333842'
    status_connected: str = '#89D185'
    status_disconnected: str = '#F48771'
    btn_bg: str = '#2c313a'
    btn_pressed: str = '#21252b'
    btn_active: str = '#3e4451'
    btn_disabled: str = '#1e2227'
    btn_fg_disabled: str = '#5c6370'
    tab_inactive: str = '#21252b'
