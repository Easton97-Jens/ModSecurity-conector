# Change Record

**Language:** English | [Deutsch](CR-20260811-protected-nginx-broker-caller-repin-v5.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260811-protected-nginx-broker-caller-repin-v5 |
| Date (UTC) | 2026-08-11 |
| Base revision | `49c40779a7b6de9f699391bcd524ea069787df42` |
| Previous protected broker SHA | `7a9240d35e50475cc1a381fa103b0bb5cca2bee3` |
| Active protected broker SHA | `49c40779a7b6de9f699391bcd524ea069787df42` |
| Broker Framework gitlink | `03880bf66b3905940466ff10b3a431a27ecc6b26` |
| Related findings | FND-PARENT-0120, FND-PARENT-0121 |

## Motivation and problem statement

PR #275 merged broker commit `49c40779a7b6de9f699391bcd524ea069787df42`,
which contains the narrow FND-PARENT-0120/FND-PARENT-0121 repair. The current
protected caller still selected the previous broker commit
`7a9240d35e50475cc1a381fa103b0bb5cca2bee3`. This separate Parent-only change
repins the caller to the available immutable broker revision before any new
protected resulting-master lifecycle is considered.

## Acceptance criteria

Both named caller jobs use the same full immutable `uses` SHA and matching
`protected_broker_sha`; both `framework_sha` inputs equal the mode-`160000`
gitlink recorded by broker `49c40779a7b6de9f699391bcd524ea069787df42`. The
helper, manifest/evidence validation, result summary, static contract tests,
and paired guides use that same tuple. No permission, trigger, gate, profile,
schema, root command, Framework gitlink, Framework/MRTS source, APR-util, or
PR #240 product change is included.

## Implementation decision and rationale

The Framework value was derived only from the Parent Git object:
`git ls-tree 49c40779a7b6de9f699391bcd524ea069787df42 -- modules/ModSecurity-test-Framework`
returned mode `160000` and commit
`03880bf66b3905940466ff10b3a431a27ecc6b26`. The caller changes only the
immutable selection tuple; it does not make a mutable reference, a
caller-selected code path, or a new privileged capability possible. Historical
Change Records remain unchanged.

## Security impact

The immutable caller-to-broker selection remains fail-closed. Static tests
continue to reject mutable refs, mismatched tuple inputs, altered job gates,
extra jobs or inputs, elevated permissions, inherited secrets, and use of
untrusted caller code at the root boundary. This record is not protected
lifecycle evidence.

## Changed files

- `.github/workflows/run-protected-nginx-root-broker.yml`
- `ci/runtime/broker/protected_nginx_broker_caller.py`
- `ci/checks/common/check-python-version-contract.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_nginx_root_broker.py`
- `docs/security/trusted-nginx-root-broker.md`
- `docs/security/trusted-nginx-root-broker.de.md`
- this Change Record and its German companion

Framework source/Gitlink, MRTS, Framework PR #74, APR-util remediation, and
PR #240 changes or merge are out of scope.

## Tests and actual results

- The focused Parent caller/broker suite passed: 127 tests in 11.605 seconds.
- The broader selected suite ran 137 tests; 136 passed and one failed because
  the isolated worktree lacks the existing Framework-gitlink target
  `modules/ModSecurity-test-Framework/ci/lib/common.sh`. The failing snapshot
  integration is not a repin-source failure and no Framework materialization
  was performed.
- `make check-ci-security-contract` passed: 26 tests plus validate-only
  actionlint, zizmor, and gitleaks lock checks.
- The checksum-verified actionlint `1.7.12` run with ShellCheck passed.
- The checksum-verified zizmor `1.29.0` offline workflow scan passed; both
  safe fixtures passed and both insecure fixtures were rejected as expected.
- In-memory syntax compilation of the four changed Python files passed.

## Commands executed

- `PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 "$PARENT_PYTHON" -m unittest -v tests.test_protected_nginx_broker_caller tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile tests.test_nginx_root_broker_workflow tests.test_ci_security_workflows tests.test_python_version_contract` — PASS, 127 tests.
- `make PYTHON="$PARENT_PYTHON" check-ci-security-contract` — PASS.
- `actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml ci/fixtures/workflow-permission-contract/*.yml` — PASS, using the checksum-verified `1.7.12` task-local binary.
- `zizmor --offline .github/workflows` — PASS, using the checksum-verified `1.29.0` task-local binary; safe fixtures passed and the insecure fixtures returned the expected nonzero rejection.
- `make PYTHON="$PARENT_PYTHON" check-python-version-contract` — exit 2 for pre-existing unrelated workflow inventory violations; it reported no protected-caller tuple violation.

`$PARENT_PYTHON` denotes the policy-selected Parent virtual-environment
interpreter. Its locally available version was `3.14.4`; `.python-version`
declares CI lane `3.14.6`.

## Runtime evidence

No new protected workflow dispatch, root action, NGINX start, CRS fetch,
evidence readback, process/socket/PID/listener cleanup, pull-request check,
or merge has occurred at the time of this record. The prior failures remain
historical failure evidence only.

## Checks not run and rationale

Hosted pull-request checks, CodeQL, SonarQube Cloud, review/conversation
resolution, SHA-bound squash merge, resulting-master checks, and the protected
no-CRS/OWASP-CRS lifecycle are pending the separate authorized Draft PR and
its exact final head. No local root runtime is a substitute. The broad
documentation checks are blocked in this isolated worktree by existing absent
Framework-gitlink targets; the paired changed documents receive focused parity
and link review.

## Known limitations

The selected local Parent venv is `3.14.4`, not the declared CI lane `3.14.6`.
It is useful local test evidence but does not replace exact hosted Python-lane
evidence. The isolated worktree intentionally does not materialize the
Framework gitlink, so the one broad snapshot integration test cannot run here.

## Remaining risks

FND-PARENT-0120 and FND-PARENT-0121 remain unverified until a successful
resulting-master lifecycle proves both profiles, evidence readback, and
process/socket/PID/listener cleanup. The APR-util HTTP 404 remains a separate
Framework-owned blocker; PR #240 remains merge-blocked even if this caller
lifecycle later succeeds.

## Final review status

Pre-commit scope and security review are pending final diff validation. No
commit, push, pull request, hosted check, review, merge, or runtime success is
claimed by this record.

## Final diff and review status

The intended scope is the nine files listed above. The final exact committed
caller-blob validation, PR-head checks, and resulting-master lifecycle remain
pending.
