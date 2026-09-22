# -*- coding: UTF-8 -*-

'''
Module
    options.py
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
    Defines IDECobotBundleOptions TypedDict specification.
'''

from __future__ import annotations

from typing import TypedDict

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IDECobotBundleOptions(TypedDict, total=False):
    '''
        IDECobot bundle options configuration specification.

        It defines:

            :attributes:
                | info_file - Path to the idecobot package configuration file.
                | file_path - Optional initial DSL script file path to load into the editor.
                | robot_config - Path to custom robot kinematics geometry configuration file.
                | port - Serial device path or descriptor.
                | baudrate - Serial transmission baudrate.
    '''

    info_file: str
    file_path: str
    robot_config: str
    port: str
    baudrate: int
