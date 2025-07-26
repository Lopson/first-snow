"""renpy
init -5 python:
"""

from typing import TYPE_CHECKING
from time import time
from renpy.exports.displayexports import restart_interaction
from renpy.display import screen
if TYPE_CHECKING:
    from renpy import store
    from renpy import config

store._screenshot_taken = 0.0


def screenshot_callback(_) -> None:
    store._screenshot_taken = time()
    restart_interaction()


def screenshot_overlay() -> None:
    if not screen.has_screen('screenshot_indicator'):
        return
    if not screen.get_screen('screenshot_indicator') and store._screenshot_taken:
        screen.show_screen('screenshot_indicator')
    elif (screen.get_screen('screenshot_indicator') and
            time() - store._screenshot_taken > 4.0):
        screen.hide_screen('screenshot_indicator')
        store._screenshot_taken = 0.0


config.screenshot_callback = screenshot_callback # pyright: ignore[reportAttributeAccessIssue]
config.overlay_functions.append(screenshot_overlay)
