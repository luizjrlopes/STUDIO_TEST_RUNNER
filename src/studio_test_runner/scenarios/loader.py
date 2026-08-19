from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_suite(path: str | Path) -> dict[str, Any]:
    suite_path = Path(path)
    with suite_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Suite root must be a JSON object")
    if not isinstance(payload.get("id"), str) or not payload["id"].strip():
        raise ValueError("Suite must define a non-empty string id")
    assertions = payload.get("assertions")
    if not isinstance(assertions, list) or not assertions:
        raise ValueError("Suite must define a non-empty assertions list")
    for index, item in enumerate(assertions, start=1):
        if not isinstance(item, dict) or not isinstance(item.get("type"), str):
            raise ValueError(f"Assertion #{index} must be an object with a type")
    return payload
