#!/usr/bin/env bash
# Scaffold the .security/ directory used by the security-scan skill.
# Idempotent: safe to re-run; never overwrites an existing threat_model.md or findings.
set -euo pipefail

ROOT="${1:-.}"
SEC_DIR="$ROOT/.security"

mkdir -p "$SEC_DIR/findings" "$SEC_DIR/tool-results" "$SEC_DIR/validation" "$SEC_DIR/patches"

# .gitignore inside .security/ so noisy raw tool output isn't committed,
# but the threat model, findings, manifest, patches, and summary report are.
if [ ! -f "$SEC_DIR/.gitignore" ]; then
  cat > "$SEC_DIR/.gitignore" <<'EOF'
# Raw scanner output and bulky repro artifacts are evidence/scratch — keep locally, don't commit.
tool-results/
validation/
EOF
fi

if [ ! -f "$SEC_DIR/threat_model.md" ]; then
  echo "[init] No threat model found at $SEC_DIR/threat_model.md — build one (see references/threat-model.md)."
else
  echo "[init] Existing threat model found — treat it as source of truth and refresh only stale parts."
fi

echo "[init] .security/ ready at: $SEC_DIR"
echo "       findings/     -> one finding per file (SEC-NNN-slug.md), numbered by severity"
echo "       tool-results/ -> raw scanner output per tool (gitignored)"
echo "       validation/   -> repro notes/commands/output per finding, SEC-NNN/ (gitignored)"
echo "       patches/      -> proposed fix diffs SEC-NNN-suggested.patch (never auto-applied)"
echo "       scan_manifest.md + report.md -> written during/after the scan"
