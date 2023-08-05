"""
Author: Benedikt Vollmerhaus
License: MIT
"""

import logging
import threading
import typing

from blurwal import paths
from blurwal.backends import base


class Transition(threading.Thread):
    """
    A thread for asynchronously transitioning between two blur levels.

    It supports being stopped to enable reversing a running transition.
    The current blur level is saved on each frame, so that a subsequent
    thread may begin reversing the previous transition from there, even
    if that transition was interrupted.
    """

    def __init__(self, from_blur_level: int, to_blur_level: int,
                 backend: base.Backend) -> None:
        super().__init__()
        self._stop_event = threading.Event()

        self._from_blur_level: int = from_blur_level
        self._to_blur_level: int = to_blur_level
        self._backend: base.Backend = backend

        self.current_level: int = from_blur_level

    def stop(self) -> None:
        """
        Stop the currently running blur transition.

        :return: None
        """
        self._stop_event.set()

    def is_stopped(self) -> bool:
        """
        Return whether the blur transition has been stopped.

        :return: Whether the blur transition has been stopped
        """
        return self._stop_event.is_set()

    def run(self) -> None:
        """
        Begin transitioning from the initial to the target blur level.

        This is done by changing the wallpaper to each intermediate frame
        in quick succession (speed depends on the backend's performance).

        :return: None
        """
        if self._from_blur_level < self._to_blur_level:
            logging.info('Blurring from blur level %s to %s.',
                         self._from_blur_level, self._to_blur_level)

            blur_levels: typing.Iterable = range(self._from_blur_level + 1,
                                                 self._to_blur_level + 1)
        else:
            logging.info('Unblurring from blur level %s to %s.',
                         self._from_blur_level, self._to_blur_level)

            blur_levels = reversed(range(self._to_blur_level,
                                         self._from_blur_level))

        for level in blur_levels:
            if self.is_stopped():
                break

            self.current_level = level

            blur_frame = paths.CACHE_DIR / f'frame-{level}.jpg'
            self._backend.change_to(blur_frame)
