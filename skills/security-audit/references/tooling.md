# Security tooling

Deterministic tools and semantic LLM review catch different bugs — run both. Tools give broad, repeatable
coverage and find known-CVE dependencies and obvious sink patterns fast; semantic review (against
`policies/*`) finds logic, authz, and chained issues tools miss. **A tool hit is a candidate, never a
finding** — always confirm it against real code and validate before reporting.

Sub-agents run these per partition and save raw output under `.security/tool-results/` (one file per
tool, JSON/SARIF where supported). If a tool reports hits, triage them against code and turn confirmed
actionable issues into normal `.security/findings/SEC-NNN-<slug>.md` reports; do not create readable
Markdown summaries under `.security/tool-results/`. Prefer tools already present; install only when
allowed and useful. If network/install is blocked, fall back to the `grep`-able patterns in the policy
files and to code review — record the gap as a blindspot.

**Run only "safe/static" tools by default.** Everything here reads code, manifests, or lockfiles without
executing the project. Do **not** run `npm/pip/bundle install`, builds, `go generate`, `make`, test
suites, or Docker builds just to make a scanner happy — those run attacker-controlled lifecycle scripts
(see the repo-safety tiering in SKILL.md). Prefer offline/local modes; don't upload proprietary code to a
hosted SaaS (Snyk, hosted CodeQL) unless the repo is already configured for it. Note any tool that
downloads a rules/CVE DB. **A non-zero exit because a scanner found issues is normal** — capture the exit
code in `scan_manifest.md` and continue; don't abort the scan.
Prompt the user to install required tools if they are unavailable and you cannot install them yourself
in local userspace or the sandbox. Give the user a concrete command list.

## Detect what's present first

```bash
# language/ecosystem fingerprint
ls package.json pnpm-lock.yaml go.mod Cargo.toml pyproject.toml requirements*.txt \
   pom.xml build.gradle* composer.json Gemfile *.csproj 2>/dev/null
# which tools are already installed
for t in semgrep trivy grype osv-scanner gitleaks trufflehog bandit gosec govulncheck \
         cargo-audit npm pnpm yarn pip-audit safety codeql snyk syft checkov tfsec hadolint; do
  command -v "$t" >/dev/null 2>&1 && echo "have: $t"
done
```

## Multi-language SAST

**Semgrep** — the default static analyzer; fast, language-agnostic, huge community ruleset.
```bash
pipx install semgrep        # or: pip install --break-system-packages semgrep
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
go install github.com/google/osv-scanner/cmd/osv-scanner@latest
osv-scanner scan --recursive --format sarif --output .security/tool-results/osv.sarif <target>
```

**Trivy** (deps + container images + IaC + secrets in one):
```bash
trivy fs --scanners vuln,secret,misconfig --format sarif -o .security/tool-results/trivy.sarif <target>
trivy image <image:tag>     # scan a built container
```

**Grype** (+ Syft for SBOM):
```bash
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
gitleaks detect --source . --redact --report-format sarif --report-path .security/tool-results/gitleaks.sarif
trufflehog git file://. --json > .security/tool-results/trufflehog.json   # verifies many secret types live
```
If a secret is real (not a fixture): report a **redacted fingerprint + location** (type, `path:line`,
prefix/suffix, confidence), recommend rotation + history rewrite (`git filter-repo`), and never paste
the full value into artifacts or chat. See `policies/secrets-and-supply-chain.md`.

## Per-language deep analyzers

- **Python:** `bandit -r <pkg> -f sarif -o .security/tool-results/bandit.sarif` (insecure APIs, `eval`, `pickle`,
  `subprocess shell=True`, weak crypto). See `policies/python.md`.
- **Go:** `gosec -fmt sarif -out .security/tool-results/gosec.sarif ./...` plus `govulncheck`. See `policies/go.md`.
- **JS/TS:** `semgrep` + `npm audit`; `eslint-plugin-security` if an eslint config exists. See `policies/javascript-typescript.md`.
- **Java/Kotlin/JVM:** OWASP Dependency-Check + `semgrep` JVM rules; SpotBugs/FindSecBugs if a build is set up. See `policies/jvm.md`.
- **C/C++:** `clang-tidy` / `cppcheck --enable=all`; compile with `-fsanitize=address,undefined` and run
  the test suite or a PoC; `clang --analyze`. See `policies/memory-safety.md`.
- **Rust:** `cargo audit` (or `cargo deny check advisories`) + `cargo clippy`; audit every `unsafe` block
  and FFI boundary by hand. See `policies/memory-safety.md`.
- **Shell:** `shellcheck` on tracked scripts (quoting/injection/`eval` issues — high-value for installers).
- **Ruby / PHP / .NET:** `bundle audit`, `composer audit --format=json`, `dotnet list package --vulnerable
  --include-transitive`.

## IaC / containers / cloud

- `checkov -d . -o sarif --output-file-path .security/tool-results/` — Terraform/CFN/K8s/Dockerfile/Ansible misconfig.
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
