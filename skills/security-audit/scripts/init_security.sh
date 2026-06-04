#!/usr/bin/env bash
# Scaffold the .security/ directory used by the security-audit skill.
# Idempotent: safe to re-run; never overwrites an existing threat_model.md or findings.
set -euo pipefail

ROOT="${1:-.}"
SEC_DIR="$ROOT/.security"

mkdir -p "$SEC_DIR/findings" "$SEC_DIR/fixed" "$SEC_DIR/tool-results" "$SEC_DIR/validation"

# .gitignore inside .security/ so noisy raw tool output isn't committed,
# but threat model, findings, fixed findings, manifest, tool triage, completion gate, and summary report are.
if [ ! -f "$SEC_DIR/.gitignore" ]; then
  cat > "$SEC_DIR/.gitignore" <<'EOF'
# Raw scanner output and bulky repro artifacts are evidence/scratch — keep locally by default.
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
echo "       latest_reviewed_commit -> cursor written after each commit-history review step"
echo "       commit_review_progress.md -> in-flight commit queue/progress log"
echo "       findings/     -> one finding per file (SEC-NNN-slug.md), chronological IDs"
echo "       fixed/        -> remediated findings moved here, keeping original SEC-NNN IDs"
echo "       tool-results/ -> raw scanner output only (gitignored)"
echo "       validation/   -> repro notes/commands/output per finding, SEC-NNN/ (gitignored)"
echo "       tool_triage.md -> every tool output/advisory mapped to finding/dismissal/blocker"
echo "       completion_gate.txt -> final audit_completion_gate.py output"
echo "       scan_manifest.md + report.md -> written during/after the scan"
