"""renpy
init python:
"""

# TODO This doesn't seem to be used anywhere, delete.

from typing import Any
from renpy import config
from renpy.text.textsupport import TAG as TEXT_TAG # pyright: ignore[reportMissingImports]     


def url_tag(
        tag: str,
        argument: str,
        contents: list[tuple[Any, str]]) -> list[tuple[Any, str]]:
    return [(TEXT_TAG, u'a={}'.format(contents[0][1]))] + \
        contents + \
        [(TEXT_TAG, u'/a')]


config.custom_text_tags['url'] = url_tag
