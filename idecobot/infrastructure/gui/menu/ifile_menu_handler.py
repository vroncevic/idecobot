# -*- coding: UTF-8 -*-

'''
Module
    ifile_menu_handler.py
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
    Defines structural interface protocol IFileMenuHandler for script file actions.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IFileMenuHandler(Protocol):
    '''
    Structural interface protocol for file menu script actions.

    It defines:

        :methods:
            | new_script - Resets editor to empty template script.
            | open_script_dialog - Shows open file dialog and loads script.
            | save_script_dialog - Shows save file dialog and persists script.
            | get_version - Returns protocol version string.
    '''

    def new_script(self) -> None:
        '''
        Resets editor to empty template script.
        '''

    def open_script_dialog(self) -> None:
        '''
        Shows open file dialog and loads script into editor.
        '''

    def save_script_dialog(self) -> None:
        '''
        Shows save file dialog and persists active script.
        '''

    def get_version(self) -> str:
        '''
        Returns protocol version string.

        :return: Version string.
        '''
