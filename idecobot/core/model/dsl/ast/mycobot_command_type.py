# -*- coding: UTF-8 -*-

'''
Module
    mycobot_command_type.py
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
    Defines MyCobotCommandType enumeration for high-level DSL instruction types.
'''

from __future__ import annotations

from enum import Enum

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotCommandType(Enum):
    '''
        Enumeration of supported myCobot DSL instruction command types.

        It defines:

            :attributes:
                | HOME - Returns all 6 joints to vertical zero origin.
                | RELAX - Disables servo motor torque (emergency release).
                | POWER - Powers on and engages all servo joints.
                | SPEED - Sets default speed percentage for subsequent motions.
                | WAIT - Pauses execution for specified seconds.
                | TOOL - End-effector action (GRIP or RELEASE).
                | MOVE_JOINTS - Multi-axis joint space motion (J1 through J6).
                | MOVE_COORDS - Cartesian space tool center point motion (X, Y, Z, Rx, Ry, Rz).
    '''

    HOME = 'HOME'
    RELAX = 'RELAX'
    POWER = 'POWER'
    SPEED = 'SPEED'
    WAIT = 'WAIT'
    TOOL = 'TOOL'
    MOVE_JOINTS = 'MOVE_JOINTS'
    MOVE_COORDS = 'MOVE_COORDS'
