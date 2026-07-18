# Change Record: Phase-4 evidence identity binding

**Language:** English | [Deutsch](CR-20260718-phase4-evidence-identity-binding.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260718-phase4-evidence-identity-binding` |
| Date (UTC) | `2026-07-18` |
| Base revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Finding | `FND-PARENT-0027` |
| Boundary | Parent Phase-4 evidence validator, Parent Makefile promotion wiring, and Parent tests only; Framework and MRTS unchanged. |

## Motivation and problem statement

`matching_events` accepted a Phase-4 event only when its `rule_id` and
`phase` matched.  A copied or pre-positioned event could therefore satisfy a
first-byte or no-full-buffering PASS case even when it belonged to another
run, connector, selected native profile (through its canonical event-side
integration mode), or transaction.

## Acceptance criteria

- The canonical result and a Phase-4 event used for a promotion must match the
  selected connector, `run_id`, canonical native profile/integration mode,
  `rule_id`, phase, and the result case's `transaction_ids`.
- Missing identity metadata fails closed.
- Foreign run, copied connector, copied native integration mode for another
  selected profile, arbitrary wrong integration mode, and foreign transaction
  fixtures are rejected for both first-byte and no-full-buffer checks.
- A same-run native Apache control remains accepted.
- The actual Parent first-byte, no-full-buffering, and promotion targets invoke
  their corresponding Parent identity checks in addition to the Framework check.
- English/German Change Records and their README links state only observed
  local evidence; no Framework, MRTS, Git, or delivery action occurs.

## Implementation decision and rationale

The Parent checker derives the expected native identity from
`FULL_LIFECYCLE_IDENTITIES`, binds the canonical result to the selected
connector and CLI run ID, and requires `transaction_ids` already carried by
the canonical result case. The matcher rejects every event that lacks or
differs in any of those fields. This reuses the identity model already used by
the Parent six-connector core checker and changes neither a Framework producer
contract nor the evidence schema. A dedicated Parent Makefile helper now runs
the profile check for every strict gate and additionally runs the matching
first-byte, no-full-buffer, or promotion check for its corresponding target.
`host_profile` is result-level metadata validated before this matcher runs;
the event schema carries the canonical `integration_mode` that the selected
native profile maps to.

## Security impact

The corrected Parent trust boundary prevents a rule-and-phase lookalike from
being promoted by the Parent first-byte, no-full-buffer, or promotion target
as the current selected host's Phase-4 runtime evidence. The result boundary
validates the selected `host_profile`; the event boundary validates its
canonical native `integration_mode`. This record does not claim that
`FND-PARENT-0027` is closed: the Framework-authoritative checker requires a
separate Framework-owned identity-binding task.

## Changed files

- `Makefile`
- `ci/checks/evidence/check-full-lifecycle-evidence.py`
- `tests/test_full_lifecycle_evidence.py`
- `tests/test_full_lifecycle_gate_wiring.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260718-phase4-evidence-identity-binding.md`
- `reports/audits/change-records/CR-20260718-phase4-evidence-identity-binding.de.md`

## Commands executed

| Command | Result |
| --- | --- |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_full_lifecycle_evidence` before the matcher correction | Expected failure: the five requested spoofing classes and the alternate foreign-transaction class were accepted; the legitimate Apache control passed. |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_full_lifecycle_evidence` after the matcher correction | passed: 17 tests, including all negative fixtures and the legitimate Apache control. |
| `rtk env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_full_lifecycle_evidence tests.test_six_connector_core_completion` | passed: 19 focused Parent tests. |
| `rtk env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_full_lifecycle_gate_wiring tests.test_full_lifecycle_evidence tests.test_six_connector_core_completion` | passed: 20 focused Parent tests, including the static Makefile contract that reaches the Parent first-byte, no-full-buffer, and promotion checks. |
| `rtk make -n check-first-byte-before-response-end check-no-full-response-buffering check-full-lifecycle-promotion NO_CRS_RUN_ID=phase4-wiring-control ...` | passed: emitted the Parent profile check plus the target-specific Parent first-byte, no-full-buffer, and promotion commands. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -c '<check_change_record_pair(...)>'` against this English/German pair | passed: required headings, identity metadata, and bilingual pair invariants. |
| `rtk env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHON=/root/git/ModSecurity-conector/.venv/bin/python make check-bilingual-docs` | blocked by absent Framework documentation targets in this dedicated worktree; after the record-heading correction, the output reported no error in this Change Record pair. |
| `rtk git diff --check` | passed. |

## Runtime evidence

Not run. The verified evidence is a focused Parent unit/contract test of the
validator boundary; it is not a connector runtime or traffic claim.

## Checks not run and rationale

No connector build, runtime harness, CRS/MRTS matrix, CodeQL, SonarQube Cloud,
GitHub Action, commit, push, pull request, or merge was run. They require a
separate authorized delivery or runtime scope and, where applicable, an exact
pull-request head SHA. `make check-doc-links` was not run because its target
invokes the Framework documentation checker; the current task excludes
Framework work and this worktree has no populated Framework documentation
targets. The exhaustive `security-diff-scan` worker workflow was not run
because all available delegation slots were already occupied; its capability
preflight returned `ready`.

## Known limitations

This correction validates identity fields already present in the Parent
canonical event model. It deliberately does not create, sign, or alter a
Framework producer contract. A runtime producer that omits any required field
now fails closed and needs a separately scoped producer remediation if that
occurs in an actual harness run.

## Remaining risks

This change does not provide a signature or immutable manifest chain for a
malicious producer or result file; those are separate evidence-authenticity
boundaries. It does ensure that this validator no longer treats a matching
`rule_id` and phase as sufficient identity evidence.

## Final diff and review status

The first identity-matcher commit alone did not wire the Parent checks into
the actual first-byte and promotion Make targets; an independent security
review identified that reachability gap. This Change Record is updated with
the Parent-wiring remediation and its static contract test. The Framework
checker remains a separately owned boundary. Exact PR-head, CI, and review
evidence is recorded in the canonical finding rather than claimed here.
