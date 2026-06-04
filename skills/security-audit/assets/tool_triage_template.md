# Tool result triage — <repo> @ <commit> — <date>

## Raw outputs

| Output | Tool | Status | Decision | Notes |
|--------|------|--------|----------|-------|
| tool-results/<file> | <tool> | parsed\|failed\|partial | findings:<ids>\|dismissed:<n>\|blocked:<reason> | <short note> |

## Dependency advisories

| Advisory | Package | Version | Fixed version | Scope | Tool(s) | Reachability evidence | Decision |
|----------|---------|---------|---------------|-------|---------|-----------------------|----------|
| CVE-YYYY-NNNN | <package> | <version> | <version/unknown> | runtime\|dev\|test\|build | <tools> | <imports/callers/package/deployment evidence> | finding:SEC-NNN\|candidate\|dismissed:<reason>\|blocked:<reason> |

## Other tool hits

| Tool | Rule/id | Location | Decision | Reason |
|------|---------|----------|----------|--------|
| <tool> | <rule/advisory> | <path:line> | finding:SEC-NNN\|candidate\|dismissed:<reason>\|blocked:<reason> | <evidence-backed reason> |

## Blockers

- <tool/output/advisory> — <what blocked validation and what is needed next>
