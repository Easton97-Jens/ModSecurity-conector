# Change Record: Parent Common runtime-smoke result-object refactor

**Language:** English | [Deutsch](CR-20260729-sonar-common-runtime-result.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-common-runtime-result |
| Date (UTC) | 2026-07-29 |
| Base revision | dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc |
| Boundary | Parent `common/` runtime-smoke source, its direct Parent regression tests, and this English/German Change Record pair and indexes. Framework/MRTS, Gitlinks, workflows, SonarQube Cloud configuration, exclusions, suppressions, Quality Gates, and `master` are unchanged. |
| Delivery status | Draft PR [#164](https://github.com/Easton97-Jens/ModSecurity-conector/pull/164) exists. Its first head `265e3e90debb0c33546cbd6aa4c32dc4a1bf4fb3` passed all applicable GitHub Actions but failed the SonarQube Cloud new-code gate. The source follow-up head `9ea886a6fd4a8e8b27b1e0c3d7c5102c6d4e3278` then passed its applicable GitHub Actions and SonarQube Cloud Quality Gate with 0 New Issues and 0.0% New-Code Duplication. This additive documentation correction requires a fresh exact-head gate before the Draft can be made ready; no merge or `master` integration is claimed. |

## Motivation and problem statement

Current `master` has 623 unresolved SonarQube Cloud rows and 1,057 duplicated
lines (0.2%). SonarQube Cloud identifies two `python:S107` rows on the
26-parameter `writer_args` and `write_result` signatures in
`common/scripts/run_local_runtime_smoke.py`. The same pair is the only Common
CPD block in that file: lines 1428 and 1610, each 26 lines, for 52 duplicated
lines.

The runner emits evidence consumed by local runtime-smoke automation. The
refactor must therefore retain every option, value, default, PASS/BLOCKED
status, and missing-dependency entry sent to `write_smoke_result.py`.

## Acceptance criteria

- Result data is carried by one typed immutable value rather than duplicated
  long function signatures.
- `writer_args` produces the same option/value evidence for a CRS-backed,
  blocked runtime result, including status, request statuses, rule identity,
  security evidence, paths, and missing dependencies.
- The existing runtime-output containment, CRS source, request-body framing,
  and finite-socket controls remain passing.
- The exact Draft-PR head must report 0 New Issues, 0.0% Duplication on New
  Code, a passing Quality Gate, and fewer total duplicated lines than the
  recorded `master` baseline.

## Implementation decision and rationale

`SmokeResult` is a frozen dataclass containing the previously positional
evidence fields. `writer_args` and `write_result` each accept that one value.
The first hosted analysis exposed a new `python:S3776` at `writer_args` and
new duplicate result-construction blocks. The follow-up extracts immutable
`BackendEvidence`, derives `SmokeWriterValues` separately, and builds each
result through `smoke_result`. This keeps status and evidence ownership
explicit without repeated positional field ordering or repeated result blocks.
The writer still emits the same command-line protocol and invokes the same
`write_smoke_result.py` entry point.

## Security impact

This change touches the runtime evidence boundary but does not change request
parsing, URL/path validation, process execution, output-root validation, or
the writer program. The direct regression test asserts a representative
blocked CRS result's emitted values; existing security tests retain rejected
symlinks, unsafe roots, writable CRS inputs, malformed body framing, and
oversize body controls. Focused diff review found no weakened control or new
plausible high- or critical-impact issue.

## Changed files

- common/scripts/run_local_runtime_smoke.py
- tests/test_common_runtime_smoke_crs_source_security.py
- this English/German Change Record pair and both indexes

## Tests and actual results

| Command or procedure | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests/test_common_runtime_smoke_crs_source_security.py tests/test_local_runtime_smoke_request_body.py` | passed outside the sandbox: 37 tests, including the new writer-result argument regression and HTTP request-body controls. |
| Same command after the Sonar-remediation follow-up | passed outside the sandbox: 39 tests, including direct `BackendEvidence`/path composition, simple-backend CRS-value preservation, and the prior writer-result and request-body controls. |
| Same command in the clean integration clone before this documentation correction | passed: 39 tests, including the result/evidence composition, simple-backend CRS-value preservation, runtime-path, and request-body controls. |
| Same suite inside the sandbox | blocked by the sandbox's loopback-socket restriction (`PermissionError: [Errno 1] Operation not permitted`) after the non-socket CRS/path tests passed. The outside-sandbox run is the recorded full result. |
| `python -m py_compile common/scripts/run_local_runtime_smoke.py tests/test_common_runtime_smoke_crs_source_security.py` in the clean integration clone | passed using a task-owned bytecode cache. |
| `git diff --check` | passed again after the follow-up. |

## Commands executed

The test command, compilation, and `git diff --check` listed above are the
complete local validation commands recorded so far. The first exact PR head
completed applicable GitHub Actions but failed the new-code Sonar criteria;
the source follow-up head `9ea886a6fd4a8e8b27b1e0c3d7c5102c6d4e3278` completed
the applicable GitHub Actions and passing Sonar analysis. No connector-host
command is represented as local evidence. That source-head evidence does not
attest to a later documentation-only PR head.

## Runtime evidence

The focused tests use local loopback HTTP handlers only. They verify request
body framing and bounded reads but do not start an Envoy, Traefik, Lighttpd, or
libModSecurity host runtime. They are regression evidence for the changed
writer boundary, not connector-host evidence.

## Checks not run and rationale

- No host connector runtime or libModSecurity integration run was selected:
  this refactor does not change the host protocol/adapter behavior.
- The first exact PR head had all applicable GitHub Actions pass, but SonarQube
  Cloud reported one new `python:S3776`, 58 new duplicate lines (23.9%), and
  1,094 total duplicate lines. Those failed acceptance criteria triggered the
  follow-up extraction. The source follow-up head `9ea886a6fd4a8e8b27b1e0c3d7c5102c6d4e3278`
  subsequently passed its applicable GitHub Actions and SonarQube Cloud
  Quality Gate with 0 New Issues and 0.0% New-Code Duplication. A later
  documentation-only head still needs its own normal exact-head gate.
- `make check-bilingual-docs` is blocked by 20 pre-existing links into the
  unpopulated Framework submodule. After the required-record headings were
  corrected, it reports no error for this record pair; the broad check cannot
  pass until that external checkout is populated.

## Known limitations

The exact hosted source-follow-up analysis at
`9ea886a6fd4a8e8b27b1e0c3d7c5102c6d4e3278` established a lower global
duplicate-line measure, the absence of the new `python:S3776` row, and the
required new-code Quality Gate. The typed values keep fields shallowly
immutable; their tuple `missing` collection avoids mutable dependency entries,
while the `argparse.Namespace` source remains the existing mutable input
boundary. A documentation-only successor still needs its own protected
exact-head gate before merge.

## Remaining risks

The existing runtime-smoke caller paths are covered by the focused result
argument and boundary tests, but connector-host behavior remains outside this
source-only refactor's evidence. The source follow-up has hosted SonarQube
Cloud evidence; any successor head must repeat the normal protected PR gate.

## Final diff and review status

The diff is restricted to the selected Common runtime-smoke writer contract,
its direct regression tests, and required bilingual traceability. No Framework
or MRTS source/Gitlink, workflow, scanner control, suppression, or default
branch is included. The source follow-up is pushed and has its recorded passing
exact-head hosted analysis. The Draft remains open, and this documentation
correction requires fresh exact-head checks before a Ready transition or
protected handoff.
