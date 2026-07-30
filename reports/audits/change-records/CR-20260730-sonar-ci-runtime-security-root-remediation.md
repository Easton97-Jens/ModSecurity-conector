# Change Record: Parent CI runtime SonarQube Cloud remediation and verified-root hardening

**Language:** English | [Deutsch](CR-20260730-sonar-ci-runtime-security-root-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-ci-runtime-security-root-remediation` |
| Date (UTC) | `2026-07-30` |
| Base revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | Selected current SonarQube Cloud Code Smell keys: `AZ9cRyd3HhV2CayPTPxL`, `AZ9cRyd3HhV2CayPTPxM`, `AZ7b3dfYcO69wzd-_jHf`, `AZ7b3dfYcO69wzd-_jHg`, `AZ9cRydQHhV2CayPTPxF`, `AZ7b3diDcO69wzd-_jHy`, `AZ7TenozHrNUCHtbhYSE`, `AZ7RRan5GxvN3xmvwZcC`, `AZ7RRan5GxvN3xmvwZcE`, `AZ7RRan5GxvN3xmvwZcD`, and `AZ7RRan5GxvN3xmvwZcB`; security remediation `FND-PARENT-0074`; aggregate Sonar tracking `FND-SONAR-0016`. |
| Boundary | Parent `ci/runtime/**`, shared Parent `ci/lib/runtime_path_utils.py`, direct Parent tests, this English/German Change Record pair, and paired Change Record indexes only. No `.github/`, `scripts/`, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, `NOSONAR`, workflow, or `master` change is included. |

## Motivation and problem statement

The current master analysis `43a50e20-8bdd-453a-bc44-549a7e3d7588` is bound
to `caddd86d1eede95de53aa1bc971dd26d875df21c` and reports 78 open findings
under `ci/runtime`: three scanner-labelled anchors in `common` and 75 in
`lifecycle`. This record deliberately fixes only the 11 current, low-risk,
source-applicable Code Smell keys listed above. The scanner-labelled `common`
anchors are already-safe rule leads, higher-risk orchestration candidates lack
a safe one-PR proof, and an active independent PR owns
`AZ9cRycZHhV2CayPTPw4`; none is suppressed, marked false-positive, or claimed
fixed here.

Source-to-sink review also found that both lifecycle case runners applied
`Path(...).resolve()` to selected `VERIFIED_RUN_ROOT` input before artifact
directory creation. A lower-privileged actor sharing a sticky temporary parent
could preseed a final or ancestor symlink and redirect runner-owned writes.
The native case runner could then compile, reuse, or execute a fixed-name
oracle below the redirected tree. This bounded local filesystem-integrity
defect is separately tracked as `FND-PARENT-0074`.

## Acceptance criteria

- The selected 11 Code Smell keys receive the smallest behavior-preserving
  source changes; no other current `ci/runtime` finding is claimed remediated.
- Case runners preserve `CLI > VERIFIED_RUN_ROOT > fallback` precedence while
  rejecting unsafe roots before runner-owned writes, compiler output, native
  oracle reuse/execution, or child-harness launch.
- Final-root and parent-component symlink controls exit `77` without mutating
  a target; a legitimate private root, relative lexical normalization, and
  `--explain` non-materialization remain valid.
- Existing report layout, full-matrix command classification, timestamp
  parsing, case-result filename, terminal statuses, and native case metadata
  retain their prior semantics.
- The exact PR head must receive zero new SonarQube Cloud issues, zero new
  duplicated lines, and `0.0%` New-Code duplication without weakening a
  scanner, Quality Gate, test, or security control.

## Implementation decision and rationale

`prepare_verified_runtime_artifact_root()` centralizes selection in
`ci/lib/runtime_path_utils.py`. It lexically makes a path absolute without
resolving an input-controlled link, then delegates to the existing
descriptor-based no-follow owner/mode validator. Both case runners call it
before directory materialization or child work, fail closed with exit `77` on
`ValueError`, and create runner-owned case, log, and native-oracle directories
with `ensure_safe_runtime_directory()`.

The narrow Sonar changes only give repeated immutable strings private owners
or flatten the exact terminal-status conditional. They preserve original bytes,
ordering, command construction, report tables, timestamps, and return mapping.

## Alternatives considered

Resolving a selected root before validation was rejected because it follows a
preseeded symlink before no-follow inspection. A lexical check alone was
rejected because it cannot close an existing final or ancestor symlink.
Suppressions, `NOSONAR`, Quality Gate/rule changes, and external false-positive
actions were rejected because they do not repair the source boundary or prove
the required exact-head quality result.

Higher-risk complexity, Unicode, regular-expression, and runner-orchestration
findings remain unchanged because a behavior-preserving one-PR remediation was
not proven. The independent active-PR key `AZ9cRycZHhV2CayPTPw4` is outside
this diff.

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
| Manual revision-bound SonarQube Cloud API inventory procedure retained in the task plan | passed: analysis `43a50e20-8bdd-453a-bc44-549a7e3d7588` matches base `caddd86d1eede95de53aa1bc971dd26d875df21c`; the selected 11 keys and independent active-PR key were recorded. |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile ci/lib/runtime_path_utils.py ci/runtime/lifecycle/collect-no-crs-source.py ci/runtime/lifecycle/run-native-case-comparison.py ci/runtime/lifecycle/run-verified-case.py ci/runtime/lifecycle/run-verified-report-run.py tests/test_collect_no_crs_source.py tests/test_runtime_artifact_utils.py tests/test_runtime_path_security.py` | passed: the five changed production files and three changed tests compile. |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_runtime_artifact_utils tests.test_runtime_path_security tests.test_generated_report_evidence_integrity` | passed: 102 tests in 15.050s. |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_runtime_artifact_utils tests.test_runtime_path_security` | passed: 26 tests in 2.440s after the final legitimate broad-root rejection regression. |
| Manual terminal-status JSONL procedure retained in `FND-PARENT-0074` local receipt | passed: `NOT_EXECUTABLE`, `SKIPPED`, `BLOCKED`, `UNSUPPORTED`, `NOT_APPLICABLE`, `NOT_EXECUTED`, and `PASS` each exit `0`. |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_collect_no_crs_source.CollectNoCrsSourceTest.test_explicit_terminal_statuses_keep_their_existing_precedence` | `blocked_missing_local_checkout`: import stops at missing `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`; Framework/MRTS was not initialized or changed. |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_runtime_path_security.RuntimePathSecurityTest.test_case_runners_reject_symlinked_verified_roots_before_runtime_actions tests.test_runtime_path_security.RuntimePathSecurityTest.test_precreated_verified_runtime_root_symlink_is_rejected tests.test_runtime_path_security.RuntimePathSecurityTest.test_verified_case_explain_does_not_materialize_a_runtime_root` | passed: 3 tests in 0.090s; final-root and parent-component controls exit `77` before observed target mutation, artifact output, compiler output, or harness launch. |
| Manual Codex Security `security-diff-scan` procedure, report range `caddd86d1eede95de53aa1bc971dd26d875df21c...working-tree`, retained under `FND-PARENT-0074` | passed: all eight changed source/test rows were fully reviewed; no reportable diff-introduced security finding survived. |
| `rtk proxy -- make check-bilingual-docs` | `blocked_missing_local_checkout`: the new Change Record pair was not reported; diagnostics are the uninitialized Framework link targets plus the task-owned untracked `cleanup-manifest.md` without a German companion. |
| `rtk proxy -- make check-doc-links` | `blocked_missing_local_checkout`: diagnostics are only the uninitialized Framework link targets; no new Change Record link is reported. |
| `rtk proxy -- env VERIFIED_RUN_ROOT=/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/build PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make lint` | `blocked_missing_local_checkout`: POSIX/Bash syntax and all `ci/*.py` compilation passed before `check-no-crs-source-normalization` imports the absent Framework file. |
| `rtk proxy -- git diff --check` after the final Change Record update | passed. |

### Manual procedure details

The public SonarQube Cloud inventory procedure first requests
`https://sonarcloud.io/api/project_analyses/search?project=Easton97-Jens_ModSecurity-conector&branch=master`, selects analysis
`43a50e20-8bdd-453a-bc44-549a7e3d7588`, and confirms its revision equals
`caddd86d1eede95de53aa1bc971dd26d875df21c`. It then requests
`https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&branch=master&statuses=OPEN,CONFIRMED,REOPENED&ps=500`, filters paths below `ci/runtime/`, and compares the returned keys with the eleven Tracking keys and `AZ9cRycZHhV2CayPTPw4`. The procedure is read-only and uses no credential, issue mutation, suppression, or Quality Gate change.

For the terminal-status procedure, a task-owned `cases.jsonl` contains one
`{"case_id":"allow_without_marker","status":SOURCE_STATUS,"actual_status":200,"live_executed":SOURCE_STATUS=="PASS"}` row for each
`SOURCE_STATUS` in `NOT_EXECUTABLE`, `SKIPPED`, `BLOCKED`, `UNSUPPORTED`,
`NOT_APPLICABLE`, `NOT_EXECUTED`, and `PASS`. The procedure calls
`case_observations([source], "nginx", "1100001", {"allow_without_marker": (200, None)})` and compares the returned status with `NOT_EXECUTED`, `NOT_EXECUTED`, `BLOCKED`, `UNSUPPORTED`, `NOT_APPLICABLE`, `NOT_EXECUTED`, and `PASS`, respectively. This exact source-contract procedure is retained in the `FND-PARENT-0074` evidence receipt; its ordinary module test cannot import in this worktree while the Framework Gitlink is intentionally uninitialized.

The manual loader constructs `source` and `collector` without importing the
Framework-dependent test module:

```python
import importlib.util
import json
from pathlib import Path

source = Path("cases.jsonl")
source.write_text(json.dumps({"case_id": "allow_without_marker", "status": SOURCE_STATUS, "actual_status": 200, "live_executed": SOURCE_STATUS == "PASS"}) + "\n", encoding="utf-8")
spec = importlib.util.spec_from_file_location("collect_no_crs_source", Path("ci/runtime/lifecycle/collect-no-crs-source.py"))
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
cases, _ = collector.case_observations([source], "nginx", "1100001", {"allow_without_marker": (200, None)})
```

The procedure repeats the `source.write_text(...)` and
`collector.case_observations(...)` lines once for every listed `SOURCE_STATUS`.

For the Codex Security review, the scan uses base
`caddd86d1eede95de53aa1bc971dd26d875df21c`, restores the exact Git-diff set
`ci/lib/runtime_path_utils.py`, `ci/runtime/lifecycle/collect-no-crs-source.py`,
`ci/runtime/lifecycle/run-native-case-comparison.py`,
`ci/runtime/lifecycle/run-verified-case.py`,
`ci/runtime/lifecycle/run-verified-report-run.py`,
`tests/test_collect_no_crs_source.py`, `tests/test_runtime_artifact_utils.py`,
and `tests/test_runtime_path_security.py` after the generic worklist excludes
`ci/` and `tests/`, then performs full-file source/control/sink and bypass
review for each row. Its sealed manifest SHA-256 is
`f25310a5fd1b2c074d8be405895549c6c3c30f0acd242ace818b16dc1eef463a`; it
records complete eight-row coverage and zero reportable diff-introduced
findings.

## Tests and actual results

The focused controls cover the shared selection helper and both direct runner
interfaces. Explicit CLI input overrides `VERIFIED_RUN_ROOT`, which overrides
the historical fallback; a private root remains usable and relative input is
normalized without link resolution. The runners reject final-root and
parent-component symlinks before observed writes or children. `--explain`
returns without materializing a root.

The report-evidence suite confirms that extracted static strings preserve
existing report bytes and full-matrix command semantics. The direct
`collect-no-crs-source.py` JSONL control confirms every retained terminal-status
mapping. These are focused local source/contract controls, not a connector
matrix or hosted CI result.

## Security impact

The verified-root change repairs a validated local/shared-host filesystem
boundary. The precondition is a lower-privileged actor able to create a final
or ancestor symlink below a shared sticky temporary parent before the private
runner child is created. The repair uses repository-native descriptor traversal,
no-follow, ownership, and mode checks before artifact, compiler, executable,
or harness sinks.

It does not claim safety for independent caller-owned `--build-root`,
`--tmp-root`, native `--output-dir`, connector/framework roots, or a same-UID
actor able to mutate an already private root. No live cross-user race,
connector host, remote endpoint, GitHub token, secret, or external-PR execution
path was exercised. The sealed security review found no new diff-introduced
security candidate.

## Documentation status

This English/German pair records the Sonar boundary, selected repair keys,
verified-root decision, security finding, focused controls, and delivery limits.
Both Change Record indexes are updated. `FND-PARENT-0074` is a local
control-plane record and is not staged as versioned product documentation.

## Runtime evidence

No connector runtime matrix, networked preparation, package installation,
generated-report refresh, or production deployment was run. The deterministic
symlink controls exercise real runner entry points in task-owned temporary
storage; they are local filesystem-integrity controls, not a live multi-user
race or production connector result.

## Compatibility and generated artifacts

No generated artifact is committed. The literal extractions preserve report and
native-case string values, result filename, full-matrix prefix, UTC conversion,
table structure, status mapping, and command construction. The intentional
compatibility change is to reject unsafe/symlinked roots rather than resolve
them; trusted private absolute roots and documented precedence remain usable.

## Known limitations

The intentionally uninitialized Framework Gitlink blocks
`tests.test_collect_no_crs_source` and the runtime-environment suite in this
isolated Parent worktree. Initializing or changing Framework/MRTS to obtain a
passing result is out of scope and was not attempted. The local tests do not
prove cross-user race resistance beyond deterministic symlink controls and
descriptor-based implementation review.

## Remaining risks

The other 67 current `ci/runtime` findings remain outside this PR's bounded
remediation set. The security repair awaits a task-owned commit, normal push,
Draft PR, and fresh exact-head GitHub/SonarQube Cloud evidence before
`FND-PARENT-0074` can become `verified` or `closed`.

## Checks not run and rationale

- The full connector/runtime matrix, host preparation, networked checks,
  package installation, generated-report refresh, and a live cross-user race
  were not run: they would expand the focused Parent source/contract scope.
- Framework/MRTS source, Gitlinks, workflows, `.github/`, `scripts/`, scanner
  configuration, suppressions, exclusions, Quality Gates, external Sonar issue
  state, and `master` were unchanged/not run by this task.
- Hosted GitHub Actions, PR review, SonarQube Cloud PR analysis, and merge
  evidence require the eventual exact Draft PR head and are not inferred
  locally.

## Final diff and review status

The local scoped diff contains verified-root hardening, eleven narrow
Sonar-oriented maintainability repairs, direct regression controls, and this
bilingual traceability pair. The focused security diff scan has zero reportable
diff-introduced findings. At authoring, there is no task commit, push, Draft PR,
hosted check, review, exact-head SonarQube Cloud result, or `master` integration
claim; those facts must be added only after observation.
