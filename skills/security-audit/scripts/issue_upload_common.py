#!/usr/bin/env python3
"""Shared deterministic parser and HTTP helpers for security finding uploaders."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ID_RE = re.compile(r"SEC-(\d+)", re.IGNORECASE)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
SECTION_RE = re.compile(r"^# ([^\n#].*)$", re.MULTILINE)
METADATA_RE = re.compile(r"^(?:[-*]\s+)?([A-Za-z][A-Za-z0-9 _/-]*):\s*(.*)$")


@dataclass(frozen=True)
class Finding:
    sec_id: str
    index: int
    path: Path
    title: str
    severity: str
    attack_path_severity: str
    status: str
    origin: str
    metadata: dict[str, str]
    summary: str
    validation: str
    evidence: str
    proposed_patch: str
    attack_path_analysis: str
    raw_text: str
    fixed: bool

    @property
    def category(self) -> str:
        return self.metadata.get("Category", "")

    @property
    def standards(self) -> str:
        return self.metadata.get("Standards", "")

    @property
    def cwe(self) -> str:
        return self.metadata.get("CWE", "")

    @property
    def cwe_description(self) -> str:
        return self.metadata.get("CWE description", "")

    @property
    def cwe_mapping(self) -> str:
        return self.metadata.get("CWE mapping", "")

    @property
    def commit(self) -> str:
        return self.metadata.get("Commit", "")

    @property
    def fixed_in_commit(self) -> str:
        return self.metadata.get("Fixed in commit", "")

    @property
    def resolution(self) -> str:
        return self.metadata.get("Resolution", "")

    @property
    def detected_by(self) -> str:
        return self.metadata.get("Detected by", "")

    @property
    def location(self) -> str:
        explicit = self.metadata.get("Location", "")
        if explicit:
            return explicit
        for line in self.evidence.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith(("```", "Note:")):
                continue
            if re.search(r"\(L\d+|\w+/.+:\d+|^[\w./-]+\.\w+", stripped):
                return stripped
        return ""

    @property
    def issue_title(self) -> str:
        sev = self.severity or "unknown"
        return f"[{self.sec_id}][{sev}] {self.title}"


def strip_comments(text: str) -> str:
    return COMMENT_RE.sub("", text).strip()


def section_map(text: str) -> dict[str, str]:
    matches = list(SECTION_RE.finditer(text))
    sections: dict[str, str] = {}
    for i, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()
    return sections


def parse_metadata(section: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in section.splitlines():
        match = METADATA_RE.match(line.strip())
        if match:
            metadata[match.group(1).strip()] = match.group(2).strip()
    return metadata


def parse_proposed_patch(text: str) -> str:
    marker = re.search(r"^Proposed patch:\s*$", text, re.MULTILINE)
    if not marker:
        return ""
    after = text[marker.end() :]
    next_section = re.search(r"^# ", after, re.MULTILINE)
    return after[: next_section.start()].strip() if next_section else after.strip()


def parse_header(text: str) -> tuple[str, str, str, str, str]:
    prefix = text.split("\n# ", 1)[0]
    lines = [line.strip() for line in prefix.splitlines() if line.strip()]
    if not lines:
        raise ValueError("finding has no title")

    title = lines[0]
    severity = ""
    attack_path = ""
    status = ""
    origin = ""
    for line in lines[1:]:
        if line.startswith("Criticality:"):
            value = line.split(":", 1)[1].strip()
            match = re.match(r"([A-Za-z-]+)(?:\s+\(attack path:\s*([A-Za-z-]+)\))?", value)
            if match:
                severity = match.group(1).lower()
                attack_path = (match.group(2) or "").lower()
        elif line.startswith("Status:"):
            status = line.split(":", 1)[1].strip().lower()
        elif line.startswith("Origin:"):
            origin = line.split(":", 1)[1].strip()
    return title, severity, attack_path, status, origin


def parse_finding(path: Path, security_root: Path) -> Finding:
    raw_text = path.read_text(encoding="utf-8")
    text = strip_comments(raw_text)
    id_match = ID_RE.search(path.name)
    if not id_match:
        raise ValueError(f"{path}: filename does not contain SEC-NNN")
    index = int(id_match.group(1))
    sec_id = f"SEC-{index:03d}"
    title, severity, attack_path, status, origin = parse_header(text)
    sections = section_map(text)
    metadata = parse_metadata(sections.get("Metadata", ""))
    fixed = "fixed" in path.relative_to(security_root).parts or metadata.get("Resolution", "").lower() == "fixed"
    return Finding(
        sec_id=sec_id,
        index=index,
        path=path,
        title=title,
        severity=severity,
        attack_path_severity=attack_path,
        status=status,
        origin=origin,
        metadata=metadata,
        summary=sections.get("Summary", ""),
        validation=sections.get("Validation", ""),
        evidence=sections.get("Evidence", ""),
        proposed_patch=parse_proposed_patch(text),
        attack_path_analysis=sections.get("Attack-path analysis", ""),
        raw_text=text,
        fixed=fixed,
    )


def iter_findings(security_root: Path, index_from: int | None = None, include_fixed: bool = False) -> list[Finding]:
    paths = sorted((security_root / "findings").glob("SEC-*.md"))
    if include_fixed:
        paths.extend(sorted((security_root / "fixed").glob("SEC-*.md")))
    findings = [parse_finding(path, security_root) for path in paths]
    if index_from is not None:
        findings = [finding for finding in findings if finding.index >= index_from]
    return sorted(findings, key=lambda finding: (finding.index, str(finding.path)))


def finding_markdown_body(finding: Finding) -> str:
    meta_rows = [
        ("Finding", finding.sec_id),
        ("Severity", finding.severity),
        ("Attack-path severity", finding.attack_path_severity),
        ("Status", finding.status),
        ("Origin", finding.origin),
        ("Category", finding.category),
        ("CWE", finding.cwe),
        ("CWE description", finding.cwe_description),
        ("CWE mapping", finding.cwe_mapping),
        ("Standards", finding.standards),
        ("Commit", finding.commit),
        ("Fixed in commit", finding.fixed_in_commit),
        ("Resolution", finding.resolution),
        ("Detected by", finding.detected_by),
        ("Location", finding.location),
        ("Source file", str(finding.path)),
    ]
    metadata = "\n".join(f"- **{key}:** {value}" for key, value in meta_rows if value)
    sections = [
        "## Metadata\n" + metadata,
        "## Summary\n" + (finding.summary or "_No summary section parsed._"),
        "## Validation\n" + (finding.validation or "_No validation section parsed._"),
        "## Evidence\n" + (finding.evidence or "_No evidence section parsed._"),
    ]
    if finding.proposed_patch:
        sections.append("## Proposed patch\n" + finding.proposed_patch)
    if finding.attack_path_analysis:
        sections.append("## Attack-path analysis\n" + finding.attack_path_analysis)
    sections.append(
        "<details>\n<summary>Original finding markdown</summary>\n\n"
        "```markdown\n"
        + finding.raw_text.strip()
        + "\n```\n</details>"
    )
    return "\n\n".join(sections)


def finding_html_body(finding: Finding) -> str:
    markdown = finding_markdown_body(finding)
    escaped = html.escape(markdown)
    return "<pre>" + escaped + "</pre>"


def get_api_key(env_name: str) -> str:
    value = os.environ.get(env_name)
    if not value:
        raise SystemExit(f"Missing API key in ${env_name}")
    return value


def request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    allow_404: bool = False,
) -> Any:
    if params:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
        url = url + ("&" if "?" in url else "?") + query
    body = None
    request_headers = {"Accept": "application/json", **(headers or {})}
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        request_headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, method=method, headers=request_headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
            if not payload:
                return None
            return json.loads(payload.decode("utf-8"))
    except urllib.error.HTTPError as error:
        if allow_404 and error.code == 404:
            return None
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed with HTTP {error.code}: {detail}") from error


def paginated_get(url: str, headers: dict[str, str], *, params: dict[str, Any] | None = None) -> list[Any]:
    items: list[Any] = []
    page = 1
    while True:
        page_params = dict(params or {})
        page_params.setdefault("per_page", 100)
        page_params.setdefault("page", page)
        batch = request_json("GET", url, headers=headers, params=page_params)
        if not batch:
            break
        if isinstance(batch, dict) and "results" in batch:
            current = batch.get("results") or []
        elif isinstance(batch, list):
            current = batch
        else:
            current = []
        items.extend(current)
        if len(current) < int(page_params["per_page"]):
            break
        page += 1
    return items


def project_id_help(provider: str) -> str:
    return {
        "github": "Target repository as owner/repo, for example acme/api-service.",
        "gitlab": (
            "Target project as a numeric GitLab project id or path such as group/subgroup/project. "
            "Path values are URL-encoded by the script."
        ),
        "plane": (
            "Target Plane project. Use project_uuid with --workspace-slug, or workspace_slug/project_uuid "
            "as a single value."
        ),
    }.get(provider, "Provider project/repository identifier.")


def host_help(provider: str) -> str:
    return {
        "github": (
            "Optional GitHub Enterprise host or API base URL. Examples: https://github.example.com "
            "or https://github.example.com/api/v3. Defaults to https://api.github.com."
        ),
        "gitlab": (
            "Optional GitLab host or API base URL. Examples: https://gitlab.example.com "
            "or https://gitlab.example.com/api/v4. Defaults to https://gitlab.com/api/v4."
        ),
        "plane": (
            "Optional Plane API base URL for self-hosted Plane. Defaults to https://api.plane.so."
        ),
    }.get(provider, "Provider API host/base URL for self-hosted instances.")


def add_common_args(parser: argparse.ArgumentParser, provider: str) -> None:
    parser.add_argument(
        "--security-dir",
        default=".security",
        help="Path to the .security directory containing findings/ and optionally fixed/. Defaults to %(default)s.",
    )
    parser.add_argument("--project-id", required=True, help=project_id_help(provider))
    parser.add_argument("--host", help=host_help(provider))
    parser.add_argument(
        "--finding-index-from",
        type=int,
        help=(
            "Only upload findings whose SEC-NNN index is greater than or equal to this number. "
            "Useful for uploading only newly created findings after a previous import."
        ),
    )
    parser.add_argument(
        "--label",
        help="Optional issue/work-item label to create if missing and apply to every uploaded finding.",
    )
    parser.add_argument(
        "--api-key-env-name",
        default=f"{provider.upper()}_API_KEY",
        help=(
            "Environment variable containing the provider API token. Defaults to %(default)s. "
            "The token is read locally and is never written into uploaded issue bodies."
        ),
    )
    parser.add_argument(
        "--include-fixed",
        action="store_true",
        help="Also upload fixed historical reports from .security/fixed/. By default only .security/findings/ is uploaded.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse findings and print planned uploads without creating labels, issues, or work items.",
    )


def load_findings_or_exit(args: argparse.Namespace) -> list[Finding]:
    security_root = Path(args.security_dir)
    if not security_root.exists():
        raise SystemExit(f"Security directory not found: {security_root}")
    findings = iter_findings(security_root, args.finding_index_from, args.include_fixed)
    if not findings:
        raise SystemExit("No findings matched the requested range.")
    return findings


def print_result(provider: str, finding: Finding, response: Any) -> None:
    url = ""
    if isinstance(response, dict):
        url = response.get("html_url") or response.get("web_url") or response.get("url") or response.get("id", "")
    print(f"{provider}: uploaded {finding.sec_id} -> {url}")
