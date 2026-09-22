# -*- coding: UTF-8 -*-

'''
Module
    menu_bar.py
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
    Defines MenuBar composite coordinating domain-specific menu handlers.
'''

from __future__ import annotations

from tkinter import Menu

from idecobot.infrastructure.gui.menu.idiagnostics_menu_handler import IDiagnosticsMenuHandler
from idecobot.infrastructure.gui.menu.ifile_menu_handler import IFileMenuHandler
from idecobot.infrastructure.gui.menu.ihelp_menu_handler import IHelpMenuHandler
from idecobot.infrastructure.gui.menu.menu_bar_constants import MenuBarConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MenuBar:
    '''
    Application menu bar coordinating domain-specific menu action handlers.

    It defines:

        :attributes:
            | _menu_bar - Injected Tkinter Menu instance.
            | _file_handler - Injected IFileMenuHandler for script operations.
            | _diagnostics_handler - Injected IDiagnosticsMenuHandler for robot diagnostics.
            | _help_handler - Injected IHelpMenuHandler for reference and dialogs.
            | _constants - Injected MenuBarConstants configuration.
        :methods:
            | __init__ - Initializes MenuBar with injected handlers and widgets.
            | get_file_handler - Returns the file menu handler.
            | get_diagnostics_handler - Returns the diagnostics menu handler.
            | get_help_handler - Returns the help menu handler.
            | new_script - Delegates to file handler to reset editor.
            | open_script_dialog - Delegates to file handler to open script.
            | save_script_dialog - Delegates to file handler to save script.
            | show_about_dialog - Delegates to help handler for about dialog.
            | show_dsl_help - Delegates to help handler for DSL reference.
            | get_version - Returns component version string.
            | constants - Property returning injected MenuBarConstants.
            | menu_bar - Property returning Tkinter Menu widget.
            | file_handler - Property returning file menu handler.
            | diagnostics_handler - Property returning diagnostics menu handler.
            | help_handler - Property returning help menu handler.
    '''

    _menu_bar: Menu
    _file_handler: IFileMenuHandler
    _diagnostics_handler: IDiagnosticsMenuHandler
    _help_handler: IHelpMenuHandler
    _constants: MenuBarConstants

    def __init__(
        self,
        menu_bar: Menu,
        file_handler: IFileMenuHandler,
        diagnostics_handler: IDiagnosticsMenuHandler,
        help_handler: IHelpMenuHandler,
        constants: MenuBarConstants
    ) -> None:
        '''
        Initializes menu bar composite with injected domain handlers.

        :param menu_bar: Injected Tkinter Menu instance.
        :param file_handler: Injected IFileMenuHandler.
        :param diagnostics_handler: Injected IDiagnosticsMenuHandler.
        :param help_handler: Injected IHelpMenuHandler.
        :param constants: Injected MenuBarConstants configuration.
        '''
        self._menu_bar = menu_bar
        self._file_handler = file_handler
        self._diagnostics_handler = diagnostics_handler
        self._help_handler = help_handler
        self._constants = constants

    def get_file_handler(self) -> IFileMenuHandler:
        '''
        Returns the file menu handler.

        :return: IFileMenuHandler instance.
        '''
        return self._file_handler

    def get_diagnostics_handler(self) -> IDiagnosticsMenuHandler:
        '''
        Returns the diagnostics menu handler.

        :return: IDiagnosticsMenuHandler instance.
        '''
        return self._diagnostics_handler

    def get_help_handler(self) -> IHelpMenuHandler:
        '''
        Returns the help menu handler.

        :return: IHelpMenuHandler instance.
        '''
        return self._help_handler

    def new_script(self) -> None:
        '''
        Delegates to file handler to reset editor.
        '''
        self._file_handler.new_script()

    def open_script_dialog(self) -> None:
        '''
        Delegates to file handler to open script dialog.
        '''
        self._file_handler.open_script_dialog()

    def save_script_dialog(self) -> None:
        '''
        Delegates to file handler to save script dialog.
        '''
        self._file_handler.save_script_dialog()

    def show_about_dialog(self) -> None:
        '''
        Delegates to help handler for about dialog.
        '''
        self._help_handler.show_about_dialog()

    def show_dsl_help(self) -> None:
        '''
        Delegates to help handler for DSL reference.
        '''
        self._help_handler.show_dsl_help()

    @property
    def constants(self) -> MenuBarConstants:
        '''
        Returns injected MenuBarConstants.

        :return: MenuBarConstants instance.
        '''
        return self._constants

    @property
    def menu_bar(self) -> Menu:
        '''
        Returns underlying Tkinter Menu.

        :return: Tkinter Menu instance.
        '''
        return self._menu_bar

    @property
    def file_handler(self) -> IFileMenuHandler:
        '''
        Returns file menu handler.

        :return: IFileMenuHandler instance.
        '''
        return self._file_handler

    @property
    def diagnostics_handler(self) -> IDiagnosticsMenuHandler:
        '''
        Returns diagnostics menu handler.

        :return: IDiagnosticsMenuHandler instance.
        '''
        return self._diagnostics_handler

    @property
    def help_handler(self) -> IHelpMenuHandler:
        '''
        Returns help menu handler.

        :return: IHelpMenuHandler instance.
        '''
        return self._help_handler

    def get_version(self) -> str:
        '''
        Returns component version string.

        :return: Version string.
        '''
        return __version__
