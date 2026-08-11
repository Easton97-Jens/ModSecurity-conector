# Change Record

**Language:** English | [Deutsch](CR-20260811-trusted-nginx-broker-crs-placeholder-worker-directory-repair.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260811-trusted-nginx-broker-crs-placeholder-worker-directory-repair |
| Date (UTC) | 2026-08-11 |
| Base revision | `4749c02c6dd5e285c4309b4e69b0bb28ae459e48` |
| Findings | FND-PARENT-0120, FND-PARENT-0121 |
| Failure evidence | GitHub Actions run `31421851336` |

## Motivation and problem statement

This Parent-only repair records the narrow handling for the pinned CRS zero-byte
placeholder and worker-written broker runtime directories. Run `31421851336`
is failure evidence only; it does not establish a hosted lifecycle result.

## Acceptance criteria

The broker contract binds the exact CRS repository, release tag, commit,
empty-placeholder Git blob, and SHA-256; admits no other empty CRS file; and
retains fail-closed metadata and provenance checks. Only broker-created logs,
state, and CRS audit directories may use root ownership, the admitted worker
group, and exact mode `0730`. The EN/DE documents and records state the same
facts without hosted, PR, runtime, lifecycle, evidence-readback, or cleanup
success claims.

## Implementation decision and rationale

The CRS tuple remains `https://github.com/coreruleset/coreruleset.git`,
`v4.28.0`, and `55b09f5acfd16413e7b31041100711ceb7adc89c`. The only
approved empty leaf is `plugins/empty-after.conf`, bound to Git blob
`e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` and SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Only logs, state, and the CRS audit directory are root-owned, use the admitted
worker GID, require exact `0730`, and require non-symlink paths. Other
directory-metadata and broker security controls remain unchanged.

## Security impact

The named pinned leaf is not a general empty-file exception. The worker-write
allowance adds no broad writable directory and no caller-provided path, command,
executable, manifest field, or permission.

## Changed files

- `ci/runtime/broker/nginx_root_broker.py`
- `tests/test_nginx_root_broker.py`
- `tests/test_nginx_root_broker_crs_profile.py`
- `docs/security/trusted-nginx-root-broker.md`
- `docs/security/trusted-nginx-root-broker.de.md`
- this Change Record and its German companion

Framework source/Gitlink, MRTS, and PR #240 product changes are out of scope.
This record was authored before delivery. The current user authorizes one
separate Parent commit, push, and Draft PR; any merge, including PR #240's, is
out of scope.

## Tests and actual results

- In-memory compile: passed.
- `tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile`:
  passed, 55 tests in 11.750 seconds.
- `tests.test_nginx_root_broker_workflow tests.test_protected_nginx_broker_caller tests.test_ci_security_workflows tests.test_python_version_contract`:
  passed, 72 tests in 1.384 seconds.
- `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract`:
  passed, 26 tests plus validate-only actionlint/zizmor/gitleaks.
- Aggregate selection including the snapshot contract: 81 passed and 1 failed
  because the isolated worktree lacks
  `modules/ModSecurity-test-Framework/ci/lib/common.sh`; this is not presented
  as a source regression.

## Commands executed

The test selections and CI security contract listed above were executed with
their stated results. `git diff --check` passed. Scoped documentation checks
are recorded after their execution in the final review.

## Runtime evidence

There is no successful hosted, PR, root, worker, NGINX, CRS, audit,
evidence-readback, cleanup, or lifecycle evidence. Run `31421851336` remains
failure evidence only.

## Checks not run and rationale

Direct `py_compile` was blocked because the worktree cannot create
`__pycache__`. Direct `check-python-version-contract.py --json` exits 1 both
on clean base/master `4749c02c6dd5e285c4309b4e69b0bb28ae459e48` and on this
task diff because of unrelated existing workflow inventory violations; it is
unchanged baseline evidence, not a repair result. No hosted workflow, root
action, NGINX start, CRS fetch, audit, evidence readback, cleanup, PR, or
delivery action was run.

## Known limitations

The evidence is local source/static evidence only. It does not validate a
writable hosted runner, GitHub Actions context, real root/master-worker
behavior, or a protected resulting-master lifecycle.

## Remaining risks

A future protected resulting-master run must independently demonstrate both
`no-crs` and `owasp-crs`, evidence readback, and cleanup. PR #240 is not
unblocked by this record.

## Final review status

The scoped critical-literal, heading, and reciprocal-link parity review passed,
and `git diff --check` passed. `make check-bilingual-docs` exited 1 because
the isolated worktree lacks Framework paths referenced by existing repository
documents; its reported missing targets are outside the assigned files and this
Parent-only repair. No delivery state is claimed.

## Final diff and review status

This record is limited to the Parent repair based at
`4749c02c6dd5e285c4309b4e69b0bb28ae459e48`; it claims no commit, published
head, PR, hosted check, review, lifecycle, or merge.
