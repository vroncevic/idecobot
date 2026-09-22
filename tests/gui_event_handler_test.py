# -*- coding: UTF-8 -*-

'''
Module
    gui_event_handler_test.py
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
    Unit tests for GUIEventHandler event mediator.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.infrastructure.gui.setup.gui_event_handler import GUIEventHandler
from idecobot.infrastructure.gui.setup.igui_event_target import IGUIEventTarget

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGUIEventHandler(TestCase):
    '''
    Test cases for GUIEventHandler user interaction event dispatching.

    It defines:

        :attributes:
            | _handler - Target GUIEventHandler instance under test.
            | _target_mock - Mock implementing IGUIEventTarget protocol.
        :methods:
            | setUp - Initializes fixtures before each test execution.
            | test_connect_port_without_target - Tests connect_port when target is unset.
            | test_connect_port_with_target - Tests connect_port dispatch to target.
            | test_disconnect_port_without_target - Tests disconnect_port when target is unset.
            | test_disconnect_port_with_target - Tests disconnect_port dispatch to target.
            | test_run_stream_without_target - Tests run_stream when target is unset.
            | test_run_stream_with_target - Tests run_stream dispatch to target.
            | test_pause_stream_without_target - Tests pause_stream when target is unset.
            | test_pause_stream_with_target - Tests pause_stream dispatch to target.
            | test_stop_stream_without_target - Tests stop_stream when target is unset.
            | test_stop_stream_with_target - Tests stop_stream dispatch to target.
            | test_append_log_without_target - Tests append_log when target is unset.
            | test_append_log_with_target - Tests append_log dispatch to target.
            | test_on_bytecode_without_target - Tests on_bytecode when target is unset.
            | test_on_bytecode_with_target - Tests on_bytecode dispatch to target.
            | test_get_version - Tests retrieval of component version string.
    '''

    _handler: GUIEventHandler
    _target_mock: MagicMock

    def setUp(self) -> None:
        '''
        Initializes fixtures before each test execution.
        '''
        self._handler = GUIEventHandler()
        self._target_mock = MagicMock(spec=IGUIEventTarget)

    def test_connect_port_without_target(self) -> None:
        '''
        Tests connect_port when target is unset.
        '''
        self.assertFalse(self._handler.connect_port('/dev/ttyUSB0', 115200))

    def test_connect_port_with_target(self) -> None:
        '''
        Tests connect_port dispatch to target.
        '''
        self._target_mock.connect_port.return_value = True
        self._handler.set_target(self._target_mock)

        result: bool = self._handler.connect_port('/dev/ttyACM0', 9600)
        self.assertTrue(result)
        self._target_mock.connect_port.assert_called_once_with('/dev/ttyACM0', 9600)

    def test_disconnect_port_without_target(self) -> None:
        '''
        Tests disconnect_port when target is unset.
        '''
        self._handler.disconnect_port()

    def test_disconnect_port_with_target(self) -> None:
        '''
        Tests disconnect_port dispatch to target.
        '''
        self._handler.set_target(self._target_mock)
        self._handler.disconnect_port()
        self._target_mock.disconnect_port.assert_called_once()

    def test_run_stream_without_target(self) -> None:
        '''
        Tests run_stream when target is unset.
        '''
        self._handler.run_stream()

    def test_run_stream_with_target(self) -> None:
        '''
        Tests run_stream dispatch to target.
        '''
        self._handler.set_target(self._target_mock)
        self._handler.run_stream()
        self._target_mock.run_stream.assert_called_once()

    def test_pause_stream_without_target(self) -> None:
        '''
        Tests pause_stream when target is unset.
        '''
        self._handler.pause_stream()

    def test_pause_stream_with_target(self) -> None:
        '''
        Tests pause_stream dispatch to target.
        '''
        self._handler.set_target(self._target_mock)
        self._handler.pause_stream()
        self._target_mock.pause_stream.assert_called_once()

    def test_stop_stream_without_target(self) -> None:
        '''
        Tests stop_stream when target is unset.
        '''
        self._handler.stop_stream()

    def test_stop_stream_with_target(self) -> None:
        '''
        Tests stop_stream dispatch to target.
        '''
        self._handler.set_target(self._target_mock)
        self._handler.stop_stream()
        self._target_mock.stop_stream.assert_called_once()

    def test_append_log_without_target(self) -> None:
        '''
        Tests append_log when target is unset.
        '''
        self._handler.append_log('Info log')

    def test_append_log_with_target(self) -> None:
        '''
        Tests append_log dispatch to target.
        '''
        self._handler.set_target(self._target_mock)
        self._handler.append_log('Target log message')
        self._target_mock.append_log.assert_called_once_with('Target log message')

    def test_on_bytecode_without_target(self) -> None:
        '''
        Tests on_bytecode when target is unset.
        '''
        self._handler.on_bytecode([])

    def test_on_bytecode_with_target(self) -> None:
        '''
        Tests on_bytecode dispatch to target.
        '''
        frames = [MyCobotFrame(cmd_id=0x22, payload=b'\x00', delay_after_sec=0.1)]
        self._handler.set_target(self._target_mock)
        self._handler.on_bytecode(frames)
        self._target_mock.on_bytecode.assert_called_once_with(frames)

    def test_get_version(self) -> None:
        '''
        Tests retrieval of component version string.
        '''
        self.assertEqual(self._handler.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
