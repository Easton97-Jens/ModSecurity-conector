# Change Record: CR-20261018-traefik-verified-relay-tls

**Language:** English | [Deutsch](CR-20261018-traefik-verified-relay-tls.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-traefik-verified-relay-tls |
| Date (UTC) | 2026-10-18 |
| Base revision | `a29019558678222b88913be0e202db3c9d14323a` |


## Motivation and problem statement

The exact-head Sonar analysis of a29019558678222b88913be0e202db3c9d14323a reports S5332 on the synthetic authorization relay listener. Replace that plaintext listener with verified TLS; do not suppress or accept the issue.

## Acceptance criteria

Serve TLS with a fresh private runtime CA and an IP-SAN leaf for 127.0.0.1. Require CA trust and hostname verification; reject plaintext, wrong CA and wrong SAN before engine access. Preserve authorization-response capacity 32768 and all request/sample behavior. Keep private keys outside Git and published artifacts.

## Implementation decision and rationale

Use Python 3.14 HTTPSServer with TLS 1.2 minimum and HTTP/1.1 ALPN. Generate one-day synthetic certificates using existing OpenSSL, remove the CA private key immediately after signing, and retain the leaf key only in a private task directory. Configure the existing forwardAuth middleware with HTTPS, tls.ca and insecureSkipVerify: false before YAML validation and host startup. The pinned Traefik contract uses ClientTLS.ca, rather than serversTransport settings. Sources: [Python HTTPSServer](https://docs.python.org/3.14/library/http.server.html), [pinned Traefik ClientTLS](https://github.com/traefik/traefik/blob/fc92cc118a0557a029c7019d5ee06665127b0f13/pkg/types/tls.go), [pinned forwardAuth client](https://github.com/traefik/traefik/blob/fc92cc118a0557a029c7019d5ee06665127b0f13/pkg/middlewares/auth/forward.go).

Both synthetic `openssl req` operations explicitly use `-config /dev/null`. Every subject and certificate extension is supplied by the fixture, so certificate generation does not depend on the host OpenSSL configuration, which is absent in the private controller. The controller's filesystem exposure stays unchanged.

The exact-head 782f31ed analysis reports five S1192 duplicated filename literals. Named constants now bind those same artifact names across generation, verification, public receipts and cleanup. The OpenSSL argument values, public certificate names and private-key deletion behavior are unchanged; 31 TLS/quality/authorization regressions pass after this extraction. The strict hosted zero gate still requires a new analysis of the published correction.

## Changed files

The Traefik-specific i12_auth/auth_proxy.py binds HTTPS; i12_auth/tls_fixture.py creates bounded private certificates and configures trust; i12_auth/prepare.py stages that helper and records public certificate hashes only. tests/test_traefik_i12_tls.py and tests/test_traefik_i12_quality_controls.py verify real TLS and rejection boundaries. This paired Change Record documents the result.

## Commands executed

All local commands use RTK and the Parent virtual environment. The focused TLS, quality-control and authorization suite passed 30 tests before the final public-certificate manifest addition. The final combined TLS/quality/auth/source-export/native-measurement/ledger suite passed 58 tests in 17.594 seconds; bilingual-documentation and Change Record tests passed 42 tests. AST syntax for all five Python files and git diff --check passed; exact commands, exit codes and source hashes are retained in relay-tls/final.json under the external task evidence directory.

The private-controller preparation exposed the missing host configuration dependency before a host launch. A real regression with `OPENSSL_CONF` pointing to a nonexistent file failed before the correction. After explicitly selecting the empty configuration, 31 TLS/quality/authorization tests passed, including actual certificate-chain and IP-SAN verification with that missing configuration. Separate failure and passing receipts are retained as `checks/root-relay-missing-openssl-config-before-20261018.*` and `checks/root-relay-independent-openssl-config-after-20261018.*`.

## Security impact

Certificate-chain and IP hostname verification remain enabled. No verification bypass, package installation, issue-state change or Quality Gate weakening occurs. The generator rejects reused, symlinked, writable or foreign-owned paths. The relay rejects shared or symlinked private keys. CA private material is deleted after signing; do not publish or commit the remaining runtime server.key. Public receipts contain certificate hashes only.

## Runtime evidence

Real local TLS sockets prove successful verified sample forwarding, rejection of plaintext/untrusted/missing-CA/wrong-SAN connections before the stubbed engine collaborator, and a healthy TLS neighbor after rejection. Test servers stop and private temporary directories are removed. These are synthetic relay controls, not a Traefik host lifecycle claim. Existing a290 and acceptance captures remain sealed and unchanged.

## Known limitations

The upstream native authorization engine retains its existing private loopback HTTP transport. This change covers the HTTPS listener reported by S5332. Actual Traefik use of the generated CA and runtime cleanup still require a fresh separately owned host capture; existing captures cannot be relabeled.

## Remaining risks

One-day synthetic certificates must be generated immediately before each fresh capture. Private runtime leaf keys must remain excluded from evidence publication. A fresh exact-head hosted analysis is required before claiming that S5332 is resolved.

## Checks not run and rationale

No actual Traefik host, Go/race/vet run, hosted scan or Git/Sonar mutation is performed by this bounded fixture task. Parent owns integration, fresh host execution and hosted checks. The actual TLS server and certificate rejection paths are exercised locally.

## Final diff and review status

The bounded diff preserves maxResponseBodySize=32768 and existing sample/transport semantics, adds no product change and does not edit acceptance producers or sealed captures. The 58 regression tests, 42 documentation tests, five syntax checks and whitespace check passed; hosted and host acceptance remain outstanding.
