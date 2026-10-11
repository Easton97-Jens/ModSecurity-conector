# Change Record: CR-20261011-response-limit-policy-removal

**Language:** English | [Deutsch](CR-20261011-response-limit-policy-removal.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261011-response-limit-policy-removal |
| Date (UTC) | 2026-10-11 |
| Base revision | `498653c2a193d34b7b25b2903b1e4db1c45e7f73` |

## Motivation and problem statement

Connector response ceilings could reject or truncate data before libModSecurity
applied its configured response policy. The stacked change removes that second
policy from Common and all ten logical connector profiles. Response inspection
limit and action belong exclusively to `SecResponseBodyLimit` and
`SecResponseBodyLimitAction`.

## Acceptance criteria

Remove connector response-limit configuration, defaults, cumulative byte gates
and truncation; preserve request policy, access/MIME selection and `off`/`safe`/
`strict` host behavior. Preserve genuine technical guards and distinguish their
failures from native response `BODY_LIMIT`. Retain native operation results,
interventions and phase completion. Every response-inspection fixture supplies
both native directives explicitly. Verify boundary cases, modes, multichunk and
file input, varied limits, removed-option rejection and bodies above the old
1 MiB ceiling. Maintain EN/DE references and report hosted evidence separately.
A completed current-head Sonar analysis with zero new issues, hotspots and
new-code duplication remains required for verified delivery.

## Implementation decision and rationale

Removed options include Common `response_body_limit`, HAProxy
`response-body-limit` and Envoy `max_response_body_bytes`, together with their
response-only fields, defaults and fallback helpers. Request limits and request
`body_limit_action` remain. Adapters offer complete valid chunks to the engine;
libModSecurity selects Reject or ProcessPartial. Common retains a disruptive
response intervention captured during append through later chunks and phase
completion. Native response limit rejection keeps phase 4 and HTTP 403;
technical pointer, overflow, transport or storage failures keep technical
classification. The inspected-byte counter describes bytes offered to the
engine, not the engine's internal ProcessPartial prefix.

## Changed files

- Common configuration, body/resource/mapper/transaction contracts, native runtime,
  decision/intervention classification and MRC1 response transport.
- Apache, NGINX, HAProxy, Envoy, Traefik and lighttpd response routes, connector
  configuration, harnesses, tests and EN/DE READMEs.
- `ci/checks/documentation/connector_config_reference.py`, its generated
  `examples/*/configuration-reference.md` and `.de.md` companions,
  `examples/common/` references and
  `reports/connector-configuration-inventory.json`.
- Response fixtures under `common/rules/`, connector harnesses and
  `ci/runtime/lifecycle/cases/apache-phase4-response/`; the NGINX workflow fixture
  arguments; Common, adapter, transport, event and removed-option regressions.
- `docs/phase4-mode-budget.md` / `.de.md`,
  `docs/response-limit-stack-checklist.md` / `.de.md`, repository concept,
  runtime-failure policy, Traefik compiler guide and example README pairs.
- This EN/DE Change Record pair. No Framework/MRTS source or dependency manifests
  are changed.

## Commands executed

The following coordinator checks passed on the implementation worktree before
final stack transfer. Their results do not establish checks for a future PR SHA.

```sh
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_engine_response_limits
rtk proxy make check-common-helpers check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity check-adapter-contracts check-directive-parity PYTHON=/root/git/ModSecurity-conector/.venv/bin/python BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/engine-response-limits-20261011/root-checks/build
rtk proxy make check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
rtk proxy git diff --check
```

The engine suite passed 81 genuine native scenarios. Common helper, SDK,
security, memory, flow, adapter and directive checks passed. Documentation and
link checks passed; generated-reference generation/check passed. Two integrated
fixture compile errors were repaired. The focused 13-test rerun and subsequent
57-test integrated run passed. The final fresh-tree integrated 57-test run passed in 22.053 seconds, including
all 81 native Common scenarios and the matching phase-4-rule regression.

Component validation also passed: HAProxy binding/SPOA builds and genuine
16-case response suite and final six-method real-library suite; Envoy `build_ext_proc.sh` with
`ENVOY_EXT_PROC_COMMON_TEST=1` across eight CGo/libModSecurity packages and the
binary; Envoy authz/observer, Traefik forwardAuth and lighttpd stock-sidecar
builds; strict C17 MRC1 and observer companion tests; 31 lighttpd gate/supervisor/
namespace tests. Apache C17 syntax passed after intervention-retention changes. The native-owned
pytest sweep passed 136 tests and 174 subtests, including 19 required-fixture
helper tests. External run artifacts are retained
under `/var/tmp/codex/ModSecurity-conector/runs/engine-response-limits-20261011/`.

Follow-up validation after the first CI/Sonar feedback passed: 30 Common native,
event and error tests including all 81 genuine engine scenarios; 58 HAProxy tests
and 53 subtests, binding/self-test/SPOP build and adoption/HTX checks; 27 Apache
tests and the NGINX adoption check; 33 Traefik/private-socket tests (two hosted
tests skipped), seven engine-service tests and Traefik integration contracts.
Independent review found no concrete issue in the seven-file repair diff.
The final NGINX fixture metadata correction passed 32 existing tests and
138 subtests; required limit/action helper checks and diff validation passed.

## Security impact

Untrusted response data reaches the engine without a connector inspection
ceiling. Bounded operations remain: pointer and integer checks, file reads and
descriptors, fixed scratch storage, MRC1 32 KiB body chunks and 64 KiB frames,
protocol/message limits, header/event metadata and transport timeouts. Request
policy is preserved. No authentication, isolation, warnings, tests, scanner
exceptions or Quality Gate requirements are weakened. An omitted engine policy
uses native semantics; deployment owners must configure their intended native
limit and action.

## Runtime evidence

The real-library Common suite uses libModSecurity 3.0.14 with limits 128 and
1024, both Reject and ProcessPartial, `off`/`safe`/`strict`, below/equal/above
payloads and chunk sizes 17/65536. Additional marker cases distinguish the
native partial prefix from later data. Explicit 1.5 MiB and 3 MiB limits with
2 MiB bodies expose the former hidden 1 MiB ceiling. HAProxy's genuine component
suite includes memory/file input and native intervention retention. The NGINX
body-buffer fixture distinguishes its payload length from the explicitly supplied
engine limit/action in generated evidence; payload sizing does not configure
inspection policy. Envoy's
native regression supplies `2097152` and Reject explicitly and inspects a tail
past 1 MiB; its borrowed-response test accepts 300 callbacks. MRC1 component
checks send multiple valid chunks beyond the former cumulative cap and reject
oversized frames technically. These are component/engine results; they do not
prove hosted lifecycle behavior for any of the ten profiles.

## Known limitations

The stock-sidecar suite passed 33 of 34 tests; its RST rule-block delivery test
produced no events. The legacy `transaction_phase_runtime_companion_test.c`
lossy-event assertion also fails with the real library. Both failures were
reproduced on the unchanged initial base; their assertions remain intact. An
additional native transaction-binding selection passed 24 tests and failed two
old request-ID/stop expectations, also reproduced on the unchanged base. A broad
owned sweep was interrupted without a terminal summary and is not a pass. The
compiled-out lighttpd `#if 0` legacy buffered exchange is not an active response
capacity; the active sidecar streams fixed scratch chunks. NGINX and HAProxy
native C17/host verification still lack required host sources/headers or runtime
artifacts. A complete hosted response-limit matrix remains missing for all ten
profiles; individual hosted NGINX event/buffer fixtures do not cover that matrix.

## Remaining risks

Component success does not establish native host buffer ownership, commit timing,
late intervention delivery or transport lifecycle in deployed hosts. The four
reproduced base failures remain open. The fresh integrated run and independent static safety review passed.
Current-head CI/Sonar and delivery verification must be reconciled before
claiming complete verification.

## Checks not run and rationale

No complete ten-profile hosted response-limit matrix was run: the required pinned host environments
and run evidence are unavailable. The first completed Sonar analysis of
`77e8085b663b46c9eb22b11864aadd0161dc5060` failed with ten issues, zero hotspots
and zero duplication. Resource cleanup, declarations, helper complexity and
fixture parameters were repaired. The completed analysis of
`777d67efcd040b98d7d0c288379ab55012ef51b1` reported zero new issues and hotspots,
but two new duplicated lines/blocks (0.2%). Shared Authz fixture construction
replaces the duplicate setup without changing assertions or explicit policy
arguments. The compiler-guide generator now matches its generated files;
22 guide tests and bilingual/path/link checks passed. The completed source-head
analysis of `6875be20f0c9c30b4ca8ad9ec62f65ac35d863cd` passed: zero new issues,
hotspots, duplicated lines, blocks and density; Quality Gate OK. The full local
`make quick-check` passed, including ten unittest summaries totaling 302 tests.
Final PR-head CI/Sonar readback, including documentation follow-ups, is recorded
in #407. Base-PR analysis is not evidence for this change. NGINX/
HAProxy native checks blocked by missing host artifacts are not passes. The fresh integrated rerun passed. The fresh native pytest run passed 136 tests
and 174 subtests in 44.77 seconds. Final Common helper/SDK/security/memory/flow/
adapter/directive checks, 21 generated references, bilingual documentation, paths
and links passed. The five newer base files and Framework gitlink stayed unchanged.

## Final diff and review status

Implementation worktree diff whitespace check passed. Static source safety review found no current issue, and its diff whitespace
check passed; content review and fresh-base reconciliation are complete.
The task branch was committed and pushed, and stacked
[Draft PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
is open against the specified base branch. First-head CI exposed the reviewed
Apache checker fingerprint and Traefik header-only API expectations; both test
contracts were updated without removing their assertions. Follow-up delivery
requires fresh exact-head CI/Sonar readback. No merge was performed.
The [stack checklist](../../../docs/response-limit-stack-checklist.md) separates
implementation, executable tests and missing real-host evidence.
