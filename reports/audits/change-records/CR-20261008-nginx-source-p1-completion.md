# Change Record: CR-20261008-nginx-source-p1-completion

**Language:** English | [Deutsch](CR-20261008-nginx-source-p1-completion.de.md)

Actual source P1 completion, not host delivery.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-source-p1-completion |
| Date (UTC) | 2026-10-08 |
| Base revision | `9cfae553e7e69b1db8211f1a4ce0afc986b88604` |

## Motivation and problem statement

Native allow-only P1 processing previously had no source completion event unless a rule callback happened. A driver or cleanup event cannot prove that actual request-header processing completed.

## Acceptance criteria

Emit only after native return1, completed Common P1 and the existing no-intervention continuation. Require no event for denial, invalid native return, clock/budget failures, terminal/cleaned state or duplicate P1 execution. Never claim host200, actual delivered allow, request EOS or full-request success.

## Implementation decision and rationale

Add a narrow constructor guarded by actual Common waiting state, no active phase, exactly completed P1 mask, last_completed P1, no error and no cleanup. Preserve the actual native return before intervention overwrites ret. Emit through the established bounded request-event writer after all intervention branches; missing/failed sink remains warning-only.

## Changed files

connectors/nginx/src/ngx_http_modsecurity_request_completion.h; connectors/nginx/src/ngx_http_modsecurity_access.c; connectors/nginx/SOURCE_MAP.json; tests/test_nginx_p1_completion_source.py; this EN/DE pair.

## Commands executed

RTK-wrapped Parent .venv unittest tests.test_nginx_p1_completion_source compiles actual full P1 caller/result boundary plus real Common transitions, budgets and JSONL with C17 -Wall -Wextra -Werror. Original source RED: 3 expected missing-event failures across 4 methods; changed source GREEN: 4 methods. Logs stream-c-p1-completion-red-final.log and stream-c-p1-completion-green.log retain the results. Final regression of P1, connection/URI, budget, P3/P4, materialization and context accounting passes 31 tests (stream-c-p1-completion-cross-final.log), including a real Common failure injected during the controlled native callback. Syntax/SOURCE_MAP identity, ci/tools/new-change-record.py check, make check-bilingual-docs and make check-doc-links (explicit current Framework checkout) pass. No unrelated source edits.

## Security impact

Custom request_headers_complete/MSCONN_PHASE1_COMPLETE is preserved by the actual Common protocol view. It has rule empty, ok/allow/requestedallow, actual_action empty, http0/visible0/not_observable, genuine request metadata and bounded reason native_return=1;common_completed=1. No rule, host delivery or transport success is manufactured.

## Runtime evidence

Controlled C17 source/serializer tests only. Native processing, host metadata/header plumbing and monotonic clock are controlled; Common transitions, budget bridge, event constructor and serializer are actual source. No native NGINX runtime was run.

## Known limitations

Completion describes P1 only. Existing request logging remains warning-only; a missing source event must not be inferred by an evidence consumer. Existing callers' budget/fault/enforcement semantics remain unchanged.

## Remaining risks

The coordinator must rebuild and execute fresh native runs before runtime coverage or canonical acceptance. Existing raw denial vocabulary is Common engine_decision/MSCONN_EVENT_ENGINE_DECISION when transport_result is not_observable; RULE_MATCHED serializes as rule_match. Source callback names must not be confused with raw JSONL.

## Checks not run and rationale

No native build/runtime, E2E, remote CI, Sonar, Framework edits, Gitlink changes or push: outside this bounded producer task.

## Final diff and review status

Focused source diff reviewed. No Common semantic change, new context field or synthetic evidence. SOURCE_MAP includes the new productive header. Separate six-file commit with native-generated EN/DE headings.
