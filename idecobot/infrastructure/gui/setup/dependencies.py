# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Encapsulates core GUI components for simplification of GUI bundle.
'''

from __future__ import annotations

from tkinter import Tk
from typing import TypedDict

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.communication.iserial_port_scanner import ISerialPortScanner
from idecobot.infrastructure.gui.editor.editor_panel import EditorPanel
from idecobot.infrastructure.gui.jog.jog_panel import JogPanel
from idecobot.infrastructure.gui.log.log_panel import LogPanel
from idecobot.infrastructure.gui.menu.menu_bar import MenuBar
from idecobot.infrastructure.gui.stream.connection_panel import ConnectionPanel
from idecobot.infrastructure.gui.stream.status_bar import StatusBar
from idecobot.infrastructure.gui.toolbar.toolbar import Toolbar
from idecobot.infrastructure.storage.iscript_storage_service import IScriptStorageService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GUIBundleDependencies(TypedDict):
    '''
        Encapsulates core GUI components for simplification of GUI bundle.

        It defines:

            :attributes:
                | service - Core robot application service.
                | scanner - Hardware serial port scanner.
                | storage - DSL script storage service.
                | root - Desktop Tk main window.
                | menu_bar - Application top menu bar.
                | toolbar - Quick action toolbar.
                | port_panel - Serial port connection header.
                | jog_panel - Manual 6-DOF jog controller.
                | editor_panel - Syntax-highlighted DSL editor.
                | log_panel - Serial monitor console.
                | status_bar - Telemetry stream status bar.
    '''

    service: IService
    scanner: ISerialPortScanner
    storage: IScriptStorageService
    root: Tk
    menu_bar: MenuBar
    toolbar: Toolbar
    port_panel: ConnectionPanel
    jog_panel: JogPanel
    editor_panel: EditorPanel
    log_panel: LogPanel
    status_bar: StatusBar
