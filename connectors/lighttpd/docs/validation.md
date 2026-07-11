# lighttpd Validation

Status: `minimal_runtime_smoke` for the native Phase-1 header path

## Evidence layers

| Layer | Target | Verified behavior |
| --- | --- | --- |
| Legacy bridge build | `build-lighttpd-bridge` | compile only |
| Legacy bridge self-test | `self-test-lighttpd-bridge` | local probe only; not host evidence |
| Native module build | `build-lighttpd-connector` | C17 PIC compile and link with `-Werror` |
| Config load | `check-lighttpd-config` | real lighttpd 1.4.84 loads module, validates Common config and rules |
| Start smoke | `start-smoke-lighttpd` | real process starts, remains alive, and stops cleanly; zero requests |
| Runtime smoke | `runtime-smoke-lighttpd` | real host path returns baseline 200 and Phase-1 rule 403 |
| Decision event | runtime smoke | JSONL contains `connector=lighttpd` and `rule_id=1000001`; no body payload field |

## Native config-load check

The harness generates a temporary Common runtime configuration and lighttpd
configuration below `BUILD_ROOT`. It invokes:

```text
LIGHTTPD_BIN -m <connector-module-dir> -tt -f <generated-config>
```

This causes the real loader to resolve `mod_msconnector.so`, execute plugin
initialization/default setup, validate the Common configuration, initialize
libmodsecurity, and load the targeted rule file.

## Request-free start smoke

`start-smoke-lighttpd` first repeats config-load validation, starts lighttpd in
foreground mode, checks the PID after startup, sends no request, terminates the
process, and waits for clean shutdown. Its PASS line records `requests=0`.

## Minimal runtime smoke

`runtime-smoke-lighttpd` is intentionally separate. With compatibility module
autoload disabled, it uses lighttpd's core `OPTIONS *` path, so only the native
connector module is needed in the temporary module directory.

It verifies:

1. `OPTIONS *` without the test header returns HTTP 200.
2. The same real lighttpd request with `X-Modsec-Smoke: block` returns HTTP 403.
3. Common/libmodsecurity rule `1000001` is identified in the JSONL event.
4. The event carries connector metadata and contains no request/response body
   payload field.
5. The host process remains stable and is stopped cleanly.

The block is produced from `common/rules/modsecurity_targeted_smoke.conf` and
mapped by the module with `http_status_set_err()`.

## Resource and ownership checks

Both mappers enforce header count and total-header byte limits before runtime
entry. Common resource guards enforce the remaining configured header and body
limits. Nonzero body data is never advertised. Header arrays and the runtime
transaction are destroyed at request reset, including request-mapping and
transaction-begin failure paths.

Repository C-standard checks compile connector C code with C17, optional C23,
and optional future-C modes. Only C17 is required by the native build.

## Explicitly unverified

The current evidence does not verify:

- request-body capture, Phase 2, or body truncation;
- response-body capture, Phase 4, or late intervention;
- redirect/drop/connection-abort behavior;
- multi-worker/thread stress, long-running resilience, or production hardening;
- CRS loading/effectiveness or any full CRS matrix;
- security verification, production readiness, or full-matrix readiness.

Therefore connector metadata uses `minimal_runtime_smoke` and
`partial_runtime_path`, not a broader verified or production status.

## Canonical Phase-4 validation

The native module does not implement a response-body hook.  Consequently,
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort`, and
`late_intervention_status_metadata` are `not_implemented`.

Phase-4 cases must remain `NOT_EXECUTED` (or be omitted by capability
selection) until a native response-body path and honest intervention timing are
implemented.  They are not `UNSUPPORTED`: the current statement concerns this
module, not an impossibility in lighttpd.  The existing response-start header
hook and Phase-1 403 smoke neither prove a Phase-4 rule nor original/requested/
visible response status, a late action, or an abort.  Events and reports remain
metadata-only.
