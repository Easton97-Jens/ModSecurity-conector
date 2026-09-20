# Protocol and Hardening Policy

## Transport dimensions

Treat H1 (HTTP/1.1), H2 (HTTP/2), and H3 (HTTP/3 over QUIC) as independent verification dimensions. `h2c` is distinct from TLS H2/ALPN.

A passed H1 result does not prove H2/H3, ALPN, QUIC/UDP, multiplexing/stream behavior, header compression, reset behavior, or transport-dependent strict behavior.

H2/H3 are normally optional/environment-dependent, but become mandatory when explicitly requested or when the change/claim touches transport-specific code/config/evidence, ALPN/QUIC/stream/header/reset logic, or an H2/H3 defect/compatibility claim.

A required unavailable transport yields truthful `blocked`/partial task outcome, not a pass.

## Runtime evidence

Transport claims require an actually forced/observed transport plus appropriate client-visible and host/connector correlation for the scope. Client-only output, a protocol label, build, config, or capability manifest is insufficient for a hosted connector lifecycle claim.

H3 claims additionally require actual QUIC/UDP evidence; do not retain raw sensitive connection identifiers.

## Normal build authority

Normal repository production-standard C/C++ builds remain authoritative. Hardened builds, sanitizers, static analysis, and future-language diagnostics are separate dimensions and cannot compensate for a failed/blocked required normal build.

## Hardening and sanitizers

Select diagnostic flags only after checking compiler/version, artifact type/linkage, host/SDK contract, and output root. Do not apply executable-only flags to shared/loadable artifacts or leak sanitizer/hardening flags into production configuration.

Report normal build, hardened build, ASan/UBSan/TSan/other sanitizer, static analysis, H1/H2/H3 separately. No passed dimension proves another.
