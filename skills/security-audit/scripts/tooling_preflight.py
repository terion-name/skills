#!/usr/bin/env python3
"""Strict tooling preflight for the security-audit skill.

The script fingerprints the repository, checks Docker availability, identifies the
scanner set expected for the detected ecosystems, and prints a Markdown decision
record the agent can place in .security/tooling_preflight.md.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Tool:
    name: str
    category: str
    image: str
    why: str
    install: str


TOOLS = {
    "semgrep": Tool(
        "semgrep",
        "SAST",
        "semgrep/semgrep",
        "multi-language source/security rule scanning",
        "brew install semgrep  # or: pipx install semgrep",
    ),
    "trivy": Tool(
        "trivy",
        "SCA/IaC/secrets",
        "aquasec/trivy or ghcr.io/aquasecurity/trivy",
        "filesystem dependency CVEs, IaC misconfigurations, secrets, image scans",
        "brew install trivy",
    ),
    "gitleaks": Tool(
        "gitleaks",
        "secrets",
        "ghcr.io/gitleaks/gitleaks",
        "working-tree and git-history secret scanning",
        "brew install gitleaks",
    ),
    "syft": Tool(
        "syft",
        "SBOM",
        "anchore/syft",
        "SBOM generation for supply-chain evidence",
        "brew install syft",
    ),
    "grype": Tool(
        "grype",
        "SCA/CVE",
        "anchore/grype",
        "vulnerability scan from filesystem or SBOM",
        "brew install grype",
    ),
    "osv-scanner": Tool(
        "osv-scanner",
        "SCA/CVE",
        "ghcr.io/google/osv-scanner",
        "OSV dependency vulnerability matching from lockfiles/manifests",
        "brew install osv-scanner",
    ),
    "checkov": Tool(
        "checkov",
        "IaC",
        "bridgecrew/checkov",
        "Terraform/CloudFormation/Kubernetes/Dockerfile policy scanning",
        "brew install checkov  # or: pipx install checkov",
    ),
    "bandit": Tool(
        "bandit",
        "Python SAST",
        "ghcr.io/pycqa/bandit/bandit",
        "Python dangerous API and insecure pattern scanning",
        "pipx install bandit",
    ),
    "gosec": Tool(
        "gosec",
        "Go SAST",
        "ghcr.io/securego/gosec",
        "Go dangerous API and insecure pattern scanning",
        "brew install gosec  # or: go install github.com/securego/gosec/v2/cmd/gosec@latest",
    ),
    "hadolint": Tool(
        "hadolint",
        "Dockerfile",
        "hadolint/hadolint",
        "Dockerfile linting and hardening checks",
        "brew install hadolint",
    ),
    "dependency-check": Tool(
        "dependency-check",
        "JVM SCA",
        "owasp/dependency-check",
        "JVM dependency CVE scanning",
        "brew install dependency-check",
    ),
    "dep-scan": Tool(
        "dep-scan",
        "SCA/risk",
        "ghcr.io/appthreat/dep-scan",
        "multi-ecosystem dependency risk, SBOM, VEX-oriented scanning",
        "docker pull ghcr.io/appthreat/dep-scan",
    ),
}


def has_any(root: Path, patterns: list[str]) -> bool:
    return any(root.glob(pattern) for pattern in patterns)


def detect_ecosystems(root: Path) -> dict[str, bool]:
    return {
        "javascript/typescript": has_any(root, ["package.json", "pnpm-lock.yaml", "package-lock.json", "yarn.lock", "tsconfig.json"]),
        "python": has_any(root, ["pyproject.toml", "requirements*.txt", "Pipfile", "poetry.lock", "setup.py"]),
        "go": has_any(root, ["go.mod", "**/*.go"]),
        "rust": has_any(root, ["Cargo.toml", "Cargo.lock"]),
        "jvm": has_any(root, ["pom.xml", "build.gradle", "build.gradle.kts", "gradle.lockfile", "**/*.java", "**/*.kt"]),
        "dotnet": has_any(root, ["*.csproj", "*.sln", "packages.lock.json"]),
        "ruby": has_any(root, ["Gemfile", "Gemfile.lock", "*.gemspec"]),
        "php": has_any(root, ["composer.json", "composer.lock"]),
        "iac": has_any(root, ["**/*.tf", "**/*.tfvars", "**/*.yaml", "**/*.yml", "Dockerfile", "**/Dockerfile", "docker-compose*.yml", "charts/**"]),
        "dockerfile": has_any(root, ["Dockerfile", "**/Dockerfile"]),
    }


def required_tools(ecosystems: dict[str, bool]) -> list[str]:
    required = ["semgrep", "trivy", "gitleaks", "syft", "grype", "osv-scanner"]
    if ecosystems.get("iac"):
        required.append("checkov")
    if ecosystems.get("dockerfile"):
        required.append("hadolint")
    if ecosystems.get("python"):
        required.append("bandit")
    if ecosystems.get("go"):
        required.append("gosec")
    if ecosystems.get("jvm"):
        required.extend(["dependency-check", "dep-scan"])
    return list(dict.fromkeys(required))


def docker_status() -> tuple[bool, str]:
    if shutil.which("docker") is None:
        return False, "docker CLI not found"
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{.ServerVersion}}"],
            check=True,
            capture_output=True,
            text=True,
            timeout=12,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        detail = getattr(exc, "stderr", "") or getattr(exc, "stdout", "") or str(exc)
        return False, "docker CLI found, but daemon is unavailable: " + detail.strip()
    version = result.stdout.strip() or "unknown"
    return True, f"Docker daemon available (server {version})"


def local_status(tool_names: list[str]) -> dict[str, str]:
    return {name: (shutil.which(name) or "") for name in tool_names}


def markdown(root: Path, ecosystems: dict[str, bool], tool_names: list[str], docker_ok: bool, docker_msg: str) -> str:
    local = local_status(tool_names)
    detected = ", ".join(name for name, present in ecosystems.items() if present) or "none detected"
    rows = []
    for name in tool_names:
        tool = TOOLS[name]
        status = "container-ready" if docker_ok else ("local-ready" if local[name] else "missing")
        local_value = local[name] or "-"
        rows.append(
            f"| {tool.name} | {tool.category} | {status} | `{tool.image}` | `{local_value}` | {tool.why} |"
        )

    if docker_ok:
        decision = (
            "Docker is available. Proceed with containerized instrumental scans using the official "
            "per-tool images in `references/tooling.md`. Host-local scanner binaries are optional; "
            "do not skip a required scanner merely because it is not installed on the host."
        )
    else:
        missing = [name for name in tool_names if not local[name]]
        decision = (
            "Docker is not available. Stop before the audit scan unless the user explicitly says to "
            "continue with only available local tools. Recommended path: install/start Docker, then "
            "rerun this preflight. If the user approves degraded local-only scanning, record that "
            "approval and the missing tools in `.security/scan_manifest.md` and `.security/report.md`."
        )
        if missing:
            decision += "\n\nMissing local tools: " + ", ".join(missing) + "."

    install_lines = "\n".join(f"- `{TOOLS[name].install}`" for name in tool_names if not local[name])
    if not install_lines:
        install_lines = "- All required local tools appear to be installed, but containerized scans are still preferred when Docker works."

    return "\n".join(
        [
            "# Security tooling preflight",
            "",
            f"- Repo: `{root}`",
            f"- Docker: {docker_msg}",
            f"- Ecosystems detected: {detected}",
            "",
            "## Required scanners",
            "",
            "| Tool | Category | Status | Container image | Local binary | Why |",
            "|------|----------|--------|-----------------|--------------|-----|",
            *rows,
            "",
            "## Decision",
            "",
            decision,
            "",
            "## Local install guidance when Docker is unavailable",
            "",
            "Prefer installing Docker and rerunning containerized scans:",
            "",
            "- macOS: `brew install --cask docker` or install Docker Desktop from Docker's official site, then start it.",
            "- Linux: install Docker Engine from your distribution or Docker's official packages, then ensure `docker info` works.",
            "",
            "If Docker cannot be used and the user explicitly approves local-only scanning, install the missing tools locally:",
            "",
            install_lines,
            "",
            "## Notes",
            "",
            "- Prefer official per-tool containers over broad third-party toolbox images.",
            "- Pin image tags or digests for repeatable audits when practical.",
            "- Container network access may be needed for rule/CVE DB updates; record it in the manifest.",
            "- Mount repository code read-only and write outputs only to `.security/tool-results/`.",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run strict security-audit tooling preflight.")
    parser.add_argument("--repo", default=".", help="Repository root to fingerprint. Defaults to current directory.")
    parser.add_argument("--write", help="Optional Markdown output path, e.g. .security/tooling_preflight.md.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when Docker is unavailable.")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    ecosystems = detect_ecosystems(root)
    tool_names = required_tools(ecosystems)
    docker_ok, docker_msg = docker_status()
    report = markdown(root, ecosystems, tool_names, docker_ok, docker_msg)

    if args.write:
        output = Path(args.write)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report + "\n", encoding="utf-8")

    print(report)
    return 2 if args.strict and not docker_ok else 0


if __name__ == "__main__":
    sys.exit(main())
