# Change Record: Parent common/scripts SonarQube Cloud remediation

**Language:** English | [Deutsch](CR-20260801-sonar-common-scripts-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-common-scripts-remediation` |
| Date (UTC) | 2026-08-01 |
| Base revision | `6b4aca18d390363764b96d85cd31969b9bb114a1` |
| Tracking | Current SonarQube Cloud `common/scripts/` inventory: 15 Security and 12 Maintainability rows. |
| Boundary | Parent `common/scripts/`, direct Parent tests, and this English/German Change Record pair and indexes only. |
| Delivery state | A task-owned Draft PR is authorized; no commit, push, PR, hosted analysis, or merge is claimed by this pre-delivery record. |

## Motivation and problem statement

The current `common/scripts/` SonarQube Cloud inventory reports 15 Security
and 12 Maintainability issues. The runtime-smoke helper accepts request,
runtime-path, process, loopback-listener, and evidence-output inputs. Its
single long execution path also mixed preparation, probes, outcome creation,
and cleanup. The smoke-result writer and C++ targeted evaluator contained
maintainability findings around concentrated control flow and manual resource
cleanup.

## Implementation decision and rationale

The Python runner now validates the narrow local smoke protocol before request
metadata reaches loopback URLs or the evaluator: supported methods, origin-form
targets, bounded port numbers, fixed probe targets, targeted evaluator
arguments, regular non-symlink connector binaries, and verified output roots
are all explicit contracts. Process arguments remain structured lists and the
result writer is called directly rather than through a Python subprocess.

The runner's Lighttpd and generic proxy paths are decomposed into preparation,
probe, evidence, outcome, and cleanup helpers. Exception paths release started
processes and local servers before returning. The writer is split into small
payload and document helpers while retaining connector-name, verified-root,
and descriptor-based no-follow controls before every output write. The C++
evaluator uses RAII for engine, rules, transaction, and rule-error cleanup;
the resulting source is C++17-compatible.

No SonarQube Cloud rule, Quality Gate, exclusion, suppression, `NOSONAR`,
workflow, Framework, MRTS, Gitlink, or `master` change is part of this work.

## Acceptance criteria

All 27 current source rows in the stated SonarQube Cloud scope have a concrete
source remediation; malformed local request data fails before a network or
evaluator sink; runtime output and executable boundaries remain fail-closed;
normal local smoke result generation remains available; the evaluator compiles
under C++17; focused regression tests pass; and the eventual exact PR head
must demonstrate zero new issues and 0.0% New-Code duplication without scanner
configuration changes.

## Changed files

- `common/scripts/run_local_runtime_smoke.py`
- `common/scripts/write_smoke_result.py`
- `common/scripts/modsecurity_targeted_eval.cc`
- `tests/test_local_runtime_smoke_request_body.py`
- `tests/test_common_runtime_smoke_crs_source_security.py`
- this English/German Change Record pair and their indexes.

## Commands executed

| Command | Result |
| --- | --- |
| Selected Parent Python: `python -m py_compile common/scripts/run_local_runtime_smoke.py common/scripts/write_smoke_result.py` | passed. |
| Selected Parent Python: `python -m unittest -q tests.test_local_runtime_smoke_request_body tests.test_common_runtime_smoke_crs_source_security tests.test_write_smoke_result_security tests.test_c_cpp_diagnostics` | passed: 55 tests. |
| `make check-targeted-evaluator-cpp17` with a task-owned build root and the available dynamic `libmodsecurity.so.3.0.15` | passed: the targeted C++17 evaluator compiled; it was not executed. |
| `git diff --check` | passed before documentation delivery; rerun is required before commit. |
| Sealed Codex Security diff review | passed: complete coverage of the three changed product sources and zero reportable findings. |

## Security impact

The change narrows the local smoke helper's input boundary without expanding
its authority. It makes loopback request construction deterministic, stops
unexpected methods and request-target forms before the local handlers or
evaluator, keeps executable selection to the named regular connector binary,
and preserves verified output-path and no-follow write controls. Structured
subprocess arguments remain in use. C++ RAII prevents error-path resource
ownership from depending on repeated manual cleanup branches.

## Remaining risks

The local helper still executes the explicitly selected connector binary and
links against the supplied local libmodsecurity build for its test-only
evaluator. The added validation narrows those inputs but does not establish
publisher provenance for a developer-controlled binary or library; this is the
same local-development trust boundary and requires normal reviewed build
provisioning.

## Runtime evidence

Focused Python controls cover malformed and absolute-form request handling,
request-body protocol contracts, CRS source security, result-writer output
containment, and C/C++ diagnostics. The targeted evaluator has a successful
C++17 compilation control against the available dynamic libmodsecurity.

## Known limitations

The isolated task environment did not run a complete connector-host runtime
matrix. The targeted evaluator compile used the available dynamic library after
a static-link attempt showed unresolved transitive libraries in that local
artifact set; this is a local linkage-environment limitation, not a source
change or a claimed runtime result.

## Checks not run and rationale

- A complete connector-host runtime matrix was not run because this task is
  scoped to `common/scripts/` source remediation and the isolated environment
  has no task-provisioned host-binary matrix.
- A static targeted-evaluator link was not accepted as evidence because the
  available static libmodsecurity artifact lacked its transitive YAJL, Lua, and
  XML link inputs. The dynamic C++17 compilation control passed instead.
- GitHub Actions and SonarQube Cloud checks cannot exist until the authorized
  task-owned Draft PR is committed and published. Their results are required
  for the exact PR head before any merge consideration.

## Final diff and review status

The sealed security-diff review is retained outside the checkout at
`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/security-diff-scan/report.md`.
It covered every changed product source file and found no reportable security
finding. This record intentionally does not claim a commit, push, PR number,
hosted check, SonarQube Cloud result, merge, or resulting `master` revision
before those facts are observed.
