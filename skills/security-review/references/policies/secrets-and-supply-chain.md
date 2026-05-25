# Policy: secrets & supply chain

Two of the highest-impact, most common real findings. Supply-chain compromise of an artifact users run as
root is critical (see `assets/example_finding.md`'s class). A leaked control-plane secret can be instant takeover.

## Hardcoded / leaked secrets

**Rule:** no credentials in source, config-in-repo, history, logs, or client bundles.

Look for: API keys, tokens, passwords, private keys (`BEGIN ... PRIVATE KEY`), cloud creds (AWS
`AKIA...`, GCP service-account JSON), DB connection strings with passwords, JWT signing keys, `.env`
committed, secrets in CI YAML, secrets baked into Docker images / layers, secrets in client/browser
bundles (anything shipped to the browser is public).

Scan working tree **and history** (`gitleaks detect`, `trufflehog git file://.`). A secret removed in the
latest commit is still exposed in history.

**Handling real secrets:** report a **redacted fingerprint + location** — never the full value, in
artifacts or chat. Record type, `path:line`, a prefix/suffix and confidence
(`AWS-key-like token at config/prod.env:12, prefix AKIA…/suffix …X7Q, confidence high`) — enough to
locate and triage, not to use. Recommend (1) rotate/revoke immediately (assume compromised once
committed), (2) move to a secret manager / env injection, (3) purge history (`git filter-repo`), (4) add
detection to CI. Distinguish real secrets from test fixtures/examples, but when unsure, treat as real and flag.

## Dependency integrity

- **Unpinned / unverified downloads:** `curl ... | bash`, `wget && chmod +x && run`, `pip install`/`npm i`
  of unpinned versions in install/build scripts, downloads without checksum or signature verification
  (the example finding's `get_url` without `force:true`/checksum is exactly this). Fix: pin versions, verify
  SHA256 / GPG signature before execution, download to a root-owned private dir (not world-writable `/tmp`).
- **Lockfiles:** present and committed; CI installs with `--frozen-lockfile` / `npm ci` / `pip install
  --require-hashes`. Integrity hashes intact.
- **Dependency confusion:** internal package names not claimed on the public registry → an attacker
  publishes a malicious public package of the same name that gets pulled. Check private scopes are
  reserved and the registry/scope is pinned.
- **Typosquats / abandoned packages:** suspicious near-miss names, recently-changed maintainers, packages
  with install scripts (`postinstall`, `setup.py` code) doing network/FS work.
- **Known CVEs:** run the SCA tools in `tooling.md`; rate by reachability (a vuln on a live code path > an
  unreachable transitive one).

## Build, CI/CD, release

The moment dev/CI surface produces an artifact users execute, it's security-critical:

- Release workflows: are artifacts built from a verified ref, signed, checksummed, and is the checksum
  *enforced* by the installer (publishing a SHA without verifying it does nothing)?
- CI secrets: scoped, masked (`no_log` in Ansible, masked vars in CI), not echoed to logs; forks can't
  exfiltrate them via PR-triggered workflows (`pull_request_target` abuse).
- Action/step pinning: third-party CI actions pinned to a commit SHA, not a mutable tag.
- Workflow permissions least-privilege; no `write-all` token by default.
- Container base images pinned by digest; multi-stage builds so secrets/build tools don't ship in the
  final image.

## Privileged install / provisioning

For installers and IaC that run as root (Ansible/shell/etc.): staging dirs must be root-owned and not
world-writable; downloads forced + checksum-verified before extraction; archives validated (no traversal/
absolute paths) before `unarchive dest=/`; predictable paths in shared dirs (`/tmp`) are a local-privesc
vector. This is the `infra-and-iac.md` overlap and the example finding's exact bug.

## Tools

`gitleaks`, `trufflehog`, `osv-scanner`/`trivy`/`grype` (CVE), `syft` (SBOM), `npm/pip/cargo/go` native
audits. See `tooling.md` for commands.
