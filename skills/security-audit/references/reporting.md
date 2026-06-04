# Validation, severity, chaining, and reporting

This covers Steps 4–7: how to validate a candidate, how to rate it, how to chain findings, and the exact
output formats. The target shapes are `assets/example_finding.md` (per finding) and the summary table below.

---

## Validation

Validation is what makes this more than a scanner: a candidate becomes a *finding* only when you've
shown it's real. This is the orchestrator's job because it needs the whole-repo picture.

For each candidate (scariest first), pick the strongest validation you can:

**Tier 1 — dynamic reproduction (preferred).** Build the minimal PoC that proves the source reaches the
sink, inside the sandbox. Examples: send a request whose payload reaches the SQL string / shell / file
path; craft a tar whose entry escapes the extraction dir; present a forged token that the auth check
accepts; trigger the overflow under a sanitizer. Capture the command, stdout/stderr, exit code, and any
artifact (a written file, a crash, a leaked value). This is the `# Validation` evidence block in the
example finding.

**Tier 2 — targeted code-review proof.** When dynamic repro isn't possible (declarative/IaC bug, missing
toolchain, network blocked, or repro would be destructive), trace the exact code path with `path:line`
evidence at every hop and explain why the guard is absent or bypassable. Explicitly record *why* dynamic
validation was skipped (e.g. "ansible not installable, proxy 403; validated the extraction primitive
directly instead") — the example finding does exactly this.

**Tier 3 — unvalidated.** You can't reproduce it and the code path is ambiguous. Keep it, but label it
`unvalidated` and lower its confidence. Don't inflate severity on unvalidated findings.

Then classify on a four-tier ladder:

- `validated` — reproduced, or proven with strong code/dataflow evidence.
- `likely` — strong attack path and impact, but not fully reproduced (the honest middle; use it instead
  of over-claiming `validated` or under-claiming a clear bug as `unvalidated`).
- `unvalidated` — plausible but missing evidence; report only if high-impact/important.
- `false-positive` — drop from `findings/`, but list in the summary's "considered and dismissed" section
  so the user sees the coverage.

**Validation rubric.** Write an explicit checkbox rubric per finding (see the example finding's `## Rubric`)
— each box is a claim you confirmed. This makes the finding auditable and forces you to actually check
each link rather than asserting the conclusion. Save repro notes/commands/output under
`.security/validation/SEC-NNN/`.

**Negative evidence and revalidation.** Every finding should say what would have made it a false positive
and what you checked: ownership guards, sanitizers, allowlists, deployment preconditions, framework
behavior, compensating controls, or later fixes. Also include a short revalidation plan for the proposed
fix and the main patch regression risk. When the user later remediates a finding, rerun that specific
validation plan before moving it to `.security/fixed/`.

**Secret redaction.** When evidence involves a real secret, never write the full value into a finding,
validation artifact, or chat. Record location + type + a redacted fingerprint that's enough to locate
and triage it: `AWS-key-like token at config/prod.env:12, prefix AKIA…/suffix …X7Q, confidence high`.
Recommend rotation + history purge.

---

## Severity and criticality

Compute severity in three moves, recorded in the finding's attack-path block:

1. **Likelihood** (low/medium/high): how reachable and how hard to trigger. Remote + unauthenticated +
   deterministic → high. Requires local access, a race, or an operator action → lower.
2. **Impact** (low/medium/high): what successful exploitation grants. Root/RCE/full data disclosure →
   high. Limited info leak or DoS → lower.
3. **Matrix severity** = combine likelihood × impact, then **adjust by threat-model policy** to a final
   severity. The policy adjustment is where the threat model earns its keep: the same matrix severity is
   raised or lowered based on trust boundary and reachability for *this* project. Record `Matrix
   severity`, `Policy adjusted`, and `Final` separately (as the example does: `Final: high | Matrix
   severity: medium | Policy adjusted: medium`), with a one-paragraph rationale for any divergence.

Severity definitions come from the threat model's §4 calibration. If none exists, fall back to:

| Severity | Meaning |
|----------|---------|
| **Critical** | Unauthenticated RCE/admin; supply-chain compromise of root-executed artifacts; sandbox→host escape; control-plane secret leak. |
| **High** | Authenticated privesc; cross-tenant data exposure; local→root needing only low-priv access; management auth bypass. |
| **Medium** | Local unprivileged secret/file disclosure; DoS; missing crypto integrity (availability only); operator-only injection. |
| **Low** | Static-docs XSS; verbose error leakage; CI/test-only with no released-artifact impact; missing rate-limit behind an IdP. |
| **Informational** | Security-adjacent correctness, hardening, observability, or operational regression with no confirmed attacker-controlled exploit path yet, but useful for history and follow-up. |

Be honest about what *lowers* severity — local-only, requires operator action, requires a pre-existing
foothold. The example finding keeps a root-file-write at **high** rather than critical precisely because
it's local-only and needs a root playbook run. Calibrated severity builds trust; inflated severity burns it.

In commit-history review, keep informational candidates when they affect a security control, billing or
resource-accounting invariant, tenant/session lifecycle, release safety, or evidence needed to validate a
future exploit chain. Mark them `informational` rather than dropping them as "not security" too early.

---

## Exploit chaining

Individual findings rarely tell the whole story. The point of chaining is to show that findings which
look medium in isolation can compose into a critical kill-chain — and to quantify *that*.

For each plausible chain:

- Order the links: what the attacker does first, what each step grants, what it unlocks next.
- Note the **entry trust level** (unauthenticated? local? operator?) and the **terminal impact**.
- Assign the chain a severity that reflects the *composed* outcome — which can exceed any single link.
  An auth-bypass (high) + an IDOR (medium) + a deserialization sink (high) reachable only post-auth can
  become **unauthenticated RCE (critical)** as a chain even though no single finding was critical-remote.
- Reference the constituent finding IDs so the chain is traceable.

Classic chains to look for: input-validation gap → injection sink; SSRF → cloud metadata → credential
theft → privesc; path traversal → arbitrary write → cron/sudoers/systemd → RCE (the example finding's
class); auth bypass → admin API → secret read → lateral movement; prototype pollution → gadget → RCE;
file upload → content-type confusion → stored XSS → session theft.

Document chains in `.security/report.md` and cross-link the findings.

---

## Per-finding report format

One file per finding at `.security/findings/SEC-NNN-<slug>.md`, following `assets/finding_template.md`
(which mirrors `assets/example_finding.md`). Required sections:

- **Header:** `Title`, `Criticality: <level> (attack path: <level>)`, `Status: <validated|likely|
  unvalidated|false-positive>`. In commit/diff mode, also tag `Origin: <introduced-by-diff|pre-existing|
  uncertain>` so reviewers know whether the PR caused it.
- **# Metadata:** repo, commit, fixed-in commit if applicable, author (if known), created date, category
  (`auth|injection|ssrf|supply-chain|secrets|cve|container|iac|crypto|memory|functional-regression|other`),
  standards mapping (`ASVS vX.Y.Z-...`, `OWASP APIx:YYYY`, `CWE-...`, `NIST SSDF ...`, `SLSA`/Scorecard
  where applicable), detected-by (`manual|semgrep|trivy|commit-review|...`), signals (e.g. `Security,
  Validated, Patch generated, Attack-path`), resolution if applicable. In commit-history review, `Commit`
  is the commit that introduced the issue; `Fixed in commit` is the later commit that remediated it, if
  already fixed.
- **# Summary:** plain-language description of the bug, the root cause, *and* the fix direction, in a
  few sentences. A reader should understand the whole thing from this alone.
- **# Validation:** the `## Rubric` checkboxes you confirmed, then a `## Report` paragraph describing how
  you validated (dynamic PoC output, or why you used code review), with environment caveats. Include
  `## Negative evidence / false-positive checks` and `## Revalidation after fix`. Link to
  `.security/validation/SEC-NNN/`.
- **# Evidence:** the minimal code excerpts (`path (Lstart to Lend)`) with a one-line note above each
  explaining what it shows. Keep excerpts short — enough to prove the point, not whole files. Reference
  the supporting `.security/tool-results/<tool>` entry where a tool corroborated it. Redact any secret.
- **Proposed patch:** a unified `diff` that fixes the root cause minimally. Keep the patch embedded in
  the finding; do not create a separate patch artifact. Propose only — never apply during the scan.
- **# Attack-path analysis:** `Final | Decider | Matrix severity | Policy adjusted`, then `## Rationale`,
  `## Likelihood`, `## Impact`, `## Assumptions`, `## Path` (one-line arrow chain), `## Path evidence`
  (`path:line` per hop), `## Narrative`, `## Controls` (what's missing), `## Patch regression risk`,
  `## Blindspots` (what you couldn't fully verify). This block is what lets a reviewer trust the severity.

## Finding numbering and lifecycle

Assign finding IDs chronologically. For every scan, including the first one, inspect both
`.security/findings/` and `.security/fixed/`, find the highest existing `SEC-NNN`, and assign new
findings starting at the next unused ID. Do not reuse IDs from fixed findings, and do not renumber old
findings when severity changes. Severity belongs in the finding metadata and the severity-sorted summary
table, not in the ID sequence.

When a finding is remediated, move its file from `.security/findings/` to `.security/fixed/` and update
its metadata with `Resolution: fixed`, the fix commit/date if known, and any follow-up validation notes.
Leave the original filename/ID intact so historical reports, validation artifacts, and attack chains
remain traceable.

Commit-history review can create fixed historical reports directly: if an old commit introduced a bug
that a later commit already fixed, write the standard finding to `.security/fixed/` with `Commit:
<introducing sha>`, `Fixed in commit: <fix sha>`, and `Resolution: fixed`. If the same issue already
exists in `.security/findings/` or `.security/fixed/`, enrich the existing report with the commit evidence
instead of creating a duplicate.

Do not use alternate metadata keys for historical reports. Fixed reports must still use the same header,
`# Metadata`, `Criticality`, `Commit`, `Fixed in commit`, `Category`, `Detected by`, and `Resolution`
fields as open findings. `Commit` is the introducing commit in commit-history mode; never put the review
HEAD or `.security` artifact commit there when the actual introducing commit is known. Extra narrative
about introduction/fix series belongs in `# Summary`, `# Evidence`, or validation text, not in replacement
keys such as `Introduced:` / `Fixed:`.

Candidate promotion is intentionally broader than final reporting. If a worker reports a broken security,
billing, resource, or lifecycle invariant, validate and rank it instead of silently dismissing it because
it is "only" low or informational. Dismiss only with concrete evidence that the invariant still holds in
the child commit and current/future state.

## Tool-derived findings

Raw scanner output is evidence, not a report. Store it under `.security/tool-results/`, then triage the
hits against the actual code. Any actionable tool-derived issue that survives code/dataflow confirmation
and validation becomes a standard `.security/findings/SEC-NNN-<slug>.md` file using the normal per-finding
format above. Set `Detected by` to the tool name (for example `semgrep`, `trivy`, or `gitleaks`) and link
the raw output path in `# Evidence` or `# Validation`.

Do not write Markdown summaries under `.security/tool-results/`. Dismissed tool hits belong in
`.security/report.md` under "Considered and dismissed" when they are relevant to coverage; otherwise the
raw scanner output and `scan_manifest.md` are enough.

---

## Summary report format

`.security/report.md`:

```
# Security scan summary — <repo> @ <commit/diff> — <date>

## Executive summary
<overall risk posture and the top one or two issues, in plain language>

## Scope
<commit, branch, paths reviewed, deployment assumptions; link to .security/threat_model.md>

## Findings
| ID | Severity | Status | Title | Location | Finding |
|----|----------|--------|-------|----------|---------|
| SEC-001 | critical | validated | ... | path:line | findings/SEC-001-...md |
| SEC-002 | high | likely | ... | path:line | findings/SEC-002-...md |
...
(sorted critical → low)

## Attack chains
- **Chain A (critical):** SEC-003 → SEC-005 → SEC-001 — <one-line story, entry trust → terminal impact>
...

## Dependency / CVE summary
- <only actionable known-vuln deps, with reachability notes>

## Standards / framework coverage
- <ASVS/API/CWE/NIST/SLSA/Scorecard mappings used, and notable unmapped areas>

## Supply-chain evidence dossier
- <SBOM/provenance/attestation/signing/Scorecard-style checks/KEV/VEX status, with output paths>

## Secrets summary
- <redacted, location + type only — no values>

## Considered and dismissed (false positives)
- <candidate> — why it's not exploitable.

## Fixed findings
- <SEC-NNN> — <title>, fixed in <commit/date if known>. Link to fixed/SEC-NNN-...md.

## Commit history review
- Cursor: <latest reviewed commit, or none>
- Range reviewed: <oldest>..<newest>; <n> reviewed, <n> skipped as non-functional.
- New findings from commits: <ids>. Enriched existing findings: <ids>. Fixed historical findings: <ids>.

## Coverage
- Scanned: <surfaces / dirs / diff>. Languages: <...>. See scan_manifest.md for tools + commands.
- Manual review covered: <security-sensitive areas inspected>.
- DFD/source-sink coverage: <flows, sources, sinks, sanitizers/guards, business invariants reviewed>.
- Cloud/IaC identity paths: <workload/service account/OIDC -> cloud role -> API actions -> assets reviewed>.
- Not scanned / out of scope: <...>.

## Recommended next actions
1. <ordered remediation + follow-up validation>

## Blindspots
- <env gaps, tools that couldn't run, paths not dynamically validated>
```

If there are no findings, say so clearly and still include coverage, skipped tools, and blindspots.

## Scan manifest format

`.security/scan_manifest.md` makes coverage auditable (its own artifact so the report stays readable):

```
# Scan manifest — <repo> @ <commit> (<branch>, <clean|dirty>) — <date>

## Tools run
| Tool | Version | Command | Exit | Output | Class |
|------|---------|---------|------|--------|-------|
| semgrep | 1.x | semgrep scan --config ... | 0 | tool-results/semgrep.sarif | static |
| osv-scanner | 1.x | osv-scanner scan -r . | 1(findings) | tool-results/osv.json | static |
...
(non-zero exit caused by findings is normal — record it, don't treat it as scan failure)

## Tools skipped
- <tool> — <missing binary | unsupported ecosystem | no network | too risky | timeout | no manifest>

## Coverage statement
- Languages / package managers: <...>
- IaC / container / CI files: <...>
- Auth & secret surfaces, public entry points reviewed: <...>
- DFD/source-sink inventory reviewed: <flows/sources/sinks/guards, custom scanner modeling gaps>.
- Business invariants reviewed: <tenant isolation, billing/resource accounting, quotas, workflow state,
  idempotency, lifecycle cleanup>.
- Supply-chain evidence dossier: <SBOM/provenance/attestation/signing/Scorecard-style checks/KEV/VEX>.
- Cloud/IaC identity paths: <workload identities, OIDC principals, roles, effective permissions, assets>.
- Commit history review: <range, count reviewed/skipped, latest cursor, progress file path>.
- Any project-code-executing commands run (and why): <... or "none">
```


Keep the chat reply short: counts by severity, the top one or two chains in plain words, the highest-
leverage fix, and a pointer to `.security/`. Don't paste tool logs or full findings into chat.
