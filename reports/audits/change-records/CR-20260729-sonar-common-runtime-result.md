# Change Record: Parent Common runtime-smoke result-object refactor

**Language:** English | [Deutsch](CR-20260729-sonar-common-runtime-result.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-common-runtime-result |
| Date (UTC) | 2026-07-29 |
| Base revision | dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc |
| Boundary | Parent `common/` runtime-smoke source, its direct Parent regression tests, and this English/German Change Record pair and indexes. Framework/MRTS, Gitlinks, workflows, SonarQube Cloud configuration, exclusions, suppressions, Quality Gates, and `master` are unchanged. |
| Delivery status | Local candidate at record authoring. No task commit, push, pull request, hosted analysis, review, merge, or `master` integration is claimed. |

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
evidence fields. `writer_args` and `write_result` each accept that one value;
all call sites construct named fields, so status and evidence ownership are
explicit and no positional field ordering remains between the two functions.
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
| Same suite inside the sandbox | blocked by the sandbox's loopback-socket restriction (`PermissionError: [Errno 1] Operation not permitted`) after the non-socket CRS/path tests passed. The outside-sandbox run is the recorded full result. |
| `git diff --check` before record authoring | passed. |

## Commands executed

The test command and `git diff --check` listed above are the complete commands
executed before record authoring. No hosted or connector-host command is
represented as local evidence.

## Runtime evidence

The focused tests use local loopback HTTP handlers only. They verify request
body framing and bounded reads but do not start an Envoy, Traefik, Lighttpd, or
libModSecurity host runtime. They are regression evidence for the changed
writer boundary, not connector-host evidence.

## Checks not run and rationale

- No host connector runtime or libModSecurity integration run was selected:
  this refactor does not change the host protocol/adapter behavior.
- Hosted SonarQube Cloud and GitHub Actions results do not exist at record
  authoring; they must be rechecked on the exact pushed Draft-PR head.
- `make check-bilingual-docs` is blocked by 20 pre-existing links into the
  unpopulated Framework submodule. After the required-record headings were
  corrected, it reports no error for this record pair; the broad check cannot
  pass until that external checkout is populated.

## Known limitations

Only the exact hosted PR analysis can establish a lower global duplicate-line
measure, the closure of the two baseline `python:S107` rows, and the required
new-code Quality Gate. The typed value keeps fields shallowly immutable; its
tuple `missing` collection avoids mutable dependency entries, while the
`argparse.Namespace` source remains the existing mutable input boundary.

## Remaining risks

The existing runtime-smoke caller paths are covered by the focused result
argument and boundary tests, but connector-host behavior remains outside this
source-only refactor's evidence. Hosted SonarQube Cloud analysis remains the
required measure for the global-count acceptance criteria.

## Final diff and review status

The diff is restricted to the selected Common runtime-smoke writer contract,
its direct regression test, and required bilingual traceability. No Framework
or MRTS source/Gitlink, workflow, scanner control, suppression, or default
branch is included. Local validation above passed; hosted delivery evidence is
pending a normal task-branch commit, push, and Draft PR.
