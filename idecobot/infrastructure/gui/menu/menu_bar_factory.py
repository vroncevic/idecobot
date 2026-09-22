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
    Defines MenuBarFactory assembling domain handlers into MenuBar.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import Menu, Tk

from idecobot.infrastructure.diagnostics.idiagnostics_coordinator import IDiagnosticsCoordinator
from idecobot.infrastructure.gui.menu.diagnostics_menu_handler import DiagnosticsMenuHandler
from idecobot.infrastructure.gui.menu.file_menu_handler import FileMenuHandler
from idecobot.infrastructure.gui.menu.help_menu_handler import HelpMenuHandler
from idecobot.infrastructure.gui.menu.menu_bar import MenuBar
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


class MenuBarFactory:
    '''
    Factory assembling domain menu handlers and wiring cascades.

    It defines:

        :methods:
            | create_menu_bar - Constructs Menu widgets, wires domain handlers, and returns MenuBar.
            | get_version - Returns factory version string.
    '''

    @classmethod
    def create_menu_bar(
        cls,
        root: Tk,
        storage: IScriptStorageService,
        on_load: Callable[[str], None],
        on_get: Callable[[], str],
        on_new: Callable[[], None],
        diagnostics: IDiagnosticsCoordinator,
        on_log: Callable[[str], None],
        constants: MenuBarConstants,
        workspace_dir: str
    ) -> MenuBar:
        '''
        Constructs and wires the top-level MenuBar with domain handlers.

        :param root: Root Tk window.
        :param storage: Injected IScriptStorageService.
        :param on_load: Callback to load content into editor.
        :param on_get: Callback to get content from editor.
        :param on_new: Callback to clear editor.
        :param diagnostics: Injected IDiagnosticsCoordinator.
        :param on_log: Callback to append messages to serial monitor log.
        :param constants: Injected MenuBarConstants configuration.
        :param workspace_dir: Mandatory user workspace directory path.
        :return: Fully assembled MenuBar instance.
        '''
        file_handler: FileMenuHandler = FileMenuHandler(
            root=root,
            storage=storage,
            on_load=on_load,
            on_get=on_get,
            on_new=on_new,
            constants=constants,
            workspace_dir=workspace_dir
        )

        diagnostics_handler: DiagnosticsMenuHandler = DiagnosticsMenuHandler(
            diagnostics=diagnostics,
            on_log=on_log
        )

        help_handler: HelpMenuHandler = HelpMenuHandler(
            root=root,
            constants=constants
        )

        menu_bar: Menu = Menu(root)

        file_menu: Menu = Menu(menu_bar, tearoff=False)
        file_menu.add_command(
            label=constants.label_new_script,
            command=file_handler.new_script,
            accelerator=constants.accel_new
        )
        file_menu.add_command(
            label=constants.label_open_script,
            command=file_handler.open_script_dialog,
            accelerator=constants.accel_open
        )
        file_menu.add_command(
            label=constants.label_save_script,
            command=file_handler.save_script_dialog,
            accelerator=constants.accel_save
        )
        file_menu.add_separator()
        file_menu.add_command(
            label=constants.label_exit,
            command=root.quit
        )
        menu_bar.add_cascade(label=constants.label_file_menu, menu=file_menu)

        diagnostics_menu: Menu = Menu(menu_bar, tearoff=False)
        diagnostics_menu.add_command(
            label=constants.label_diag_link,
            command=diagnostics_handler.diagnose_link
        )
        diagnostics_menu.add_command(
            label=constants.label_diag_angles,
            command=diagnostics_handler.diagnose_angles
        )
        diagnostics_menu.add_command(
            label=constants.label_diag_coords,
            command=diagnostics_handler.diagnose_coords
        )
        diagnostics_menu.add_command(
            label=constants.label_diag_temperatures,
            command=diagnostics_handler.diagnose_temperatures
        )
        diagnostics_menu.add_command(
            label=constants.label_diag_voltages,
            command=diagnostics_handler.diagnose_voltages
        )
        diagnostics_menu.add_separator()
        diagnostics_menu.add_command(
            label=constants.label_diag_power_on,
            command=diagnostics_handler.diagnose_power_on
        )
        diagnostics_menu.add_command(
            label=constants.label_diag_release,
            command=diagnostics_handler.diagnose_release_servos
        )
        menu_bar.add_cascade(
            label=constants.label_diagnostics_menu,
            menu=diagnostics_menu
        )

        help_menu: Menu = Menu(menu_bar, tearoff=False)
        help_menu.add_command(
            label=constants.label_dsl_reference,
            command=help_handler.show_dsl_help
        )
        help_menu.add_separator()
        help_menu.add_command(
            label=constants.label_about,
            command=help_handler.show_about_dialog
        )
        menu_bar.add_cascade(label=constants.label_help_menu, menu=help_menu)

        root.config(menu=menu_bar)

        return MenuBar(
            menu_bar=menu_bar,
            file_handler=file_handler,
            diagnostics_handler=diagnostics_handler,
            help_handler=help_handler,
            constants=constants
        )

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns factory version string.

        :return: Version string.
        '''
        return __version__
