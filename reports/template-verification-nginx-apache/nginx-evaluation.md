# NGINX Evaluation

Status: reviewed

NGINX rating: partial with current `/src` smoke PASS scope

Reason: `connectors/nginx` contains an adapter-owned source tree, metadata,
origin documentation, harness files, and connector docs. The current `/src`
runtime evidence is improved: NGINX common smoke has 54 PASS, 0 FAIL,
0 BLOCKED, and NGINX all-scope smoke has 60 PASS, 0 FAIL, 0 BLOCKED. The
connector still remains `partial` because RESPONSE_BODY blocking and the full
minimum runtime matrix are not verified.

## Evidence Summary

| Area | Status | Evidence |
| --- | --- | --- |
| README/docs | OK | `connectors/nginx/README.md`, `connectors/nginx/docs/` |
| Local test folder | OK | `connectors/nginx/tests` is absent. |
| Adapter-owned source | OK | `connectors/nginx/src/`, `connectors/nginx/metadata.c`, `connectors/nginx/ORIGIN.md` |
| NGINX build include contract | OK | `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` is supported by `connectors/nginx/config`; current build includes the common header path. |
| Docroot runtime work parent | OK for `/src` | Parent `Makefile` exports `NGINX_HARNESS_PARENT=$(BUILD_ROOT)`; current runtime path is below `/src/ModSecurity-conector-build`. |
| Current `make smoke-nginx` | PASS | `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx`: 60 PASS, 0 FAIL, 0 BLOCKED. |
| Current `make smoke-common` | PASS | Apache 54 PASS; NGINX 54 PASS; both 0 FAIL and 0 BLOCKED. |
| Historical 11 BLOCKED rows | Resolved | Classified as environment/docroot permission blocker in `nginx-blocked-runtime-cases.md`. |
| RESPONSE_BODY blocking | Not verified | `response_body_pass` is pass-through only; no blocking response-body testcase with HTTP 403 was executed for both connectors. |
| More than `partial` | Not allowed | Full minimum matrix evidence is incomplete. |

## Current Runtime Counts

| Command | Scope | PASS | FAIL | BLOCKED | XFAIL |
| --- | --- | ---: | ---: | ---: | ---: |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | all | 60 | 0 | 0 | 0 |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | common | 54 | 0 | 0 | 0 |

Evidence files:

- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/nginx.rc`
- `/src/ModSecurity-conector-build/results/connector-summary.json`

## Historical Blocker

The earlier NGINX common run had 43 PASS and 11 BLOCKED. Those rows are not
treated as PASS for the historical run. They were rerun after the docroot work
parent was moved below `BUILD_ROOT`; the current run now records PASS for the
same cases. See `nginx-docroot-permission-analysis.md` and
`nginx-blocked-runtime-cases.md`.

## Checklist

- [x] README present.
- [x] Docs present.
- [x] Local test folder removed.
- [x] Harness/adapter structure present.
- [x] NGINX build can find `common/include/msconnector/rule_load_stats.h`.
- [x] Current `/src` NGINX all-scope smoke passed.
- [x] Current `/src` NGINX common smoke passed.
- [x] Historical 11 BLOCKED rows documented and rerun.
- [ ] RESPONSE_BODY blocking verified.
- [ ] Full minimum runtime matrix verified.
- [ ] Connector can be promoted beyond `partial`.

## Decision

NGINX remains `partial`. The current `/src` smokes are PASS for their executed
scope, but runtime completeness and RESPONSE_BODY blocking remain unverified.
