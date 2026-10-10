# Change Record: CR-20261008-nginx-native-required-framework-pin

**Language:** English | [Deutsch](CR-20261008-nginx-native-required-framework-pin.de.md)

Separate Framework Gitlink update; this record does not certify a native run.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-required-framework-pin |
| Date (UTC) | 2026-10-08 |
| Base revision | `767de5bf4e901f256dffbca76547af4ee6b54757` |

## Motivation and problem statement

The Parent's integrated selected-native dispatch needs the Framework's closed
operation descriptors, original evidence authority and strict Canonical mapping.
Its old Gitlink did not include those coordinated contracts.

## Acceptance criteria

Pin the published, clean Framework commit
`61b9f33ad44fa92b916059d2f3e1944c6a4f1bf3` separately. Preserve all 97 selected
Required identities and the MRTS Gitlink. Do not weaken evidence validation or
claim that a pin or passing source tests closes the 45 fresh-runtime gaps.

## Implementation decision and rationale

Use the normally published Framework follow-up after its complete native lint
and No-CRS contract suite pass. The Framework adds 42 explicit native routes,
strict original-byte authority/receipt validation and the approved configuration
contracts; the current plan has 42 native, 10 configuration, 31 derived and 14
YAML invocations. No additional Parent dispatch change is needed for this pin.

## Changed files

`modules/ModSecurity-test-Framework` and this EN/DE Change Record pair only.
The Framework's `tools/MRTS` remains
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`; neither `.gitmodules` is changed.

## Commands executed

RTK-proxied Framework `make test-no-crs-contract`: 385 tests, exit 0.
RTK-proxied Framework `make lint`: exit 0, including provenance, workflow,
catalog and documentation gates. Parent `make lint` at the base revision:
exit 0. Actual Framework Git HEAD, clean worktree, Gitlink and regular files
were inspected; normal push, `git ls-remote` and PR API readback agree on the
new Framework SHA. PR #137 remains OPEN/DRAFT with its base unchanged.

## Security impact

Selected Required records still need genuine evidence. Missing caller authority,
missing execution descriptors, foreign identities, contradictory native facts
and modified retained bytes remain rejected. No protected runner, trusted Base,
HostGate, validator or namespace guard is replaced or relaxed.

## Runtime evidence

No fresh integrated native execution is claimed by this update. The original
Canonical status remains NOT_EXECUTED. Earlier diagnostic artifacts are not
relabelled as evidence for this new Parent/Framework tuple.

## Known limitations

The final Parent trust-dependent tests must run after this committed Gitlink
and the matching clean local Framework checkout. Fresh revision-specific PR CI
and Sonar results remain distinct from the successful local Make checks. Ruff
is unavailable and its separate lint check has not run.

## Remaining risks

Actual native artifact provenance, every Required request/configuration/fault
observation, cleanup and final Canonical validation still require the fresh
integrated runtime. The protected workflow's independent Base and administrative
runner prerequisites remain unresolved; a local candidate run cannot satisfy them.

## Checks not run and rationale

Post-pin Parent focus checks and the complete native lifecycle have not run
before this pin commit because they require its clean exact Gitlink tuple.
No protected dispatch is attempted while trusted-Base prerequisites are missing.

## Final diff and review status

Scope is limited to the Gitlink and this paired record. The Framework history
and MRTS are unchanged. Review checks the exact published SHA and preserves the
distinction between source integration, local runtime and protected attestation.
