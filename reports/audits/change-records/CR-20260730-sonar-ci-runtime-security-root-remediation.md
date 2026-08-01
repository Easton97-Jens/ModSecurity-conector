# Change Record: Parent CI runtime SonarQube Cloud remediation and verified-root hardening

**Language:** English | [Deutsch](CR-20260730-sonar-ci-runtime-security-root-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-ci-runtime-security-root-remediation` |
| Date (UTC) | `2026-08-01` |
| Base revision | `30f7f58097d8b9659e27c64afde1c394c2f5f308` |
| Goal | Preserve the reviewed CI-runtime remediation in one fresh Parent history that can be verified against the current `master` without replaying an earlier delivery history. |
| Boundary | Parent `ci/runtime/**`, shared Parent `ci/lib/runtime_path_utils.py`, direct Parent tests, this English/German Change Record pair, and their indexes only. No Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, `NOSONAR`, workflow, or direct `master` change is included. |

## Motivation and problem statement

The remediation selected eleven historical, low-risk source-applicable
CI-runtime Code Smell repairs and a verified-runtime-root filesystem hardening
change. The historical selection was based on an earlier master analysis; this
replacement does not claim that analysis, its issue count, or any hosted result
as current evidence. The replacement must be inventoried and verified against
its own exact head.

Previously, both lifecycle case runners resolved a selected
`VERIFIED_RUN_ROOT` before descriptor-based validation and then created
runner-owned artifacts below it. A lower-privileged actor sharing a temporary
parent could precreate a final or ancestor symlink, causing writes, native
oracle output, or child-harness work to occur below an unintended location.

An earlier delivery history is retained separately. It is intentionally not
replayed here: the pull-request range security control evaluates commit
history as well as the final tree. This replacement contains only the reviewed
final content on the current Parent base and asserts no inherited CI, review,
SonarQube Cloud, or delivery result.

## Acceptance criteria

- The selected historical Code Smell repairs remain limited to the reviewed
  source paths; no broader current `ci/runtime` inventory is claimed fixed.
- Case runners preserve `CLI > VERIFIED_RUN_ROOT > fallback` precedence while
  rejecting unsafe roots before runner-owned writes, compiler output, native
  oracle reuse or execution, and child-harness launch.
- Final-root and ancestor-component symlink controls exit `77` before a target
  mutation; a legitimate private root, lexical relative normalization, and
  `--explain` non-materialization remain valid.
- Report layout, command classification, timestamp conversion, result
  filename, terminal-status semantics, and native case metadata retain their
  prior behavior.
- The exact replacement PR head must have zero new SonarQube Cloud issues,
  zero new duplicated lines, and `0.0%` New-Code duplication without weakening
  a scanner, test, Quality Gate, or security control.
- The exact replacement commit range must pass the repository's normal
  redacted pull-request Secret Scanning control.

## Implementation decision and rationale

`prepare_verified_runtime_artifact_root()` centrally selects and lexically
absolutizes the requested root without resolving an input-controlled link. It
then delegates to the existing descriptor-based no-follow owner/mode validator.
The native and verified case runners call that control before materializing a
run directory or performing child work, fail closed with exit `77` on
`ValueError`, and use `ensure_safe_runtime_directory()` for runner-owned
descendants.

The narrow maintainability changes give repeated immutable strings private
owners or flatten the exact terminal-status conditional. They preserve bytes,
ordering, command construction, report tables, timestamps, and return mapping.

## Alternatives considered

Replaying the earlier branch, resolving input paths before validation,
suppression, `NOSONAR`, Quality-Gate changes, or scanner changes were rejected.
They would either preserve the old history-bound control failure, follow a
preseeded link, or replace a repair with an unverified exception.

## Changed files

- `ci/lib/runtime_path_utils.py`
- `ci/runtime/lifecycle/collect-no-crs-source.py`
- `ci/runtime/lifecycle/run-native-case-comparison.py`
- `ci/runtime/lifecycle/run-verified-case.py`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `tests/test_collect_no_crs_source.py`
- `tests/test_runtime_artifact_utils.py`
- `tests/test_runtime_path_security.py`
- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-security-root-remediation.md`
- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-security-root-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <repository-venv>/bin/python -m py_compile` for the five changed production files and three changed tests | passed. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-root>/tmp <repository-venv>/bin/python -m unittest -q tests.test_runtime_artifact_utils tests.test_runtime_path_security` | passed: 26 tests in 2.395s. |
| Focused `importlib` terminal-status procedure for `collect-no-crs-source.py` with seven JSONL source statuses | passed: all seven retained their expected canonical status. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-root>/tmp <repository-venv>/bin/python -m unittest -q tests.test_collect_no_crs_source` | `blocked_missing_local_checkout`: import requires the intentionally absent Parent-pinned Framework file `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`; Framework/MRTS was not initialized or changed. |
| `rtk proxy -- git diff --check` and exact content comparison of the eight source/test paths with the reviewed final remediation tree | passed. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <repository-venv>/bin/python ci/checks/documentation/check-bilingual-docs.py` | `blocked_missing_local_checkout`: no new Change Record or changed-file diagnostic; only pre-existing links into the intentionally absent Parent-pinned Framework checkout are missing. |
| Exact replacement-head GitHub Actions, pull-request Secret Scanning, review, SonarQube Cloud, and master integration | not run: no replacement PR exists at record authoring. |

## Security impact

The changed boundary accepts a CLI argument or `VERIFIED_RUN_ROOT` environment
value and controls runner-owned directories, logs, compiled native-oracle
output, JSON artifacts, and child-harness work. The descriptor-based
no-follow, owner, and mode checks are the closest control before those sinks.
The direct negative controls must show that a final or ancestor symlink is
rejected before side effects, while a private legitimate root remains usable.

The replacement does not change the Secret Scanning workflow, Gitleaks
provisioning/lock record, Quality Gate, exclusions, suppressions, or any
credential. A successful exact-range scan is required before integration; no
scanner output, detector match, or secret-like value is recorded here.

This change does not claim to secure unrelated caller-owned `--build-root`,
`--tmp-root`, native `--output-dir`, connector/framework roots, a same-UID
attacker able to modify an already-private root, or a live cross-user race.

## Compatibility and generated artifacts

No generated artifact is committed. The intentional compatibility change is to
reject unsafe or symlinked verified roots rather than resolve them; trusted
private absolute roots and documented precedence remain usable.

## Documentation status

The paired English/German Change Record and indexes retain the navigation entry.
The bilingual documentation check found no new Change Record or changed-file
diagnostic; it is blocked only by links into the intentionally absent
Parent-pinned Framework checkout.

## Runtime evidence

No connector matrix, host preparation, package installation, generated-report
refresh, networked preparation, production deployment, or live cross-user
race is claimed. Focused runtime evidence is reported only after the
replacement commands have been run.

## Known limitations

Framework/MRTS source, Gitlinks, workflows, scanner configuration, external
Sonar issue state, and `master` are outside the source scope. A Framework-
dependent test or repository-wide documentation target may remain blocked by
the intentionally uninitialized Parent-pinned Framework checkout; that status
was reproduced for the complete collector module and is recorded above.

## Remaining risks

The replacement preserves a bounded selected repair set; it does not claim to
eliminate the broader current `ci/runtime` SonarQube Cloud inventory. The
fresh range Secret Scan, exact-head hosted checks, review, SonarQube Cloud
result, and mergeability remain independent delivery gates.

## Checks not run and rationale

- The complete Framework-dependent collector module cannot import until the
  Parent-pinned Framework checkout is present; initializing or modifying it is
  outside the authorized Parent-only scope.
- The full connector/runtime matrix, host preparation, package installation,
  generated-report refresh, networked checks, and live cross-user race were
  not run because they exceed the focused source/contract scope.
- Hosted checks, review, SonarQube Cloud, pull-request Secret Scanning, and
  integration require the eventual exact replacement PR head and are not
  inferred locally.

## Delivery status

At authoring, the fresh local branch is based on
`30f7f58097d8b9659e27c64afde1c394c2f5f308`. No replacement-PR hosted check,
review, SonarQube Cloud analysis, or master integration is claimed. Before a
protected merge, the final local, remote, and PR head must match; required
checks, the fresh range Secret Scan, review state, SonarQube Cloud result, and
mergeability must be observed for that exact head.

## Final diff and review status

The intended replacement diff is the final reviewed runtime-root hardening and
bounded maintainability repair tree, reconstructed on current `master` rather
than copied as historical commits. It requires a fresh focused security review,
local regression evidence, documentation validation, and hosted exact-head
verification before a delivery claim can be made.
