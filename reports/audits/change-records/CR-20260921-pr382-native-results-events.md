# Change Record: PR #382 native results and events

**Language:** English | [Deutsch](CR-20260921-pr382-native-results-events.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260921-pr382-native-results-events` |
| Date (UTC) | `2026-09-21` |
| Base revision | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |
| Continuation base | `6ff390486e90a10c30c7fb6199870532ecde367a` |
| Tested implementation revision | `10b3379561de81a8018467b724b4edb8c8742ef2` |
| Branch | `fix/unified-native-results-events-20260921` |
| Pull request | [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

Delivery scope: Parent repository only. The PR is Draft; no merge performed.

## Motivation and problem statement

Direct libModSecurity body-append return values were treated differently by
native bindings. A zero append result can represent configured `ProcessPartial`,
whereas final phase evaluation requires one. Technical failures also reached
different event classes. This PR establishes shared predicates and event
normalization; this continuation repairs its test setup and the missing Common
engine-failure mapping. The full cross-connector migration is not finished.

## Acceptance criteria

Use the [paired implementation/verification checklist](../../../docs/pr-382-checklist.md).
Completed slices require both actual source changes and matching test evidence.
A complete migration additionally requires all selected native/companion routes,
consistent error/sink behavior, full regression checks, and real host/transport
validation. These broader criteria remain open.

## Implementation decision and rationale

Keep native byte ingestion, phase evaluation, host return codes, and engine
interventions distinct. Do not apply the byte-append helper to
`msc_request_body_from_file()`, which has additional failure meanings.

The Common callback-failure bridge now maps
`MSCONNECTOR_ERROR_MODSECURITY_FAILURE` to
`MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE`, matching the changed
native bindings. Existing host-error, timeout, engine-unavailable, body-limit,
protocol, and phase-sequence mappings remain intact. The change does not alter
a host action or claim a rule matched.

The C fixture extractor already returns the complete declaration for the named
Common functions. Removing duplicate return-type prefixes fixes compilation
without weakening compiler warnings or assertions. A separate compiled test
exercises the actual classifier and contract ownership with a recording sink.
Updated NGINX source checks follow the shared predicates and still require
terminal failure, a committed-response abort, and no success accounting after a
failed append. They are source checks, not substitutes for native tests.

## Security impact

Engine failure must not become allow/log-only, a false rule block, or a false
successful inspection. Error cause remains separate from observed host action.
No validation, warning flag, redaction, private-log-file control, dependency,
branch protection, or existing CI gate is disabled by this continuation.
No request/response payload or credential is added to these reports.

## Changed files

This continuation changes:

- `common/src/modsecurity_engine.c`
- `tests/test_native_result_event_protocol.py`
- `tests/test_native_error_classification.py`
- `tests/test_nginx_upstream_security_contract.py`
- `.github/workflows/lint.yml`
- `docs/pr-382-checklist.md` and `docs/pr-382-checklist.de.md`
- this Change Record and its German companion.

The earlier PR commits also introduced the shared native/event headers and
modified Apache, HAProxy, NGINX response handling, Common Runtime, JSONL, and
integrity hashing. Those earlier changes are tracked in the PR diff, not newly
claimed as completed by this continuation. No generated configuration output
or Framework/MRTS files changed.

## Commands executed

GitHub CI [run 35628608293, job 106429001084](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35628608293/job/106429001084)
reported successful terminal steps for both commands at the tested implementation
revision:

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
```

The first command compiles actual Common serializer/hash and extracted native
callback/classifier code with `-std=c17 -Wall -Wextra -Werror`. It also checks
source wiring. The second command checks Phase-4 migration and NGINX source
contracts. These results do not make the overall workflow green.

Related `test-common`, `test-apache`, `test-nginx`, and `quick-framework-check`
workflows failed at that revision. Old Apache adoption and NGINX adoption/mutation
expectations are still unresolved. They are not waived or hidden. Later
checklist/Change Record commits are documentation only; their current-head CI
must be read separately.

A GitHub compare of the continuation base through
`41c2d4e9dd6a5563ca1007ad574c17575003623c` confirmed seven expected changed files
before this Change Record pair, with only seven added production-code lines.
This is a scoped remote diff review, not a local `git diff --check` execution.

## Runtime evidence

No complete six-family native HTTP or transport matrix was executed in this
continuation. Using six connector identities in a Common fixture does not prove
six independent host integrations. Host-specific Strict support is not promoted.

## Checks not run and rationale

Local repository-native builds/tests and `git diff --check` were not executed:
the required local project wrapper was unavailable and no local checkout was
established. Validation uses the actual GitHub CI steps described above.
Final-head full CI, dedicated link validation, complete native failure injection,
and host log/transport equivalence remain open unless subsequently documented.

## Known limitations

NGINX request/file paths, late technical-intervention handling, producer-to-sink
logging, duplicate terminal records, and direct/companion profile equivalence
still need work. In particular, missing transport observation must not be
misrepresented as an executed block. Existing structural check failures still
block review readiness. The broad EN/DE contract/migration guides and examples
are not yet complete.

## Remaining risks

Accepting a valid partial-ingestion result does not prove that all supplied
bytes were inspected. A late abort cannot retract data already sent. A shared
JSON schema cannot create missing host observations or supply unsupported
reset/abort capabilities. JSONL name/action normalization can affect downstream
log consumers and requires completed migration guidance before release.

## Final diff and review status

Overall: `partial`. The focused source/test fixes are committed and the named
CI steps passed. The checklist and Change Record distinguish present code,
verified slices, failed checks, and checks not run. The PR remains Draft;
there was no merge, direct master push, deployment, dependency change, or
Framework/MRTS write. Required final-head CI is not claimed to have passed.
