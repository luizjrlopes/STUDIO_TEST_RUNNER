#!/usr/bin/env sh
set -eu
PYTHONPATH=src python -m studio_test_runner run fixtures/valid --suite suites/orchestration-core.json --report-dir reports
