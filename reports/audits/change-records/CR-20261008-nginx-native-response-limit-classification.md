# Change Record: CR-20261008-nginx-native-response-limit-classification

**Language:** English | [Deutsch](CR-20261008-nginx-native-response-limit-classification.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-response-limit-classification |
| Date (UTC) | 2026-10-08 |
| Base revision | `8b575c094140f3a92bb030a83f27b4c44b00127e` |

## Motivation and problem statement

A native response-body Reject has no rule correlation. It must not enter SAFE's rule-only log-only path or claim Engine EOS.

## Acceptance criteria

Accept only the exact native response-limit signature; seal BODY_LIMIT without a rule, suppress downstream forwarding and reject unexpected append-time rule decisions before actual Engine completion.

## Implementation decision and rationale

Use the existing closed predicate `ngx_http_modsecurity_is_response_body_limit_rejection` before rule-only dispatch in `ngx_http_modsecurity_process_intervention`. The actual context distinguishes native request/response-body limit rejection. Arbitrary no-rule 403 responses are not body-limit proof and cannot borrow SAFE rule semantics.

## Changed files

`connectors/nginx/SOURCE_MAP.json`, `connectors/nginx/src/ngx_http_modsecurity_common.h`, `connectors/nginx/src/ngx_http_modsecurity_module.c` and `tests/test_nginx_native_intervention_chain.py`. Materialization includes the existing response-limit/P4 observation headers. Documentation: this `.md` / `.de.md` pair only; Framework, MRTS, generic validators and Gitlinks are unchanged by this documentation repair.

## Commands executed

Source-owner verification: `/root/.local/bin/rtk proxy env RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/runs/nginx-all-required-20261008T124555Z PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/nginx-all-required-20261008T124555Z/pycache /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_nginx_bounded_event_uri tests.test_nginx_request_error_events tests.test_nginx_native_intervention_chain -v` freshly passed 32 controls in total, including 12 actual-source collector controls with `-std=c17 -Wall -Wextra -Werror`. Valid SAFE/STRICT/off controls and wrong-signature, early-rule, invalid-return and missing-correlation negatives remain covered. This documentation repair does not rerun those source tests. Parent scaffold creation and `rtk proxy python3 ci/tools/new-change-record.py check` validate document structure only.

Documentation-repair checks (no native execution): `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` exited 0; `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_change_record` passed 20 tests, exit 0. `rtk proxy make check-bilingual-docs PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` exited 2 on 22 existing missing Framework-submodule links; `rtk proxy make check-doc-links FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` exited 2 on existing missing submodule path references. None concerns this pair. `rtk git diff --check` exited 0. The fresh source-owner combined log `root-uri-limit-final-focus.log` reports 32 passing controls (five URI, 15 request-error, 12 intervention), not native runtime proof.

## Security impact

No synthetic rule or EOS is introduced; technical Reject suppresses downstream body forwarding. Framework containment/freshness, Required selection and strict event validators remain unchanged.

## Runtime evidence

This is source-state/collector unit proof, not a fresh module artifact or actual native request result. No canonical PASS or Exact-Head runtime proof is claimed.

## Known limitations

The classification depends on the closed Engine-specific signature and actual response-body completion. Concurrent budget/cleanup changes are not part of this record's source slice.

## Remaining risks

Integrated native validation with genuinely rebuilt artifacts must confirm the Engine signature, technical rejection and completion behavior.

## Checks not run and rationale

Fresh complete module/binary build, integrated native requests, full Required canonical validation and remote CI/Sonar were not run in this docs-only task; source-owner/runtime coordination remains necessary.

## Final diff and review status

The focused documentation repair follows the Parent generator/schema and uses the full base revision. Equivalent EN/DE facts retain the original source/unit evidence boundary. Unrelated orchestration and source changes are preserved; archive success proves structure only.
