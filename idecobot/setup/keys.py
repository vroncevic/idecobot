# -*- coding: UTF-8 -*-

'''
Module
    keys.py
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
    Runtime components and interface constraints for the idecobot bundle.
'''

from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar

from ats_utilities.base.setup.bundle import BaseBundle

from idecobot.core.service.communication.imycobot_streamer import IMyCobotStreamer
from idecobot.core.service.iservice import IService
from idecobot.infrastructure.cli.icli import ICLI
from idecobot.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IDECobotBundleKeys:
    '''
        Runtime component and configuration keys for the idecobot bundle.

        It defines:

            :attributes:
                | DEPENDENCY_BASE - Base ATS bundle dependency key.
                | DEPENDENCY_SERVICE - Core robot service dependency key.
                | DEPENDENCY_GUI - GUI presentation adapter dependency key.
                | DEPENDENCY_STREAMER - Robot communication streamer dependency key.
                | DEPENDENCY_CLI - Command line interface adapter dependency key.
                | OPTION_INFO_FILE - Info file configuration key.
                | OPTION_FILE_PATH - Initial DSL script file path key.
                | OPTION_ROBOT_CONFIG - Robot kinematic geometry configuration file key.
                | OPTION_PORT - Default serial port device key.
                | OPTION_BAUDRATE - Default serial baudrate key.
            :methods:
                | get_dependency_to_type - Returns mapping of dependencies to expected types.
                | get_option_to_type - Returns mapping of options to expected types.
    '''

    DEPENDENCY_BASE: ClassVar[str] = 'base'
    DEPENDENCY_SERVICE: ClassVar[str] = 'service'
    DEPENDENCY_GUI: ClassVar[str] = 'gui'
    DEPENDENCY_STREAMER: ClassVar[str] = 'streamer'
    DEPENDENCY_CLI: ClassVar[str] = 'cli'

    OPTION_INFO_FILE: ClassVar[str] = 'info_file'
    OPTION_FILE_PATH: ClassVar[str] = 'file_path'
    OPTION_ROBOT_CONFIG: ClassVar[str] = 'robot_config'
    OPTION_PORT: ClassVar[str] = 'port'
    OPTION_BAUDRATE: ClassVar[str] = 'baudrate'

    @classmethod
    def get_dependency_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of bundle dependencies to their expected types.

            :return: MappingProxyType of dependency keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.DEPENDENCY_BASE: BaseBundle,
            cls.DEPENDENCY_SERVICE: IService,
            cls.DEPENDENCY_GUI: IGUI,
            cls.DEPENDENCY_STREAMER: IMyCobotStreamer,
            cls.DEPENDENCY_CLI: ICLI,
        })

    @classmethod
    def get_option_to_type(cls) -> MappingProxyType[str, type | tuple[type, ...]]:
        '''
            Returns the mapping of bundle options to their expected types.

            :return: MappingProxyType of option keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.OPTION_INFO_FILE: str,
            cls.OPTION_FILE_PATH: str,
            cls.OPTION_ROBOT_CONFIG: str,
            cls.OPTION_PORT: str,
            cls.OPTION_BAUDRATE: int,
        })
