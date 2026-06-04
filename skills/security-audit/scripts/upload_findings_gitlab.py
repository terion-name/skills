#!/usr/bin/env python3
"""Upload .security findings to GitLab Issues."""

from __future__ import annotations

import argparse
import urllib.parse

from issue_upload_common import add_common_args, finding_markdown_body, get_api_key, load_findings_or_exit, print_result, request_json


HELP_EPILOG = """\
Examples:
  # Preview planned GitLab issues.
  ./scripts/upload_findings_gitlab.py --project-id group/project --label security --dry-run

  # Upload only new findings to gitlab.com.
  export GITLAB_API_KEY=glpat-...
  ./scripts/upload_findings_gitlab.py \\
    --project-id group/subgroup/project \\
    --label security \\
    --finding-index-from 24

  # Upload to self-hosted GitLab with a custom token env var.
  export INTERNAL_GITLAB_TOKEN=...
  ./scripts/upload_findings_gitlab.py \\
    --host https://gitlab.example.com \\
    --project-id 12345 \\
    --label security-audit \\
    --api-key-env-name INTERNAL_GITLAB_TOKEN

Notes:
  - Requires a GitLab token that can create project issues and labels.
  - --project-id accepts numeric ids or project paths; project paths are URL-encoded by the script.
  - By default uploads only .security/findings/. Add --include-fixed to upload .security/fixed/ too.
  - Issue descriptions include parsed finding reports, not raw .security/tool-results/.
"""


LABEL_COLOR = "#b60205"
LABEL_DESCRIPTION = "Security finding imported from .security reports"


def api_base(host: str | None) -> str:
    normalized = (host or "https://gitlab.com").rstrip("/")
    if "://" not in normalized:
        normalized = "https://" + normalized
    if normalized.endswith("/api/v4"):
        return normalized
    return normalized + "/api/v4"


def project_path(project_id: str) -> str:
    return urllib.parse.quote(project_id, safe="")


def ensure_label(base: str, project_id: str, label: str, headers: dict[str, str]) -> None:
    project = project_path(project_id)
    encoded_label = urllib.parse.quote(label, safe="")
    existing = request_json("GET", f"{base}/projects/{project}/labels/{encoded_label}", headers=headers, allow_404=True)
    if existing:
        return
    request_json(
        "POST",
        f"{base}/projects/{project}/labels",
        headers=headers,
        data={"name": label, "color": LABEL_COLOR, "description": LABEL_DESCRIPTION},
    )


def upload(args: argparse.Namespace) -> None:
    findings = load_findings_or_exit(args)
    if args.dry_run:
        for finding in findings:
            print(f"DRY-RUN gitlab: {finding.sec_id} -> {finding.issue_title}")
        return

    token = get_api_key(args.api_key_env_name)
    headers = {"PRIVATE-TOKEN": token}
    base = api_base(args.host)
    project = project_path(args.project_id)
    if args.label:
        ensure_label(base, args.project_id, args.label, headers)

    for finding in findings:
        payload = {"title": finding.issue_title, "description": finding_markdown_body(finding)}
        if args.label:
            payload["labels"] = args.label
        response = request_json("POST", f"{base}/projects/{project}/issues", headers=headers, data=payload)
        print_result("gitlab", finding, response)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_common_args(parser, "gitlab")
    args = parser.parse_args()
    upload(args)


if __name__ == "__main__":
    main()
