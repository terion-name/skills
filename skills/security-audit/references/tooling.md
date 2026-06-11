# Security tooling

Deterministic tools and semantic LLM review catch different bugs — run both. Tools give broad, repeatable
coverage and find known-CVE dependencies and obvious sink patterns fast; semantic review (against
`policies/*`) finds logic, authz, and chained issues tools miss. **A tool hit is a candidate first, not
an automatic finding** — always confirm it against real code and validate before reporting. In the final
audit, no tool-derived candidate may remain unresolved: promote it to a standard SEC finding/fixed report,
dismiss it with evidence, or mark validation blocked.

Sub-agents run these per partition and save raw output under `.security/tool-results/` (one file per
tool, JSON/SARIF where supported). If a tool reports hits, triage them against code and turn confirmed
actionable issues into normal `.security/findings/SEC-NNN-<slug>.md` reports; do not create readable
Markdown summaries under `.security/tool-results/`.

## Strict tooling preflight

Run this before threat modeling, partitioning, or scan fan-out:

```bash
scripts/tooling_preflight.py --write .security/tooling_preflight.md
```

This is a hard gate:

- **Docker available:** run instrumental scans in containers. Do not degrade to "whatever is installed
  locally"; local host binaries are optional fallback only if the relevant container image is blocked.
- **Docker unavailable:** stop before the scan. Tell the user which scanners are required, which local
  tools are missing, and recommend installing/starting Docker (`brew install --cask docker` on macOS, or
  Docker Engine/Desktop from Docker's official packages). Continue with available local tools only when
  the user explicitly says to do so.
- **Image/DB pull blocked:** stop and report the blocked image, rule pack, or CVE DB unless an equivalent
  cached image/DB is already available or the user explicitly approves degraded coverage.
- Record the preflight decision, Docker status, scanner images, versions/digests when known, missing
  tools, and any user-approved degradation in `.security/scan_manifest.md`.

There is no preferred single "all tools" image for this skill. Broad toolbox images tend to be stale,
over-privileged, or tuned for offensive/network testing rather than repository-grounded SAST/SCA. Kali's
official containers are base images and do not ship the default tool metapackage; OWASP secureCodeBox is
a Kubernetes scanner orchestration platform, not a local one-shot repository scanner. Prefer official
per-tool containers:

| Need | Preferred container image | Notes |
|------|---------------------------|-------|
| Multi-language SAST | `semgrep/semgrep` | Use OSS/local scans; disable metrics; no SaaS token unless user asked. |
| SCA + IaC + secrets | `aquasec/trivy` or `ghcr.io/aquasecurity/trivy` | Mount a cache for DB updates. |
| Secret scan | `ghcr.io/gitleaks/gitleaks` | Scan working tree and git history; redact output. |
| SBOM | `anchore/syft` | Write CycloneDX JSON to `.security/tool-results/`. |
| SBOM/filesystem CVE | `anchore/grype` | Cross-check Trivy/OSV results; use SBOM input when available. |
| OSV dependencies | `ghcr.io/google/osv-scanner` | Good lockfile/manifests coverage. |
| IaC graph scan | `bridgecrew/checkov` | Add `--no-guide` to avoid external guide lookups. |
| Python SAST | `ghcr.io/pycqa/bandit/bandit` | Use when Python files are present. |
| Go SAST | `ghcr.io/securego/gosec` | Use when Go files are present. |
| Dockerfile lint | `hadolint/hadolint` | Use when Dockerfiles are present. |
| JVM SCA | `owasp/dependency-check` | Prefer cache + NVD API key if user provides one. |
| Multi-ecosystem dependency risk | `ghcr.io/appthreat/dep-scan` | Useful supplement; can emit SBOM/VEX-style artifacts. |

**Run only "safe/static" tools by default.** Everything here reads code, manifests, or lockfiles without
executing the project. Do **not** run `npm/pip/bundle install`, builds, `go generate`, `make`, test
suites, or Docker builds just to make a scanner happy — those run attacker-controlled lifecycle scripts
(see the repo-safety tiering in SKILL.md). Prefer offline/local modes; don't upload proprietary code to a
hosted SaaS (Snyk, hosted CodeQL) unless the repo is already configured for it. Note any tool that
downloads a rules/CVE DB. **A non-zero exit because a scanner found issues is normal** — capture the exit
code in `scan_manifest.md` and continue; don't abort the scan.

## Container run pattern

Create output/cache directories first:

```bash
mkdir -p .security/tool-results .security/tool-cache
```

Default safety posture:

- Mount source read-only: `-v "$PWD:/src:ro"`.
- Mount only output/cache paths read-write: `-v "$PWD/.security/tool-results:/out"`.
- Prefer `--user "$(id -u):$(id -g)"` when the image supports it, so outputs are not root-owned.
- Keep network enabled only when needed for rule/CVE DB updates. Record that in the manifest.
- Pin explicit image tags or digests for repeatable audits when practical. Avoid `latest` in regulated or
  long-running audit programs.

Common container commands:

```bash
# Semgrep SAST
docker run --rm --user "$(id -u):$(id -g)" \
  -e SEMGREP_SEND_METRICS=off \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" \
  semgrep/semgrep semgrep scan --config auto --sarif --output /out/semgrep.sarif /src

# Trivy filesystem SCA/IaC/secrets
docker run --rm --user "$(id -u):$(id -g)" \
  -e TRIVY_CACHE_DIR=/cache \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" -v "$PWD/.security/tool-cache/trivy:/cache" \
  aquasec/trivy fs --scanners vuln,secret,misconfig --format sarif -o /out/trivy.sarif /src

# Gitleaks working tree + history
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" \
  ghcr.io/gitleaks/gitleaks detect --source /src --redact --report-format sarif --report-path /out/gitleaks.sarif

# SBOM + Grype CVE pass
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" \
  anchore/syft /src -o cyclonedx-json=/out/sbom.cdx.json
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/.security/tool-results:/out" -v "$PWD/.security/tool-cache/grype:/cache" \
  -e GRYPE_DB_CACHE_DIR=/cache \
  anchore/grype sbom:/out/sbom.cdx.json -o sarif --file /out/grype.sarif

# OSV lockfile/manifests
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" \
  ghcr.io/google/osv-scanner scan source --recursive --format json --output-file /out/osv.json /src
```

If a container exits non-zero because it found issues, capture the output and continue. If it exits
because the image, network, cache, or permissions failed, fix the environment or stop for user input; do
not silently mark the tool skipped.

## Multi-language SAST

**Semgrep** — the default static analyzer; fast, language-agnostic, huge community ruleset.
```bash
# Container preferred (after Step 0 confirms Docker):
docker run --rm --user "$(id -u):$(id -g)" -e SEMGREP_SEND_METRICS=off \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" \
  semgrep/semgrep semgrep scan --config auto --sarif --output /out/semgrep.sarif /src

# Local only when Docker is unavailable and the user explicitly approved degraded scanning:
semgrep scan --config auto --sarif --output .security/tool-results/semgrep.sarif <target>
# focused, higher-signal rule packs:
semgrep scan --config p/security-audit --config p/secrets --config p/owasp-top-ten <target>
```
Triage every `semgrep` hit against code — its autoconfig rules have false positives.

**CodeQL** (deep dataflow, when available and worth the setup cost): build a database
(`codeql database create`), then run the language's `security-extended` query suite. Best for tracing
taint from source to sink in large codebases; slower to set up than Semgrep.

## Dependency / CVE scanning (SCA)

Find known-vulnerable dependencies. Use whichever is available; results overlap but differ in DB coverage.

**OSV-Scanner** (Google OSV DB; covers most ecosystems via lockfiles):
```bash
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" \
  ghcr.io/google/osv-scanner scan source --recursive --format json --output-file /out/osv.json /src

# Local only with explicit degraded approval:
osv-scanner scan --recursive --format sarif --output .security/tool-results/osv.sarif <target>
```

**Trivy** (deps + container images + IaC + secrets in one):
```bash
docker run --rm --user "$(id -u):$(id -g)" -e TRIVY_CACHE_DIR=/cache \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" -v "$PWD/.security/tool-cache/trivy:/cache" \
  aquasec/trivy fs --scanners vuln,secret,misconfig --format sarif -o /out/trivy.sarif /src

# Local only with explicit degraded approval:
trivy fs --scanners vuln,secret,misconfig --format sarif -o .security/tool-results/trivy.sarif <target>
trivy image <image:tag>     # scan a built container
```

**Grype** (+ Syft for SBOM):
```bash
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" \
  anchore/syft /src -o cyclonedx-json=/out/sbom.cdx.json
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/.security/tool-results:/out" -v "$PWD/.security/tool-cache/grype:/cache" \
  -e GRYPE_DB_CACHE_DIR=/cache \
  anchore/grype sbom:/out/sbom.cdx.json -o sarif --file /out/grype.sarif

# Local only with explicit degraded approval:
syft <target> -o cyclonedx-json > .security/tool-results/sbom.json
grype sbom:.security/tool-results/sbom.json -o sarif > .security/tool-results/grype.sarif
```

Per-ecosystem native auditors (fast, no extra install):
```bash
npm audit --json                 # or: pnpm audit --json / yarn npm audit
pip-audit -r requirements.txt    # or: uv pip ... ; safety check
govulncheck ./...                # Go; reachability-aware, low false positives
cargo audit                      # Rust (RustSec DB)
bundle audit                     # Ruby
dotnet list package --vulnerable # .NET
mvn org.owasp:dependency-check-maven:check   # Java (OWASP Dependency-Check)
```

When scanning a CVE hit, check **reachability**: a vulnerable transitive dep that no code path reaches is
lower severity than one on a live request path. `govulncheck` does this natively; for others, confirm a
call path exists before rating high.

## Secret scanning

Find committed credentials, keys, tokens — in the working tree **and** git history.
```bash
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" \
  ghcr.io/gitleaks/gitleaks detect --source /src --redact --report-format sarif --report-path /out/gitleaks.sarif

# Local only with explicit degraded approval:
gitleaks detect --source . --redact --report-format sarif --report-path .security/tool-results/gitleaks.sarif
trufflehog git file://. --json > .security/tool-results/trufflehog.json   # verifies many secret types live
```
If a secret is real (not a fixture): report a **redacted fingerprint + location** (type, `path:line`,
prefix/suffix, confidence), recommend rotation + history rewrite (`git filter-repo`), and never paste
the full value into artifacts or chat. See `policies/secrets-and-supply-chain.md`.

## Per-language deep analyzers

- **Python:** container preferred:
  ```bash
  docker run --rm --user "$(id -u):$(id -g)" \
    -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" \
    ghcr.io/pycqa/bandit/bandit -r /src -f sarif -o /out/bandit.sarif
  ```
  Local degraded-only: `bandit -r <pkg> -f sarif -o .security/tool-results/bandit.sarif`. Finds
  insecure APIs, `eval`, `pickle`, `subprocess shell=True`, weak crypto. See `policies/python.md`.
- **Go:** container preferred:
  ```bash
  docker run --rm --user "$(id -u):$(id -g)" \
    -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" -w /src \
    ghcr.io/securego/gosec -fmt sarif -out /out/gosec.sarif ./...
  ```
  Local degraded-only: `gosec -fmt sarif -out .security/tool-results/gosec.sarif ./...`; add
  `govulncheck` when already installed and safe for the repo. See `policies/go.md`.
- **JS/TS:** `semgrep` + `npm audit`; `eslint-plugin-security` if an eslint config exists. See `policies/javascript-typescript.md`.
- **Java/Kotlin/JVM:** OWASP Dependency-Check or OWASP dep-scan in containers; `semgrep` JVM rules.
  SpotBugs/FindSecBugs only if the project already builds safely. See `policies/jvm.md`.
- **C/C++:** `clang-tidy` / `cppcheck --enable=all`; compile with `-fsanitize=address,undefined` and run
  the test suite or a PoC; `clang --analyze`. See `policies/memory-safety.md`.
- **Rust:** `cargo audit` (or `cargo deny check advisories`) + `cargo clippy`; audit every `unsafe` block
  and FFI boundary by hand. See `policies/memory-safety.md`.
- **Shell:** `shellcheck` on tracked scripts (quoting/injection/`eval` issues — high-value for installers).
- **Ruby / PHP / .NET:** `bundle audit`, `composer audit --format=json`, `dotnet list package --vulnerable
  --include-transitive`.

## IaC / containers / cloud

Container preferred:

```bash
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD:/src:ro" -v "$PWD/.security/tool-results:/out" \
  bridgecrew/checkov --directory /src --output sarif --output-file-path /out --no-guide

find . -name 'Dockerfile' -print0 | while IFS= read -r -d '' f; do
  out=".security/tool-results/hadolint-${f#./}.json"
  mkdir -p "$(dirname "$out")"
  docker run --rm -i hadolint/hadolint hadolint --format json - < "$f" > "$out"
done
```

Local degraded-only:

- `checkov -d . -o sarif --output-file-path .security/tool-results/ --no-guide` — Terraform/CFN/K8s/Dockerfile/Ansible misconfig.
- `tfsec .` / `trivy config .` — Terraform & general IaC.
- `hadolint Dockerfile` — Dockerfile best-practice & security lint.
- `ansible-lint` — Ansible role/playbook issues (relevant for privileged provisioning — the example finding's class).
- `kube-score` / `kubesec` / `kube-linter` — Kubernetes manifest hardening.
See `policies/infra-and-iac.md`.

## Fuzzing (optional, high-value for parsers / native code)

For input parsers, decoders, and memory-unsafe code, a short fuzzing run finds crashes static tools miss:
- Go: native `go test -fuzz=Fuzz -fuzztime=60s`.
- Rust: `cargo fuzz run <target>` (libFuzzer).
- C/C++: build a libFuzzer/AFL++ harness with `-fsanitize=address,fuzzer`.
- Python: `atheris`.
Use only inside the sandbox, time-boxed; treat any crash as a candidate to validate and triage for severity.

## Aggregating output

Many tools emit SARIF — a common format you can merge and dedupe. Have sub-agents normalize hits to
`{tool, rule, path:line, severity, message}` in their report so you can cross-reference tool hits against
the semantic findings during validation. Where two independent tools flag the same location, confidence
is higher; where only one does, scrutinize harder.

Raw tool output stays in `.security/tool-results/`. The human-readable artifact for a confirmed tool hit
is the standard finding file in `.security/findings/`; tool-only noise does not get its own report.
