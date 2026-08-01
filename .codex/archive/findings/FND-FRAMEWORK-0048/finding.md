# FND-FRAMEWORK-0048 — Workflow-tool publisher expands default-branch metadata directly in shell source

- Category: `security_hardening`
- Repository / ownership: `framework` / `framework`
- Priority / severity / confidence: `P1` / `medium` / `reproduced`
- Status / feasibility: `fixed` / `feasible_now`
- Release blocker / security relevance: `true` / `true`

## Summary

The constrained Framework workflow-tool publisher expanded
`github.event.repository.default_branch` directly inside two `run` blocks.
Checksum-verified Zizmor reported four high-confidence template-injection
findings because GitHub expressions are rendered before shell parsing. The
local repair uses exact step-local `DEFAULT_BRANCH` environment mappings,
quoted variable references, and `git check-ref-format --branch` before ref
construction; the publisher profile hashes and regression tests bind that form.

## Observed and expected behavior

Before the repair, `zizmor --offline .github` returned exit code 1 with four
findings in `.github/workflows/update-workflow-tools.yml` at lines 192, 202,
205, and 225. The metadata appeared directly in shell source for branch fetch,
existing-branch validation, and reusable-branch validation.

The publisher must treat repository metadata as data, not script text. It must
carry the value through a reviewed environment map, quote every shell use,
validate it as a branch ref, and preserve the existing read-only resolver and
validator dependencies before the write-capable publisher can run.

## Impact, boundaries, and preconditions

The affected job has `contents: write` and `pull-requests: write`. A
shell-significant value crossing this boundary could change a publisher shell
command. Current evidence does not claim an untrusted PR author can modify
repository default-branch metadata; the observation is nevertheless a required
CI-security failure and release-blocking hardening gap.

It requires a scheduled or manual updater execution after resolver and
validator success and a shell-significant metadata value, or a future broadening
of the metadata trust boundary.

## Evidence and reproduction

- Run: `20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e`
- Evidence: `evidence/zizmor-template-injection-remediation.md`
- SHA-256: `2c8ab7e8fc947188f9bd9ca312457a21042051580a2c18bafdfc368b7feac468`
- Pre-fix: checksum-verified `zizmor --offline .github`, exit `1`
- Post-fix: same command, exit `0`, no active findings
- Verified PR remediation head: `1fd3b362e0fed9766c6920e3c7bd1939535850f2`

No publisher, GitHub token operation, remote action, or PR workflow was run
during reproduction.

## Root cause and remediation

The workflow used GitHub expression syntax within shell source. The remediation
adds exact `DEFAULT_BRANCH` environment maps to the two publisher steps,
validates the value through `git check-ref-format --branch`, references it only
as a quoted shell variable, and updates the contract step profiles and body
digests. It does not relax permissions, action pins, validator dependency,
branch condition, or draft-only delivery controls.

## Acceptance and validation

The direct expression must not occur in a publisher `run` body; both environment
maps must match the reviewed profile; branch validation and quoted uses must
remain in the hashed program body; static workflow contracts and Zizmor must
pass. The exact hosted consolidation PR must pass applicable workflow-security
checks before the finding can become verified or closed.

## Dependencies, blockers, and residual risk

No implementation dependency remains. The exact PR #42 head now passed hosted
workflow lint/Zizmor, the Sonar PR Quality Gate, and all other applicable
controls. This strengthens the `fixed` disposition, but the finding is neither
`verified` nor closed until normal master integration and resulting-master
evidence. `FND-FRAMEWORK-0047` is a separate action-lock provenance repair;
`FND-SONAR-0002` remains an independent master-integration blocker.

## History

- 2026-07-22T16:30:00Z: reproduced by checksum-verified Zizmor, repaired in
  the Framework consolidation worktree, and locally rechecked with no active
  Zizmor findings.
- 2026-07-22T17:24:06Z: the local repair was committed at
  `22747d460a9f7be02760edf05c311be376492457`; clean-worktree, exact-range
  whitespace, and native `make lint` checks passed. Hosted exact-head evidence
  remains required.
- 2026-07-22T17:42:25Z: PR #42 head
  `1fd3b362e0fed9766c6920e3c7bd1939535850f2` passed hosted workflow
  lint/Zizmor, the Sonar PR Quality Gate, and all other applicable controls.
