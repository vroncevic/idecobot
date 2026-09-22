# -*- coding: UTF-8 -*-

'''
Module
    theme.py
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
    Configures modern dark TTK styles and widget palettes for idecobot.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Style

from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.theme.font_config import FontConfig
from idecobot.infrastructure.gui.theme.theme_constants import ThemeConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ThemeManager:
    '''
        Configures dark theme styles and design tokens for the Tkinter desktop user interface.

        It defines:

            :methods:
                | apply_theme - Applies dark theme stylesheet and color palette to root window.
                | configure_buttons - Configures button styles using design tokens and constants.
                | configure_containers - Configures container, label, and notebook styles.
                | get_version - Returns theme manager version string.
    '''

    @classmethod
    def configure_buttons(
        cls,
        style: Style,
        palette: ColorPalette,
        fonts: FontConfig,
        constants: ThemeConstants
    ) -> None:
        '''
            Configures button styles for standard, accent, success, and danger actions.

            :param style: Active ttk.Style instance.
            :param palette: Color palette design tokens.
            :param fonts: Typography design tokens.
            :param constants: Theme style and color constants.
            :exceptions: None.
        '''
        fg: str = palette.fg_text
        style.configure(
            constants.style_button,
            font=fonts.body_bold,
            padding=list(constants.btn_padding),
            background=palette.btn_bg,
            foreground=fg
        )
        style.map(
            constants.style_button,
            background=[
                ('pressed', palette.btn_pressed),
                ('active', palette.btn_active),
                ('disabled', palette.btn_disabled)
            ],
            foreground=[
                ('pressed', fg),
                ('active', palette.fg_white),
                ('disabled', palette.btn_fg_disabled)
            ]
        )
        style.configure(
            constants.style_accent_button,
            font=fonts.body_bold,
            padding=list(constants.action_btn_padding),
            background=constants.color_accent_bg,
            foreground=palette.fg_white
        )
        style.map(
            constants.style_accent_button,
            background=[
                ('pressed', constants.color_accent_pressed),
                ('active', constants.color_accent_active),
                ('disabled', palette.btn_pressed)
            ],
            foreground=[
                ('pressed', palette.fg_white),
                ('active', palette.fg_white),
                ('disabled', palette.btn_fg_disabled)
            ]
        )
        style.configure(
            constants.style_success_button,
            font=fonts.body_bold,
            padding=list(constants.action_btn_padding),
            background=constants.color_success_bg,
            foreground=palette.fg_white
        )
        style.map(
            constants.style_success_button,
            background=[
                ('pressed', constants.color_success_pressed),
                ('active', constants.color_success_active),
                ('disabled', palette.btn_pressed)
            ],
            foreground=[
                ('pressed', palette.fg_white),
                ('active', palette.fg_white),
                ('disabled', palette.btn_fg_disabled)
            ]
        )
        style.configure(
            constants.style_danger_button,
            font=fonts.body_bold,
            padding=list(constants.action_btn_padding),
            background=constants.color_danger_bg,
            foreground=palette.fg_white
        )
        style.map(
            constants.style_danger_button,
            background=[
                ('pressed', constants.color_danger_pressed),
                ('active', constants.color_danger_active),
                ('disabled', palette.btn_pressed)
            ],
            foreground=[
                ('pressed', palette.fg_white),
                ('active', palette.fg_white),
                ('disabled', palette.btn_fg_disabled)
            ]
        )

    @classmethod
    def configure_containers(
        cls,
        style: Style,
        palette: ColorPalette,
        fonts: FontConfig,
        constants: ThemeConstants
    ) -> None:
        '''
            Configures container styles for frames, labels, and notebooks.

            :param style: Active ttk.Style instance.
            :param palette: Color palette design tokens.
            :param fonts: Typography design tokens.
            :param constants: Theme style and container constants.
            :exceptions: None.
        '''
        bg_dark: str = palette.bg_dark
        bg_card: str = palette.bg_card
        fg: str = palette.fg_text

        style.configure(constants.style_frame, background=bg_dark)
        style.configure(
            constants.style_card_frame,
            background=bg_card,
            relief=constants.relief_flat
        )
        style.configure(
            constants.style_label,
            background=bg_dark,
            foreground=fg,
            font=fonts.body
        )
        style.configure(
            constants.style_header_label,
            background=bg_card,
            foreground=palette.fg_white,
            font=fonts.header
        )
        style.configure(
            constants.style_status_label,
            background=palette.bg_canvas,
            foreground=fg,
            font=fonts.status
        )

        style.configure(constants.style_notebook, background=bg_dark, borderwidth=0)
        style.configure(
            constants.style_notebook_tab,
            background=palette.tab_inactive,
            foreground=fg,
            padding=list(constants.tab_padding),
            font=fonts.body
        )
        style.map(
            constants.style_notebook_tab,
            background=[('selected', bg_card)],
            foreground=[('selected', palette.fg_white)]
        )
        style.configure(
            constants.style_combobox,
            fieldbackground=bg_card,
            background=palette.tab_inactive,
            foreground=fg
        )

    @classmethod
    def apply_theme(
        cls,
        root: Tk,
        palette: ColorPalette,
        fonts: FontConfig,
        constants: ThemeConstants
    ) -> None:
        '''
            Applies dark theme stylesheet and color palette to root window.

            :param root: Root Tk application window.
            :param palette: Injected ColorPalette design tokens.
            :param fonts: Injected FontConfig typography tokens.
            :param constants: Injected ThemeConstants style configuration.
            :exceptions: None.
        '''
        root.configure(bg=palette.bg_dark)
        style: Style = Style(root)
        style.theme_use(constants.theme_name)
        cls.configure_buttons(style, palette, fonts, constants)
        cls.configure_containers(style, palette, fonts, constants)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns theme manager version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
