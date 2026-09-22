# -*- coding: UTF-8 -*-

'''
Module
    gui_factory_test.py
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
    Unit tests for GUIFactory desktop interface assembly.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.infrastructure.gui.engine import IDECobotGUI
from idecobot.setup.bundle import IDECobotBundle
from idecobot.setup.factory import IDECobotBundleFactory
from idecobot.setup.gui_factory import GUIFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGUIFactory(TestCase):
    '''
        Test cases for GUIFactory desktop interface construction.

        It defines:

            :methods:
                | test_create_gui - Tests GUIFactory creates a valid IDECobotGUI instance.
                | test_get_version - Tests GUIFactory version string retrieval.
    '''

    def test_create_gui(self) -> None:
        '''
            Tests GUIFactory constructs and wires IDECobotGUI with domain service.
        '''
        bundle: IDECobotBundle = IDECobotBundleFactory.create_bundle()
        gui: IDECobotGUI = GUIFactory.create(service=bundle.service)
        self.assertIsNotNone(gui)
        self.assertTrue(gui.is_initialized())
        gui.get_bundle().root.destroy()
        if isinstance(bundle.gui, IDECobotGUI):
            bundle.gui.get_bundle().root.destroy()

    def test_get_version(self) -> None:
        '''
            Tests retrieval of factory version string.
        '''
        version: str = GUIFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
