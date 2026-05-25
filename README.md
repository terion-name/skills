# Skills

My collection of crafted skills.

## Install

Skills are published at https://skills.sh

```bash
npx skills add terion-name/skills
```

Or install a single skill:

```bash
npx skills add terion-name/skills/writing-good-code
```

## Skills

### Code quality

A skillset for guiding AI coding agents to write and maintain code that is **simple, readable, and correct** — biased against over-engineering, pattern cargo-culting, and the wrong abstractions that calcify over time. Based on professional literature and articles.

#### Philosophy

Modern, practical, non-religious. Avoids the dogmatic mid-2000s Clean Code style (3-line methods, polymorphism-over-conditionals-always, `IFoo`-per-`Foo`) that reads well in books and produces unmaintainable codebases.

Core ideas:

- **Complexity = obscurity + dependencies** (Ousterhout).
- **Modules hide secrets, not steps** (Parnas).
- **Simple is not-complected; easy is near-at-hand** (Hickey).
- **Duplication is far cheaper than the wrong abstraction** (Metz).
- **Cognitive load is the real budget**; agents must use mechanical proxies for the human "feel" they lack (Zakirullin).
- **Beauty is a correctness heuristic** (DHH, Alexander).

Influences: Ousterhout, Beck (*Tidy First?*), Parnas, Hickey, Fowler, Metz, North (CUPID), Carmack/Muratori on over-abstraction, Alexis King ("Parse, don't validate"), Carson Gross (Locality of Behavior), Gall, Conway, Hyrum, Chesterton, Spolsky (leaky abstractions), Thomson (Postel critique), the Go Proverbs, Rob Pike, DHH, the Grug Brained Developer.

For further details see [docs page](docs/code-quality.md)

| Skill | Description |
|---|---|
| [`writing-good-code`](skills/writing-good-code/) | Greenfield authoring — naming, module shape, depth, errors, language idioms |
| [`refactoring-and-reviewing-code`](skills/refactoring-and-reviewing-code/) | Improving existing code without changing behavior — smells, tidyings, safe sequences |
| [`abstraction-quality`](skills/abstraction-quality/) | Decision procedure for when to extract an abstraction and when to duplicate instead |

The three code-quality skills interlink: `writing-good-code` and `refactoring-and-reviewing-code` both reference `abstraction-quality` for the extract-vs-duplicate question.

### Security

A defender-first skillset for repository security review: threat model first, tool-assisted scan second, validation before severity, and durable artifacts under `.security/`. It is modeled after the Codex/Aardvark style of scanning: combine deterministic tools with semantic review, then prove or discard findings instead of shipping scanner noise.

#### Philosophy

Security review should be adversarial without becoming theatrical. The goal is not to produce the longest list of possible weaknesses; the goal is to identify realistic attack paths through the system the user actually runs.

Core ideas:

- **Threat model before checklist**; assets, trust boundaries, and reachable entry points decide what matters.
- **Scanner output is evidence, not a finding**; every serious issue needs code-path validation.
- **Severity follows exploitability**; reachability and impact beat generic CVSS labels.
- **Proof stays local and safe**; no external attacks, no secret disclosure, no destructive testing.
- **Reports are working artifacts**; `.security/` should help the next scan and the remediation pass.

For further details see [docs page](docs/security-scan.md)

| Skill | Description |
|---|---|
| [`security-scan`](skills/security-scan/) | Threat-model-driven security scanning, validation, exploit chaining, and `.security/` reporting |

### API architecture

| Skill | Description |
|---|---|
| [`orpc-contract-first`](skills/orpc-contract-first/) | oRPC contract-first API design for TypeScript monorepos with contracts in a shared package |

## Coder Mux agents

Agent definitions for [Coder Mux](https://github.com/coder/mux) live under [`agents/`](agents/) in this repo. They are Markdown persona files with YAML frontmatter. Unlike `AGENTS.md`, this is a Mux-specific format, not a broadly standardized repository instruction format.

For further details see [docs page](docs/agents.md)

| Agent | Description |
|---|---|
| [`Orchestrator`](agents/orchestrator.md) | Coordinates delegated implementation, integrates child patches, and keeps the parent workspace focused. It was in mux untill it was [removed](https://github.com/coder/mux/pull/3224) from basic set, alternative provided by [@ibetitsmike](https://github.com/ibetitsmike). |
| [`Security Officer`](agents/security_officer.md) | Runs threat-model-driven security reviews and writes `.security/` scan artifacts |

## Adding skills manually

The `SKILL.md` files are plain Markdown and work in any harness. Two patterns:

**A) Native skills format** — the harness loads the folder directly.

**B) Paste into instructions** — strip the YAML frontmatter, paste the body into the harness's instruction file. Works everywhere.

---

### Claude Code

Drop the skill folder into your project or user skills directory:

```bash
# project-level
cp -r skills/writing-good-code .claude/skills/

# user-level (all projects)
cp -r skills/writing-good-code ~/.claude/skills/
```

### Claude.ai

Upload each skill folder via the Skills UI, or use `npx skills add terion-name/skills`.

### OpenAI Codex CLI

Add to `AGENTS.md` in the repo root (project-level) or `~/.codex/instructions.md` (user-level).

For Coder Mux, copy or symlink the files in `agents/` into `.mux/agents/` for project-level agents or `~/.mux/agents/` for global agents. The `Security Officer` agent composes with the `security-scan` skill: the agent supplies the runnable persona and guardrails, while the skill supplies the methodology, policy references, tooling guidance, and report formats.

### Gemini CLI

Add skill bodies to `GEMINI.md` in the repo root, or to `~/.gemini/GEMINI.md` for user-level.

### Cursor

Create a rule file for each skill under `.cursor/rules/`:

```bash
# strip frontmatter and write to a .mdc rule file
awk 'BEGIN{f=0} /^---/{f++; next} f>=2{print}' skills/writing-good-code/SKILL.md \
  > .cursor/rules/writing-good-code.mdc
```

Or paste the body manually into `.cursorrules`.

### Windsurf

Append the skill body to `.windsurfrules` at the project root:

```bash
awk 'BEGIN{f=0} /^---/{f++; next} f>=2{print}' skills/writing-good-code/SKILL.md \
  >> .windsurfrules
```

### Cline / Roo

Paste the skill body into `.clinerules` at the project root, or add it via the Cline system prompt UI.

### GitHub Copilot

Append skill bodies to `.github/copilot-instructions.md`:

```bash
awk 'BEGIN{f=0} /^---/{f++; next} f>=2{print}' skills/writing-good-code/SKILL.md \
  >> .github/copilot-instructions.md
```



### Aider

Pass skill files with `--read` at startup:

```bash
aider --read skills/writing-good-code/SKILL.md
```

Or add to `.aider.conf.yml`:

```yaml
read:
  - skills/writing-good-code/SKILL.md
```

### Continue (VS Code / JetBrains)

Add skill files as context via `.continue/config.json` using the `file` context provider, or paste the body into a custom system prompt in the Continue settings.

## Structure

```
skills/
├── <skill-name>/
│   ├── SKILL.md          # agent instructions + trigger description (YAML frontmatter)
│   ├── references/       # supporting docs the agent can pull on demand
│   ├── assets/           # optional templates and worked examples
│   └── scripts/          # optional helper scripts
agents/
├── <agent-name>.md       # Coder Mux agent definition source
└── ...
```

Each `SKILL.md` has a YAML frontmatter block with `name` and `description` fields. The `description` controls when the agent decides the skill is relevant.

Agent files also use YAML frontmatter. They are not required to use the skills, and the format is currently specific to Coder Mux rather than the general `AGENTS.md` convention.

## License

MIT
