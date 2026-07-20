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
  local and delivery evidence; they do not claim a Framework or MRTS action or
  a merge.

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
canonical native `integration_mode`. The Parent-consumer disposition of
`FND-PARENT-0027` is `fixed`, not `verified` or closed. The formerly separate
Framework-authoritative identity gap `FND-CROSS-0006` was independently
remediated by Framework PR #34 and verified on Framework master
`3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f`. Current Parent master records
the later Framework master revision
`efdbcbd98afeed0f39f8912ce1140aaa5742f507`; PR #57 has no Framework gitlink
delta. This Parent record neither claims a Framework/MRTS action nor changes
the separate default-branch SonarQube backlog `FND-SONAR-0002`.

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

## Delivery evidence

### Historical initial observation — 2026-07-18 UTC

- The implementation commits were pushed on
  `agent/harden-evidence-phase4-binding`:
  `8b7b13b294fe4043fb4002c1cb96ba3de72986f8`
  (`ci: bind phase4 evidence identity`) and
  `0124b0d685c69129d4aeace8eff75ccc288e7a8e`
  (`ci: wire phase4 identity checks into promotion gates`).
- The initial Draft-PR observation was bound to
  `0124b0d685c69129d4aeace8eff75ccc288e7a8e`; it is historical only and is
  not evidence for a later PR head.

### Current base-update observation — 2026-07-20 UTC

- The current task direction conditionally authorizes Parent-master
  integration only after every protection and exact-head gate. It does not
  authorize a Framework-master merge, MRTS action, direct master write, or
  bypass.
- GitHub normally updated Draft PR
  [#57](https://github.com/Easton97-Jens/ModSecurity-conector/pull/57) with
  current Parent master `9ef0619b9c00729c16b7056943d7843785223095`. The
  resulting PR head is the signed normal merge commit
  `7a36393797cc7ec7b1659e6823b74e0a58ec9f6e`, with the branch five commits
  ahead and zero behind that base. The task-owned worktree was then safely
  fast-forwarded, so local `HEAD`, remote branch, and PR head all matched this
  observation.
- At that exact observed head, all 39 GitHub check runs were terminal: 33
  passed and six were scope-supported skips, with no failed, cancelled, or
  pending run. The six strict ruleset contexts passed; CodeQL passed with zero
  open code-scanning alerts, and SonarCloud's Quality Gate passed with zero
  new issues and zero security hotspots.
- GitHub reported `OPEN`, `DRAFT`, `MERGEABLE`, and `CLEAN`; there were zero
  submitted reviews, review threads, inline comments, and requested reviewers.
  The current PR diff contains only eight Parent files. It contains no
  Framework, MRTS, or gitlink-path delta; both its base and head record
  Framework `efdbcbd98afeed0f39f8912ce1140aaa5742f507`. It therefore does not
  include the separate Framework Draft PR #36.
- This Change Record correction intentionally creates a new PR head when
  committed and pushed. The preceding exact-head checks and review are then
  historical evidence only: the new head requires a complete fresh
  GitHub-Checks, CodeQL, SonarCloud, review/thread, and final-diff cycle before
  readiness or any merge decision. No merge has been performed.

## Checks not run and rationale

No connector build, runtime harness, CRS/MRTS matrix, or Framework change was
run. They remain outside the Parent-consumer validation scope. `make
check-doc-links` was not run because its target invokes the Framework
documentation checker; this dedicated worktree has no populated Framework
documentation targets. The exhaustive `security-diff-scan` worker workflow is
not claimed for the current base-update observation; a focused independent
diff review found no concrete new bypass at
`7a36393797cc7ec7b1659e6823b74e0a58ec9f6e`. No exact-head remote check exists
for the yet-to-be-created documentation commit, so its complete fresh delivery
cycle remains required. No merge occurred.

## Known limitations

This correction validates identity fields already present in the Parent
canonical event model. It deliberately does not create, sign, or alter a
Framework producer contract. A runtime producer that omits any required field
now fails closed and needs a separately scoped producer remediation if that
occurs in an actual harness run. `FND-CROSS-0006` is now independently
verified on Framework master; this Parent-only PR neither closes
`FND-PARENT-0027` nor addresses the separate Framework default-branch
SonarQube backlog `FND-SONAR-0002`.

## Remaining risks

This change does not provide a signature or immutable manifest chain for a
malicious producer or result file; those are separate evidence-authenticity
boundaries. It does ensure that this validator no longer treats a matching
`rule_id` and phase as sufficient identity evidence. The Framework-authoritative
checker identity boundary has separately been verified through Framework PR
#34; the residual risk is not a claim that either #57 or this record changes
the separate Framework default-branch SonarQube backlog.

## Final diff and review status

The first identity-matcher commit alone did not wire the Parent checks into
the actual first-byte and promotion Make targets; an independent security
review identified that reachability gap. The follow-up commit
`0124b0d685c69129d4aeace8eff75ccc288e7a8e` and its static contract test
remediated that Parent reachability issue. A focused independent review of the
normally updated head `7a36393797cc7ec7b1659e6823b74e0a58ec9f6e` found no new
concrete security bypass, and its observed exact-head CI/CodeQL/Sonar evidence
is recorded above. This documentation correction makes that head historical;
after its own commit and push, a fresh exact-head review and all required
checks must pass before #57 can leave Draft or enter the conditional
Parent-master integration flow. No merge has been performed.
