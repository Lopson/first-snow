"""renpy
init -1 python:
"""

# Image-related helper functions.

from renpy.display.displayable import Displayable
from renpy.display.image import ImageReference
from renpy.display.transform import Transform


def get_base_image(image_name: str) -> Displayable | None:
    """
    This function gets the root displayable of a given image that's
    already been defined.

    @param image_name: The name of an image definition.
    @return: The displayable that corresponds to the given name.
    """

    ref: ImageReference = ImageReference(image_name)

    # If we can't find the target of a given displayable, then bail.
    if not ref.find_target():
        return None
    if ref.target is None:
        return None
    
    src: Displayable = ref.target
    
    # Let's try to get the actual root displayable that may be nested
    # within a bunch of `Transform`s.
    while True:
        if not isinstance(src, Transform):
            break
        if src.child is None:
            return None
        src = src.child
    
    return src
