# Change Record: CI security hardening

**Language:** English | [Deutsch](CR-20260716-ci-security-hardening.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260716-ci-security-hardening` |
| Date (UTC) | `2026-07-16` |
| Base revision | `c8450a9feaef3da9c999586ea60398653601f037` |
| Boundary | Parent CI, documentation, and traceability only; Framework and MRTS unchanged. |

## Motivation and problem statement

The repository used mutable GitHub Action tags and lacked a clean, documented
general CI-security baseline. The legacy security PR mixed this useful scope
with repository-owned Codex agents, skills, hooks, extension contracts, and
historical records that are intentionally not adopted.

## Acceptance criteria

- All remote GitHub Actions workflow references use recorded immutable SHAs.
- Workflow linting, redacted PR-range secret scanning, advisory full-history
  scanning, exact-SHA OSV comparison, bounded CodeQL, and trust-bounded
  Scorecard workflows are present.
- Go modules use fixed Go `1.24.0`; C/C++ CodeQL scope is stated as bounded.
- Tool provenance, checksums, licenses, and minimum permissions are recorded.
- English/German documentation and this Change Record describe only the
  retained general CI-security scope.

## Implementation decision and rationale

Use checksum-verified official release binaries for `actionlint`, `zizmor`,
and Gitleaks instead of repository-owned Codex tooling. Pin GitHub Actions to
official tag commits and maintain the provenance record. OSV compares the
event's exact base and head SHAs and makes no dependency change. Full-history
Gitleaks and scheduled OSV are advisory until historical findings are triaged.

## Changed files

Changed files are limited to Parent `.github/workflows/`, generic CI security
tooling and fixtures, focused CI-security tests/Make target, English/German
CI-security and audit documentation, and this Change Record pair. No
`.agents/**`, Codex skill, agent, hook-policy, extension-contract, Framework,
MRTS, or gitlink file is changed.

## Commands executed

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` | passed: 5 focused static tests and all three downloaded-binary lock records validated. |
| `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | passed. |
| `PYTHONDONTWRITEBYTECODE=1 make check-doc-links` | passed, including the Framework documentation-link checker. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile ci/tools/fetch_security_tool.py tests/test_ci_security_workflows.py` | passed. |
| Checksum-verified `actionlint` with the available ShellCheck binary over all workflow files | passed. |
| Checksum-verified `zizmor --offline .github/workflows` | passed: no findings (the upstream baseline reports 77 configured suppressions). |
| `zizmor` safe and deliberately insecure fixtures | passed: safe fixture accepted; insecure fixture rejected as expected. |
| Checksum-verified Gitleaks over `c8450a9feaef3da9c999586ea60398653601f037..HEAD` with redaction | passed: one commit scanned; no leaks found. |
| `git diff --check` | passed. |

The locally downloaded validation binaries were obtained only through the
checksum-verifying fetch helper in the registered task-owned temporary store.
The required GitHub workflow validation still applies to the exact replacement
PR head SHA.

## Security impact

The retained scope introduces read-minimized CI analysis only. It enables no
automatic dependency remediation, branch-protection modification, merge,
review bypass, or fork-head execution. Tool downloads verify a recorded
SHA-256 before extraction and the workflow documentation states remaining
scope and trust limitations.

## Runtime evidence

Not applicable. This change does not modify connector code or establish
HTTP/1.1, HTTP/2, HTTP/3, CRS, MRTS, or host-runtime evidence.

## Known limitations

CodeQL C/C++ analysis is limited to reproducible common-helper C17 checks.
Fork pull requests do not run Scorecard against an untrusted head. Gitleaks
full-history and scheduled OSV scans are advisory pending historical triage.

## Remaining risks

SHA pins do not remove risks in downstream action runtime dependencies or
container images. Static and dependency scanners can miss unavailable,
unreachable, or non-source risks; their result remains scoped evidence.

## Checks not run and rationale

No connector build, runtime, protocol, sanitizer, full CRS/MRTS matrix, or
dependency update is run because this is CI-security infrastructure. Required
replacement-PR GitHub checks, reviews, and SonarQube evidence are collected
only for the exact final PR head SHA.

## Final diff and review status

Focused local validation and scoped-diff review passed. Exact-SHA draft-PR
verification, review, and SonarQube disposition remain pending. Legacy PR #44
checks are not evidence for this record.
