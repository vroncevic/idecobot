# -*- coding: UTF-8 -*-

'''
Module
    validator.py
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
    Validator for the GUI bundle.
'''

from __future__ import annotations

from tkinter import Tk
from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_value import not_none
from ats_utilities.validation.check_type import istype

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.communication.iserial_port_scanner import ISerialPortScanner
from idecobot.infrastructure.gui.editor.editor_panel import EditorPanel
from idecobot.infrastructure.gui.jog.jog_panel import JogPanel
from idecobot.infrastructure.gui.log.log_panel import LogPanel
from idecobot.infrastructure.gui.menu.imenu_bar import IMenuBar
from idecobot.infrastructure.gui.setup.bundle import GUIBundle
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


class GUIBundleValidator:
    '''
        Validator for the GUI bundle.

        It defines:

            :methods:
                | validate - Validates the GUI bundle.
                | is_valid - Checks if the GUI bundle is valid.
    '''

    @classmethod
    def validate(cls, bundle: GUIBundle) -> None:
        '''
            Validates the GUI bundle.

            :param bundle: The GUI bundle to be validated.
            :exceptions:
                | ATSValueError: The GUI bundle must be provided and have proper values.
                | ATSTypeError:  The GUI bundle must be an instance of GUIBundle and
                |                its attributes must be instances of their respective types.
        '''
        ctx: str = 'gui_bundle_validator::validate(...)'
        msg_bundle_none: str = 'the gui bundle must be provided'
        msg_bundle_istype: str = 'the gui bundle must be an instance of GUIBundle'

        not_none(bundle, ctx, msg_bundle_none)
        istype(bundle, GUIBundle, ctx, msg_bundle_istype)

        not_none(bundle.service, ctx, 'the service must be provided')
        istype(bundle.service, IService, ctx, 'the service must be an instance of IService')

        not_none(bundle.scanner, ctx, 'the scanner must be provided')
        istype(bundle.scanner, ISerialPortScanner, ctx, 'the scanner must be an instance of ISerialPortScanner')

        not_none(bundle.storage, ctx, 'the storage must be provided')
        istype(bundle.storage, IScriptStorageService, ctx, 'the storage must be an instance of IScriptStorageService')

        not_none(bundle.root, ctx, 'the root window must be provided')
        istype(bundle.root, Tk, ctx, 'the root window must be an instance of Tk')

        not_none(bundle.menu_bar, ctx, 'the menu bar must be provided')
        istype(bundle.menu_bar, IMenuBar, ctx, 'the menu bar must be an instance of IMenuBar')

        not_none(bundle.toolbar, ctx, 'the toolbar must be provided')
        istype(bundle.toolbar, IToolbar, ctx, 'the toolbar must be an instance of IToolbar')

        not_none(bundle.port_panel, ctx, 'the port panel must be provided')
        istype(bundle.port_panel, ConnectionPanel, ctx, 'the port panel must be an instance of ConnectionPanel')

        not_none(bundle.jog_panel, ctx, 'the jog panel must be provided')
        istype(bundle.jog_panel, JogPanel, ctx, 'the jog panel must be an instance of JogPanel')

        not_none(bundle.editor_panel, ctx, 'the editor panel must be provided')
        istype(bundle.editor_panel, EditorPanel, ctx, 'the editor panel must be an instance of EditorPanel')

        not_none(bundle.log_panel, ctx, 'the log panel must be provided')
        istype(bundle.log_panel, LogPanel, ctx, 'the log panel must be an instance of LogPanel')

        not_none(bundle.status_bar, ctx, 'the status bar must be provided')
        istype(bundle.status_bar, StatusBar, ctx, 'the status bar must be an instance of StatusBar')

    @classmethod
    def is_valid(cls, bundle: GUIBundle) -> bool:
        '''
            Checks if the GUI bundle is valid.

            :param bundle: The GUI bundle to be checked.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(bundle)
            return True

        except (ATSValueError, ATSTypeError):
            return False
