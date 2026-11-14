# Change Record: CR-20261114-fzipi-archive-integration

**Language:** English | [Deutsch](CR-20261114-fzipi-archive-integration.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261114-fzipi-archive-integration |
| Date (UTC) | 2026-11-14 |
| Base revision | `b1017969f766209eb9401820a4aca01d71180636` |

## Motivation and problem statement

Parent b1017969 selected Framework 2cc331d8. Five Parent workflows stopped at the
stale generated test archive. The complete local native path also exposed stale
Apache/HAProxy source contracts and a Common checker that treated split-owner
Framework source paths as Parent-relative paths. The separate [Framework PR 173](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/173)
repairs those contracts without weakening their checks.

## Acceptance criteria

Select the verified Framework master, preserve product behavior and all other
component/tool/runtime versions, retain 100 automatic cases and unchanged MRTS,
and pass native publication reconstruction and new-pin checks. Current-head
Parent CI/Sonar must pass before the separately authorized master integration.
No prior-head result qualifies a future Parent commit.

## Implementation decision and rationale

Select actual squash master `939d1718b7548a36ff7a550080ed8b811aad8a98`, not PR
head `c250f92d34e8e7f04304f54067d049acd3b76c3c`. Both have exact Git tree
`ddd24ee9293efeba21ee151b2439c4a1cb71a301`. Framework changes are three strict
checkers, four regression modules, canonical archive and EN/DE record. The source
binding updater reports VERIFIED without inventory changes. The regenerated
archive describes 8211 definitions; it does not select or execute them all.

Use the existing native synchronizer and its fixed target registry. Its input is
an immutable Git extraction of Framework `ci/lib/common.sh`, SHA-256
`38be065c9214c1953cba6baec49c3cf3e7ae5a369dec61ba56e59b36be083f87`,
under the allowed runner temporary root. The tool parses this file as data; it
never sources it. Two initial validation attempts rejected checkout paths outside
that root with exit 2. The documented extracted-snapshot path passed unchanged
controls; no input boundary or validator was modified.

## Changed files

Framework gitlink, Parent project-version lock, 22 generated workflow projections
and this new EN/DE record pair: 26 paths. No Parent product source or MRTS content
changes. Framework implementation/test changes were delivered separately in PR173.

## Commands executed

The actual shell entry was `rtk bypass python3`; it launched `rtk bypass bash -c`
with the external archive-pin `context.sh`, then these RTK child commands using
the configured Framework Python. Context binds Parent b1017969, Framework939d1718,
profile h1, explicit roots and external output/build/temp/log directories.

- `ci/tools/sync-framework-component-versions.py --validate`: 0 before/after sync.
- Same tool `--sync` and `--check`: 0 / 0. Inputs include the extracted common
  snapshot, exact Framework SHA, existing read-only Framework object root and
  explicit unchanged MRTS SHA `ee2174431c4edf97e66afe32558ce8454deb2397`.
- Native `ci/tools/new-change-record.py create --name fzipi-archive-integration --base-revision b1017969f766209eb9401820a4aca01d71180636 --date 2026-11-14`: 0.

Native `--verify-primary --base b1017969f766209eb9401820a4aca01d71180636`,
`rtk make check-active-inventory` and complete `rtk make quick-check` passed (0).
The full 660705-byte quick-check log was Secrets-checked in overlapping bounded
chunks before inspection: real Apache/NGINX/HAProxy C17 compilation, Common
security, documentation and final syntax/whitespace steps passed. All 23 existing
regular projections equal their trusted-base bytes with only the exact Framework
SHA replacement. All other component/tool/runtime bytes remain unchanged. Final
record/archive and staged-byte checks are separate precommit checks.

## Security impact

Keeps strict saturating-counter/native-capture checks and full Common scan scope.
No rule suppression, weaker compiler warning, changed gate or WAF bypass. Previous
exact operator approvals are bound to different indices/Framework commits and
are not transferred. Any required new exact admission remains separate.

## Runtime evidence

External Framework evidence: 71 focused tests and complete native quick-check
passed before publication. All nine Framework PR-head workflows passed (seven PR and two push runs).
Full Sonar log binds SCM c250f92d, terminal gate PASSED and EXECUTION SUCCESS;
complete PR173 API readback: zero unresolved issues, zero hotspots in both review
states, gate OK and 0.0% new duplication. Authoritative merge/master and tree
equality are verified. These are Framework delivery results, not new Parent CI
or host runtime. No new host runtime campaign is required by this pin-only change.

## Known limitations

Archive availability is not execution of 8211 definitions. Strict static contracts
are not general C reachability or all-host runtime proofs. New Parent local checks passed; current-head remote delivery evidence is pending.
The subsequent Framework master analysis is separately failed: 115 pre-existing
issues (32 security reports, 83 code smells), all created before this task and
none in PR173 changed files. The user explicitly selected task changes on zero
and legacy issues separately. No rule, gate, finding disposition or baseline was
changed to hide that result.

## Remaining risks

A changed index or Framework target invalidates an exact operator proposal.
Parent merge remains conditional on current-head checks and any required exact
admission; no previous receipt is broadened or reused for a different scope.

## Checks not run and rationale

No new Parent commit, CI or master merge is claimed. Local new-pin checks passed;
final record/staged-byte verification and exact admission remain pending. MRTS remains read-only at the unchanged SHA above;
no initialization, update, checkout or full materialization is performed.

## Final diff and review status

Canonical scaffold identity/date/base retained. Native sync/check, worktree
primary verification, inventory and complete quick-check passed. Existing regular
projections reviewed as SHA-only replacements. Record review, staged-byte
verification and exact admission precede normal commit/push; new-head Parent
CI/Sonar remain mandatory before authorized master integration.
