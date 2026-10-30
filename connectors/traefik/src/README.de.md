# Traefik-Quellcode

**Sprache:** [English](README.md) | Deutsch

- `traefik_build_starter.c` bietet Metadaten zur Kompilierungszeit.
- `traefik_decision_service.h` / `.c` implementieren den lokalen
  Decision-Service-Starter; `traefik_decision_service_main.c` bietet
  `--decide-uri` an.
- `traefik_modsecurity_mapper.c` adaptiert die Request-/Response-Verträge von
  Common.
- `traefik_forwardauth_service_main.c` wählt das Kompatibilitätsprofil
  `forwardAuth` und die gemeinsame HTTP-Autorisierungslaufzeit aus.
- `traefik_engine_service.c` implementiert den separaten nativen Engine-Dienst
  über eine private UDS mit den Befehlen `--check-config --config PATH` und
  `--serve --config PATH --socket PATH`.

Produktprogramme akzeptieren `--self-test` nicht mehr. Regressionen für
Entscheidungen, Engine-Protokoll und Listener-Eigentum liegen nun im gepinnten
Framework unter `connector_native_tests/connectors/traefik/src/`. Der Zustand der
Fehlerinjektions-Hooks gehört zum Framework; Produktkompilierung verwendet
neutrale Operationsschnittstellen.

Aus dem Connector-Wurzelverzeichnis erfolgen die Aufrufe mit
`make -C connectors/traefik self-test-decision-service ON_DEMAND_TESTS=1` oder
`make -C connectors/traefik test-engine-service ON_DEMAND_TESTS=1`.
Der Engine-Test verlangt zusätzlich ein explizites kurzes externes
`TRAEFIK_ENGINE_SOCKET_TEST_PARENT`; das Framework erzeugt darin ein privates
Unterverzeichnis. Native Middleware-Tests laufen über `framework-go-test` mit
einem schreibgeschützten Go-Overlay. Assertions mit Zugriff auf private
Paketsymbole bleiben erhalten, ohne Tests in Produktpakete einzufügen. Die
Standardauswahl bleibt inventarbegrenzt; das vollständige Spezialmodul wird nur
mit explizitem `ON_DEMAND_TESTS=1` ausgewählt.

Harnesses, Fixtures und Runtime-Smoke-Skripte gehören zum Framework unter
`connector_suite/adapters/traefik/`. Produktdienste und Builds bleiben im
Connector und laden keinen Framework-Code. Native Middleware und das
Kompatibilitätsprofil `forwardAuth` bleiben getrennte Nachweisprofile. Ein Build
oder lokaler Test promotet keine Request-/Response-Unterstützung im Host.
