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
import json
import re
import subprocess
import sys
from pathlib import Path


ADVISORY_RE = re.compile(r"\b(?:CVE-\d{4}-\d{4,}|GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4})\b", re.I)
SECURITY_DIR_DEFAULT = ".security"
VALID_REVIEW_STATUSES = {"skip", "reviewed-no-finding", "candidate"}


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


def git_commit_list(repo: Path, args: list[str]) -> list[str] | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


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


def first_line(path: Path) -> str:
    text = read_text(path).strip()
    return text.splitlines()[0].strip() if text else ""


def validate_history_ledger(repo: Path, security_dir: Path, head: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    target_head = first_line(security_dir / "commit_review_target_head")
    start_cursor = first_line(security_dir / "commit_review_start_cursor")
    queue_path = security_dir / "commit_review_queue.txt"
    ledger_path = security_dir / "commit_review_ledger.jsonl"
    review_dir = security_dir / "commit-reviews"

    if not target_head:
        errors.append("history required, but .security/commit_review_target_head is missing or empty")
    elif head and target_head != head:
        errors.append(f"history target head is {target_head}, but current HEAD is {head}; refresh and review the new range")

    if not start_cursor:
        errors.append("history required, but .security/commit_review_start_cursor is missing or empty")

    queue = [line.strip() for line in read_text(queue_path).splitlines() if line.strip()]
    if not queue_path.exists():
        errors.append("history required, but .security/commit_review_queue.txt is missing")
    elif not queue:
        errors.append("history required, but .security/commit_review_queue.txt is empty")
    elif len(queue) != len(set(queue)):
        errors.append("commit_review_queue.txt contains duplicate commits")

    expected: list[str] | None = None
    if target_head and start_cursor:
        if start_cursor in {"FIRST_RUN", "first-run", "none", "NONE", "-"}:
            all_recent = git_commit_list(repo, ["log", "--since=2 months ago", "--format=%H", "--reverse"])
            expected = all_recent[-1000:] if all_recent is not None else None
        else:
            expected = git_commit_list(repo, ["rev-list", "--reverse", f"{start_cursor}..{target_head}"])
        if expected is None:
            errors.append("could not compute expected commit history queue from git")
        elif queue and queue != expected:
            errors.append(
                "commit_review_queue.txt does not match expected git range "
                f"(expected {len(expected)} commits, found {len(queue)})"
            )

    if not ledger_path.exists():
        errors.append("history required, but .security/commit_review_ledger.jsonl is missing")
        return errors, warnings

    entries: dict[str, dict[str, object]] = {}
    malformed = 0
    for lineno, line in enumerate(read_text(ledger_path).splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            entry = json.loads(stripped)
        except json.JSONDecodeError:
            malformed += 1
            continue
        commit = str(entry.get("commit", "")).strip()
        if not commit:
            errors.append(f"ledger line {lineno} has no commit")
            continue
        if commit in entries:
            errors.append(f"ledger contains duplicate entry for {commit}")
        entries[commit] = entry

    if malformed:
        errors.append(f"commit_review_ledger.jsonl has {malformed} malformed JSON line(s)")

    if queue:
        missing = [sha for sha in queue if sha not in entries]
        extra = [sha for sha in entries if sha not in set(queue)]
        if missing:
            sample = ", ".join(missing[:20])
            suffix = " ..." if len(missing) > 20 else ""
            errors.append(f"ledger is missing queued commits: {sample}{suffix}")
        if extra:
            sample = ", ".join(extra[:20])
            suffix = " ..." if len(extra) > 20 else ""
            warnings.append(f"ledger contains commits outside current queue: {sample}{suffix}")

    for sha in queue:
        entry = entries.get(sha)
        if not entry:
            continue
        status = str(entry.get("status", "")).strip()
        if status not in VALID_REVIEW_STATUSES:
            errors.append(f"{sha}: invalid ledger status {status!r}")
            continue
        artifact_rel = str(entry.get("review_artifact", "")).strip()
        artifact = security_dir / artifact_rel if artifact_rel else review_dir / f"{sha}.md"
        artifact_text = read_text(artifact)
        if not artifact.exists():
            errors.append(f"{sha}: missing per-commit review artifact {artifact}")
        elif sha not in artifact_text:
            errors.append(f"{sha}: review artifact does not mention the commit SHA")

        changed_paths = entry.get("changed_paths", [])
        if not isinstance(changed_paths, list) or not changed_paths:
            errors.append(f"{sha}: ledger must include non-empty changed_paths")

        elapsed = entry.get("elapsed_seconds")
        if not isinstance(elapsed, (int, float)) or elapsed < 0:
            errors.append(f"{sha}: ledger must include actual non-negative elapsed_seconds")

        if status == "skip":
            reason = str(entry.get("skip_reason", "")).strip()
            if len(reason) < 12:
                errors.append(f"{sha}: skip entry needs a concrete skip_reason")
            if artifact.exists() and len(artifact_text.strip()) < 250:
                errors.append(f"{sha}: skip review artifact is too thin to audit")
            continue

        required_booleans = ["parent_child_diff_checked", "current_head_trace_checked"]
        for key in required_booleans:
            if entry.get(key) is not True:
                errors.append(f"{sha}: ledger must set {key}=true for functional reviews")

        files_inspected = entry.get("files_inspected", [])
        if not isinstance(files_inspected, list) or not files_inspected:
            errors.append(f"{sha}: functional review needs files_inspected")

        probes = entry.get("probes", [])
        if not isinstance(probes, list) or not probes:
            errors.append(f"{sha}: functional review needs probe checklist results")

        traced = entry.get("caller_traces", []) or entry.get("invariants_checked", [])
        if not isinstance(traced, list) or not traced:
            errors.append(f"{sha}: functional review needs caller_traces or invariants_checked")

        promotion_gate = str(entry.get("promotion_gate_result", "")).strip()
        if len(promotion_gate) < 8:
            errors.append(f"{sha}: functional review needs promotion_gate_result")

        if status == "candidate":
            candidates = entry.get("candidates", [])
            if not isinstance(candidates, list) or not candidates:
                errors.append(f"{sha}: candidate status requires candidates list")
        if artifact.exists() and len(artifact_text.strip()) < 900:
            errors.append(f"{sha}: functional review artifact is too thin to prove per-commit review")

    return errors, warnings


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
        ledger_errors, ledger_warnings = validate_history_ledger(repo, security_dir, head)
        errors.extend(ledger_errors)
        warnings.extend(ledger_warnings)
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
