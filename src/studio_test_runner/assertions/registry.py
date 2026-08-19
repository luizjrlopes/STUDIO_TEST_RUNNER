from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any, Callable

from ..models import AssertionResult, Evidence, StudioTree
from .common import matching_paths

AssertionFn = Callable[[StudioTree, dict[str, Any], str], AssertionResult]


def _id(spec: dict[str, Any], index: str) -> str:
    return str(spec.get("id") or index)


def path_exists(tree: StudioTree, spec: dict[str, Any], index: str) -> AssertionResult:
    path = str(spec.get("path", "")).strip("/")
    passed = bool(path) and tree.exists(path)
    return AssertionResult(_id(spec, index), "path_exists", passed,
        f"Path {'exists' if passed else 'is missing'}: {path}",
        [Evidence(path=path, observed=passed, expected=True)])


def path_absent(tree: StudioTree, spec: dict[str, Any], index: str) -> AssertionResult:
    path = str(spec.get("path", "")).strip("/")
    passed = bool(path) and not tree.exists(path)
    return AssertionResult(_id(spec, index), "path_absent", passed,
        f"Path {'is absent' if passed else 'unexpectedly exists'}: {path}",
        [Evidence(path=path, observed=not passed, expected=False)])


def glob_count(tree: StudioTree, spec: dict[str, Any], index: str) -> AssertionResult:
    pattern = str(spec.get("pattern", ""))
    found = matching_paths(tree.files, pattern)
    minimum = int(spec.get("min", 0))
    maximum = spec.get("max")
    passed = len(found) >= minimum and (maximum is None or len(found) <= int(maximum))
    expected = {"min": minimum, "max": maximum}
    return AssertionResult(_id(spec, index), "glob_count", passed,
        f"Pattern {pattern} matched {len(found)} file(s)",
        [Evidence(path=item, detail="matched") for item in found] + [Evidence(observed=len(found), expected=expected)])


def specialist_write_scope(tree: StudioTree, spec: dict[str, Any], index: str) -> AssertionResult:
    manifests = matching_paths(tree.files, "**/write-manifest.json")
    violations: list[Evidence] = []
    inspected = 0
    import json
    for relative in manifests:
        payload = json.loads((tree.root / relative).read_text(encoding="utf-8"))
        if payload.get("actor_level") != "SPECIALIST":
            continue
        inspected += 1
        writes = payload.get("writes", [])
        specialist_root = PurePosixPath(relative).parent
        expected_report = str(specialist_root / "specialist_report.json")
        for target in writes:
            normalized = str(PurePosixPath(str(target)))
            if normalized != expected_report:
                violations.append(Evidence(path=normalized, detail=f"SPECIALIST write outside own report; expected only {expected_report}"))
    passed = not violations
    message = f"Specialist write scope valid across {inspected} manifest(s)" if passed else f"Detected {len(violations)} Specialist write-scope violation(s)"
    return AssertionResult(_id(spec, index), "specialist_write_scope", passed, message, violations or [Evidence(observed=inspected, detail="specialist manifests inspected")])


def owner_cross_area_write(tree: StudioTree, spec: dict[str, Any], index: str) -> AssertionResult:
    manifests = matching_paths(tree.files, "**/write-manifest.json")
    violations: list[Evidence] = []
    inspected = 0
    import json
    for relative in manifests:
        payload = json.loads((tree.root / relative).read_text(encoding="utf-8"))
        level = payload.get("actor_level")
        if level not in {"AREA_OWNER", "SUPER_OWNER"}:
            continue
        inspected += 1
        area = payload.get("area")
        for target in payload.get("writes", []):
            parts = PurePosixPath(str(target)).parts
            if len(parts) < 2 or parts[0] != ".studio":
                continue
            target_area = parts[1]
            if level == "AREA_OWNER" and area and target_area != area:
                violations.append(Evidence(path=str(target), detail=f"AREA_OWNER from {area} attempted write in {target_area}"))
            if level == "SUPER_OWNER" and area == "GENERAL_ORCHESTRATION" and target_area not in {"GENERAL_ORCHESTRATION"}:
                violations.append(Evidence(path=str(target), detail=f"SUPER_OWNER attempted local write inside {target_area}"))
    passed = not violations
    return AssertionResult(_id(spec, index), "owner_cross_area_write", passed,
        f"Owner write boundaries valid across {inspected} manifest(s)" if passed else f"Detected {len(violations)} cross-area owner write violation(s)",
        violations or [Evidence(observed=inspected, detail="owner manifests inspected")])


def handoff_targets_resolve(tree: StudioTree, spec: dict[str, Any], index: str) -> AssertionResult:
    manifests = matching_paths(tree.files, "**/handoff.json")
    violations: list[Evidence] = []
    import json
    for relative in manifests:
        payload = json.loads((tree.root / relative).read_text(encoding="utf-8"))
        target_area = payload.get("target_area")
        target_agent = payload.get("target_agent")
        if target_area and not tree.exists(f".studio/{target_area}"):
            violations.append(Evidence(path=relative, detail=f"target area missing: {target_area}"))
        if target_area and target_agent:
            candidates = [p for p in tree.directories if p.endswith(f"/agents/{target_agent}") and p.startswith(f".studio/{target_area}/")]
            if not candidates:
                violations.append(Evidence(path=relative, detail=f"target agent missing: {target_agent} in {target_area}"))
    passed = not violations
    return AssertionResult(_id(spec, index), "handoff_targets_resolve", passed,
        f"Resolved {len(manifests)} handoff target(s)" if passed else f"Detected {len(violations)} unresolved handoff reference(s)",
        violations or [Evidence(observed=len(manifests), detail="handoffs inspected")])


def json_files_valid(tree: StudioTree, spec: dict[str, Any], index: str) -> AssertionResult:
    import json
    pattern = str(spec.get("pattern", "**/*.json"))
    paths = matching_paths(tree.files, pattern)
    errors: list[Evidence] = []
    for relative in paths:
        try:
            json.loads((tree.root / relative).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(Evidence(path=relative, detail=str(exc)))
    passed = not errors
    return AssertionResult(_id(spec, index), "json_files_valid", passed,
        f"Validated {len(paths)} JSON file(s)" if passed else f"Detected {len(errors)} invalid JSON file(s)", errors or [Evidence(observed=len(paths))])


REGISTRY: dict[str, AssertionFn] = {
    "path_exists": path_exists,
    "path_absent": path_absent,
    "glob_count": glob_count,
    "specialist_write_scope": specialist_write_scope,
    "owner_cross_area_write": owner_cross_area_write,
    "handoff_targets_resolve": handoff_targets_resolve,
    "json_files_valid": json_files_valid,
}


def evaluate_assertion(tree: StudioTree, spec: dict[str, Any], index: int) -> AssertionResult:
    assertion_type = spec.get("type")
    fn = REGISTRY.get(str(assertion_type))
    if fn is None:
        return AssertionResult(str(spec.get("id") or index), str(assertion_type), False, f"Unknown assertion type: {assertion_type}")
    try:
        return fn(tree, spec, str(index))
    except Exception as exc:
        return AssertionResult(str(spec.get("id") or index), str(assertion_type), False, f"Assertion raised {type(exc).__name__}: {exc}")
