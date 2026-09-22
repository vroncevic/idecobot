# -*- coding: UTF-8 -*-

'''
Module
    tool_codec.py
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
    Defines ToolCodec assembling SET_GRIPPER binary frames.
'''

from __future__ import annotations

from struct import pack

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


class ToolCodec:
    '''
        Encodes end-effector tool gripper actions into binary frames.

        It defines:

            :attributes:
                | _constants - Injected ProtocolConstants low-level framing parameters.
            :methods:
                | __init__ - Initializes tool codec with protocol constants.
                | pack_gripper - Assembles SET_GRIPPER binary frame.
                | get_version - Returns tool codec component version string.
    '''

    _constants: ProtocolConstants

    def __init__(self, constants: ProtocolConstants) -> None:
        '''
            Initializes ToolCodec with protocol constants.

            :param constants: Injected ProtocolConstants instance.
            :exceptions: None.
        '''
        self._constants = constants

    def pack_gripper(self, state: int, speed: int) -> MyCobotFrame:
        '''
            Assembles SET_GRIPPER binary frame.

            :param state: Gripper state (1=grip, 0=release).
            :param speed: Operating velocity percentage.
            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''
        payload: bytes = pack(
            self._constants.format_gripper_command,
            state & self._constants.byte_mask,
            speed & self._constants.byte_mask
        )

        return MyCobotFrame(
            self._constants.cmd_set_gripper,
            payload,
            self._constants.gripper_delay
        )

    def get_version(self) -> str:
        '''
            Returns the tool codec component version string.

            :return: The component version string.
            :exceptions: None.
        '''
        return __version__
