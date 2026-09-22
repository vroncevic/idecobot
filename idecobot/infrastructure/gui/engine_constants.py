# -*- coding: UTF-8 -*-

'''
Module
    engine_constants.py
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
    Defines EngineConstants frozen dataclass for IDECobotGUI desktop coordinator.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class EngineConstants:
    '''
        Constants for IDECobotGUI desktop adapter, default baudrate, and log messages.

        It defines:

            :attributes:
                | default_baudrate - Baseline serial communication baudrate.
                | log_connected - Log message template for successful port connection.
                | log_connect_failed - Log message template for failed port connection.
                | log_disconnected - Log message for port disconnection.
                | log_stream_starting - Log message template when trajectory streaming begins.
                | log_stream_busy - Log message when streamer is unable to start.
                | log_stream_paused - Log message when streaming is paused.
                | log_stream_stopped - Log message when streaming is stopped.
                | log_stream_completed - Log message when streaming completes normally.
                | log_stream_error - Log message when streaming encounters an execution error.
                | log_file_loaded - Log message template when a file is successfully loaded.
                | log_file_error - Log message template when file loading fails.
    '''

    default_baudrate: int = 115200
    log_connected: str = 'COMM: Connected to {port} @ {baud} bps'
    log_connect_failed: str = 'COMM: Failed to connect to {port}'
    log_disconnected: str = 'COMM: Disconnected from robot'
    log_stream_starting: str = 'STREAM: Starting execution of {count} instructions...'
    log_stream_busy: str = 'STREAM: Could not start streaming (port closed or busy)'
    log_stream_paused: str = 'STREAM: Paused execution'
    log_stream_stopped: str = 'STREAM: Stopped execution'
    log_stream_completed: str = 'STREAM: Batch completed or stopped'
    log_stream_error: str = 'STREAM: Execution encountered an error'
    log_file_loaded: str = 'FILE: Loaded script from {filepath}'
    log_file_error: str = 'ERROR: Failed to load file {filepath}: {err}'
