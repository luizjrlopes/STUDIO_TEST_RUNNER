# Studio Test Runner

[English](README.md) | [Português](README.pt-BR.md)

External conformance and regression runner for **Studio V5** distributions. It does not reimplement the Studio runtime. Instead, it inspects a materialized Studio tree, executes declarative scenarios, evaluates invariants, compares snapshots, and produces evidence-rich reports.

## Why this repository exists

Studio V5 already owns routing, state, agents, writers, handoffs and gates. This project is deliberately independent: its job is to prove that a distribution still obeys those rules after changes.

The runner focuses on questions such as:

- are required files and boundaries present?
- can a Specialist write only to its own `specialist_report` inside `.studio`?
- do Area Owners stay inside their own area?
- does the Super Owner coordinate boundaries without mutating another area's local state?
- are handoff references and declared targets resolvable?
- do expected snapshots still match observed behavior?

## Quick start

No third-party runtime dependency is required for the built-in suites.

```bash
python -m studio_test_runner --help
python -m studio_test_runner run fixtures/valid --suite suites/orchestration-core.json
python -m studio_test_runner run fixtures/invalid_specialist_write --suite suites/specialist-scope.json
python -m studio_test_runner regress snapshots/baseline.json snapshots/candidate.json
```

From a source checkout, either install editable mode or set `PYTHONPATH=src`:

```bash
PYTHONPATH=src python -m studio_test_runner run fixtures/valid --suite suites/orchestration-core.json --report-dir reports
```

## Outputs

Every run can emit:

- terminal summary;
- `report.json` for automation;
- `report.md` for review;
- `report.html` for portfolio/demo use.

Exit codes:

- `0`: all assertions passed;
- `1`: at least one assertion failed;
- `2`: invalid command/input.

## Scenario format

Suites are JSON and remain intentionally declarative. Example:

```json
{
  "id": "orchestration-core",
  "assertions": [
    {"type": "path_exists", "path": ".studio/GENERAL_ORCHESTRATION"},
    {"type": "specialist_write_scope"},
    {"type": "owner_cross_area_write"}
  ]
}
```

## Design principles

- **external verifier** — never becomes a second Studio runtime;
- **deny by default** — scope assertions fail closed;
- **evidence first** — every assertion returns observed paths/details;
- **deterministic core** — no LLM required to run conformance checks;
- **portable** — Python standard library only for the core runner;
- **small surface** — assertions are composable and auditable.

See [`docs/architecture.md`](docs/architecture.md), [`docs/assertions.md`](docs/assertions.md), and [`docs/scenario-authoring.md`](docs/scenario-authoring.md).
