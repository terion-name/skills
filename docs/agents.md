# What these Coder Mux agents are, and why they exist

## The problem

Some agent work is too large for one context window and too risky to run as a single wandering process. Implementation tasks need investigation, coding, patch integration, verification, and sometimes follow-up fixes. Security review needs threat modeling, broad scanning, validation, and careful reporting. If one agent tries to hold all of that in its own context, it becomes easier for it to lose the thread, re-read the same files, or mix coordination work with implementation work.

The `agents/` directory contains [Coder Mux](https://github.com/coder/mux) agent definition source files. They are Markdown persona files with YAML frontmatter: Mux reads the frontmatter as metadata/tool policy and the Markdown body as the agent's system prompt.

This is not the same thing as `AGENTS.md`. `AGENTS.md` is the emerging cross-tool convention for repository instructions. Mux agent definitions are a Mux-specific format for defining selectable modes and runnable sub-agents.

They are not replacements for the skills. They are operational wrappers: they define who the worker is, which tools it can use, what it should not do, and what shape its final report must have.

## The philosophy

The agents are written around a division of labor.

**The parent coordinates.** It keeps the main workspace coherent, decides which tasks can run in parallel, applies child patches, and runs final verification.

**Children do bounded work.** A child agent gets a compact brief, a narrow scope, and a clear acceptance bar. It should finish the delegated job and report back, not expand into adjacent work.

**Patches move through explicit integration.** Child workspaces produce patches; the parent applies them deliberately. This keeps concurrent work from silently trampling the main workspace.

**Security artifacts are separate from remediation.** The `Security Officer` writes `.security/**` by default. Source-code fixes are a later, explicit task. That separation keeps audit evidence stable and prevents a scan from quietly becoming a feature branch.

## The agents

| Agent | Purpose |
|---|---|
| [`Orchestrator`](../agents/orchestrator.md) | Coordinates delegated implementation work, applies child patches, and verifies the result |
| [`Security Officer`](../agents/security_officer.md) | Performs repository-grounded security review and writes threat model, findings, tool output, validation notes, and summary report |

## Orchestrator

The `Orchestrator` agent is for multi-agent implementation. It is intentionally not a general coding worker. Its job is to translate an accepted plan into concrete subtasks, spawn the right child agents, await them, apply their patches, and verify the integrated result.

It favors parallelism when subtasks are independent and sequencing when one task produces files or behavior another task needs. It treats dependency analysis as part of coordination: outputs, inputs, prerequisites, and verification targets decide whether tasks can run together.

The important constraint is that the orchestrator stays out of direct implementation. It can use repository commands for coordination and verification, but broad code investigation and code edits belong to delegated workers. That keeps the parent context reserved for integration judgment.

## Security Officer

The `Security Officer` agent is a runnable security-review worker. It is designed to compose with the [`security-review`](../skills/security-review/) skill.

By default it:

- Builds or refreshes `.security/threat_model.md`.
- Runs available static, dependency, secret, infrastructure, and language-specific security tools.
- Performs manual, threat-model-driven review of sensitive surfaces.
- Validates findings where safe.
- Writes individual findings under `.security/findings/`.
- Writes scanner output, validation notes, suggested patches, a scan manifest, and a final report under `.security/`.

It does not apply source-code fixes by default. That is deliberate. A security review should produce stable evidence and prioritized remediation guidance first; implementation can follow as a separate task.

## How the agents compose with skills

Skills are portable methodology. Agents are runnable personas.

The `security-review` skill contains the deeper policy references, tooling guidance, templates, severity calibration, and exploit-chaining rules. The `Security Officer` agent contains the runtime behavior: guardrails, artifact locations, tool posture, and final `agent_report` expectations.

The same pattern can apply elsewhere. A skill can teach how to do the work; an agent can define how to delegate, isolate, report, and integrate that work in a Mux runtime.

## Manual use

Mux discovers project-level agent definitions from `.mux/agents/*.md` and global definitions from `~/.mux/agents/*.md`. Copy or symlink the files from this repo's `agents/` directory into one of those locations.

If another harness does not support Mux agent definitions directly, the prompt body can still be adapted manually, but the frontmatter schema and tool policy are not portable by default. The skills remain the most portable layer: each `SKILL.md` can be loaded natively where supported or pasted into the target agent instructions.
