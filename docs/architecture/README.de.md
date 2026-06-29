# Architekturdokumente

**Sprache:** [English](README.md) | Deutsch

Status: umgesetzt

Die Architekturdokumente definieren, was connector-neutral ist, was
serverspezifisch bleibt und wie gemeinsame Evidence auf Common-C-first-
Datenformen abgebildet wird.

## Dokumente

| Dokument | Zweck |
| --- | --- |
| `architecture.md` | High-Level-Repository-Architektur und libmodsecurity-v3-Transaktionsfluss |
| `c-vs-cpp-decision.md` | C-first-Public-API-Entscheidung und C++-Grenzen |
| `common-extraction-plan.md` | Was nach `common/` verschoben werden darf und wann |
| `common-runtime-boundaries.md` | Was die neuen Common-C-Helfer besitzen und was nicht |
| `adapter-owned-layer.md` | Adaptereigene Quellgrenzen neben beibehaltenen Upstream-Importen oder, für NGINX, nach der Upstream-Entfernung |
| `shadow-build-source-plan.md` | Generierte `$BUILD_ROOT`-Connector-Quellstrategie |
| `apache-adapter-owned-migration-plan.md` | Geplante Kriterien für die materialisierte Apache-Autotools-/APXS-Migration |
| `connector-adapter-interface.md` | Zukünftige Adapterverantwortlichkeiten und Berichtsmetadaten |
| `capability-model.md` | Capability-Vokabular für YAML-Cases und Zusammenfassungen |
| `status-model.md` | Runtime-, Import- und Common-Operation-Status-Mapping |
| `refactor-phase-1-plan.md` | Erster konservativer Common-Foundation-Plan |
| `refactor-phase-3-review.md` | Erste Implementierungsreview der Common-Extraktion |
| `refactor-phase-6-review.md` | Erste Review des adaptereigenen Source-Gerüsts |
| `refactor-phase-9-review.md` | Quellmigration im Besitz des NGINX-Adapters und PR #377-Status |
| `replace-and-reduce-plan.md` | Kontrollierte Upstream-Ersatzkandidaten und Phase-4-Entscheidung |

## Aktuelle Grenze

`common/` enthält nur connector-neutrale Typen, kleine Metadatenhelfer und
Dokumentation. `connectors/apache/` und `connectors/nginx/` besitzen jetzt die
connector-spezifischen Modul-Layouts, die Monorepo-Default-Builds über
`$BUILD_ROOT/apache-build/connector-src` und
`$BUILD_ROOT/nginx-build/connector-src` verwenden; ihre `src/`-Verzeichnisse
enthalten nur produktiven Connector-Quellcode. Apache-Hooks, NGINX-Filter,
serverspezifisches Config-Parsing und libmodsecurity-Transaction-Ownership
bleiben connector-spezifisch und gehören nicht Common.
