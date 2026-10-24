# Change Record: CR-20261008-nginx-native-fixture-followup-framework-pin

**Language:** English | [Deutsch](CR-20261008-nginx-native-fixture-followup-framework-pin.de.md)

Framework-only follow-up pin; no runtime success is claimed.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-fixture-followup-framework-pin |
| Date (UTC) | 2026-10-08 |
| Base revision | `ca8ac4b0598da65b178f670652047052cda7a531` |

## Motivation and problem statement

Generic Framework discovery incorrectly treated the native-only Reject source
fixture as an executable YAML case. Its missing generic expectation was correctly
rejected, causing five failures in the previous Parent focus. A separate
regular-file validator extraction closes the remaining Sonar complexity finding.

## Acceptance criteria

Pin the normally published, clean and tested Framework follow-up. Preserve all
97 selected Required identities, strict missing-native-proof rejection and the
MRTS Gitlink. Do not convert source gates into runtime acceptance.

## Implementation decision and rationale

Update only the Framework Gitlink from
`61b9f33ad44fa92b916059d2f3e1944c6a4f1bf3` to
`7db219af6b6e911b73de8b437f82e63efdb06bde`. The native-only fixture opts out of
generic discovery, not the Required native contract. The extraction preserves
regular-file ownership, mode, size, bytes and digest checks. Both Framework
causes remain separate commits; no history is rewritten.

## Changed files

`modules/ModSecurity-test-Framework` Gitlink and this EN/DE record pair.

## Commands executed

RTK-proxied Framework `make test-no-crs-contract`: 399 tests in 178.376s,
exit 0; full native `make lint`: terminal exit 0. Normal push and remote-ref
readback confirm the exact new Framework SHA. Independent scan at that SHA
closes all 16 tracked findings; no open/new issues, duplication 0.0% and hotspots
0. The two scaffold-lint CI checks were still pending at the last readback.
Parent `make check-bilingual-docs check-doc-links`, Change Record archive check
and `git diff --check` passed, exit 0. The nested Framework checkout matches
the new pin and actual MRTS remains clean and unchanged at
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`.

## Security impact

No validator, evidence, ownership, containment, freshness, warning or Quality
Gate is relaxed. Selected Required native cases still require their original
runtime proof; generic fixture omission is not native success.

## Runtime evidence

None from this pin. All 45 final runtime gaps remain open; original Canonical
NOT_EXECUTED and final-run validation count 0 remain unchanged.

## Known limitations

The complete Parent focus must rerun after this pin. Current-source binary,
module, actual requests, fault injection and full canonical evidence are still
required. Framework CI completion is distinct from its local lint and Sonar.

## Remaining risks

Unexpected runtime artifact refresh must fail closed in the planned local
no-egress run. Local candidate evidence is not protected Root attestation;
independent Trusted Base, workflow, runner and Host-Gate prerequisites remain
blocked.

## Checks not run and rationale

Post-pin full Parent focus, full E2E and protected workflow have not run yet.
Ruff remains unavailable; native lint success does not claim Ruff validation.
No MRTS, administrative integration, merge, retarget or undraft action is taken.

## Final diff and review status

The Framework source diff was reviewed independently and by the coordinator;
its full local gates are green and normal publication is verified. Parent diff
is confined to the new Gitlink and paired record; final runtime work remains.
