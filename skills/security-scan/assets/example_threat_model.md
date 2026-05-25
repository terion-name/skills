<!--
ANONYMIZED WORKED EXAMPLE — not a real project. Shows the target shape and quality bar for a threat
model (see references/threat-model.md and assets/threat_model_template.md). Fictional product.
-->

# Threat model — host-provisioner

## 1. Overview
host-provisioner is a root-run provisioning and operations toolkit for a single Linux VPS. It installs a
container runtime, a reverse proxy, a web admin console, an auth proxy, optional self-hosted identity,
backup timers, and a small compiled CLI. In real use it is a single-owner control plane for development
sandboxes, not a hostile multi-tenant PaaS. The security goal: keep the host hardened, keep containers
private by default, and make any public exposure explicit and recoverable. Production/runtime code is the
installer, the `scripts/` toolkit, and the Ansible roles; tests, docs, and CI are dev/CI surface unless
they publish release artifacts. Implemented controls include a default-deny firewall (only 22/80/443 plus
configured ports), loopback binding for the admin console and runtime API, ForwardAuth on management
routes, an auth proxy with group checks and secure cookies, isolated container idmaps, and snapshot/S3
backup exports for recovery.

## 1b. Assets (what an attacker wants)
OIDC client secrets and identity admin credentials; S3 backup keys; the admin console / runtime API
(host root-equivalent); release/signing artifacts users execute as root; container workloads and their data.

## 2. Threat model, trust boundaries, and assumptions
**Trusted (compromise = game over, not "vulnerabilities"):** host root, members of the runtime admin
group, and the selected OIDC IdP.

**Attacker-controlled inputs:** internet traffic to the proxy on 80/443 and any raw ports opened from
container config; browser/OIDC callback traffic; data sent to published workload services; malicious or
compromised containers; S3 backup objects if the bucket is attacker-writable. Container config labels are
attacker-controlled only where non-admin tenants can set them; in the single-owner model they are operator-controlled.

**Operator-controlled inputs (dangerous by design, run as root):** install/CLI flags, the config file,
domains, storage device paths, S3/backup credentials, cluster tokens and peer CIDRs, external OIDC
settings. Injection that requires these is lower severity than remote-attacker control, but still matters
for defense-in-depth.

**Developer/CI-controlled inputs:** tests, fixtures, docs, build scripts, CI workflows — security-critical
once they publish release artifacts users run as root.

## 3. Attack surface, mitigations, and attacker stories
- **Bootstrap / supply chain:** installer is used via `curl | bash` as root; it downloads release bundles
  and third-party binaries. A compromised release or unverified downloaded binary is a critical root-RCE
  path. Checksums exist in release output but the installer does not enforce verification before execution.
- **Management plane:** an unauthenticated attacker hits the proxy, not the admin console (loopback +
  auth-proxy + PAM) or the runtime API (loopback + OIDC group mapping) directly. A bypass in the
  ForwardAuth config, auth-proxy policy, group-claim handling, or API auth mapping would be high/critical.
- **Dynamic workload publishing:** a sync script reads container config and publishes HTTP/raw routes; it
  rejects malformed routes, dedupes, writes atomically, and syncs the firewall. An admin intentionally
  exposing a service is operator action; if an untrusted tenant could set those labels it would be a
  serious boundary violation.
- **Container isolation:** containers are private by default; binding `0.0.0.0` inside one is not public.
  Default profiles enable nesting/syscall intercepts for container-in-container; a strict profile omits
  them. Workload vulns are contained unless published or an escape reaches host root.
- **Identity & secrets:** secrets live in `0600` config, env, and compose files, and also in the runtime
  config store, so admin/root equals secret access. Some provisioning tasks render secrets without
  suppressing logs — audit to avoid CI/operator log leakage.
- **Backups/restore:** export streams a filesystem snapshot through compression to object storage;
  restore prompts before destructive ops. Backups aren't signed/encrypted by the tool, so confidentiality/integrity depend on
  the provider; a compromised bucket can feed a malicious restore, but exploitation needs operator restore.
- **Cluster/network:** join tokens, peer-CIDR firewall openings, and an "insecure" cluster DB remote
  relying on firewall restriction — a broad/attacker-controlled CIDR can expose cluster services.
- **Host/local users:** credential files under the config dir are `0600`; local unprivileged users aren't
  a primary trust boundary, but file modes and predictable paths still matter (see the worked finding).

**Out-of-scope calibration:** XSS/SQLi inside a workload the tool merely hosts is a workload issue unless
the tool publishes it without intended auth. SSRF via configured S3/OIDC endpoints is operator-controlled.
Vulns only in tests/docs/build tooling are low unless they affect release artifacts.

## 4. Criticality calibration
- **Critical:** unauthenticated access to the admin console / runtime API / root shell; supply-chain
  compromise of the installer or root-executed release bundles; container escape to host root from the
  default profile; leakage of OIDC client secrets, identity admin creds, or S3 keys.
- **High:** authenticated non-admin gaining management access via bad group mapping; untrusted tenant
  exposing internal services / raw ports; broad cluster-firewall rules; S3 restore accepting
  attacker-controlled streams; route-auth bypass on group-restricted routes.
- **Medium:** local unprivileged secret read via bad file modes / unsuppressed logs; DoS via malformed
  labels; missing backup integrity when only availability is affected; operator-only argument injection.
- **Low:** static-docs XSS; verbose errors leaking internal paths; config that only aborts install;
  CI/test-only issues with no released-artifact impact; missing rate limits where the IdP is the enforcer.

## 5. Review priorities
1. Bootstrap / supply-chain integrity (download verification, root extraction, predictable paths).
2. Management-plane auth (ForwardAuth, auth-proxy, OIDC group mapping) for bypass.
3. Secret handling (file modes, log suppression, where secrets are stored).
4. Container isolation and any path from a published workload to host root.
