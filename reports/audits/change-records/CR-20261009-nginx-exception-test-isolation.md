# Change Record: CR-20261009-nginx-exception-test-isolation

**Language:** English | [Deutsch](CR-20261009-nginx-exception-test-isolation.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-exception-test-isolation |
| Date (UTC) | 2026-10-09 |
| Base revision | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |

## Motivation and problem statement

Three `python:S5778` findings identify fixture construction inside exception
assertions. A fixture failure could satisfy the expected exception instead of
demonstrating failure at the intended operation.

## Acceptance criteria

Each reported assertion contains only its tested call. Preserve exact exception
types/messages, descriptor-close checks, and projection reuse rejection. Both
affected test modules must retain their passing behavior without suppressions.

## Implementation decision and rationale

Prepare `PreparedInvocation` and the validator `Mock` before the cleanup and
fsync exception contexts. Compute the projection source path, worker GID and
avoid-roots list before the reuse exception context. Fixture errors now fail
outside the expected-exception boundary. Product and Framework code are unchanged.

## Changed files

- `tests/test_nginx_sequence_driver_phases.py`
- `tests/test_nginx_selected_native_projection.py`
- `reports/audits/change-records/CR-20261009-nginx-exception-test-isolation.md`
- `reports/audits/change-records/CR-20261009-nginx-exception-test-isolation.de.md`

## Commands executed

Commands used `rtk proxy`, the explicit existing Parent virtual-environment
interpreter (`$PARENT_PYTHON`), `PYTHONNOUSERSITE=1`,
`PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, and external
`TMPDIR`, `RUNNER_TEMP`, `PYTHONPYCACHEPREFIX`.

- Bounded external AST characterization of the three reported assertions:
  unchanged baseline exit 1 with five ambiguity diagnostics; corrected exit 0,
  three assertions with one tested call each.
- `$PARENT_PYTHON -m unittest -v tests.test_nginx_sequence_driver_phases tests.test_nginx_selected_native_projection`:
  unchanged baseline exit 0, 25 tests in 2.924s; corrected exit 0, 25 tests in
  3.686s; no skips in either run.
- Native `ci/tools/new-change-record.py create --name nginx-exception-test-isolation --base-revision 240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee --date 2026-10-09`:
  exit 0; generated both scaffolds before factual editing.
- `make check-bilingual-docs PYTHON=$PARENT_PYTHON FRAMEWORK_ROOT=$FRAMEWORK_ROOT`:
  exit 2 for pre-existing missing linked Framework paths in this isolated
  worktree. `make check-doc-links` with the same explicit overrides: exit 2
  for the same checkout limitation. No submodule or symlink was added.
- Native `ci/tools/new-change-record.py check`: exit 0, paired archive structure
  only. `git diff --check`, `py_compile` of both changed tests, and ShellCheck
  of the external validation helpers: exit 0. `rtk --version`: `0.51.0`;
  `rtk gain` available; no hook or tool installation performed.

Logs are retained in the external task analysis directory
`analysis/nginx-all-required-20261008T124555Z/sonar-exception-r1`.

## Security impact

Avoids false-positive exception tests. No product permission, freshness guard,
validator, exception requirement, dependency or Quality Gate is weakened.

## Runtime evidence

None. Controlled unit collaborators and filesystem projection preparation do
not prove hosted NGINX requests, Root/nobody process roles or Canonical coverage.

## Known limitations

The AST check characterizes only the three reported contexts, not the full
Sonar analyzer. Remote closure requires fresh analysis of the published revision.
Full documentation-link checks require a populated integration checkout.

## Remaining risks

Independent integration validation and remote Sonar readback remain necessary.
The 25-test result does not establish a complete repository or runtime result.

## Checks not run and rationale

No native build, hosted runtime, full repository suite, scanner authentication,
privileged test or administrative operation was run in this isolated slice.
Root owns concurrent exact-head integration/runtime and subsequent publication.

## Final diff and review status

Minimal fixture-only diff reviewed with all existing negative assertions
preserved; EN/DE technical facts match. No commit, push, PR-state change,
Framework/MRTS modification or runtime claim was made by this task. Final
archive/whitespace validation is recorded in the external handoff; full
documentation-link checks remain limited as stated above.
