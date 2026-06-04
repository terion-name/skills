#!/usr/bin/env python3
"""Upload .security findings to GitHub Issues."""

from __future__ import annotations

import argparse
import urllib.parse

from issue_upload_common import add_common_args, finding_markdown_body, get_api_key, load_findings_or_exit, print_result, request_json


HELP_EPILOG = """\
Examples:
  # Preview what would be uploaded from the local .security directory.
  ./scripts/upload_findings_github.py --project-id owner/repo --label security --dry-run

  # Upload only findings SEC-012 and above to github.com.
  export GITHUB_API_KEY=ghp_...
  ./scripts/upload_findings_github.py --project-id owner/repo --label security --finding-index-from 12

  # Upload to GitHub Enterprise using a custom token env var.
  export GH_ENTERPRISE_TOKEN=...
  ./scripts/upload_findings_github.py \\
    --host https://github.example.com \\
    --project-id owner/repo \\
    --label security-audit \\
    --api-key-env-name GH_ENTERPRISE_TOKEN

Notes:
  - Requires a token with permission to create issues and labels in the target repository.
  - By default uploads only .security/findings/. Add --include-fixed to upload .security/fixed/ too.
  - Issue bodies include the parsed finding report, not raw .security/tool-results/.
"""


LABEL_COLOR = "b60205"
LABEL_DESCRIPTION = "Security finding imported from .security reports"


def api_base(host: str | None) -> str:
    if not host:
        return "https://api.github.com"
    normalized = host.rstrip("/")
    if "://" not in normalized:
        normalized = "https://" + normalized
    if normalized.endswith("/api/v3"):
        return normalized
    if "api.github.com" in normalized:
        return normalized
    return normalized + "/api/v3"


def ensure_label(base: str, repo: str, label: str, headers: dict[str, str]) -> None:
    encoded = urllib.parse.quote(label, safe="")
    url = f"{base}/repos/{repo}/labels/{encoded}"
    existing = request_json("GET", url, headers=headers, allow_404=True)
    if existing:
        return
    request_json(
        "POST",
        f"{base}/repos/{repo}/labels",
        headers=headers,
        data={"name": label, "color": LABEL_COLOR, "description": LABEL_DESCRIPTION},
    )


def upload(args: argparse.Namespace) -> None:
    findings = load_findings_or_exit(args)
    labels = [args.label] if args.label else []
    if args.dry_run:
        for finding in findings:
            print(f"DRY-RUN github: {finding.sec_id} -> {finding.issue_title}")
        return

    token = get_api_key(args.api_key_env_name)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    base = api_base(args.host)
    repo = args.project_id
    if args.label:
        ensure_label(base, repo, args.label, headers)

    for finding in findings:
        response = request_json(
            "POST",
            f"{base}/repos/{repo}/issues",
            headers=headers,
            data={"title": finding.issue_title, "body": finding_markdown_body(finding), "labels": labels},
        )
        print_result("github", finding, response)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_common_args(parser, "github")
    args = parser.parse_args()
    upload(args)


if __name__ == "__main__":
    main()
