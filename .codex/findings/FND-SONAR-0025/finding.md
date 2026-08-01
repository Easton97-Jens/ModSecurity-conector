# Finding FND-SONAR-0025: Lighttpd lifecycle fixture input lacks verified runtime-root containment

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `security_candidate` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P2` / `low` / `validated` |
| Status / feasibility | `verified` / `feasible_now` |
| Release blocker / security relevant | no / yes |
| Sonar inventory | `pythonsecurity:S8707`, `AZ9cRymfHhV2CayPTPzM` |

## Summary, behavior, and impact

SonarQube Cloud reported that `--entity-fixture-result` reached
`Path.read_text()` without proving the selected file belonged to the verified
private runtime root. The canonical runner normally writes the fixture below
its private smoke directory, but a direct lifecycle-helper caller could select
an unrelated readable path. The other data-bearing lifecycle CLI inputs had
the same missing containment precondition.

The patch applies the existing Parent private-root, absolute-path, regular-file
and no-symlink control to all six data inputs. It changes the fixture read to
the existing descriptor-relative `O_NOFOLLOW` reader. This is a validated
local developer/CI/operator CLI artifact boundary. It is not evidence of a
remote Lighttpd HTTP arbitrary-file-read exploit, so the calibrated severity
is `low` rather than Sonar's generic HIGH impact label.

## Scope, preconditions, and reproduction

- Affected files/symbols: `safe_runtime_output.py`,
  `write_patched_lifecycle_results.py`, `safe_input_path`,
  `read_runtime_input_text`, `load_fixture_result`, and `main`.
- A direct caller must supply the historical helper with a chosen absolute
  `--entity-fixture-result` path. A material cross-privilege impact would also
  require a separate actor from the private-root owner; repository evidence
  does not establish one.
- The focused lifecycle suite supplies outside-root and symlink paths for all
  six data-bearing options and asserts rejection before result, projection, or
  summary publication. It also preserves the valid in-root lifecycle control.

## Evidence

Run ID: `lighttpd-sonar-security-20260728`.

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| `sonarqube-cloud-issue-AZ9cRymfHhV2CayPTPzM.json` | `81891db472788897c2f98e78dca90bc1ad3422f8bb296190b906bd97a7cfd45d` | One open in-scope `pythonsecurity:S8707` issue at the fixture reader. |
| `test-patched-event-validation.log` | `ce229433d6e29eec70abd1e41fb09656f335146304be8054068362ce787cc4ad` | Eight focused hostile-path and legitimate-control tests passed. |
| `test-patched-host-contract.log` | `00ea1ddd907f040d93ead44b04b4d917cbe1b93d9b23f108ce6b7c4a3f48c6c6` | Seventeen Lighttpd host-contract tests passed. |
| `security-diff-scan/report.md` | `a5e3bcfb9bbd2ce405602b0a61a9f4a5278c64b784b494865873667bd6614ae0` | Sealed complete review of both changed source files found no diff-introduced reportable candidate. |

All artifacts are retained below
`/var/tmp/codex/ModSecurity-conector/runs/lighttpd-sonar-security-20260728/`.

## Root cause, remediation, and acceptance

`load_fixture_result()` used a plain `Path.read_text()` for a CLI-selected
fixture path and the main function passed other CLI paths into readers without
first binding them to the verified root. `safe_input_path()` now delegates to
`runtime_artifact_path(..., must_exist=True)` for every input. Fixture content
then flows through `read_runtime_artifact_text()`, which opens with no-follow
descriptor semantics and verifies a regular file.

Acceptance requires that escaped paths, symlinks, missing files and
non-regular fixture inputs fail before publication; valid lifecycle data stays
compatible; focused tests and the sealed diff review pass; and an exact PR
head proves the original key absent with zero new issues and zero new-code
duplication. Draft PR #201 satisfies the exact-head hosted criterion. No Sonar
policy, exclusion, suppression, `NOSONAR`, Framework, MRTS, or Gitlink change
is permitted.

## Dependencies, controls, related findings, and residual risk

Draft PR #201's exact head has completed GitHub Actions and SonarQube Cloud
verification: all executed GitHub checks passed; the Quality Gate is `OK`; the
OPEN/CONFIRMED PR issue query, `new_violations`, and new duplicated lines are
zero; and new-code duplication density is `0.0`. The relevant regression
suites are `test_patched_event_validation.py` and
`test_patched_host_contract.py`; the legitimate lifecycle control is explicitly
retained.

`FND-SONAR-0001` and `FND-SONAR-0016` are related Sonar context, not
duplicates. A future defense-in-depth change could make JSONL event readers
use the same descriptor-confined reader. Within a private current-user-owned,
non-group/world-writable root, the remaining normal-read interval is
same-identity hardening rather than an evidenced lower-privilege attack path.

Draft Parent PR [#201](https://github.com/Easton97-Jens/ModSecurity-conector/pull/201)
is open against `master`. Its GitHub head, remote branch and local task head
all resolve to `620ce4b8f731ee2e01fd3b9cf21abc4bc38511e6`. Hosted checks and
the exact-head Sonar readback are verified; this record does not claim a merge
or a `master` result.

## History

- `2026-07-30T13:52:50Z`: exact Sonar issue and local CLI boundary revalidated;
  the focused patch and regressions were completed.
- `2026-07-30T14:12:09Z`: the complete security-diff report was sealed; it
  found no newly introduced reportable security candidate.
- `2026-07-30T14:12:09Z`: status set to `fixed`, pending exact draft-PR hosted
  verification. No merge or `master` change has occurred.
- `2026-07-30T14:31:00Z`: Draft Parent PR #201 created and exact head verified
  across local Git, remote branch and GitHub; hosted checks and Sonar pending.
- `2026-07-30T14:32:00Z`: all executed GitHub checks passed and exact-head
  SonarQube Cloud verification returned Quality Gate `OK`, zero open PR issues,
  zero new violations, and `0.0` / zero new-code duplication. Status promoted
  to `verified`; no merge or `master` change occurred.
