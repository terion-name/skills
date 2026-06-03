# Incremental commit history review

Run this after the current-HEAD sweep. It borrows the Codex Security pattern of reviewing commits
incrementally so newly introduced issues are caught close to their origin and historical findings retain
their introduction/fix evidence.

## Cursor and commit range

Use `.security/latest_reviewed_commit` as the durable cursor. It contains one commit SHA: the latest
commit whose diff has been assessed, including skipped non-functional commits.

- If the cursor exists and is non-empty, review commits after it through `HEAD`.
- If the cursor is absent or empty, review commits from the last 2 months, capped at 1000 commits.
- Always process commits from oldest to newest.

Useful commands:

```bash
# First run: last 2 months, cap 1000, oldest first.
git log --since="2 months ago" --format=%H --reverse | tail -n 1000

# Later runs: after cursor, oldest first.
git rev-list --reverse <latest-reviewed-sha>..HEAD
```

Before starting, write `.security/commit_review_progress.md` with the range, total count, current batch,
completed/skipped counts, and latest cursor. Update it after each commit or subagent batch so a resumed
agent can continue without relying on conversation context.

## Commit triage

For each commit, inspect metadata and changed paths first (`git show --stat --name-status --format=fuller
<sha>` plus the diff summary). Skip obviously non-functional commits, but still advance the cursor and
record the skip reason in `commit_review_progress.md` and `scan_manifest.md`.

Usually skip:

- docs-only changes (`README`, docs, comments with no generated/runtime effect)
- formatting-only changes with no semantic diff
- purely visual styling copy/CSS changes when they do not affect auth, data flow, templating, CSP,
  generated assets, dependency/runtime config, or privileged UI actions
- test-only changes that cannot affect release artifacts or security controls

Do not skip:

- dependency, lockfile, build, CI, Docker, IaC, release/signing, or installer changes
- auth, authorization, session, crypto, parsing, serialization, template, file/network I/O, subprocess,
  privilege, data migration, permissions, logging/redaction, or secret-handling changes
- "refactors" that move checks, defaults, path construction, deserialization, input validation, or trust
  boundaries

## Subagent strategy

Actively use subagents. The orchestrator owns the queue, cursor, final validation, severity, dedupe, and
artifact writes; commit-review subagents own per-commit investigation.

Batch independent commits when possible (for example 5-20 commits per wave, adjusted for diff size), but
keep each subagent scoped to one commit unless a run of tiny related commits is safer as a small batch.
Use `run_in_background: true`, then await the batch. After every completed commit, update
`.security/latest_reviewed_commit` to that SHA and update `.security/commit_review_progress.md`.

Commit subagent prompt shape:

```text
Task: Security/functional regression review for commit <sha>.
Scope: Review only this commit's changes, then trace directly affected logic in the current repository.
Threat-model context: <relevant boundaries/assets from .security/threat_model.md>.
Do:
1. Inspect the commit metadata, changed files, and diff.
2. Decide whether the commit is obviously non-functional. If yes, report SKIP with a concise reason.
3. If functional, trace affected call paths, trust boundaries, data/control flow, defaults/config, and
   downstream consumers touched by the diff.
4. Look for security bugs and serious functional regressions introduced by this commit using the same
   policy/reporting methodology as the main security review.
5. If you suspect a bug, identify source -> sink or broken invariant, affected paths, introduction
   evidence from the commit diff, and whether later code appears to fix it.
Report back:
- status: skip | reviewed-no-finding | candidate
- commit, subject, author date
- files inspected and related logic traced
- skip reason or candidate finding(s)
- possible fixed-in commit, if apparent
Constraints: read-only review; do not patch; do not assign final severity.
```

## Reconciliation and artifacts

For every candidate, validate with the same validation/severity/chaining rules as the current-HEAD scan.
Then reconcile against existing `.security/findings/` and `.security/fixed/` before writing:

- If the issue is still present and not already reported, write a normal finding in `.security/findings/`.
  Include `Commit: <introducing sha>` in metadata.
- If the issue was introduced by an old commit but fixed by a later commit, still write the finding for
  history, but place it in `.security/fixed/`. Include both `Commit: <introducing sha>` and
  `Fixed in commit: <fix sha>` in metadata, plus validation notes explaining how the later fix was found.
- If the same unresolved issue already exists in `.security/findings/`, do not create a duplicate.
  Enrich the existing finding with the introducing commit, additional evidence, affected commit references,
  and any validation details.
- If the same fixed issue already exists in `.security/fixed/`, enrich that report rather than creating
  a duplicate.

When a commit-review candidate is dismissed, record the reason in the summary report's "Considered and
dismissed" section only if it is useful coverage context; otherwise keep it in the progress/manifest.
