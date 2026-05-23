# Runtime Test Run Under `/src`

Status: current `/src` smokes PASS for executed scope

## Current Environment

```text
SOURCE_ROOT=/src
BUILD_ROOT=/src/ModSecurity-conector-build
REFRESH=1
```

Working directory:

```text
/root/git/ModSecurity-conector
```

## Commands

| Command | Result | Summary |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED. |

## Evidence Files

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/apache.rc`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/nginx.rc`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.txt`

## Apache

- Current common scope: 54 PASS, 0 FAIL, 0 BLOCKED.
- `phase1_header_block`: PASS, expected 403, actual 403.
- `response_body_pass`: PASS, expected 200, actual 200.
- `response_body_basic_block`: not executed.

Apache remains `partial` because RESPONSE_BODY blocking and full matrix
promotion are not verified.

## NGINX

- Current common scope: 54 PASS, 0 FAIL, 0 BLOCKED.
- Current all scope: 60 PASS, 0 FAIL, 0 BLOCKED.
- `phase1_header_block`: PASS, expected 403, actual 403.
- `response_body_pass`: PASS, expected 200, actual 200.
- `response_body_basic_block`: not executed.

NGINX remains `partial` because RESPONSE_BODY blocking and full matrix
promotion are not verified.

## Historical NGINX Docroot Blocker

The prior `/src` report state had 11 NGINX BLOCKED rows. That state is
preserved in `nginx-blocked-runtime-cases.md`. The current reruns resolved the
BLOCKED rows after the NGINX harness work parent was placed below
`BUILD_ROOT`.

## RESPONSE_BODY

RESPONSE_BODY blocking verified: no.

`response_body_pass` is a pass-through case. It does not prove response-body
blocking for either Apache or NGINX.
