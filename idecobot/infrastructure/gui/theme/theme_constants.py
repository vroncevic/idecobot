# -*- coding: UTF-8 -*-

'''
Module
    theme_constants.py
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
    Defines ThemeConstants frozen dataclass for desktop GUI theming.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class ThemeConstants:
    '''
        Constants for desktop GUI theming, TTK style names, paddings, and action colors.

        It defines:

            :attributes:
                | theme_name - TTK built-in theme engine identifier.
                | btn_padding - Horizontal and vertical padding for standard buttons.
                | action_btn_padding - Horizontal and vertical padding for colored action buttons.
                | tab_padding - Horizontal and vertical padding for notebook tabs.
                | color_accent_bg - Normal background color for accent buttons.
                | color_accent_pressed - Pressed background color for accent buttons.
                | color_accent_active - Hover/active background color for accent buttons.
                | color_success_bg - Normal background color for success buttons.
                | color_success_pressed - Pressed background color for success buttons.
                | color_success_active - Hover/active background color for success buttons.
                | color_danger_bg - Normal background color for danger buttons.
                | color_danger_pressed - Pressed background color for danger buttons.
                | color_danger_active - Hover/active background color for danger buttons.
                | style_button - TTK style identifier for standard buttons.
                | style_accent_button - TTK style identifier for accent buttons.
                | style_success_button - TTK style identifier for success buttons.
                | style_danger_button - TTK style identifier for danger buttons.
                | style_frame - TTK style identifier for standard container frames.
                | style_card_frame - TTK style identifier for card container frames.
                | style_label - TTK style identifier for standard labels.
                | style_header_label - TTK style identifier for section header labels.
                | style_status_label - TTK style identifier for status readouts.
                | style_notebook - TTK style identifier for tabbed notebooks.
                | style_notebook_tab - TTK style identifier for individual notebook tabs.
                | style_combobox - TTK style identifier for dropdown comboboxes.
                | relief_flat - Relief style string for flat card frames.
    '''

    theme_name: str = 'clam'
    btn_padding: tuple[int, int] = (6, 2)
    action_btn_padding: tuple[int, int] = (8, 2)
    tab_padding: tuple[int, int] = (10, 4)
    color_accent_bg: str = '#0e639c'
    color_accent_pressed: str = '#0b4d79'
    color_accent_active: str = '#1177bb'
    color_success_bg: str = '#2e7d32'
    color_success_pressed: str = '#1b5e20'
    color_success_active: str = '#388e3c'
    color_danger_bg: str = '#c62828'
    color_danger_pressed: str = '#b71c1c'
    color_danger_active: str = '#e53935'
    style_button: str = 'TButton'
    style_accent_button: str = 'Accent.TButton'
    style_success_button: str = 'Success.TButton'
    style_danger_button: str = 'Danger.TButton'
    style_frame: str = 'TFrame'
    style_card_frame: str = 'Card.TFrame'
    style_label: str = 'TLabel'
    style_header_label: str = 'Header.TLabel'
    style_status_label: str = 'Status.TLabel'
    style_notebook: str = 'TNotebook'
    style_notebook_tab: str = 'TNotebook.Tab'
    style_combobox: str = 'TCombobox'
    relief_flat: str = 'flat'
