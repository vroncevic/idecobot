# -*- coding: UTF-8 -*-

'''
Module
    test_connection_panel.py
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
    Unit tests for ConnectionPanel and ConnectionPanelFactory.
'''

from __future__ import annotations

from tkinter import Frame, Tk
from unittest import TestCase, main

from idecobot.infrastructure.gui.stream.connection_constants import (
    ConnectionConstants,
)
from idecobot.infrastructure.gui.stream.connection_panel import ConnectionPanel
from idecobot.infrastructure.gui.stream.connection_panel_factory import (
    ConnectionPanelFactory,
)
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.theme.font_config import FontConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockScanner:
    '''
        Mock serial port scanner implementing structural subtyping for ISerialPortScanner.
    '''

    def __init__(self, ports: list[str] | None = None) -> None:
        self._ports: list[str] = ports if ports is not None else ['/dev/ttyUSB0', '/dev/ttyUSB1']

    def scan_ports(self) -> list[str]:
        '''
            Returns mock list of ports.

            :return: List of port strings.
        '''
        return list(self._ports)


class TestConnectionPanel(TestCase):
    '''
        Unit tests verifying ConnectionPanelFactory assembly and ConnectionPanel operations.

        It defines:

            :methods:
                | setUp - Initializes root Tk window and dependencies.
                | tearDown - Destroys root Tk window.
                | test_factory_creation - Verifies panel assembly by ConnectionPanelFactory.
                | test_port_selection - Tests port scanning and programmatic selection.
                | test_toggle_connection - Tests connect/disconnect button event cycle.
                | test_set_connected_visual_states - Tests visual state toggles.
    '''

    def setUp(self) -> None:
        '''
            Sets up Tkinter root and dependencies before each test.
        '''
        self.root: Tk = Tk()
        self.root.withdraw()
        self.parent: Frame = Frame(self.root)
        self.scanner: MockScanner = MockScanner()
        self.palette: ColorPalette = ColorPalette()
        self.fonts: FontConfig = FontConfig()
        self.constants: ConnectionConstants = ConnectionConstants()
        self.connected_args: list[tuple[str, int]] = []
        self.disconnected_called: bool = False

    def tearDown(self) -> None:
        '''
            Destroys Tkinter root after each test.
        '''
        self.root.destroy()

    def _on_connect(self, port: str, baud: int) -> bool:
        self.connected_args.append((port, baud))
        return True

    def _on_disconnect(self) -> None:
        self.disconnected_called = True

    def test_factory_creation(self) -> None:
        '''
            Tests that ConnectionPanelFactory produces a correctly wired ConnectionPanel.
        '''
        panel: ConnectionPanel = ConnectionPanelFactory.create_connection_panel(
            parent=self.parent,
            scanner=self.scanner,
            on_connect=self._on_connect,
            on_disconnect=self._on_disconnect,
            palette=self.palette,
            fonts=self.fonts,
            constants=self.constants
        )
        self.assertIsNotNone(panel)
        self.assertIsInstance(panel, ConnectionPanel)
        self.assertEqual(panel.constants, self.constants)
        self.assertFalse(panel.is_connected)
        self.assertEqual(panel.get_selected_port(), '/dev/ttyUSB0')

    def test_port_selection(self) -> None:
        '''
            Tests selecting port and getting baudrate.
        '''
        panel: ConnectionPanel = ConnectionPanelFactory.create_connection_panel(
            parent=self.parent,
            scanner=self.scanner,
            on_connect=self._on_connect,
            on_disconnect=self._on_disconnect,
            palette=self.palette,
            fonts=self.fonts,
            constants=self.constants
        )
        panel.set_port('/dev/ttyUSB1')
        self.assertEqual(panel.get_selected_port(), '/dev/ttyUSB1')
        self.assertEqual(panel.get_selected_baudrate(), int(self.constants.default_baudrate))

    def test_toggle_connection(self) -> None:
        '''
            Tests toggling connection on and off.
        '''
        panel: ConnectionPanel = ConnectionPanelFactory.create_connection_panel(
            parent=self.parent,
            scanner=self.scanner,
            on_connect=self._on_connect,
            on_disconnect=self._on_disconnect,
            palette=self.palette,
            fonts=self.fonts,
            constants=self.constants
        )
        panel.toggle_connection()
        self.assertTrue(panel.is_connected)
        self.assertEqual(len(self.connected_args), 1)
        self.assertEqual(self.connected_args[0][0], '/dev/ttyUSB0')

        panel.toggle_connection()
        self.assertFalse(panel.is_connected)
        self.assertTrue(self.disconnected_called)

    def test_set_connected_visual_states(self) -> None:
        '''
            Tests direct state setting on ConnectionPanel.
        '''
        panel: ConnectionPanel = ConnectionPanelFactory.create_connection_panel(
            parent=self.parent,
            scanner=self.scanner,
            on_connect=self._on_connect,
            on_disconnect=self._on_disconnect,
            palette=self.palette,
            fonts=self.fonts,
            constants=self.constants
        )
        panel.set_connected(True)
        self.assertTrue(panel.is_connected)
        panel.set_connected(False)
        self.assertFalse(panel.is_connected)


if __name__ == '__main__':
    main()
