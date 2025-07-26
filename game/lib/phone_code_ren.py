"""renpy
init python:
"""

from typing import TypeAlias
from renpy.display.screen import show_screen, hide_screen
from renpy.exports.displayexports import restart_interaction, showing, transition
from renpy.exports.statementexports import pause

PhoneEntry: TypeAlias = list[tuple[bool, str, str]]

class Phone:
    def __init__(self):
        self.messages: dict[str, PhoneEntry] = {}
        self.waiting: bool = False

    def message(self, who: str, time: str, message: str, to: bool = False) -> None:
        self.messages.setdefault(who, [])
        self.messages[who].append((to, time, message))
        restart_interaction()

    def clear(self, who: str) -> None:
        self.messages[who] = []
        restart_interaction()

    def show(self, mode, **kwargs) -> None:
        show_screen('phone', mode=mode, **kwargs)
        if showing('phone', layer='screens'):
            transition(dissolve, layer='screens') # pyright: ignore[reportUndefinedVariable]

    def hide(self) -> None:
        hide_screen('phone')

    def wait(self) -> None:
        self.waiting = True
        pause()
        self.waiting = False
