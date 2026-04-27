# skills

A personal collection of reusable skills for AI coding agents — Claude Code, Cursor, Copilot, Codex, and others that follow the [Agent Skills](https://skills.sh) format.

## Install

```bash
npx skills add terion-name/skills
```

Or install a single skill:

```bash
npx skills add terion-name/skills/writing-good-code
```

## Skills

### Code quality

| Skill | Description |
|---|---|
| [`writing-good-code`](skills/writing-good-code/) | Greenfield authoring — naming, module shape, depth, errors, language idioms |
| [`refactoring-and-reviewing-code`](skills/refactoring-and-reviewing-code/) | Improving existing code without changing behavior — smells, tidyings, safe sequences |
| [`abstraction-quality`](skills/abstraction-quality/) | Decision procedure for when to extract an abstraction and when to duplicate instead |

The three code-quality skills interlink: `writing-good-code` and `refactoring-and-reviewing-code` both reference `abstraction-quality` for the extract-vs-duplicate question.

## Adding skills manually

Copy any skill folder into your project's `.claude/skills/` or your user-level `~/.claude/skills/`:

```bash
cp -r skills/writing-good-code ~/.claude/skills/
```

For other harnesses (Cursor, Cline, aider): the `SKILL.md` bodies are plain Markdown — paste or symlink them into your `CLAUDE.md` / `AGENTS.md`.

## Structure

```
skills/
├── <skill-name>/
│   ├── SKILL.md          # agent instructions + trigger description (YAML frontmatter)
│   └── references/       # supporting docs the agent can pull on demand
└── ...
```

Each `SKILL.md` has a YAML frontmatter block with `name` and `description` fields. The `description` controls when the agent decides the skill is relevant.

## License

MIT
