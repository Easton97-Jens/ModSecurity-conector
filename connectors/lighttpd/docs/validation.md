# lighttpd Validation

**Language:** English | [Deutsch](validation.de.md)

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
| Patched core + module build | `build-lighttpd-patched-host` | copied/patched/configured/installed 1.4.84 core and module staged with matching ABI markers and hashes |
| Patched host load | `check-lighttpd-patched-host` | staged patched binary exports hook symbols and loads staged module through real `lighttpd -tt` |
| Patched lifecycle smoke | `runtime-smoke-lighttpd-patched` | isolated patched host baseline 200 and Phase-1 rule 403; checked-in invocation keeps response streaming disabled |
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

## Patched-host boundary

The patched target is intentionally separate from the stock compatibility path
and generic stock No-CRS runner. The full-lifecycle profile selects it. It
copies and patches only lighttpd 1.4.84, builds and stages the core and module
together, validates the matching plugin ABI through `lighttpd -tt`, then runs
only the narrow Phase-1 smoke. Its checked-in generated runtime file requires
both body modes to be `none` and its manifest records
`phase4_runtime_evidence=not_executed`.

The patch invokes its response callback in `http_chunk.c` before HTTP/1
transfer framing, not at `network_write()` or on `r->write_queue`. In the
selected scope it receives the current synchronous, borrowed identity entity
range with a monotonic offset and a single EOS. The module appends the range to
Common Runtime and invokes the Phase-4 finish API only at EOS. The callback
happens before socket writes, so a later short write or `EAGAIN` cannot
duplicate inspection. This is a source/build and static-contract result, not a
host fault-injection or response-stream runtime result. gzip/br, HTTP/2, and
unexamined file/zero-copy output routes are outside the selected contract.

At a disruptive EOS decision, safe/minimal source behavior preserves the
visible response and records `log_only`; strict explicitly logs `NOT EXECUTED`
and continues. No real client has established commitment, an incomplete body,
host survival, and a subsequent independent request, so neither outcome is
canonical P4/late-intervention evidence.

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

- response-body streaming runtime, Phase 4, or late intervention;
- short-write/EAGAIN fault injection, response truncation, or body limits;
- redirect/drop/connection-abort behavior;
- multi-worker/thread stress, long-running resilience, or production hardening;
- CRS loading/effectiveness or any full CRS matrix;
- security verification, production readiness, or full-matrix readiness.

Therefore connector metadata uses `minimal_runtime_smoke` and
`partial_runtime_path`, not a broader verified or production status.

## Canonical Phase-4 validation

The stock module does not implement a response-body hook. The patched 1.4.84
module has an identity entity-body source path, but no canonical streaming host
run. Consequently `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort`, and
`late_intervention_status_metadata` remain `not_implemented` for the selected
evidence profile.

Phase-4 cases remain `NOT_EXECUTED` (or are omitted by capability selection)
until real host and client artifacts prove the timing and transport outcome.
They are not `UNSUPPORTED`: this concerns the selected evidence profile, not an
impossibility in lighttpd. The response-start hook, static source contract, and
Phase-1 smoke do not prove a client-visible Phase-4 rule, original/requested/
visible response status, a late action, or an abort. Events and reports remain
metadata-only.
