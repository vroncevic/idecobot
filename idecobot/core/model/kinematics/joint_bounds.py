# -*- coding: UTF-8 -*-

'''
Module
    joint_bounds.py
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
    Defines JointBounds immutable value object for 6-DOF robotic manipulator joints.
'''

from __future__ import annotations

from dataclasses import dataclass

from idecobot.core.model.kinematics.joint_limit import JointLimit

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class JointBounds:
    '''
        Defines mechanical angular boundaries for all 6 joints of myCobot 280.

        It defines:

            :attributes:
                | j1 - Angular limits for Joint 1.
                | j2 - Angular limits for Joint 2.
                | j3 - Angular limits for Joint 3.
                | j4 - Angular limits for Joint 4.
                | j5 - Angular limits for Joint 5.
                | j6 - Angular limits for Joint 6.
    '''

    j1: JointLimit
    j2: JointLimit
    j3: JointLimit
    j4: JointLimit
    j5: JointLimit
    j6: JointLimit
