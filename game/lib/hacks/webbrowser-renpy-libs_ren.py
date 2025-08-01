# Hotfix to prevent Ren'Py library environment from messing with running web
# browsers on Linux.

"""renpy
init python:
"""

# NOTE Another piece of code that I don't think is necessary anymore.

import os
from contextlib import contextmanager
from typing import Iterator, Self, TYPE_CHECKING
from webbrowser import open_new
from renpy.pyanalysis import pure
if TYPE_CHECKING:
    from renpy import config
    from renpy.ui import Action


@contextmanager
def without_renpy_libs() -> Iterator[None]:
    libpath: str | None = os.getenv('LD_LIBRARY_PATH')
    gamedir: str = os.path.dirname(config.gamedir)
    if libpath:
        paths: list[str] = libpath.split(os.pathsep)
        filtered_paths: list[str] = [p for p in paths if not p.startswith(gamedir)]
        os.environ['LD_LIBRARY_PATH'] = os.pathsep.join(filtered_paths)
    yield
    if libpath:
        os.environ['LD_LIBRARY_PATH'] = libpath


@pure
class OpenURL(Action):
    def __init__(self: Self, url: str) -> None:
        self.url = url

    def __call__(self: Self) -> None:
        try:
            with without_renpy_libs():
                open_new(self.url)
        except:
            pass
