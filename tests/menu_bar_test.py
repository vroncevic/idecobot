# -*- coding: UTF-8 -*-

'''
Module
    test_menu_bar.py
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
    Unit tests for MenuBar, MenuBarFactory, and MenuBarConstants.
'''

from __future__ import annotations

from tkinter import Menu, Tk
from unittest import TestCase, main

from idecobot.infrastructure.gui.menu.menu_bar import MenuBar
from idecobot.infrastructure.gui.menu.menu_bar_constants import MenuBarConstants
from idecobot.infrastructure.gui.menu.menu_bar_factory import MenuBarFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
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


class TestMenuBar(TestCase):
    '''
        Unit tests verifying MenuBarFactory assembly and MenuBar operation.

        It defines:

            :methods:
                | setUp - Initializes Tk root window and dependencies.
                | tearDown - Destroys root Tk window.
                | test_factory_creation - Verifies menu bar assembly.
                | test_new_script - Verifies new script action triggers callback.
    '''

    def setUp(self) -> None:
        '''
            Initializes Tk root window and mock dependencies before each test.
        '''
        self.root: Tk = Tk()
        self.root.withdraw()
        self.storage: MockStorage = MockStorage()
        self.constants: MenuBarConstants = MenuBarConstants()
        self.loaded_code: str = ''
        self.editor_text: str = 'move(1, 10.0, 30)'
        self.new_called: bool = False

    def tearDown(self) -> None:
        '''
            Destroys Tk root window after each test.
        '''
        self.root.destroy()

    def _create_menu_bar(self) -> MenuBar:
        return MenuBarFactory.create_menu_bar(
            root=self.root,
            storage=self.storage,
            on_load=lambda code: setattr(self, 'loaded_code', code),
            on_get=lambda: self.editor_text,
            on_new=lambda: setattr(self, 'new_called', True),
            constants=self.constants
        )

    def test_factory_creation(self) -> None:
        '''
            Verifies MenuBarFactory creates a configured MenuBar.
        '''
        bar: MenuBar = self._create_menu_bar()
        self.assertIsNotNone(bar)
        self.assertIsInstance(bar, MenuBar)
        self.assertEqual(bar.constants, self.constants)
        self.assertIsInstance(bar.menu_bar, Menu)

    def test_new_script(self) -> None:
        '''
            Verifies new_script action triggers on_new callback.
        '''
        bar: MenuBar = self._create_menu_bar()
        bar.new_script()
        self.assertTrue(self.new_called)


if __name__ == '__main__':
    main()
