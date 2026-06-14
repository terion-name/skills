#!/usr/bin/env python3
"""Update the security-audit skill's prepared CWE reference catalog.

The source CWE XML is intentionally kept outside the skill. This script downloads
MITRE's latest zipped XML catalog, extracts the catalog XML, parses the schema's
structured fields, and writes compact agent-friendly references under
`references/cwe/`.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import tempfile
import urllib.request
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


DEFAULT_SOURCE_URL = "https://cwe.mitre.org/data/xml/cwec_latest.xml.zip"
DEFAULT_SCHEMA_URL = "https://cwe.mitre.org/data/xsd/cwe_schema_latest.xsd"
NS = {"cwe": "http://cwe.mitre.org/cwe-7"}
TAG_RE = re.compile(r"[^a-z0-9]+")
WHITESPACE_RE = re.compile(r"\s+")

TAXONOMY_LABEL_PRIORITY = [
    "PLOVER",
    "WASC",
    "7 Pernicious Kingdoms",
    "CLASP",
    "OWASP Top Ten 2021",
    "OWASP Top Ten 2017",
    "OWASP Top Ten 2013",
    "OWASP Top Ten 2010",
    "OWASP Top Ten 2007",
    "OWASP Top Ten 2004",
]

BROAD_TAXONOMY_LABELS = {
    "Broken Access Control",
    "Identification and Authentication Failures",
    "Injection Flaws",
    "Insecure Direct Object Reference",
    "Security Misconfiguration",
    "Software and Data Integrity Failures",
    "Unvalidated Input",
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "in",
    "of",
    "or",
    "the",
    "to",
    "used",
    "use",
    "using",
}


def collapse(text: str, *, max_chars: int | None = None) -> str:
    value = WHITESPACE_RE.sub(" ", text).strip()
    if max_chars is not None and len(value) > max_chars:
        return value[: max_chars - 1].rstrip() + "..."
    return value


def text_of(element: ET.Element | None, *, max_chars: int | None = None) -> str:
    if element is None:
        return ""
    return collapse(" ".join(element.itertext()), max_chars=max_chars)


def child(parent: ET.Element, name: str) -> ET.Element | None:
    return parent.find(f"cwe:{name}", NS)


def children(parent: ET.Element, name: str) -> list[ET.Element]:
    return list(parent.findall(f"cwe:{name}", NS))


def child_text(parent: ET.Element, name: str, *, max_chars: int | None = None) -> str:
    return text_of(child(parent, name), max_chars=max_chars)


def child_texts(parent: ET.Element, name: str, *, max_chars: int | None = None) -> list[str]:
    return [text_of(item, max_chars=max_chars) for item in children(parent, name) if text_of(item)]


def scalar(value: str) -> str:
    return collapse(value)


def parse_taxonomy_mappings(entry: ET.Element) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    mappings = child(entry, "Taxonomy_Mappings")
    if mappings is None:
        return output
    for mapping in children(mappings, "Taxonomy_Mapping"):
        item: dict[str, str] = {
            "taxonomy": scalar(mapping.attrib.get("Taxonomy_Name", "")),
            "entry_id": child_text(mapping, "Entry_ID"),
            "entry_name": child_text(mapping, "Entry_Name"),
            "mapping_fit": child_text(mapping, "Mapping_Fit"),
        }
        item = {key: value for key, value in item.items() if value}
        if item:
            output.append(item)
    return output


def quoted_term(name: str) -> str:
    match = re.search(r"\('([^']+)'\)", name)
    if match:
        return match.group(1)
    return ""


def taxonomy_label(mappings: list[dict[str, str]]) -> tuple[str, str]:
    by_taxonomy: dict[str, list[dict[str, str]]] = {}
    for mapping in mappings:
        taxonomy = mapping.get("taxonomy", "")
        by_taxonomy.setdefault(taxonomy, []).append(mapping)

    for taxonomy in TAXONOMY_LABEL_PRIORITY:
        for mapping in by_taxonomy.get(taxonomy, []):
            label = mapping.get("entry_name", "")
            if label and label not in BROAD_TAXONOMY_LABELS:
                return label, taxonomy

    return "", ""


def derive_short_label(name: str, mappings: list[dict[str, str]]) -> tuple[str, str]:
    mapped, source = taxonomy_label(mappings)
    if mapped:
        return mapped, source

    quoted = quoted_term(name)
    if quoted:
        return quoted, "cwe-name-quoted-term"

    cleaned = re.sub(r"\s*\([^)]*\)\s*", " ", name)
    return collapse(cleaned), "cwe-name"


def slugify(label: str, *, max_words: int = 8, max_chars: int = 60) -> str:
    slug = TAG_RE.sub("-", label.lower()).strip("-")
    words = [word for word in slug.split("-") if word]
    if len(words) > max_words:
        meaningful = [word for word in words if word not in STOPWORDS]
        if len(meaningful) >= 2:
            words = meaningful[:max_words]
        else:
            words = words[:max_words]
    slug = "-".join(words)
    if len(slug) > max_chars:
        kept: list[str] = []
        for word in words:
            candidate = "-".join([*kept, word])
            if len(candidate) > max_chars:
                break
            kept.append(word)
        slug = "-".join(kept) if kept else slug[:max_chars].strip("-")
    return slug or "cwe"


def parse_related_weaknesses(entry: ET.Element) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    related = child(entry, "Related_Weaknesses")
    if related is None:
        return output
    for item in children(related, "Related_Weakness"):
        row = {
            "nature": scalar(item.attrib.get("Nature", "")),
            "cwe": "CWE-" + scalar(item.attrib.get("CWE_ID", "")),
            "view_id": scalar(item.attrib.get("View_ID", "")),
            "ordinal": scalar(item.attrib.get("Ordinal", "")),
            "chain_id": scalar(item.attrib.get("Chain_ID", "")),
        }
        output.append({key: value for key, value in row.items() if value and value != "CWE-"})
    return output


def parse_weakness_ordinalities(entry: ET.Element) -> list[str]:
    output: list[str] = []
    ordinalities = child(entry, "Weakness_Ordinalities")
    if ordinalities is None:
        return output
    for item in children(ordinalities, "Weakness_Ordinality"):
        value = child_text(item, "Ordinality")
        if value:
            output.append(value)
    return output


def parse_consequences(entry: ET.Element, *, max_chars: int) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    consequences = child(entry, "Common_Consequences")
    if consequences is None:
        return output
    for consequence in children(consequences, "Consequence"):
        row = {
            "scope": child_texts(consequence, "Scope"),
            "impact": child_texts(consequence, "Impact"),
            "likelihood": child_text(consequence, "Likelihood"),
            "note": child_text(consequence, "Note", max_chars=max_chars),
        }
        output.append({key: value for key, value in row.items() if value})
    return output


def parse_detection_methods(entry: ET.Element, *, max_chars: int) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    methods = child(entry, "Detection_Methods")
    if methods is None:
        return output
    for method in children(methods, "Detection_Method"):
        row = {
            "method": child_text(method, "Method"),
            "effectiveness": child_text(method, "Effectiveness"),
            "description": child_text(method, "Description", max_chars=max_chars),
        }
        output.append({key: value for key, value in row.items() if value})
    return output


def parse_mitigations(entry: ET.Element, *, max_chars: int) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    mitigations = child(entry, "Potential_Mitigations")
    if mitigations is None:
        return output
    for mitigation in children(mitigations, "Mitigation"):
        row = {
            "phase": child_texts(mitigation, "Phase"),
            "strategy": child_text(mitigation, "Strategy"),
            "effectiveness": child_text(mitigation, "Effectiveness"),
            "description": child_text(mitigation, "Description", max_chars=max_chars),
        }
        output.append({key: value for key, value in row.items() if value})
    return output


def parse_modes(entry: ET.Element, *, max_chars: int) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    modes = child(entry, "Modes_Of_Introduction")
    if modes is None:
        return output
    for introduction in children(modes, "Introduction"):
        row = {
            "phase": child_text(introduction, "Phase"),
            "note": child_text(introduction, "Note", max_chars=max_chars),
        }
        output.append({key: value for key, value in row.items() if value})
    return output


def parse_observed_examples(entry: ET.Element, *, max_chars: int, limit: int) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    examples = child(entry, "Observed_Examples")
    if examples is None:
        return output
    for example in children(examples, "Observed_Example")[:limit]:
        row = {
            "reference": child_text(example, "Reference"),
            "description": child_text(example, "Description", max_chars=max_chars),
            "link": child_text(example, "Link"),
        }
        output.append({key: value for key, value in row.items() if value})
    return output


def parse_related_attack_patterns(entry: ET.Element) -> list[str]:
    patterns = child(entry, "Related_Attack_Patterns")
    if patterns is None:
        return []
    ids: list[str] = []
    for pattern in children(patterns, "Related_Attack_Pattern"):
        capec_id = scalar(pattern.attrib.get("CAPEC_ID", ""))
        if capec_id:
            ids.append("CAPEC-" + capec_id)
    return ids


def parse_applicable_platforms(entry: ET.Element) -> dict[str, list[str]]:
    platforms = child(entry, "Applicable_Platforms")
    if platforms is None:
        return {}
    output: dict[str, list[str]] = {}
    for item in list(platforms):
        tag = item.tag.rsplit("}", 1)[-1].lower()
        name = scalar(item.attrib.get("Name", "")) or text_of(item)
        if name:
            output.setdefault(tag, []).append(name)
    return output


def parse_weakness(entry: ET.Element, *, max_chars: int, example_limit: int) -> dict[str, Any]:
    cwe_id = "CWE-" + entry.attrib["ID"]
    name = scalar(entry.attrib.get("Name", ""))
    mappings = parse_taxonomy_mappings(entry)
    short_label, label_source = derive_short_label(name, mappings)
    filename_label = slugify(short_label)
    return {
        "id": cwe_id,
        "number": int(entry.attrib["ID"]),
        "kind": "weakness",
        "name": name,
        "short_label": short_label,
        "filename_tag": f"{cwe_id}-{filename_label}",
        "label_source": label_source,
        "abstraction": scalar(entry.attrib.get("Abstraction", "")),
        "structure": scalar(entry.attrib.get("Structure", "")),
        "status": scalar(entry.attrib.get("Status", "")),
        "description": child_text(entry, "Description", max_chars=max_chars),
        "extended_description": child_text(entry, "Extended_Description", max_chars=max_chars),
        "likelihood_of_exploit": child_text(entry, "Likelihood_Of_Exploit"),
        "taxonomy_mappings": mappings,
        "related_weaknesses": parse_related_weaknesses(entry),
        "weakness_ordinalities": parse_weakness_ordinalities(entry),
        "applicable_platforms": parse_applicable_platforms(entry),
        "modes_of_introduction": parse_modes(entry, max_chars=max_chars),
        "common_consequences": parse_consequences(entry, max_chars=max_chars),
        "detection_methods": parse_detection_methods(entry, max_chars=max_chars),
        "potential_mitigations": parse_mitigations(entry, max_chars=max_chars),
        "observed_examples": parse_observed_examples(entry, max_chars=max_chars, limit=example_limit),
        "related_attack_patterns": parse_related_attack_patterns(entry),
        "mapping_notes": text_of(child(entry, "Mapping_Notes"), max_chars=max_chars),
    }


def parse_category(entry: ET.Element, *, max_chars: int) -> dict[str, Any]:
    cwe_id = "CWE-" + entry.attrib["ID"]
    name = scalar(entry.attrib.get("Name", ""))
    mappings = parse_taxonomy_mappings(entry)
    short_label, label_source = derive_short_label(name, mappings)
    filename_label = slugify(short_label)
    members: list[str] = []
    relationships = child(entry, "Relationships")
    if relationships is not None:
        for relation in children(relationships, "Has_Member"):
            member_id = scalar(relation.attrib.get("CWE_ID", ""))
            if member_id:
                members.append("CWE-" + member_id)
    return {
        "id": cwe_id,
        "number": int(entry.attrib["ID"]),
        "kind": "category",
        "name": name,
        "short_label": short_label,
        "filename_tag": f"{cwe_id}-{filename_label}",
        "label_source": label_source,
        "status": scalar(entry.attrib.get("Status", "")),
        "summary": child_text(entry, "Summary", max_chars=max_chars),
        "taxonomy_mappings": mappings,
        "members": members,
    }


def parse_catalog(xml_bytes: bytes, *, max_chars: int, example_limit: int, include_categories: bool) -> tuple[dict[str, str], list[dict[str, Any]]]:
    root = ET.parse(io.BytesIO(xml_bytes)).getroot()
    manifest = {
        "catalog_name": scalar(root.attrib.get("Name", "")),
        "catalog_version": scalar(root.attrib.get("Version", "")),
        "catalog_date": scalar(root.attrib.get("Date", "")),
    }

    entries: list[dict[str, Any]] = []
    for weakness in root.findall(".//cwe:Weakness", NS):
        entries.append(parse_weakness(weakness, max_chars=max_chars, example_limit=example_limit))
    if include_categories:
        for category in root.findall(".//cwe:Category", NS):
            entries.append(parse_category(category, max_chars=max_chars))
    entries.sort(key=lambda item: (int(item["number"]), item["kind"]))
    return manifest, entries


def download_xml_zip(source_url: str) -> tuple[bytes, str]:
    with urllib.request.urlopen(source_url, timeout=120) as response:
        payload = response.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        xml_members = [
            member
            for member in archive.infolist()
            if member.filename.lower().endswith(".xml") and not member.is_dir()
        ]
        if not xml_members:
            raise RuntimeError(f"{source_url} did not contain an XML file")
        xml_member = max(xml_members, key=lambda item: item.file_size)
        with archive.open(xml_member) as handle:
            return handle.read(), xml_member.filename


def read_xml_source(args: argparse.Namespace) -> tuple[bytes, str, str]:
    if args.xml:
        path = Path(args.xml)
        return path.read_bytes(), str(path), "local-xml"
    xml_bytes, member = download_xml_zip(args.source_url)
    return xml_bytes, f"{args.source_url}#{member}", "downloaded-zip"


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent) as handle:
        handle.write(text)
        tmp_name = handle.name
    Path(tmp_name).replace(path)
    path.chmod(0o644)


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_outputs(
    output_dir: Path,
    source: str,
    source_kind: str,
    catalog_manifest: dict[str, str],
    entries: list[dict[str, Any]],
    *,
    source_url: str,
    schema_url: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = output_dir / "cwe-catalog.jsonl"
    labels_path = output_dir / "cwe-labels.json"
    index_path = output_dir / "cwe-index.md"
    manifest_path = output_dir / "manifest.json"

    jsonl = "\n".join(json_dumps(entry) for entry in entries) + "\n"
    labels = {
        entry["id"]: {
            "name": entry.get("name", ""),
            "short_label": entry.get("short_label", ""),
            "filename_tag": entry.get("filename_tag", ""),
            "label_source": entry.get("label_source", ""),
            "kind": entry.get("kind", ""),
            "abstraction": entry.get("abstraction", ""),
            "status": entry.get("status", ""),
        }
        for entry in entries
    }

    weakness_count = sum(1 for entry in entries if entry.get("kind") == "weakness")
    category_count = sum(1 for entry in entries if entry.get("kind") == "category")
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    manifest: dict[str, Any] = {
        **catalog_manifest,
        "source": source,
        "source_kind": source_kind,
        "source_url": source_url,
        "schema_url": schema_url,
        "generated_at_utc": generated_at,
        "entry_count": len(entries),
        "weakness_count": weakness_count,
        "category_count": category_count,
        "files": {
            "catalog_jsonl": jsonl_path.name,
            "labels_json": labels_path.name,
            "index_markdown": index_path.name,
        },
    }

    lines = [
        "# CWE Reference Catalog",
        "",
        "Generated for the security-audit skill. Use `cwe-catalog.jsonl` as the structured source of truth and `cwe-labels.json` for filename tags.",
        "",
        f"- Source: `{source}`",
        f"- Schema: `{schema_url}`",
        f"- Catalog: {catalog_manifest.get('catalog_name', '')}",
        f"- Version/date: {catalog_manifest.get('catalog_version', '')} / {catalog_manifest.get('catalog_date', '')}",
        f"- Generated: {generated_at}",
        f"- Entries: {len(entries)} ({weakness_count} weaknesses, {category_count} categories)",
        "",
        "## Report Usage",
        "",
        "For every validated, likely, or unvalidated finding, choose the closest CWE weakness and include:",
        "",
        "```",
        "CWE: CWE-22 - Path Traversal",
        "CWE description: Improper limitation of a pathname to a restricted directory allows traversal outside the intended root.",
        "CWE mapping: primary; the source accepts a user-controlled path and the sink resolves it without a containment check.",
        "Standards: CWE-22, <other mappings>",
        "```",
        "",
        "Use `filename_tag` for report filenames, e.g. `SEC-001-[HIGH]-[CWE-22-path-traversal]-arbitrary-file-read.md`.",
        "",
        "## Index",
        "",
        "| CWE | Kind | Abstraction | Short label | Name | Filename tag |",
        "|-----|------|-------------|-------------|------|--------------|",
    ]
    for entry in entries:
        lines.append(
            "| {id} | {kind} | {abstraction} | {short_label} | {name} | {filename_tag} |".format(
                id=entry.get("id", ""),
                kind=entry.get("kind", ""),
                abstraction=entry.get("abstraction", ""),
                short_label=str(entry.get("short_label", "")).replace("|", "\\|"),
                name=str(entry.get("name", "")).replace("|", "\\|"),
                filename_tag=entry.get("filename_tag", ""),
            )
        )

    atomic_write(jsonl_path, jsonl)
    atomic_write(labels_path, json.dumps(labels, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    atomic_write(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    atomic_write(index_path, "\n".join(lines) + "\n")


def default_output_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "cwe"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Download/parse MITRE CWE XML and generate compact security-audit references. "
            "By default pulls cwec_latest.xml.zip from cwe.mitre.org."
        )
    )
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL, help=f"CWE XML zip URL. Default: {DEFAULT_SOURCE_URL}")
    parser.add_argument("--schema-url", default=DEFAULT_SCHEMA_URL, help=f"CWE XSD URL recorded in manifest. Default: {DEFAULT_SCHEMA_URL}")
    parser.add_argument("--xml", help="Use a local CWE XML file instead of downloading the zip.")
    parser.add_argument("--output-dir", default=str(default_output_dir()), help="Directory for generated references.")
    parser.add_argument(
        "--max-text-chars",
        type=int,
        default=1200,
        help="Maximum characters retained for long descriptive fields in each JSONL record.",
    )
    parser.add_argument(
        "--observed-example-limit",
        type=int,
        default=3,
        help="Maximum observed examples retained per CWE record.",
    )
    parser.add_argument(
        "--exclude-categories",
        action="store_true",
        help="Write only Weakness entries; categories are included by default for taxonomy context.",
    )
    args = parser.parse_args()

    try:
        xml_bytes, source, source_kind = read_xml_source(args)
        catalog_manifest, entries = parse_catalog(
            xml_bytes,
            max_chars=args.max_text_chars,
            example_limit=args.observed_example_limit,
            include_categories=not args.exclude_categories,
        )
        write_outputs(
            Path(args.output_dir),
            source,
            source_kind,
            catalog_manifest,
            entries,
            source_url=args.source_url,
            schema_url=args.schema_url,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should print concise failures.
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(
        "updated CWE references: "
        f"{len(entries)} entries in {Path(args.output_dir).resolve()} "
        f"({catalog_manifest.get('catalog_name', 'unknown catalog')})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
