# -*- coding: UTF-8 -*-

'''
Module
    serial_transport_test.py
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
    Unit tests for SerialTransport hardware communication channel.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from serial import SerialException

from idecobot.infrastructure.communication.transport.serial_transport import SerialTransport
from idecobot.infrastructure.communication.transport.transport_constants import TransportConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSerialTransport(TestCase):
    '''
    Test cases for SerialTransport physical serial channel operations.

    It defines:

        :attributes:
            | _constants - Injected TransportConstants configuration settings.
            | _transport - Target SerialTransport instance under test.
        :methods:
            | setUp - Initializes fixtures before each test execution.
            | test_init_defaults - Tests initial properties and defaults.
            | test_configure - Tests updating port path and communication baudrate.
            | test_open_success - Tests successful port opening.
            | test_open_serial_exception - Tests handling SerialException on open.
            | test_open_os_error - Tests handling OSError on open.
            | test_close_when_open - Tests closing active connection.
            | test_close_exception_handled - Tests handling exceptions during close.
            | test_close_when_not_open - Tests close call when disconnected.
            | test_write_when_not_open - Tests write when connection is closed.
            | test_write_success - Tests transmitting data over serial.
            | test_write_serial_exception - Tests handling write failure.
            | test_read_when_not_open - Tests reading data when connection is closed.
            | test_read_success - Tests receiving byte payload from serial.
            | test_read_serial_exception - Tests handling read failure.
            | test_flush_when_open - Tests flushing communication buffers.
            | test_flush_exception_handled - Tests handling flush failure.
            | test_flush_when_not_open - Tests flush call when disconnected.
            | test_get_version - Tests retrieval of component version string.
    '''

    _constants: TransportConstants
    _transport: SerialTransport

    def setUp(self) -> None:
        '''
        Initializes fixtures before each test execution.
        '''
        self._constants = TransportConstants()
        self._transport = SerialTransport(self._constants)

    def test_init_defaults(self) -> None:
        '''
        Tests initial properties and defaults.
        '''
        self.assertFalse(self._transport.is_open())

    def test_configure(self) -> None:
        '''
        Tests updating port path and communication baudrate.
        '''
        self._transport.configure('/dev/ttyUSB1', 9600)
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_inst: MagicMock = MagicMock()
            mock_inst.is_open = True
            mock_serial_cls.return_value = mock_inst

            self.assertTrue(self._transport.open())
            mock_serial_cls.assert_called_once_with(
                port='/dev/ttyUSB1',
                baudrate=9600,
                timeout=self._constants.default_timeout
            )

    def test_open_success(self) -> None:
        '''
        Tests successful port opening.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_inst: MagicMock = MagicMock()
            mock_inst.is_open = True
            mock_serial_cls.return_value = mock_inst

            result: bool = self._transport.open()
            self.assertTrue(result)
            self.assertTrue(self._transport.is_open())

    def test_open_serial_exception(self) -> None:
        '''
        Tests handling SerialException on open.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_serial_cls.side_effect = SerialException('Device busy')

            result: bool = self._transport.open()
            self.assertFalse(result)
            self.assertFalse(self._transport.is_open())

    def test_open_os_error(self) -> None:
        '''
        Tests handling OSError on open.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_serial_cls.side_effect = OSError('Permission denied')

            result: bool = self._transport.open()
            self.assertFalse(result)
            self.assertFalse(self._transport.is_open())

    def test_close_when_open(self) -> None:
        '''
        Tests closing active connection.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_inst: MagicMock = MagicMock()
            mock_inst.is_open = True
            mock_serial_cls.return_value = mock_inst

            self._transport.open()
            self._transport.close()
            mock_inst.close.assert_called_once()
            self.assertFalse(self._transport.is_open())

    def test_close_exception_handled(self) -> None:
        '''
        Tests handling exceptions during close.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_inst: MagicMock = MagicMock()
            mock_inst.is_open = True
            mock_inst.close.side_effect = SerialException('Close failure')
            mock_serial_cls.return_value = mock_inst

            self._transport.open()
            self._transport.close()
            self.assertFalse(self._transport.is_open())

    def test_close_when_not_open(self) -> None:
        '''
        Tests close call when disconnected.
        '''
        self._transport.close()
        self.assertFalse(self._transport.is_open())

    def test_write_when_not_open(self) -> None:
        '''
        Tests write when connection is closed.
        '''
        written: int = self._transport.write(b'\xfe\xfe\x01')
        self.assertEqual(written, self._constants.zero_bytes_written)

    def test_write_success(self) -> None:
        '''
        Tests transmitting data over serial.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_inst: MagicMock = MagicMock()
            mock_inst.is_open = True
            mock_inst.write.return_value = 3
            mock_serial_cls.return_value = mock_inst

            self._transport.open()
            written: int = self._transport.write(b'\xfe\xfe\x01')
            self.assertEqual(written, 3)
            mock_inst.write.assert_called_once_with(b'\xfe\xfe\x01')

    def test_write_serial_exception(self) -> None:
        '''
        Tests handling write failure.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_inst: MagicMock = MagicMock()
            mock_inst.is_open = True
            mock_inst.write.side_effect = SerialException('Broken pipe')
            mock_serial_cls.return_value = mock_inst

            self._transport.open()
            written: int = self._transport.write(b'\xfe\xfe\x01')
            self.assertEqual(written, self._constants.zero_bytes_written)

    def test_read_when_not_open(self) -> None:
        '''
        Tests reading data when connection is closed.
        '''
        data: bytes = self._transport.read(4)
        self.assertEqual(data, self._constants.empty_payload)

    def test_read_success(self) -> None:
        '''
        Tests receiving byte payload from serial.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_inst: MagicMock = MagicMock()
            mock_inst.is_open = True
            mock_inst.read.return_value = b'\xfe\xfe\x02\x01'
            mock_serial_cls.return_value = mock_inst

            self._transport.open()
            data: bytes = self._transport.read(4)
            self.assertEqual(data, b'\xfe\xfe\x02\x01')
            mock_inst.read.assert_called_once_with(4)

    def test_read_serial_exception(self) -> None:
        '''
        Tests handling read failure.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_inst: MagicMock = MagicMock()
            mock_inst.is_open = True
            mock_inst.read.side_effect = SerialException('Read error')
            mock_serial_cls.return_value = mock_inst

            self._transport.open()
            data: bytes = self._transport.read(4)
            self.assertEqual(data, self._constants.empty_payload)

    def test_flush_when_open(self) -> None:
        '''
        Tests flushing communication buffers.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_inst: MagicMock = MagicMock()
            mock_inst.is_open = True
            mock_serial_cls.return_value = mock_inst

            self._transport.open()
            self._transport.flush()
            mock_inst.flush.assert_called_once()

    def test_flush_exception_handled(self) -> None:
        '''
        Tests handling flush failure.
        '''
        with patch('idecobot.infrastructure.communication.transport.serial_transport.Serial') as mock_serial_cls:
            mock_inst: MagicMock = MagicMock()
            mock_inst.is_open = True
            mock_inst.flush.side_effect = SerialException('Flush failed')
            mock_serial_cls.return_value = mock_inst

            self._transport.open()
            self._transport.flush()

    def test_flush_when_not_open(self) -> None:
        '''
        Tests flush call when disconnected.
        '''
        self._transport.flush()
        self.assertFalse(self._transport.is_open())

    def test_get_version(self) -> None:
        '''
        Tests retrieval of component version string.
        '''
        self.assertEqual(self._transport.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
