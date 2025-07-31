"""renpy
init python:
"""

from itertools import chain
from typing import Any, Callable, TYPE_CHECKING
from renpy.display.anim import Animation, TransitionAnimation
from renpy.display.transform import Transform
from renpy.exports.displayexports import image
if TYPE_CHECKING:
    from .renpy_path_ren import renpy_listdir


def call_function(x: Callable) -> Any: return x()


def animation_from_folder(name: str,
                          folder: str,
                          fps: int = 12,
                          loop_frames: int = 3,
                          reverse: bool = False,
                          wrapper: Callable = call_function,
                          **kwargs) -> None:
    """
    Helper function to define an animation from a set of files in a folder.
    This function assumes a workflow of having X intro frames and Y <= X loop
    frames (default Y = 3).

    The animations are represented by renpy.display.anim.TransitionAnimation
    objects. These take, for each frame, a tuple consisting of a displayable
    and the time it should be shown for. Transitions in-between frames can
    be accomplished by having a 3rd argument pointint for those, but because
    we're creating these objects via the Animation function, these automatically
    get set to None.
    """
    frame_duration: float = 1.0 / fps
    frames: list[tuple[str | Transform, float]]
    if kwargs:
        frames = [(Transform(filename, **kwargs), frame_duration)
                  for filename in sorted(renpy_listdir(folder, full_path=True))]
    else:
        frames = [(filename, frame_duration)
                  for filename in sorted(renpy_listdir(folder, full_path=True))]

    if reverse:
        frames = list(reversed(frames))
    anim: TransitionAnimation = Animation(*chain(*frames))
    image(name + '_main', anim)
    image(name + '_init', frames[0][0])

    if loop_frames:
        loop_anim: TransitionAnimation = Animation(*chain(*frames[-loop_frames:]))
        image(name + '_loop', loop_anim)
        image(name, wrapper(
            lambda: showrepeat(name + '_main', # pyright: ignore[reportUndefinedVariable]
                               len(frames) * frame_duration,
                               name + '_loop',
                               loop_frames * frame_duration)))
    else:
        image(name, wrapper(lambda: name + '_main'))
