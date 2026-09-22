# -*- coding: UTF-8 -*-

'''
Module
    itoolbar.py
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
    Defines structural interface protocol IToolbar for application quick-action toolbar.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

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
class IToolbar(Protocol):
    '''
        Structural interface protocol for application toolbar actions.

        It defines:

            :methods:
                | update_stream_state - Updates button active/disabled states based on stream state.
                | set_connected - Updates connection indicator state.
                | get_version - Returns protocol version string.
    '''

    def update_stream_state(self, state: StreamState) -> None:
        '''
            Updates button active/disabled states based on stream state.

            :param state: Current StreamState member.
        '''

    def set_connected(self, connected: bool) -> None:
        '''
            Updates connection indicator state.

            :param connected: True if robot is linked, False otherwise.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
        '''

