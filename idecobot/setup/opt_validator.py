# -*- coding: UTF-8 -*-

'''
Module
    opt_validator.py
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
    Defines IDECobotBundleOptionsValidator for validating bundle options.
'''

from __future__ import annotations

from collections.abc import Mapping

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from idecobot.setup.keys import IDECobotBundleKeys
from idecobot.setup.options import IDECobotBundleOptions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IDECobotBundleOptionsValidator:
    '''
        Validator for the idecobot bundle options.

        It defines:

            :methods:
                | validate - Validates the idecobot bundle options.
                | is_valid - Checks if the idecobot bundle options are valid.
    '''

    @classmethod
    def validate(cls, options: IDECobotBundleOptions) -> None:
        '''
            Validates the idecobot bundle options.

            :param options: The idecobot bundle options to validate.
            :exceptions:
                | ATSValueError: The options must be provided.
                | ATSTypeError:  The options must be a Mapping and attribute types must match.
        '''
        ctx: str = 'idecobot_bundle_options_validator::validate(...)'
        msg_none: str = 'the idecobot bundle options must be provided'
        msg_type: str = 'the idecobot bundle options must be a Mapping'

        not_none(options, ctx, msg_none)
        istype(options, Mapping, ctx, msg_type)

        for attr_name, expected_type in IDECobotBundleKeys.get_option_to_type().items():
            if attr_name in options:
                type_name: str = (
                    '/'.join(t.__name__ for t in expected_type)
                    if isinstance(expected_type, tuple)
                    else expected_type.__name__
                )
                msg_attr: str = f'the {attr_name.replace("_", " ")} must be an instance of {type_name}'
                val = options.get(attr_name)
                istype(val, expected_type, ctx, msg_attr)

    @classmethod
    def is_valid(cls, options: IDECobotBundleOptions) -> bool:
        '''
            Checks if the idecobot bundle options are valid.

            :param options: The idecobot bundle options to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(options)
            return True

        except (ATSValueError, ATSTypeError):
            return False
