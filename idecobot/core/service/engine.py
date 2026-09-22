# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Core service facade orchestrating kinematic modeling, DSL compilation, streaming, and control.
'''

from __future__ import annotations

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


class Service:
    '''
        Core service orchestrating robot kinematic boundaries, DSL, streaming, and control.

        It defines:

            :attributes:
                | _bounds - MyCobotBounds kinematic limits model.
                | _validator - IKinematicValidator domain service.
                | _dsl_service - High-level DSL parsing, linting, and compilation service.
                | _streamer - Manipulator trajectory and frame streamer.
                | _controller - Direct interactive jog and controller service.
            :methods:
                | __init__ - Initializes the service facade with injected abstractions.
                | is_initialized - Checks if the service is properly initialized.
                | get_bounds - Returns the active MyCobotBounds.
                | get_validator - Returns the active IKinematicValidator.
                | get_dsl_service - Returns the active IMyCobotDslService.
                | get_streamer - Returns the active IMyCobotStreamer.
                | get_controller - Returns the active IMyCobotController.
                | get_version - Returns service implementation version.
    '''

    _bounds: MyCobotBounds
    _validator: IKinematicValidator
    _dsl_service: IMyCobotDslService
    _streamer: IMyCobotStreamer
    _controller: IMyCobotController

    def __init__(
        self,
        bounds: MyCobotBounds,
        validator: IKinematicValidator,
        dsl_service: IMyCobotDslService,
        streamer: IMyCobotStreamer,
        controller: IMyCobotController
    ) -> None:
        '''
            Initializes the service facade with injected abstractions.

            :param bounds: MyCobotBounds kinematic boundary model.
            :param validator: Injected IKinematicValidator domain service.
            :param dsl_service: IMyCobotDslService abstraction.
            :param streamer: IMyCobotStreamer abstraction.
            :param controller: IMyCobotController abstraction.
            :exceptions: None.
        '''
        self._bounds = bounds
        self._validator = validator
        self._dsl_service = dsl_service
        self._streamer = streamer
        self._controller = controller

    def is_initialized(self) -> bool:
        '''
            Verifies all sub-services and models are initialized.

            :return: True if all services are present, False otherwise.
            :exceptions: None.
        '''
        return bool(
            self._bounds is not None
            and self._validator is not None
            and self._dsl_service is not None
            and self._streamer is not None
            and self._controller is not None
        )

    def get_bounds(self) -> MyCobotBounds:
        '''
            Returns the active MyCobotBounds model.

            :return: MyCobotBounds instance.
            :exceptions: None.
        '''
        return self._bounds

    def get_validator(self) -> IKinematicValidator:
        '''
            Returns the active IKinematicValidator domain service.

            :return: IKinematicValidator instance.
            :exceptions: None.
        '''
        return self._validator

    def get_dsl_service(self) -> IMyCobotDslService:
        '''
            Returns the active IMyCobotDslService.

            :return: IMyCobotDslService abstraction.
            :exceptions: None.
        '''
        return self._dsl_service

    def get_streamer(self) -> IMyCobotStreamer:
        '''
            Returns the active IMyCobotStreamer.

            :return: IMyCobotStreamer abstraction.
            :exceptions: None.
        '''
        return self._streamer

    def get_controller(self) -> IMyCobotController:
        '''
            Returns the active IMyCobotController.

            :return: IMyCobotController abstraction.
            :exceptions: None.
        '''
        return self._controller

    def get_version(self) -> str:
        '''
            Returns service implementation version.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
