# Change Record: CR-20261008-nginx-bounded-native-uri

**Language:** English | [Deutsch](CR-20261008-nginx-bounded-native-uri.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-bounded-native-uri |
| Date (UTC) | 2026-10-08 |
| Base revision | `68bf814e0d850f68f20bd26da59ed7a351e3633d` |

## Motivation and problem statement

Long or heavily escaped request URIs can exhaust the strict Common JSON writer. NGINX needs a bounded URI projection without concealing errors in other metadata.

## Acceptance criteria

Bound only the URI; preserve existing truncation/redaction flags and the query marker even when the query starts beyond the safe prefix. Keep oversized non-URI metadata and write errors strict.

## Implementation decision and rationale

`ngx_http_modsecurity_bounded_event_uri` projects the URI into a bounded stack buffer. The 256-byte storage permits at most 255 escaped JSON bytes; `?<redacted>` remains present for queries, including long escaped prefixes. `ngx_http_modsecurity_write_event_jsonl` and `ngx_http_modsecurity_write_phase_event_jsonl` use this projection with the real Common serializer. All other fields remain unchanged.

## Changed files

`connectors/nginx/src/ngx_http_modsecurity_event_uri.h`, `connectors/nginx/src/ngx_http_modsecurity_common.h`, `connectors/nginx/SOURCE_MAP.json`, and `tests/test_nginx_bounded_event_uri.py`; existing producer controls are in `tests/test_nginx_request_error_events.py`. The materializer explicitly includes the new header. Documentation: this `.md` / `.de.md` pair only; Framework, MRTS and Gitlinks are not changed by this documentation repair.

## Commands executed

Source-owner verification: `/root/.local/bin/rtk proxy env RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/runs/nginx-all-required-20261008T124555Z PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/nginx-all-required-20261008T124555Z/pycache /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_nginx_bounded_event_uri tests.test_nginx_request_error_events tests.test_nginx_native_intervention_chain -v` passed 32 controls in total (five URI, 15 request-error and 12 intervention controls), compiling actual producer code and Common JSON serialization with `-std=c17 -Wall -Wextra -Werror`. This documentation repair does not rerun those source tests. Parent scaffold creation and `rtk proxy python3 ci/tools/new-change-record.py check` validate document structure only.

Documentation-repair checks (no native execution): `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` exited 0; `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_change_record` passed 20 tests, exit 0. `rtk proxy make check-bilingual-docs PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` exited 2 on 22 existing missing Framework-submodule links; `rtk proxy make check-doc-links FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` exited 2 on existing missing submodule path references. None concerns this pair. `rtk git diff --check` exited 0. The fresh source-owner combined log `root-uri-limit-final-focus.log` reports 32 passing controls (five URI, 15 request-error, 12 intervention), not native runtime proof.

## Security impact

Query redaction and explicit truncation remain visible. Oversized non-URI metadata still fails; serializer and sink errors are not converted to successful events. No payload, synthetic rule or relaxed validation is introduced.

## Runtime evidence

No live native runtime evidence is claimed. Compiled controls are source/serializer unit proof, not canonical Required-case coverage or Exact-Head proof.

## Known limitations

The bounded projection is NGINX-specific and applies only to URI metadata. It is not a general Common metadata truncation policy.

## Remaining risks

A fresh source-bound module/binary build and actual Required-case execution must still establish integrated native behavior and artifact identity.

## Checks not run and rationale

Fresh complete module/binary build, integrated native requests, full Required canonical validation and remote CI/Sonar were not run in this docs-only task; these require separate source-owner/runtime coordination.

## Final diff and review status

The four-file documentation repair uses the Parent generator/schema, full base revision and equivalent EN/DE facts. Source files and unrelated work are preserved. Archive success proves structure only, not native execution.
