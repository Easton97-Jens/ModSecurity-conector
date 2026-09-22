# Change Record: PR #382 native results and events

**Language:** English | [Deutsch](CR-20260921-pr382-native-results-events.de.md)

## Identity and current scope

| Field | Value |
| --- | --- |
| Change ID | `CR-20260921-pr382-native-results-events` |
| Updated (UTC) | `2026-09-22` |
| PR base | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |
| Native implementation checkpoint | `52445b18bf5944208f218871ce0f87f8f077d47d` |
| Latest code/test checkpoint | `092dfd1c8937f9712c03da011e61f1e4eab31840` |
| Branch | `fix/unified-native-results-events-20260921` |
| Pull request | [Draft #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

Parent repository only. No merge, master push, deployment, dependency update,
Framework/MRTS write, scanner suppression or issue acceptance. Current scope is
adoption-check remediation and accurate documentation, not a new host capability.
The [checklist](../../../docs/pr-382-checklist.md) separates implemented,
verified and remaining items. Overall migration status remains `partial`.

## Motivation and acceptance criteria

Direct native byte-append zero can represent configured `ProcessPartial`; phase
processing requires one. Host callback results and file APIs retain their own
contracts. A technical failure must not become a rule match or successful safe
observation. Logs must distinguish requested decisions from observed host actions.

The latest slice must recognize the actual bounded terminal NGINX helper and
HAProxy Rule-ID helper without accepting omitted calls, inverted guards or
unchecked results. Existing negative tests remain active. The user requires
zero new Sonar findings on the exact delivery SHA; a green quality gate from an
older revision does not satisfy that requirement.

## Earlier implemented changes retained

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

## 2026-09-22: adoption checker root causes and fixes

The NGINX checker expected `return ret`, but the reviewed chain now returns
`ngx_http_modsecurity_phase4_fail_control(r, mcf, ctx, cause)`. Commit `7bd3b235`
requires that exact terminal dispatch. The isolated fixture omitted its private
header and two mutation anchors still matched the old code. Concurrent commit
`f7aa2f2c` was preserved: it includes the real header, repairs the anchors,
requires exit status 1 plus the exact FAIL diagnostic, retains all 96 existing
tests and adds four regressions. No force push or overwrite was used.

The subsequent lint failure at `f7aa2f2c` was traced to two obsolete HAProxy
Rule-ID spelling probes. The real decoder initializes its buffer with `{0}` and
returns early when extraction is `<= 0`; the probes expected the former inline
assignments. Commit `092dfd1c` inspects the extracted, comment-masked decoder
and its intervention callsite. An exact whitespace-normalized contract retains
initialization, early failure return, conversion termination and integer bounds.
Eight isolated mutations test those requirements and reject a comment-only or
missing helper call. Existing compiled decoder tests remain unchanged.

Changed files in this slice:

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `ci/checks/connectors/haproxy/check-haproxy-common-adoption.py`
- `tests/test_haproxy_adoption_rule_id.py`
- `.github/workflows/lint.yml` (adds the HAProxy regression step)
- paired checklist, contract/migration guide and Change Record.

No production C source changes were needed for the latest checker slice.

## Fresh verification and exact boundaries

At `092dfd1c8937f9712c03da011e61f1e4eab31840`,
[lint job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
passed the following individual steps:

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_event_transport_observation tests.test_sonar_zero_gate
python -m unittest -v tests.test_nginx_request_native_results
python -m unittest -v tests.test_nginx_late_error_results
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
python -m unittest -v tests.test_nginx_common_adoption
python -m unittest -v tests.test_haproxy_adoption_rule_id
```

These groups contain respectively 29, 9, 9, 33, 100 and 8 tests. The NGINX/HAProxy
adoption tests mutate isolated source snapshots; compiled native tests exercise
actual selected functions with controlled collaborators. Neither is a six-host
HTTP test. Configuration-reference steps also passed.

At the same checkpoint, `test-common`, `test-apache`, `quick-framework-check`
and `test-nginx` completed successfully. The NGINX syntax/dry-run step is in
[job 106648735305](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893302/job/106648735305).
This supersedes earlier failure descriptions for those checks; workflow titles
and preflight artifacts still do not prove a full native runtime matrix.

At documentation preparation, the newest remote Sonar confirmation and overall
lint conclusion were pending. No final-head all-green claim is made. Each later
commit, including this documentation update, requires its own fresh analysis.

## Historical evidence preserved

| Revision | Evidence | Interpretation |
| --- | --- | --- |
| `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` | [Lint job 106449766690](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888258/job/106449766690) | Focused native/event tests passed; the then-current NGINX mutations failed |
| `1709e1def4706f0124d56fc687b3faf1fd8e2946` | [Job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579) | 16 Apache mutation tests and scoped guards passed, followed by an unrelated NGINX-check failure |
| `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` | [HAProxy job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189) | Eight compiled helper tests and native API compile/link compatibility passed |
| `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d` | [Lint job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958) | All 100 NGINX adoption tests and the exact-head Sonar-zero step passed; later lint failed on obsolete HAProxy probes |

Earlier detailed records remain in Git history. These successes and failures
are revision-scoped, not assertions about the latest head.

## Sonar and security impact

`ci/checks/common/check-sonar-zero.py` uses job-scoped GitHub read permissions,
checks provider and exact SHA, and requires completed successful analysis plus
explicit zero issue/hotspot/annotation counts. Missing or ambiguous results fail.
Credentials and unrestricted environment data are not logged. No issue was
accepted or rule disabled to obtain a result. The earlier `039b7f12`
[analysis](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106450287547)
reported four zero finding counts; the `f7aa2f2c` exact-head step also passed.
These do not establish the later delivery's result or measured test coverage.

This slice strengthens fixture and call-result validation. It does not remove
existing safety gates, alter engine policy, change resource limits or grant
unsupported strict/reset capabilities. A late abort cannot retract sent bytes.

## Remaining work and checks not run

Complete typed request-event handling and all remaining native/API routes;
compare producer-to-sink behavior, duplicate events and log-I/O failures in each
direct/companion/middleware/sidecar integration. Finish supported-transport
failure injection, neighbor-stream survival, runtime log comparisons, broad
connector guides and historical consumer/hash-version compatibility review.

Local commands, native builds and local `git diff --check` were not run because
the repository's required RTK execution wrapper was unavailable. Validation used
actual GitHub CI. Full six-family live HTTP/transport verification, all required
final-head checks and release review remain open. Changes were reviewed through
GitHub per-commit comparison; concurrent branch commits were preserved.

## Delivery status

NGINX adoption remediation and the HAProxy checker follow-up have the passing
scoped tests above. Request/file and late-error implementation subsets now have
explicit separate checklist entries. The current delivery is still Draft and
`partial` overall; no merge or deployment is authorized by these test results.
