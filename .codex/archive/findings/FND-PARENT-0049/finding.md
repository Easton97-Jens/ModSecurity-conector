# FND-PARENT-0049 — Update-submodules dependency command is invalid as a YAML plain scalar

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0049 |
| Category | ci_failure |
| Repository / ownership | parent / parent |
| Priority / severity | P1 / not_applicable |
| Confidence / status | confirmed / fixed |
| Feasibility | requires_user_decision |
| Release blocker | yes |
| Security relevant | yes |

## Observation and impact

Draft Parent [PR #92](https://github.com/Easton97-Jens/ModSecurity-conector/pull/92)
initial head `f22e3fdb322e93cf9b37e13ede13007c912e0f9b` caused five shared
structure/quick-check jobs to fail before Framework candidate validation. The
Framework workflow-YAML checker reported:

```text
error .github/workflows/update-submodules.yml: invalid YAML
yaml.scanner.ScannerError: mapping values are not allowed here
line 94, column 83: --only-binary=:all: --require-hashes
```

The one cause affected `scaffold-lint`, `quick-check`, `apache-structure`,
`common-structure`, and `nginx-structure`; it is not five independent defects.
The failure occurs before candidate code and the write-capable publisher, so it
fails closed and does not broaden a privilege boundary.

The quoting correction and its static regression are present at exact PR #92
head `40a419d5b0f599566469060112b7e55dbab05744`. Its 39 hosted checks are
terminal: 33 succeeded and 6 were expectedly skipped; SonarQube Cloud passed
its Quality Gate with zero new issues and zero security hotspots. This proves
the task-owned PR correction, but it is not master-only workflow evidence.

## Root cause and safe remediation boundary

The initial remediation placed `--only-binary=:all:` in an unquoted YAML plain
scalar. Its closing colon is followed by whitespace, so YAML treats it as a
mapping delimiter. Quote the complete `run:` command and add a static
regression that requires the quote form. Preserve the exact hash lock,
`--require-hashes`, `--only-binary=:all:`, validator `contents: read`, and the
separate gated publisher. Do not change Framework, MRTS, the gitlink,
permissions, secrets, or publisher code.

## Acceptance criteria and validation plan

1. PyYAML parses the workflow successfully after the command is quoted.
2. Static coverage requires the exact quoted command while retaining its order
   between the interpreter contract and `make quick-check`.
3. Focused workflow-security tests, `make check-ci-security-contract`, focused
   bilingual tests, and `git diff --check` pass.
4. A focused CI-supply-chain security review covers the amendment.
5. Fresh exact-head PR #92 checks replaced the initial parser failures at
   `40a419d5b0f599566469060112b7e55dbab05744`. Only a later separately
   authorized master integration can verify the master-only
   FND-PARENT-0049/FND-PARENT-0048/FND-PARENT-0045 outcome.

## Evidence

Retained receipt:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T051154Z-fnd-parent-0045-update-submodules-validation-0a8cca09/evidence/pr-92-yaml-scalar-failure.md`

SHA-256:
`68f7d8f2d693799369778f5111864954bacf679e75d5e02794ec73f9c0e9cce2`

Exact-head success receipt:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T051154Z-fnd-parent-0045-update-submodules-validation-0a8cca09/evidence/pr-92-40a419d-exact-head-checks.md`

SHA-256:
`7aff214afed70a39ec9863fc855627e835a6eb66a48ed9873be894de20165d2e`

## Current disposition

The finding is `fixed`, not `verified`: the original PR-head parsing failure no
longer reproduces and the legitimate static controls pass, but the generic
finding policy also requires a separately authorized merge and master-only
workflow rerun before final verification. No merge, master change, Framework
candidate publication, gitlink update, or MRTS action occurred.

## History

- `2026-07-23T06:15:15Z` — Initial PR #92 CI exposed the invalid plain scalar.
  This is distinct from FND-PARENT-0048: that finding identifies the missing
  dependency; this one identifies the YAML encoding regression introduced by
  its first corrective implementation.
- `2026-07-23T06:42:32Z` — Final PR #92 head
  `40a419d5b0f599566469060112b7e55dbab05744` completed the exact-head hosted
  check cycle successfully; this finding moved to `fixed` pending the separate
  master-only verification.
