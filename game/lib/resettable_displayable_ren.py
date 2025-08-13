"""renpy
init -500 python:
"""


from typing import Callable
from renpy.display.displayable import Displayable
from renpy.display.image import ImageReference, DynamicImage
from renpy.easy import displayable
from renpy.display.render import Render, render # pyright: ignore[reportMissingImports]

class ResettableDisplayable(Displayable):
    """
    Resettable animation displayables.
    """
    # Thanks to Asceai on Freenode.

    def __init__(self, child: Callable, **kwargs) -> None:
        super(ResettableDisplayable, self).__init__(**kwargs)
        self.base = child
        self.child = displayable(self.base())
        self.st_reset: float = 0.0
        self.at_reset: float = 0.0
        self.reset: bool = False

    def render(self, width: int, height: int, st: float, at: float) -> Render:
        if self.reset:
            self.child = displayable(self.base())
            self.st_reset = st
            self.at_reset = at
            self.reset = False

        return render(
            self.child, width, height, st - self.st_reset, at - self.at_reset)

    def Reset(self):
        return SetField(self, "reset", True) # pyright: ignore[reportUndefinedVariable]

    def visit(self) -> list:
        return [ self.child ]

def ResetDisplayable(disp: str):
    targetref = displayable(disp)
    
    if isinstance(targetref, ImageReference) or isinstance(targetref, DynamicImage):
        targetref.find_target()
        return targetref.target.Reset() # type: ignore

class CappedDisplayable(Displayable):
    def __init__(self, child: Displayable | str, cap, **kwargs) -> None:
        super(CappedDisplayable, self).__init__(**kwargs)
        self.child = displayable(child)
        self.cap = cap

    def render(self, width, height, st, at) -> Render:
        return render(
            self.child, width, height, min(self.cap, st), min(self.cap, at))
