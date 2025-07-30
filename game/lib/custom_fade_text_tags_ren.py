"""renpy
init python hide:
"""

# NOTE Candidate for removal as no use of these tags was found.
# Additionally, we can do this with ATL statements on the
# dialogue line itself these days.

from typing import Any
from renpy import config
from renpy.text.textsupport import ( # pyright: ignore[reportMissingImports]
    TAG as TEXT_TAG, TEXT as TEXT_TEXT
)


def fade(
        tag: str,
        argument: str,
        contents: list[tuple[Any, str]]) -> list[tuple[Any, str]]:
    new: list[tuple[Any, str]] = []
    tags: int = 0
    delta: float

    if ',' in argument:
        start, end = [float(x) for x in argument.split(',', 1)]
        delta = end - start
        new.append((TEXT_TAG, 'alpha={}'.format(start)))
        tags += 1
    else:
        delta = float(argument)

    amount: int = sum(len(s) for (t, s) in contents if t == TEXT_TEXT)
    step: float = delta / amount

    for (type, value) in contents:
        if type == TEXT_TEXT:
            for c in value:
                new.append((TEXT_TAG, 'alpha=+{}'.format(step)))
                new.append((TEXT_TEXT, c))
                tags += 1
        else:
            new.append((type, value))

    for _ in range(tags):
        new.append((TEXT_TAG, '/alpha'))

    return new

def fade_size(tag: str,
              argument: str,
              contents: list[tuple[Any, str]]) -> list[tuple[Any, str]]:
    new: list[tuple[Any, str]] = []
    tags: int = 0
    delta: float

    if ',' in argument:
        start, end = [int(x) for x in argument.split(',', 1)]
        delta = float(end - start)
        new.append((TEXT_TAG, 'size={}'.format(start)))
        tags += 1
    else:
        delta = float(argument)

    amount: int = sum(len(s) for (t, s) in contents if t == TEXT_TEXT)
    step: float = delta / amount
    intermediate: float = 0.0

    for (type, value) in contents:
        if type == TEXT_TEXT:
            for c in value:
                intermediate += step
                if round(intermediate) >= 1:
                    increment: int = int(round(intermediate))
                    intermediate -= increment
                    new.append((TEXT_TAG, 'size=+{}'.format(increment)))
                    tags += 1
                new.append((TEXT_TEXT, c))
        else:
            new.append((type, value))

    for _ in range(tags):
        new.append((TEXT_TAG, '/size'))

    return new

config.custom_text_tags['fade'] = fade
config.custom_text_tags['fadesize'] = fade_size
