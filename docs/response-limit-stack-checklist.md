# Response-limit stack checklist

**Language:** English | [Deutsch](response-limit-stack-checklist.de.md)

## Stack identity

Base PR: [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382).
Base branch: `fix/unified-native-results-events-20260921`.
Exact base: `498653c2a193d34b7b25b2903b1e4db1c45e7f73`.
New branch: `fix/engine-owned-response-limits-stack-20261011`.
Draft PR: [#407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407),
targeting the base branch; no merge is authorized.

## Implementation

- [x] Inventory Common and all ten actual logical adapter profiles.
- [x] Remove response options/defaults, metadata ceilings, SIZE_MAX policy helper,
  cumulative byte rejection and connector truncation from response ingestion.
- [x] Preserve request policy, engine access/MIME configuration and host modes.
- [x] Verify native response BODY_LIMIT recognition and retained interventions.
- [x] Preserve technical frame/chunk/scratch/buffer/descriptor/header/event guards.
- [x] Update generated configuration references, examples and EN/DE ownership docs.

## Executable tests

- [x] Configuration inventories and removed options; explicit checked-in fixtures.
- [x] Real libModSecurity below/exact/above, Reject/ProcessPartial, multichunk,
  different explicit limits, supported modes and payloads above old 1 MiB.
- [x] File-backed HAProxy binding component tests; hosted adapter proof remains open.
- [x] Selected integrated Common/connector/safety/regression tests and documentation checks; base failures are listed separately below.
- [ ] Completed Sonar analysis for the new PR head: zero new issues/hotspots and
  zero new-code duplication; no scanner exceptions or relaxed checks.

The first completed analysis of `77e8085b663b46c9eb22b11864aadd0161dc5060`
reported ten issues, zero hotspots and zero duplication. Follow-up source changes
address resource cleanup, declarations, helper complexity and fixture parameters;
the reviewed Apache fingerprint and Traefik API expectation were updated too.
The completed analysis of `777d67efcd040b98d7d0c288379ab55012ef51b1`
reported zero new issues and hotspots, but two new duplicated lines/blocks
(0.2%). The shared Authz fixture setup now replaces that duplication; the
compiler-guide generator also removes its obsolete response option. The new
head requires its own completed analysis; live delivery status is in #407.

Common real-library validation passed 81 scenarios; HAProxy binding validation
passed 16 cases. Envoy passed eight real CGo/libModSecurity packages and its
binary build. MRC1/observer component checks and 31 lighttpd gate/supervisor/
namespace tests passed. The stock-sidecar suite passed 33/34; its RST event
failure and the legacy Common lossy-event assertion were reproduced on the base.
Their assertions remain intact. The fresh-tree integrated 57-test run passed in 22.053 seconds, including 81
native Common scenarios and a matching phase-4 rule. The fresh native-owned
136-test/174-subtest sweep passed in 44.77 seconds. Common contracts, safety
checks, 21 generated references, bilingual documentation, paths and links passed
in the final run. Two further native binding expectations
failed unchanged on the base. A broader interrupted sweep is not a pass. Apache C17 syntax passed; NGINX/HAProxy native checks lack host artifacts.

## Missing real-host evidence

Fresh hosted lifecycle evidence remains separate for each profile below.
Builds, source wiring, stubs and Common engine tests do not check these boxes.

- [ ] Apache native hosted lifecycle.
- [ ] NGINX native hosted lifecycle and memory/file buffer delivery.
- [ ] HAProxy native HTX hosted lifecycle.
- [ ] HAProxy SPOE/SPOP with native-HTX response companion hosted lifecycle.
- [ ] Envoy ext_proc hosted lifecycle.
- [ ] Envoy ext_authz with response observer hosted lifecycle.
- [ ] Traefik native UDS middleware hosted lifecycle.
- [ ] Traefik forwardAuth with response observer hosted lifecycle.
- [ ] lighttpd Stock sidecar hosted lifecycle.
- [ ] lighttpd patched native hosted lifecycle.

## Safety and evidence limits

Fixed working-buffer capacity is not an engine limit. The active lighttpd sidecar
streams fixed scratch chunks. Its buffered legacy exchange is compiled out under
`#if 0`; its retained 1 MiB capacity is not a current runtime response ceiling.
NGINX file scratch, MRC1 frames/body chunks, Envoy gRPC messages, Traefik UDS,
HAProxy SPOP/HTX frames, header/event metadata, overflow guards and transport
timeouts remain active. No historical runtime report is a result for this head.

See [ownership contract](phase4-mode-budget.md) and
[Change Record](../reports/audits/change-records/CR-20261011-response-limit-policy-removal.md).
