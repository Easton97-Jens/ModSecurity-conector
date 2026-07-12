# Roadmap

**Language:** English | [Deutsch](roadmap.de.md)


Status: current evidence-based roadmap snapshot

This roadmap records what the repository can currently prove from checked-in
code, generated reports, local result summaries, and documentation. Generated
coverage, mapped-only inventory, API-only smoke results, and source provenance
are useful evidence, but they do not by themselves promote connector behavior.

## Current Focus

- Keep Apache, NGINX, and HAProxy evidence scoped to the real-world connector
  path:
  HTTP client to server process to connector module to libmodsecurity to HTTP
  response.
- Keep generated report status aligned with `TEST-COVERAGE-SUMMARY.md`,
  `reports/testing/generated/canonical/full-runtime-matrix.generated.md`,
  `reports/testing/generated/canonical/final-consistency-audit.generated.md`, and
  `reports/testing/README.md`.
- Preserve the distinction between default local connector summaries and
  force-all/full-matrix evidence. Full-Matrix failures remain visible and
  classified; they are not blanket connector PASS proof.
- Keep `RESPONSE_BODY` non-verified and non-promoted until both Apache and
  NGINX return stable HTTP 403 for the same response-body blocking YAML case.
- Keep RAW argument collection work mapped-only until a configured local
  ModSecurity v3 source contains PR #3564 behavior and both connectors pass
  real HTTP smokes for the same YAML cases.
- Maintain source attribution, license, origin/provenance metadata, and adapter
  metadata drift checks while Apache, NGINX, and HAProxy source stays
  adapter-owned.

## Implemented

- Monorepo layout with repo-local Apache, NGINX, and HAProxy connector source
  trees under `connectors/apache/`, `connectors/nginx/`, and
  `connectors/haproxy/`.
- Placeholder scaffolds for `connectors/{envoy,lighttpd,traefik}/`.
- Connector-neutral C-first headers in `common/include/msconnector/` for
  directives, options/defaults, rule-load stats, request, response,
  transaction, intervention, capability, origin/provenance, logging, and
  status data shapes.
- Small connector-neutral helper implementations in `common/src/` for status,
  intervention, origin, and capability metadata.
- Apache and NGINX metadata files, `ORIGIN.md` files, `SOURCE_MAP.json` files,
  central attribution copies under `licenses/`, and drift checks through
  `ci/checks/common/check-adapter-metadata-drift.sh`.
- Adapter-owned Apache build inputs, APXS/Autotools files, harness files, and
  productive source under `connectors/apache/src/`.
- Adapter-owned NGINX module `config`, harness files, and productive source
  under `connectors/nginx/src/`, including recorded PR #377 phase-4 source
  provenance for NGINX files.
- Shared directive and option metadata used by Apache and NGINX without moving
  server hook/filter/runtime ownership into `common/`.
- Apache and NGINX support for the directive set documented in
  `docs/connectors/directive-parity.md`; NGINX-only phase-4 controls remain
  connector-specific.
- Rule-load stats metadata in
  `common/include/msconnector/rule_load_stats.h`; NGINX reports through its
  existing startup log path, while Apache stores the counters as internal
  config metadata only.
- Framework-backed public targets in the connector `Makefile`, including
  `make lint`, `make summary`, `make case-matrix`, `make smoke-common`,
  `make smoke-apache`, `make smoke-nginx`, and `make smoke-all`.
- YAML case corpus and generated report flow owned by
  `modules/ModSecurity-test-Framework`, with connector evidence emitted under
  `reports/testing/` and root summary copy `TEST-COVERAGE-SUMMARY.md`.
- Current generated coverage summary for 140 YAML cases, including 80 former expected-failure
  cases, 10 mapped-only import inventory entries, 11 connector-gap cases,
  13 runtime-difference cases, and 24 `RESPONSE_BODY` cases that remain
  non-verified.
- Runtime result metadata aligned with `msconnector_status`,
  `msconnector_origin`, and `msconnector_intervention` while keeping the
  shell/Python harness independent of C FFI.
- Real-world connector result metadata for Apache, NGINX, and HAProxy
  summaries, including server/proxy binary, connector module or SPOA/SPOP
  integration path, libmodsecurity path, origin, and verified variable families
  derived only from passing active/imported cases.
- Current generated default runtime evidence reports Apache 54 PASS /
  0 FAIL / 0 BLOCKED, NGINX 60 PASS / 0 FAIL / 0 BLOCKED, and HAProxy
  55 PASS / 0 FAIL / 0 BLOCKED. This is default-smoke evidence only; it is
  not a blanket stability claim for force-all, former expected-failure,
  mapped-only, future, or blocked cases.
- Current force-all runtime evidence reports Apache 100 PASS / 27 FAIL /
  0 BLOCKED, NGINX 95 PASS / 39 FAIL / 0 BLOCKED, and HAProxy 104 PASS /
  23 FAIL / 0 BLOCKED, with former expected-failure, future, connector-gap,
  runtime-difference, and response-body pass-through results not promoted.
- Current Full-Matrix evidence reports 3074 PASS / 782 FAIL / 0 BLOCKED. The
  final consistency audit recommends no next runtime-fixable connector cluster.
- Documentation for the capability model, status model, adapter interface,
  common runtime boundaries, directive parity, rule-load stats, source
  attribution, and license/origin policy.

## Next Milestones

- Promote the documented YAML case shape into a machine-readable schema after
  the shared YAML shape and connector-specific extension behavior settle.
- Extend shared fixture support for external files, schema/DTD/XML fixtures,
  file-backed operators, binary/NUL payload representation, and larger response
  fixtures.
- Keep `reports/testing/case-matrix.md` and generated matrix reports refreshed
  from current connector summaries without using them as standalone runtime
  proof.
- Reconcile tracked generated runtime reports with any newly executed local
  smoke results before updating PASS/FAIL wording in status docs.
- Add clearer connector-specific config-test support for cases that cannot be
  expressed as plain HTTP smokes, such as invalid NGINX phase-4 config.
- Add or refine stable audit-log parsers for section-aware checks; keep
  volatile fields out of required assertions.
- Promote NGINX-only TX scoring and redirect cases to common only after Apache
  equivalence is implemented, tested, and documented.
- Promote multipart filename/file-collection edge cases only after connector
  runtime evidence and native/semantic comparison justify promotion.

## Later / Deferred

- Envoy, Lighttpd, and Traefik remain deferred. They need stable Common
  metadata, stable harness behavior, a selected integration approach, and
  real-world connector summaries before any compatibility claim.
- HAProxy has an evidence-scoped SPOA/SPOP runtime path with default and
  force-all smoke evidence, while broader capability gaps remain reported and
  non-promoted.
- Apache parity for NGINX-specific phase-4 directives remains deferred.
- Common reporting for rule-load stats and Apache post-config display of those
  counters remain deferred until aggregation and merge semantics are designed.
- Further reduction of Apache/NGINX adapter-owned source remains deferred until
  equivalent behavior exists in maintained local code, attribution stays under
  `licenses/`, `ORIGIN.md`, and `SOURCE_MAP.json`, and relevant real-world
  smokes still pass.
- Full CRS v2/v3 compatibility comparison, performance baselines, graceful
  restart lifetime checks, vhost/UID audit-log scenarios, HTTP/2, streaming,
  and body-buffering coverage remain later work.
- A dedicated `smoke-api` target for connector-free v3 public C API regression
  candidates remains a possible addition; API-only results must stay separate
  from connector proof.

## Blocked / Waiting On

- `RESPONSE_BODY` blocking is waiting on stable Apache and NGINX real HTTP 403
  behavior for the same YAML probe. PR #377 source is recorded for NGINX, but
  source intake is not response-body validation.
- RAW argument collections are waiting on local ModSecurity v3 support for
  PR #3564 plus passing Apache and NGINX real-world smokes.
- XML schema/DTD validation, parser-error cases, file-backed operators,
  malformed multipart bodies, HTTP/2, streaming, and large body/response
  scenarios are waiting on explicit fixture and transport support.
- `v3_action_nolog_pass_no_audit` remains former expected-failure because local Apache/NGINX
  observations and GitHub Actions audit behavior have differed.
- Future connectors are waiting on a selected integration path and a real server
  harness that can emit the same status/origin/intervention metadata.
- Fresh environments can still be blocked until source downloads, toolchains,
  libmodsecurity builds, server builds, and connector module builds complete.

## Unknowns / Design Decisions

- Whether the YAML schema should be JSON Schema, a custom validator, or both.
- How much connector-specific YAML extension should be allowed in otherwise
  common cases.
- Where to draw the first durable Common runtime API boundary beyond metadata
  helpers without absorbing Apache hooks, NGINX filters, body handling, or
  transaction lifetime too early.
- How to represent response-body empty replies, late interventions, and
  already-sent-header behavior in a stable status model.
- Whether Apache response-body parity should use shared behavior, Apache-only
  directives, or a narrower documented support level.
- HAProxy integration path: SPOE service, Lua, or native filter.
- Envoy integration path: native C++ filter, external processing, Lua, or Wasm.
- Lighttpd integration path: native plugin or `mod_magnet`.
- Traefik integration path: plugin/middleware, Yaegi, Wasm, or another
  documented integration route.

## Recommended Next Actions

- Run `make lint`, `make summary`, and `make case-matrix` before changing
  status docs, then record the exact results.
- Run `make smoke-common`, `make smoke-apache`, `make smoke-nginx`, or
  `make smoke-all` only when the environment is expected to have the required
  local source-build prerequisites; record PASS/FAIL/BLOCKED exactly.
- Refresh generated reports with `make generate-test-matrix` and verify with
  `make check-test-matrix` whenever YAML cases, import status, or connector
  summary inputs change.
- Keep response-body blocking and RAW-ARGS in blocked/waiting-on sections until
  local source support and both real-world connector smokes prove them.
- Keep future connector work as design-only/deferred until Common metadata and
  harness behavior are stable enough to avoid copying Apache/NGINX assumptions.
- Keep source attribution and license files synchronized whenever connector
  source is moved, reduced, or refreshed.
