# Change Record

**Language:** English | [Deutsch](CR-20260809-update-submodules-run-37.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260809-update-submodules-run-37 |
| Date (UTC) | 2026-08-09 |
| Base revision | 128a2f63f182758b1c1a1d4746f5e56f609d245d |

## Motivation and problem statement

GitHub Actions Update submodules Run #37, ID 31307156102, failed after its
resolver moved Parent gitlink 3a8074e0b7ef698b941e7649b8a86e639f838a0c to
Framework candidate 4c9af1cee72caa0107fa011e59eef9e853338cf5. Resolver job
93229208675 passed. Validator job 93229238042 detached the candidate and
started make quick-check; its first real failure was
test_haproxy_prepare_does_not_rebuild_a_verified_runtime_binary at
tests/test_prepare_runtime_components.py:1254 with AssertionError: True is not
false. Two related cache-reuse failures followed, make exited 2, and publisher
job 93229465918 was skipped with no commit, push, or pull-request mutation.

This was category C, Parent/Framework compatibility: the Parent test fixture
encoded the former real HAProxy provenance 3.2.21 and
0cb8818a26c5f888e0cb1c40f1b3acb9fb952527d1733f769ce688fedd680339 but did
not pass it as test input. Candidate 4c9af1c correctly defaults to HAProxy
3.2.22 and afca3a26d573df53d0e1fc475dcd743ec5875e038e1476c80e871d70228ca2da,
detects stale provenance, rebuilds, and invalidates a reuse assertion. It was
not a resolver, checkout, publisher, or GitHub-permission failure.

## Acceptance criteria

- The fixture uses atomic synthetic baseline and target version/digest tuples;
  it never treats a real current Framework production pin as a unit-test
  prerequisite.
- A synthetic future tuple proves verified binary reuse without a download or
  rebuild, while the separate BUILD_ROOT exit-77 negative control remains.
- Candidate validation remains read-only and mandatory make quick-check runs
  before the write-capable publisher can become eligible.
- The publisher re-resolves the candidate and current Parent master gitlink,
  permits only the Framework gitlink, and fails closed for stale, malformed,
  foreign, auto-merge, or ambiguous maintenance state.
- State A creates a branch normally; proven state B updates one marked Draft PR
  through a SHA-bound lease; proven state C reuses only a verified merged
  updater branch through the same explicit lease; every other state fails.
- The always-run read-only result job treats a resolver success plus
  changed=false and skipped validator/publisher as success, but keeps unknown
  output and validator/publisher failures red.

## Implementation decision and rationale

The Parent cache-fixture helper now supplies synthetic HAPROXY_VERSION,
HAPROXY_SOURCE_URL, HAPROXY_SHA256_URL, HAPROXY_SHA256, and matching source
directory values. Baseline 3.2.9000/a*64 and target 3.2.9001/b*64 are test-only
values, passed atomically through the existing environment seam. No Framework
shell file is sourced, parsed, or evaluated to obtain a value. A future-tuple
test verifies the intended reuse behavior.

The workflow retains resolver, validator, and publisher separation and adds an
always-run read-only outcome job. Resolver validates exactly one official
reference and the current gitlink. Validator checks candidate ancestry, official
origin, detached recursive cleanliness, and mandatory make quick-check.

Before any publisher commit/push, current Framework master and Parent master
are read again; a moved Parent gitlink fails rather than publishing a stale
transition. The publisher constructs exactly one mode-160000 gitlink change
from current master with commit-tree and rejects every other staged path. It
uses normal push only for absent branch state A and
--force-with-lease=refs/heads/chore/update-submodules:EXPECTED_REMOTE_HEAD only
for proven state B or C. It does not delete a branch, use a general force
push, enable auto-merge, or use a PAT, SSH, or deploy-key fallback.

The current remote chore/update-submodules state was C-like:
fd7e63d7994fd9322c5bbb7862ef283d436c88d5 is the head of merged PR #258 and
there is no open matching PR. Its old body lacks the new marker, so the
workflow rechecks its actual metadata/history at execution time rather than
trusting this observation.

## Changed files

- .github/workflows/update-submodules.yml
- tests/test_prepare_runtime_components.py
- tests/test_ci_security_workflows.py
- reports/audits/change-records/CR-20260809-update-submodules-run-37.md
- reports/audits/change-records/CR-20260809-update-submodules-run-37.de.md

No Framework source, MRTS source, Parent Gitlink, .gitmodules file, generator,
or generated documentation changed.

## Commands executed

The detached pre-fix reproduction used Parent
83094eb659f0b5df8c2df30b1ae718d524a9adf0 and candidate
4c9af1cee72caa0107fa011e59eef9e853338cf5. Its supporting local CPython 3.14.4
and PyYAML 6.0.3 run reproduced the same first three failures and exit 2;
hosted CPython 3.14.6 Run #37 evidence is authoritative.

Post-fix checks passed in the task worktree against the same candidate:

- focused five managed-cache tests, including the synthetic future tuple and
  separate BUILD_ROOT control;
- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_ci_security_workflows, 24 tests;
- make check-ci-security-contract, including local immutable security-tool lock
  validation;
- workflow YAML parse and Bash syntax checks;
- candidate-bound make quick-check, including 96 core tests and its remaining
  repository checks;
- actionlint with ShellCheck and zizmor offline plus its safe/unsafe fixtures.

The initial check-python-version-contract run failed only at pre-existing
inventory entries unrelated to update-submodules; it did not report this
workflow. It is recorded as a baseline limitation, not a waived failure.

## Security impact

make quick-check remains mandatory in the contents-read validator, whose
checkout disables persisted credentials and has no GH_TOKEN or secrets
reference. The contents-write/pull-requests-write publisher is a fresh
non-recursive checkout and does not run quick-check or a Framework submodule
command. Candidate SHA validation, official URL checks, ancestry checks,
pre-publish re-resolution, no stale-master transition, exact index/raw-diff
validation, explicit B/C leases, PR marker/draft/author/auto-merge checks, and
post-push head re-read reduce TOCTOU and foreign-branch overwrite risk.

The required quick-check necessarily exercises reviewed candidate code in the
isolated read-only validation boundary. This record claims no new Framework
shell sourcing, parser, command substitution, or publisher-side Framework
execution to obtain versions.

## Runtime evidence

The portable authoritative source is [GitHub Actions Run #37](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31307156102)
and the resolver, validator, and publisher job IDs named above. A secret-free
local corroborating summary is sealed for FND-PARENT-0114 with SHA-256
335cbf19594d0c17b29820d7b09920e0e1e48ef0c08c30acc7d551210bbd100b; it records
resolver success, candidate/current SHA, validator failure, make quick-check
start, first error, follow-on errors, exit 2, and skipped publisher. It is not
versioned product or delivery proof. No raw GitHub log is copied into this
record.

Each post-fix result above names the native command and its observed outcome
against this task worktree. Raw local stdout is intentionally not treated as
delivery evidence; exact-head PR checks, CI security checks, Sonar Quality Gate,
and review evidence remain required and are explicitly pending below.

## Known limitations

The local environment has CPython 3.14.4 while the workflow declares 3.14.6;
the exact hosted Run #37 is the patch-version authority. Static tests and
read-only state inspection cannot execute GitHub scheduler expressions, a
GitHub token, branch-protection behavior, concurrent remote races, or an actual
later Framework update. The task is explicitly forbidden to merge this PR or
dispatch the post-merge master workflow.

## Remaining risks

GitHub state may change between REST reads and the next action. The workflow
rechecks state and binds B/C pushes to the observed remote SHA, but no local
test can make a multi-service branch/PR operation globally atomic. A failed
candidate quick-check, stale candidate, moved master gitlink, lease failure,
foreign state, PR-creation race, token configuration error, or Hosted check
failure remains fail closed and must not create a fallback or auto-merge.

## Checks not run and rationale

At this record stage, final exact-head hosted checks, CodeQL, CI Security,
actionlint, zizmor, SonarQube Cloud Quality Gate, review-thread state, and
branch-protection state are pending the authorized normal push and exactly one
Draft PR. The later master workflow run is intentionally not dispatched. The
local exact CPython 3.14.6 reproduction is unavailable.

## Final diff and review status

The intended diff is Parent-only: test fixture de-coupling, updater workflow
hardening/result reporting, focused static contracts, and this bilingual Change
Record. It contains no Framework/MRTS source change, Gitlink change, .gitmodules
change, general force push, fallback credential, token expansion, Quality Gate
weakening, suppression, or auto-merge. Final exact-path staging, normal commit,
normal push, one Draft PR, and current-head hosted/sonar/review verification
remain required before delivery is complete.

## Framework-pin drift audit

| Component | Framework source | Parent hits classified | Quick-check relevance | Correction |
| --- | --- | --- | --- | --- |
| HAProxy | ci/lib/common.sh defaults | Runtime-cache test fixture was causal | yes | Synthetic atomic fixture tuples |
| NGINX | Framework provider/configuration | Parent forwarding or non-runtime references | no causal duplicate | None |
| Apache httpd | Framework provider/configuration | Documentation/generator literals only | no causal duplicate | None |
| APR | Framework provider/configuration | Documentation/reference material only | no causal duplicate | None |
| APR-util | Framework provider/configuration | Documentation/reference material only | no causal duplicate | None |
| PCRE2 | Framework provider/configuration | Parent forwarding/reference material | no causal duplicate | None |
| CRS | Framework provider/configuration | Documentation/reference material | no direct fixture | None |
| ModSecurity v3 | Framework provider/configuration | Test/reference material, not this fixture | no causal duplicate | None |
| Traefik | Framework/provider metadata | Documentation metadata only | no causal duplicate | None |
| Envoy | Framework/provider metadata | Documentation metadata only | no causal duplicate | None |
| lighttpd | Framework/provider metadata | Documentation metadata only | no causal duplicate | None |
