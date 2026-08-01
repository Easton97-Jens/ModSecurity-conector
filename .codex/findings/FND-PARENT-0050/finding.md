# FND-PARENT-0050 — Parent ModSecurity v3 generic Git acquisition remediation is locally verified; hosted evidence is pending

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0050 |
| Category | security_hardening |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / medium / validated |
| Status / feasibility | fixed / feasible_now |
| Release blocker / security relevant | true / true |
| Historical validated Parent revision | 2404f66d3919bda6f2e5a721f5e070f1cb61cb68 |
| Current reviewed Parent candidate | c53ea5de38bc884fdd7f8b686005f6c22ee0a628 |
| Framework revision consumed read-only | 77d73decd094a8f289fbe0ef2582f12430923e24 |
| Parent impact | The direct generic-acquisition defect is remediated locally; #55 remains release-blocked until fresh exact-head runtime evidence and the FND-CROSS-0001 gate pass. |
| MRTS impact | none; original MRTS remains read-only |

## Historical observation and current disposition

The retained historical source-to-sink trace validated a control-order and evidence-integrity gap. At historical Parent revision 2404f66d, the route could materialize a generic GitHub HTTPS ModSecurity v3 checkout and invoke the shared build before Framework immutable OWASP-origin, approved-commit, and reviewed-recursive-topology admission ran. The intentionally stopped partial build is excluded from FND-CROSS-0001 runtime evidence.

Current Parent candidate c53ea5d removes that generic V3 acquisition path. After the Framework configuration guard passes, Parent reserves an entry-marker-owned but absent staging child and invokes the public Framework ci_provision_approved_modsecurity_v3_checkout API at the revision already recorded by the Parent gitlink. Parent then re-verifies the checkout, reads metadata through verified /usr/bin/git with a minimal scrubbed environment, writes a complete managed-cache marker, and atomically publishes only after all of those controls pass. The existing build-time Framework checkout guard remains defense in depth.

There is no ModSecurity v3 call to prepare_git_component in the new route. Rejected configuration, bridge, or post-provision verification paths return blocked records and cannot fall back to generic Git or publish unverified staging. The direct static/control-order defect is therefore remediated and locally regression-tested. This finding remains open because local controls do not substitute for a fresh exact-head hosted strict/full producer, terminal evidence gate, review, SonarQube, or protected integration.

## Scope and boundary

Affected Parent content is limited to:

- ci/provisioning/components/prepare-runtime-components.py;
- tests/test_prepare_runtime_components.py; and
- the existing English/German Change Record pair for PR #55.

Framework source, Framework/MRTS gitlinks, MRTS source, branches, commits, and pull requests are unchanged. Framework revision 77d73de is used read-only; it already exposes the reviewed public provisioning API. No current task action requires a Framework or MRTS delivery.

## Root cause and remediation

The historical Parent route classified ModSecurity v3 as a generic Git component and postponed immutable checkout admission until after acquisition and the shared build path. The corrected Parent route delegates fresh source creation to Framework's immutable public API, which owns the approved origin, full commit, recursive topology, fresh-root, and host-Git controls. Parent owns only safe staging reservation, re-verification, cache admission, and publication after Framework approval.

The exact candidate also prevents ambient Git/loader configuration from affecting Parent metadata reads by using verified /usr/bin/git, a fixed PATH, disabled global/system configuration, disabled hooks/fsmonitor, and a minimal environment.

## Acceptance criteria

1. Rejected V3 configuration cannot call the Framework bridge, generic Git, or a build sink. **Passed locally.**
2. An approved V3 source is acquired only through the Framework public fresh-destination bridge; Parent does not call prepare_git_component for V3. **Passed locally.**
3. A bridge or post-provision verification failure preserves a published cache, removes only its managed staging entry, and cannot write completion metadata or publish the rejected checkout. **Passed locally.**
4. The exact Framework provenance/fresh-root regression suite passes at the Parent-recorded Framework revision. **Passed locally.**
5. Fresh exact-head #55 evidence uses the legitimate strict/full producer, reaches the terminal gate, and satisfies FND-CROSS-0001 plus PR review, SonarQube, and branch-protection requirements. **Pending.**

## Validation plan

- Retain the historical evidence and the current local bridge-validation artifact; do not reinterpret stopped historical output as runtime evidence.
- Use the separate #74 Apache producer remediation to obtain the legitimate full-producer foundation without weakening its strict terminal gate.
- Reconcile #55 against the resulting master, then inspect its fresh exact hosted checks, FND-CROSS-0001 evidence, SonarQube, reviews, threads, and mergeability before protected integration.

## Evidence

Historical retained source-to-sink evidence:

- Candidate revision: 2404f66d3919bda6f2e5a721f5e070f1cb61cb68
- Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260723T162517Z-fnd-cross-0001-runtime-evidence-bcda7d1d/evidence/parent-modsecurity-v3-provenance-gap.md
- SHA-256: b18f34ca2f6a056e9fb4055d6f52bf22f64560645a97dece53f437da10d66fe
- The isolated partial build stopped with exit 130 immediately after the ordering result was confirmed and is excluded from runtime evidence.

Current retained local remediation evidence:

- Candidate revision: c53ea5de38bc884fdd7f8b686005f6c22ee0a628
- Artifact: .codex/runs/20260726T081500Z-pr55-framework-v3-bridge/evidence/local-bridge-validation.md
- SHA-256: ba0954d5d9c3e7c6bc31d558f55b9acc99b44ee93984c817aed1fba35d381f15
- Parent source/cache controls: 44 tests passed; Framework V3 provenance/fresh-root controls: 18 tests passed; CI-security contract, bilingual-documentation, and whitespace checks passed.
- This is local validation only, not hosted runtime, delivery, or master evidence.

## Dependencies and residual risk

Framework's public bridge at 77d73de is already available through the recorded Parent gitlink, so no Framework source delivery or Parent gitlink change is a remaining dependency. The remaining delivery dependencies are the separate #74 Apache runtime-producer remediation, FND-CROSS-0001 legitimate runtime evidence, and #55 exact-head PR controls.

No risk is accepted. Parent PR #55 must not be integrated on the historical stopped run or on local controls alone. Until the fresh exact-head evidence passes, the finding remains a release blocker even though the direct generic acquisition route has been removed.

## History

- 2026-07-23T16:25:17Z — Retained isolated source-to-sink evidence validated the historical Parent V3 control-order gap; the partial build was stopped and excluded from FND-CROSS-0001 runtime evidence.
- 2026-07-23T17:41:30Z — Static review of candidate 59321ca found that its Framework configuration guard still delegated V3 acquisition to generic bare Git before the later checkout guard.
- 2026-07-26T08:15:00Z — Normal Parent PR #55 commit c53ea5d replaced the generic V3 path with the current Framework public bridge. Parent 44-test and Framework 18-test controls passed; fresh hosted evidence remains pending.
