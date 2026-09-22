# -*- coding: UTF-8 -*-

'''
Module
    imycobot_streamer.py
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
    Defines structural interface protocol for streaming compiled binary frames.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.stream_config import StreamConfig
from idecobot.core.model.communication.stream_progress import StreamProgress
from idecobot.core.model.communication.stream_state import StreamState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMyCobotStreamer(Protocol):
    '''
        Defines structural interface protocol for streaming frame batches to manipulator.

        It defines:

            :methods:
                | stream - Initiates streaming of compiled frame sequence.
                | pause - Temporarily pauses active transmission.
                | resume - Resumes paused transmission.
                | stop - Cancels active frame streaming.
                | get_state - Queries current streamer lifecycle state.
                | get_progress - Retrieves current streaming progress snapshot.
                | get_version - Returns protocol interface version.
    '''

    def stream(self, frames: Sequence[MyCobotFrame], config: StreamConfig | None = None) -> bool:
        '''
            Initiates streaming of compiled frame sequence.

            :param frames: Sequence of MyCobotFrame binary instructions.
            :param config: Optional streaming execution configuration.
            :return: True if streaming commenced, False otherwise.
        '''

    def pause(self) -> None:
        '''
            Temporarily pauses active transmission.
        '''

    def resume(self) -> None:
        '''
            Resumes paused transmission.
        '''

    def stop(self) -> None:
        '''
            Cancels active frame streaming.
        '''

    def get_state(self) -> StreamState:
        '''
            Queries current streamer lifecycle state.

            :return: Active StreamState enumeration member.
        '''

    def get_progress(self) -> StreamProgress:
        '''
            Retrieves current streaming progress snapshot.

            :return: Current StreamProgress instance.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol interface version string.

            :return: Version string.
        '''
