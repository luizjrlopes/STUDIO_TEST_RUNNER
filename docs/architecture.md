# Architecture

The runner has five deliberately small layers:

1. **discovery** scans a target tree without mutating it;
2. **scenario loader** validates declarative suites;
3. **assertions** evaluate deterministic invariants;
4. **reporting** turns results into terminal/JSON/Markdown/HTML evidence;
5. **regression** compares result snapshots between Studio versions.

The runner never writes into the inspected Studio target. Its only writes are reports in the user-selected report directory.

## Authority model verified by built-in assertions

The built-in scope assertions encode a narrow subset of Studio V5 invariants useful for regression:

- Specialist: focal execution; inside `.studio`, its observed writes must be limited to its own `specialist_report`;
- Area Owner: local coordination; cannot write another area's local state;
- Super Owner: global coordination through boundaries; cannot mutate another executor area's local state directly;
- writer/script effects should be represented as explicit observed writes rather than inferred from prose.

The runner is extensible: add an assertion function to `assertions/registry.py` and reference its `type` from a suite.
