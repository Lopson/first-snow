"""renpy
init -1 python:
"""

# NOTE This file is also a prime candidate for deletion.
# While this is a really smart way of initializing images,
# it's also incredibly obscure and undocumented. Instead of
# doing this, let's instead use Ren'Py's default behaviors or
# create our own LayeredImages. That way, everything is explicit
# and easy to modify moving forward.

# Helper function to automatically define images from a folder.

from itertools import product
from re import compile, Pattern
from typing import Any, Callable, TYPE_CHECKING
from renpy.display.image import list_images, ImageReference
from renpy.display.transform import Transform
from renpy.exports.displayexports import image
from renpy.display.layout import MultiBox
if TYPE_CHECKING:
    from renpy.defaultstore import Fixed
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


def FittingComposite(parts: list[str]) -> MultiBox:
    img: MultiBox = Fixed(xfit=True, yfit=True)
    for widget in parts:
        img.add(widget)

    return img


def define_dynamic_images(dir: str,
                          base_name: list[str] = [],
                          variants: dict[str, Any] = {},
                          **transforms) -> list[str]:
    images: list[str] = []

    # Iterate over all base folders present in `dir`.
    # The typical use-case here seems to e.g. point to a directory with sprites
    # in them and each folder in `dir` represents a different character or
    # version of a character.
    for base in renpy_listdir(dir):
        print(base)
        bpath: str = renpy_join(dir, base)
        if not renpy_isdir(bpath):
            continue

        # If a folder name has underscores, those are meant to represent
        # different version of the same thing. We want to split those for
        # naming purposes later on in this function. E.g., "eileen" and
        # "eileen_right".
        bname: list[str] = base_name + base.split('_')
        parts: list[list[None | tuple[str, str, str]]] = []

        # Iterate over all the attribute/parts/layer folders of a given
        # folder in `dir`. E.g., go over all of the folders within "eileen".
        for part in renpy_listdir(bpath):
            ppath = renpy_join(bpath, part)
            if not renpy_isdir(ppath):
                continue

            # A folder whose name starts with an underscore is considered
            # "optional" according to the original comment.
            if part.startswith('_'):
                parts.append([None])
                # "Make sure optionals sort last." Unsure why this would
                # be necessary?
                part = 'z' + part
            else:
                parts.append([])

            # Find all the images in the attribute/part/layer folder
            # we're currently on. We're on O(n^3) complexity at this point,
            # which is highly inefficient...
            for x in renpy_listdir(ppath):
                if AUTO_IMAGE_REGEXP.search(x):
                    name: str = AUTO_IMAGE_REGEXP.sub('', x)
                    parts[-1].append((part, name, renpy_join(ppath, x)))

            # No images found in this folder? don't count it at all.
            if not parts[-1] or parts[-1] is None:
                del parts[-1]

        # If the first component of a filename matches a character's name.
        tf: dict[str, Any]
        if base in sprite_offsets.keys(): # pyright: ignore[reportUndefinedVariable]
            # Get the vertical offset and apply it to all the transforms
            # that are to be applied to each image.
            tf = transforms.copy()
            tf['yoffset'] = sprite_offsets[base] # pyright: ignore[reportUndefinedVariable]
        else:
            tf = transforms

        # Iterate over all possible cross-combinations and create the images.
        for combo in product(*parts):
            combo = sorted(v for v in combo if v is not None)
            pname: list[str] = [name for (_, name, _) in combo]

            id: str = ' '.join(bname + pname)
            img: MultiBox = FittingComposite(
                list(file for (_, _, file) in combo))
            define_image(id, img, **tf)
            images.append(id)

            for vname, vfunc in variants.items():
                vid: str = id + ' ' + vname
                vimg: MultiBox = FittingComposite(
                    list(vfunc(id, file) for (_, _, file) in combo))
                define_image(vid, vimg, **tf)
                images.append(vid)

    return images


def apply_image_variants(name: str,
                         func: Callable,
                         base_name: str | None = None) -> None:
    image_name: str
    for image_name in list_images():
        if base_name and not image_name.startswith(base_name):
            continue

        image_ref: ImageReference = ImageReference(image_name)
        variant = func(image_name, image_ref)
        image(image_name + ' ' + name, variant)
