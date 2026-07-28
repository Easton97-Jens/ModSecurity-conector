# Change Record: Traefik bounded result-text serialization remediation for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260728-sonar-traefik-result-nullability.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-traefik-result-nullability |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Boundary | Parent Traefik result serialization, its direct C17 source-contract test, this English/German pair, and its indexes only. Framework, MRTS, gitlinks, workflows, Sonar policy, and generated reports remain unchanged. |
| Finding linkage | Targets `c:S2637` keys `AZ9cRyv8HhV2CayPTP10`, `AZ9cRyv8HhV2CayPTP11`, and `AZ9cRyv8HhV2CayPTP12`, plus the first candidate's `c:S3519` keys `AZ-oL-mYW3nRPo6lC6ub`, `AZ-oL-mYW3nRPo6lC6uc`, and `AZ-oL-mYW3nRPo6lC6ud` tracked by `FND-SONAR-0019`. No external issue is claimed closed before exact-head hosted evidence. |

## Motivation and problem statement

`traefik_engine_send_result` writes optional transaction, rule, and redirect
text into a private local-engine Unix-socket result frame. The nullable-copy
form produced three `c:S2637` reports. The first candidate used a shared
one-byte empty C-string fallback, which removed those reports but produced
three BLOCKER `c:S3519` reports because Sonar could model a positive copy from
the fallback.

The existing bounded-size helper returns zero for that fallback, so the
reported out-of-bounds path is not proven dynamically reachable. It is still a
Quality-Gate blocker. The correction must preserve zero-length absent fields,
field order, bytes, maxima, action, phase, status, and flags without a
suppression, protocol change, or weaker limit.

## Acceptance criteria

- Nullable optional pointers retain size zero for absent values.
- One private bounded copy helper accepts size zero without a source and
  rejects a positive-length null source before reading or writing bytes.
- The direct C17 socketpair harness verifies absent, populated, and
  maximum-length fields byte-for-byte plus the null-source negative control.
- Focused C17, diagnostics, Traefik security contracts, documentation, and
  security-diff validation pass without a Sonar policy change.
- No hosted result, review, merge, master update, Framework/MRTS change, or
  full host-runtime result is asserted before observation.

## Implementation decision and rationale

The serializer keeps nullable source pointers and lets
`traefik_engine_bounded_string_size` express an absent field as zero. The new
private `traefik_engine_copy_bounded_text` succeeds for size zero; otherwise it
rejects a null destination or source before its bounded byte loop.
`traefik_engine_send_result` frees its payload and returns failure if that
invariant is violated. Decision/session control flow, frame layout, maxima,
clamping, and decision metadata remain unchanged.

## Changed files

- `connectors/traefik/src/traefik_engine_service.c`
- `tests/test_sonar_reliability_contract.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <workspace-venv>/python -B tests/test_sonar_reliability_contract.py` | passed: 11 tests, including absent, populated, maximum-length, and positive-length-null-source C17 harness controls. |
| `<workspace-venv>/python -B -m unittest -v tests.test_c_cpp_diagnostics` | passed: 7 C/C++ diagnostics-contract tests. |
| `TMPDIR=<task-owned external root> make check-remaining-connectors-c17` | passed: every remaining-connector C translation unit, including Traefik, compiles under C17 with `-Wall -Wextra -Werror`. |
| `<workspace-venv>/python -B -m unittest -v tests.test_bilingual_docs tests.test_traefik_native_local_plugin tests.test_traefik_runtime_smoke_security` | passed: 39 focused documentation and Traefik runtime/security-contract tests. |
| `git diff --check` and the full bilingual-documentation overlay | passed: no whitespace error; all language pairs, Change Record structure, repository path references, and documentation links passed in a task-owned overlay with the Parent-pinned Framework revision `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`. |
| Focused `codex-security:security-diff-scan` of the local successor patch | passed: the sealed exact-local-patch review at snapshot `2d37a63df4555e967210366aad018478e3385564a02cb57c6dce62588d59651c` reviewed both changed files fully and produced no reportable security finding. |

## Security impact

This is a private Unix-socket serialization boundary. The record does not claim
a demonstrated runtime out-of-bounds read: the prior `c:S3519` path lacks the
interprocedural size relation. The revised helper nevertheless fails closed for
a positive-length null source without expanding serialization. The sealed local
security review found no reportable vulnerability in the changed serializer or
its directly supporting test.

## Runtime evidence

The actual C translation unit is compiled and executed over a Unix socket pair.
The direct harness proves absent, populated, maximum-length, and null-source
behaviors, including rejection before destination mutation for a positive-length
null source. This is focused source-level protocol evidence, not a full
Traefik/Common/libmodsecurity host-runtime test.

## Known limitations

Verified libmodsecurity development headers/libraries are unavailable, so the
full host/plugin runtime is not claimed. The focused review is limited to the
two changed files and does not replace exact-head hosted Sonar analysis.

## Remaining risks

A deployed Traefik host, loaded plugin, and live Common/libmodsecurity
transaction can add behavior that the local harness does not execute. The
external `c:S2637` and `c:S3519` dispositions remain open until a fresh hosted
analysis observes the successor PR head.

## Checks not run and rationale

- The full Traefik host/plugin runtime was not run because no verified
  libmodsecurity development header/library pair is available in the approved
  local environment.
- Exact-head GitHub, SonarQube Cloud, review, and merge checks are not
  currently observed for this successor; they must be re-read after its normal
  update to Draft PR #150.

## Final diff and review status

Draft Parent PR #150 remains open against `master`; its first published head
failed on the new `c:S3519` blockers. The local successor has passed its sealed
security-diff review and focused local checks, but makes no hosted result
claim. After its normal update, exact-head checks, SonarQube Cloud readback,
and review remain mandatory.
