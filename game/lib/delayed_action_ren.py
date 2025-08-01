"""renpy
init python:
"""

from threading import Timer
from renpy.ui import Action


class Delayed(Action):
    """
    Delayed action.
    Useful for scheduling an action for execution later in a screen.
    """

    def __init__(self, delay: float, callback) -> None:
        self.delay: float = delay
        self.callback = callback
        self.timer: Timer | None = None

    def __call__(self) -> None:
        self.timer = Timer(self.delay, self.do)
        self.timer.start()

    def do(self) -> None:
        try:
            for callback in self.callback:
                try:
                    callback()
                except TypeError:
                    raise
                except:
                    pass
        except TypeError:
            try:
                self.callback()
            except:
                pass
