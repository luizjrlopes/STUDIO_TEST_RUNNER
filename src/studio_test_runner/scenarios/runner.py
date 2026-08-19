from __future__ import annotations

from pathlib import Path
from typing import Any

from ..assertions import evaluate_assertion
from ..discovery import discover_tree
from ..models import SuiteResult


def run_suite(target: str | Path, suite: dict[str, Any], *, fail_fast: bool = False) -> SuiteResult:
    tree = discover_tree(target)
    results = []
    for index, assertion in enumerate(suite["assertions"], start=1):
        result = evaluate_assertion(tree, assertion, index)
        results.append(result)
        if fail_fast and not result.passed:
            break
    return SuiteResult(suite_id=suite["id"], target=str(tree.root), results=results)
