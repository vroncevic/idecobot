# -*- coding: UTF-8 -*-

'''
Module
    mycobot_streamer.py
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
    Defines MyCobotStreamer executing frame batch transmissions on a background worker thread.
'''

from __future__ import annotations

from collections.abc import Sequence
from threading import Event, Thread
from time import sleep

from idecobot.core.model.communication.mycobot_frame import MyCobotFrame
from idecobot.core.model.communication.stream_config import StreamConfig
from idecobot.core.model.communication.stream_progress import StreamProgress
from idecobot.core.model.communication.stream_state import StreamState
from idecobot.core.service.communication.itransport import ITransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/idecobot'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/idecobot/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MyCobotStreamer:
    '''
        Asynchronously streams sequences of compiled robot frames over injected transport.

        It defines:

            :attributes:
                | _transport - Injected ITransport communications channel.
                | _state - Current StreamState lifecycle status.
                | _current_step - Index of frame currently executing.
                | _total_steps - Total number of frames in active job.
                | _stop_event - Event signaling cancellation of stream.
                | _pause_event - Event signaling pause state.
            :methods:
                | __init__ - Initializes streamer with injected transport.
                | stream - Initiates transmission worker thread.
                | pause - Temporarily halts transmission loop.
                | resume - Resumes transmission loop.
                | stop - Signals worker thread to terminate.
                | get_state - Returns current StreamState.
                | get_progress - Returns progress snapshot.
                | _worker - Worker thread loop transmitting frames.
    '''

    _transport: ITransport

    def __init__(self, transport: ITransport) -> None:
        '''
            Initializes streamer with injected transport abstraction.

            :param transport: Injected ITransport channel.
            :exceptions: None.
        '''
        self._transport = transport
        self._state: StreamState = StreamState.CONNECTED if transport.is_open() else StreamState.DISCONNECTED
        self._current_step: int = 0
        self._total_steps: int = 0
        self._stop_event: Event = Event()
        self._pause_event: Event = Event()
        self._pause_event.set()
        self._thread: Thread | None = None

    def stream(
        self,
        frames: Sequence[MyCobotFrame],
        config: StreamConfig | None = None
    ) -> bool:
        '''
            Initiates streaming of compiled frames on a background thread.

            :param frames: Sequence of MyCobotFrame instructions.
            :param config: Optional stream execution options.
            :return: True if started successfully, False otherwise.
            :exceptions: None.
        '''
        if not self._transport.is_open() or not frames:
            return False
        if self._state == StreamState.STREAMING:
            return False

        self._current_step = 0
        self._total_steps = len(frames)
        self._stop_event.clear()
        self._pause_event.set()
        self._state = StreamState.STREAMING

        self._thread = Thread(
            target=self._worker,
            args=(tuple(frames), config),
            daemon=True
        )
        self._thread.start()
        return True

    def _worker(
        self,
        frames: tuple[MyCobotFrame, ...],
        config: StreamConfig | None
    ) -> None:
        '''
            Worker thread loop transmitting frames to robot.

            :param frames: Tuple of MyCobotFrames.
            :param config: Optional stream configuration.
            :exceptions: None.
        '''
        delay_scale: float = config.playback_rate if config is not None else 1.0
        for idx, frame in enumerate(frames):
            if self._stop_event.is_set():
                break
            self._pause_event.wait()
            self._current_step = idx + 1
            raw_bytes: bytes = frame.to_bytes()
            self._transport.write(raw_bytes)
            sleep_sec: float = frame.delay_after_sec * delay_scale
            if sleep_sec > 0:
                sleep(sleep_sec)

        self._state = StreamState.STOPPED if self._stop_event.is_set() else StreamState.CONNECTED

    def pause(self) -> None:
        '''
            Pauses active transmission loop.

            :exceptions: None.
        '''
        if self._state == StreamState.STREAMING:
            self._pause_event.clear()
            self._state = StreamState.PAUSED

    def resume(self) -> None:
        '''
            Resumes paused transmission loop.

            :exceptions: None.
        '''
        if self._state == StreamState.PAUSED:
            self._pause_event.set()
            self._state = StreamState.STREAMING

    def stop(self) -> None:
        '''
            Cancels frame transmission.

            :exceptions: None.
        '''
        self._stop_event.set()
        self._pause_event.set()
        self._state = StreamState.STOPPED

    def get_state(self) -> StreamState:
        '''
            Queries current streamer lifecycle state.

            :return: StreamState enum member.
            :exceptions: None.
        '''
        return self._state

    def get_progress(self) -> StreamProgress:
        '''
            Retrieves current streaming progress snapshot.

            :return: StreamProgress instance.
            :exceptions: None.
        '''
        percent: float = (
            (self._current_step / self._total_steps) * 100.0 if self._total_steps > 0 else 0.0
        )
        return StreamProgress(
            state=self._state,
            current_step=self._current_step,
            total_steps=self._total_steps,
            command_name='',
            progress_percent=percent
        )
