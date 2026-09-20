# NGINX Deep Security Delta

## Current logical profile

- `nginx`
- selected host route: native NGINX HTTP module
- product source: `connectors/nginx/`

## Host-specific boundaries

Assess directive registration and config merge; rewrite/preaccess/access/content phases; header/body/log filters; request cleanup; worker lifecycle; main requests, subrequests, internal redirects, named locations and `error_page`; asynchronous request-body callbacks; NGINX request/config/connection pools; `ngx_chain_t` and `ngx_buf_t` ownership/flags; temporary/file buffers; dynamic-module ABI/build; module ordering with gzip/gunzip/brotli/charset/SSI/slice/range/proxy/FastCGI/gRPC/cache/mirror/auth_request; and worker-user/runtime-path permissions.

Pay special attention to:

- callback after request finalization/client disconnect;
- body already consumed or stored in temporary files;
- borrowed buffer lifetime and chain reuse;
- `last_buf` versus `last_in_chain`, flush, file buffers, sendfile/directio;
- request and response transformations before/after WAF inspection;
- cache/retry/internal-redirect paths that could bypass expected inspection;
- post-commit P4 Safe versus real Strict abort/reset;
- HTTP/2/HTTP/3 claims only when selected runtime evidence exists;
- worker identity/capability preflight before native runtime claims.

## Required common checks

Load all common modules except `filesystem-ipc.md` unless a selected NGINX harness/service path actually uses local IPC.

Required baseline modules:

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

## NGINX-specific validation seeds

Where repository-native harnesses support them, cover request-body memory/file paths, async callback timing, subrequest/main-request isolation, internal redirect/error_page, split/zero/file buffers, flush and EOS, module ordering, keepalive follow-up requests, worker reload/shutdown, bounded soak/memory diagnostics, and current native P4 cases.
