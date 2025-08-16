"""renpy
init -1 python:
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

    The animations are represented by `renpy.display.anim.TransitionAnimation`
    objects. These take, for each frame, a tuple consisting of a displayable
    and the time it should be shown for. Transitions in-between frames can
    be accomplished by having a 3rd argument pointint for those, but because
    we're creating these objects via the Animation function, these automatically
    get set to None.

    The folder given must contain or sub-contain all of the animation frames
    with their order reflected by numbers in their filenames. E.g., if you want
    this function to create a 10-frame animation, you're expected to number the
    animation cels from 01 to 10 and have those numbers be the filenames.

    Based on the given animation, three images will be created: one that contains
    the whole animation; one that contains a "hover" loop, and another that's just
    the first frame of the animation for "inactive" states.

    @param name: The base name of the three image objects that'll be created.
    @param folder: The path to the animation from the `game` folder (excluded). E.g.,
        `ui/side/menu_new`.
    @param fps: The frame rate of the animation.
    @param loop_frames: How many of the last few frames of the animations are to be
        used to create a "hover" loop.
    @param reverse: If we want to reverse the order of the frames of the animation.
    @param wrapper: a callable that needs to return a displayable object. This, in turn,
        is to be used to create an animation that can play itself from start to finish and
        then immediately transition to a loop. Defaults to function `call_function`, which
        simply creates a given object or calls a given function. The goal in this project
        is to use this argument with the class `ResettableDisplayable` as its value.
    """

    # Calculate the frame rate of the animation.
    frame_duration: float = 1.0 / fps

    # Get an ordered list containing the filenames of all the frames of the
    # animation. The ordering will be based on the filenames themselves.
    #
    # The `kwargs` part here is so that you are given a chance to apply
    # transforms to all of the animation frames. These can be passed on like
    # usual: as arguments that represent transform properties.
    frames: list[tuple[str | Transform, float]]
    if kwargs:
        frames = [(Transform(filename, **kwargs), frame_duration)
                  for filename in sorted(renpy_listdir(folder, full_path=True))]
    else:
        frames = [(filename, frame_duration)
                  for filename in sorted(renpy_listdir(folder, full_path=True))]

    # If the `reverse` flag is given, then the list of frames is reversed.
    if reverse:
        frames = list(reversed(frames))
    
    # Create the basic image objects containing the entire animation, `_main`,
    # and just the first frame of the animation, `_init`, for "inactive" states.
    anim: TransitionAnimation = Animation(*chain(*frames))
    image(name + '_main', anim)
    image(name + '_init', frames[0][0])

    # If we're to loop frames, then create another image containing just the loop
    # and an image that directly uses the `name` argument that contains the whole
    # animation and its loop section. This latter is the one that's meant to used
    # in "active" states.
    if loop_frames:
        loop_anim: TransitionAnimation = Animation(*chain(*frames[-loop_frames:]))
        image(name + '_loop', loop_anim)
        image(name, wrapper(
            # NOTE `showrepeat` is a transform.
            lambda: showrepeat(name + '_main', # pyright: ignore[reportUndefinedVariable]
                               len(frames) * frame_duration,
                               name + '_loop',
                               loop_frames * frame_duration)))
    # If we don't want to loop, then just create an image with the name set to the
    # `name` argument.
    else:
        image(name, wrapper(lambda: name + '_main'))
