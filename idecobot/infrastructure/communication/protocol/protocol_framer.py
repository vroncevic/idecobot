# -*- coding: UTF-8 -*-

'''
Module
    protocol_framer.py
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
    Defines ProtocolFramer serializing MyCobot frames into binary packets with framing markers.
'''

from __future__ import annotations

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.protocol_constants import ProtocolConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProtocolFramer:
    '''
        Assembles raw wire packets with framing headers, lengths, and footers.

        It defines:

            :attributes:
                | _constants - Injected ProtocolConstants low-level framing parameters.
            :methods:
                | __init__ - Initializes framer with protocol constants.
                | encode_frame - Serializes MyCobotFrame into binary packet with markers.
                | format_hex - Formats binary packet as uppercase space-separated hex string.
                | extract_response_payload - Extracts validated payload from raw response bytes.
                | get_version - Returns framer component version string.
    '''

    _constants: ProtocolConstants

    def __init__(self, constants: ProtocolConstants) -> None:
        '''
            Initializes ProtocolFramer with protocol constants.

            :param constants: Injected ProtocolConstants instance.
            :exceptions: None.
        '''
        self._constants = constants

    def encode_frame(self, frame: MyCobotFrame) -> bytes:
        '''
            Serializes MyCobotFrame into full binary packet with header, length, cmd ID, and footer.

            :param frame: Injected MyCobotFrame data model.
            :return: Complete serialized binary packet as bytes.
            :exceptions: None.
        '''
        length: int = len(frame.payload) + self._constants.length_overhead

        return (
            self._constants.header_prefix
            + bytes([
                length & self._constants.byte_mask,
                frame.cmd_id & self._constants.byte_mask
            ])
            + frame.payload
            + self._constants.footer_suffix
        )

    def format_hex(self, frame: MyCobotFrame) -> str:
        '''
            Formats binary frame as uppercase space-separated hex string.

            :param frame: Injected MyCobotFrame data model.
            :return: Hexadecimal representation string.
            :exceptions: None.
        '''
        return self.encode_frame(frame).hex(' ').upper()

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
        if (
            len(raw_bytes) >= min_frame_len
            and raw_bytes[0] == self._constants.header_byte_1
            and raw_bytes[1] == self._constants.header_byte_2
        ):
            payload_end: int = prefix_len + payload_len
            return raw_bytes[prefix_len:payload_end]

        return None

    def get_version(self) -> str:
        '''
            Returns the framer component version string.

            :return: The component version string.
            :exceptions: None.
        '''
        return __version__
