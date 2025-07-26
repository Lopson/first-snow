"""renpy
init python:
"""


def renpy_quote(text: str) -> str:
    """
    Function to escape text for safe use in Ren'Py.
    """
    if text and isinstance(text, str):
        return text.replace('[', '[[').replace('{', '{{')
    else:
        raise ValueError
