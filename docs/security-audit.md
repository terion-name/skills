# What this skill is, and why it exists

## The problem

Security review has a failure mode that looks a lot like bad AI code review: the output is plausible, voluminous, and only partly useful. A scanner finds a hundred things. Some are real. Some are development-only. Some are unreachable. Some matter only if three unrelated assumptions are true. The human still has to do the hard work: decide what the system protects, trace attacker-controlled input, validate the path, and explain which fixes actually reduce risk.

AI agents make this worse when they treat security as a checklist. They know the vocabulary: XSS, SSRF, SQL injection, secrets, CVEs, deserialization, IAM, container escape. Left unguided, they can produce a report that sounds like a security audit but has no threat model, no reachability analysis, no proof, and no clear next move.

The `security-audit` skill exists to force a better shape:

**Threat model first.** Before looking for bugs, the agent has to identify assets, trust boundaries, entry points, privileged sinks, assumptions, and what "critical" means for this repository.

**Tools plus semantic review.** Deterministic scanners are valuable, but incomplete. LLM review is flexible, but fallible. The skill uses both: scanners for breadth, policy-guided code review for the bugs scanners miss, and validation to keep both honest.

**Validation before severity.** A dependency CVE is not automatically high. A dangerous API call is not automatically exploitable. A finding becomes serious when attacker-controlled input crosses a real boundary and reaches a meaningful sink.

**Durable artifacts.** The output is not just chat. The scan writes `.security/threat_model.md`, `.security/report.md`, `.security/scan_manifest.md`, one file per finding, scanner output, validation notes, and suggested patches. Later scans can reuse that context instead of starting from zero.

## The philosophy

The skill is defender-first and repository-grounded. It is written for code the user owns or is authorized to audit. It does not attack external systems, does not exfiltrate secrets, and does not turn proof-of-concepts into weaponized tooling.

It is also intentionally skeptical of scanner theater. A good security report is not a leaderboard of tool output. It is a short list of credible ways the system can be harmed, tied to the code paths and deployment assumptions that make those harms possible.

Core positions:

**A threat model is the index.** Without a threat model, every issue competes on generic severity labels. With one, the scan knows which boundaries matter: internet to app, user to tenant, tenant to admin, container to host, CI input to release artifact, package registry to install script, untrusted file to parser.

**Reachability is the difference between signal and noise.** The skill asks: can an attacker actually control the input, can they reach this code path in the supported deployment, and do existing controls block the path?

**Validation is part of the work, not a nice extra.** Where safe, findings should be reproduced in a sandbox. Where reproduction is not practical, the report should say why and give strong static evidence instead. The statuses are deliberately blunt: `validated`, `likely`, `unvalidated`, or `false_positive`.

**Severity is local.** The same bug can be low in one repository and critical in another. An arbitrary file write in a root-run container entrypoint is different from an operator-only dev script. The threat model supplies the calibration.

**Security scanning must not become the attack.** The skill treats the repository as untrusted. Static reads and analyzers are preferred. Commands that execute project code are documented and isolated, because installing dependencies, running tests, or building Docker images can itself trigger malicious lifecycle scripts.

## The approach

The audit follows seven stages.

**Threat model.** Create or refresh `.security/threat_model.md`: overview, assets, trust boundaries, entry points, privileged operations, security controls, assumptions, attack-surface map, criticality calibration, and review priorities.

**Scope.** Decide whether the scan is a full audit, a PR/diff review, or a targeted component review. Partition the work by attack surface, service, language, or top-level directory.

**Scan.** Run deterministic tooling where relevant: SAST, dependency/CVE scanners, secret scanners, IaC and container scanners, and language-specific analyzers. In parallel, review the code against the policy references for web/API bugs, language-specific hazards, memory safety, infrastructure, secrets, and supply chain.

**Validate.** Reproduce candidate findings in the sandbox when safe, or validate them by targeted code review when dynamic proof would be destructive, unavailable, or misleading. Drop false positives instead of dressing them up.

**Severity and chaining.** Rate likelihood and impact under the repository threat model. Then look across findings for kill chains: a medium auth bypass plus a medium object access bug plus a dangerous sink may be a high or critical attack path together.

**Report.** Write one file per finding, a scan manifest, and a summary report. Findings include evidence, validation, impact, likelihood, remediation, false-positive checks, and optionally a suggested patch. The skill proposes patches but does not apply them unless the user asks for remediation afterward.

**Commit history.** After the current-HEAD sweep, continue into the incremental per-commit pass unless the user explicitly scoped it out. Review the first-run two-month/1000-commit window, then advance the durable cursor after each commit is assessed or skipped.

## What good output looks like

A good finding says, in plain terms, who the attacker is, what input they control, what boundary they cross, what code path they hit, what asset or sink is affected, and what evidence supports the claim.

It is specific about uncertainty. If a tool was missing, a build was too risky to run, a dependency was not reachable in the observed code path, or validation was static only, the report says so.

It keeps secrets redacted. Full credentials, tokens, cookies, private keys, and connection strings never belong in chat or artifacts. The report should give enough fingerprinting context to rotate and remove the secret, not enough to misuse it.

It produces files a future agent can use. The next scan should be faster and sharper because `.security/threat_model.md` and `.security/scan_manifest.md` already explain the system and the prior coverage.

## What this skill cannot do

It cannot prove a system is secure. It can only improve the odds that realistic issues are found, validated, prioritized, and explained.

It also cannot replace environment knowledge. Deployment topology, cloud IAM, production flags, tenant model, release permissions, and secret-management reality often live outside the repository. The skill records those assumptions and blind spots instead of pretending they do not matter.

The useful standard is narrower: fewer scanner-only false positives, fewer missed trust-boundary bugs, clearer remediation, and a report that a developer can act on without needing to reverse-engineer the audit.

## Reference map

- [`skills/security-audit/SKILL.md`](../skills/security-audit/SKILL.md) — the main workflow and trigger description.
- [`references/threat-model.md`](../skills/security-audit/references/threat-model.md) — how to build and refresh the repository threat model.
- [`references/tooling.md`](../skills/security-audit/references/tooling.md) — scanner choices, commands, ecosystem notes, and offline fallbacks.
- [`references/reporting.md`](../skills/security-audit/references/reporting.md) — validation, severity, exploit chaining, and report format.
- [`references/policies/`](../skills/security-audit/references/policies/) — web/API, language, infrastructure, secrets, supply-chain, and memory-safety review policies.
- [`assets/`](../skills/security-audit/assets/) — templates and worked examples for threat models and findings.
- [`scripts/init_security.sh`](../skills/security-audit/scripts/init_security.sh) — helper to scaffold `.security/`.
