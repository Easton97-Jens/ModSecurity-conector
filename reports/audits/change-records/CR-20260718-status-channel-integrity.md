# Change Record: CI status-channel integrity

**Language:** English | [Deutsch](CR-20260718-status-channel-integrity.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260718-status-channel-integrity` |
| Date (UTC) | `2026-07-18` |
| Base revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Finding | `FND-PARENT-0025` |
| Boundary | Parent CI status runner, Apache lint wiring, tests, and documentation only; Framework and MRTS are unchanged. |

## Motivation and problem statement

`ci/tools/run-check-status.py` previously parsed a `CHECK_STATUS_REASON` line
from combined child `stdout` and `stderr`. A child exiting `77` could therefore
print the approved Apache prerequisite string and turn an allowed lint result
into success. The output stream was acting as an unauthenticated status
channel.

## Acceptance criteria

- A child-produced approved marker in either `stdout` or `stderr` cannot
  authorize a blocked result.
- The missing Apache development prerequisite remains an allowed, structured
  lint disposition only when the Parent runner detects it before starting the
  child.
- A usable APXS/header control path still runs the child and preserves success
  or failure semantics.
- Direct, unclassified exit `77` results remain nonzero.
- Parent regression tests and bilingual documentation describe the resulting
  control boundary truthfully.

## Implementation decision and rationale

The runner no longer parses child text for a reason. It persists a version-2
record with `status_source`; only its
`--blocked-if-missing-apache-development` preflight can issue the allowed
`apache_development_prerequisite` disposition. That preflight resolves
`APXS_BIN`, `APXS`, `CI_APXS_BIN_CANDIDATES`, or `apxs`/`apxs2`, then requires
an executable APXS whose `-q INCLUDEDIR` result is absolute and contains
`httpd.h`. When it succeeds, the child runs normally; any later child exit
`77` remains unclassified and nonzero. The Apache child script no longer emits
a status-control marker.

The SonarCloud follow-up keeps that decision boundary unchanged. It assigns
the resolved APXS candidates to one explicitly typed `tuple[str, ...]` value
and returns it once, preserving the existing priority and malformed-config
behavior without adding a second status channel.

## Security impact

The controlled inputs are direct-child `stdout`, `stderr`, and exit status.
The asset is the CI decision to allow an optional Apache prerequisite block.
The Parent runner now owns that authorization through a separate persisted
record and parent preflight. Child output remains diagnostic only. This patch
does not change runtime-host evidence, report governance, Framework behavior,
MRTS, or a connector runtime claim.

## Changed files

- `ci/tools/run-check-status.py`
- `Makefile`
- `ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh`
- `tests/test_optional_prerequisite_status.py`
- `ci/README.md` and `ci/README.de.md`
- this English/German Change Record pair and its README index links

## Commands executed

| Command | Result |
| --- | --- |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 CODEX_TEMP_ROOT=<task-owned-build-root> /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_optional_prerequisite_status` before the source fix | failed as expected: the new postcondition suite reported five failures and six errors, including both forged-marker cases that the old runner incorrectly allowed. |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 CODEX_TEMP_ROOT=<task-owned-build-root> make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-optional-prerequisite-status` after the source fix | passed: 18 focused tests, including forged `stdout`/`stderr` markers, an unapproved marker, a real missing-APXS/header preflight, a usable-APXS control, recursive Make, and the actual Apache lint target. |
| Retained original stderr and stdout spoof probes through the patched runner | passed: each probe returned `77` with `allowed_by_contract: false`, `reason: "unclassified direct blocked exit code 77"`, and `status_source: "child_exit_code"`. |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -c '<compile selected files>'` | passed: `ci/tools/run-check-status.py` and `tests/test_optional_prerequisite_status.py` compiled in memory without checkout bytecode output. |
| `rtk shellcheck -x ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh` | failed on existing diagnostics at lines 4 and 86–87 (`SC1007` and `SC2086`); this change removes only the status marker at line 31 and does not alter those unrelated command-construction lines. |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs` | failed because this sparse worktree does not materialize linked Framework documentation; after the Change Record headings were corrected, the checker reported no error for this Change Record pair or its README links. |
| `rtk git diff --check` | passed. |
| `rtk env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 CODEX_TEMP_ROOT=/var/tmp/codex/ModSecurity-conector /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_optional_prerequisite_status` | passed: 20 focused tests. The SonarCloud `python:S8495` follow-up preserves `APXS_BIN` → `APXS` → `CI_APXS_BIN_CANDIDATES` → fallback priority, has one candidate-return path, and exercises an absolute configured APXS with an empty `PATH`. |

## Runtime evidence

Not applicable. This is a CI status-channel correction. It neither starts a
connector host nor establishes HTTP, CRS, MRTS, or lifecycle evidence.

## Checks not run and rationale

`rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile ci/tools/run-check-status.py tests/test_optional_prerequisite_status.py` was blocked because `py_compile` attempts to create checkout-local `__pycache__` despite `PYTHONDONTWRITEBYTECODE=1`, and this worktree correctly rejects that write. The focused import-and-execution tests above passed without bytecode output.

Full lint, connector builds, runtime harnesses, and generator/report tests were
not run in this isolated remediation worktree. The original draft PR #56 head
`63f4c9694f3f1c1372ce6db86ea1f88a38f01a92` was committed, pushed, and had 33
passing GitHub checks with CodeQL and the SonarQube Cloud Quality Gate passing.
The SonarCloud API nevertheless reports task-owned open issue
`AZ90uTmr7VSiD7VvMb8Y` (`python:S8495`) at this function, so this follow-up
requires a fresh exact-head CI, CodeQL, SonarQube Cloud, and review cycle
before any `verified_pr` claim. No merge is authorized.

## Known limitations

The Apache preflight intentionally covers only this lint allowance. Other
status-wrapper call sites are separate root causes and are not changed here.

## Remaining risks

The preflight trusts the job's configured APXS candidate inputs, but it never
trusts a child result to authorize a block. A usable APXS can still lead to a
later genuine child failure or unclassified `77`, which remains red.

## Final diff and review status

Focused regression coverage, in-memory syntax validation, and `git diff
--check` passed. Required Change Record headings, reciprocal language links,
and both README index links were manually validated. The bilingual target still
fails only because this sparse worktree lacks linked Framework documentation;
it reports no error for this Change Record pair. The initial implementation was
delivered through draft PR #56; this SonarCloud follow-up remains
`remediation_required` until its new exact PR head is pushed and independently
verified. No merge or runtime-evidence claim was made.
