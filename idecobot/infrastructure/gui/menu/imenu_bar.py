# -*- coding: UTF-8 -*-

'''
Module
    imenu_bar.py
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
    Defines structural interface protocol IMenuBar for application top-level menu bar.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMenuBar(Protocol):
    '''
        Structural interface protocol for top-level menu bar operations.

        It defines:

            :methods:
                | open_script_dialog - Shows open file dialog and loads script.
                | save_script_dialog - Shows save file dialog and saves script.
                | new_script - Resets editor to empty template script.
                | show_about_dialog - Displays about dialog.
                | show_dsl_help - Displays DSL syntax reference dialog.
                | get_version - Returns protocol version string.
    '''

    def open_script_dialog(self) -> None:
        '''
            Shows open file dialog and loads script into editor.
        '''

    def save_script_dialog(self) -> None:
        '''
            Shows save file dialog and saves current script.
        '''

    def new_script(self) -> None:
        '''
            Resets editor to empty template script.
        '''

    def show_about_dialog(self) -> None:
        '''
            Displays about dialog.
        '''

    def show_dsl_help(self) -> None:
        '''
            Displays DSL syntax reference dialog.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
        '''

