# -*- coding: UTF-8 -*-

'''
Module
    menu_bar_constants.py
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
    Defines MenuBarConstants frozen dataclass for MenuBar component.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class MenuBarConstants:
    '''
        Constants for menu bar cascade headers, menu item labels, accelerators, and dialogs.

        It defines:

            :attributes:
                | label_file_menu - Title string for the File cascade menu.
                | label_help_menu - Title string for the Help cascade menu.
                | label_new_script - Action label for creating a new script.
                | label_open_script - Action label for opening an existing script.
                | label_save_script - Action label for saving active script.
                | label_exit - Action label for exiting application.
                | label_dsl_reference - Action label for DSL syntax reference dialog.
                | label_about - Action label for application about dialog.
                | accel_new - Keyboard shortcut accelerator string for new script.
                | accel_open - Keyboard shortcut accelerator string for open script.
                | accel_save - Keyboard shortcut accelerator string for save script.
                | title_open_dialog - Dialog window title for opening scripts.
                | title_save_dialog - Dialog window title for saving scripts.
                | title_error_dialog - Dialog window title for error alerts.
                | title_about_dialog - Dialog window title for about dialog.
                | title_help_dialog - Dialog window title for DSL syntax reference.
                | file_extension - Standard DSL file extension.
                | filetypes - Supported file type filters for file dialogs.
                | about_text - Informational text displayed in about dialog.
                | help_text - Reference syntax text displayed in help dialog.
    '''

    label_file_menu: str = 'File'
    label_help_menu: str = 'Help'
    label_new_script: str = 'New Script'
    label_open_script: str = 'Open .cobot Script...'
    label_save_script: str = 'Save .cobot Script...'
    label_exit: str = 'Exit'
    label_dsl_reference: str = 'DSL Reference'
    label_about: str = 'About idecobot'
    accel_new: str = 'Ctrl+N'
    accel_open: str = 'Ctrl+O'
    accel_save: str = 'Ctrl+S'
    title_open_dialog: str = 'Open myCobot DSL Script'
    title_save_dialog: str = 'Save myCobot DSL Script'
    title_error_dialog: str = 'Open Error'
    title_about_dialog: str = 'About idecobot'
    title_help_dialog: str = 'DSL Syntax Reference'
    file_extension: str = '.cobot'
    filetypes: tuple[tuple[str, str], ...] = (
        ('myCobot Scripts', '*.cobot'),
        ('All Files', '*.*')
    )
    about_text: str = (
        'idecobot v1.0.0\n'
        'Robot IDE & Motion Studio for Elephant Robotics myCobot 280\n'
        'Copyright (C) 2026 Vladimir Roncevic\n'
        'GPLv3 License'
    )
    help_text: str = (
        'Commands:\n'
        '  MOVE J1:0 J2:20 J3:0 J4:0 J5:0 J6:0 SPEED:30\n'
        '  MOVE X:100 Y:120 Z:150 RX:0 RY:0 RZ:0 SPEED:30\n'
        '  HOME\n'
        '  POWER\n'
        '  RELAX\n'
        '  TOOL GRIP / TOOL RELEASE\n'
        '  SPEED 50\n'
        '  WAIT 1.5\n'
    )
