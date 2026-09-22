# -*- coding: UTF-8 -*-

'''
Module
    streamer_factory.py
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
    Defines StreamerFactory assembling transport and framer into streamer instance.
'''

from __future__ import annotations

from idecobot.core.service.communication.itransport import ITransport
from idecobot.infrastructure.communication.protocol.iprotocol_framer import IProtocolFramer
from idecobot.infrastructure.communication.streamer.mycobot_streamer import MyCobotStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerFactory:
    '''
        Factory assembling transport and protocol framer into streamer instance.

        It defines:

            :methods:
                | create - Assembles transport and framer into streamer instance.
                | get_version - Returns streamer factory version string.
    '''

    @classmethod
    def create(
        cls,
        transport: ITransport,
        framer: IProtocolFramer
    ) -> MyCobotStreamer:
        '''
            Assembles transport and framer into streamer instance.

            :param transport: Injected ITransport channel instance.
            :param framer: Injected IProtocolFramer protocol encoder instance.
            :return: Fully wired MyCobotStreamer instance.
            :exceptions: None.
        '''
        return MyCobotStreamer(transport=transport, framer=framer)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns streamer factory version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
