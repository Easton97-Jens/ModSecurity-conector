# Change Record: Parent response-header fixture containment for SonarQube Cloud S8707

**Language:** English | [Deutsch](CR-20260727-sonar-response-header-fixture-containment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-response-header-fixture-containment |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | SonarQube Cloud `pythonsecurity:S8707` receipt `AZ9cRyfJHhV2CayPTPxt` at `ci/runtime/common/response-header-test-backend.py`, fixture-file read path. |
| Boundary | The Parent response-header backend, a focused Parent regression test, and this English/German Change Record pair. Framework/MRTS source, Gitlinks, workflows, report generation, SonarQube Cloud configuration, suppressions, external issue state, and master remain unchanged. |

## Motivation and problem statement

The backend already constrained `--body-file` to a regular file inside a
configured `--safe-root`, but `--fixture-file` was read through `Path.read_text`
without the same containment check. A caller able to control the local backend
invocation could select a readable JSON-shaped file outside the intended
runtime root. The fixture influences bounded response status/headers, so this
is a real broken-control path rather than a cosmetic scanner signal.

## Acceptance criteria

- Fixture reads resolve an existing regular file inside an explicit safe root
  (or the pre-existing CWD fallback), before JSON is read or a listener starts.
- Traversal and an in-root symlink resolving outside the safe root are rejected.
- A valid in-root fixture remains accepted and fixture files do not acquire the
  body file's one-megabyte limit.
- The existing body-file size limit remains enforced.
- No response header validation, listener sequencing, Framework/MRTS source,
  Gitlink, workflow, scanner configuration, suppression, or master change.

## Implementation decision and rationale

`resolve_regular_file` generalizes the existing body resolver while retaining
its strict resolution, regular-file, containment, and optional maximum-size
checks. `resolve_body_file` continues to pass `MAX_BODY_BYTES`; the new
`resolve_fixture_file` intentionally does not. `load_fixture_file` resolves
through that control before `read_text`, and `main` passes parsed safe roots
into the fixture path. Validation errors still reach `parser.error` before
server construction.

## Changed files

- ci/runtime/common/response-header-test-backend.py
- tests/test_response_header_backend_fixture_paths.py
- reports/audits/change-records/CR-20260727-sonar-response-header-fixture-containment.md
- reports/audits/change-records/CR-20260727-sonar-response-header-fixture-containment.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_response_header_backend_fixture_paths tests.test_response_header_backend.ResponseHeaderBackendTest.test_backend_uses_declarative_status_and_marker_header tests.test_response_header_backend.ResponseHeaderBackendTest.test_invalid_fixture_headers_are_rejected_before_listening tests.test_response_header_backend.ResponseHeaderBackendTest.test_both_host_harnesses_use_the_fixture_for_any_response_headers_rule
rtk proxy git diff --check
```

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused fixture/backend controls | passed: 7 tests. |
| Legitimate in-root fixture | passed: declarative status and marker header remain served. |
| Unsafe absolute fixture path | passed: rejected before listener startup. |
| In-root symlink to outside fixture | passed: rejected by resolved containment. |
| Compatibility | passed: a valid fixture larger than the body limit remains accepted; body files remain limited. |
| Existing invalid header and host-harness fixture wiring | passed. |
| `git diff --check` | passed: no whitespace errors. |

## Security impact

The baseline source-to-sink path is validated: CLI `--fixture-file` flowed to
`Path.read_text` without the existing safe-root control. The candidate now
uses strict canonical containment and a regular-file test before the sink, so
relative traversals and symlink-outside-root targets fail. The harness invokes
the backend with a harness-owned `--safe-root` and fixture under that runtime
root. The candidate does not change request parsing, header validation,
network exposure, or body-file constraints.

There is a residual pathname TOCTOU consideration if an adversary can replace
an in-root file after validation but before the later pathname read. That
hostile concurrent-writer model is outside the demonstrated harness-owned
runtime-root contract; it is not represented as a globally closed descriptor-
level guarantee. No security finding is marked closed until an exact-head
analysis is observed.

## Documentation status

This complete English/German Change Record pair documents the validated
baseline, the candidate control, exact local checks, compatibility decision,
and residual scope. Both change-record indexes are updated.

## Runtime evidence

The focused test runs exercise the local Python backend and static host-harness
fixture wiring only. No broad connector runtime matrix or production deployment
was run or claimed.

## Known limitations

The full `tests.test_response_header_backend` module contains Framework-
dependent metadata cases that are outside this narrow path-control change and
were not needed to exercise the changed read boundary. Hosted GitHub and
SonarQube Cloud analysis have not yet examined the candidate.

## Remaining risks

The safety of the no-`--safe-root` CWD fallback depends on a trusted, narrow
working directory, as it did for body files before this candidate. A hostile
writer of the harness-owned runtime root would require a separate descriptor-
relative/no-follow design and explicit lifecycle/ownership evidence. This
candidate makes no conclusion about the other current S8707 inventory rows or
the broader 1,022-item backlog.

## Checks not run and rationale

- Full connector builds, runtime matrices, Framework/MRTS tests, and report
  generation are not applicable to this narrow Parent backend boundary.
- Hosted GitHub checks and exact-head SonarQube Cloud analysis are pending.
  This record grants neither external issue closure nor master-merge authority.

## Final diff and review status

The candidate contains only the minimal Parent path-control repair, direct
negative/compatibility regression tests, and required bilingual traceability.
An independent security review found the baseline control gap validated and
the candidate adequate under the harness-owned-root assumption. Commit, push,
PR, hosted checks, external Sonar disposition, and merge facts will be added
only after they are observed.
