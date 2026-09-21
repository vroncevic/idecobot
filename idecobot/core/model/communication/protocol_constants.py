# -*- coding: UTF-8 -*-

'''
Module
    protocol_constants.py
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
    Defines ProtocolConstants immutable dataclass for Elephant Robotics serial protocol framing.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ProtocolConstants:
    '''
        Elephant Robotics serial protocol framing markers, command IDs, and scaling factors.

        It defines:

            :attributes:
                | header_byte_1 - Primary framing header marker byte (0xFE).
                | header_byte_2 - Secondary framing header marker byte (0xFE).
                | footer_byte - Packet framing footer marker byte (0xFA).
                | header_prefix - Serialized two-byte header prefix (b'\\xfe\\xfe').
                | footer_suffix - Serialized single-byte footer suffix (b'\\xfa').
                | length_overhead - Header length overhead including length and cmd_id (2).
                | byte_mask - Bitmask for single-byte masking operations (0xFF).
                | cmd_power_on - Binary command ID for servo power on (0x10).
                | cmd_release_servos - Binary command ID to release servo motors (0x13).
                | cmd_get_angles - Binary command ID querying current joint angles (0x20).
                | cmd_send_angles - Binary command ID transmitting joint angle positions (0x22).
                | cmd_send_coords - Binary command ID transmitting Cartesian coordinates (0x25).
                | cmd_set_gripper - Binary command ID commanding end-effector gripper (0x66).
                | cmd_nop - Binary NOP/idle command ID (0x00).
                | angle_scale_factor - Fixed-point scaling factor for joint angles (100.0).
                | coord_scale_factor - Fixed-point scaling factor for coordinates (100.0).
                | default_frame_delay - Recommended post-transmission pause in seconds (0.05).
                | servo_delay - Recommended post-transmission pause for power/relax in seconds (0.1).
                | gripper_delay - Recommended post-transmission pause for gripper in seconds (0.5).
                | home_delay - Recommended post-transmission pause for home movement in seconds (1.0).
                | min_angles_response_len - Minimum payload length for angle response frame (12).
                | min_angles_frame_len - Minimum complete frame length containing 12 bytes payload (16).
                | full_angles_response_len - Total frame length for read angles response including footer (17).
                | format_angles_command - Struct pack format for SEND_ANGLES payload ('>6hB').
                | format_coords_command - Struct pack format for SEND_COORDS payload ('>6hBB').
                | format_gripper_command - Struct pack format for SET_GRIPPER payload ('>BB').
                | format_joints_payload - Struct unpack format for joint data payload ('>6h').
    '''

    header_byte_1: int = 0xFE
    header_byte_2: int = 0xFE
    footer_byte: int = 0xFA
    header_prefix: bytes = b'\xfe\xfe'
    footer_suffix: bytes = b'\xfa'
    length_overhead: int = 2
    byte_mask: int = 0xFF
    cmd_power_on: int = 0x10
    cmd_release_servos: int = 0x13
    cmd_get_angles: int = 0x20
    cmd_send_angles: int = 0x22
    cmd_send_coords: int = 0x25
    cmd_set_gripper: int = 0x66
    cmd_nop: int = 0x00
    angle_scale_factor: float = 100.0
    coord_scale_factor: float = 100.0
    default_frame_delay: float = 0.05
    servo_delay: float = 0.1
    gripper_delay: float = 0.5
    home_delay: float = 1.0
    min_angles_response_len: int = 12
    min_angles_frame_len: int = 16
    full_angles_response_len: int = 17
    format_angles_command: str = '>6hB'
    format_coords_command: str = '>6hBB'
    format_gripper_command: str = '>BB'
    format_joints_payload: str = '>6h'
