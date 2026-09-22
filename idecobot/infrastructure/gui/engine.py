# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Defines IDECobotGUI main graphical interface adapter coordinating the 3-tier view.
'''

from __future__ import annotations

from collections.abc import Sequence

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.stream_progress import StreamProgress
from idecobot.core.model.communication.stream_state import StreamState
from idecobot.core.service.iservice import IService
from idecobot.infrastructure.communication.iserial_port_scanner import ISerialPortScanner
from idecobot.infrastructure.gui.engine_constants import EngineConstants
from idecobot.infrastructure.gui.setup.bundle import GUIBundle
from idecobot.infrastructure.storage.iscript_storage_service import IScriptStorageService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IDECobotGUI:
    '''
        Main desktop graphical interface adapter for idecobot motion studio and DSL IDE.

        It defines:

            :attributes:
                | _bundle - Managed GUIBundle containing assembled desktop components.
                | _constants - Injected EngineConstants operational configuration.
                | _service - Core robot application service facade.
                | _scanner - Serial port scanner.
                | _storage - Script storage service.
            :methods:
                | __init__ - Initializes the IDE window and coordinates GUIBundle components.
                | get_bundle - Returns managed GUIBundle instance.
                | is_initialized - Verifies all GUI components are created.
                | start - Starts the Tkinter main event loop.
                | stop - Closes and destroys the window.
                | load_file - Loads an initial DSL script file into the editor.
                | connect_port - Connects to specified serial port.
                | disconnect_port - Disconnects from serial port.
                | run_stream - Compiles script and initiates robot streaming.
                | pause_stream - Pauses active trajectory streaming.
                | stop_stream - Stops active trajectory streaming.
                | on_stream_progress - Handles streaming telemetry from background thread.
                | append_log - Appends entry to serial monitor console.
                | on_bytecode - Handles compiled bytecode display.
                | get_version - Returns GUI adapter version string.
    '''

    _bundle: GUIBundle
    _constants: EngineConstants
    _service: IService
    _scanner: ISerialPortScanner
    _storage: IScriptStorageService

    def __init__(self, bundle: GUIBundle, constants: EngineConstants) -> None:
        '''
            Initializes the IDE window and coordinates GUIBundle components.

            :param bundle: Injected pre-assembled GUIBundle.
            :param constants: Injected EngineConstants configuration.
            :exceptions: None.
        '''
        self._bundle = bundle
        self._constants = constants
        self._service = bundle.service
        self._scanner = bundle.scanner
        self._storage = bundle.storage

    def get_bundle(self) -> GUIBundle:
        '''
            Returns the managed GUIBundle.

            :return: Assembled GUIBundle instance.
            :exceptions: None.
        '''
        return self._bundle

    def is_initialized(self) -> bool:
        '''
            Verifies all GUI components are created.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return (
            self._bundle.root is not None
            and self._bundle.editor_panel is not None
        )

    def start(self) -> None:
        '''
            Starts the Tkinter main event loop.

            :exceptions: None.
        '''
        self._bundle.root.mainloop()

    def stop(self) -> None:
        '''
            Closes and destroys the window.

            :exceptions: None.
        '''
        self._service.get_streamer().stop()
        self._service.get_controller().disconnect()
        self._bundle.root.destroy()

    def load_file(self, filepath: str) -> None:
        '''
            Loads an initial DSL script file into the editor.

            :param filepath: Path to .cobot script file.
            :exceptions: None.
        '''
        try:
            content: str = self._storage.load_script(filepath)
            self._bundle.editor_panel.set_text(content)
            self.append_log(self._constants.log_file_loaded.format(filepath=filepath))

        except (OSError, ValueError) as err:
            self.append_log(
                self._constants.log_file_error.format(filepath=filepath, err=err)
            )

    def connect_port(self, port: str, baud: int = 115200) -> bool:
        '''
            Connects to specified serial port.

            :param port: Serial device path string.
            :param baud: Communication baudrate.
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''
        connected: bool = self._service.get_controller().connect(port, baud)

        if connected:
            self._bundle.toolbar.set_connected(True)
            self.append_log(
                self._constants.log_connected.format(port=port, baud=baud)
            )

            def on_connected_settled() -> None:
                self._service.get_controller().get_transport().flush()
                self._bundle.menu_bar.get_diagnostics_handler().run_startup_diagnostics()

            self._bundle.root.after(1200, on_connected_settled)
        else:
            self._bundle.toolbar.set_connected(False)
            self.append_log(self._constants.log_connect_failed.format(port=port))

        return connected

    def disconnect_port(self) -> None:
        '''
            Disconnects from serial port.

            :exceptions: None.
        '''
        self._service.get_controller().disconnect()
        self._bundle.toolbar.set_connected(False)
        self.append_log(self._constants.log_disconnected)

    def run_stream(self) -> None:
        '''
            Compiles script and initiates robot streaming.

            :exceptions: None.
        '''
        frames: Sequence[MyCobotFrame] | None = (
            self._bundle.editor_panel.compile_code()
        )

        if not frames:
            return

        self.append_log(
            self._constants.log_stream_starting.format(count=len(frames))
        )
        started: bool = self._service.get_streamer().stream(frames)

        if not started:
            self.append_log(self._constants.log_stream_busy)

    def pause_stream(self) -> None:
        '''
            Pauses active trajectory streaming.

            :exceptions: None.
        '''
        self._service.get_streamer().pause()
        self.append_log(self._constants.log_stream_paused)

    def stop_stream(self) -> None:
        '''
            Stops active trajectory streaming.

            :exceptions: None.
        '''
        self._service.get_streamer().stop()
        self.append_log(self._constants.log_stream_stopped)

    def on_stream_progress(self, progress: StreamProgress) -> None:
        '''
            Handles streaming telemetry safely from background worker thread.

            :param progress: StreamProgress telemetry object.
            :exceptions: None.
        '''
        def update_ui() -> None:
            self._bundle.status_bar.update_progress(progress)
            self._bundle.toolbar.update_stream_state(progress.state)

            if progress.state == StreamState.STOPPED:
                self.append_log(self._constants.log_stream_completed)
            elif progress.state == StreamState.ERROR:
                self.append_log(self._constants.log_stream_error)

        self._bundle.root.after_idle(update_ui)

    def append_log(self, message: str) -> None:
        '''
            Appends entry to serial monitor console.

            :param message: Log message string.
            :exceptions: None.
        '''
        self._bundle.log_panel.append_log(message)

    def on_bytecode(self, frames: Sequence[MyCobotFrame]) -> None:
        '''
            Handles compiled bytecode display.

            :param frames: Compiled frame sequence.
            :exceptions: None.
        '''
        self._bundle.log_panel.set_bytecode(frames)

    def get_version(self) -> str:
        '''
            Returns GUI adapter version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

