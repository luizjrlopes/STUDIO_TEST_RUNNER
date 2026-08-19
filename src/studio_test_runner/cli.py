from __future__ import annotations

import argparse
import json
import os

from .regression import compare_snapshots
from .reporting import write_reports
from .scenarios import load_suite, run_suite


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="studio-test-runner", description="Conformance and regression runner for Studio V5")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Run a declarative conformance suite")
    run.add_argument("target", help="Studio/project directory to inspect")
    run.add_argument("--suite", required=True, help="Path to suite JSON")
    run.add_argument("--report-dir", default=os.getenv("STUDIO_TEST_RUNNER_REPORT_DIR", "reports"))
    run.add_argument("--fail-fast", action="store_true", default=os.getenv("STUDIO_TEST_RUNNER_FAIL_FAST", "false").lower() == "true")
    run.add_argument("--json", action="store_true", help="Print machine-readable result to stdout")
    regress = sub.add_parser("regress", help="Compare two runner JSON snapshots")
    regress.add_argument("baseline")
    regress.add_argument("candidate")
    regress.add_argument("--json", action="store_true")
    return parser


def _run(args: argparse.Namespace) -> int:
    suite = load_suite(args.suite)
    result = run_suite(args.target, suite, fail_fast=args.fail_fast)
    paths = write_reports(result, args.report_dir)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False))
    else:
        print(f"Suite: {result.suite_id}")
        for item in result.results:
            print(f"{'PASS' if item.passed else 'FAIL'}  {item.assertion_id:<28} {item.message}")
        print(f"\n{result.passed_count}/{len(result.results)} assertions passed")
        print(f"Reports: {paths['html']} | {paths['json']} | {paths['markdown']}")
    return 0 if result.passed else 1


def _regress(args: argparse.Namespace) -> int:
    result = compare_snapshots(args.baseline, args.candidate)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Regressions: {len(result['regressions'])}")
        for item in result["regressions"]:
            print(f"FAIL  {item}")
        for item in result["improvements"]:
            print(f"PASS  {item} (improved)")
        if result["removed_assertions"]:
            print("Removed assertions: " + ", ".join(result["removed_assertions"]))
    return 0 if result["passed"] else 1


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            return _run(args)
        if args.command == "regress":
            return _regress(args)
    except (FileNotFoundError, NotADirectoryError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    return 2
