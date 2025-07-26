"""renpy
init -500 python:
"""


from renpy.display.displayable import Displayable
from renpy.display.image import ImageReference, DynamicImage
from renpy.easy import displayable

class ResettableDisplayable(Displayable):
    """
    Resettable animation displayables.
    """
    # Thanks to Asceai on Freenode.

    def __init__(self, child, **kwargs):
        super(ResettableDisplayable, self).__init__(**kwargs)
        self.base = child
        self.child = displayable(self.base())
        self.st_reset = 0.0
        self.at_reset = 0.0
        self.reset = False

    def render(self, width, height, st, at):
        if self.reset:
            self.child = displayable(self.base())
            self.st_reset = st
            self.at_reset = at
            self.reset = False

        return renpy.render(
            self.child, width, height, st - self.st_reset, at - self.at_reset)

    def Reset(self):
        return SetField(self, "reset", True)

    def visit(self):
        return [ self.child ]

def ResetDisplayable(disp):
    targetref = displayable(disp)
    if isinstance(targetref, ImageReference) or isinstance(targetref, DynamicImage):
        targetref.find_target()
        return targetref.target.Reset()

class CappedDisplayable(Displayable):
    def __init__(self, child, cap, **kwargs):
        super(CappedDisplayable, self).__init__(**kwargs)
        self.child = displayable(child)
        self.cap = cap

    def render(self, width, height, st, at):
        return renpy.render(
            self.child, width, height, min(self.cap, st), min(self.cap, at))
