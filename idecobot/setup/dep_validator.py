# -*- coding: UTF-8 -*-

'''
Module
    dep_validator.py
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
    Defines IDECobotBundleDependenciesValidator for validating bundle dependencies.
'''

from __future__ import annotations

from collections.abc import Mapping

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from idecobot.setup.dependencies import IDECobotBundleDependencies
from idecobot.setup.keys import IDECobotBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IDECobotBundleDependenciesValidator:
    '''
        Validator for the idecobot bundle dependencies.

        It defines:

            :methods:
                | validate - Validates the idecobot bundle dependencies.
                | is_valid - Checks if the idecobot bundle dependencies are valid.
    '''

    @classmethod
    def validate(cls, dependencies: IDECobotBundleDependencies) -> None:
        '''
            Validates the idecobot bundle dependencies.

            :param dependencies: The idecobot bundle dependencies to validate.
            :exceptions:
                | ATSValueError: The dependencies must be provided.
                | ATSTypeError:  The dependencies must be a Mapping and match expected types.
        '''
        ctx: str = 'idecobot_bundle_dependencies_validator::validate(...)'
        msg_none: str = 'the idecobot bundle dependencies must be provided'
        msg_type: str = 'the idecobot bundle dependencies must be a Mapping'

        not_none(dependencies, ctx, msg_none)
        istype(dependencies, Mapping, ctx, msg_type)

        for attr_name, expected_type in IDECobotBundleKeys.get_dependency_to_type().items():
            msg_attr_none: str = f'the {attr_name.replace("_", " ")} must be provided'
            msg_attr_istype: str = f'the {attr_name.replace("_", " ")} must be an instance of {expected_type.__name__}'

            attribute = dependencies.get(attr_name)

            not_none(attribute, ctx, msg_attr_none)
            istype(attribute, expected_type, ctx, msg_attr_istype)

    @classmethod
    def is_valid(cls, dependencies: IDECobotBundleDependencies) -> bool:
        '''
            Checks if the idecobot bundle dependencies are valid.

            :param dependencies: The idecobot bundle dependencies to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(dependencies)
            return True

        except (ATSValueError, ATSTypeError):
            return False
