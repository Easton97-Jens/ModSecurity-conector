# Change Record: CR-20261107-acceptance-profile-checksum-followup

**Language:** English | [Deutsch](CR-20261107-acceptance-profile-checksum-followup.de.md)



## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261107-acceptance-profile-checksum-followup |
| Date (UTC) | 2026-11-07 |
| Base revision | `f89da27a293ef044e59a9582e9c814f4dabe1433` |

## Motivation and problem statement

Close the remaining profile and dependency preparation gaps while preserving the previously resolved NGINX/Apache/HTX/SPOP/ext_proc regressions and the 100 standard cases. Continue Parent Draft PR #445 and companion Framework Draft PR #169 without merge.

## Acceptance criteria

Independently execute complete Envoy ext_authz and Traefik ForwardAuth response-companion paths and native Traefik TLS/H2 Safe/Strict behavior. Require phase/rule/request/transaction/response mapping, active peer isolation, follow-up and native cleanup. Final committed-pair repetition and current required hosted checks decide readiness.

## Implementation decision and rationale

Add an explicit admitted composite late-action policy with Safe default. Strict records an abort request separately from actual downstream reset. Typed observed companion transport termination closes incomplete native transactions without fabricating EOS or attributing an unknown endpoint. Bind retained lifecycle events to a bounded method/URI SHA-256. Native Traefik gains Safe(default)/Strict phase4Mode and preserves a completed P2 denial when the downstream proxy subsequently raises http.ErrAbortHandler. Other panics and incomplete streams still propagate. Flush accepted composite response chunks so small responses remain progressive. Complete logical profile phase-ownership masks remain unchanged; only their now implemented Strict-action admission flags change.

The current hosted advisory analysis also identified parseResult complexity in the composite middleware. Extract its existing terminal-flag predicate without changing the admitted opcode/flag/decision/status/value combinations; the existing full protocol regression suite remains authoritative.

## Changed files

Envoy composite service/coordinator/transport and Common-backend bridge; Traefik composite and native middleware; exact profile registry flags; profile-qualified capability reasons; native configuration templates and generated references; selected Framework gitlink, lock and 22 workflow projections; this paired record. Framework owns adapters, tests, immutable Apache metadata retrieval and native compiler inventory.

## Commands executed

Commands use RTK and explicit source roots/revisions. Preliminary actual-host diagnostics exercised all 24 new H2 IDs. Native Traefik Go tests executed 89 top-level tests / 195 unique leaf scenarios with zero skips; 13 reader controls and go vet passed. Final pair, affected unit union, native generators/archive/pins, all-policy inheritance and current hosted CI evidence are recorded in the external report; preliminary diagnostics do not qualify the delivered pair.

## Security impact

Keep TLS/host verification, private UDS ownership, bounded metadata, engine/host/wire separation, exact source/build/artifact admission and failure diagnostics. Unknown close causes remain rejected. No authentication, validation, scanner scope, compiler warning, branch rule or Quality Gate is weakened. The shared Common backend retains its actual identity separately from logical host/handoff identity.

## Runtime evidence

Each complete logical path executes its actual host and response companion. A test-only Framework observer enables native Traefik cleanup metadata; wire and native access records independently prove the physical connection. Fresh same-launcher preflights and before/after source admission are mandatory. Exact full SHAs, immutable dependency-source proof, case IDs, failures, cleanup and integrity receipts remain external.

## Known limitations

Plain unpaired authorization services remain request-only. SPOP empty-body framing and the current lighttpd H1 applicability boundary remain as documented. No sibling integration inherits another profile result. Comprehensive acceptance is a separate step.

## Remaining risks

The existing Sonar SSH receiver rejects issue POST transitions despite available server transitions. Twenty-three prior occurrences were independently reassessed, but no server closure is claimed without saved-status readback. Existing C++20/C++23 advisory failures and 84 legacy inventory findings remain separate. Actual final hosted Sonar and Apache CRS/aggregate results are required.

## Checks not run and rationale

Comprehensive acceptance is NOT_RUN. No local Sonar scanner/setup, MRTS execution or mutation, merge or administrative change is performed.

## Final diff and review status

Use ordinary follow-up commits and the native Framework publisher. Preserve both existing Draft PR branches, historical evidence and unrelated original workspace changes. Final scoped diff, generated files, exact pins and terminal current-head checks are reconciled in the external report; this record does not independently declare readiness.
