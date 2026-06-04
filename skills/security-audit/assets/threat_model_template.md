# Threat model — <repo name>

> Scan-time security context. Source of truth for trust boundaries, assumptions, and criticality
> calibration. Refresh as the architecture changes. Cite `path:line` evidence throughout.

## 1. Overview
<What the system is in real operational terms: who runs it, single- vs multi-tenant, the security goal.>
<Which code is production/runtime vs. dev/CI surface.>
<Important controls already implemented, with file references — these are credited as mitigations later.>

## 1b. Assets (what an attacker wants)
<Secrets/credentials, PII, payment data, admin capabilities, integrity-critical state, compute
resources, release/signing artifacts. Findings that reach these rank highest.>

## 2. Threat model, trust boundaries, and assumptions
**Trusted (out of scope as "vulnerabilities"):** <e.g. host root, admins, the chosen IdP. If an attacker
gains these, the system is compromised by definition.>

**Attacker-controlled inputs:** <internet traffic, request bodies/headers, uploads, third-party
callbacks, compromised peers, untrusted containers, …>

**Operator-controlled inputs:** <install flags, config files, credentials, infra paths — run with
privilege by design; injection requiring these is lower severity than remote-attacker control.>

**Developer/CI-controlled inputs:** <tests, fixtures, build scripts, workflows — security-critical only
when they produce release artifacts users execute.>

## 3. Data-flow, source/sink, and guard inventory

| Flow | Source / trust level | Boundary crossed | Process / data store | Sink or asset | Guard / sanitizer | Evidence |
|------|----------------------|------------------|----------------------|---------------|-------------------|----------|
| <e.g. public API request -> session create> | <remote unauthenticated / authenticated tenant / operator / CI> | <internet -> API, tenant -> control plane, workload -> host, CI -> release> | <service/table/queue> | <sink/asset> | <authz/schema/allowlist/idempotency/etc.> | `<path:line>` |

**Untrusted source inventory:** <route params, headers, cookies, request bodies, webhooks, queue messages,
uploaded files, env/config, DB rows, CI inputs, container output, etc.>

**Dangerous sink inventory:** <SQL/NoSQL, filesystem, shell/subprocess, template/rendering,
deserialization, HTTP/proxy/cloud APIs, billing/ledger writes, queue publishes, logs, secrets, etc.>

**Sanitizers and guards:** <authz/ownership, schema validation, allowlists/blocklists, contextual encoding,
parameterized queries, SSRF DNS/IP pinning, CSRF, idempotency, rate limits, wallet/entitlement checks,
redaction.>

**Scanner modeling gaps:** <custom framework/router/ORM/RPC/template/queue/generated client behavior that
static tools may miss.>

## 4. Business invariants and abuse cases

| Invariant | Assets protected | Abuse case | Current guard | Evidence |
|-----------|------------------|------------|---------------|----------|
| <tenant can only access own objects> | <tenant data> | <swap object id / replay terminal summary / use another project token> | <ownership check> | `<path:line>` |
| <every admitted resource is billable> | <credits/compute/egress> | <request unsupported tier / proxy class / failure path> | <price + wallet + entitlement checks> | `<path:line>` |

## 5. Attack surface, mitigations, and attacker stories
For each surface: how an attacker reaches it · existing mitigations · what goes wrong if a control fails.

- **Bootstrap / supply chain:** <…>
- **Management / control plane:** <…>
- **Application / API surface:** <…>
- **Data stores & external I/O (SSRF, deserialization):** <…>
- **Isolation (containers/VM/sandbox):** <…>
- **Identity & secrets:** <…>
- **Backups / restore / storage:** <…>
- **Cluster / network edge:** <…>
- **Host / local users:** <…>

**Out-of-scope calibration:** <what is explicitly NOT this project's problem, to avoid wasted effort /
inflated severity.>

## 6. Criticality calibration
Define, for THIS project, with examples drawn from the surfaces above. Anchor to trust boundary + reachability.

- **Critical:** <…>
- **High:** <…>
- **Medium:** <…>
- **Low:** <…>

## 7. Review priorities
<The handful of areas that deserve the deepest scan in THIS repo, in order — where the orchestrator
should concentrate sub-agents and validation effort first.>
