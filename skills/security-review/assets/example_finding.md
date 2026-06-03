<!--
ANONYMIZED WORKED EXAMPLE — not a real project. Shows the target shape and quality bar for a finding
file (see references/reporting.md and assets/finding_template.md). Fictional repo/author/commit.
-->

Predictable world-writable bundle path enables arbitrary root file write during provisioning
Criticality: high (attack path: high)
Status: validated
Origin: introduced-by-diff

# Metadata
Repo: example-org/host-provisioner
Commit: abc1234
Author: maintainer@example.com
Created: 2026-01-15, 10:52 AM
Category: iac
Detected by: manual review + semgrep
Assignee: Unassigned
Signals: Security, Validated, Patch generated, Attack-path
Resolution: —

# Summary
A new Ansible role enables prebuilt plugin bundles by default, downloads the bundle to a predictable path
under world-writable `/tmp`, and later extracts it to `/` as root. The `get_url` task sets neither
`force: true` nor a `checksum`, so under Ansible's default `force: false` semantics a pre-existing file at
that path is accepted as-is. Because `/tmp` is world-writable and the filename is derived from the public
release ref and architecture, a local unprivileged user can pre-seed the path before the root-run
playbook executes; on a fresh install the extract task's guard is satisfied and attacker-controlled tar
entries are written anywhere under `/` as root. Fix: stage to a root-owned `0700` dir via `tempfile`,
download with `force: true` + a cryptographic `checksum`, and validate archive members before extraction.

# Validation
## Rubric
- [x] The role runs as root (`become: true`) and is reached by the normal installer.
- [x] Prebuilt bundles are enabled by default and the bundle filename is predictable from public ref + arch.
- [x] The download target is under world-writable `/tmp` with no `force: true` and no checksum.
- [x] The extract task runs on a fresh install (plugin-present guard is false) and unarchives to `/`.
- [x] Demonstrated the root-extraction primitive writing a root-owned file the unprivileged user could not.
## Report
Validated against commit abc1234 by targeted code review plus a direct reproduction of the extraction
primitive. This is a declarative/Ansible flaw, not a memory-safety bug, so sanitizer/debugger validation
is N/A. A full end-to-end playbook run was not possible (ansible not installable in the sandbox; package
install returned proxy 403s), so dynamic repro was scoped to the privileged-extraction primitive.

Dynamic primitive: as user `nobody`, created the predictable `/tmp/host-provisioner-plugins-main-amd64.tar.gz`
containing a tar entry `usr/local/share/poc-root-write` owned root:root. Extracting it as root with
`tar -xzf <archive> -C /` (the primitive behind `unarchive: dest=/ remote_src: true`) produced a
root-owned file under `/usr/local/share`, a directory the unprivileged user cannot write. Repro notes,
commands, and output saved under `.security/validation/SEC-001/`.

# Evidence
roles/plugins/defaults/main.yml (L18 to 20)
  Note: prebuilt bundles enabled by default; release ref is predictable.
```
plugin_bundle_enabled: true
plugin_bundle_repo: example-org/host-provisioner
plugin_bundle_main_ref: plugins-main
```

roles/plugins/tasks/main.yml (L51 to 61)
  Note: downloaded to a predictable world-writable /tmp path with no force/checksum, so a pre-existing
  local file is accepted.
```
- name: Download prebuilt plugin bundle
  ansible.builtin.get_url:
    url: "https://github.com/{{ plugin_bundle_repo }}/releases/download/{{ ref }}/plugins-linux-{{ arch }}.tar.gz"
    dest: "/tmp/host-provisioner-plugins-{{ ref }}-{{ arch }}.tar.gz"
    mode: "0644"
  register: plugin_bundle_download
  failed_when: false
```

roles/plugins/tasks/main.yml (L72 to 79)
  Note: the registered archive is extracted as root into / when plugin files are missing (fresh install).
```
- name: Install prebuilt plugin bundle
  ansible.builtin.unarchive:
    src: "{{ plugin_bundle_download.dest }}"
    dest: /
    remote_src: true
  when:
    - plugin_bundle_usable | default(false)
    - plugin_bundle_download.changed or not plugin_index.stat.exists
```

Proposed patch:
```diff
--- a/roles/plugins/tasks/main.yml
+++ b/roles/plugins/tasks/main.yml
@@
+- name: Create root-owned staging file for the plugin bundle
+  ansible.builtin.tempfile:
+    state: file
+    suffix: "-plugin-bundle.tar.gz"
+  register: plugin_bundle_tmp
+
 - name: Download prebuilt plugin bundle
   ansible.builtin.get_url:
     url: "https://github.com/{{ plugin_bundle_repo }}/releases/download/{{ ref }}/plugins-linux-{{ arch }}.tar.gz"
-    dest: "/tmp/host-provisioner-plugins-{{ ref }}-{{ arch }}.tar.gz"
-    mode: "0644"
+    dest: "{{ plugin_bundle_tmp.path }}"
+    force: true
+    mode: "0600"
+    checksum: "sha256:{{ plugin_bundle_sha256 }}"
   register: plugin_bundle_download
   failed_when: false
```

# Attack-path analysis
Final: high | Decider: policy | Matrix severity: high | Policy adjusted: high
## Rationale
Kept at high. The bug is in the main root-run provisioning role; static evidence shows default-enabled
bundles, a predictable world-writable path, no checksum/force, and root extraction into `/`, and the
primitive was reproduced. Impact is full host compromise via arbitrary root file write. Not raised to
critical because exploitation is local-only, requires a pre-existing low-privilege foothold, and depends
on a root/operator playbook run — limiting remote reach.
## Likelihood
medium — straightforward once a local user can write `/tmp` and the filename is predictable, but not
remotely reachable and gated on a root/operator install or convergence run (most plausibly first provisioning).
## Impact
high — an arbitrary root-owned file write during provisioning. Writing `/etc/cron.d`, `sudoers.d`, a
systemd unit, or a shell profile realistically yields root code execution and full host compromise.
## Assumptions
- A local unprivileged user (or compromised low-priv process) can write `/tmp` before provisioning.
- The playbook is run as root via the normal installer/reconfigure path.
- Fresh install (or a missing plugin index) so the extract guard is true.
- Release ref + arch are predictable (main → plugins-main, x86_64 → amd64).
## Path
local user -> pre-seed /tmp/host-provisioner-plugins-<ref>-<arch>.tar.gz -> root get_url (no force/checksum) -> unarchive dest=/ -> root file write/RCE
## Path evidence
- `site.yml:1-4` — provisioning play runs with `become: true` (root).
- `roles/plugins/defaults/main.yml:18-20` — bundles enabled by default; predictable main ref.
- `roles/plugins/tasks/main.yml:51-61` — predictable `/tmp` dest, no force/checksum.
- `roles/plugins/tasks/main.yml:72-79` — extract to `/` as root on fresh install.
## Narrative
A local attacker pre-creates the predictable bundle path in world-writable `/tmp`. When the root
playbook runs on a fresh host, `get_url` (force=false) accepts the existing file and `unarchive` extracts
its attacker-controlled entries into `/` as root, allowing a write to any root-consumed config path and
hence root code execution. Local-only and gated on an operator run, so high rather than critical.
## Controls
- Playbook uses root via `become: true`.
- No checksum/signature verification on the download.
- No `force: true`, so a pre-existing world-writable-dir file is reused.
- No root-owned private staging dir.
- No archive-path allowlist / extraction sandbox before `unarchive dest=/`.
## Blindspots
- No full end-to-end Ansible run in this stage (toolchain unavailable).
- `get_url` behavior varies by version, but the integrity gap and predictable dest remain.
- Real-world likelihood depends on whether untrusted local users exist before provisioning.
