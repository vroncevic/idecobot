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

from idecobot.infrastructure.gui.menu.idiagnostics_menu_handler import IDiagnosticsMenuHandler
from idecobot.infrastructure.gui.menu.ifile_menu_handler import IFileMenuHandler
from idecobot.infrastructure.gui.menu.ihelp_menu_handler import IHelpMenuHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMenuBar(Protocol):
    '''
    Structural interface protocol for top-level menu bar coordinating domain handlers.

    It defines:

        :methods:
            | get_file_handler - Returns the file menu actions handler.
            | get_diagnostics_handler - Returns the diagnostics menu actions handler.
            | get_help_handler - Returns the help menu actions handler.
            | get_version - Returns protocol version string.
    '''

    def get_file_handler(self) -> IFileMenuHandler:
        '''
        Returns the file menu actions handler.

        :return: IFileMenuHandler instance.
        '''

    def get_diagnostics_handler(self) -> IDiagnosticsMenuHandler:
        '''
        Returns the diagnostics menu actions handler.

        :return: IDiagnosticsMenuHandler instance.
        '''

    def get_help_handler(self) -> IHelpMenuHandler:
        '''
        Returns the help menu actions handler.

        :return: IHelpMenuHandler instance.
        '''

    def get_version(self) -> str:
        '''
        Returns protocol version string.

        :return: Version string.
        '''
