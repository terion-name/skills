---
name: security-audit
description: >-
  Run a thorough, defender-first security audit of a codebase, modeled on the Codex/Aardvark
  pipeline: build/refresh a threat model, scan current code and recent commits for vulnerabilities and
  serious commit-introduced functional regressions, validate findings, chain exploitable issues, rank by
  severity, and write `.security/` artifacts. Use whenever the user invokes `/security-audit`,
  `/sec-audit`, `/sec-review`, or asks to scan/audit/review code they control for vulnerabilities,
  CVEs, XSS, SQLi, SSRF, RCE, secrets, memory-safety bugs, threat modeling, PR/diff security review, or
  asks whether code is safe. Defensive assessment of the user's own codebase only.
---

# Security Audit

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

0. **Tooling preflight** — before threat modeling or scanning, prove whether containerized security
   tooling is available. See `references/tooling.md` and `scripts/tooling_preflight.py`.
1. **Threat model** — establish or refresh `.security/threat_model.md`. See `references/threat-model.md`.
2. **Scope** — decide what to scan (full repo, a diff, a subtree) and partition it for parallel work.
3. **Current-HEAD scan** — fan out across the current tree: deterministic tools (SAST / SCA-CVE /
   secrets) **and** semantic sub-agent review, in parallel, per surface. See `references/tooling.md` and
   `references/policies/*`.
4. **Validate** — triage every tool output first, then reproduce candidate findings in the sandbox to
   kill false positives. See `references/reporting.md` ("Validation").
5. **CWE + severity + chaining** — map each finding to a primary CWE weakness, rate it, and chain
   related findings into attack paths. See `references/reporting.md` and `references/cwe/`.
6. **Report** — write one file per finding to `.security/findings/`, then a `.security/report.md` summary.
7. **Commit history review** — after the current-HEAD sweep, review commits incrementally from oldest to
   newest, using `.security/latest_reviewed_commit` as the cursor. See `references/commit-history-review.md`.
8. **Completion gate** — run `scripts/audit_completion_gate.py` before the final chat summary. If it
   fails, the audit is not complete; continue the missing work instead of reporting success.

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
  slug** (e.g. `SEC-auth-001`, `SEC-iac-001`) and its raw tool output into
  `.security/tool-results/<partition>/`, and by reserving `report.md`, `scan_manifest.md`, and final
  `SEC-NNN` numbering for the orchestrator after `task_await`. Tell each agent not to write the
  summary/manifest. The orchestrator merges, assigns final IDs after the highest existing ID in
  `.security/findings/` and `.security/fixed/`, builds the chains, and writes the top-level artifacts.

Division of labor: the **agent** owns the persona, guardrails, and per-finding review; the **skill** owns
the deep per-language policies, severity calibration, and cross-finding exploit chaining. Keep them in
sync — if you change the `.security/` layout or status vocab in one, change it in the other.

## Hard rules (delegate-first)

These are workflow constraints. Your edit/read tools remain available, but treat them as off-limits
except where explicitly allowed below — the point is to preserve your context for orchestration.

- **Delegate all audit work.** The main agent is the orchestrator only. It must not directly inspect
  product code, parse raw scanner output, perform dependency/CVE reachability analysis, run validation
  PoCs, trace call paths, decide whether a tool hit is real from raw evidence, or draft code-evidence
  sections from its own file reads. Every investigative or analytical task goes to a sub-agent.
- **Main-context allowlist.** In the main context, do only orchestration: read this skill and reference
  docs; read/write `.security` control artifacts and sub-agent reports; run `git` commands to determine
  HEAD/base/commit queues; run `scripts/init_security.sh`, `scripts/tooling_preflight.py`, and
  `scripts/audit_completion_gate.py`; create directories; assign final `SEC-NNN` IDs; merge sub-agent
  outputs; run the completion gate; request reruns when evidence is thin. Reading filenames/counts is
  fine. Reading product files or raw `.security/tool-results/*` content for analysis is not.
- **Log delegation.** Every sub-agent task must append a JSONL record to `.security/delegation_log.jsonl`
  with `phase`, `subagent_id` or worker name, scoped task, status, and output artifact. The completion
  gate requires this log for the expected audit phases.
- **No direct fallback.** If sub-agents are unavailable or fail, stop and report that the audit is blocked
  or ask the user whether to run an explicitly degraded single-agent audit. Do not silently continue in
  the main context.
- **Delegate investigation.** Spawn `explore` sub-agents with narrow prompts (one surface / directory /
  question each). Treat their reports as the source of repo facts (paths, symbols, callsites, control
  flow); if a report is ambiguous or contradicts other evidence, send a follow-up sub-agent instead of
  opening files yourself.
- **Delegate scanning and tool triage.** Spawn sub-agents to run scanners and separate sub-agents to
  triage raw outputs/advisories. The main agent may check that tool output files exist and that
  `tool_triage.md` accounts for them, but must not parse raw SARIF/JSON/CVE output itself.
- **Delegate commit review.** After the current-HEAD sweep, immediately continue into commit-review
  subagents for the incremental commit flow. Prefer many one-commit subagents over broad queue workers,
  and require each no-finding result to include the invariants, callers, and future touches it checked.
  Broken-invariant notes such as fail-open guards, billing drift, exposed internals, or unsafe config
  combinations must be promoted to candidates for validation. Keep the queue, cursor, progress log,
  dedupe, and final artifacts with the orchestrator.
- **Delegate validation evidence; own final judgment.** The orchestrator owns the final validation
  status, severity calibration, and exploit-chain decision, but gathers evidence only through validation
  sub-agents. If reproduction or targeted code proof is needed, spawn a validation sub-agent with the
  exact question. The main agent reviews the returned evidence, asks for reruns if weak, and then makes
  the final decision.
- **`bash` is for orchestration only in the main context:** `git` queue/base commands, scaffolding,
  preflight, completion gate, counts, and artifact moves. Do not run scanners, builds, tests, PoCs,
  `rg`/`sed`/`cat`/`nl` over product code, or raw tool-result parsing in main context.
- **Do not patch the codebase as part of the scan.** Like Codex, you *propose* patches as diffs inside
  findings; you do not apply them. If the user explicitly asks you to fix afterward, that's a separate
  step (and a good fit for the `orchestrate` skill).
- **The current worktree is the source of truth for `.security/`.** Use only `.security/**` artifacts
  that exist on disk now. If `.security` files are tracked in git but deleted in the worktree, treat that
  as an intentional reset/fresh start unless the user explicitly asks you to recover old artifacts. Do
  not read deleted `.security` files from `HEAD`, `git show`, prior commits, stashes, or reflogs to seed
  the threat model, cursor, progress, findings, fixed reports, numbering, or dedupe. Git history is for
  reviewing product commits, not resurrecting audit state.
- **Artifacts are append-only-ish.** Never delete prior findings without the user's say-so; supersede them.
  When a finding is fixed, move it from `.security/findings/` to `.security/fixed/` and keep its original
  `SEC-NNN` ID. Never recycle IDs.
- **No false completion.** Do not say "complete" or produce the final chat summary until the completion
  gate passes. If history was in scope, `.security/latest_reviewed_commit` must reach the audited `HEAD`.
  If `.security/tool-results/` contains scanner output, `.security/tool_triage.md` must account for every
  raw result file and every CVE/GHSA/advisory ID as a finding, explicit dismissal, or blocked validation.
  `candidate` is an intermediate triage decision, not a final state; before completion, every candidate
  from tools must be promoted to a normal
  `findings/SEC-NNN-[SEVERITY]-[CWE-NNN-label]-*.md` or
  `fixed/SEC-NNN-[SEVERITY]-[CWE-NNN-label]-*.md` report,
  dismissed with concrete evidence, or marked blocked with the missing evidence source.
- **CWE is required for findings.** Every normal finding/fixed report must include a primary CWE mapping
  in metadata (`CWE`, `CWE description`, `CWE mapping`, and `Standards: CWE-...`). Use
  `references/cwe/cwe-catalog.jsonl` and `references/cwe/cwe-labels.json`; do not invent ad hoc CWE
  names or filename labels when the catalog contains the code.
- **Ask for first-run history depth.** When commit history is in scope, `.security/latest_reviewed_commit`
  is absent/empty, and the user's initial prompt did not explicitly specify a history range/depth, stop
  and ask before creating `.security/commit_review_queue.txt`. Offer choices such as `latest N commits`,
  `since <date/duration>`, `range <base>..HEAD`, or `all history`; do not silently choose a default.

## Prerequisites

- **Max Task Nesting Depth ≥ 1** (Settings → Agents → Task Settings) so `task` sub-agents can be spawned.
  If sub-agent spawning fails, surface that as the blocker. You can still run a degraded single-threaded
  scan yourself, but say so explicitly — parallel delegation is the intended mode.
- A git repository is ideal (enables diff/commit scoping and patch generation) but not required.
- Docker is the preferred scanner runtime. Network access may be needed to pull scanner images or update
  rule/CVE databases; `references/tooling.md` defines the strict preflight and offline/degraded options.
- CWE reference data lives under `references/cwe/`. Use the bundled catalog by default. If the catalog is
  missing, or the user asks to refresh CWE, run `scripts/update_cwe_reference.py` before drafting findings
  and record the catalog version/date in `.security/scan_manifest.md`.

## Step 0 — Tooling preflight (must be first)

Before threat modeling, partitioning, or spawning scan agents, read `references/tooling.md` and run:

```bash
scripts/tooling_preflight.py --write .security/tooling_preflight.md
```

This is a gate, not a courtesy check:

- If Docker works, run instrumental security scans in containers with the official per-tool images listed
  in `references/tooling.md`. Do not skip a required scanner just because the host machine lacks the
  local binary.
- If Docker is missing or the daemon cannot run, stop before the audit scan. Tell the user which scanners
  are required for this repo, which local tools are missing, and recommend installing/starting Docker so
  scans run in isolated containers with mounted code.
- Offer exactly one degraded option: the user may explicitly say to continue with only available local
  tools. Do not infer approval from silence. If they approve, record "user-approved degraded tooling" and
  every missing scanner in `.security/scan_manifest.md` and `.security/report.md`.
- If scanner images or CVE/rule DB updates cannot be pulled because of network/registry restrictions,
  treat that like missing Docker: list the blocked image/DB and stop unless the user explicitly approves
  continuing with cached/available tools.

## Step 1 — Threat model

Read `references/threat-model.md`, then:

- If `.security/threat_model.md` exists in the current worktree, **read it and treat it as the source of
  truth** for trust boundaries, assumptions, and criticality calibration. Refresh only the parts the user
  flags as stale, or that the current diff obviously changes.
- If it does **not** exist in the current worktree, build it now. Do not recover a deleted tracked threat
  model from git history. Run `scripts/init_security.sh` to scaffold the `.security/` directory, then
  spawn 2–4 `explore` sub-agents in parallel to map the architecture (entry points, auth,
  DFD/source-sink flows, data stores, external I/O, privileged operations, build/release/supply-chain).
  Synthesize their reports into `.security/threat_model.md` using `assets/threat_model_template.md`.

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
I/O, deserialization, subprocess/shell, crypto, IPC), by DFD flow / trust-boundary crossing, by business
invariant (tenant isolation, billing/resource accounting, workflow state), by top-level directory/service,
or by language. Each partition becomes one scan sub-agent. Maximize independent-batch size; partitions
rarely depend on each other, so default to running them all at once.

## Step 3 — Scan (parallel fan-out)

For each partition, spawn a scan sub-agent (`run_in_background: true`). Give each the **scan task brief**
below. Then `task_await` the batch.

Each sub-agent does two complementary things, because — as Codex documents — LLM semantic review and
deterministic tooling catch different bugs:

1. **Run deterministic tools** for its partition (SAST, dependency/CVE scan, secret scan). Exact tools
   and container commands per ecosystem are in `references/tooling.md`. If Step 0 found Docker available,
   use containers rather than host-local binaries. If Step 0 did not complete, or degraded local-only
   scanning was not explicitly approved by the user, stop and ask the orchestrator to complete Step 0.
   Tool output is *input to triage*, not a finding by itself — every tool hit must be confirmed against
   real code before it becomes a candidate. But raw tool output is never allowed to stay untriaged.
   After tools run, write `.security/tool_triage.md` using `assets/tool_triage_template.md`: one row per
   tool-output file, and for SCA/CVE tools one row per advisory ID (`CVE-*`, `GHSA-*`, ecosystem
   advisory) with decision `finding:<SEC-NNN>`, `candidate`, `dismissed:<reason>`, or `blocked:<reason>`.
2. **Semantic review** against the relevant policy file(s) in `references/policies/`. These encode the
   strict rules per language/surface (injection, XSS, SSRF, deserialization, auth/IDOR, memory safety,
   secrets, IaC, etc.) with the dangerous patterns and the sinks to grep for.
3. **Business-invariant review** for full audits: money/credits, quotas, tenant boundaries, authorization
   scopes, workflow state machines, idempotency/replay, lifecycle events, and resource accounting. Do this
   even when there is no commit diff; scanners rarely find these.

Sub-agents return **candidate findings** (suspected, not yet validated), each with: title, location
(`path:line`), the vulnerability class, a one-line why, and the data/control flow from source to sink.
They do **not** assign final severity — that's your job after validation and chaining.

After scanner sub-agents finish, spawn dedicated **tool-triage sub-agents** for raw outputs/advisory sets
before validation. Do not parse SARIF/JSON/CVE output in the main context. The orchestrator only assigns
output groups to workers, receives their triage rows, checks coverage/counts, and asks for reruns when a
tool file or advisory ID is missing.

### Scan task brief (Orchestrator → scan sub-agent)

```

### Tool-triage task brief (Orchestrator → tool-triage sub-agent)

```
- Task: Triage security-audit tool outputs for <tool/output group>.
- Inputs: <raw .security/tool-results paths>, threat model path, relevant package/runtime context from scan sub-agent reports.
- Do:
  1. Parse only the assigned raw tool outputs.
  2. For each raw output file, produce a Raw outputs row for .security/tool_triage.md.
  3. For each SCA advisory/CVE/GHSA/ecosystem advisory, determine package, version, fixed version,
     dependency scope, runtime/deployment evidence, and decision.
  4. Promote production/runtime advisories with reachable or not-disproven reachability to candidate findings.
     Related advisories may be grouped into one coherent dependency finding by package/service/root cause,
     but the finding must list the advisory IDs and affected runtime evidence.
  5. Dismiss only with concrete evidence: dev-only, test-only, not installed, not packaged, unreachable,
     fixed by current lockfile, scanner false positive, or validation blocked.
- Report back: tool_triage rows plus candidate findings. Do not assign final SEC IDs or final severity.
- Constraints: read-only; do not modify code; do not summarize raw output without per-file/advisory decisions.
```
- Task: Security-audit partition <name> for vulnerabilities.
- Surface / scope: <files, directories, or attack surface this partition covers>
- Threat-model context: <relevant trust boundaries + what's reachable, pulled from .security/threat_model.md>
- Do:
  1. Confirm Step 0 tooling preflight is present. If Docker was available, run deterministic tools through
     the official scanner containers listed in references/tooling.md, with source mounted read-only and
     outputs under .security/tool-results/. If Docker was not available, proceed only when the orchestrator
     gives explicit user-approved degraded-tooling permission. Only run "safe/static" tools per the
     skill's repo-safety tiering — never project install/build scripts.
     If a tool reports anything that survives triage or cannot be dismissed, turn it into a normal
     candidate finding; do not write Markdown summaries in .security/tool-results/.
  2. Semantically review the code against references/policies/<relevant>.md. Look specifically for the
     sink patterns and dangerous APIs listed there.
  3. Build a small source/sink/guard table for this partition: untrusted sources, dangerous sinks,
     propagators, sanitizers/guards, and scanner modeling gaps. Use it to drive review.
  4. Review relevant business invariants from the threat model (tenant isolation, billing/resource
     accounting, workflow state, idempotency/replay, lifecycle cleanup).
  5. For each suspected issue, trace source -> sink or invariant break and confirm it against the actual
     code (no tool-only findings).
  6. Report every raw tool output path and every CVE/GHSA/advisory ID found by SCA tools with a triage
     decision. Production/runtime dependency CVEs that are reachable or whose reachability cannot be
     disproven with code/package evidence must become candidate findings; do not bury them in raw output.
  7. Record tools run/skipped (+ versions, commands, exit codes, why-skipped) for the manifest.
- Report back: a list of CANDIDATE findings. Each = {title, path:line, vuln_class, one_line_why,
  source_to_sink_flow_or_broken_invariant, primary_cwe_if_obvious, standards_mapping_if_obvious,
  supporting evidence snippets}.
  Mark anything you could not confirm as "needs validation".
- Do NOT assign final severity, do NOT chain exploits, do NOT patch. Keep scope to this partition.
- Constraints: read-only review + running scanners only; do not modify code; PoC only inside the sandbox if trivially safe.
```

## Step 4 — Validate (you, the orchestrator)

This is the step that separates a real finding from scanner noise — Codex's core value-add. Read the
"Validation" and "Tool-derived findings" sections of `references/reporting.md`.

First, finish delegated tool triage. `.security/tool_triage.md` is mandatory whenever
`.security/tool-results/` contains output. Tool-triage sub-agents must account for each scanner output
file and each dependency advisory from Trivy/Grype/OSV/Dependency-Check/dep-scan/npm/pnpm/yarn/etc. The
orchestrator merges their rows and checks coverage; it does not inspect raw tool output itself. Tool
triage may use `candidate` while validation is still running, but the final audit must not leave
`candidate` rows unresolved. Actionable tool findings are normal SEC reports, not separate Markdown
reports in `tool-results/` or a bucket of "follow-up" CVEs in the summary.

Then validate candidates through validation sub-agents (prioritize the scariest first):

- For each candidate, spawn a validation sub-agent with the exact claim, paths, source/sink flow,
  supporting tool rows, threat-model assumptions, and requested proof.
- Where practical, the validation sub-agent reproduces it in the sandbox: minimal PoC proving source
  reaches sink, captured command/stdout/stderr/exit code/artifact. The main agent does not run PoCs.
- If reproduction is not possible, the validation sub-agent performs targeted code-review proof and
  records why dynamic reproduction was skipped.
- The orchestrator reviews returned evidence and assigns `validated`, `likely`, `unvalidated`, or
  `false-positive`. If evidence is thin, send a follow-up validation sub-agent instead of reading the
  code yourself.

If a validation check fails because of an environment gap (tool missing, network 403), record the
blindspot and delegate code-review validation — don't silently drop the finding.

### Validation task brief (Orchestrator → validation sub-agent)

```
- Task: Validate candidate <temp id/title>.
- Candidate: <title, suspected class, affected paths, source->sink or broken invariant, tool-triage rows>.
- Threat model context: <relevant assets/trust boundaries/reachability>.
- Do:
  1. Confirm whether attacker-controlled input or changed behavior reaches the sink/invariant break.
  2. Prefer a safe minimal repro only if it does not execute risky project lifecycle code or touch external systems.
  3. If using code-review proof, cite path:line evidence for every hop and explain why dynamic repro was skipped.
  4. Check negative evidence: guards, sanitizers, allowlists, deployment preconditions, compensating controls, later fixes.
  5. Return validation rubric, evidence snippets, recommended status, confidence, blindspots, and patch regression risk.
- Constraints: read-only except safe validation artifacts under .security/validation/<temp id>/; no source patching.
```

## Step 5 — CWE + severity + exploit chaining

For each validated/likely finding, use sub-agent evidence and follow `references/reporting.md`:

- **Map CWE first.** Search `references/cwe/cwe-catalog.jsonl` and `references/cwe/cwe-labels.json` by
  candidate class, sink, and common name. Choose the closest primary **weakness** entry, not a broad
  category, unless no weakness fits. Record `CWE: CWE-NNN - <short label>`, the catalog description, and
  a one-sentence mapping rationale. CWE guides classification and remediation language; it is not proof
  that the issue exists and it must not replace validation evidence.
- Assign **likelihood** and **impact**, derive a **matrix severity**, then apply threat-model policy to
  reach a **final severity** (critical / high / medium / low). Record the rationale, assumptions, and the
  attacker preconditions — the attack-path block in `assets/example_finding.md` is the target shape.
- **Chain.** Individually-medium findings can compose into a critical kill-chain (e.g. an auth bypass +
  an IDOR + a deserialization sink = unauthenticated RCE). Look across findings for chains and document
  them: the ordered path, what each link grants, and the combined severity (which can exceed any single link's).
  If chain evidence requires extra code/path checks, delegate a chain-validation sub-agent.

## Step 6 — Report

Write artifacts (read `references/reporting.md` for the exact templates, and use `assets/finding_template.md`):

- **One file per finding** at `.security/findings/SEC-NNN-[SEVERITY]-[CWE-NNN-label]-<slug>.md`, drafted by finding-draft
  sub-agents and finalized mechanically by the orchestrator, in the `assets/example_finding.md` shape:
  title, criticality (with attack-path severity), status, metadata, CWE code/description/mapping, summary,
  validation (rubric + report), evidence (code excerpts with notes), proposed patch (diff), and
  attack-path analysis (final/likelihood/impact/assumptions/path/path-evidence/narrative/controls/
  blindspots). Assign IDs chronologically by starting after the highest `SEC-NNN` file currently present
  on disk in `.security/findings/` or `.security/fixed/`; do not count deleted tracked files from git
  history. Use the uppercase final severity in the filename and the primary CWE `filename_tag` from
  `references/cwe/cwe-labels.json`, e.g.
  `SEC-001-[CRITICAL]-[CWE-22-path-traversal]-arbitrary-file-read.md`. Do not generate new labels at
  report time unless the CWE is absent from the catalog; if that happens, use the CWE official name,
  record the custom label decision in the finding, and prefer refreshing the catalog. Do not renumber or
  reuse fixed IDs that still exist in the worktree. Put repro artifacts under `.security/validation/SEC-NNN/`.
  Keep proposed patches embedded in the finding file.
- **Tool triage** at `.security/tool_triage.md` using `assets/tool_triage_template.md`: every raw
  scanner output file and every dependency advisory/CVE/GHSA from tool output must have a decision,
  linked finding, or explicit dismissal/blocker.
- **A scan manifest** at `.security/scan_manifest.md`: Step 0 tooling preflight decision, Docker status,
  required scanner images, tools detected + versions, commands run + exit codes + output paths (flagged
  static vs. project-executing), tools skipped + why (container image unavailable, DB/rules blocked,
  user-approved degraded local-only missing binary, unsupported ecosystem, too risky, timeout), and a
  coverage statement (languages, package managers, IaC/CI files, auth/secret surfaces, public entry
  points). This makes coverage auditable.
- **A summary** at `.security/report.md`, drafted by a report-draft sub-agent from the finding files,
  tool triage, manifest, and commit ledger, then sanity-checked by the orchestrator: executive summary,
  scope, a severity-sorted findings table (ID, severity, CWE, status, title, location, link), the chained
  attack paths, dependency/CVE summary (only actionable, with reachability), tool triage summary,
  redacted secrets summary, false positives considered, tool + manual coverage, recommended next actions,
  and blindspots / what wasn't scanned.

Do not stop here when commit history is in scope. The current-HEAD report is an interim checkpoint; keep
going into Step 7 in the same run unless the user explicitly scoped the audit to current HEAD / a single
diff / a subtree, or explicitly told you to stop before history review. Do **not** auto-apply any patch.

## Step 7 — Commit history review

After the current-HEAD sweep and interim report, read `references/commit-history-review.md` and run the
incremental per-commit flow immediately unless the user explicitly scoped the request to current HEAD, a
single diff/PR, or a subtree. Do not merely write a queued backlog and stop; creating
`.security/commit_review_progress.md` is the start of the history pass, not a completion point. This flow
looks for security issues and serious functional regressions introduced by individual commits.

Use `.security/latest_reviewed_commit` as the durable cursor only if it exists in the current worktree and
is non-empty. If it is deleted or absent, treat this as a first run. The first-run depth must come from
the user's initial prompt; if it does not, ask the user before queue creation. Supported scopes include
`latest_commits`, `since`, `latest_commits_or_since`, `range`, and `all`. On later runs, review commits
after the cursor through `HEAD`. Always process oldest to newest. Do not recover a deleted cursor from
git history.

Actively use subagents and keep durable progress:

- Before reviewing, write `.security/commit_review_start_cursor`, `.security/commit_review_target_head`,
  `.security/commit_review_scope.json`, and `.security/commit_review_queue.txt` with the exact ordered
  queue. Then update `.security/commit_review_progress.md`, `.security/commit_review_ledger.jsonl`, and
  `.security/commit-reviews/<sha>.md` as each commit is actually assessed so a resumed agent can continue
  without relying on chat context. `commit_review_scope.json` records the user-selected first-run scope,
  for example `{"mode":"latest_commits","count":1000}` or `{"mode":"since","since":"2026-04-01"}`.
- The queue is immutable once written for that pass. Do not shrink, renormalize, or drop old queue entries
  because wall-clock time moved during a long run. If HEAD changes, finish the queued target HEAD first or
  create a new explicit follow-up queue after recording the previous pass state.
- Spawn commit-review subagents in background batches. Scope each subagent to one commit unless a tiny
  run of related commits is safer as a small batch.
- For each commit, first decide whether it is obviously non-functional. Skip docs-only, formatting-only,
  and purely visual changes when they cannot affect runtime behavior, but record the skip reason.
- For functional commits, review the diff and trace directly affected logic: call paths, trust boundaries,
  downstream consumers, config/defaults, data/control flow, and security-sensitive invariants.
- After each commit is assessed or skipped, append a valid JSONL ledger entry, write its per-commit review
  artifact, and only then write that SHA to `.security/latest_reviewed_commit`. Never bulk-advance the
  cursor. If you cannot finish the queue, leave the cursor at the last actually reviewed commit and report
  history review in progress.

Use the same validation, severity, chaining, and finding format as the current-HEAD scan. If a commit
introduced an issue, set `Commit: <introducing sha>` in the finding metadata. Before writing, reconcile
only against `.security/findings/` and `.security/fixed/` files currently present on disk: enrich an
existing report if it is the same issue; write to `.security/findings/` if still present; write to
`.security/fixed/` with `Fixed in commit: <sha>` if a later commit already fixed it. Do not dedupe
against deleted reports from git history unless the user explicitly asked to restore old audit state.
After the per-commit pass, update `.security/report.md` and `.security/scan_manifest.md` with
commit-review coverage, skipped commits, new/enriched findings, and the latest cursor.

## Step 8 — Completion gate

Before the final chat summary, run the deterministic completion gate and save its output:

```bash
scripts/audit_completion_gate.py --history-required yes > .security/completion_gate.txt 2>&1
```

Use `--history-required no` only when the user's original prompt explicitly scoped the audit to current
HEAD, a diff/PR, or a subtree and the report/manifest state why history is out of scope.

If the gate fails, do **not** report the audit as complete. Fix the missing work:

- If history is incomplete, continue Step 7 until `.security/latest_reviewed_commit` equals `git rev-parse HEAD`.
- If the history ledger/queue/artifacts are incomplete, write the missing per-commit entries by actually
  reviewing those commits; do not synthesize ledger rows to satisfy the gate.
- If the delegation log is missing phases, dispatch the missing sub-agent work and record real outputs;
  do not synthesize delegation rows for work done in the main context.
- If tool outputs are untriaged, finish `.security/tool_triage.md`; create findings for actionable or
  not-disproven production CVEs, and record evidence-backed dismissals for non-actionable advisories.
  Do not leave unresolved `candidate` decisions in `.security/tool_triage.md`.
- If a required artifact is missing, write it.

Only after the gate passes, finish with a short chat summary: counts by severity, the top one or two
attack paths in plain language, the highest-leverage fix, and the commit history cursor/coverage. Keep
logs out of chat; point to the files. If findings exist, include a short "Upload findings" note with
user-run commands for GitHub/GitLab/Plane or point to the uploader `--help`; do not run those scripts
unless the upload rule below was satisfied.

## `.security/` layout

This layout matches the **Security Officer** agent so the two are drop-in compatible (see "Composing
with the Security Officer agent" below):

```
.security/
├── threat_model.md            # persistent; created once, refreshed as architecture changes
├── tooling_preflight.md        # Docker/tool availability gate and required scanner set
├── latest_reviewed_commit     # latest commit SHA assessed by the incremental commit-review flow
├── commit_review_start_cursor # cursor before this history pass, or FIRST_RUN
├── commit_review_target_head  # HEAD the queue is expected to reach
├── commit_review_scope.json   # user-selected first-run history scope/depth
├── commit_review_queue.txt    # exact ordered commits for this pass, one SHA per line
├── commit_review_progress.md  # in-flight commit queue/progress so long reviews can resume
├── commit_review_ledger.jsonl # one machine-checkable review decision per queued commit
├── commit-reviews/            # one auditable per-commit review artifact per queued commit
├── report.md                  # latest scan summary (exec summary + severity table + chains + coverage)
├── scan_manifest.md           # tools run/skipped, versions, commands, exit codes, coverage statement
├── tool_triage.md             # every tool output/advisory mapped to finding/dismissal/blocker
├── delegation_log.jsonl       # one record per sub-agent task/output
├── completion_gate.txt        # output of scripts/audit_completion_gate.py from the final pass
├── findings/
│   └── SEC-NNN-[SEVERITY]-[CWE-NNN-label]-slug.md  # one finding per file, chronological IDs
├── fixed/
│   └── SEC-NNN-[SEVERITY]-[CWE-NNN-label]-slug.md  # fixed findings moved here; IDs stay reserved
├── tool-results/              # raw scanner output only; actionable hits become normal findings
├── tool-cache/                # scanner DB/cache mounts; gitignored
└── validation/
│   └── SEC-NNN/               # repro notes, commands, captured output/artifacts per finding
```

Keep `threat_model.md`, `latest_reviewed_commit`, `commit_review_progress.md`, `report.md`,
`scan_manifest.md`, `findings/`, and `fixed/` committed so the security context persists across scans
(later scans get faster by focusing on new commits, like Codex incremental scans). If the user deletes
those tracked artifacts in the worktree, respect that as a reset and start from the files that remain.
Raw files in `tool-results/` and bulky `validation/` artifacts can be gitignored if noisy.
`tool-cache/` should always be gitignored; it is scanner cache/database state, not audit evidence.

## CWE reference maintenance

Use the generated CWE catalog for taxonomy mapping and filename labels:

```bash
scripts/update_cwe_reference.py
```

The updater downloads MITRE's latest `cwec_latest.xml.zip`, extracts the XML catalog, and writes
`references/cwe/manifest.json`, `references/cwe/cwe-catalog.jsonl`, `references/cwe/cwe-labels.json`,
and `references/cwe/cwe-index.md`. For offline development or testing against a fixed view, pass
`--xml <path-to-cwe.xml>`. The generated labels are deterministic: the updater prefers short taxonomy
labels such as PLOVER when useful and falls back to a normalized CWE name. Agents should use those
pre-generated labels in filenames instead of asking an LLM to invent labels during an audit.

## Upload findings to issue trackers

Use the bundled upload scripts when the user wants to create tracker issues from `.security/findings/`
without exposing an airgapped GitHub Enterprise, GitLab, or Plane service to the agent. The scripts run
where the user has network access, read the provider token from an environment variable, parse findings
deterministically, and upload each matching finding as one issue/work item. They do not upload raw
`.security/tool-results/`.

Default behavior: **do not run upload scripts after an audit.** At the end of a security audit, if
findings exist, print concise user-run instructions and point to each script's `--help`. This keeps
airgapped or self-hosted issue trackers under the user's control.

Only run an upload script yourself when the user's **initial audit prompt** explicitly asks to upload
findings and provides the required arguments for the chosen provider (for example provider, project id,
host/workspace when needed, label/issue type if desired, and token env var if not using the default).
If upload was requested later as a separate follow-up, treat it as a separate task and run only the
specific requested script. Never guess a project id, host, workspace, issue type, or token env var.

Common options:

```bash
scripts/upload_findings_github.py --project-id owner/repo --label security --finding-index-from 12
scripts/upload_findings_gitlab.py --project-id group/project --host https://gitlab.example.com --label security
scripts/upload_findings_plane.py --project-id workspace-slug/project-uuid --host https://plane.example.com --label security --issue-type "Security Finding"
```

- `--project-id`: GitHub `owner/repo`; GitLab numeric ID or URL-encoded path input (`group/project` is encoded by the script); Plane `project_uuid` plus `--workspace-slug`, or `workspace_slug/project_uuid`.
- `--host`: optional provider base URL for self-hosted GitLab or Plane; GitHub Enterprise hosts are converted to `/api/v3`.
- `--finding-index-from`: optional first `SEC-NNN` index to upload.
- `--label`: optional label; scripts create it if missing.
- `--issue-type`: Plane-only work item type; created if missing. The Plane script also creates custom properties mirroring the security finding template (`SEC ID`, `Severity`, `Status`, `Category`, `CWE`, `CWE description`, `CWE mapping`, `Standards`, `Commit`, `Fixed in commit`, `Resolution`, `Location`, `Detected by`, `Finding path`) and fills them deterministically.
- `--api-key-env-name`: optional token env var, defaulting to `GITHUB_API_KEY`, `GITLAB_API_KEY`, or `PLANE_API_KEY`.
- `--include-fixed`: also upload `.security/fixed/` historical findings.
- `--dry-run`: parse and print planned uploads without API writes.
- Each uploader has detailed help and examples: `scripts/upload_findings_github.py --help`,
  `scripts/upload_findings_gitlab.py --help`, `scripts/upload_findings_plane.py --help`.

## Reference map

- `references/threat-model.md` — how to build/refresh the threat model; format and what each section must cover.
- `references/tooling.md` — security tools per ecosystem (SAST, SCA/CVE, secrets, fuzzing), install +
  container run commands, and strict missing-tool behavior. Read before Step 0 and Step 3.
- `references/reporting.md` — validation method, severity/criticality calibration, exploit chaining, and
  the finding + summary report formats. Read before Steps 4–7.
- `references/commit-history-review.md` — incremental per-commit review after the current-HEAD sweep:
  cursor handling, commit selection, skip rules, subagent prompt, and fixed/unresolved reconciliation.
  Read before Step 7.
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
- `assets/threat_model_template.md`, `assets/finding_template.md`, `assets/tool_triage_template.md` —
  fill-in templates.
- `assets/example_finding.md`, `assets/example_threat_model.md` — anonymized, fully worked examples
  showing the target shape and quality bar. Read these to calibrate voice and depth before writing your own.
- `scripts/init_security.sh` — scaffold the `.security/` directory.
- `scripts/tooling_preflight.py` — fingerprint the repo, check Docker, identify required scanner images
  and missing local tools, and write `.security/tooling_preflight.md`.
- `scripts/audit_completion_gate.py` — fail-fast guard before the final summary; verifies required
  artifacts, history cursor completion, and scanner/advisory triage.
- `scripts/upload_findings_github.py`, `scripts/upload_findings_gitlab.py`, `scripts/upload_findings_plane.py` —
  upload parsed findings to issue trackers from a user-controlled network environment.
