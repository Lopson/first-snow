"""renpy
init python:
"""

from time import time
from threading import Timer
from renpy.rollback import NoRollback
from typing import Callable


class ExtendableEvent(NoRollback):
    def __init__(
            self, interval: float,
            stop_func: Callable,
            start_func: Callable | None = None) -> None:
        self.ends_at: float | None = None
        self.timer: Timer | None = None
        self.interval: float | None = interval
        self.start_func: Callable | None = start_func
        self.stop_func: Callable = stop_func

    def trigger(self) -> None:
        now = time()
        if self.ends_at is not None and now < self.ends_at:
            self.timer = Timer(self.ends_at - now, self.trigger)
            self.timer.run()
        else:
            self.timer = None
            self.stop_func()

    def start(self, run_start=True) -> None:
        if self.interval is not None:
            self.ends_at = time() + self.interval
            self.timer = Timer(self.interval, self.trigger)
            self.timer.start()
            if run_start and self.start_func:
                self.start_func()

    def cancel(self) -> None:
        if self.timer is not None:
            self.timer.cancel()

    def extend(self, interval) -> None:
        new_ends = time() + interval
        self.interval = interval
        if new_ends < self.ends_at:
            self.cancel()
            self.start(run_start=False)
        else:
            self.ends_at = new_ends

    def has_ended(self) -> bool:
        return self.timer is None
