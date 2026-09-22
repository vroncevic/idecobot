# -*- coding: UTF-8 -*-

'''
Module
    gui_bundle_factory_constants.py
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
    Defines GUIBundleFactoryConstants frozen dataclass for desktop GUI bundle assembly.
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


@dataclass(slots=True, frozen=True)
class GUIBundleFactoryConstants:
    '''
        Constants for desktop GUI bundle assembly, window geometry, and paned weights.

        It defines:

            :attributes:
                | window_title - Application main window title string.
                | min_width - Minimum window width in pixels.
                | min_height - Minimum window height in pixels.
                | paned_padx - Horizontal padding for the primary paned container.
                | paned_pady - Vertical padding for the primary paned container.
                | weight_top - Paned layout expansion weight for top manual control tier.
                | weight_mid - Paned layout expansion weight for middle editor tier.
                | weight_bot - Paned layout expansion weight for bottom monitor tier.
                | default_home_speed - Default joint speed percentage for zero home command.
                | attr_zoomed - Window attribute flag for maximized state on X11/Linux.
                | state_zoomed - Window state string for maximized state on Windows.
    '''

    window_title: str = 'idecobot — myCobot 280 Motion Studio & DSL Editor'
    min_width: int = 1050
    min_height: int = 720
    paned_padx: int = 4
    paned_pady: int = 2
    weight_top: int = 2
    weight_mid: int = 4
    weight_bot: int = 3
    default_home_speed: int = 30
    attr_zoomed: str = '-zoomed'
    state_zoomed: str = 'zoomed'
