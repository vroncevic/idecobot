# -*- coding: UTF-8 -*-

'''
Module
    test_theme.py
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
    Unit tests for desktop GUI theming, design tokens, and ThemeManager.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Style
from unittest import TestCase, main

from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.theme.font_config import FontConfig
from idecobot.infrastructure.gui.theme.theme import ThemeManager
from idecobot.infrastructure.gui.theme.theme_constants import ThemeConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTheme(TestCase):
    '''
        Unit tests for ThemeConstants, ColorPalette, FontConfig, and ThemeManager.

        It defines:

            :methods:
                | setUp - Initializes root Tk window for theme inspection.
                | tearDown - Destroys root Tk window.
                | test_color_palette_defaults - Verifies ColorPalette default color tokens.
                | test_font_config_defaults - Verifies FontConfig default typography tokens.
                | test_theme_constants_defaults - Verifies ThemeConstants default identifiers.
                | test_apply_theme - Verifies ThemeManager applies styles to Tk root.
    '''

    def setUp(self) -> None:
        '''
            Initializes Tk root window before each test.
        '''
        self.root: Tk = Tk()
        self.root.withdraw()
        self.palette: ColorPalette = ColorPalette()
        self.fonts: FontConfig = FontConfig()
        self.constants: ThemeConstants = ThemeConstants()

    def tearDown(self) -> None:
        '''
            Destroys Tk root window after each test.
        '''
        self.root.destroy()

    def test_color_palette_defaults(self) -> None:
        '''
            Verifies ColorPalette default design tokens.
        '''
        self.assertTrue(self.palette.bg_dark.startswith('#'))
        self.assertTrue(self.palette.bg_card.startswith('#'))
        self.assertTrue(self.palette.fg_white.startswith('#'))
        self.assertEqual(self.palette.accent_blue, '#61afef')
        self.assertEqual(self.palette.accent_green, '#98c379')

    def test_font_config_defaults(self) -> None:
        '''
            Verifies FontConfig typography definitions.
        '''
        self.assertEqual(len(self.fonts.body), 2)
        self.assertEqual(len(self.fonts.body_bold), 3)
        self.assertEqual(len(self.fonts.header), 3)
        self.assertEqual(len(self.fonts.code), 2)


    def test_theme_constants_defaults(self) -> None:
        '''
            Verifies ThemeConstants style names, paddings, and hex codes.
        '''
        self.assertEqual(self.constants.theme_name, 'clam')
        self.assertEqual(self.constants.style_button, 'TButton')
        self.assertEqual(self.constants.style_accent_button, 'Accent.TButton')
        self.assertEqual(self.constants.relief_flat, 'flat')

    def test_apply_theme(self) -> None:
        '''
            Verifies ThemeManager.apply_theme applies style configurations without errors.
        '''
        ThemeManager.apply_theme(
            root=self.root,
            palette=self.palette,
            fonts=self.fonts,
            constants=self.constants
        )
        style: Style = Style(self.root)
        self.assertEqual(style.theme_use(), self.constants.theme_name)


if __name__ == '__main__':
    main()
