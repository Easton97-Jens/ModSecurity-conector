# Change Record: Python 3.14.6 and Go 1.26.5 toolchain baseline

**Language:** English | [Deutsch](CR-20260721-python314-go1265-toolchain-baseline.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260721-python314-go1265-toolchain-baseline` |
| Date (UTC) | `2026-07-21` |
| Base revision | `2ade0d40983b7af21a65b8cd2884866b85626393` |
| Boundary | Parent Python/Go toolchain declarations, checked-in CI contracts, Parent tests, generated Parent documentation, and this Change Record pair only; Framework, MRTS, both gitlinks, dependencies, and historical Change Records are unchanged. |
| Finding linkage | `FND-PARENT-0044` (local canonical finding record): observed Parent CI-security contract blocker caused by a stale Python checker expectation. The reproduced command and its result are recorded below. |
| Delivery status | Local candidate verification is complete. No commit, push, pull request, remote CI, review, SonarQube Cloud result, or master integration is asserted by this record. |

## Motivation and problem statement

The Parent declared exact Python `3.13.14` and Go `1.24.13` baselines. This
change upgrades the checked-in Python contract to `3.14.6` and the two Parent
Go modules plus their CodeQL selectors to `1.26.5`. Exact version declarations
remain necessary: a floating minor version would permit unreviewed patch drift.

The current master also contains an observed CI-security contract failure. All
checked-in `actions/setup-python` workflow uses and the reviewed
`ci/tooling/security-tools.lock.yml` entry already use immutable
`actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0`,
but `check-python-version-contract.py` still expected v6.3.0. Its fail-closed
result rejected every valid Python setup job and obscured the remaining Python
ordering checks. The repair updates the checker and its positive/negative
fixtures to the already reviewed v7 reference; it does not change the workflow
pin or security-lock entry.

## Acceptance criteria

- `.python-version` declares exact stable `3.14.6`; the updater, interpreter
  checker, workflow checker, workflow metadata, and focused fixtures/tests
  accept only the `3.14.N` series.
- The updater remains read-only until its default-branch-gated publisher;
  `automation/update-python-314` and
  `chore(ci): propose Python 3.14 patch update` replace the former 3.13
  identity without changing permissions, triggers, trusted checkout, or the
  PR-only boundary.
- The Python workflow checker accepts exactly the existing immutable v7.0.0
  setup reference and continues to reject a mutable tag, shortened SHA, wrong
  comment, or unreviewed reference.
- Both Parent Go modules declare `go 1.26.5`, and both Go CodeQL jobs select
  `go-version: '1.26.5'`.
- Generator-derived EN/DE compiler guides, CI-security documentation, build
  documentation, and focused tests describe the same exact baselines.
- No `go.sum`, dependency version, `toolchain` directive, action pin,
  security-lock value, workflow permission, trigger, Framework content, or
  MRTS content changes.
- Exact Python `3.14.6` and Go `1.26.5` runtime evidence must come from an
  observed hosted CI run for the exact delivery head before verification or
  protected delivery.

## Implementation decision and rationale

The implementation pins `3.14.6` and `1.26.5` in their existing authoritative
files. Python continues to use `python-version-file: .python-version`; Go
continues to use its module declarations and exact CodeQL setup selectors.
This retains one reviewable source of truth for each toolchain.

| Alternative | Disposition | Reason |
| --- | --- | --- |
| Floating `3.14` or `1.26` | Rejected | A runner, tool cache, or automatic resolution could select an unreviewed patch release. |
| Keep Python `3.13.14` or Go `1.24.13` | Rejected | It does not satisfy the requested new baselines. |
| Change the v7 workflow pin or security lock to make the checker pass | Rejected | Workflows and lock already agree on the verified immutable v7 reference; only the checker expectation is stale. |
| Add a Go `toolchain` directive, run `go get`, or update dependencies | Rejected | This is a constrained toolchain-baseline update; dependency graph changes require separate compatibility evidence. |

The Python contract repair is atomic with the version uplift: checker, fixtures,
and tests use the same exact v7 reference as the already reviewed workflows
and lock. It restores the legitimate control without converting an integrity
failure into an allow-all rule. Go remains limited to two `go.mod` directives,
matching CodeQL selectors, and generator-derived documentation.

## Changed files

- `.python-version`, `.github/workflows/update-python-version.yml`,
  `scripts/update-python-version.py`, and the Parent Python interpreter and
  workflow-contract checkers.
- Focused Parent Python updater, interpreter-contract, workflow-contract, and
  CI-security tests with their version-contract fixtures.
- `.github/workflows/ci-security-codeql.yml`,
  `connectors/envoy/ext_proc/go.mod`,
  `connectors/traefik/native_middleware/go.mod`, and
  `scripts/generate_compiler_guides.py` with focused tests and generated
  compiler-guide outputs.
- `docs/build/README.md`, `docs/build/README.de.md`,
  `docs/security/ci-security-tooling.md`, and
  `docs/security/ci-security-tooling.de.md`.
- The Change Record indexes and this English/German Change Record pair.

Framework, MRTS, `go.sum`, historical Python-3.13 and Go-1.24.13 Change
Records, immutable action pins, and the security-tools lock are not changed.

## Commands executed

| Command or evidence | Result |
| --- | --- |
| `env PYTHON=/root/git/ModSecurity-conector/.venv/bin/python PYTHONDONTWRITEBYTECODE=1 make check-python-version-contract` against the base revision | failed, exit `2`: the checker required `actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6.3.0` and found no exact reference because checked-in workflows already use v7.0.0. This is the reproduced legitimate blocker. |
| `env PYTHON=/root/git/ModSecurity-conector/.venv/bin/python PYTHONDONTWRITEBYTECODE=1 make check-python-version-contract` on the candidate | passed: `Python 3.14.6; 25 Python-executing workflow jobs`. This is the same command that failed against the base revision. |
| Focused Python contracts, CI-security, compiler-guide, and bilingual-document unit suite | passed: 98 tests across `tests.test_update_python_version`, `tests.test_python_interpreter_contract`, `tests.test_python_version_contract`, `tests.test_ci_security_workflows`, `tests.test_compiler_guides`, and `tests.test_bilingual_docs`. |
| `make check-ci-security-contract` | passed: 15 CI-security tests plus validate-only checks of the pinned actionlint, zizmor, and gitleaks tool records. |
| `make check-compiler-guides` | passed: 19 generated-guide, shell-shape, link, and EN/DE parity tests. |
| `python -m compileall -q ci scripts tests` | passed using the repository virtual environment. |
| `git diff --check`, plus no diff for `ci/tooling/security-tools.lock.yml` or either `go.sum` | passed. No action-lock, module-integrity, or whitespace change was introduced. |
| `make check-bilingual-docs` | blocked, exit `2`, solely by absent link targets under the intentionally uninitialized Parent Framework gitlink. The focused bilingual-document unit suite and compiler-guide parity checks passed; Framework and MRTS were not initialized or changed. |
| `GOTOOLCHAIN=local go test ./...` in each actual Go module | blocked, exit `1`: local Go is `1.26.0`, while each migrated module correctly requires at least `1.26.5`. No automatic toolchain download was allowed. |
| Exact Python `3.14.6` and Go `1.26.5` local runtime checks | not available: local executables are Python `3.14.4` and Go `1.26.0`, so they cannot evidence the exact declared targets. |

Exact-head hosted CI, review, SonarQube Cloud, and protected-delivery results
remain pending. No unobserved remote check is represented as passed.

## Security impact

This is a CI supply-chain and toolchain-baseline change. The v7 Python action
remains an official full immutable commit covered by the reviewed lock. The
checker repair restores its ability to distinguish that allowed reference from
mutable, shortened, or malformed alternatives; no permission, trigger, lock,
or pin is weakened.

Raising exact Python and Go declarations changes the tools selected by hosted
CI and modules, not connector request parsing, authorization, protocol
handling, or runtime privilege. It does not claim that a particular upstream
toolchain advisory is reachable or resolved without exact-head evidence.

## Runtime evidence

Not applicable. This change does not start a connector, change a connector
protocol path, or establish HTTP/1.1, HTTP/2, HTTP/3, CRS, Framework, MRTS, or
host-runtime compatibility evidence. The required exact toolchain result is
hosted CI evidence, not local connector runtime evidence.

## Known limitations

The local environment provides Python `3.14.4` and Go `1.26.0`, not exact
Python `3.14.6` and Go `1.26.5`. It can validate source shapes and documentation
but cannot prove that exact hosted toolchains execute all focused Python and Go
checks. The task worktree intentionally leaves the Framework gitlink
unpopulated; a full-tree documentation check must report that foreign
dependency rather than modify Framework or MRTS.

## Remaining risks

A Python or Go major/minor baseline change can expose compatibility differences
that static checks do not reveal. Exact-head hosted CI, including Python
candidate validation, CodeQL Go setup, focused Python tests, Go module checks,
documentation checks, reviews, and SonarQube Cloud where configured, remain
required before a verified PR or protected delivery. No risk is accepted,
hidden, or transferred by this record.

## Checks not run and rationale

- Exact hosted GitHub Actions execution with Python `3.14.6` and Go `1.26.5`
  has not been observed; it is the required exact-toolchain evidence.
- Exact PR-head CI, review/thread state, SonarQube Cloud Quality Gate, and
  protected merge/master checks do not exist at this in-progress record state.
- Connector builds and runtimes are not selected because this constrained
  declaration change does not alter connector runtime code; they are not a
  substitute for the required focused CI checks.
- A full-tree documentation/link result may be blocked by the intentionally
  uninitialized Framework gitlink. Framework and MRTS remain out of scope.

## Final diff and review status

The local diff was reviewed against the stated scope: it is limited to Parent
Python/Go declarations, version contracts/tests, generator-owned guides,
paired documentation, and this Change Record. The original checker failure is
no longer reproduced, while mutable, short-SHA, missing-comment, and
wrong-comment setup-python fixtures remain negative controls. Exact-head CI,
review, delivery data, and any resulting-master evidence remain pending and
must be recorded only after observation.
