# Change Record: CR-20261008-nginx-native-cleanup-and-technical-faults

**Language:** English | [Deutsch](CR-20261008-nginx-native-cleanup-and-technical-faults.de.md)

Source-level evidence only; the integrated native runtime remains unverified.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-cleanup-and-technical-faults |
| Date (UTC) | 2026-10-08 |
| Base revision | `f0aa2fe099837d44d760012d28bd247729c73120` |

## Motivation and problem statement

Required fault records need genuine technical and cleanup observations. The native logging failure and transaction-construction failure paths previously lacked those observations.

## Acceptance criteria

Emit the actual retained Common error class; observe cleanup only after Common cleanup and the native cleanup call return. Never issue a replacement HTTP response from logging, repeat native cleanup, or read the freed native transaction.

## Implementation decision and rationale

Reuse the Common cleanup-observation constructor and existing JSONL writer. Capture the native-cleanup completion boolean, clear the native pointer, then serialize the actual Common transition. Pre-admission protocol errors have no invented transaction; native-allocation failures preserve their connector error before real cleanup.

## Changed files

`connectors/nginx/SOURCE_MAP.json`, `src/ngx_http_modsecurity_module.c`, `src/ngx_http_modsecurity_log.c` under that connector; `tests/test_nginx_native_cleanup_bridge.py`, `tests/test_nginx_native_logging.py`; this EN/DE pair. The already committed cleanup header is added to the materialization contract.

## Commands executed

RTK-wrapped Python unittest focus: native cleanup bridge (5), native logging (8), technical failure events (4), engine-call budget (5), response-header caller (5): 27 tests, exit 0. Evidence: external `root-cleanup-fault-callers-final-focus.log`. RTK-wrapped change-record and Git whitespace checks are required before commit.

## Security impact

The writer and Common validation remain strict. Cleanup observation write failure cannot undo cleanup and is explicitly logged; missing evidence must still prevent canonical certification. No payload, secret, fake rule ID, or trusted-root claim is introduced.

## Runtime evidence

None for the new integrated module. Tests compile current source with controlled host/native fixtures; they are not real NGINX requests or canonical coverage.

## Known limitations

The cleanup hook is void. Its observation cannot repair an earlier failed writer or alter the already visible response. Full materialization, fresh module build and native lifecycle remain required.

## Remaining risks

Pool-cleanup registration and allocation failures still depend on the real host lifecycle. Strict readers and runtime fixtures must validate the exact emitted identities and preserved causes.

## Checks not run and rationale

No fresh integrated native E2E, full lint or protected Exact-Head workflow: canonical integration and fresh build are not yet complete; protected trusted-base/host approval is separate.

## Final diff and review status

Reviewed the cleanup/logging changes and their explicit materializer entry. Unrelated pending config and raw-H1 work is excluded. No required record is closed by this source-only validation.
