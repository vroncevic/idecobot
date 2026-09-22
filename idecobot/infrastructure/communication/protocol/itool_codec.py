# -*- coding: UTF-8 -*-

'''
Module
    itool_codec.py
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
    Defines structural interface protocol for end-effector tool and gripper command encoding.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IToolCodec(Protocol):
    '''
        Defines structural interface protocol for robot tool command serialization.

        It defines:

            :methods:
                | pack_gripper - Assembles SET_GRIPPER binary frame.
                | get_version - Returns tool codec component version string.
    '''

    def pack_gripper(self, state: int, speed: int) -> MyCobotFrame:
        '''
            Assembles SET_GRIPPER binary frame.

            :param state: Gripper state (1=grip, 0=release).
            :param speed: Operating velocity percentage.
            :return: Serialized MyCobotFrame instance.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the tool codec component version string.

            :return: Component version string.
            :exceptions: None.
        '''
