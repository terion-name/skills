#!/usr/bin/env python3
"""Upload .security findings to Plane work items with a security-finding work item type."""

from __future__ import annotations

import argparse
import re
from typing import Any

from issue_upload_common import (
    add_common_args,
    finding_html_body,
    finding_markdown_body,
    get_api_key,
    load_findings_or_exit,
    print_result,
    request_json,
)


HELP_EPILOG = """\
Examples:
  # Preview planned Plane work items. Project id may be workspace_slug/project_uuid.
  ./scripts/upload_findings_plane.py \\
    --project-id workspace-slug/project-uuid \\
    --label security \\
    --issue-type "Security Finding" \\
    --dry-run

  # Upload findings to Plane Cloud using the default PLANE_API_KEY env var.
  export PLANE_API_KEY=...
  ./scripts/upload_findings_plane.py \\
    --project-id workspace-slug/project-uuid \\
    --label security \\
    --issue-type "Security Finding"

  # Upload to self-hosted Plane using an explicit workspace slug and custom token env var.
  export INTERNAL_PLANE_TOKEN=...
  ./scripts/upload_findings_plane.py \\
    --host https://plane.example.com \\
    --workspace-slug workspace-slug \\
    --project-id project-uuid \\
    --label security-audit \\
    --issue-type "Security Finding" \\
    --api-key-env-name INTERNAL_PLANE_TOKEN

Notes:
  - Requires a Plane API key that can create project labels, work item types, properties, and work items.
  - The script creates/uses a work item type, default "Security Finding".
  - The work item type gets deterministic custom properties: SEC ID, Severity, Status, Category,
    CWE, CWE description, CWE mapping, Standards, Commit, Fixed in commit, Resolution, Location,
    Detected by, and Finding path.
  - By default uploads only .security/findings/. Add --include-fixed to upload .security/fixed/ too.
  - Work item bodies include parsed finding reports, not raw .security/tool-results/.
"""


LABEL_COLOR = "#b60205"
LABEL_DESCRIPTION = "Security finding imported from .security reports"
DEFAULT_ISSUE_TYPE = "Security Finding"
EXTERNAL_SOURCE = "codex-security-audit"

PROPERTY_SCHEMA = [
    ("SEC ID", "TEXT", "Chronological SEC-NNN finding identifier"),
    ("Severity", "TEXT", "Final severity from the security report"),
    ("Status", "TEXT", "Validation status"),
    ("Category", "TEXT", "Security report category"),
    ("CWE", "TEXT", "Primary CWE code and short label"),
    ("CWE description", "TEXT", "Catalog description for the primary CWE"),
    ("CWE mapping", "TEXT", "Finding-specific CWE mapping rationale"),
    ("Standards", "TEXT", "ASVS/API/CWE/NIST/SLSA mappings when present"),
    ("Commit", "TEXT", "Introducing commit when known"),
    ("Fixed in commit", "TEXT", "Fix commit when already remediated"),
    ("Resolution", "TEXT", "Resolution metadata"),
    ("Location", "TEXT", "Primary affected location"),
    ("Detected by", "TEXT", "Manual/tool/commit-review signal"),
    ("Finding path", "TEXT", "Local .security finding file path"),
]


def api_base(host: str | None) -> str:
    normalized = (host or "https://api.plane.so").rstrip("/")
    if "://" not in normalized:
        normalized = "https://" + normalized
    return normalized


def split_plane_project(project_id: str, workspace_slug: str | None) -> tuple[str, str]:
    if workspace_slug:
        return workspace_slug, project_id
    if "/" in project_id:
        workspace, project = project_id.split("/", 1)
        if workspace and project:
            return workspace, project
    raise SystemExit("Plane requires --workspace-slug, or --project-id as workspace_slug/project_uuid")


def plane_project_url(base: str, workspace: str, project: str, suffix: str) -> str:
    return f"{base}/api/v1/workspaces/{workspace}/projects/{project}/{suffix.lstrip('/')}"


def plane_headers(token: str) -> dict[str, str]:
    return {"X-API-Key": token}


def plane_list(url: str, headers: dict[str, str], params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    cursor = None
    while True:
        query = {"per_page": 100, **(params or {})}
        if cursor:
            query["cursor"] = cursor
        response = request_json("GET", url, headers=headers, params=query)
        if isinstance(response, list):
            items.extend(response)
            return items
        if not isinstance(response, dict):
            return items
        batch = response.get("results") or response.get("data") or []
        if isinstance(batch, list):
            items.extend(item for item in batch if isinstance(item, dict))
        cursor = response.get("next_cursor") or response.get("next")
        if not cursor:
            return items


def stable_external_id(prefix: str, name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"{prefix}-{slug}"[:255]


def ensure_label(base: str, workspace: str, project: str, label: str, headers: dict[str, str]) -> str:
    url = plane_project_url(base, workspace, project, "labels/")
    labels = plane_list(url, headers, {"fields": "id,name"})
    for item in labels:
        if item.get("name", "").lower() == label.lower():
            return str(item["id"])
    created = request_json(
        "POST",
        url,
        headers=headers,
        data={
            "name": label,
            "color": LABEL_COLOR,
            "description": LABEL_DESCRIPTION,
            "external_source": EXTERNAL_SOURCE,
            "external_id": stable_external_id("label", label),
        },
    )
    return str(created["id"])


def issue_type_description() -> str:
    fields = ", ".join(name for name, _, _ in PROPERTY_SCHEMA)
    return (
        "Security finding work item type for Codex .security reports. "
        "Body mirrors the finding template: Metadata, Summary, Validation, Evidence, Proposed patch, "
        "and Attack-path analysis. Custom properties: "
        + fields
    )


def ensure_issue_type(base: str, workspace: str, project: str, issue_type: str, headers: dict[str, str]) -> str:
    url = plane_project_url(base, workspace, project, "work-item-types/")
    types = plane_list(url, headers)
    for item in types:
        if item.get("name", "").lower() == issue_type.lower():
            return str(item["id"])
    created = request_json(
        "POST",
        url,
        headers=headers,
        data={
            "name": issue_type,
            "description": issue_type_description(),
            "is_active": True,
            "external_source": EXTERNAL_SOURCE,
            "external_id": stable_external_id("work-item-type", issue_type),
        },
    )
    return str(created["id"])


def ensure_property(
    base: str,
    workspace: str,
    project: str,
    type_id: str,
    display_name: str,
    property_type: str,
    description: str,
    headers: dict[str, str],
) -> str:
    url = plane_project_url(base, workspace, project, f"work-item-types/{type_id}/work-item-properties/")
    properties = plane_list(url, headers)
    for item in properties:
        if item.get("display_name", item.get("name", "")).lower() == display_name.lower():
            return str(item["id"])
    created = request_json(
        "POST",
        url,
        headers=headers,
        data={
            "display_name": display_name,
            "name": display_name,
            "description": description,
            "property_type": property_type,
            "is_active": True,
            "external_source": EXTERNAL_SOURCE,
            "external_id": stable_external_id("property", display_name),
        },
    )
    return str(created["id"])


def ensure_properties(base: str, workspace: str, project: str, type_id: str, headers: dict[str, str]) -> dict[str, str]:
    return {
        name: ensure_property(base, workspace, project, type_id, name, property_type, description, headers)
        for name, property_type, description in PROPERTY_SCHEMA
    }


def priority_for(severity: str) -> str:
    return {"critical": "urgent", "high": "high", "medium": "medium", "low": "low"}.get(severity.lower(), "none")


def property_values(finding) -> dict[str, str]:
    return {
        "SEC ID": finding.sec_id,
        "Severity": finding.severity,
        "Status": finding.status,
        "Category": finding.category,
        "CWE": finding.cwe,
        "CWE description": finding.cwe_description,
        "CWE mapping": finding.cwe_mapping,
        "Standards": finding.standards,
        "Commit": finding.commit,
        "Fixed in commit": finding.fixed_in_commit,
        "Resolution": finding.resolution,
        "Location": finding.location,
        "Detected by": finding.detected_by,
        "Finding path": str(finding.path),
    }


def set_property_value(
    base: str,
    workspace: str,
    project: str,
    work_item_id: str,
    property_id: str,
    value: str,
    external_id: str,
    headers: dict[str, str],
) -> None:
    url = plane_project_url(
        base,
        workspace,
        project,
        f"work-items/{work_item_id}/work-item-properties/{property_id}/values/",
    )
    request_json(
        "POST",
        url,
        headers=headers,
        data={"value": value, "external_source": EXTERNAL_SOURCE, "external_id": external_id},
    )


def upload(args: argparse.Namespace) -> None:
    findings = load_findings_or_exit(args)
    workspace, project = split_plane_project(args.project_id, args.workspace_slug)
    issue_type_name = args.issue_type or DEFAULT_ISSUE_TYPE

    if args.dry_run:
        for finding in findings:
            print(f"DRY-RUN plane: {finding.sec_id} -> {finding.issue_title} ({workspace}/{project})")
        return

    token = get_api_key(args.api_key_env_name)
    headers = plane_headers(token)
    base = api_base(args.host)
    label_ids = [ensure_label(base, workspace, project, args.label, headers)] if args.label else []
    type_id = ensure_issue_type(base, workspace, project, issue_type_name, headers)
    properties = ensure_properties(base, workspace, project, type_id, headers)
    work_items_url = plane_project_url(base, workspace, project, "work-items/")

    for finding in findings:
        response = request_json(
            "POST",
            work_items_url,
            headers=headers,
            data={
                "name": finding.issue_title,
                "description_html": finding_html_body(finding),
                "description_stripped": finding_markdown_body(finding),
                "priority": priority_for(finding.severity),
                "labels": label_ids,
                "type": type_id,
                "external_source": EXTERNAL_SOURCE,
                "external_id": f"{EXTERNAL_SOURCE}-{finding.sec_id.lower()}",
            },
        )
        work_item_id = str(response["id"])
        for name, value in property_values(finding).items():
            if value:
                set_property_value(
                    base,
                    workspace,
                    project,
                    work_item_id,
                    properties[name],
                    value,
                    f"{EXTERNAL_SOURCE}-{finding.sec_id.lower()}-{stable_external_id('field', name)}",
                    headers,
                )
        print_result("plane", finding, response)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_common_args(parser, "plane")
    parser.add_argument(
        "--workspace-slug",
        help=(
            "Plane workspace slug. Optional when --project-id is workspace_slug/project_uuid; "
            "required when --project-id is only the project UUID."
        ),
    )
    parser.add_argument(
        "--issue-type",
        help=(
            f"Plane work item type name to create/use. Defaults to {DEFAULT_ISSUE_TYPE!r}. "
            "The script creates matching security-report custom properties if they do not exist."
        ),
    )
    args = parser.parse_args()
    upload(args)


if __name__ == "__main__":
    main()
