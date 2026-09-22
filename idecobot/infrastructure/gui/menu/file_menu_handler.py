# -*- coding: UTF-8 -*-

'''
Module
    file_menu_handler.py
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
    Handles file menu actions: new script, open script, and save script dialogs.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo

from idecobot.infrastructure.gui.menu.menu_bar_constants import MenuBarConstants
from idecobot.infrastructure.storage.iscript_storage_service import IScriptStorageService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FileMenuHandler:
    '''
    Handles file menu actions: new script, open script, and save script dialogs.

    It defines:

        :attributes:
            | _root - Injected root Tk window.
            | _storage - Injected IScriptStorageService.
            | _on_load - Callback for loading script text into editor.
            | _on_get - Callback for retrieving active script text.
            | _on_new - Callback for resetting script editor.
            | _constants - Injected MenuBarConstants configuration.
            | _workspace_dir - Mandatory user workspace directory path.
        :methods:
            | __init__ - Initializes file menu handler with injected dependencies.
            | new_script - Resets editor to empty template script.
            | open_script_dialog - Shows open file dialog and loads script.
            | save_script_dialog - Shows save file dialog and persists script.
            | get_version - Returns handler version string.
    '''

    _root: Tk
    _storage: IScriptStorageService
    _on_load: Callable[[str], None]
    _on_get: Callable[[], str]
    _on_new: Callable[[], None]
    _constants: MenuBarConstants
    _workspace_dir: str

    def __init__(
        self,
        root: Tk,
        storage: IScriptStorageService,
        on_load: Callable[[str], None],
        on_get: Callable[[], str],
        on_new: Callable[[], None],
        constants: MenuBarConstants,
        workspace_dir: str
    ) -> None:
        '''
        Initializes file menu handler with injected dependencies.

        :param root: Root Tk window.
        :param storage: Injected IScriptStorageService.
        :param on_load: Callback to load content into editor.
        :param on_get: Callback to get content from editor.
        :param on_new: Callback to clear editor.
        :param constants: Injected MenuBarConstants configuration.
        :param workspace_dir: Mandatory user workspace directory path.
        '''
        self._root = root
        self._storage = storage
        self._on_load = on_load
        self._on_get = on_get
        self._on_new = on_new
        self._constants = constants
        self._workspace_dir = workspace_dir

    def new_script(self) -> None:
        '''
        Resets editor to empty template script.
        '''
        self._on_new()

    def open_script_dialog(self) -> None:
        '''
        Shows open file dialog and loads script into editor.
        '''
        path: str = askopenfilename(
            parent=self._root,
            title=self._constants.title_open_dialog,
            initialdir=self._workspace_dir,
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
        Shows save file dialog and persists active script.
        '''
        path: str = asksaveasfilename(
            parent=self._root,
            title=self._constants.title_save_dialog,
            initialdir=self._workspace_dir,
            defaultextension=self._constants.file_extension,
            filetypes=list(self._constants.filetypes)
        )
        if path:
            content: str = self._on_get()
            self._storage.save_script(path, content)

    def get_version(self) -> str:
        '''
        Returns handler version string.

        :return: Version string.
        '''
        return __version__
