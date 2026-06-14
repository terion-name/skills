<One-line title: what the bug is and its primary impact>
Criticality: <critical|high|medium|low|informational> (attack path: <critical|high|medium|low|informational>)
Status: <validated|likely|unvalidated|false-positive>
Origin: <introduced-by-diff|pre-existing|uncertain>   # commit/diff mode only; omit for full audits

# Metadata
Repo: <owner/name>
Commit: <introducing short sha, or reviewed HEAD/diff sha when not known. In commit-history mode this MUST be the introducing commit, not the review HEAD>
Fixed in commit: <short sha if already fixed; omit if unresolved. Do not replace with nonstandard "Fixed:" metadata>
Author: <if known>
Created: <date, time>
Category: <auth|injection|ssrf|supply-chain|secrets|cve|container|iac|crypto|memory|functional-regression|other>
CWE: <CWE-NNN - short label from references/cwe/cwe-labels.json>
CWE description: <one-sentence description from references/cwe/cwe-catalog.jsonl, trimmed for readability>
CWE mapping: <primary|approximate|advisory-provided>; <one-sentence rationale that ties the weakness to this finding>
Standards: <CWE-NNN, ASVS vX.Y.Z-..., OWASP APIx:YYYY, NIST SSDF PW/RV/..., SLSA/Scorecard where applicable>
Detected by: <manual review|commit-review|semgrep|trivy|osv-scanner|gitleaks|codeql|other>
Assignee: <Unassigned>
Signals: Security, <Validated|Likely|Unvalidated>, <Patch generated>, <Attack-path>
Resolution: <if applicable>

# Summary
<Plain-language description of the bug, its root cause, and the fix direction, in a few sentences. A
reader should understand the whole finding from this paragraph alone. State where the untrusted input
enters, the sink it reaches, why the guard is absent or bypassable, and the recommended remediation.>

# Validation
## Rubric
- [ ] <Each box is a discrete claim you confirmed — e.g. "Confirmed the route loads the object by
      user-supplied id with no ownership check.">
- [ ] <…>
- [ ] <Demonstrate the primitive / reproduce the impact.>
## Report
<How you validated. If dynamic: the PoC, the command run, and the observed result (with output excerpts).
If code-review only: trace each hop with path:line and state explicitly why dynamic repro was skipped
(missing toolchain, network blocked, would be destructive). Record environment caveats.>
## Negative evidence / false-positive checks
<What you checked that could have made this non-exploitable: ownership guards, sanitizers, allowlists,
framework behavior, deployment preconditions, later fixes. Say what still failed and why.>
## Revalidation after fix
<How to confirm remediation: command/test/static check/manual trace, and what regression risk the patch has.>

# Evidence
<path/to/file (Lstart to Lend)>
  Note: <one line explaining what this excerpt shows>
```
<minimal code excerpt — enough to prove the point, not the whole file>
```

<repeat per evidence location>

Proposed patch:
```diff
<unified diff that fixes the root cause minimally — PROPOSED only, not applied>
```

# Attack-path analysis
Final: <severity> | Decider: <model_decided|policy> | Matrix severity: <severity> | Policy adjusted: <severity>
## Rationale
<Why this final severity. What raised or lowered it relative to the matrix, in terms of trust boundary
and reachability for this project.>
## Likelihood
<low|medium|high> - <why: reachability, preconditions, determinism.>
## Impact
<low|medium|high> - <what successful exploitation grants.>
## Assumptions
- <each precondition the exploit requires>
## Path
<entry trust level> -> <step> -> <step> -> <terminal impact>
## Path evidence
- `path:line` - <what this hop establishes>
- <…>
## Narrative
<Prose walkthrough of the attack from the attacker's point of view, tying the path evidence together.>
## Controls
- <missing control that would prevent this>
- <…>
## Patch regression risk
- <behavior/security compatibility risk introduced by the proposed fix, and tests/checks that should cover it>
## Blindspots
- <what you could not fully verify, env gaps, assumptions not exhaustively checked>
