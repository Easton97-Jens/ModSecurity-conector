# Traefik source

**Language:** English | [Deutsch](README.de.md)

- `traefik_build_starter.c` provides compile-time metadata.
- `traefik_decision_service.h` / `.c` implement the local decision-service
  starter; `traefik_decision_service_main.c` provides `--decide-uri`.
- `traefik_modsecurity_mapper.c` adapts the Common request/response contracts.
- `traefik_forwardauth_service_main.c` selects the compatibility `forwardAuth`
  profile and the shared HTTP authorization runtime.
- `traefik_engine_service.c` implements the separate private-UDS native engine
  service with `--check-config --config PATH` and
  `--serve --config PATH --socket PATH` commands.

Product binaries no longer accept `--self-test`. Decision, engine protocol and
listener-ownership regression definitions now live in the pinned Framework
under `connector_native_tests/connectors/traefik/src/`. Fault-injection hook
state is Framework-owned; production compilation uses neutral operation seams.

From the Connector root run
`make -C connectors/traefik self-test-decision-service ON_DEMAND_TESTS=1` or
`make -C connectors/traefik test-engine-service ON_DEMAND_TESTS=1`.
The engine test additionally requires an explicit short external
`TRAEFIK_ENGINE_SOCKET_TEST_PARENT`; the Framework allocates a private child.
Native middleware tests run through `framework-go-test` with a read-only Go
overlay, preserving package-private assertions without adding tests to product
packages. Default Go selection remains inventory-limited; the full specialist
module is selected only with explicit `ON_DEMAND_TESTS=1`.

Harnesses, fixtures and runtime smoke scripts belong to Framework
`connector_suite/adapters/traefik/`. Product services and builds remain in the
Connector and do not load Framework code. Native middleware and compatibility
`forwardAuth` remain separate evidence profiles. A build or local test does not
promote hosted request/response support.
