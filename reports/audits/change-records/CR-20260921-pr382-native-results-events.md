# Change Record: PR #382 native results and events

**Language:** English | [Deutsch](CR-20260921-pr382-native-results-events.de.md)

## Continuation 2026-09-22: NGINX adoption/mutation repair

Change ID remains `CR-20260921-pr382-native-results-events`.
Tested revision: `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d`.
The bounded next step, checklist V06b, is `passed`; the overall PR remains
`partial` and Draft. The older sections below retain the historical
`039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` continuation and its failures;
this section supersedes their NGINX adoption/mutation status only.

The checker expected a plain `return ret`, although the reviewed code now
returns the terminal `ngx_http_modsecurity_phase4_fail_control` result. Two
mutations still searched for the old fragment, and the isolated repository
copy omitted `ngx_http_modsecurity_phase4_error.h`. The missing header also
caused unrelated macro/include failures that could disguise a mutation's
actual result.

Changed validation files:

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`: require the exact terminal dispatch and arguments rather than accepting arbitrary failure handling.
- `tests/test_nginx_common_adoption.py`: copy the actual private header, repair both stale anchors, require exit status 1 and the precise `FAIL:` line, retain all 96 existing tests, and add four fixture/dispatch regression tests.

New regressions cover byte-identical header copying, missing header, forbidden
macro mutation inside that header, and discarding the terminal-dispatch result
before returning success. No runtime code, workflow, dependency, warning flag,
scanner rule or security setting changed. Concurrent identical checker commit
`7bd3b2355c84bc6bd630de6b19ea6115b5eb64f2` was preserved as the parent of the
fixture commit; no force push was used.

[Lint run 35696836181, job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958)
passed the complete `python -m unittest -v tests.test_nginx_common_adoption`
step at the tested revision. Native/event, request-native, late-error/reentry,
Phase-4/security, configuration-reference and exact-head Sonar-zero steps also
passed. **The overall job failed later at `Run lightweight lint`.** Its cause
is not established by the mutation-step result and remains a separate open item.

[NGINX run 35696836186, job 106645456976](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836186/job/106645456976)
passed scaffold and Common-contract checks, then failed its separate native
syntax/regression guard. A request-body assertion still expects `if (ret != 1)`;
the owning source was not repaired in this step. Neither failed workflow is
reported as green.

[Sonar check 106645541548](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106645541548)
completed successfully for the exact tested SHA with **0 new issues,
0 accepted issues, 0 Security Hotspots and 0 annotations**. New-code coverage
remains 0.0%; no measured coverage improvement is claimed.

The paired checklist marks V06b complete and records these results. V06 combined
validation, V07 all-required-checks, remaining implementation, producer/sink and
real-host/profile/transport criteria remain open. Local project commands were
not run because the required RTK path was unavailable; evidence is from GitHub
CI. The documentation-only follow-up needs its own fresh CI/Sonar checks and
must not inherit this tested SHA's results. No merge, master push, deployment,
Framework/MRTS write or issue acceptance was performed.

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260921-pr382-native-results-events` |
| Date (UTC) | `2026-09-21` |
| Base revision | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |
| Current continuation base | `83c5f88179f0f33be66c68913f4b0ce694cd19f2` |
| Tested implementation revision | `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` |
| Branch | `fix/unified-native-results-events-20260921` |
| Pull request | [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

Scope: Parent repository only. The PR remains Draft; no merge or master push.
Earlier continuation evidence remains in Git history and the checklist.

## Motivation and problem statement

Native byte-append zero can mean configured `ProcessPartial`; phase processing
requires one. Prior PR commits introduced shared predicates, typed errors and
JSONL/hash normalization. They did not complete all connector routes or tests.

This continuation fixes a real metadata error: `not_observable` was treated as
proof of a host action. It repairs stale Apache adoption expectations without
removing negative tests, preserves HAProxy behavior while reducing reported
complexity, and implements the user's explicit zero-new-Sonar-finding requirement.
The entire connector migration is still incomplete.

## Acceptance criteria

The [paired checklist](../../../docs/pr-382-checklist.md) separates implemented,
verified and open items. Known unobserved events must not claim executed actions;
actual evidence fields and custom events must survive normalization. Shared
predicates must not be applied to unrelated API conventions. Apache safety
mutations and HAProxy call/cleanup order must remain tested. Sonar must report
zero new issues and hotspots on the exact head, not merely a green Quality Gate.
All remaining route, native-host, log-sink and final-head requirements stay open.

## Implementation decision and rationale

Known rule events without observation now use `MSCONN_EVENT_ENGINE_DECISION`, an
empty `actual_action` and a neutral message. Known technical errors retain their
cause and error status. NULL, empty and `not_observable` all mean no observation.
No timestamp, HTTP observation, counter, EOS or transport flag is synthesized.
The real JSONL and integrity code use the same idempotent view, after validating
the original input. Unknown application events keep their existing semantics.

Apache checkers now inspect shared return predicates, typed event status and a
single bounded canonical writer. The removed handwritten JSON fallback is not
required by obsolete assertions. New mutations reject inverted append/phase
guards, removed serialization-error return and technical errors logged as rule
blocks. A later linear status-assignment check removes a reported regex risk.

HAProxy extracts bounded Rule-ID decoding and dependency-ordered resource cleanup.
A remote commit diff confirmed 36 added and 22 removed binding lines, with the
existing evaluation sequence retained. New compiled tests exercise the actual
selected source with controlled API seams and the real Common Rule-ID decoder.

The Sonar guard reads only GitHub Checks using a job-scoped read credential. It
requires the exact SHA and provider, a successful completed analysis and explicit
zero issue/hotspot/annotation counts. Missing or ambiguous evidence fails rather
than passing. Responses, polling and diagnostic output are bounded; redirects
are rejected. No scanner exclusions, accepted findings or suppressed rules are
used. Repository identity rejects traversal and stays ASCII-only.

## Changed files

This continuation changes the following code and validation surfaces:

- `common/include/msconnector/event_protocol.h`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `ci/checks/common/check-sonar-zero.py`
- `ci/checks/connectors/apache/apache_common_adoption_base.py`
- `ci/checks/connectors/apache/check-apache-common-adoption.py`
- `tests/test_apache_common_adoption.py`
- `tests/test_event_transport_observation.py`
- `tests/test_sonar_zero_gate.py`
- `tests/test_haproxy_binding_refactor.py`
- `.github/workflows/lint.yml` and `.github/workflows/test-haproxy.yml`
- `docs/pr-382-checklist.md` and `docs/pr-382-checklist.de.md`
- `docs/pr-382-event-contract.md` and `docs/pr-382-event-contract.de.md`
- this Change Record and its German companion.

Earlier native-result, Common error-classifier, Apache/NGINX and serializer/hash
changes remain in the PR. No dependencies, generated configuration, Framework,
MRTS, branch protection or scanner configuration were changed.

## Commands executed

GitHub CI [run 35634888258, job 106449766690](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888258/job/106449766690)
completed these individual steps successfully at the tested implementation SHA:

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_event_transport_observation tests.test_sonar_zero_gate
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
python ci/checks/common/check-sonar-zero.py
```

The overall lint job failed at the NGINX adoption/mutation step. Passed individual
steps are not represented as a green overall workflow. The new fixtures compile
with `-std=c17 -Wall -Wextra -Werror`; they exercise actual selected Common/native
code with controlled surrounding state, not six real hosts.

GitHub CI [run 35634888103, job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189)
passed the following at the same implementation SHA:

```sh
python3 -m unittest -v tests.test_haproxy_binding_refactor
python3 tests/test_haproxy_libmodsecurity_compat.py
```

All eight evaluation/cleanup/Rule-ID tests and the existing compile/link
compatibility step passed. Native API seams in these tests are controlled;
this is not a live HAProxy HTTP result.

Apache scoped adoption checks and all 16 mutation tests passed at
`1709e1def4706f0124d56fc687b3faf1fd8e2946` in
[run 35633647191, job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579).
That job then failed at the NGINX checker. The later linear Apache source-check
refactor needs its own complete validation; no earlier pass is promoted to it.

[Sonar check 106450287547](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106450287547)
completed on `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` with **0 new issues,
0 accepted issues, 0 Security Hotspots and 0 annotations**. It reports 0.0%
new-code duplication and 0.0% new-code coverage. The latter is not represented
as measured test coverage. Every later head requires a fresh analysis.

## Security impact

An engine failure must not become allow/log-only, a false rule block or false
successful inspection. Missing host observations must not be presented as
executed enforcement. Original input validation and query redaction are kept.
No raw body, credential or unrestricted environment is added to event evidence.

The new Sonar check has only job-scoped `checks: read` and `contents: read`.
Credentials are not printed, forwarded on redirects or written into evidence.
The guard is stricter than the existing green Quality Gate and is not a
replacement for code, mutation, security or host integration tests.

## Runtime evidence

No complete six-family live HTTP/transport matrix was performed. Common fixture
family labels are not independent host runs. HAProxy source-function tests and
compile/link compatibility establish their stated layers only. Hosted CI builds
and preflight artifacts alone do not establish client-visible behavior. No
unsupported strict profile or reset/abort capability is promoted.

## Known limitations

NGINX request/file paths and late technical-intervention handling remain open.
The NGINX chain checker and stale mutation fragments still fail. Complete
producer/sink comparison, duplicate terminal records, I/O failures, other event
classes and direct/companion route equivalence still need work. The broad
connector guides and final compatibility/versioning review are incomplete.

## Remaining risks

A valid partial-ingestion return does not prove all supplied bytes were inspected.
A late abort cannot retract data already sent. Normalization cannot create host
observations; producers still need consistent flags and statuses. The new event
identifier, empty actual action and normalized integrity view affect consumers;
the [contract guide](../../../docs/pr-382-event-contract.md) documents migration
requirements without claiming historical format compatibility is settled.

## Checks not run and rationale

Local native builds, local project tests and local `git diff --check` were not
run because the required project execution wrapper is unavailable. Validation
uses the actual GitHub CI results above. Full six-family host/transport failure
injection, complete log-sink equivalence and all-green final-head CI remain open.
The final documentation commit needs its own bilingual/link/CI/Sonar results.

## Final diff and review status

Overall: `partial`. The new metadata fix, Apache validation updates and HAProxy
refactor are committed with the stated tests; exact implementation-head Sonar
zero is verified. The NGINX validation gap and remaining implementation/runtime
criteria prevent completion. Checklists and contract guidance are bilingual.
The PR remains Draft. No merge, direct master push, deployment, dependency,
Framework/MRTS write, issue acceptance or scanner suppression was performed.
