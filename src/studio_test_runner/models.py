from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Evidence:
    path: str | None = None
    detail: str | None = None
    observed: Any = None
    expected: Any = None


@dataclass(slots=True)
class AssertionResult:
    assertion_id: str
    assertion_type: str
    passed: bool
    message: str
    evidence: list[Evidence] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"assertion_id": self.assertion_id, "assertion_type": self.assertion_type, "passed": self.passed, "message": self.message, "evidence": [asdict(item) for item in self.evidence]}


@dataclass(slots=True)
class SuiteResult:
    suite_id: str
    target: str
    results: list[AssertionResult]

    @property
    def passed(self) -> bool:
        return all(item.passed for item in self.results)

    @property
    def passed_count(self) -> int:
        return sum(item.passed for item in self.results)

    @property
    def failed_count(self) -> int:
        return len(self.results) - self.passed_count

    def to_dict(self) -> dict[str, Any]:
        return {"suite_id": self.suite_id, "target": self.target, "passed": self.passed, "summary": {"total": len(self.results), "passed": self.passed_count, "failed": self.failed_count}, "results": [item.to_dict() for item in self.results]}


@dataclass(slots=True)
class StudioTree:
    root: Path
    files: tuple[str, ...]
    directories: tuple[str, ...]

    def exists(self, relative_path: str) -> bool:
        normalized = relative_path.strip("/")
        return normalized in self.files or normalized in self.directories
