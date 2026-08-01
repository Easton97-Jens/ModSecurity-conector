# FND-FRAMEWORK-0052 — Framework PR #42 CPython 3.14 Pyright rejects two test-fixture annotations

## Identity

| Field | Value |
| --- | --- |
| Category | ci_failure |
| Repository / ownership | framework / framework |
| Priority / severity / confidence | P1 / not_applicable / confirmed |
| Status / feasibility | verified / already_fixed |
| Release blocker / security relevant | false / false |
| Historical failed revision | f2f77336e57e9ce6b20af0f8b128c4bb1b062e1c |
| Exact fixed revision | 2930e04e1558b5b10bdeb87a76abb077a2085566 |
| Exact verified Framework master | 935cf14c676a24672be5c336e92cd13457cc35c8 |
| Pull request / check | #42 / python-ci-security-quality |

## Summary

Historical Framework PR #42 head f2f77336e57e9ce6b20af0f8b128c4bb1b062e1c
failed GitHub Actions Python-quality run 29961019802, job 89061788219, while
hosted CPython 3.14.6 ran the pinned Pyright command. The retained receipt
records exactly two test-fixture diagnostics: urllib.error.HTTPError requires
Message[str, str] headers rather than an untyped empty dict, and an inferred
dict[str, str] cannot be mixed with dict[str, object] because dictionaries are
invariant.

The focused test-only correction is now in exact PR head
2930e04e1558b5b10bdeb87a76abb077a2085566. Its hosted CPython 3.14.6
Python-quality run 29962792445/job 89067507532 passes the pinned Pyright
phase, current OSV and SonarQube Cloud checks pass, and no review or inline
comment remains. The retained verification receipt is
framework-pr42-2930e04-hosted-verification.md, SHA-256
4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.

This historical P1 non-security CI blocker is distinct from the earlier OSV,
Ruff, and five-diagnostic Pyright findings. PR #42 was normally merged at
2026-07-23T07:41:13Z, and exact resulting Framework master
935cf14c676a24672be5c336e92cd13457cc35c8 has bound CI security Python quality
workflow run 29989195066 completed `success`. Its tree
5df6cce7d7385a041a817ff54fae777902645f1d equals the reviewed PR-head tree.
The retained postmerge receipt is framework-pr42-20260723-postmerge-
verification.md, SHA-256
0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1.
The original Pyright CI failure is therefore verified, not closed.

## Observed and expected behavior

The historical Python-quality workflow reached its pinned Pyright phase and failed
with exactly two errors at tests/ci_security/test_update_python_version.py:224
and :255. The job reported no updater runtime, workflow, dependency, OSV,
permission, token, or security-control failure.

The existing pinned Pyright command must complete under hosted CPython 3.14.6
with the repository type-quality configuration unchanged. The fixtures must
accurately model standard-library HTTPError headers and heterogeneous release
records without changing updater behavior.

## Impact, root cause, and remediation

The historical f2 PR head could not satisfy a required Python-quality gate. The fixtures
are behaviorally sufficient but incompletely typed for the pinned Pyright
standard-library contract: HTTPError hdrs is Message[str, str], and Python
dictionaries are invariant. The product updater and CI configuration are not
the failing boundary.

The focused correction constructs Message[str, str] for the HTTPError fixture
headers and annotates the heterogeneous fixture record as dict[str, object].
It changes no updater code, Pyright/Ruff configuration, dependency, workflow
permission, suppression, Quality Gate, or security control.

The exact resulting-master Python-quality workflow now succeeds, so this
repaired non-security defect is no longer a release blocker. This does not
weaken any static-analysis, formatter, workflow, test, security, or
quality-gate control.

## Evidence and reproduction

| Field | Value |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-f2-hosted-pyright-failure.md |
| Artifact type | task_owned_framework_pr42_f2_hosted_pyright_failure_receipt |
| SHA-256 | 519327a8a07a13ba70a4679577d31a792238a949d3f7ea6d44270e23ed903050 |
| Producer command | node "$TOOLS_DIR/pyright/index.js" --project pyrightconfig.json |
| Working directory | GitHub Actions hosted runner for Framework PR #42 |
| Exit code / observed at | 1 / 2026-07-22T21:55:59Z |
| Retention status | task_owned_retained_evidence |

Reproduce by inspecting GitHub Actions run 29961019802/job 89061788219 for
exact head f2f77336e57e9ce6b20af0f8b128c4bb1b062e1c, verifying the retained
receipt hash, then running the repository pinned Pyright command in the hosted
workflow or an equivalently provisioned Framework tool environment after the
focused follow-up is submitted.

### Resulting-master evidence

| Field | Value |
| --- | --- |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md |
| Artifact type | task_owned_framework_pr42_resulting_master_verification_receipt |
| SHA-256 | 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1 |
| Commands | RTK-wrapped GitHub PR/ref/commit/workflow/check-suite, SonarQube Cloud, and boundary-state readback; exact commands are retained in the receipt |
| Working directory / exit code / observed at | /root/git/ModSecurity-conector / 0 / 2026-07-23T07:51:09Z |
| Retention status | task_owned_retained_evidence |

The receipt records the normal `merge` of PR #42, exact master
935cf14c676a24672be5c336e92cd13457cc35c8, and successful CI security Python
quality workflow run 29989195066. It is the resulting-master evidence for the
verified transition; it does not claim separate SonarQube or Cloudflare
delivery conditions are passing.

## Acceptance criteria and validation plan

1. Only tests/ci_security/test_update_python_version.py changes, and existing
   runtime assertions retain their behavior.
2. Focused Ruff lint, Ruff format check, the direct unittest module, and make
   test-ci-security-contract pass without a Pyright/Ruff/workflow/control
   change.
3. Exact PR #42 head 2930e04e1558b5b10bdeb87a76abb077a2085566 passes hosted
   python-ci-security-quality, including pinned Pyright under CPython 3.14.6;
   historical run 29961019802 is not replacement evidence.
4. Current exact-head OSV and SonarQube Cloud results are reread with the
   remaining required PR checks before verified_pr is considered.
5. PR #42 is normally merged and exact resulting-master evidence records a
   successful CI security Python quality workflow before this finding is
   verified; no Parent gitlink or MRTS change occurs. Closure is outside this
   update's scope.

The validation sequence is one-file diff/whitespace review; focused
repository-native Ruff, unittest, and contract checks; explicit one-file
commit/push plus SHA equality; then a fresh hosted Pyright result and complete
current-head PR recheck.

## Regression and legitimate-control tests

Regression tests:

- python -m unittest tests.ci_security.test_update_python_version -v
- ruff check tests/ci_security/test_update_python_version.py
- ruff format --check tests/ci_security/test_update_python_version.py
- make test-ci-security-contract
- GitHub Actions python-ci-security-quality on the new exact PR #42 head

Legitimate controls:

- The HTTPError fixture still exercises the updater HTTP 404 path with typed
  empty Message headers.
- The unrelated Python 3.13 record remains excluded before release-flag
  evaluation while the heterogeneous fixture is type-safe.
- Hosted Pyright, OSV, and SonarQube Cloud controls remain enabled.

## Dependencies, blockers, related findings, and residual risk

- Dependencies: none for this verified finding; closure is intentionally out
  of scope for this update.
- Blockers: none for this repaired Pyright defect.
- Related findings: FND-FRAMEWORK-0046, FND-FRAMEWORK-0049,
  FND-FRAMEWORK-0051, FND-SONAR-0002, and FND-GITHUB-0007.

No risk is accepted for this Pyright defect. The successful resulting-master
Python-quality workflow verifies the original failure. FND-SONAR-0002 and
FND-GITHUB-0007 are separate accepted PR #42 delivery limitations; their global
records remain separately blocked, and neither limitation blocks, closes, or
otherwise alters this repaired finding. No static-analysis, formatter,
workflow, dependency, test, security, or Quality Gate control may be weakened
to obtain a pass.

## History

- 2026-07-23T07:51:09Z — framework_pr42_resulting_master_pyright_verified:
  PR #42 was normally merged at 2026-07-23T07:41:13Z. Exact resulting Framework
  master 935cf14c676a24672be5c336e92cd13457cc35c8, whose tree
  5df6cce7d7385a041a817ff54fae777902645f1d equals the reviewed PR-head tree,
  has successful CI security Python quality run 29989195066. Retained postmerge
  verification receipt SHA-256 is
  0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1.
  FND-SONAR-0002 and FND-GITHUB-0007 remain separate accepted PR #42 delivery
  limitations and do not block this repaired Pyright defect.
- 2026-07-22T22:35:46Z — framework_pr42_2930_exact_head_pyright_fixed:
  exact head 2930e04e1558b5b10bdeb87a76abb077a2085566 passed hosted CPython
  3.14.6 pinned Pyright in run 29962792445/job 89067507532. The retained
  receipt SHA-256 is
  4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.
  Status is fixed only; no master merge, resulting-master evidence, Parent
  gitlink action, or MRTS action occurred.
- 2026-07-22T22:08:40Z — framework_pr42_f2_hosted_pyright_fixture_failure_tracked:
  allocated after deduplication as a distinct CI failure. Exact PR #42 head
  f2f77336e57e9ce6b20af0f8b128c4bb1b062e1c failed run 29961019802/job
  89061788219 with exactly two test-fixture type diagnostics under hosted
  CPython 3.14.6. The task-owned source correction is uncommitted; no hosted
  success, merge, Parent action, or MRTS action is claimed.
