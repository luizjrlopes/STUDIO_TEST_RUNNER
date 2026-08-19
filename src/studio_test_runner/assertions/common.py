from __future__ import annotations

import fnmatch
import json
from pathlib import Path
from typing import Iterable

from ..models import Evidence


def matching_paths(paths: Iterable[str], pattern: str) -> list[str]:
    return [path for path in paths if fnmatch.fnmatch(path, pattern)]


def load_json_files(root: Path, paths: Iterable[str]) -> list[tuple[str, object]]:
    loaded: list[tuple[str, object]] = []
    for relative in paths:
        path = root / relative
        try:
            loaded.append((relative, json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError):
            continue
    return loaded


def evidence_for_paths(paths: Iterable[str], detail: str) -> list[Evidence]:
    return [Evidence(path=item, detail=detail) for item in paths]
