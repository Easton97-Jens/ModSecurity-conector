# Change Record: Parent cache-test unused local remediation for SonarQube Cloud S1481

**Language:** English | [Deutsch](CR-20260721-sonar-s1481-cache-test-unused-local.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260721-sonar-s1481-cache-test-unused-local |
| Date (UTC) | 2026-07-21 |
| Base revision | 2ade0d40983b7af21a65b8cd2884866b85626393 |
| Tracking | One Parent-only python:S1481 Code Smell: AZ9cRzAcHhV2CayPTP44; retained finding ID FND-SONAR-0016. |
| Boundary | The Parent NGINX runtime-component cache-contract test and this Parent traceability pair/index only; Framework, MRTS, gitlinks, production runtime-component code, scanner configuration, and Quality Gates remain unchanged. |

## Motivation and problem statement

`RuntimeComponentCacheContractTest.test_nginx_discards_marker_owned_partial_root_before_build`
defines a nested NGINX build mock. The mock reads `NGINX_BUILD_DIR` into
`active_build_path`, but no assertion, fixture, artifact path, or control-flow
branch observes that local. SonarQube Cloud rule `python:S1481` reports the
dead assignment. The surrounding test must keep verifying managed partial-root
cleanup, NGINX artifact creation, executable permissions, and cache-manifest
readiness without introducing a scanner suppression.

## Acceptance criteria

- Remove only the unused `active_build_path` assignment for
  `AZ9cRzAcHhV2CayPTP44`.
- Preserve the mock's use of `NGINX_PREFIX` and every existing partial-cache
  cleanup, artifact, executable, and manifest assertion.
- Run selected-file Python syntax, the complete focused cache-contract test
  module, bilingual/Change-Record checks, and final diff validation before
  delivery.
- Obtain fresh exact Draft-PR SonarQube Cloud evidence before claiming the key
  is resolved; the PR must stay unmerged.

## Implementation decision and rationale

The assignment is deleted rather than renamed or replaced with `_`: the value
has no observable use, while `active_nginx_prefix` remains the sole derived
path used to create the binary, module, and configuration fixtures. This is a
single-source, single-key maintainability correction, not a mechanical
project-wide `python:S1481` sweep.

## Security impact

The change is confined to a Parent test mock and removes no validation,
containment, dependency, file-path, network, subprocess, authentication,
authorization, logging, scanner, Quality-Gate, suppression, `NOSONAR`, or
false-positive control. The focused assessment found no security-boundary
change requiring a separate security-finding remediation.

## Changed files

- tests/test_runtime_component_cache_contract.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| Selected Parent virtual-environment identity check | passed: `/root/git/ModSecurity-conector/.venv/bin/python`, Python `3.14.4`, venv prefix verified. |
| Selected-file Python syntax with external bytecode cache | passed: `python -B -s -m compileall -q tests/test_runtime_component_cache_contract.py`. |
| Focused `tests.test_runtime_component_cache_contract` `unittest` module | passed: 25 tests. |
| Initial auxiliary source-structure assertion | failed only because its broad count included the separate, used Apache `active_build_path`; no product check failed. |
| Corrected NGINX-block source-structure assertion | passed: the `build_nginx` mock no longer contains `active_build_path` or `NGINX_BUILD_DIR` and retains `active_nginx_prefix`. |
| Focused Change Record pair contract | passed: required sections, matching identity values, heading levels, and table structure. |
| `tests.test_bilingual_docs` `unittest` module | passed: 11 tests. |
| `rtk proxy git diff --check` | passed. |

Hosted exact-head evidence remains future work at record creation; this record
does not claim unobserved CI, SonarQube Cloud, review, or delivery results.

## Runtime evidence

No connector runtime path or production runtime-component implementation
changes. The focused Parent contract test is the behavioral control for the
mock that prepares the NGINX artifacts used by the cache-recovery scenario.

## Checks not run and rationale

- A connector build/runtime or CRS/MRTS matrix is not applicable: no connector
  source, production lifecycle, transport behavior, Framework file, or MRTS
  file changes.
- A full repository Sonar sweep is not used as local evidence. SonarQube Cloud
  PR analysis for the exact head is the required hosted decision point.

## Known limitations

This correction addresses one current SonarQube Cloud observation only. The
focused test proves its existing Parent cache-contract behavior, not a complete
NGINX build or runtime lifecycle. The current CI lane is `3.13.14` from
`.python-version`; the available local Parent venv is `3.14.4`, so exact-lane
execution remains a required hosted check.

## Remaining risks

The broader Parent-only SonarQube Cloud backlog remains separately tracked.
Hosted exact-head SonarQube Cloud and GitHub Actions evidence are still
required for a Draft PR, which must remain unmerged.

## Final diff and review status

Local source, focused test, traceability, and final-diff checks passed. The
intended source diff removes one dead test-local assignment and adds bilingual
traceability. Before a Draft PR is called verified, exact local/remote/PR SHA
equality, applicable GitHub checks (including the configured Python `3.13.14`
lane), SonarQube Cloud Quality Gate, selected-key query, and PR state must be
rechecked for the actual head.
