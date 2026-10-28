# Change Record: CR-20261028-submodule-native-prerequisites

**Language:** English | [Deutsch](CR-20261028-submodule-native-prerequisites.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261028-submodule-native-prerequisites |
| Date (UTC) | 2026-10-28 |
| Base revision | `cac9461a4e831ea5c45a1eeec4ef21ce63d203e9` |

## Motivation and problem statement

Run `40658370393`, job `122715236041`, passes the earlier NGINX and PyYAML fixes, then fails selected case `apache.zero_result_releases_native_buffers_without_a_rule`. The updater omits the Apache/APR/ModSecurity development prerequisites required by that fixture and already installed in ordinary quick-check jobs. Its failed namespace stdout is also lost because errexit exits after the command substitution before printing it.

## Acceptance criteria

Provision the established native prerequisites before baseline/sandbox setup. Keep captured diagnostics on failure and preserve the nonzero candidate status even when stdout contains a COMPLETE marker. Retain source/output verification, cleanup and final failure enforcement. Keep Apache C17 outputs inside the existing external root, preserving the complete standard/archived selections (100 cases / 80 executions; 1893 cases / 839 executions).

## Implementation decision and rationale

Reuse `build-essential apache2-dev libmodsecurity-dev` as an ordinary-runner setup step after the Python interpreter contract and before immutable baseline capture. The resulting tools, headers and libraries remain behind the existing read-only runtime mounts. No compiler-alias bypass or broader host directory is added.

Capture namespace status explicitly, print captured stdout, and then propagate failure before checking COMPLETE. Stderr remains directly visible. Existing continue-on-error, physical verification, final enforcement and cleanup gates remain unchanged.

A bounded audit of the remaining lint path found the Apache C17 script defaults to absent `/var/tmp`. The fixed candidate environment now sets `APACHE_C_STANDARDS_OUT` to `/external/build/apache-c-standards`; no `/var` exposure is introduced.

## Changed files

- `.github/workflows/update-submodules.yml`: native prerequisites and failure-output/status handling.
- `ci/tools/run-readonly-submodule-validation-namespace.py`: confined Apache standards output.
- `tests/test_ci_security_workflows.py`, `tests/test_run_readonly_submodule_validation_namespace.py`: prerequisite/order, diagnostics/status/cleanup and output-boundary regressions. One new method is on demand only.
- `config/testing/active-cases.json`: four reviewed source hash slots, unchanged execution arrays.
- `reports/testing/test-selection-archive.generated.json`: native regeneration; retained on-demand definitions increase to 6194, with no new automatic selection.
- `docs/build/README.md`, `docs/build/README.de.md`, and this English/German record pair.

## Commands executed

All project shell commands used task-local RTK `v1.0.1`.

| Check | Actual result |
| --- | --- |
| Python 3.15.1: `ON_DEMAND_TESTS=1` unittest selectors `test_update_submodules_separates_validation_from_publishing`, `test_submodule_namespace_failure_keeps_diagnostics_status_and_cleanup`, `test_candidate_environment_uses_only_namespace_views_for_sources` | Exit 0, 3 passed. The diagnostics regression exercises success, candidate exit 17 with a COMPLETE marker, and missing completion; stdout/stderr and cleanup are checked. |
| Focused workflow/diagnostics tests under Python 3.12.14 and 3.15.1 | Both pass; the original workflow loaded in memory reproduces the lost-stdout failure. |
| Original fixed environment loaded in memory | Apache standards output override is absent; its script falls back to forbidden `/var/tmp`. Corrected environment regression passes. |
| Local exact Apache selector | Fails in setup because Apache/APR development prerequisites are absent; no product assertion executes. No system package installation or skip was introduced locally. |
| Current-master ordinary CI positive control: run `40658304761`, job `122714681042` | Terminal success at the same source revision; logs show previously uninstalled Apache/APR/ModSecurity development packages installed, followed by the exact Apache case passing. This is not a jailed updater result. |
| Full inventory admission, exact selection comparison, native archive generation and `--check`, variable documentation | Passed; complete standard and on-demand execution arrays are unchanged. |
| Documentation and final whitespace checks | Passed: bilingual documentation, links, Change Record structure and final whitespace checks. |

## Security impact

Source and runtime mounts, fixed compilers, no-new-privileges, UID/GID drop, write probes, physical inventory/output checks, sanitizers, job permissions, ref allowlists and publisher policy are unchanged. Native setup runs before candidate execution. Captured candidate output was already printed on success; failure now retains those diagnostics too without accepting a failing status or completion marker as success.

## Runtime evidence

Local shell regressions prove diagnostic/status/cleanup behavior; source and environment tests prove the fixed Apache output mapping. The current-master ordinary CI provides a positive native fixture control. The full privileged namespace with this patch still needs a fresh hosted execution after normal integration; no complete updater, hosted runtime or I12 success is claimed.

## Known limitations

The original hosted traceback is unavailable because stdout was discarded and the run retained no artifacts. The prerequisite diagnosis is supported by fixture setup requirements, the missing updater install step, local missing-prerequisite reproduction and the same-source ordinary CI positive control. The repaired failure-output path prevents this loss in subsequent runs. Local namespace/sanitizer execution remains constrained by this environment; no protection is weakened to work around it.

## Remaining risks

A separate downstream publisher problem was also confirmed by read-only rendering of candidate `3a4f2281568139d94fda6b51dc2e07bb8fc06c67`: the central lock digest changes from `3981782d6ea6acc7e087a851709df220c83677bfeb92ee7836d1ec4e90b8d3b9` to `880b1d19b6d78e52a1588033ce794a35d09e58040b8af763d90fcdb9f99c0d34`, but generated-PR inventory companions are not updated/staged. This does not cause the current Apache validation failure. It remains outside this scoped repair; fixing it requires independently verified trusted-base derivation and atomic companion handling, not a bare allowlist expansion or arbitrary hash refresh.

## Checks not run and rationale

Fresh full hosted namespace execution and publisher execution require normal integration into an allowed ref. No dispatch allowlist is widened. Local native execution cannot replace missing development packages or unavailable namespace/sanitizer support. No new connector matrix, historical I12 campaign or Sonar closure is claimed.

## Final diff and review status

Independent read-only review found no material blocker in the four implementation/test files. Final head-bound CI and delivery remain pending; no merge, master change or `verified_pr` status is claimed.
