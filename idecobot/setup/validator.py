# -*- coding: UTF-8 -*-

'''
Module
    validator.py
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
    Defines IDECobotBundleValidator for validating bundle instances.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from idecobot.core.service.communication.imycobot_streamer import IMyCobotStreamer
from idecobot.core.service.iservice import IService
from idecobot.infrastructure.cli.icli import ICLI
from idecobot.infrastructure.gui.igui import IGUI
from idecobot.setup.bundle import IDECobotBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IDECobotBundleValidator:
    '''
        Validator for the idecobot bundle instance.

        It defines:

            :methods:
                | validate - Validates the idecobot bundle instance.
                | is_valid - Checks if the idecobot bundle instance is valid.
    '''

    @classmethod
    def validate(cls, bundle: IDECobotBundle) -> None:
        '''
            Validates the idecobot bundle instance.

            :param bundle: The idecobot bundle instance to validate.
            :exceptions:
                | ATSValueError: The bundle must be provided and have non-None attributes.
                | ATSTypeError:  The bundle attributes must match required interfaces.
        '''
        ctx: str = 'idecobot_bundle_validator::validate(...)'
        msg_bundle_none: str = 'the idecobot bundle must be provided'
        msg_bundle_istype: str = 'the idecobot bundle must be an instance of IDECobotBundle'
        msg_base_none: str = 'the base bundle must be provided'
        msg_service_none: str = 'the service must be provided'
        msg_gui_none: str = 'the gui must be provided'
        msg_streamer_none: str = 'the streamer must be provided'
        msg_cli_none: str = 'the cli must be provided'
        msg_base_istype: str = 'the base bundle must be an instance of BaseBundle'
        msg_service_istype: str = 'the service must be an instance of IService'
        msg_gui_istype: str = 'the gui must be an instance of IGUI'
        msg_streamer_istype: str = 'the streamer must be an instance of IMyCobotStreamer'
        msg_cli_istype: str = 'the cli must be an instance of ICLI'

        not_none(bundle, ctx, msg_bundle_none)
        istype(bundle, IDECobotBundle, ctx, msg_bundle_istype)

        not_none(bundle.base, ctx, msg_base_none)
        not_none(bundle.service, ctx, msg_service_none)
        not_none(bundle.gui, ctx, msg_gui_none)
        not_none(bundle.streamer, ctx, msg_streamer_none)
        not_none(bundle.cli, ctx, msg_cli_none)

        istype(bundle.base, BaseBundle, ctx, msg_base_istype)
        istype(bundle.service, IService, ctx, msg_service_istype)
        istype(bundle.gui, IGUI, ctx, msg_gui_istype)
        istype(bundle.streamer, IMyCobotStreamer, ctx, msg_streamer_istype)
        istype(bundle.cli, ICLI, ctx, msg_cli_istype)

    @classmethod
    def is_valid(cls, bundle: IDECobotBundle) -> bool:
        '''
            Checks if the idecobot bundle is valid.

            :param bundle: The idecobot bundle to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(bundle)
            return True

        except (ATSValueError, ATSTypeError):
            return False
