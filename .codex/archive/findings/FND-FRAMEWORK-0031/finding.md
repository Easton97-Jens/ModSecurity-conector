# FND-FRAMEWORK-0031 — Flow-sequence action-pin bypass

- **Status:** verified on resulting Framework master — Cloud revalidation pending
- **Severity / priority:** high / P1
- **Cloud finding:** `48ddc89c01548191aac6fdc953d4a69b` (`new` in the supplied export)
- **Affected Framework revision:** `784977615acfc55567e37b863309abc4a38ac877`

## Root cause and impact

`flow_mapping_uses_values()` starts action extraction after `{` or a comma in
a braced mapping, but not after `[`. A valid `steps: [uses:
actions/setup-python@v6]` flow sequence consequently does not reach the full
SHA enforcement check. A pull request could use mutable external Actions
despite the immutable-pin security gate.

## Remediation and proof

Framework PR [#38](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/38)
at `8907c8ec047df070a579fab926e25b0d94dfbc2e` recognizes flow-sequence
mapping entries after `[` and contains negative mutable-tag/alternate-comma
and positive full-SHA tests. The original negative case failed before the
correction; afterward the focused suite passed (25 tests), alongside the
direct real-workflow pin check, Python compilation, Change Record,
bilingual-documentation, documentation-link, and diff checks.

All applicable GitHub checks for that exact head passed, including CodeQL for
actions/c-cpp/python, secret scanning, OSV, OpenSSF Scorecard, workflow
security quality, and the SonarQube Cloud Quality Gate (zero new issues and
zero security hotspots). The PR is ready for review with no review request or
unresolved review thread. PR #38 then merged, with exact merge commit
`9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b`. GitHub reports its resulting
master tree as `4a91bfc7c47efef3b8e44d993e8f4ab1ed5a8cbc`, identical to the
reviewed PR-head tree; the original negative and full-SHA legitimate-control
tests pass against that tree. The resulting-master Actions and CodeQL checks
also pass.

The master-only SonarQube Cloud result still fails on the pre-existing
Security Rating on New Code E condition. It is separately tracked as
`FND-SONAR-0002`, is not attributed to this change, and prevents aggregate
master-integration completion without its own remediation or risk decision.
The Cloud finding is deliberately not closed: it remains `new` until an exact
merged-master Codex Cloud scan is available. Parent and MRTS remain out of
scope and unchanged.

The Parent remains uncommitted and still records Framework
`784977615acfc55567e37b863309abc4a38ac877`. Its local submodule working tree
temporarily reports a revision mismatch because the Framework checkout advanced
to the merge result. The required non-forcing restoration to the Parent-recorded
commit is currently blocked by the sandbox refusing the Framework `index.lock`
write; no forced checkout or Parent pointer update was attempted.

The source export is
`.codex/findings/codex-security-findings-2026-07-20T17-18-10.034Z.csv`
(SHA-256 `4836e7d8a1aba6088f1d125e7f48dd2cb333c2e7d4c1d19117d911c0aad45daf`).
The full dependency-backed local permission/lint suite is not run because the
Framework-owned CPython 3.13.14 environment is absent; the exact-head GitHub
CI completed successfully instead.
