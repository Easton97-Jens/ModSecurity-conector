# Change Record: PR #382 native results and events

**Language:** English | [Deutsch](CR-20260921-pr382-native-results-events.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260921-pr382-native-results-events` |
| Date (UTC) | `2026-09-22` |
| Base revision | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |
| Native implementation checkpoint | `52445b18bf5944208f218871ce0f87f8f077d47d` |
| Latest code/test checkpoint | `092dfd1c8937f9712c03da011e61f1e4eab31840` |
| Branch | `fix/unified-native-results-events-20260921` |
| Pull request | [Draft #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

Parent repository only. No merge, master push, deployment, dependency update,
Framework/MRTS write, scanner suppression or issue acceptance. Current scope is
adoption-check remediation and accurate documentation, not a new host capability.
The [checklist](../../../docs/pr-382-checklist.md) separates implemented,
verified and remaining items. Overall migration status remains `partial`.

## Motivation and problem statement

Direct native byte-append zero can represent configured `ProcessPartial`; phase
processing requires one. Host callback results and file APIs retain their own
contracts. A technical failure must not become a rule match or successful safe
observation. Logs must distinguish requested decisions from observed host actions.

The next blocking adoption checks still expected pre-refactor source spellings.
The previous documentation update also omitted required Change Record headings
and identity labels. This follow-up fixes the documents, not their validator.

## Acceptance criteria

Recognize the actual bounded terminal NGINX helper and HAProxy Rule-ID helper
without accepting omitted calls, inverted guards or unchecked results. Keep
existing negative tests active. Reconcile EN/DE checklist entries with actual
implementation subsets and revision-scoped tests. Retain the required Change
Record structure, equal identity fields and bilingual parity.

The user requires zero new Sonar findings on the exact delivery SHA. Old analysis
or a green quality gate alone is insufficient. Security-scan findings and missing
runtime evidence remain open independently of a successful Sonar analysis.

## Implementation decision and rationale

Shared native predicates and typed error classification cover the stated
Apache/HAProxy/Common paths and NGINX response processing. `event_protocol.h`
normalizes known events for both JSONL and hashing after original-input
validation. Missing observations use an empty actual action; unknown custom
events and actual counters/transport metadata are preserved. Query redaction
remains active. Apache's handwritten JSON fallback is removed.

HAProxy extracts bounded Rule-ID decoding and dependency-ordered cleanup.
The Common engine bridge maps native engine failure to invalid-engine-response
without merging timeout, protocol, connector and body-limit causes.

NGINX request changes through `fcbaca03` accept valid partial byte ingestion,
keep file-reader results strict and enforce cumulative file/body bounds. Request
phase completion occurs only after native success, and failed request re-entry
remains terminal. Changes at `52445b18` prevent negative late interventions and
mandatory Phase-4 log failures from reaching successful Safe log-only handling.
A bounded private helper permits only synchronous core-generated terminal error
responses; later retries remain blocked. These are implemented subsets, not
proof that every request-event producer or host transport is complete.

The NGINX checker expected `return ret`, but the reviewed chain now returns
`ngx_http_modsecurity_phase4_fail_control(r, mcf, ctx, cause)`. Commit `7bd3b235`
requires that exact terminal dispatch. The isolated fixture omitted its private
header and two mutation anchors still matched the old code. Concurrent commit
`f7aa2f2c` was preserved: it includes the real header, repairs the anchors,
requires exit status 1 plus the exact FAIL diagnostic, retains all 96 existing
tests and adds four regressions. No force push or overwrite was used.

The subsequent lint failure at `f7aa2f2c` was traced to two obsolete HAProxy
Rule-ID spelling probes. The real decoder initializes its buffer with `{0}` and
returns early when extraction is `<= 0`; the probes expected former inline
assignments. Commit `092dfd1c` inspects the extracted, comment-masked decoder
and its intervention callsite. The whitespace-normalized contract retains
initialization, early failure return, conversion termination and integer bounds.
Eight isolated tests reject unsafe changes, comment-only guards and missing
helper calls. Existing compiled decoder tests remain unchanged.

## Changed files

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `ci/checks/connectors/haproxy/check-haproxy-common-adoption.py`
- `tests/test_haproxy_adoption_rule_id.py`
- `.github/workflows/lint.yml` (adds the HAProxy regression step)
- Paired checklist, contract/migration guide and Change Record.

The latest checker slice changes no production C source. The documentation
follow-up restores required headings and identity labels, preserves test
boundaries and records the outstanding security-scan finding.

## Commands executed

At `092dfd1c8937f9712c03da011e61f1e4eab31840`,
[lint job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
passed these individual CI steps:

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_event_transport_observation tests.test_sonar_zero_gate
python -m unittest -v tests.test_nginx_request_native_results
python -m unittest -v tests.test_nginx_late_error_results
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
python -m unittest -v tests.test_nginx_common_adoption
python -m unittest -v tests.test_haproxy_adoption_rule_id
```

These groups contain respectively 29, 9, 9, 33, 100 and 8 tests. Configuration
reference steps also passed. At the same checkpoint, `test-common`, `test-apache`,
`quick-framework-check` and `test-nginx` completed successfully. NGINX syntax and
dry-run evidence is in [job 106648735305](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893302/job/106648735305).
These are CI executions, not locally executed commands.

### Historical evidence

| Revision | Evidence | Interpretation |
| --- | --- | --- |
| `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` | [Lint job 106449766690](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888258/job/106449766690) | Focused native/event tests passed; the then-current NGINX mutations failed |
| `1709e1def4706f0124d56fc687b3faf1fd8e2946` | [Job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579) | 16 Apache mutations and scoped guards passed, followed by a NGINX-check failure |
| `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` | [HAProxy job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189) | Eight compiled helper tests and native API compile/link compatibility passed |
| `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d` | [Lint job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958) | 100 NGINX adoption tests and exact-head Sonar-zero passed; later lint failed on obsolete HAProxy probes |

Older records remain in Git history. Results do not transfer to later revisions.
The `91f07e12` documentation validation failed because this record did not retain
the required template sections/identity labels. This follow-up restores them;
its own successful validation is not claimed until CI confirms it.

## Security impact

Existing validation, redaction, failure propagation, independent limits and
unsupported-profile rejection remain active. No safety check or compiler warning
was disabled. This slice does not invent strict/reset capability. A late abort
cannot retract bytes already sent.

### Sonar and independent security scanning

`ci/checks/common/check-sonar-zero.py` checks the provider and exact SHA and
requires completed successful analysis with explicit zero issue/hotspot/annotation
counts. Missing or ambiguous results fail. No issue was accepted or rule disabled.

[Sonar check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571)
for `91f07e124fe09056dc46dc59d65693f406b4b1a1` reports 0 new issues, 0 accepted
issues, 0 Security Hotspots and 0 annotations. Reported new-code duplication is
0.2% and coverage is 0.0%; zero findings is not a claim that these metrics are
also zero or that coverage was measured by the regression fixtures. The next
commit still needs its own analysis.

The independent [secret-scan job 106651564952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35698779824/job/106651564952)
for `91f07e12` reports one finding. Its available log does not identify a rule,
file or commit. It is unresolved, not dismissed as a false positive; no secret
value is reproduced here and no exception or history rewrite is introduced.

## Runtime evidence

NGINX/HAProxy adoption tests mutate isolated source snapshots. Compiled native
tests exercise selected actual functions with controlled host/engine/log
collaborators. These are not six live hosts. Workflow names and preflight
artifacts do not establish native HTTP/transport behavior or equal real-route logs.

## Known limitations

The overall implementation is incomplete. Typed request-error events, remaining
native/API routes and producer-to-sink behavior still need work. Documentation
validation of this follow-up and final-head CI/Sonar results require fresh
confirmation. The independent secret-scan finding remains open.

## Remaining risks

Verify duplicate terminal records, log open/write/short-write/serialization
failures and requested-versus-observed actions in every direct, companion,
middleware and sidecar route. Complete supported transport failure injection,
client-byte and neighbor-stream checks, runtime log comparisons, connector
guides and historical consumer/hash-version compatibility review.

## Checks not run and rationale

Local project commands, native builds and local `git diff --check` were not run
because the mandatory RTK execution wrapper was unavailable. Verification uses
actual GitHub CI and remote commit comparisons. Full six-family live HTTP and
transport verification, all required final-head checks and release review remain
open. Security-finding location and disposition have not been established.

## Final diff and review status

NGINX adoption remediation and the HAProxy checker follow-up have the passing
scoped tests above. Request/file and late-error subsets now have explicit
checklist entries. EN/DE records use the required template without weakening its
validator. Concurrent commits are preserved. This delivery remains Draft and
`partial` overall; no merge or deployment has been performed.
