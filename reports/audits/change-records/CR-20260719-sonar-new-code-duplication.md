# Change Record: SonarQube Cloud new-code duplication remediation

**Language:** English | [Deutsch](CR-20260719-sonar-new-code-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260719-sonar-new-code-duplication` |
| Date (UTC) | `2026-07-19` |
| Base revision | `79d224a1c20d648974923630c7746d4b6511f9be` |
| Tracking | SonarQube Cloud Draft PR #61 new-code duplication remediation; no standalone finding was created. |
| Boundary | Parent `common` event JSON serialization and its focused smoke test only; Framework and MRTS are unchanged. |

## Motivation and problem statement

The exact-head SonarQube Cloud analysis for Draft PR #61 reported 106 new
lines, two new duplicated lines, two new duplicated blocks, and a new-code
duplication density of `1.8867924528301887%` (displayed as 1.9%). Both blocks
were in `common/src/event.c`: the shared validation body of required transport
case IDs and optional transport metadata values.

## Acceptance criteria

- Preserve the existing required-versus-optional empty-value semantics.
- Keep the existing length and permitted-character validation for nonempty
  transport tokens.
- Preserve omission and truncation when any optional transport metadata value
  is invalid, while retaining serialization for a valid control.
- Remove the reported duplicate validation body without a SonarQube setting,
  suppression, exclusion, or quality-gate workaround.
- Obtain a fresh PR-head SonarQube Cloud readback after the follow-up commit.

## Implementation decision and rationale

A private `is_bounded_transport_token(const char *value, int allow_empty)`
now owns the existing `strlen` limit and ASCII token-character predicate.
`is_bounded_transport_case_id` calls it with `0`; the optional-value wrapper
calls it with `1`. This keeps all existing callers and their contracts intact,
avoids a public API change, and removes only the duplicated implementation.

The focused Common helper smoke test adds an invalid `reset_by` value containing
a space. It verifies `truncated`, omission of both optional provenance fields,
and absence of the rejected value. A separate valid `reset_by`/`reset_code`
control verifies normal serialization and `truncated:false`.

## Security impact

The changed validators control transport/correlation metadata before it enters
the event JSON provenance fragment. The refactor retains the required case-ID
rule, optional null/empty allowance, 128-byte bound, token alphabet, and the
all-or-nothing clearing of five optional values. An independent focused review
found no plausible security candidate when those invariants are retained.

## Changed files

- `common/src/event.c`
- `ci/checks/common/check-common-helpers.sh`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| `rtk env BUILD_ROOT=<task-owned run>/build/gcc-c17 TMPDIR=<task-owned run>/tmp CC=gcc make check-common-helpers-c17` | passed with GCC 15.2.0 and `-std=c17 -Wall -Wextra -Werror`. |
| `rtk env BUILD_ROOT=<task-owned run>/build/clang-c17 TMPDIR=<task-owned run>/tmp CC=clang make check-common-helpers-c17` | passed with Clang 21.1.8 and `-std=c17 -Wall -Wextra -Werror`. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned run>/tmp make check-common-security-contract` | passed: `common security contract: ok`. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned run>/tmp make check-common-flow-integrity` | passed: `common flow integrity: ok`. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned run>/tmp make check-bilingual-docs` | blocked by missing Framework link targets in the sparse worktree; after correcting the Change Record headings, it reported no error for this pair. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned run>/tmp make check-doc-links` | blocked by the same missing Framework link targets; no changed Parent link was reported. |
| `rtk git diff --check` | passed after the documentation additions. |

## Runtime evidence

Not applicable. This is a private Common validation refactor and smoke-test
addition; it does not start a connector host or make a runtime compatibility
claim.

## Checks not run and rationale

- `make check-common-helpers-c23` is advisory and was not selected because the
  changed C code has no C23-specific behavior; the required C17 checks passed
  with both available compilers.
- Full connector builds, host runtime harnesses, Framework checks, and MRTS
  checks were not run because no connector, Framework, or MRTS behavior changed.
- Fresh exact-head SonarQube Cloud and GitHub PR checks are delivery evidence,
  not local evidence; they must be observed before any verified-PR claim.

## Known limitations

This record captures the pre-remediation SonarQube Cloud metric. The final
zero-duplication result is not asserted until the new commit's PR analysis is
observed and bound to its exact SHA.

## Remaining risks

An inverted `allow_empty` argument could either accept empty case IDs or reject
legitimate empty optional values. The required/optional wrapper calls and the
new negative-plus-control smoke coverage mitigate that risk. No raw transport
identifier or request-derived payload is retained by this record.

## Final diff and review status

The scoped implementation, independent security review, C17 smoke checks,
Common security/data-flow contracts, and `git diff --check` have passed. The
documentation commands are blocked only by pre-existing missing Framework link
targets in this sparse worktree and report no error for this Change Record
pair. Scoped diff review, commit/push, and exact-head SonarQube Cloud evidence
are assessed through PR delivery; this record does not authorize a merge.
