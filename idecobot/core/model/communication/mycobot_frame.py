# -*- coding: UTF-8 -*-

'''
Module
    mycobot_frame.py
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
    Defines MyCobotFrame immutable data model for Elephant Robotics binary serial frames.
'''

from __future__ import annotations

from dataclasses import dataclass

from idecobot.core.model.communication.protocol_constants import ProtocolConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MyCobotFrame:
    '''
        Represents a raw binary frame conforming to Elephant Robotics serial protocol.
        Format: 0xFE 0xFE [Length] [CmdID] [Payload] 0xFA

        It defines:

            :attributes:
                | cmd_id - Integer command identifier (e.g., 0x22 for SEND_ANGLES).
                | payload - Binary byte sequence payload.
                | delay_after_sec - Recommended pause delay after transmitting this frame.
            :methods:
                | to_bytes - Assembles and returns the full serialized binary frame.
                | to_hex_string - Formats frame as uppercase space-separated hex bytes.
    '''

    cmd_id: int
    payload: bytes = b''
    delay_after_sec: float = 0.0

    def to_bytes(self, constants: ProtocolConstants | None = None) -> bytes:
        '''
            Serializes into full binary frame with header, length, command ID, and footer.

            :param constants: Optional ProtocolConstants framing configuration.
            :return: Complete binary packet as bytes.
            :exceptions: None.
        '''
        cfg: ProtocolConstants = constants if constants is not None else ProtocolConstants()
        length: int = len(self.payload) + cfg.length_overhead

        return (
            cfg.header_prefix
            + bytes([length & cfg.byte_mask, self.cmd_id & cfg.byte_mask])
            + self.payload
            + cfg.footer_suffix
        )

    def to_hex_string(self, constants: ProtocolConstants | None = None) -> str:
        '''
            Formats binary frame as uppercase space-separated hex string.

            :param constants: Optional ProtocolConstants framing configuration.
            :return: Hexadecimal representation string.
            :exceptions: None.
        '''
        return self.to_bytes(constants=constants).hex(' ').upper()
