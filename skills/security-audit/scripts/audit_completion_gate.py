#!/usr/bin/env python3
"""Fail-fast completion checks for security-audit artifacts.

This script is intentionally conservative. It does not decide whether an audit is
good; it catches two common false completions:

1. Commit history was in scope, but `.security/latest_reviewed_commit` did not
   reach the audited `HEAD`.
2. Scanner output exists, especially CVE/advisory output, but it was not
   triaged into findings or explicit dismissals.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


ADVISORY_RE = re.compile(r"\b(?:CVE-\d{4}-\d{4,}|GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4})\b", re.I)
SECURITY_DIR_DEFAULT = ".security"


def git_head(repo: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None
    return result.stdout.strip()


def read_text(path: Path, max_bytes: int = 10_000_000) -> str:
    try:
        data = path.read_bytes()
    except OSError:
        return ""
    if len(data) > max_bytes:
        data = data[:max_bytes]
    return data.decode("utf-8", errors="ignore")


def iter_tool_files(tool_results: Path) -> list[Path]:
    if not tool_results.exists():
        return []
    ignored_parts = {"tool-cache", ".cache", "__pycache__"}
    files: list[Path] = []
    for path in tool_results.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def all_artifact_text(security_dir: Path) -> str:
    chunks: list[str] = []
    for rel in ["report.md", "tool_triage.md", "scan_manifest.md"]:
        chunks.append(read_text(security_dir / rel))
    for base in ["findings", "fixed"]:
        for path in sorted((security_dir / base).glob("SEC-*.md")):
            chunks.append(read_text(path))
    return "\n".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a security-audit run is allowed to be called complete.",
    )
    parser.add_argument("--repo", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--security-dir", default=SECURITY_DIR_DEFAULT, help="Path to .security directory.")
    parser.add_argument(
        "--history-required",
        choices=["yes", "no"],
        default="yes",
        help="Use 'no' only when the user explicitly scoped the audit to current HEAD/diff/subtree.",
    )
    parser.add_argument(
        "--max-advisories-to-print",
        type=int,
        default=40,
        help="Maximum untriaged advisory IDs to print in the error output.",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    security_dir = Path(args.security_dir)
    if not security_dir.is_absolute():
        security_dir = repo / security_dir

    errors: list[str] = []
    warnings: list[str] = []

    for rel in ["tooling_preflight.md", "threat_model.md", "scan_manifest.md", "report.md"]:
        if not (security_dir / rel).exists():
            errors.append(f"missing required artifact: {security_dir / rel}")

    if args.history_required == "yes":
        head = git_head(repo)
        cursor_path = security_dir / "latest_reviewed_commit"
        progress_path = security_dir / "commit_review_progress.md"
        cursor = read_text(cursor_path).strip().splitlines()[0] if cursor_path.exists() else ""
        if not head:
            errors.append("history required, but git HEAD could not be determined")
        if not cursor:
            errors.append("history required, but .security/latest_reviewed_commit is missing or empty")
        elif head and cursor != head:
            errors.append(f"history required, but latest_reviewed_commit is {cursor} and HEAD is {head}")
        if not progress_path.exists():
            errors.append("history required, but .security/commit_review_progress.md is missing")
        else:
            progress = read_text(progress_path)
            if head and head not in progress:
                warnings.append("commit_review_progress.md does not mention current HEAD; verify range completion")
    else:
        report_manifest = read_text(security_dir / "report.md") + "\n" + read_text(security_dir / "scan_manifest.md")
        if "history" not in report_manifest.lower():
            warnings.append("history not required, but report/manifest do not explain why it was out of scope")

    tool_files = iter_tool_files(security_dir / "tool-results")
    artifact_text = all_artifact_text(security_dir)
    triage_text = read_text(security_dir / "tool_triage.md")

    if tool_files and not triage_text:
        errors.append("tool-results exist, but .security/tool_triage.md is missing")

    unreferenced_files: list[str] = []
    for path in tool_files:
        rel = str(path.relative_to(security_dir))
        name = path.name
        if rel not in artifact_text and name not in artifact_text:
            unreferenced_files.append(rel)
    if unreferenced_files:
        sample = ", ".join(unreferenced_files[:20])
        suffix = " ..." if len(unreferenced_files) > 20 else ""
        errors.append(f"tool result files are not referenced by findings/report/tool_triage: {sample}{suffix}")

    advisory_ids: set[str] = set()
    for path in tool_files:
        if path.suffix.lower() not in {".json", ".sarif", ".txt", ".xml", ".csv", ".md"}:
            continue
        advisory_ids.update(match.upper() for match in ADVISORY_RE.findall(read_text(path)))

    if advisory_ids:
        finding_text = "\n".join(
            read_text(path)
            for base in ["findings", "fixed"]
            for path in sorted((security_dir / base).glob("SEC-*.md"))
        )
        triage_or_report = triage_text + "\n" + read_text(security_dir / "report.md")
        missing_advisories = sorted(
            advisory for advisory in advisory_ids if advisory not in finding_text and advisory not in triage_or_report
        )
        if missing_advisories:
            sample = ", ".join(missing_advisories[: args.max_advisories_to_print])
            suffix = " ..." if len(missing_advisories) > args.max_advisories_to_print else ""
            errors.append(f"advisory IDs appear in tool-results but are not triaged: {sample}{suffix}")

    if errors:
        print("SECURITY AUDIT COMPLETION GATE: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        for warning in warnings:
            print(f"- warning: {warning}", file=sys.stderr)
        return 1

    print("SECURITY AUDIT COMPLETION GATE: PASS")
    for warning in warnings:
        print(f"- warning: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
