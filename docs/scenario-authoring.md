# Scenario authoring

Suites are JSON objects with an `id` and a non-empty `assertions` array.

```json
{
  "id": "my-suite",
  "assertions": [
    {"id": "root", "type": "path_exists", "path": ".studio"}
  ]
}
```

Keep one assertion focused on one invariant. Prefer explicit evidence over broad pass/fail labels.

## Fixture convention

A fixture is a small synthetic project/Studio tree. It should contain only the elements required to demonstrate the behavior under test. Invalid fixtures are first-class and should fail for one known reason.

## Observed writes

Use `write-manifest.json` next to the actor fixture:

```json
{
  "actor_level": "SPECIALIST",
  "area": "WEB_FRONTEND",
  "writes": [
    ".studio/WEB_FRONTEND/agents/AG_WEB_A02/result/specialist_report.json"
  ]
}
```
