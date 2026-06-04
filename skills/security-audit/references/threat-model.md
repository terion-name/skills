# Threat model

The threat model is the scan-time security context for the repo. It is what turns a flat vulnerability
checklist into a *prioritized* assessment: it records what is internet-reachable, who is trusted, what
the privileged operations are, and what "critical" means for this specific project. Every later stage
(scan partitioning, validation effort, severity) reads from it. Build it once, refresh it as the
architecture changes.

Persist it at `.security/threat_model.md`. The format below matches `assets/example_threat_model.md`.

## When to build vs. refresh

- **Missing** → build from scratch (this doc).
- **Exists** → read it, treat trust boundaries / assumptions / criticality calibration as authoritative,
  and refresh only stale parts or what the current diff clearly changes. Don't re-derive the whole thing.

## How to build it (delegate the mapping)

Do not read the whole repo yourself. Spawn `explore` sub-agents in parallel, one per concern, with
narrow prompts. A good default set:

1. **Entry points & exposure** — what listens on the network, what's behind auth, what's public vs.
   loopback, what ports/routes exist, what reverse proxy / ingress config does. Find the request path
   from "untrusted internet input" to code.
2. **AuthN/AuthZ & identity** — how users authenticate, where authorization is enforced, session/cookie
   handling, IdP/OIDC/SSO config, admin vs. user roles, group/claim mapping.
3. **Data-flow / source-sink map** — external entities, data stores, data flows, trust-boundary crossings,
   untrusted sources, dangerous sinks, context-specific sanitizers/guards, file reads/writes,
   subprocess/shell execution, outbound HTTP (SSRF surface), serialization/deserialization, message
   queues, secrets storage.
4. **Privilege & supply chain** — anything that runs as root/admin, installers, downloaded binaries,
   `curl | bash`, release/CI workflows that produce artifacts users execute, container/VM/sandbox config.

Each explore sub-agent reports concrete `path:line` evidence for what it found. Synthesize into the template.

### Explore brief (for threat-model mapping)

```
- Task: Map the <concern> attack surface of this repo for a threat model. Read-only.
- Find and report (with path:line): <the concern's specific questions from the list above>
- Report the trust level of each input (untrusted remote / authenticated user / operator-only / dev-CI),
  and which code runs with elevated privilege.
- Do NOT assess vulnerabilities yet; just map the surface and cite evidence.
```

## Required sections

Use `assets/threat_model_template.md`. It must cover:

### 1. Overview
What the system *is*, in real operational terms (not just "a web app"): who runs it, single-tenant vs.
multi-tenant, what the security goal is. Name the production/runtime code vs. the dev/CI surface.
List the important controls that are already implemented (with file references) — these are the
mitigations you'll credit later when calibrating severity. Also enumerate the **assets** an attacker
wants (secrets, PII, payment data, admin capabilities, integrity-critical state, release/signing
artifacts) — findings that reach an asset rank highest.

### 2. Threat model, trust boundaries, and assumptions
State who/what is **trusted** (e.g. host root, admins, the chosen IdP) — if an attacker gains these,
the system is by definition compromised, so those aren't "vulnerabilities". Then enumerate inputs by
trust level:
- **Attacker-controlled:** internet traffic, request bodies, headers, uploaded files, third-party
  callbacks, anything a malicious client or compromised peer can send.
- **Operator-controlled:** install flags, config files, credentials, infra paths. These run with
  privilege "by design"; injection that *requires* malicious operator input is real but lower severity
  than remote-attacker control. Say so explicitly.
- **Developer/CI-controlled:** tests, fixtures, build scripts, workflows. Becomes security-critical the
  moment it produces release artifacts users execute as root.

The trust-boundary calibration is the most important judgment in the whole scan. A bug behind an
operator-only boundary and the same bug on the unauthenticated edge differ by two severity classes.

### 3. Data-flow, source/sink, and guard inventory
Use a compact DFD-style table: external entities, processes/services, data stores, data flows, and the
trust boundary each flow crosses. Then list:

- **Sources:** request bodies/headers, route params, cookies, webhook payloads, queue messages, uploaded
  files, env/config, database rows controlled by users/operators, CI inputs, container/workload output.
- **Sinks:** SQL/NoSQL, shell/subprocess, filesystem, template/rendering, deserialization, crypto, HTTP
  client/proxy, cloud APIs, admin/provider APIs, logs, billing/ledger writes, queue publishes.
- **Sanitizers/guards:** authz/tenant ownership checks, schema validation, allowlists/blocklists,
  escaping/encoding, parameterized queries, SSRF DNS/IP pinning, CSRF checks, idempotency keys, rate
  limits, wallet/entitlement checks, redaction.
- **Unknown framework modeling:** custom routers, ORMs, RPC layers, template systems, queue contracts, or
  generated clients that scanners may not understand.

This inventory drives scan partitioning and source-to-sink validation. Missing or ambiguous trust
boundaries are threat-model findings and should be called out.

### 4. Business invariants and abuse cases
List domain rules that must hold even when a malicious authenticated user, tenant admin, webhook sender,
operator, or CI actor uses valid features in unusual order. Include money, credits, quotas, entitlement
classes, tenant ownership, workflow state machines, retries/idempotency, lifecycle events, and resource
limits. These invariants must be reviewed in full audits, not only in commit-history mode.

### 5. Attack surface, mitigations, and attacker stories
Walk each surface (bootstrap/supply-chain, management plane, dynamic workloads, isolation, identity &
secrets, backups/restore, cluster/network, host/local-user). For each: how an attacker reaches it, what
mitigations already exist, and a concrete "attacker story" of what would go wrong if a control failed.
Include an **out-of-scope calibration** paragraph: what is explicitly *not* this project's problem
(e.g. XSS inside a workload the project merely hosts) so the scan doesn't waste effort or inflate severity.

### 6. Criticality calibration
Define, **for this project**, what counts as critical / high / medium / low, with examples drawn from the
actual surfaces. This is what the severity step in `references/reporting.md` will apply. Anchor it to
trust boundaries and reachability, not to generic CVSS vibes. Example anchors:
- **Critical:** unauthenticated remote code execution or admin access; supply-chain compromise of
  root-executed artifacts; container/sandbox escape to host; leakage of control-plane secrets.
- **High:** authenticated privilege escalation; broken authz exposing other tenants' data; a local→root
  primitive that requires only low-privilege local access; auth bypass on a management route.
- **Medium:** local unprivileged secret disclosure via file modes; DoS via malformed input; missing
  cryptographic integrity where only availability is affected; operator-only argument injection.
- **Low:** static-docs XSS; verbose errors leaking internal paths; CI/test-only issues with no released
  artifact impact; missing rate-limit where an upstream IdP is the real enforcement point.

## Quality bar

End the model with **review priorities**: the handful of areas (in order) that deserve the deepest scan
in this repo — this is where the orchestrator concentrates sub-agents and validation effort first.

A good threat model lets a reader predict the severity of a hypothetical bug before seeing it, just from
where it sits. If your calibration can't distinguish "world-writable `/tmp` path used by a root installer"
(high/critical) from "verbose error message" (low), it isn't specific enough yet.
