# HAProxy Deep Security Delta

## Logical profiles

- `haproxy-htx`: direct native HTX filter
- `haproxy-spoe-spop`: SPOP request-side P1/P2 plus mandatory native-HTX response companion for P3/P4

Never use raw SPOP evidence as direct HTX response-body proof or vice versa.

## Host-specific boundaries

Assess HAProxy process/build glue, HTX message/slice ownership, incremental body chunks, EOS, pre-commit local replies, request/response append failure, actual transport termination, SPOP/SPOE frame parsing and ACK variables, request-ID/correlation validation, transaction map lifetime, loopback-only SPOP listener boundary, response companion handle/TTL/claim semantics, socket ownership, and cleanup/recovery.

Pay special attention to:

- HTX borrowed-slice inspection versus forwarded bytes;
- append/process failure fail-closed behavior;
- P4 Safe `log_only` versus unproven Strict behavior;
- response companion missing/expired/malformed/duplicate claims;
- length-delimited request IDs, embedded NUL/control/non-ASCII/overlong input;
- SPOP unauthenticated transport restricted to private loopback;
- MRC1/private companion IPC and matching ownership;
- distinction between historical SPOE examples and current selected routes.

## Required common checks

Load:

- `http-normalization.md`
- `request-desync.md`
- `modsecurity-bypass.md`
- `memory-lifecycle.md`
- `concurrency-races.md`
- `resource-exhaustion.md`
- `logging-disclosure.md`
- `config-injection.md`
- `supply-chain.md`
- `advisory-research.md`
- `finding-validation.md`
- `response-commit-phase4.md`
- `filesystem-ipc.md`
- `protocol-framing.md`
- `evidence-integrity.md`
- `runtime-failure-recovery.md`

## HAProxy-specific validation seeds

Where current targets support them, exercise native HTX Allow/Deny/P2/P3/P4, incremental request/response chunks, append failures, host replies, request-ID malformed cases, SPOE/SPOP protocol errors, response-companion TTL/replay/missing-correlation, service/host restart, and a legitimate follow-up transaction.
