# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory for creating the GUI bundle with strict dependency injection.
'''

from __future__ import annotations

from tkinter import BOTH, BOTTOM, Frame, TclError, Tk, TOP, VERTICAL, X
from tkinter.ttk import PanedWindow

from idecobot.core.service.iservice import IService
from idecobot.infrastructure.communication.iserial_port_scanner import ISerialPortScanner
from idecobot.infrastructure.gui.editor.editor_constants import EditorConstants
from idecobot.infrastructure.gui.editor.editor_panel import EditorPanel
from idecobot.infrastructure.gui.editor.editor_panel_factory import EditorPanelFactory
from idecobot.infrastructure.gui.jog.jog_constants import JogConstants
from idecobot.infrastructure.gui.jog.jog_coordinator import JogCoordinator
from idecobot.infrastructure.gui.jog.jog_panel import JogPanel
from idecobot.infrastructure.gui.jog.jog_panel_factory import JogPanelFactory
from idecobot.infrastructure.gui.log.log_panel import LogPanel
from idecobot.infrastructure.gui.log.log_panel_factory import LogPanelFactory
from idecobot.infrastructure.gui.menu.menu_bar import MenuBar
from idecobot.infrastructure.gui.menu.menu_bar_constants import MenuBarConstants
from idecobot.infrastructure.gui.menu.menu_bar_factory import MenuBarFactory
from idecobot.infrastructure.gui.setup.bundle import GUIBundle
from idecobot.infrastructure.gui.setup.dependencies import GUIBundleDependencies
from idecobot.infrastructure.gui.setup.gui_bundle_factory_constants import GUIBundleFactoryConstants
from idecobot.infrastructure.gui.setup.igui_event_handler import IGUIEventHandler
from idecobot.infrastructure.gui.setup.keys import GUIBundleKeys
from idecobot.infrastructure.gui.setup.options import GUIBundleOptions
from idecobot.infrastructure.gui.setup.opt_validator import GUIBundleOptionsValidator
from idecobot.infrastructure.gui.setup.registry import GUIBundleRegistry
from idecobot.infrastructure.gui.stream.connection_constants import ConnectionConstants
from idecobot.infrastructure.gui.stream.connection_panel import ConnectionPanel
from idecobot.infrastructure.gui.stream.connection_panel_factory import ConnectionPanelFactory
from idecobot.infrastructure.gui.stream.status_bar import StatusBar
from idecobot.infrastructure.gui.stream.status_bar_constants import StatusBarConstants
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.theme.font_config import FontConfig
from idecobot.infrastructure.gui.theme.theme import ThemeManager
from idecobot.infrastructure.gui.theme.theme_constants import ThemeConstants
from idecobot.infrastructure.gui.toolbar.toolbar import Toolbar
from idecobot.infrastructure.gui.toolbar.toolbar_constants import ToolbarConstants
from idecobot.infrastructure.gui.toolbar.toolbar_factory import ToolbarFactory
from idecobot.infrastructure.storage.iscript_storage_service import IScriptStorageService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GUIBundleFactory:
    '''
        Factory for assembling GUI desktop panels with pure dependency injection.

        It defines:

            :methods:
                | create_bundle - Creates assembled GUIBundle with fully wired components.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_bundle(
        cls,
        options: GUIBundleOptions,
        handler: IGUIEventHandler,
        root: Tk | None = None,
        constants: GUIBundleFactoryConstants | None = None
    ) -> GUIBundle:
        '''
            Creates assembled GUIBundle with fully wired components.

            :param options: Validated GUI options mapping.
            :param handler: GUI event delegate implementing IGUIEventHandler.
            :param root: Optional parent Tk window.
            :param constants: Optional GUIBundleFactoryConstants configuration.
            :return: Assembled and validated GUIBundle instance.
            :exceptions:
                | ATSValueError: If options or dependencies are invalid.
                | ATSTypeError: If option attributes violate required types.
        '''
        GUIBundleOptionsValidator.validate(options)
        bundle_constants: GUIBundleFactoryConstants = (
            constants if constants is not None else GUIBundleFactoryConstants()
        )

        service: IService = options[GUIBundleKeys.OPTION_SERVICE]
        scanner: ISerialPortScanner = options[GUIBundleKeys.OPTION_SCANNER]
        storage: IScriptStorageService = options[GUIBundleKeys.OPTION_STORAGE]

        root_win: Tk = root if root is not None else Tk()
        root_win.title(bundle_constants.window_title)
        sw: int = root_win.winfo_screenwidth()
        sh: int = root_win.winfo_screenheight()
        root_win.geometry(f'{sw}x{sh}+0+0')
        root_win.minsize(bundle_constants.min_width, bundle_constants.min_height)

        palette: ColorPalette = ColorPalette()
        fonts: FontConfig = FontConfig()
        theme_constants: ThemeConstants = ThemeConstants()
        ThemeManager.apply_theme(
            root=root_win,
            palette=palette,
            fonts=fonts,
            constants=theme_constants
        )

        try:
            root_win.attributes(bundle_constants.attr_zoomed, True)
        except TclError:
            try:
                root_win.state(bundle_constants.state_zoomed)
            except TclError:
                pass

        connection_constants: ConnectionConstants = ConnectionConstants()
        toolbar_constants: ToolbarConstants = ToolbarConstants()
        jog_constants: JogConstants = JogConstants()
        jog_coordinator: JogCoordinator = JogCoordinator(
            controller=service.get_controller(),
            bounds=service.get_bounds(),
            constants=jog_constants,
            on_log=handler.append_log
        )
        editor_constants: EditorConstants = EditorConstants()
        status_bar_constants: StatusBarConstants = StatusBarConstants()
        menu_bar_constants: MenuBarConstants = MenuBarConstants()

        paned: PanedWindow = PanedWindow(root_win, orient=VERTICAL)
        paned.pack(
            fill=BOTH,
            expand=True,
            padx=bundle_constants.paned_padx,
            pady=bundle_constants.paned_pady
        )

        top_frame: Frame = Frame(paned)
        port_panel: ConnectionPanel = ConnectionPanelFactory.create_connection_panel(
            parent=top_frame,
            scanner=scanner,
            on_connect=handler.connect_port,
            on_disconnect=handler.disconnect_port,
            palette=palette,
            fonts=fonts,
            constants=connection_constants
        )
        port_panel.frame.pack(fill=X, side=TOP)

        jog_panel: JogPanel = JogPanelFactory.create_jog_panel(
            parent=top_frame,
            coordinator=jog_coordinator,
            palette=palette,
            constants=jog_constants
        )
        paned.add(top_frame, weight=bundle_constants.weight_top)

        mid_frame: Frame = Frame(paned)
        editor_panel: EditorPanel = EditorPanelFactory.create_editor_panel(
            parent=mid_frame,
            dsl_service=service.get_dsl_service(),
            on_bytecode=handler.on_bytecode,
            on_log=handler.append_log,
            palette=palette,
            fonts=fonts,
            constants=editor_constants
        )
        paned.add(mid_frame, weight=bundle_constants.weight_mid)

        bot_frame: Frame = Frame(paned)
        log_panel: LogPanel = LogPanelFactory.create_log_panel(
            parent=bot_frame,
            palette=palette,
            fonts=fonts
        )
        status_bar: StatusBar = StatusBar(
            parent=bot_frame,
            palette=palette,
            fonts=fonts,
            constants=status_bar_constants
        )
        status_bar.frame.pack(fill=X, side=BOTTOM)
        paned.add(bot_frame, weight=bundle_constants.weight_bot)

        def on_home_cmd() -> None:
            service.get_controller().home(bundle_constants.default_home_speed)

        def on_relax_cmd() -> None:
            service.get_controller().power(False)

        toolbar: Toolbar = ToolbarFactory.create_toolbar(
            parent=root_win,
            on_run=handler.run_stream,
            on_pause=handler.pause_stream,
            on_stop=handler.stop_stream,
            on_home=on_home_cmd,
            on_relax=on_relax_cmd,
            on_clear_log=log_panel.clear,
            palette=palette,
            constants=toolbar_constants
        )

        menu_bar: MenuBar = MenuBarFactory.create_menu_bar(
            root=root_win,
            storage=storage,
            on_load=lambda code: editor_panel.set_text(code),
            on_get=lambda: editor_panel.get_text(),
            on_new=lambda: editor_panel.clear(),
            constants=menu_bar_constants
        )

        dependencies: GUIBundleDependencies = {
            GUIBundleKeys.DEPENDENCY_SERVICE: service,
            GUIBundleKeys.DEPENDENCY_SCANNER: scanner,
            GUIBundleKeys.DEPENDENCY_STORAGE: storage,
            GUIBundleKeys.DEPENDENCY_ROOT: root_win,
            GUIBundleKeys.DEPENDENCY_MENU_BAR: menu_bar,
            GUIBundleKeys.DEPENDENCY_TOOLBAR: toolbar,
            GUIBundleKeys.DEPENDENCY_PORT_PANEL: port_panel,
            GUIBundleKeys.DEPENDENCY_JOG_PANEL: jog_panel,
            GUIBundleKeys.DEPENDENCY_EDITOR_PANEL: editor_panel,
            GUIBundleKeys.DEPENDENCY_LOG_PANEL: log_panel,
            GUIBundleKeys.DEPENDENCY_STATUS_BAR: status_bar
        }

        return GUIBundleRegistry.create_bundle(dependencies)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version.

            :return: The factory version string.
            :exceptions: None.
        '''
        return __version__
