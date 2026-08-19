from __future__ import annotations

import html
import json
from pathlib import Path

from ..models import SuiteResult


def _markdown(result: SuiteResult) -> str:
    lines = [f"# Studio Test Runner — {result.suite_id}", "", f"Target: `{result.target}`", "", f"Result: **{'PASS' if result.passed else 'FAIL'}** — {result.passed_count}/{len(result.results)} assertions passed.", "", "| Status | Assertion | Type | Message |", "|---|---|---|---|"]
    for item in result.results:
        message = item.message.replace("|", "\\|")
        lines.append(f"| {'PASS' if item.passed else 'FAIL'} | {item.assertion_id} | {item.assertion_type} | {message} |")
        for ev in item.evidence:
            detail = ev.detail or "evidence"
            path = f" `{ev.path}`" if ev.path else ""
            lines.append(f"|  |  |  | ↳ {detail}{path} |")
    return "\n".join(lines) + "\n"


def _html(result: SuiteResult) -> str:
    rows=[]
    for item in result.results:
        evidence="<br>".join(html.escape((ev.detail or "evidence")+(f" — {ev.path}" if ev.path else "")) for ev in item.evidence)
        rows.append(f"<tr class='{'pass' if item.passed else 'fail'}'><td>{'PASS' if item.passed else 'FAIL'}</td><td>{html.escape(item.assertion_id)}</td><td>{html.escape(item.assertion_type)}</td><td>{html.escape(item.message)}<div class='evidence'>{evidence}</div></td></tr>")
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>Studio Test Runner</title><style>body{{font-family:Inter,system-ui,sans-serif;background:#0a0f16;color:#eaf1f6;margin:0;padding:32px}}main{{max-width:1100px;margin:auto}}.summary{{border:1px solid #253445;border-radius:14px;padding:20px;background:#101923;margin-bottom:18px}}table{{width:100%;border-collapse:collapse;background:#0e1720;border:1px solid #253445}}th,td{{text-align:left;padding:12px;border-bottom:1px solid #22303e;vertical-align:top}}th{{font-size:12px;color:#8fa4b2}}.pass td:first-child{{color:#63d69f;font-weight:800}}.fail td:first-child{{color:#ff7883;font-weight:800}}.evidence{{font-size:12px;color:#91a6b4;margin-top:6px;line-height:1.5}}code{{color:#9adfc5}}</style></head><body><main><div class='summary'><h1>{html.escape(result.suite_id)}</h1><p>Target: <code>{html.escape(result.target)}</code></p><b>{'PASS' if result.passed else 'FAIL'} — {result.passed_count}/{len(result.results)} assertions passed</b></div><table><thead><tr><th>Status</th><th>Assertion</th><th>Type</th><th>Evidence</th></tr></thead><tbody>{''.join(rows)}</tbody></table></main></body></html>"""


def write_reports(result: SuiteResult, directory: str | Path) -> dict[str, Path]:
    output=Path(directory); output.mkdir(parents=True, exist_ok=True)
    json_path=output/"report.json"; md_path=output/"report.md"; html_path=output/"report.html"
    json_path.write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(_markdown(result), encoding="utf-8")
    html_path.write_text(_html(result), encoding="utf-8")
    return {"json":json_path,"markdown":md_path,"html":html_path}
