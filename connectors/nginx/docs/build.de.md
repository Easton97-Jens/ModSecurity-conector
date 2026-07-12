# NGINX-Build

**Sprache:** [English](build.md) | Deutsch

Status: Adaptereigener dynamischer Modulpfad

Der vollständige Repository-unterstützte NGINX-Kompilierungs- und lokale Verifizierungsablauf ist
dokumentiert im Root-Guide:

- [`docs/build/compilers/nginx.md`](../../../docs/build/compilers/nginx.de.md)

## Aktueller Build-Pfad

Der Helfer erstellt NGINX aus dem unterstützten Quellmodus und stellt libmodsecurity bereit
unter `BUILD_ROOT` und baut den Connector als dynamisches Modul auf:

```bash
git submodule update --init --recursive
REFRESH=1 BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

Standardmäßig ist die Connector-Quelle der Adapter-eigene Monorepo-Import:

```bash
MODSECURITY_NGINX_SOURCE_DIR=connectors/nginx
```

Legen Sie `MODSECURITY_NGINX_SOURCE_DIR=/path/to/ModSecurity-nginx` nur beim Testen fest
eine externe schreibgeschützte Kasse.

## Aktueller Laufzeitnachweis

| Beweissatz | Versucht | PASS | FEHLER | GESPERRT | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Standard-NGINX-Smoke-Test | 60 | 60 | 0 | 0 | 0 |
| NGINX erzwingt alles | 140 | 95 | 39 | 0 | 6 |

Laufzeitnachweise werden unter `/src/ModSecurity-conector-build/results/` geschrieben
und zusammengefasst in:

- `reports/testing/generated/nginx-runtime-results.generated.md`
- `reports/testing/test-coverage-overview.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft; begrenzte strikte Abbruchbeweise sind
nur als Laufzeitbeweis dokumentiert/gemeldet.
