# -*- coding: UTF-8 -*-

'''
Module
    menu_bar_factory.py
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
    Defines MenuBarFactory responsible for assembling MenuBar.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import Menu, Tk

from idecobot.infrastructure.gui.menu.menu_bar import MenuBar
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


class MenuBarFactory:
    '''
        Factory class assembling MenuBar composite and wiring cascades and actions.

        It defines:

            :methods:
                | create_menu_bar - Constructs Menu widgets, binds commands, and returns MenuBar.
    '''

    @classmethod
    def create_menu_bar(
        cls,
        root: Tk,
        storage: IScriptStorageService,
        on_load: Callable[[str], None],
        on_get: Callable[[], str],
        on_new: Callable[[], None],
        constants: MenuBarConstants
    ) -> MenuBar:
        '''
            Constructs and wires the top-level MenuBar.

            :param root: Root Tk window.
            :param storage: Injected IScriptStorageService.
            :param on_load: Callback to load content into editor.
            :param on_get: Callback to get content from editor.
            :param on_new: Callback to clear editor.
            :param constants: Injected MenuBarConstants configuration.
            :return: Fully assembled MenuBar instance.
            :exceptions: None.
        '''
        menu_bar: Menu = Menu(root)

        panel: MenuBar = MenuBar(
            root=root,
            storage=storage,
            on_load=on_load,
            on_get=on_get,
            on_new=on_new,
            menu_bar=menu_bar,
            constants=constants
        )

        file_menu: Menu = Menu(menu_bar, tearoff=False)
        file_menu.add_command(
            label=constants.label_new_script,
            command=panel.new_script,
            accelerator=constants.accel_new
        )
        file_menu.add_command(
            label=constants.label_open_script,
            command=panel.open_script_dialog,
            accelerator=constants.accel_open
        )
        file_menu.add_command(
            label=constants.label_save_script,
            command=panel.save_script_dialog,
            accelerator=constants.accel_save
        )
        file_menu.add_separator()
        file_menu.add_command(
            label=constants.label_exit,
            command=root.quit
        )
        menu_bar.add_cascade(label=constants.label_file_menu, menu=file_menu)

        help_menu: Menu = Menu(menu_bar, tearoff=False)
        help_menu.add_command(
            label=constants.label_dsl_reference,
            command=panel.show_dsl_help
        )
        help_menu.add_separator()
        help_menu.add_command(
            label=constants.label_about,
            command=panel.show_about_dialog
        )
        menu_bar.add_cascade(label=constants.label_help_menu, menu=help_menu)

        root.config(menu=menu_bar)

        return panel
