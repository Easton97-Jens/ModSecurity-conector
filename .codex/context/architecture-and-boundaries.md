# Architecture and Repository Boundaries

## Versioned authority

For current architecture and route identity, read the current checkout first, especially current product source, root `Makefile`, `docs/repository-concept.md`, `docs/architecture.md`, `docs/connectors/README.md`, affected connector docs/source, `docs/testing-and-evidence.md`, `ci/README.md`, and `tests/README.md`.

Do not freeze target names, runtime counts, capability claims, dependency versions, or point-in-time SHAs in local policy when the current repository can answer them.

## Ownership

- `common/`: host-neutral product contracts, bounded runtime support, decisions/events, limits, mapping helpers, payload-safe metadata.
- `connectors/<name>/`: host APIs, hooks/filters/middleware/services, host configuration, object lifetimes, host actions, connector build/install/harness seams.
- `ci/`: Parent orchestration, checks, lifecycle invocation, artifact producers/consumers, report generators.
- `config/`: versioned declarative contract/test inputs, not runtime secrets or general output.
- `tests/`: Parent repository contracts, not a duplicate Framework case corpus.
- Framework: reusable cases/catalogs/schemas/runners/normalizers/cross-connector report logic.
- MRTS: independent nested repository/tooling boundary; no implicit write or Gitlink authority.

A reusable Framework case or normalizer belongs in Framework. Host-specific product behavior belongs in Parent. Do not move logic across boundaries merely to avoid cross-repository work.

## Host families and logical profiles

Maintain separate evidence claims for the current logical profiles documented by the repository:

- Apache: direct native profile;
- NGINX: direct native profile;
- HAProxy: native HTX and SPOE/SPOP + response companion;
- Envoy: direct ext_proc and ext_authz + response observer;
- Traefik: native UDS middleware and forwardAuth + response observer;
- lighttpd: Stock sidecar and patched native.

Use current repository names/IDs from `docs/connectors/README.md`; this policy does not override them.

A compatibility/request-only component is not response-phase evidence. A response companion does not turn unrelated host evidence into a shared PASS. A sidecar and a patched native route are separate products/evidence paths.

## Evidence boundary

Build success, config loading, source wiring, a capability declaration, static analysis, scanner result, service self-test, or generated report does not by itself prove hosted runtime behavior. Limit claims to the actually exercised logical profile, rules/configuration, transport, revisions, and run evidence.
