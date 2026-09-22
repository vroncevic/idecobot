# -*- coding: UTF-8 -*-

'''
Module
    stream_state.py
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
    Defines StreamState enumeration representing lifecycle states of trajectory streaming.
'''

from __future__ import annotations

from enum import Enum

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamState(Enum):
    '''
        Enumeration of the hardware streaming lifecycle states.

        It defines:

            :attributes:
                | DISCONNECTED - Port is closed and robot is unlinked.
                | CONNECTED - Port is open and robot link is idle.
                | STREAMING - Actively transmitting frames to the manipulator.
                | PAUSED - Stream execution temporarily suspended.
                | STOPPED - Stream cancelled or completed.
                | ERROR - Communication error or unexpected fault encountered.
    '''

    DISCONNECTED = 'DISCONNECTED'
    CONNECTED = 'CONNECTED'
    STREAMING = 'STREAMING'
    PAUSED = 'PAUSED'
    STOPPED = 'STOPPED'
    ERROR = 'ERROR'
