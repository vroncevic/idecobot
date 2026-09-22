# -*- coding: UTF-8 -*-

'''
Module
    test_gui_engine.py
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
    Unit tests for IDECobotGUI, EngineConstants, and GUIBundleFactoryConstants.
'''

from __future__ import annotations

from unittest import TestCase, main

from idecobot.infrastructure.gui.engine import IDECobotGUI
from idecobot.infrastructure.gui.engine_constants import EngineConstants
from idecobot.infrastructure.gui.setup.gui_bundle_factory_constants import (
    GUIBundleFactoryConstants,
)
from idecobot.infrastructure.gui.setup.gui_event_handler import GUIEventHandler
from idecobot.setup.bundle import IDECobotBundle
from idecobot.setup.factory import IDECobotBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGUIEngine(TestCase):
    '''
        Unit tests for IDECobotGUI desktop coordinator and its constants.

        It defines:

            :methods:
                | setUp - Initializes bundle and GUI coordinator for tests.
                | tearDown - Cleans up Tk window after tests.
                | test_engine_constants_defaults - Verifies EngineConstants default parameters.
                | test_gui_factory_constants_defaults - Verifies GUIBundleFactoryConstants defaults.
                | test_gui_initialization - Verifies IDECobotGUI initializes and coordinates panels.
                | test_gui_logging_and_bytecode - Verifies log and bytecode dispatching.
                | test_direct_gui_dependency_injection - Verifies direct DI injection of bundle and constants.
                | test_gui_event_handler_dispatch - Verifies GUIEventHandler mediator dispatching.
    '''

    def setUp(self) -> None:
        '''
            Initializes IDECobotBundle before each test.
        '''
        self.bundle: IDECobotBundle = IDECobotBundleFactory.create_bundle()
        self.gui: IDECobotGUI = self.bundle.gui
        self.gui.get_bundle().root.withdraw()

    def tearDown(self) -> None:
        '''
            Destroys root Tk application window after each test.
        '''
        self.gui.get_bundle().root.destroy()

    def test_engine_constants_defaults(self) -> None:
        '''
            Verifies EngineConstants baseline baudrate and log templates.
        '''
        constants: EngineConstants = EngineConstants()
        self.assertEqual(constants.default_baudrate, 115200)
        self.assertIn('{port}', constants.log_connected)
        self.assertIn('{count}', constants.log_stream_starting)

    def test_gui_factory_constants_defaults(self) -> None:
        '''
            Verifies GUIBundleFactoryConstants sizing, weights, and titles.
        '''
        constants: GUIBundleFactoryConstants = GUIBundleFactoryConstants()
        self.assertEqual(constants.min_width, 1050)
        self.assertEqual(constants.min_height, 720)
        self.assertEqual(constants.weight_top, 2)
        self.assertEqual(constants.weight_mid, 4)
        self.assertEqual(constants.weight_bot, 3)

    def test_gui_initialization(self) -> None:
        '''
            Verifies IDECobotGUI reports operational initialization.
        '''
        self.assertTrue(self.gui.is_initialized())
        self.assertIsNotNone(self.gui.get_bundle())
        self.assertEqual(self.gui.get_version(), '1.0.3')

    def test_gui_logging_and_bytecode(self) -> None:
        '''
            Verifies append_log and on_bytecode execution.
        '''
        self.gui.append_log('Test info message')
        self.gui.on_bytecode([])
        self.gui.disconnect_port()

    def test_direct_gui_dependency_injection(self) -> None:
        '''
            Verifies direct DI injection of bundle and constants into IDECobotGUI.
        '''
        constants: EngineConstants = EngineConstants()
        direct_gui: IDECobotGUI = IDECobotGUI(
            bundle=self.gui.get_bundle(),
            constants=constants
        )
        self.assertTrue(direct_gui.is_initialized())
        self.assertEqual(direct_gui.get_version(), '1.0.3')
        self.assertIs(direct_gui.get_bundle(), self.gui.get_bundle())


    def test_gui_event_handler_dispatch(self) -> None:
        '''
            Verifies GUIEventHandler mediator dispatching with and without target.
        '''
        handler: GUIEventHandler = GUIEventHandler()
        self.assertFalse(handler.connect_port('COM1', 115200))
        handler.disconnect_port()
        handler.run_stream()
        handler.pause_stream()
        handler.stop_stream()
        handler.append_log('No target test')
        handler.on_bytecode([])

        handler.set_target(self.gui)
        handler.append_log('Target wired test')
        handler.on_bytecode([])
        handler.disconnect_port()


if __name__ == '__main__':
    main()
