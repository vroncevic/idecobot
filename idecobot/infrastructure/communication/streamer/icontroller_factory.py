# -*- coding: UTF-8 -*-

'''
Module
    icontroller_factory.py
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
    Defines structural interface protocol for factory assembling robot controller components.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.protocol_constants import ProtocolConstants
from idecobot.core.service.communication.itransport import ITransport
from idecobot.infrastructure.communication.protocol.imycobot_protocol_codec import IMyCobotProtocolCodec
from idecobot.infrastructure.communication.streamer.mycobot_controller import MyCobotController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IControllerFactory(Protocol):
    '''
        Defines structural interface protocol for robot controller factory.

        It defines:

            :methods:
                | create - Assembles connection, actuator, and telemetry into controller facade.
                | get_version - Returns controller factory version string.
    '''

    def create(
        self,
        transport: ITransport,
        codec: IMyCobotProtocolCodec,
        constants: ProtocolConstants
    ) -> MyCobotController:
        '''
            Assembles connection, actuator, and telemetry into controller facade.

            :param transport: Injected ITransport channel instance.
            :param codec: Injected IMyCobotProtocolCodec codec instance.
            :param constants: Injected ProtocolConstants framing parameters.
            :return: Fully wired MyCobotController instance.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns controller factory version string.

            :return: Component version string.
            :exceptions: None.
        '''
