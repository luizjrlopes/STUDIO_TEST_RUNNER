from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _index(payload: dict[str, Any]) -> dict[str, bool]:
    results = payload.get("results", [])
    return {str(item.get("assertion_id")): bool(item.get("passed")) for item in results if isinstance(item, dict)}


def compare_snapshots(baseline: str | Path, candidate: str | Path) -> dict[str, Any]:
    base = json.loads(Path(baseline).read_text(encoding="utf-8"))
    current = json.loads(Path(candidate).read_text(encoding="utf-8"))
    b = _index(base)
    c = _index(current)
    regressions = sorted(key for key, passed in b.items() if passed and c.get(key) is False)
    improvements = sorted(key for key, passed in b.items() if not passed and c.get(key) is True)
    added = sorted(set(c) - set(b))
    removed = sorted(set(b) - set(c))
    return {"baseline": str(baseline), "candidate": str(candidate), "regressions": regressions, "improvements": improvements, "added_assertions": added, "removed_assertions": removed, "passed": not regressions and not removed}
