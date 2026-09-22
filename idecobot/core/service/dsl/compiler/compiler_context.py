# -*- coding: UTF-8 -*-

'''
Module
    compiler_context.py
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
    Defines CompilerContext state container for DSL instruction compilation.
'''

from __future__ import annotations

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompilerContext:
    '''
        Execution state context tracked during DSL program compilation.

        It defines:

            :attributes:
                | speed - Current operating velocity percentage.
                | default_speed - Baseline operating velocity percentage.
                | angles - Current joint angles in degrees for joints 1 through 6.
                | coords - Current Cartesian coordinates [x, y, z, rx, ry, rz].
                | frames - Sequence of generated MyCobotFrame instances.
            :methods:
                | __init__ - Initializes compilation context with default speed and home pose.
                | reset_angles - Resets arm angles to zero home position.
                | add_frame - Appends a frame to the compiled frame list.
                | add_delay_to_last_frame - Extends delay of preceding frame by given seconds.
                | get_version - Returns context version string.
    '''

    speed: int
    default_speed: int
    angles: list[float]
    coords: list[float]
    frames: list[MyCobotFrame]

    def __init__(self, default_speed: int) -> None:
        '''
            Initializes compilation context with default speed and home pose.

            :param default_speed: Baseline velocity percentage (1-100).
            :exceptions: None.
        '''
        self.default_speed = default_speed
        self.speed = default_speed
        self.angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.coords = [0.0, 150.0, 200.0, 0.0, 0.0, 0.0]
        self.frames = []

    def reset_angles(self) -> None:
        '''
            Resets joint angles to zero degrees for all 6 joints.

            :exceptions: None.
        '''
        self.angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def add_frame(self, frame: MyCobotFrame) -> None:
        '''
            Appends a compiled frame to the frame list.

            :param frame: MyCobotFrame instance to append.
            :exceptions: None.
        '''
        self.frames.append(frame)

    def add_delay_to_last_frame(self, delay: float) -> bool:
        '''
            Extends delay_after_sec of preceding frame if present.

            :param delay: Additional delay in seconds.
            :return: True if merged with preceding frame, False if frames list is empty.
            :exceptions: None.
        '''
        if not self.frames:
            return False

        last: MyCobotFrame = self.frames[-1]
        self.frames[-1] = MyCobotFrame(
            last.cmd_id,
            last.payload,
            last.delay_after_sec + delay
        )
        return True

    def get_version(self) -> str:
        '''
            Returns the context version string.

            :return: The context version string.
            :exceptions: None.
        '''
        return __version__
