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
    Defines MenuBar implementing application top menu.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import Menu, Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo

from idecobot.infrastructure.gui.menu.menu_bar_constants import MenuBarConstants
from idecobot.infrastructure.storage.iscript_storage_service import IScriptStorageService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MenuBar:
    '''
        Application menu bar managing File and Help dropdown actions.

        It defines:

            :attributes:
                | _root - Injected root Tk window.
                | _storage - Injected IScriptStorageService.
                | _on_load - Callback for loading script text.
                | _on_get - Callback for retrieving active script text.
                | _on_new - Callback for resetting script editor.
                | _menu_bar - Injected Tkinter Menu instance.
                | _constants - Injected MenuBarConstants configuration.
            :methods:
                | __init__ - Initializes MenuBar with injected dependencies.
                | open_script_dialog - Opens file dialog and loads script.
                | save_script_dialog - Opens save dialog and persists script.
                | new_script - Resets editor to new script.
                | show_about_dialog - Displays about dialog.
                | show_dsl_help - Displays DSL help dialog.
                | get_version - Returns component version string.
                | constants - Property returning injected MenuBarConstants.
                | menu_bar - Property returning Tkinter Menu widget.
    '''

    _root: Tk
    _storage: IScriptStorageService
    _on_load: Callable[[str], None]
    _on_get: Callable[[], str]
    _on_new: Callable[[], None]
    _menu_bar: Menu
    _constants: MenuBarConstants

    def __init__(
        self,
        root: Tk,
        storage: IScriptStorageService,
        on_load: Callable[[str], None],
        on_get: Callable[[], str],
        on_new: Callable[[], None],
        menu_bar: Menu,
        constants: MenuBarConstants
    ) -> None:
        '''
            Initializes menu bar with injected dependencies.

            :param root: Root Tk window.
            :param storage: Injected IScriptStorageService.
            :param on_load: Callback to load content into editor.
            :param on_get: Callback to get content from editor.
            :param on_new: Callback to clear editor.
            :param menu_bar: Injected Tkinter Menu instance.
            :param constants: Injected MenuBarConstants configuration.
            :exceptions: None.
        '''
        self._root = root
        self._storage = storage
        self._on_load = on_load
        self._on_get = on_get
        self._on_new = on_new
        self._menu_bar = menu_bar
        self._constants = constants

    def open_script_dialog(self) -> None:
        '''
            Shows open file dialog and loads script into editor.

            :exceptions: None.
        '''
        path: str = askopenfilename(
            parent=self._root,
            title=self._constants.title_open_dialog,
            filetypes=list(self._constants.filetypes)
        )
        if path:
            try:
                content: str = self._storage.load_script(path)
                self._on_load(content)

            except (OSError, ValueError) as err:
                showinfo(self._constants.title_error_dialog, str(err), parent=self._root)

    def save_script_dialog(self) -> None:
        '''
            Shows save file dialog and saves current script.

            :exceptions: None.
        '''
        path: str = asksaveasfilename(
            parent=self._root,
            title=self._constants.title_save_dialog,
            defaultextension=self._constants.file_extension,
            filetypes=list(self._constants.filetypes)
        )
        if path:
            content: str = self._on_get()
            self._storage.save_script(path, content)

    def new_script(self) -> None:
        '''
            Resets editor to empty template script.

            :exceptions: None.
        '''
        self._on_new()

    def show_about_dialog(self) -> None:
        '''
            Displays about dialog.

            :exceptions: None.
        '''
        showinfo(
            self._constants.title_about_dialog,
            self._constants.about_text,
            parent=self._root
        )

    def show_dsl_help(self) -> None:
        '''
            Displays DSL syntax reference dialog.

            :exceptions: None.
        '''
        showinfo(
            self._constants.title_help_dialog,
            self._constants.help_text,
            parent=self._root
        )

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

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

