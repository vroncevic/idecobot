# -*- coding: UTF-8 -*-

'''
Module
    stream_progress.py
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
    Defines StreamProgress immutable model for runtime streaming telemetry.
'''

from __future__ import annotations

from dataclasses import dataclass

from idecobot.core.model.communication.stream_state import StreamState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class StreamProgress:
    '''
        Captures dynamic telemetry during sequence transmission to robot.

        It defines:

            :attributes:
                | state - Current lifecycle state of the streamer.
                | current_step - Index of the currently executing instruction (1-indexed).
                | total_steps - Total count of instructions in stream batch.
                | command_name - Human-readable name of current command.
                | progress_percent - Computed completion percentage (0.0 to 100.0).
    '''

    state: StreamState
    current_step: int
    total_steps: int
    command_name: str
    progress_percent: float
