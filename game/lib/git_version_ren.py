"""renpy
init python:
"""

from pathlib import Path

# Get git version.
def git_version() -> str:
    if hasattr(store, "git_revision"):
        return store.git_revision

    git_dir: Path = Path(config.gamedir).parent / ".git"
    if git_dir.is_dir():
        head: Path = git_dir / "HEAD"
        with open(head, 'r') as f:
            parts: list[str] = f.read().strip().split()

        if parts[0] == 'ref:':
            ref: Path = git_dir / parts[1]
            with open(ref, 'r') as f:
                rev: str = f.read().strip()
        else:
            rev: str = parts[0]

        return rev[:7]

    return "[unknown]"
