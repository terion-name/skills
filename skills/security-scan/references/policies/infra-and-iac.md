# Policy: infrastructure & IaC (containers, K8s, Terraform, Ansible, cloud)

Infra misconfig is where "small" issues become host/cluster compromise. The `assets/example_finding.md` finding
lives here. Read alongside `secrets-and-supply-chain.md`.

## Docker / Compose

- **Privilege:** `--privileged`, `--cap-add=ALL`/dangerous caps (`SYS_ADMIN`, `NET_ADMIN`), running as
  root (no `USER`), `--pid=host`/`--net=host`/`--ipc=host` (namespace escape surface).
- **Mounts:** Docker socket mounted into a container (`/var/run/docker.sock` → trivial host root),
  host-path mounts of sensitive dirs (`/`, `/etc`, `/root`), writable bind mounts.
- **Image hygiene:** base image pinned by digest; no secrets in layers/`ENV`/build args; multi-stage so
  build tooling/creds don't ship; `.dockerignore` excludes `.git`/`.env`; non-root runtime user; read-only
  rootfs where possible; healthcheck and resource limits set.
- **Build:** `ADD` of remote URLs (use verified `COPY`), unpinned `apt`/`pip`/`npm` installs.

## Kubernetes

- **Pod security:** `securityContext` — `runAsNonRoot`, drop all caps, `readOnlyRootFilesystem`,
  `allowPrivilegeEscalation: false`, no `privileged`, seccomp `RuntimeDefault`. No `hostNetwork`/`hostPID`/
  `hostIPC`/`hostPath`.
- **RBAC:** no wildcard verbs/resources, no `cluster-admin` to workloads, ServiceAccount tokens not
  auto-mounted unless needed, no `secrets`-list to broad roles.
- **Secrets:** real secrets not in plain ConfigMaps/manifests; encryption-at-rest; not in env if avoidable.
- **Network:** NetworkPolicies default-deny; no unintended `LoadBalancer`/`NodePort` exposure; `Ingress`
  TLS + auth.
- **Images:** pinned digests, `imagePullPolicy`, admission/policy controls.

## Terraform / CloudFormation / cloud IAM

- **Network exposure:** security groups / firewall rules with `0.0.0.0/0` on sensitive ports (22, 3389,
  DB ports, admin UIs); public S3/blob buckets; public DB instances.
- **IAM:** wildcard `Action: "*"` / `Resource: "*"`, `iam:PassRole` to broad principals, overly-trusting
  assume-role policies, long-lived access keys vs. roles.
- **Encryption / logging:** unencrypted storage/volumes/snapshots; disabled audit logging (CloudTrail/
  flow logs); public AMIs/snapshots.
- **State & secrets:** secrets in `.tf`/variables/state committed; remote state unencrypted or world-readable.
- **Provisioners:** `local-exec`/`remote-exec` running unvalidated input.

## Ansible / shell provisioning (the example finding's class)

- **Privileged extraction:** `unarchive`/`get_url` as root (`become: true`) into shared/world-writable
  paths; downloads to predictable `/tmp` paths a local user can pre-seed; `get_url` without `force: true`
  + `checksum:` (accepts a pre-existing attacker file); extracting archives that aren't path-validated
  into `/`. Fix: root-owned `0700` staging (`tempfile`), `force: true`, cryptographic `checksum`/signature,
  validate archive members before extraction.
- **Secrets in logs:** tasks rendering secrets without `no_log: true`.
- **Command tasks:** `shell`/`command` with unsanitized variables (injection); prefer modules over `shell`.
- **File modes:** secret files not `0600`; world-readable creds; `become` where not needed.
- **Idempotence as a control:** fresh-install code paths (missing-file conditions) often skip later guards
  — check the *first-run* path, where the example finding's exploit lived.

## Reverse proxy / network edge (Traefik / Nginx / ingress)

- Management/dashboard routes exposed without auth (ForwardAuth/oauth2-proxy bypass); admin services bound
  to `0.0.0.0` instead of loopback; TLS misconfig (weak ciphers, no HSTS); header smuggling/normalization;
  open default-deny gaps in the firewall (UFW/iptables) for cluster/raw ports broader than intended;
  OVN/cluster DB remotes "insecure" relying only on a firewall CIDR that's too broad.

## systemd / host services

Units running as root that exec writable paths; `EnvironmentFile` with secrets world-readable;
`ExecStart` of a script in a user-writable dir; missing sandboxing (`ProtectSystem`, `NoNewPrivileges`,
`PrivateTmp`); `sudoers` fragments / `cron.d` entries writable by non-root (a root-owned arbitrary write
to these → RCE, the example finding's terminal impact).

## Tools

`checkov -d .`, `trivy config .` / `tfsec`, `hadolint Dockerfile`, `kubesec`/`kube-score`, `trivy image`
for built images. Confirm every hit against the actual manifest and the deployment's real exposure.
