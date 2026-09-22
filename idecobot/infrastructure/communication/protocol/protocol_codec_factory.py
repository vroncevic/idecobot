# -*- coding: UTF-8 -*-

'''
Module
    protocol_codec_factory.py
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
    Defines ProtocolCodecFactory assembling focused protocol codec components.
'''

from __future__ import annotations

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.infrastructure.communication.protocol.motion_codec import MotionCodec
from idecobot.infrastructure.communication.protocol.mycobot_protocol_codec import MyCobotProtocolCodec
from idecobot.infrastructure.communication.protocol.protocol_framer import ProtocolFramer
from idecobot.infrastructure.communication.protocol.system_codec import SystemCodec
from idecobot.infrastructure.communication.protocol.tool_codec import ToolCodec

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProtocolCodecFactory:
    '''
        Factory assembling focused protocol framer, motion, tool, and system components.

        It defines:

            :methods:
                | create - Builds and wires a composite MyCobotProtocolCodec facade.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, constants: ProtocolConstants) -> MyCobotProtocolCodec:
        '''
            Builds and wires a composite MyCobotProtocolCodec facade.

            :param constants: Immutable protocol constants model.
            :return: Fully wired MyCobotProtocolCodec instance.
            :exceptions: None.
        '''
        return MyCobotProtocolCodec(
            framer=ProtocolFramer(constants=constants),
            motion=MotionCodec(constants=constants),
            tool=ToolCodec(constants=constants),
            system=SystemCodec(constants=constants)
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns protocol codec factory version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
