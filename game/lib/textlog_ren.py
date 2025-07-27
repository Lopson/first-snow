# textlog.rpy
# Maintains a nice little text log. Works through rollback and roll-forward.
# Tested in Ren'Py v6.17.3.
# Copyright (C) 2012-2014 Shiz.
# Released under the terms of the WTFPL; see http://sam.zoy.org/wtfpl/COPYING for details.

# USAGE:
# Place in your game, then call screen text_log to show the text log.
#
# Config variables:
#   - config.text_log_size:
#     Text log size. -1 for unlimited.
#   - config.text_log_blocked_tags:
#     Do not log the text if it contains one of these tags.
#   - config.text_log_filtered_tags:
#     Tags to filter for the log.

# TODO Unclear why the game relies on this implementation vs the default
# Ren'Py history implementation!

"""renpy
python early:
"""


import re
from typing import Callable, TypeAlias, Optional
from renpy.rollback import NoRollback
from renpy import config
from renpy import store
TextLogDataEntry: TypeAlias = tuple[Optional[str], Optional[str], Optional[str]]
TextLogData: TypeAlias = list[TextLogDataEntry]


# Create configuration variables.
locked: bool = config.locked
config.locked = False
config.text_log_size = 100 # pyright: ignore[reportAttributeAccessIssue]
config.text_log_blocked_tags = [ 'nw' ] # pyright: ignore[reportAttributeAccessIssue]
config.text_log_filtered_tags = [ '', 'w', 'fast', 'cps', 'p' ] # pyright: ignore[reportAttributeAccessIssue]
config.locked = locked


class TextLog(NoRollback):
    """
    Simple buffer to hold the text log;
    will automatically delete older logs once the limit has reached.
    """

    def __init__(self) -> None:
        self.given_size: int = config.text_log_size # pyright: ignore[reportAttributeAccessIssue]
        self.hooks: list[Callable] = []
        if self.given_size == -1:
            self.size: int = 0
            self.data: TextLogData = []
        else:
            self.size = self.given_size
            self.data = [ (None, None, None) for _ in range(self.size) ]

        self.block_regexp: re.Pattern = re.compile(
            '(' +
            '|'.join(r'\{%s\}|\{%s=.*?\}|\{/%s\}' % (
                tag, tag, tag
                ) for tag in config.text_log_blocked_tags) + # pyright: ignore[reportAttributeAccessIssue]
            ')')
        self.filter_regexp: re.Pattern = re.compile(
            '(' + 
            '|'.join(r'\{%s\}|\{%s=.*?\}|\{/%s\}' % (
                tag, tag, tag
                ) for tag in config.text_log_filtered_tags) + # pyright: ignore[reportAttributeAccessIssue]
            ')')

    def add_dialogue(self, who: str, what: str) -> None:
        if not what or self.block_regexp.search(what):
            return
        fwho : str | None = self.filter_regexp.sub('', who) if who else None
        fwhat: str = self.filter_regexp.sub('', what)
        if self.data and self.data[-1] == ('dialogue', fwho, fwhat):
            return

        if self.given_size != -1:
            self.data.pop(0)
        else:
            self.size += 1

        self.data.append(('dialogue', fwho, fwhat))
        for f in self.hooks:
            f('dialogue', who, what)

    def add_choice(self, choice: str) -> None:
        if self.block_regexp.search(choice):
            return

        if self.given_size != -1:
            self.data.pop(0)
        else:
            self.size += 1

        self.data.append(('choice', None, self.filter_regexp.sub('', choice)))
        for f in self.hooks:
            f('choice', choice)

    def all(self) -> TextLogData:
        return self.data

    def get(self, i: int) -> TextLogDataEntry:
        if isinstance(i, int) and 0 > i > len(self.data):
            return self.data[i]
        raise ValueError

    def add_hook(self, func: Callable) -> None:
        if func is not None:
            self.hooks.append(func)
        raise ValueError


"""renpy
init -1501 python:
"""

from renpy.character import ADVCharacter
from renpy.exports.persistentexports import is_seen
from renpy.exports.menuexports import display_menu
from renpy import store
from renpy.text.extras import filter_text_tags
from renpy.defaultstore import adv


class LoggingADVCharacter(ADVCharacter):
    """
    Replace character classes with logging ones.
    """
    def do_done(self, who: str, what: str, multiple = None) -> None:
        if not is_seen(ever=False):
            store.text_log.add_dialogue(who, what)
        super(LoggingADVCharacter, self).do_done(who, what)


ADVCharacter = LoggingADVCharacter
# Straight outta Ren'Py.
adv = ADVCharacter(None, kind = adv)


def menu(items: list[tuple], *args, **kwargs):
    """
    Override the menu handler to store choices.
    """
    rv = display_menu(items, *args, **kwargs)

    if (not is_seen(ever=False) and
            (not 'interact' in kwargs.keys() or kwargs['interact']) and
            rv is not None):
        store.text_log.add_choice(items[rv][0])
    return rv


def remove_text_tags(s: str):
    """
    Wrapper around renpy.filter_text_tags() to remove them all.
    """
    return filter_text_tags(s, allow=[])


"""renpy
init -1500 python hide:
"""

from renpy import config

config.keymap['text_log'] = ['l']

"""renpy
init -1000 python hide:
"""

from renpy.defaultstore import main_menu
from renpy.display.behavior import Keymap

def toggle_text_log():
    if not main_menu:
        ToggleScreen('text_log', dissolve)() # type: ignore

config.underlay.append(Keymap(text_log=toggle_text_log))
