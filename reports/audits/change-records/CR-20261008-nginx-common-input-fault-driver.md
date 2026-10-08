# Change Record: CR-20261008-nginx-common-input-fault-driver

**Language:** English | [Deutsch](CR-20261008-nginx-common-input-fault-driver.de.md)



## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-common-input-fault-driver |
| Date (UTC) | 2026-10-08 |
| Base revision | `48243d5f77a6ae52b52729b6d6a2447229f6fab6` |

## Motivation and problem statement

Two Required adapter-input faults need genuine requests reaching the actual Common guard, not malformed wire syntax or driver-produced events.

## Acceptance criteria

Exact own-worker/native-transaction/POST-URI injection, real mapper return0/diagnostic, actual400/native protocol error/noRule, bounded cleanup, and wrong-target controls.

## Implementation decision and rationale

Load an attempt-local interposer into only the owned native master. Delegate unchanged real transaction creation and real Common validator; inject one request-copy only at the matching exported validation boundary.

## Changed files

New dedicated driver, native interposer, compiled simulated-scope fixture, two focused test modules and this bilingual record.

## Commands executed

Driver missing-file RED then2GREEN; compiled scope missing-file RED then2GREEN with six wrong-target controls; C17Wall/Wextra/Werror fixture build0. Common invariant4GREEN. Isolated old-cache focus: header positive actual400/Commonreturn0/native protocol_error and driver0; wrongTX driver1/405/noledger/noevent; old bodyguard actualreturn1/405 remains RED. Cleanup verified/noNGX after.

## Security impact

No product hook, global fault switch, fabricated Common event or weakened isolation. Root-owned0600 ledger only; native library fixture is hashed and request-bound.

## Runtime evidence

Native diagnostics retained under task stream-a-input-r1/r2 with actual Root/nobody/maps/config/fault/access/events/cleanup. Artifact build b740/a904 is distinct from newer helper source48243/Framework210a33c. R1 initial helper expected phase1_error, but actual Common protocol view emits protocol_error; strict helper corrected and fresh header R2 passed. Simulated process controls remain unit-only. Body-positive/new-module and final canonical coverage are not claimed.

## Known limitations

Requires rebuilt native module containing the separately committed body-pointer guard, coordinator native slot, Framework validator and central closed receipt integration.

## Remaining risks

Native event/diagnostic and exact raw artifact hashes must agree; old-cache body acceptance is a RED control, not relabeled as new code.

## Checks not run and rationale

Protected Exact-Head, full E2E, full lint and remote checks not run. Body-positive requires newly built product guard; header diagnostic does not establish final Exact-Head PASS.

## Final diff and review status

Owned new files only. Separate commit after bounded native focus; no push, merge, amend, gitlink or MRTS changes. Central receipt validation remains coordinator-owned.
