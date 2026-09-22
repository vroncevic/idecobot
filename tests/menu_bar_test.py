# -*- coding: UTF-8 -*-

'''
Module
    menu_bar_test.py
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
    Unit tests for MenuBar, MenuBarFactory, and decomposed domain menu handlers.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import Menu, Tk
from unittest import TestCase, main

from idecobot.infrastructure.gui.menu.idiagnostics_menu_handler import IDiagnosticsMenuHandler
from idecobot.infrastructure.gui.menu.ifile_menu_handler import IFileMenuHandler
from idecobot.infrastructure.gui.menu.ihelp_menu_handler import IHelpMenuHandler
from idecobot.infrastructure.gui.menu.imenu_bar import IMenuBar
from idecobot.infrastructure.gui.menu.menu_bar import MenuBar
from idecobot.infrastructure.gui.menu.menu_bar_constants import MenuBarConstants
from idecobot.infrastructure.gui.menu.menu_bar_factory import MenuBarFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockStorage:
    '''
    Mock script storage service for MenuBar testing.
    '''

    def __init__(self) -> None:
        self.saved_scripts: dict[str, str] = {}

    def load_script(self, path: str) -> str:
        '''
        Loads script from memory.
        '''
        return self.saved_scripts.get(path, '')

    def save_script(self, path: str, content: str) -> bool:
        '''
        Saves script to memory.
        '''
        self.saved_scripts[path] = content
        return True


class MockDiagnosticsCoordinator:
    '''
    Mock diagnostics coordinator simulating telemetry queries and commands.
    '''

    def get_startup_summary(self) -> Sequence[str]:
        '''
        Returns simulated startup summary.
        '''
        return ('link ok', 'angles ok', 'coords ok', 'temps ok', 'volts ok')

    def diagnose_angles(self) -> str:
        '''
        Returns simulated angles.
        '''
        return 'angles ok'

    def diagnose_coords(self) -> str:
        '''
        Returns simulated coords.
        '''
        return 'coords ok'

    def diagnose_temperatures(self) -> str:
        '''
        Returns simulated temps.
        '''
        return 'temps ok'

    def diagnose_voltages(self) -> str:
        '''
        Returns simulated voltages.
        '''
        return 'volts ok'

    def diagnose_link(self) -> str:
        '''
        Returns simulated link responsiveness.
        '''
        return 'link ok'

    def re_enable_power(self) -> str:
        '''
        Returns simulated power enable response.
        '''
        return 'power ok'

    def release_servos(self) -> str:
        '''
        Returns simulated servo release response.
        '''
        return 'release ok'

    def get_version(self) -> str:
        '''
        Returns coordinator version.
        '''
        return '1.0.3'


class TestMenuBar(TestCase):
    '''
    Unit tests verifying MenuBarFactory assembly, domain handlers, and MenuBar operation.

    It defines:

        :methods:
            | setUp - Initializes Tk root window and dependencies.
            | tearDown - Destroys root Tk window.
            | create_menu_bar - Factory helper creating MenuBar fixture.
            | test_factory_creation - Verifies menu bar assembly and protocol compliance.
            | test_file_handler_actions - Verifies file operations delegation.
            | test_diagnostics_handler_actions - Verifies diagnostics queries and logging.
            | test_help_handler_actions - Verifies help and about dialog handlers.
    '''

    def setUp(self) -> None:
        '''
        Initializes Tk root window and mock dependencies before each test.
        '''
        self.root: Tk = Tk()
        self.root.withdraw()
        self.storage: MockStorage = MockStorage()
        self.diagnostics: MockDiagnosticsCoordinator = MockDiagnosticsCoordinator()
        self.constants: MenuBarConstants = MenuBarConstants()
        self.workspace_dir: str = '/tmp/test_workspace'
        self.loaded_code: str = ''
        self.editor_text: str = 'move(1, 10.0, 30)'
        self.new_called: bool = False
        self.logged_messages: list[str] = []

    def tearDown(self) -> None:
        '''
        Destroys Tk root window after each test.
        '''
        self.root.destroy()

    def create_menu_bar(self) -> MenuBar:
        '''
        Creates assembled MenuBar fixture.
        '''
        return MenuBarFactory.create_menu_bar(
            root=self.root,
            storage=self.storage,
            on_load=lambda code: setattr(self, 'loaded_code', code),
            on_get=lambda: self.editor_text,
            on_new=lambda: setattr(self, 'new_called', True),
            diagnostics=self.diagnostics,
            on_log=lambda msg: self.logged_messages.append(msg),
            constants=self.constants,
            workspace_dir=self.workspace_dir
        )

    def test_factory_creation(self) -> None:
        '''
        Verifies MenuBarFactory creates a configured MenuBar satisfying protocols.
        '''
        bar: MenuBar = self.create_menu_bar()
        self.assertIsNotNone(bar)
        self.assertIsInstance(bar, MenuBar)
        self.assertIsInstance(bar, IMenuBar)
        self.assertIsInstance(bar.get_file_handler(), IFileMenuHandler)
        self.assertIsInstance(bar.get_diagnostics_handler(), IDiagnosticsMenuHandler)
        self.assertIsInstance(bar.get_help_handler(), IHelpMenuHandler)
        self.assertEqual(bar.constants, self.constants)
        self.assertIsInstance(bar.menu_bar, Menu)
        self.assertEqual(bar.get_version(), '1.0.3')

    def test_file_handler_actions(self) -> None:
        '''
        Verifies file handler operations (new_script, save, version).
        '''
        bar: MenuBar = self.create_menu_bar()
        bar.new_script()
        self.assertTrue(self.new_called)
        self.assertEqual(bar.get_file_handler().get_version(), '1.0.3')

    def test_diagnostics_handler_actions(self) -> None:
        '''
        Verifies diagnostics menu actions dispatch and log results properly.
        '''
        bar: MenuBar = self.create_menu_bar()
        diag_handler = bar.get_diagnostics_handler()

        diag_handler.diagnose_link()
        self.assertIn('link ok', self.logged_messages)

        diag_handler.diagnose_angles()
        self.assertIn('angles ok', self.logged_messages)

        diag_handler.diagnose_coords()
        self.assertIn('coords ok', self.logged_messages)

        diag_handler.diagnose_temperatures()
        self.assertIn('temps ok', self.logged_messages)

        diag_handler.diagnose_voltages()
        self.assertIn('volts ok', self.logged_messages)

        diag_handler.diagnose_power_on()
        self.assertIn('power ok', self.logged_messages)

        diag_handler.diagnose_release_servos()
        self.assertIn('release ok', self.logged_messages)

        diag_handler.run_startup_diagnostics()
        self.assertEqual(len(self.logged_messages), 7 + 5)
        self.assertEqual(diag_handler.get_version(), '1.0.3')

    def test_help_handler_actions(self) -> None:
        '''
        Verifies help handler version and accessor.
        '''
        bar: MenuBar = self.create_menu_bar()
        help_handler = bar.get_help_handler()
        self.assertEqual(help_handler.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
