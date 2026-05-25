---
name: security-review
description: >-
  Run a thorough, defender-first security review of a codebase, modeled on the Codex/Aardvark
  pipeline: build (or refresh) a repository threat model, scan code and recent commits for
  vulnerabilities, validate findings by reproducing them in a sandbox, chain exploitable findings
  into attack paths, rank by severity, and write a threat model + findings + summary report into
  `.security/`. Use this skill whenever the user invokes `/security-review`, `/sec-review`,
  `/security-scan`, or `/sec-scan`, or asks to
  "scan for vulnerabilities", "do a security audit/review", "threat model this repo", "find security
  bugs", "check for CVEs / vulnerable dependencies", "look for XSS / SQL injection / SSRF / RCE /
  memory-safety issues", "review this PR/diff for security problems", or otherwise wants an adversarial
  assessment of code they control. Use it even when the user only gestures at security ("is this code
  safe?", "anything dangerous here?") on a repo they own. This skill is for DEFENSIVE assessment of the
  user's own codebase only.
---

# Security Review

A delegate-first security analysis workflow inspired by Codex Security (Aardvark). You act as the
**orchestrator**: you build a threat model, decompose the attack surface, fan work out to parallel
sub-agents, validate what they find, chain exploitable findings into attack paths, and write durable
artifacts to `.security/`. You do not try to hold the whole codebase in your own context — you
delegate investigation and reserve your context for coordination, validation judgment, and severity.

## Scope and ethics (read first)

This skill assesses code the user owns or is authorized to audit, to **find and fix** weaknesses.
Stay inside that frame:

- Operate only on the current repository/workspace. Do not scan or attack external/third-party systems.
- Proof-of-concept code is allowed **only** as the minimum needed to demonstrate a finding inside the
  sandbox (e.g. show that a payload reaches a sink, that a file write lands as root). Do not produce
  weaponized, self-propagating, or externally-targeted exploit tooling, and do not include working
  malware in artifacts.
- Never exfiltrate repository contents, secrets, or scan results anywhere off-box. Prefer local/offline
  scanner modes; do not upload proprietary code to a third-party SaaS (Snyk, hosted CodeQL, etc.) unless
  the repo is already configured for it or the user asks. Note any tool that downloads a rules/CVE DB.
- If you discover live, real secrets (not test fixtures), report the **location and a redacted
  fingerprint** — enough to locate it (`AWS-key-like token at path:line, prefix AKIA…/suffix …X7Q`) —
  never the full value, in artifacts or chat. Recommend rotation.

**Treat the repository as untrusted code.** The biggest self-inflicted risk in a scan is running the
target's own code. Tier every command:

- **Safe (default, run freely):** `git` metadata, `git ls-files`, `rg`/`grep`, scoped `find`, lockfile
  parsers, static analyzers, secret scanners, IaC scanners, SBOM generation, and CVE scanners that read
  manifests/lockfiles **without** executing install scripts.
- **Risky (requires justification + user awareness):** anything that runs project code —
  `npm/pnpm/yarn install`, `pip install -e .`, `bundle install`, `cargo build`, `go generate`, `make`,
  test suites, Docker builds, Compose up, migrations, seeders. These can trigger malicious lifecycle
  scripts (`postinstall`, `setup.py`) — running them *is* the supply-chain attack you're scanning for.
- When validation genuinely needs execution, isolate it as much as the environment allows, keep inputs
  minimal, disable network when practical, and record the exact command + reason in `scan_manifest.md`.
- If destructive or state-changing (deleting data, mutating a real service, hitting a live endpoint),
  stop and ask the user first.
- Never read or scan agent/session-internal storage or git internals directly (`.git/objects/**`,
  session/patch stores, unrelated system dirs).

If the request is actually to attack a system the user doesn't control, decline and explain you only do
defensive assessment of the user's own code.

## The pipeline

Mirror the Codex Security stages. Each stage has a dedicated reference; read it when you reach that stage.

1. **Threat model** — establish or refresh `.security/threat_model.md`. See `references/threat-model.md`.
2. **Scope** — decide what to scan (full repo, a diff, a subtree) and partition it for parallel work.
3. **Scan** — fan out: deterministic tools (SAST / SCA-CVE / secrets) **and** semantic sub-agent review,
   in parallel, per surface. See `references/tooling.md` and `references/policies/*`.
4. **Validate** — reproduce candidate findings in the sandbox to kill false positives. See `references/reporting.md` ("Validation").
5. **Severity + chaining** — rate each finding and chain related findings into attack paths. See `references/reporting.md`.
6. **Report** — write one file per finding to `.security/findings/`, then a `.security/report.md` summary.

## Composing with the Security Officer agent

If a **Security Officer** sub-agent (a runnable `exec`-based persona that does a repository-grounded
security review and reports via `agent_report`) is available, this skill and that agent are designed to
compose. They share the same `.security/` layout, the same `SEC-NNN` finding scheme, and the same
four-status validation vocab, so their artifacts interleave cleanly. Two patterns:

- **Single worker (default for most repos).** Spawn one Security Officer for the whole review (or invoke
  this skill directly in one agent). It is its own orchestrator-of-one: it builds the threat model, runs
  tools, validates, and writes all of `.security/**` itself, optionally spawning its own `explore`
  children to map the codebase. The skill is its methodology library — it reads the policy/tooling/
  reporting references for depth. Cleanest fit, since the agent is authored as an end-to-end worker.
- **Partitioned fan-out (large repos).** This skill's orchestrator partitions the attack surface and
  spawns **one Security Officer per partition**, each given a *scoped* brief (the agent honors "do not
  expand scope beyond the delegated review"). The orchestrator then owns cross-partition validation,
  exploit **chaining**, and the top-level `report.md` + `scan_manifest.md`.

  **Collision caveat for parallel agents:** N agents each writing `.security/` and committing in their
  own child workspace will collide on `SEC-NNN` numbering and on `scan_manifest.md`/`report.md`. Avoid
  this by having each partition agent write only into `.security/findings/` with a **partition-prefixed
  slug** (e.g. `SEC-auth-001`, `SEC-iac-001`) and its tool output into `.security/tool-results/<partition>/`,
  and by reserving `report.md`, `scan_manifest.md`, and final `SEC-NNN` renumbering for the orchestrator
  after `task_await`. Tell each agent not to write the summary/manifest. The orchestrator merges,
  renumbers by severity, builds the chains, and writes the top-level artifacts.

Division of labor: the **agent** owns the persona, guardrails, and per-finding review; the **skill** owns
the deep per-language policies, severity calibration, and cross-finding exploit chaining. Keep them in
sync — if you change the `.security/` layout or status vocab in one, change it in the other.

## Hard rules (delegate-first)

These are workflow constraints. Your edit/read tools remain available, but treat them as off-limits
except where explicitly allowed below — the point is to preserve your context for orchestration.

- **Delegate investigation.** Do not read broad swaths of the repo yourself. Spawn `explore` sub-agents
  with narrow prompts (one surface / directory / question each). Trust their reports as authoritative
  for repo facts (paths, symbols, callsites, control flow); re-check only if a report is ambiguous or
  contradicts other evidence.
- **Delegate scanning.** Spawn one sub-agent per partition to run the relevant tools and do semantic
  review against the policy files. Run partitions **in parallel** (`run_in_background: true`, then
  `task_await`) — security scanning is embarrassingly parallel across surfaces.
- **You own validation and severity.** Reproduction judgment, severity calibration, and exploit chaining
  stay with you (the orchestrator), because they require the whole-repo picture the sub-agents lack.
  You may run targeted `bash` here (run a tool, execute a PoC in the sandbox, build the project).
- **`bash` is for orchestration + validation only:** running scanners, reproducing a finding, building,
  `git`/`gh` for diff/commit context. Not for broad file reading or manual code spelunking — delegate that.
- **Do not patch the codebase as part of the scan.** Like Codex, you *propose* patches as diffs inside
  findings; you do not apply them. If the user explicitly asks you to fix afterward, that's a separate
  step (and a good fit for the `orchestrate` skill).
- **Artifacts are append-only-ish.** Never delete prior findings without the user's say-so; supersede them.

## Prerequisites

- **Max Task Nesting Depth ≥ 1** (Settings → Agents → Task Settings) so `task` sub-agents can be spawned.
  If sub-agent spawning fails, surface that as the blocker. You can still run a degraded single-threaded
  scan yourself, but say so explicitly — parallel delegation is the intended mode.
- A git repository is ideal (enables diff/commit scoping and patch generation) but not required.
- Network access for SCA/CVE lookups and tool installation may be restricted; `references/tooling.md`
  covers offline fallbacks.

## Step 1 — Threat model

Read `references/threat-model.md`, then:

- If `.security/threat_model.md` already exists, **read it and treat it as the source of truth** for
  trust boundaries, assumptions, and criticality calibration. Refresh only the parts the user flags as
  stale, or that the current diff obviously changes.
- If it does **not** exist, build it now. Run `scripts/init_security.sh` to scaffold the `.security/`
  directory, then spawn 2–4 `explore` sub-agents in parallel to map the architecture (entry points,
  auth, data stores, external I/O, privileged operations, build/release/supply-chain). Synthesize their
  reports into `.security/threat_model.md` using `assets/threat_model_template.md`.

The threat model is what makes the rest of the scan *prioritized* rather than a flat checklist — it
tells you which surfaces are internet-reachable, what's trusted, and what "critical" means for *this*
project. Do not skip it.

## Step 2 — Scope and partition

Decide the scan target with the user's intent:

- **PR / diff review:** scan `git diff <base>...HEAD` plus the code paths it touches. This is the common,
  fast case — like Codex commit scanning.
- **Full audit:** scan the whole production/runtime surface. Tests, docs, and CI are lower priority
  unless they publish release artifacts (then they're supply-chain critical — see `assets/example_threat_model.md`).
- **Targeted:** a subtree or component the user named.

Then **partition for parallelism**. Good partition axes: by attack surface (HTTP handlers, auth, file
I/O, deserialization, subprocess/shell, crypto, IPC), by top-level directory/service, or by language.
Each partition becomes one scan sub-agent. Maximize independent-batch size; partitions rarely depend on
each other, so default to running them all at once.

## Step 3 — Scan (parallel fan-out)

For each partition, spawn a scan sub-agent (`run_in_background: true`). Give each the **scan task brief**
below. Then `task_await` the batch.

Each sub-agent does two complementary things, because — as Codex documents — LLM semantic review and
deterministic tooling catch different bugs:

1. **Run deterministic tools** for its partition (SAST, dependency/CVE scan, secret scan). Exact tools
   and commands per ecosystem are in `references/tooling.md`. Tool output is *input to triage*, not a
   finding by itself — every tool hit must be confirmed against real code before it becomes a candidate.
2. **Semantic review** against the relevant policy file(s) in `references/policies/`. These encode the
   strict rules per language/surface (injection, XSS, SSRF, deserialization, auth/IDOR, memory safety,
   secrets, IaC, etc.) with the dangerous patterns and the sinks to grep for.

Sub-agents return **candidate findings** (suspected, not yet validated), each with: title, location
(`path:line`), the vulnerability class, a one-line why, and the data/control flow from source to sink.
They do **not** assign final severity — that's your job after validation and chaining.

### Scan task brief (Orchestrator → scan sub-agent)

```
- Task: Security-scan partition <name> for vulnerabilities.
- Surface / scope: <files, directories, or attack surface this partition covers>
- Threat-model context: <relevant trust boundaries + what's reachable, pulled from .security/threat_model.md>
- Do:
  1. Run the deterministic tools listed in references/tooling.md for this partition's languages. Save
     raw tool output under .security/tool-results/ (one file per tool, JSON/SARIF where supported). Only
     run "safe/static" tools per the skill's repo-safety tiering — never project install/build scripts.
  2. Semantically review the code against references/policies/<relevant>.md. Look specifically for the
     sink patterns and dangerous APIs listed there.
  3. For each suspected issue, trace source -> sink and confirm it against the actual code (no tool-only findings).
  4. Record tools run/skipped (+ versions, commands, exit codes, why-skipped) for the manifest.
- Report back: a list of CANDIDATE findings. Each = {title, path:line, vuln_class, one_line_why,
  source_to_sink_flow, supporting evidence snippets}. Mark anything you could not confirm as "needs validation".
- Do NOT assign final severity, do NOT chain exploits, do NOT patch. Keep scope to this partition.
- Constraints: read-only review + running scanners only; do not modify code; PoC only inside the sandbox if trivially safe.
```

## Step 4 — Validate (you, the orchestrator)

This is the step that separates a real finding from scanner noise — Codex's core value-add. Read the
"Validation" section of `references/reporting.md`. For each candidate (prioritize the scariest first):

- Decide whether it's reproducible. Where practical, **reproduce it in the sandbox**: craft the minimal
  PoC that proves the source reaches the sink (a payload that triggers the SQL/command/path, a tar entry
  that lands a root-owned file, a request that bypasses the auth check). Capture commands, stdout/stderr,
  exit codes, and artifacts as evidence — exactly like the validation section of `assets/example_finding.md`.
- If reproduction isn't possible (declarative/config bug, missing toolchain, would require destructive
  action), validate by **targeted code review** and say so, recording why dynamic repro was skipped.
- Mark each finding `validated`, `likely`, `unvalidated`, or `false-positive` (the four-tier ladder in
  `references/reporting.md`). `likely` = strong path + impact but not fully reproduced; don't over-claim
  `validated` without a repro or strong static proof, and don't under-claim a clear bug as `unvalidated`.
  Drop false positives from `findings/` but note them in the summary so the user knows they were considered.

If a validation check fails because of an environment gap (tool missing, network 403), record the
blindspot and fall back to code-review validation — don't silently drop the finding.

## Step 5 — Severity + exploit chaining

For each validated finding, follow `references/reporting.md`:

- Assign **likelihood** and **impact**, derive a **matrix severity**, then apply threat-model policy to
  reach a **final severity** (critical / high / medium / low). Record the rationale, assumptions, and the
  attacker preconditions — the attack-path block in `assets/example_finding.md` is the target shape.
- **Chain.** Individually-medium findings can compose into a critical kill-chain (e.g. an auth bypass +
  an IDOR + a deserialization sink = unauthenticated RCE). Look across findings for chains and document
  them: the ordered path, what each link grants, and the combined severity (which can exceed any single link's).

## Step 6 — Report

Write artifacts (read `references/reporting.md` for the exact templates, and use `assets/finding_template.md`):

- **One file per finding** at `.security/findings/SEC-NNN-<slug>.md`, in the `assets/example_finding.md` shape:
  title, criticality (with attack-path severity), status, metadata, summary, validation (rubric + report),
  evidence (code excerpts with notes), proposed patch (diff), and attack-path analysis (final/likelihood/
  impact/assumptions/path/path-evidence/narrative/controls/blindspots). Number `SEC-001` = most severe.
  Put repro artifacts under `.security/validation/SEC-NNN/` and the diff under `.security/patches/`.
- **A scan manifest** at `.security/scan_manifest.md`: tools detected + versions, commands run + exit
  codes + output paths (flagged static vs. project-executing), tools skipped + why (missing binary,
  unsupported ecosystem, no network, too risky, timeout), and a coverage statement (languages, package
  managers, IaC/CI files, auth/secret surfaces, public entry points). This makes coverage auditable.
- **A summary** at `.security/report.md`: executive summary, scope, a severity-sorted findings table
  (ID, severity, status, title, location, link), the chained attack paths, dependency/CVE summary (only
  actionable, with reachability), redacted secrets summary, false positives considered, tool + manual
  coverage, recommended next actions, and blindspots / what wasn't scanned.

Finish with a short chat summary: counts by severity, the top one or two attack paths in plain language,
and the single highest-leverage fix. Keep logs out of chat — point to the files. Do **not** auto-apply
any patch.

## `.security/` layout

This layout matches the **Security Officer** agent so the two are drop-in compatible (see "Composing
with the Security Officer agent" below):

```
.security/
├── threat_model.md            # persistent; created once, refreshed as architecture changes
├── report.md                  # latest scan summary (exec summary + severity table + chains + coverage)
├── scan_manifest.md           # tools run/skipped, versions, commands, exit codes, coverage statement
├── findings/
│   └── SEC-NNN-slug.md        # one finding per file (example_finding shape), numbered by severity
├── tool-results/              # raw scanner output (JSON/SARIF), one file per tool; gitignored if noisy
├── validation/
│   └── SEC-NNN/               # repro notes, commands, captured output/artifacts per finding
└── patches/
    └── SEC-NNN-suggested.patch  # proposed (never auto-applied) fix diffs
```

Keep `threat_model.md`, `report.md`, `scan_manifest.md`, `findings/`, and `patches/` committed so the
security context persists across scans (later scans get faster by focusing on new commits, like Codex
incremental scans). `tool-results/` (and bulky `validation/` artifacts) can be gitignored if noisy.

## Reference map

- `references/threat-model.md` — how to build/refresh the threat model; format and what each section must cover.
- `references/tooling.md` — security tools per ecosystem (SAST, SCA/CVE, secrets, fuzzing), install +
  run commands, and offline fallbacks. Read before Step 3.
- `references/reporting.md` — validation method, severity/criticality calibration, exploit chaining, and
  the finding + summary report formats. Read before Steps 4–6.
- `references/policies/` — strict per-surface security rules. Read the ones matching the repo's stack:
  - `web-and-api.md` — injection (SQL/NoSQL/command/LDAP), XSS, SSRF, CSRF, IDOR/broken authz, SSTI,
    path traversal, open redirect, insecure deserialization, auth/session, rate-limiting, CORS, headers.
  - `memory-safety.md` — buffer/stack/heap overflow, use-after-free, double-free, integer overflow,
    format strings, OOB read/write, type confusion (C/C++, unsafe Rust, cgo, FFI).
  - `javascript-typescript.md`, `python.md`, `go.md`, `jvm.md` — language-specific dangerous APIs and idioms.
  - `secrets-and-supply-chain.md` — hardcoded secrets, dependency confusion, unpinned/unverified
    downloads, `curl | bash`, CI/release-artifact integrity, lockfile/typosquat risks.
  - `infra-and-iac.md` — Docker/Compose, Kubernetes, Terraform, Ansible, cloud IAM, network exposure,
    privilege/escape, world-writable paths (the `assets/example_finding.md` bug class).
- `assets/threat_model_template.md`, `assets/finding_template.md` — fill-in templates.
- `assets/example_finding.md`, `assets/example_threat_model.md` — anonymized, fully worked examples
  showing the target shape and quality bar. Read these to calibrate voice and depth before writing your own.
- `scripts/init_security.sh` — scaffold the `.security/` directory.
