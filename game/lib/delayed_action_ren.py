"""renpy
init python:
"""

from threading import Timer
from typing import Callable
from renpy.ui import Action


class Delayed(Action):
    """
    Delayed action.
    Useful for scheduling an action for execution later in a screen.
    """

    def __init__(
            self,
            delay: float,
            callback: Callable | list[Callable]) -> None:
        self.delay: float = delay
        self.callback: Callable | list[Callable]  = callback
        self.timer: Timer | None = None

    def __call__(self) -> None:
        self.timer = Timer(self.delay, self.do)
        self.timer.start()

    def do(self) -> None:
        if isinstance(self.callback, list):
            for callback in self.callback:
                try:
                    callback()
                except TypeError:
                    raise
                except:
                    pass
        else:
            try:
                self.callback()
            except:
                pass
