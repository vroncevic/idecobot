# -*- coding: UTF-8 -*-

'''
Module
    gui_factory.py
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
    Defines GUIFactory for assembling and initializing the complete IDECobotGUI application.
'''

from __future__ import annotations

from tkinter import Tk

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.communication.serial_port_scanner import SerialPortScanner
from idecobot.infrastructure.gui.engine import IDECobotGUI
from idecobot.infrastructure.gui.engine_constants import EngineConstants
from idecobot.infrastructure.gui.setup.bundle import GUIBundle
from idecobot.infrastructure.gui.setup.factory import GUIBundleFactory
from idecobot.infrastructure.gui.setup.gui_bundle_factory_constants import GUIBundleFactoryConstants
from idecobot.infrastructure.gui.setup.gui_event_handler import GUIEventHandler
from idecobot.infrastructure.gui.setup.keys import GUIBundleKeys
from idecobot.infrastructure.storage.script_storage_service import ScriptStorageService
from idecobot.infrastructure.storage.storage_constants import StorageConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GUIFactory:
    '''
        Factory assembling and configuring the desktop GUI application adapter.

        It defines:

            :methods:
                | create - Creates and wires IDECobotGUI with event handlers and services.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, service: IService) -> IDECobotGUI:
        '''
            Builds and configures the desktop graphical user interface.

            :param service: Central idecobot engine domain service.
            :return: Fully configured and wired IDECobotGUI instance.
            :exceptions: None.
        '''
        handler: GUIEventHandler = GUIEventHandler()
        root: Tk = Tk()
        constants: GUIBundleFactoryConstants = GUIBundleFactoryConstants()
        bundle: GUIBundle = GUIBundleFactory.create_bundle(
            options={
                GUIBundleKeys.OPTION_SERVICE: service,
                GUIBundleKeys.OPTION_SCANNER: SerialPortScanner(),
                GUIBundleKeys.OPTION_STORAGE: ScriptStorageService(
                    constants=StorageConstants()
                )
            },
            handler=handler,
            root=root,
            constants=constants
        )
        gui: IDECobotGUI = IDECobotGUI(bundle=bundle, constants=EngineConstants())
        handler.set_target(gui)

        return gui

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: The factory version string.
            :exceptions: None.
        '''
        return __version__
