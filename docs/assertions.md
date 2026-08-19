# Built-in assertions

## `path_exists`
Requires one path to exist in the target.

## `path_absent`
Requires one path not to exist.

## `glob_count`
Checks the number of files matching a glob pattern. Accepts `min` and optional `max`.

## `json_files_valid`
Parses JSON files and returns evidence for malformed payloads.

## `handoff_targets_resolve`
Reads `handoff.json` files and verifies that declared target areas and target agents exist.

## `specialist_write_scope`
Reads observed `write-manifest.json` files. A manifest with `actor_level: SPECIALIST` may write only the `specialist_report.json` adjacent to that manifest.

## `owner_cross_area_write`
Checks observed owner writes. An Area Owner must remain in its own area; the General Orchestration Super Owner may write inside General Orchestration but not another executor area's local state.

### Why write manifests?

A static tree cannot prove who wrote a file. Fixtures and integration harnesses therefore materialize observed writes into `write-manifest.json`. This keeps the conformance runner deterministic instead of pretending provenance can be inferred from filenames.
