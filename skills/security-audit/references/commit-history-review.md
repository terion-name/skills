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
agent can continue without relying on conversation context. Record enough detail that a reviewer can see
whether a commit was truly investigated or merely skimmed: commit SHA, subject, changed paths, decision,
invariants checked, related symbols/callers traced, candidate count, and cursor after the decision.

## Commit triage

For each commit, inspect metadata and changed paths first (`git show --stat --name-status --format=fuller
<sha>` plus the diff summary). Skip obviously non-functional commits, but still advance the cursor and
record the skip reason in `commit_review_progress.md` and `scan_manifest.md`.

Do not classify a commit as non-functional just because it is small, labeled "refactor", or mostly
configuration. Many historical security findings are one-line regressions in defaults, compose files,
billing catalogs, allowlists, schemas, or error handling. When in doubt, review the commit.

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

## Depth requirements

Commit review is **diff-to-invariant** review, not a broad surface sweep. Current-HEAD scanning finds
obvious standing bugs; the commit flow catches regressions by asking what security, billing, lifecycle,
or reliability invariant changed at this exact commit.

For every functional commit, the subagent must inspect the parent and child state, not only current
`HEAD`:

```bash
git show --find-renames --find-copies --stat --name-status --format=fuller <sha>
git show --find-renames --find-copies --word-diff=plain --unified=80 <sha>
git show <sha>^:<path>    # when comparing old behavior is useful
git show <sha>:<path>
git log --reverse --ancestry-path <sha>..HEAD -- <path>   # likely later fixes touching same path
```

If the diff changes a symbol, route, schema, config variable, migration, workflow, or exported type,
trace directly affected logic:

- callers and downstream consumers (`rg` the symbol, route, env var, table/column, config key, message
  type, queue topic, metric label, or Docker service name)
- entry points that can control the changed value, including API tokens, user/org/project scoping,
  admin UI actions, webhooks, CI inputs, compose env, and database rows
- guards that should still hold after the diff: authz/tenant ownership, entitlement, credit/wallet
  admission, pricing/accounting, redaction, TLS/host allowlists, SSRF blocklists, CSRF, idempotency,
  race/lease cleanup, lifecycle billing, and resource limits
- failure behavior: fail-open vs. fail-closed, retry/drop semantics, unbounded parsing/body buffering,
  cleanup on abort/timeout, and whether a partial failure can leak, undercharge, or orphan resources

`reviewed-no-finding` is only acceptable after the subagent reports which of those probes applied and
why each held. A terse "no issue found" is insufficient and should be sent back for another pass.

## Commit probe checklist

Use these probes as a minimum checklist. Select the relevant ones per diff; do not require all probes for
every commit.

- **Auth / tenant isolation:** Did the diff add or move an object lookup, session lookup, token mapping,
  project/org field, admin route, or MCP/session transport? Verify the caller's org/project/token identity
  is checked at every lookup and return path, including delete/summary/error paths.
- **Billing / credits / entitlements:** Did the diff touch pricing catalogs, resource tiers, usage events,
  wallet/credit checks, provider mappings, request/session attribution, or billing workers? Verify every
  admitted resource has a matching price and entitlement, every usage path debits or records spend, and
  failures cannot silently drop or poison billing events.
- **Proxy / network / SSRF:** Did the diff touch egress, outgress, proxy providers, DNS, compose ports,
  callbacks, redirects, or host allow/block lists? Verify attacker-controlled upstream hosts and resolved
  destinations both pass blocklists, internal ports remain private, and headers cannot select sessions or
  bypass accounting.
- **Secrets / TLS / logging:** Did the diff add env defaults, client URLs, API keys, storage summaries,
  checkpoint/resume files, logs, audit records, or redaction code? Verify secrets are not returned,
  persisted broadly, logged, sent to public clients, or transmitted with TLS verification disabled.
- **Runner lifecycle / concurrency:** Did the diff touch warm pools, runner readiness, abort/timeout paths,
  leases, heartbeats, cleanup, checkpoint restore, or queue/event processing? Verify aborts and failures
  cannot orphan containers/sessions, skip billing, amplify work, or leak cross-tenant state.
- **Infra / CI / release:** Did the diff touch Dockerfiles, compose generation, IaC, workflows, installers,
  lockfiles, or published bundles? Verify exposed ports, token permissions, mutable dependencies,
  build-context secrets, generated artifacts, and public bundles are still safe.
- **Admin / browser UI routes:** Did the diff add server routes or privileged UI actions? Verify mutating
  actions are POST/CSRF-protected, SSR does not drop auth cookies, external links use safe schemes/opener
  policy, and public bundles do not expose internal identifiers or secrets.

Keep medium, low, and informational candidates. Do not suppress a security-adjacent regression merely
because it is not a clean exploit primitive yet; the orchestrator can later rank it, mark it
informational, or dismiss it with rationale.

## Mandatory candidate promotion gates

The subagent must return `candidate` if a functional commit introduces any of these conditions, unless it
proves with parent/child code evidence that the condition is unreachable or fully mitigated in the same
commit. Do not bury these in `reviewed-no-finding` notes.

- **Fail-open control:** a guard, admission check, entitlement check, allowlist, CSRF check, TLS check,
  wallet check, budget check, redaction, blocklist, cleanup, or lifecycle publisher becomes a no-op,
  optional, disabled by default, temporarily bypassed, deferred to a non-equivalent later guard, or catches
  an error and continues.
- **Public response/data-shape expansion:** a public or tenant-accessible route starts returning fields
  derived from cookies, browser storage, raw backend state, provider metadata, internal ids, session
  fingerprints, wallet/provider identifiers, logs, or error summaries. Treat delete/terminal/summary/error
  paths as public return paths too.
- **Billing/resource-accounting drift:** an admitted resource has no exact price, a usage event can throw
  before spend/wallet debit, a queue publish can fail after the billable action succeeds, a worker can drop
  or poison billing events, a minimum duration rounds to zero, or a repair/provisioning action runs from a
  GET/CSRF-prone route.
- **Entitlement/routing dimension mismatch:** enforcement checks only a coarse class while routing/billing
  uses finer dimensions such as provider, proxy type, tier, region, resource tier, request/session mode, or
  attribution type. Exact dimensional mismatches are candidates even if a nearby entitlement check exists.
- **Config-combination exposure:** a commit combines any secret/API key/header forwarding with an external
  default URL, `NODE_TLS_REJECT_UNAUTHORIZED=0`, insecure TLS settings, oauth/identity header trust, or
  unauthenticated host-port exposure. The risk can come from the combination, even if each line existed
  separately before.
- **Network/egress boundary split:** validation and use happen in separate steps, for example DNS is checked
  before a later dial, proxy endpoints are not checked with the same destination policy as normal traffic,
  origin headers can select sessions/routes, or compose exposes internal controller/proxy/runner services.
- **Runner/checkpoint/isolation regression:** runners share network identity unexpectedly, receive broader
  internal secrets than needed, write resume/checkpoint files containing secrets or tenant state, become
  claimable before handlers/watchdogs are armed, or cleanup/abort/timeout paths can leave live resources.
- **Release/public-bundle drift:** CI token permissions widen, deploy credentials become available to PR
  contexts, public bundles expose internal pricing/provider identifiers, dev servers expose source, or
  Docker/build contexts include files intentionally ignored by the runtime repo.

Red-flag phrases in a `reviewed-no-finding` note are a quality failure unless accompanied by a concrete
dismissal proof: `fail open`, `no-op`, `temporarily`, `disabled`, `bypass`, `not enforced`, `no guard`,
`no price`, `throws before billing`, `dropped`, `poison`, `unbounded`, `raw state`, `internal id`,
`provider id`, `secret`, `logs`, `TLS disabled`, `NODE_TLS_REJECT_UNAUTHORIZED`, `forwarded token`, `host
port`, `public dev`, `GET route`, `CSRF`, `separate DNS`, `shared netns`, `claimable before`, `orphan`.
If one appears, rerun the commit review or promote a candidate for orchestrator validation.

Do not dedupe by broad theme. Two issues are distinct if they have different introducing commits,
different broken invariants, different attacker actions, different affected services, or different fixes.
For example, "proxy entitlement bypass" and "proxy billing price mismatch" may share files but deserve
separate candidates when one admits unauthorized traffic and the other undercharges admitted traffic.

## Subagent strategy

Actively use subagents. The orchestrator owns the queue, cursor, final validation, severity, dedupe, and
artifact writes; commit-review subagents own per-commit investigation.

Parallelize by running many one-commit subagents concurrently, not by giving one subagent a large queue
to skim. Keep each subagent scoped to one commit. Only batch commits together when they are consecutive,
tiny, and form a single logical change; the batch result must still include a separate decision and probe
checklist for each commit. Use `run_in_background: true`, then await the wave. After every completed
commit, update `.security/latest_reviewed_commit` to that SHA and update `.security/commit_review_progress.md`.

Commit subagent prompt shape:

```text
Task: Security/functional regression review for commit <sha>.
Scope: Review this commit's parent->child diff deeply, then trace directly affected logic through later
commits and current HEAD.
Threat-model context: <relevant boundaries/assets from .security/threat_model.md>.
Do:
1. Inspect commit metadata, changed files, parent/child diff, and the child versions of changed files.
2. Decide whether the commit is obviously non-functional. If yes, report SKIP with a concise reason.
3. If functional, identify changed symbols/routes/schemas/config/env/db/workflows and `rg` their callers,
   downstream consumers, and current/future touches through HEAD.
4. Run the relevant commit probes from the checklist: auth/tenant isolation, billing/credits,
   proxy/network/SSRF, secrets/TLS/logging, runner lifecycle/concurrency, infra/CI/release, admin/browser UI.
5. Apply the mandatory candidate promotion gates. If any gate matches, report `candidate` unless the
   same commit contains a concrete mitigating check and you cite it.
6. Look for security bugs, serious functional regressions, and security-adjacent informational issues
   introduced by this commit using the same policy/reporting methodology as the main security review.
7. If you suspect a bug, identify source -> sink or broken invariant, affected paths, introduction
   evidence from the commit diff, and whether later code appears to fix it.
Report back:
- status: skip | reviewed-no-finding | candidate
- commit, subject, author date
- files inspected, symbols/callers traced, and probe checklist results
- promotion-gate result: matched gates, or "none" with a one-line reason
- skip reason or candidate finding(s)
- possible fixed-in commit, if apparent
Constraints: read-only review; do not patch; do not assign final severity.
```

## Reconciliation and artifacts

For every candidate, validate with the same validation/severity/chaining rules as the current-HEAD scan.
Then reconcile against existing `.security/findings/` and `.security/fixed/` before writing. Historical
validation must distinguish three states: introduced and still present, introduced and later fixed, or
introduced but later changed into a different unresolved issue.

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

Use the standard finding template for both open and fixed reports. In commit-history findings, `Commit`
is always the introducing commit, not the review HEAD or `.security` artifact commit. Use `Fixed in
commit` for the later fix. Do not replace these with nonstandard metadata such as `Introduced:` or
`Fixed:`, because deterministic parsers and issue upload scripts depend on the standard fields.

When a commit-review candidate is dismissed, record the reason in the summary report's "Considered and
dismissed" section only if it is useful coverage context; otherwise keep it in the progress/manifest.

The orchestrator should periodically audit worker quality. Sample `reviewed-no-finding` commits from each
wave; if reports lack parent/child comparison, caller tracing, probe checklists, or future-fix checks,
pause cursor advancement for that wave and rerun those commits with a stricter prompt.

After each wave, run a targeted red-flag audit over `commit_review_progress.md` before advancing too far:

```bash
rg -n "reviewed-no-finding.*(fail open|no-op|temporar|disabled|bypass|not enforced|no guard|no price|throws before billing|dropped|poison|unbounded|raw state|internal id|provider id|secret|logs|TLS|NODE_TLS_REJECT_UNAUTHORIZED|forwarded token|host port|public dev|GET route|CSRF|separate DNS|shared netns|claimable before|orphan)" .security/commit_review_progress.md
```

Every hit must be re-reviewed, promoted to a candidate, or rewritten with concrete dismissal evidence.
Also intentionally sample high-risk `reviewed-no-finding` commits touching billing, proxy/egress, compose,
CI/workflows, checkpoint/resume, runner isolation, public bundles, and auth/session response shapes.
