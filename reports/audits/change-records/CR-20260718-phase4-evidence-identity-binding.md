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
`FND-PARENT-0027` is `fixed`; this record does not claim cross-repository
closure because the Framework-authoritative checker requires the separate
Framework-owned identity-binding remediation `FND-CROSS-0006`.

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

## Delivery evidence (observed 2026-07-18 UTC)

- The implementation commits were pushed on
  `agent/harden-evidence-phase4-binding`:
  `8b7b13b294fe4043fb4002c1cb96ba3de72986f8`
  (`ci: bind phase4 evidence identity`) and
  `0124b0d685c69129d4aeace8eff75ccc288e7a8e`
  (`ci: wire phase4 identity checks into promotion gates`).
- Draft PR [#57](https://github.com/Easton97-Jens/ModSecurity-conector/pull/57)
  was `OPEN` against `master` at observation. At that observation, local `HEAD`,
  `origin/agent/harden-evidence-phase4-binding`, and the PR head all resolved
  to `0124b0d685c69129d4aeace8eff75ccc288e7a8e`.
- The PR check summary at that observation reported 33 passed checks and 0 failed checks.
  CodeQL succeeded (check run `88073814250`); SonarCloud Code Analysis
  succeeded (check run `88073815941`, Quality Gate passed with 0 new issues
  and 0 security hotspots).
- The delivery disposition at that observed head was
  `verified_pr_parent_consumer_scope`: the Parent-consumer PR head is
  verified, but that scoped result is not a repository-wide `verified_pr`
  claim while high, Framework-owned `FND-CROSS-0006` remains `validated`.
  GitHub reports no review decision, and no merge is authorized or performed.

## Checks not run and rationale

No connector build, runtime harness, CRS/MRTS matrix, or Framework change was
run. They remain outside the Parent-consumer validation scope. `make
check-doc-links` was not run because its target invokes the Framework
documentation checker; the current task excludes Framework work and this
worktree has no populated Framework documentation targets. The exhaustive
`security-diff-scan` worker workflow was not run because all available
delegation slots were already occupied; its capability preflight returned
`ready`. The current CodeQL, SonarCloud, GitHub Actions, commit, push, and
Draft-PR facts are recorded above for the observed exact PR head SHA; no merge
occurred.

## Known limitations

This correction validates identity fields already present in the Parent
canonical event model. It deliberately does not create, sign, or alter a
Framework producer contract. A runtime producer that omits any required field
now fails closed and needs a separately scoped producer remediation if that
occurs in an actual harness run. `FND-CROSS-0006` (`Framework authoritative
Phase-4 checker does not bind promoted events to selected workload identity`)
remains a high, `validated`, Framework-owned finding and prevents a
cross-repository completion claim.

## Remaining risks

This change does not provide a signature or immutable manifest chain for a
malicious producer or result file; those are separate evidence-authenticity
boundaries. It does ensure that this validator no longer treats a matching
`rule_id` and phase as sufficient identity evidence. The Framework-authoritative
checker remains a separate high-risk boundary until `FND-CROSS-0006` is
remediated and verified in its owning repository.

## Final diff and review status

The first identity-matcher commit alone did not wire the Parent checks into
the actual first-byte and promotion Make targets; an independent security
review identified that reachability gap. The follow-up commit
`0124b0d685c69129d4aeace8eff75ccc288e7a8e` and its static contract test
remediated that Parent reachability issue. The exact-head delivery evidence is
recorded above: the Parent-consumer result is
`verified_pr_parent_consumer_scope`, while `FND-CROSS-0006` prevents a
repository-wide completion claim. The PR remained Draft at that observation;
this documentation correction requires a fresh exact-head review before any
new delivery claim. No merge is authorized or performed.
