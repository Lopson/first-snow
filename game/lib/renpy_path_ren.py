"""renpy
init -100 python:
"""
# Functions for trivial I/O inspection in Ren'Py as a
# replacement for the ones in os.path.

from renpy.exports.loaderexports import list_files

all_files: list[str] = list_files()


def renpy_isdir(path) -> bool:
    return any(x for x in all_files if x.startswith(path + '/'))


def renpy_isfile(path: str) -> bool:
    return path in all_files


def renpy_exists(path: str) -> bool:
    return renpy_isfile(path) or renpy_isdir(path)


def renpy_join(*args: str) -> str:
    return '/'.join(args)


def renpy_listdir(
        path: str,
        full_path: bool = False,
        recursive: bool = False) -> set[str]:
    results: set[str] = set()

    file: str
    for file in all_files:
        if file.startswith(path + '/'):
            entry: str
            if not recursive:
                entry = file.replace(path + '/', '', 1)
                entry = entry.split('/', 1)[0]
            else:
                entry = file

            if full_path:
                results.add(path + '/' + entry)
            else:
                results.add(entry)

    return results
