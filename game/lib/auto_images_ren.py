"""renpy
init -1 python:
"""

# Helper function to automatically define images from a folder.

from re import compile, Pattern
from typing import Any, TYPE_CHECKING
from renpy.display.displayable import Displayable
from renpy.display.image import ImageReference
from renpy.display.transform import Transform
from renpy.exports.displayexports import image
from renpy.display.layout import MultiBox
if TYPE_CHECKING:
    from .renpy_path_ren import renpy_listdir, renpy_isdir, renpy_join
# sprite_offsets is defined in game/resources.rpy.


# NOTE GIFs and BMPs are NOT recommended by 8.4's documentation.
AUTO_IMAGE_REGEXP: Pattern = compile(r'\.(jpe?g|png|webp|avif|gif|bmp)$')


# Load all images from a certain directory.
def define_image(name: str,
                 image_path: str | MultiBox,
                 **transforms) -> None:
    if transforms:
        image(name, Transform(image_path, **transforms))
    else:
        image(name, image_path)


def define_images(dir: str,
                  base_name: list[str] = [],
                  variants: dict[str, Any] = {},
                  **transforms) -> list[str]:
    # The result which will contain a list of Ren'Py image names.
    images: list[str] = []

    for entry in renpy_listdir(dir):
        # NOTE I believe this here implies that the name of a file
        # has to have its key terms joined by underscores.
        # E.g.: ['misc', 'phone', 'emoji', 'sleepy.webp']
        name: list[str] = base_name + entry.split('_')
        path_: str = renpy_join(dir, entry)

        if renpy_isdir(path_):
            images.extend(define_images(
                path_, name, variants=variants, **transforms))
        elif AUTO_IMAGE_REGEXP.search(path_):
            # Join all of the components of a filename.
            id: str = AUTO_IMAGE_REGEXP.sub('', ' '.join(name))

            # Remove the file extension from the first component of the filename.
            # This must be for edge cases where the first one has the extension?
            # Very much unclear what the intent here was.
            nid: str = name[0].rsplit('.', 2)[0]

            # If the first component of a filename matches a character's name.
            tf: dict[str, Any]
            if nid in sprite_offsets.keys(): # pyright: ignore[reportUndefinedVariable]
                tf = transforms.copy()
                # Get the vertical offset and apply it to all the transforms
                # that are to be applied to each image.
                tf['yoffset'] = sprite_offsets[nid] # pyright: ignore[reportUndefinedVariable]
            else:
                tf = transforms

            # Create the image.
            define_image(id, path_, **tf)
            images.append(id)

            # Create the image variants.
            for variant_name, variant_func in variants.items():
                variant_id = id + ' ' + variant_name
                define_image(variant_id, variant_func(id, path_), **tf)
                images.append(variant_id)

    return images


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
