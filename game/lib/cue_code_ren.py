"""renpy
init python:
"""

from typing import Final, TYPE_CHECKING
from time import time
from threading import Timer
from renpy import config
from renpy.exports.displayexports import restart_interaction
from renpy.display.screen import has_screen, get_screen, show_screen, hide_screen
if TYPE_CHECKING:
    from renpy import store

CUE_DEFAULT_SCREEN: Final[str] = 'cue'
store._cues = []


class Cue:
    def __init__(self, name: str, args, timeout: float):
        self.name: str = name
        self.args = args
        self.until: float = time() + timeout

    def is_active(self) -> float:
        return time() < self.until


def cue(name: str, timeout: float, **args) -> None:
    show_cue(name, timeout, args)
    t: Timer = Timer(timeout, restart_interaction)
    t.start()
    restart_interaction()


def show_cue(name: str, timeout: float, args=None) -> Cue:
    args = args or {}

    specific_screen: str = CUE_DEFAULT_SCREEN + '_' + name
    if has_screen(specific_screen):
        screen = specific_screen
    else:
        screen = CUE_DEFAULT_SCREEN
        args['name'] = name

    c: Cue = Cue(screen, args, timeout)
    store._cues.append(c)
    return c


def hide_cue(c: Cue) -> None:
    c.until = 0.0
    restart_interaction()


def cue_overlay_func() -> None:
    if not get_screen('cue_overlay') and store._cues:
        show_screen('cue_overlay')
    elif get_screen('cue_overlay') and not store._cues:
        hide_screen('cue_overlay')


config.overlay_functions.append(cue_overlay_func)
