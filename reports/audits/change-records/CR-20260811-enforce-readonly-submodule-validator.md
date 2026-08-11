# Change Record: enforce readonly submodule validator

**Language:** English | [Deutsch](CR-20260811-enforce-readonly-submodule-validator.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260811-enforce-readonly-submodule-validator |
| Date (UTC) | 2026-08-11 |
| Base revision | 4749c02c6dd5e285c4309b4e69b0bb28ae459e48 |
| Delivery status | Implementation record; final exact-head hosted-validation, security-scan, and delivery evidence is retained in the associated PR and scan evidence |

## Motivation and problem statement

The Framework-submodule updater validates a resolved candidate before a
separate publisher may propose a Parent gitlink update. Reader documentation
must accurately state the intended filesystem and privilege boundary without
turning the implementation description into unobserved hosted or security
evidence. A narrow one-task validation-only invocation is also required so the
exact head of the task-owned/reviewed Parent branch
`fix/ci-enforce-readonly-submodule-validation` can receive hosted validator
evidence without making publication eligible.

## Acceptance criteria

- The validator applies `umask 077` before creating a fresh private `mktemp`
  root under `RUNNER_TEMP` and again inside the isolated candidate shell before
  candidate output; all supported, legitimate workflow output roots are
  enforced beneath the candidate's private external child.
- Parent and Framework source trees and their `.git` metadata are read-only to
  the candidate.
- The candidate runs as the dedicated non-login, non-sudo
  `modsecurity-validator` identity through one `sudo -n -u` / `env -i` entry.
- `make quick-check` is unchanged.
- The validator does not receive production write permission; that permission
  remains only with the separate publisher.
- Manual `workflow_dispatch` with `validate_only: true` is restricted to the
  canonical Parent repository `Easton97-Jens/ModSecurity-conector` and the
  task-owned/reviewed `fix/ci-enforce-readonly-submodule-validation` branch;
  it is not a facility to execute arbitrary untrusted Parent refs. It uses the
  dispatched `github.sha`, forces validation even when candidate and gitlink
  are equal, and makes the publisher ineligible.
- The task-owned/reviewed Parent workflow and helper SHA are trusted before
  root-side setup; the Framework candidate remains untrusted sandbox-governed
  code. The branch allowlist is a guardrail, not protection from a hostile
  same-repository writer; that threat model requires branch protection or
  environment approval.
- The validation-only invocation is distinct from the authorized post-merge
  updater dispatch on `master` with `validate_only` false.
- Trusted setup probes verify Parent/Framework write rejection, sudo rejection,
  and external-write success before the quick check.
- A full post-lock Parent/Framework source inventory must be exactly equal
  after the quick check, and the validator external tree must meet its
  fail-closed ownership, type, permission, symlink, and hard-link contract.
- English and German documents and Change Records carry the same material
  facts and evidence limits.

## Implementation decision and rationale

The documented contract applies `umask 077` before its fresh private `mktemp`
root under `RUNNER_TEMP` and again inside the isolated candidate shell before
candidate output. A root-side helper locks the Parent and Framework trees and
their `.git` metadata root-owned and non-writable before candidate execution,
making source/Git state immutable to the candidate. All supported, legitimate
workflow output roots are enforced beneath its private external child. The
candidate enters once through `sudo -n -u` with `env -i`, no user site, and
external `HOME`, Git configuration, pip cache, bytecode cache, build, log, and
cache roots beneath that child. Trusted probes precede the
unchanged `make quick-check`. The validator is read-only; only the separate
publisher retains the narrowly scoped production-write boundary after
validation.

For exact branch-head evidence, manual `workflow_dispatch` may set
`validate_only: true` only in the canonical Parent repository on the
task-owned/reviewed `fix/ci-enforce-readonly-submodule-validation` branch. It
is not a general facility to execute arbitrary untrusted Parent refs. This path
checks out the dispatched `github.sha` in the resolver and validator, forces
the validation job even when the Framework candidate equals that dispatched
Parent gitlink, and explicitly excludes the publisher. It cannot create or
update a gitlink branch or pull request. It is not an untrusted Parent
pull-request/ref sandbox: the task-owned/reviewed Parent workflow and helper
SHA are trusted before root-side setup, while the Framework candidate remains
untrusted sandbox-governed code. A hosted success would be functional evidence
only for that reviewed SHA. The branch allowlist is a guardrail, not protection
against a hostile same-repository writer; that threat model requires branch
protection or environment approval. The separately authorized post-merge
updater dispatch runs on `master` with `validate_only` false; it validates the
trusted-default-branch transition and may reach the constrained publisher after
validation. The two invocations are not interchangeable, and validation-only
mode grants no delivery authority.

The root-side helper inventories both locked source trees before candidate
execution and verifies exact post-check equality. The inventory records path,
type, size, mode, UID, GID, and link count, plus SHA-256 for regular files and
link text for symbolic links. It separately fail-closed scans the external
tree, permitting only validator-owned directories and regular files without
group/other writes and rejecting special objects, symbolic links, and
source-tree hard links.

This implementation record documents the intended contract. It does not assert
final exact-head hosted-validation, security-scan, or delivery results; those
are retained in the associated PR and scan evidence.

## Security impact

The relevant boundary is untrusted candidate execution versus Parent and
Framework source/Git state. The documented design prevents the candidate from
writing either repository or its `.git` metadata and enforces all supported,
legitimate workflow output roots beneath its private external child. This is
not a general kernel namespace and does not prove that malicious candidate code
cannot write arbitrary unrelated globally world-writable host locations. Final
security-scan evidence is not asserted in this implementation record and is
retained in the associated scan evidence. The Parent
workflow/helper SHA is trusted before root-side setup; `validate_only` does not
sandbox an untrusted Parent ref. Its branch allowlist is not protection against
a hostile same-repository writer, which requires branch protection or
environment approval.

## Changed files

- `.github/workflows/update-submodules.yml`
- `ci/tools/prepare-readonly-submodule-validation-sandbox.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_prepare_readonly_submodule_validation_sandbox.py`
- `docs/build/README.md`
- `docs/build/README.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260811-enforce-readonly-submodule-validator.md`
- `reports/audits/change-records/CR-20260811-enforce-readonly-submodule-validator.de.md`

The implemented boundary is in `.github/workflows/update-submodules.yml` and
`ci/tools/prepare-readonly-submodule-validation-sandbox.py`, with contract
coverage in `tests/test_ci_security_workflows.py` and
`tests/test_prepare_readonly_submodule_validation_sandbox.py`. The change does
not modify the Makefile, Parent gitlink, Framework, or MRTS.

## Commands executed

The following Parent checks were independently run by the root task and
reported as direct evidence:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_prepare_readonly_submodule_validation_sandbox tests.test_ci_security_workflows` exited 0: 38 tests ran, 37 passed, and 1 was an expected skip because the `nobody` UID/GID is unavailable in the user namespace.
- `PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` exited 0, including 26 CI-workflow tests and validate-only actionlint, zizmor, and gitleaks-lock checks.
- `make check-bilingual-docs` reran after the validation-only branch-scope
  documentation correction and passed (`bilingual docs ok`).
- `git diff --check` exited 0 without output after the validation-only
  branch-scope documentation correction.

## Runtime evidence

This implementation record does not assert final exact-head hosted-runtime or
validation, publication, pull-request, merge, or other delivery results; those
are retained in the associated PR evidence.

## Checks not run and rationale

- `make quick-check` — unchanged by this task; no candidate execution was
  run locally as part of the supplied evidence.
- Hosted `update-submodules.yml` validation, including `validate_only: true` —
  final exact-head hosted evidence is not asserted here and is retained in the
  associated PR evidence.
- Security scan — final security-scan evidence is not asserted here and is
  retained in the associated scan evidence.
- `make check-bilingual-docs` initially failed because this Change Record did
  not have the checker-required headings and the baseline clone has
  uninitialized Framework link targets; after correction, its rerun passed and
  is recorded above.

## Known limitations

The record documents the intended boundary from the scoped implementation
requirements. It does not itself provide independent evidence of runner
identity behavior, filesystem permissions, or final hosted execution at the
dispatched SHA. The scoped source/output contract is not evidence of general
host filesystem isolation.

## Remaining risks

Correct operation depends on the workflow implementation continuing to create
the external private child and apply the dedicated identity and read-only
permissions before candidate execution. The contract does not contain
unrelated globally world-writable host locations that malicious candidate code
could use outside the supported workflow output contract. Final runtime,
hosted, scan, and delivery evidence remains in the associated PR and scan
evidence.

## Final diff and review status

Scoped English/German parity and `git diff --check` review passed. This
implementation record asserts only its local documentation validation; final
exact-head hosted-validation, security-scan, and delivery evidence is retained
in the associated PR and scan evidence.
