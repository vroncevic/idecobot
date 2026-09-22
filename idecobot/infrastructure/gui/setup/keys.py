# -*- coding: UTF-8 -*-

'''
Module
    keys.py
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
    Runtime components and interface constraints for the GUI bundle.
'''

from __future__ import annotations

from tkinter import Tk
from types import MappingProxyType
from typing import ClassVar, Literal

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.communication.iserial_port_scanner import ISerialPortScanner
from idecobot.infrastructure.gui.editor.editor_panel import EditorPanel
from idecobot.infrastructure.gui.jog.jog_panel import JogPanel
from idecobot.infrastructure.gui.log.log_panel import LogPanel
from idecobot.infrastructure.gui.menu.imenu_bar import IMenuBar
from idecobot.infrastructure.gui.stream.connection_panel import ConnectionPanel
from idecobot.infrastructure.gui.stream.status_bar import StatusBar
from idecobot.infrastructure.gui.toolbar.itoolbar import IToolbar
from idecobot.infrastructure.storage.iscript_storage_service import IScriptStorageService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GUIBundleKeys:
    '''
        Runtime components and interface constraints for the GUI bundle.

        It defines:

            :attributes:
                | DEPENDENCY_SERVICE - The service interface constant of the GUI bundle.
                | DEPENDENCY_SCANNER - The scanner interface constant of the GUI bundle.
                | DEPENDENCY_STORAGE - The storage interface constant of the GUI bundle.
                | DEPENDENCY_ROOT - The Tk root window constant of the GUI bundle.
                | DEPENDENCY_MENU_BAR - The application menu bar constant of the GUI bundle.
                | DEPENDENCY_TOOLBAR - The quick action toolbar constant of the GUI bundle.
                | DEPENDENCY_PORT_PANEL - The serial connection panel constant of the GUI bundle.
                | DEPENDENCY_JOG_PANEL - The manual jog panel constant of the GUI bundle.
                | DEPENDENCY_EDITOR_PANEL - The DSL editor panel constant of the GUI bundle.
                | DEPENDENCY_LOG_PANEL - The log console panel constant of the GUI bundle.
                | DEPENDENCY_STATUS_BAR - The telemetry status bar constant of the GUI bundle.
                | OPTION_SERVICE - The service option constant of the GUI bundle.
                | OPTION_SCANNER - The scanner option constant of the GUI bundle.
                | OPTION_STORAGE - The storage option constant of the GUI bundle.
            :methods:
                | get_dependency_to_type - Returns the mapping of the GUI bundle dependencies to their types.
                | get_option_to_type - Returns the mapping of the GUI bundle options to their types.
    '''

    DEPENDENCY_SERVICE: ClassVar[Literal['service']] = 'service'
    DEPENDENCY_SCANNER: ClassVar[Literal['scanner']] = 'scanner'
    DEPENDENCY_STORAGE: ClassVar[Literal['storage']] = 'storage'
    DEPENDENCY_ROOT: ClassVar[Literal['root']] = 'root'
    DEPENDENCY_MENU_BAR: ClassVar[Literal['menu_bar']] = 'menu_bar'
    DEPENDENCY_TOOLBAR: ClassVar[Literal['toolbar']] = 'toolbar'
    DEPENDENCY_PORT_PANEL: ClassVar[Literal['port_panel']] = 'port_panel'
    DEPENDENCY_JOG_PANEL: ClassVar[Literal['jog_panel']] = 'jog_panel'
    DEPENDENCY_EDITOR_PANEL: ClassVar[Literal['editor_panel']] = 'editor_panel'
    DEPENDENCY_LOG_PANEL: ClassVar[Literal['log_panel']] = 'log_panel'
    DEPENDENCY_STATUS_BAR: ClassVar[Literal['status_bar']] = 'status_bar'

    OPTION_SERVICE: ClassVar[Literal['service']] = 'service'
    OPTION_SCANNER: ClassVar[Literal['scanner']] = 'scanner'
    OPTION_STORAGE: ClassVar[Literal['storage']] = 'storage'

    @classmethod
    def get_dependency_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of the GUI bundle dependencies to their types.

            :return: The mapping of the GUI bundle dependencies to their types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.DEPENDENCY_SERVICE: IService,
            cls.DEPENDENCY_SCANNER: ISerialPortScanner,
            cls.DEPENDENCY_STORAGE: IScriptStorageService,
            cls.DEPENDENCY_ROOT: Tk,
            cls.DEPENDENCY_MENU_BAR: IMenuBar,
            cls.DEPENDENCY_TOOLBAR: IToolbar,
            cls.DEPENDENCY_PORT_PANEL: ConnectionPanel,
            cls.DEPENDENCY_JOG_PANEL: JogPanel,
            cls.DEPENDENCY_EDITOR_PANEL: EditorPanel,
            cls.DEPENDENCY_LOG_PANEL: LogPanel,
            cls.DEPENDENCY_STATUS_BAR: StatusBar,
        })

    @classmethod
    def get_option_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of the GUI bundle options to their types.

            :return: The mapping of the GUI bundle options to their types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.OPTION_SERVICE: IService,
            cls.OPTION_SCANNER: ISerialPortScanner,
            cls.OPTION_STORAGE: IScriptStorageService,
        })
