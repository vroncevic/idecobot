# -*- coding: UTF-8 -*-

'''
Module
    iprotocol_framer.py
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
    Defines structural interface protocol for serial packet framing and hex formatting.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IProtocolFramer(Protocol):
    '''
        Defines structural interface protocol for serial frame serialization and formatting.

        It defines:

            :methods:
                | encode_frame - Serializes MyCobotFrame into full binary packet with headers.
                | format_hex - Formats binary frame as uppercase space-separated hex string.
                | extract_response_payload - Extracts validated payload from raw response bytes.
                | get_version - Returns framer component version string.
    '''

    def encode_frame(self, frame: MyCobotFrame) -> bytes:
        '''
            Serializes MyCobotFrame into complete binary packet.

            :param frame: Injected MyCobotFrame data model.
            :return: Complete serialized binary packet as bytes.
            :exceptions: None.
        '''

    def format_hex(self, frame: MyCobotFrame) -> str:
        '''
            Formats binary frame as uppercase space-separated hex string.

            :param frame: Injected MyCobotFrame data model.
            :return: Hexadecimal representation string.
            :exceptions: None.
        '''

    def extract_response_payload(
        self,
        raw_bytes: bytes,
        min_frame_len: int,
        prefix_len: int,
        payload_len: int
    ) -> bytes | None:
        '''
            Extracts validated payload from robot raw response bytes.

            :param raw_bytes: Raw bytes received from robot.
            :param min_frame_len: Minimum acceptable length for frame.
            :param prefix_len: Header length prefix offset.
            :param payload_len: Expected length of payload.
            :return: Validated payload bytes, or None if invalid.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the framer component version string.

            :return: Component version string.
            :exceptions: None.
        '''

