# Traefik Connector TODO

Status: minimal_runtime_smoke (forwardAuth request path only)
Runtime status: connector-gap outside the targeted request-header proof
Canonical No-CRS status: `supported_not_verified` / `NOT EXECUTED`
Metadata evidence states: `link_verified`, `minimal_runtime_smoke`, and `connector-gap`.

The standard compatibility path remains `forwardAuth`. The separate
full-lifecycle profile dispatches `native-middleware` through
`full-lifecycle-traefik-native`, which stages the Go module in a pinned
Traefik local-plugin host and selects a private persistent UDS
Common/libmodsecurity engine. Its targeted host evidence remains
non-promoted and cannot by itself promote a lifecycle capability.

Global gate definitions are consolidated in
`docs/connectors/README.md` and `docs/testing-and-evidence.md`.

## Phase 0: Scaffold

- [x] Connector directory created
- [x] README present
- [x] TODO present
- [x] docs present
- [x] harness contract documented
- [x] src placeholder documented
- [x] no local `connectors/traefik/tests` folder

## Phase 1: Origin / Metadata

- [x] `ORIGIN.md` added
- [x] `SOURCE_MAP.json` added
- [x] `metadata.*` added
- [ ] upstream Traefik source documented
- [ ] license documented for an upstream Traefik integration

## Phase 2: Build / Local Starter

- [x] build-starter approach documented
- [x] metadata build-starter command executed
- [x] decision-service starter implemented
- [x] decision-service starter command executed
- [x] decision-service local self-test executed
- [x] connector-owned forwardAuth service entry point implemented
- [x] C17 compile/link-only connector build implemented
- [x] libmodsecurity include paths supplied explicitly
- [x] libmodsecurity library paths supplied explicitly
- [x] connector service artifact path documented
- [x] config-check and process-only start-smoke separated from build
- [ ] production Traefik build logs documented

## Phase 3: Harness

- [x] `make smoke-traefik` targeted runtime-smoke entrypoint implemented
- [x] harness command documented
- [x] BLOCKED evidence path documented
- [x] common smoke result writer used instead of connector-local JSON writer
- [x] connector-local real Traefik -> forwardAuth -> service harness implemented
- [x] allowed request returns HTTP 200 in the targeted native runtime smoke
- [x] blocked request returns rule-backed HTTP 403 through forwardAuth
- [x] native Go middleware source/build groundwork added with focused local tests
- [x] native Go middleware is selected only by the separate full-lifecycle
      local-plugin target and remains excluded from the standard forwardAuth
      Phase-1 runtime contract
- [x] pinned Traefik local-plugin host probe stages the module, confirms loading, and routes a body-bearing request without capability promotion
- [x] persistent local Common/libmodsecurity UDS Engine bridge implemented
      and targeted real-host P1/P2/P3/P4-safe evidenced without promotion

## Phase 4: No-CRS Runtime

- [ ] `make test-no-crs` executed for Traefik scope
- [ ] PASS/FAIL/BLOCKED counts documented
- [x] Architecture boundary recorded in `capabilities.json`: Traefik 3.7 can
      buffer a forwardAuth body, but the checked-in forwardAuth path does not enable
      `forwardBody` and uses `request_body_mode=none`; Phase 2 is therefore
      `not_implemented` for the selected path.
- [x] Upstream response headers and bodies are recorded as
      `unsupported_by_host_model` for `forwardAuth`.
- [ ] `make no-crs-baseline-traefik` produces current canonical evidence.
- [ ] `make evidence-check-traefik` validates the result and does not use the
      legacy Python/evaluator body probe as native service evidence.

## Phase 5: With-CRS Runtime

- [ ] `make test-with-crs` executed for Traefik scope
- [ ] CRS loaded/effective evidence documented
- [ ] PASS/FAIL/BLOCKED counts documented

## Phase 6: Coverage Matrix

- [ ] Phase 1/2/3/4 runtime status documented
- [ ] negative/pass-through status documented
- [ ] audit/log evidence documented
- [ ] RESPONSE_BODY blocking evaluated

## Phase 7: Promotion

- [ ] eligible for `adapter-owned`
- [ ] eligible for `runtime-smoke-verified`
- [ ] eligible for `crs-verified`
- [ ] eligible for promotion beyond targeted `minimal_runtime_smoke`
- [ ] current-commit runtime evidence promotes service source beyond `connector-gap`

## Compatibility and native Phase-4 boundary

The compatibility `forwardAuth` integration executes before upstream handling.
The following facets are therefore `unsupported_by_host_model` for that path:
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`, `late_intervention_log_only`,
`late_intervention_abort`, and `late_intervention_status_metadata`.

- [x] Keep compatibility Phase-4 cases `UNSUPPORTED`, not `NOT EXECUTED`,
      because that host model cannot receive the later upstream response.
- [x] Native UDS host probe records P4 safe `log_only` after commit with a
      visible 200; strict late abort is explicitly `NOT EXECUTED`.
- [x] Native Safe probe requires an HTTP/1.1 same-connection follow-up and
      writes only a diagnostic, non-promoting sidecar; incomplete host writes
      do not synthesize response EOS.
- [ ] Do not use request-side 200/403, `forwardBody`, or any decision-service
      self-test as response-body, late-action, original-status, visible-status,
      or connection-abort evidence.
- [ ] Extend the native host path with cancellation/disconnect and strict-abort
      evidence before any capability promotion.
