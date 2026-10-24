# lighttpd Deep Security Delta

## Logical profiles

- `lighttpd-stock`: traffic-owning bounded HTTP/1.1 Stock sidecar
- `lighttpd-patched`: separate patched-native host/module route

The unmodified native Stock module compatibility translation is not a fallback for either logical profile.

## Host-specific boundaries

Assess lighttpd plugin lifecycle/configuration, URI/request hooks, response start, request reset cleanup, mapper lifetime, Stock sidecar HTTP/1.1 parser/traffic ownership, patched host/module ABI pair, borrowed request and identity response-entity ranges, monotonic offsets/EOS, `mod_proxy` pre-upstream P2 gate, host/module load compatibility, request streaming suppression, body limits, transfer framing, and runtime evidence boundaries.

Pay special attention to:

- matching patched core/module and patch/source identity;
- no upstream request byte before P2 EOS/Allow in the selected gate;
- `body_limit_action=reject` requirement for the selected streaming gate;
- rejection of incompatible host streaming/Upgrade configurations;
- entity bytes inspected before transfer framing and before socket write only where the selected contract proves it;
- no inference of H2/H3/gzip/br/file/zero-copy coverage;
- sidecar source/self-test versus actual traffic evidence;
- patched P4 source contract versus missing client-visible runtime proof.

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
- `evidence-integrity.md`
- `runtime-failure-recovery.md`

Load `filesystem-ipc.md` only if the selected sidecar/runtime path uses local IPC beyond loopback HTTP.

## lighttpd-specific validation seeds

Where current targets support them, cover stock sidecar parsing/Allow/Deny, patched host/module load, pre-upstream P2 gate, delayed/block/allow body cases, incompatible streaming configuration rejection, request reset/cleanup, borrowed-range offset/EOS behavior, response commit/P4 limitations, restart/recovery, and follow-up traffic.
