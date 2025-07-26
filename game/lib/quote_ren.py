"""renpy
init python:
"""

## Function to escape text for safe use in Ren'Py.
def renpy_quote(text: str) -> str:
    if text and isinstance(text, str):
        return text.replace('[', '[[').replace('{', '{{')
    else:
        raise ValueError
