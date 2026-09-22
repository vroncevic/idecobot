# -*- coding: UTF-8 -*-

'''
Module
    test_toolbar.py
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
    Unit tests for Toolbar, ToolbarFactory, and ToolbarConstants.
'''

from __future__ import annotations

from tkinter import Frame, Tk
from unittest import TestCase, main

from idecobot.core.model.communication.stream_state import StreamState
from idecobot.infrastructure.gui.theme.color_palette import ColorPalette
from idecobot.infrastructure.gui.toolbar.itoolbar import IToolbar
from idecobot.infrastructure.gui.toolbar.toolbar import Toolbar
from idecobot.infrastructure.gui.toolbar.toolbar_constants import ToolbarConstants
from idecobot.infrastructure.gui.toolbar.toolbar_factory import ToolbarFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolbar(TestCase):
    '''
        Unit tests verifying ToolbarFactory assembly and Toolbar operation states.

        It defines:

            :methods:
                | setUp - Initializes Tk root window and dependencies.
                | tearDown - Destroys root Tk window.
                | test_factory_creation - Tests Toolbar creation via ToolbarFactory.
                | test_set_connected_state - Tests button state changes on connection toggle.
                | test_update_stream_state - Tests stream state lifecycle changes.
    '''

    def setUp(self) -> None:
        '''
            Initializes Tk root window and tracking callbacks before each test.
        '''
        self.root: Tk = Tk()
        self.root.withdraw()
        self.parent: Frame = Frame(self.root)
        self.palette: ColorPalette = ColorPalette()
        self.constants: ToolbarConstants = ToolbarConstants()
        self.calls: list[str] = []

    def tearDown(self) -> None:
        '''
            Destroys Tk root window after each test.
        '''
        self.root.destroy()

    def create_toolbar(self) -> Toolbar:
        return ToolbarFactory.create_toolbar(
            parent=self.parent,
            on_run=lambda: self.calls.append('run'),
            on_pause=lambda: self.calls.append('pause'),
            on_stop=lambda: self.calls.append('stop'),
            on_home=lambda: self.calls.append('home'),
            on_relax=lambda: self.calls.append('relax'),
            on_clear_log=lambda: self.calls.append('clear_log'),
            palette=self.palette,
            constants=self.constants
        )

    def test_factory_creation(self) -> None:
        '''
            Verifies ToolbarFactory produces a valid Toolbar with injected constants.
        '''
        toolbar: Toolbar = self.create_toolbar()
        self.assertIsNotNone(toolbar)
        self.assertIsInstance(toolbar, Toolbar)
        self.assertIsInstance(toolbar, IToolbar)
        self.assertEqual(toolbar.constants, self.constants)
        self.assertIsNotNone(toolbar.get_frame())
        self.assertEqual(toolbar.get_version(), '1.0.2')

    def test_set_connected_state(self) -> None:
        '''
            Verifies that toolbar controls update based on connection status.
        '''
        toolbar: Toolbar = self.create_toolbar()
        toolbar.set_connected(True)
        toolbar.set_connected(False)
        self.assertIsNotNone(toolbar)

    def test_update_stream_state(self) -> None:
        '''
            Verifies button state transitions during streaming lifecycle.
        '''
        toolbar: Toolbar = self.create_toolbar()
        toolbar.update_stream_state(StreamState.STREAMING)
        toolbar.update_stream_state(StreamState.PAUSED)
        toolbar.update_stream_state(StreamState.STOPPED)
        self.assertIsNotNone(toolbar)


if __name__ == '__main__':
    main()
