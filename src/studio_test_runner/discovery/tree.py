from __future__ import annotations

from pathlib import Path

from ..models import StudioTree


def discover_tree(root: str | Path) -> StudioTree:
    base = Path(root).expanduser().resolve()
    if not base.exists():
        raise FileNotFoundError(f"Target does not exist: {base}")
    if not base.is_dir():
        raise NotADirectoryError(f"Target is not a directory: {base}")
    files: list[str] = []
    directories: list[str] = []
    for path in sorted(base.rglob("*")):
        relative = path.relative_to(base).as_posix()
        if any(part in {".git", "__pycache__"} for part in path.parts):
            continue
        if path.is_dir():
            directories.append(relative)
        elif path.is_file():
            files.append(relative)
    return StudioTree(root=base, files=tuple(files), directories=tuple(directories))
