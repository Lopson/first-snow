"""renpy
init -1500 python:
"""

# NOTE I see no reason to keep this piece of code.

from pathlib import Path
from typing import TYPE_CHECKING
from renpy.exports.actionexports import notify
from renpy.exports.displayexports import screenshot
from renpy import macapp
if TYPE_CHECKING:
    from renpy import config
    from renpy.minstore import __

# Called to make a screenshot happen.
def _screenshot():
    """
    _screenshot variant that tries multiple directories before giving up,
    in case the user has no permission to write to the game directory.
    """

    import os.path
    import os

    # Primary directory: the game.
    paths: list[str]
    paths = [config.renpy_base]
    if macapp:
        paths = []

    # Secondary directories: the destkop.
    # for p in [os.path.expanduser(b"~/Desktop")]:
    for p in [Path.home() / "Desktop"]:
        if p.exists() and p.is_dir():
            paths.append(str(p))

    for dest in paths:
        # Try to pick a filename.
        i: int = 1
        fn: Path
        while True:
            fn = Path(dest) / (config.screenshot_pattern % i) # pyright: ignore[reportAttributeAccessIssue]
            if not fn.exists():
                break
            i += 1

        try:
            if not Path.exists(fn.parent):
                Path.mkdir(fn.parent)
        except:
            pass

        try:
            if screenshot(str(fn)):
                break
        except:
            import traceback
            traceback.print_exc()
    else:
        notify(__("Failed to save screenshot."))
        return

    if config.screenshot_callback is not None: # pyright: ignore[reportAttributeAccessIssue]
        config.screenshot_callback(fn) # pyright: ignore[reportAttributeAccessIssue]
