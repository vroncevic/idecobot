# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Defines structural interface protocol for the root idecobot Service facade.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from idecobot.core.model.kinematics.mycobot_bounds import MyCobotBounds
from idecobot.core.service.communication.imycobot_controller import IMyCobotController
from idecobot.core.service.communication.imycobot_streamer import IMyCobotStreamer
from idecobot.core.service.dsl.imycobot_dsl_service import IMyCobotDslService
from idecobot.core.service.kinematics.ikinematic_validator import IKinematicValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IService(Protocol):
    '''
        Defines structural interface protocol for core idecobot services.

        It defines:

            :methods:
                | is_initialized - Checks if core service dependencies are active.
                | get_bounds - Retrieves robot kinematic boundaries.
                | get_validator - Retrieves robot kinematic validator service.
                | get_dsl_service - Retrieves high-level DSL service.
                | get_streamer - Retrieves trajectory streamer service.
                | get_controller - Retrieves interactive robot controller.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if core service dependencies are active.

            :return: True if fully initialized, False otherwise.
        '''

    def get_bounds(self) -> MyCobotBounds:
        '''
            Retrieves robot kinematic boundaries.

            :return: Active MyCobotBounds domain model.
        '''

    def get_validator(self) -> IKinematicValidator:
        '''
            Retrieves robot kinematic validator service.

            :return: Active IKinematicValidator domain service.
        '''

    def get_dsl_service(self) -> IMyCobotDslService:
        '''
            Retrieves high-level DSL service.

            :return: IMyCobotDslService abstraction.
        '''

    def get_streamer(self) -> IMyCobotStreamer:
        '''
            Retrieves trajectory streamer service.

            :return: IMyCobotStreamer abstraction.
        '''

    def get_controller(self) -> IMyCobotController:
        '''
            Retrieves interactive robot controller.

            :return: IMyCobotController abstraction.
        '''

    def get_version(self) -> str:
        '''
            Returns service implementation version string.

            :return: Component version string.
        '''
