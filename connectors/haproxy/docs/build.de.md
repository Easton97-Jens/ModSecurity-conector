# HAProxy Build

**Sprache:** [English](build.md) | Deutsch

Status: Produktions-SPOA-Laufzeit-Build verfügbar

Der vollständig vom Repository unterstützte HAProxy-Kompilierungs- und lokale Verifizierungsablauf
ist im Root-Guide dokumentiert:

- [`docs/build/compilers/haproxy.md`](../../../docs/build/compilers/haproxy.de.md)

## Aktueller Build-Pfad

```bash
git submodule update --init --recursive
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-spoa-runtime
make smoke-haproxy
```

Die Produktions-SPOA-Binärdatei wird bereitgestellt unter:

```text
/src/ModSecurity-conector-build/haproxy-spoa-runtime/haproxy-modsecurity-spoa
```

Die HAProxy-Binärdatei wird erstellt unter:

```text
/src/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy
```

## Aktueller Laufzeitnachweis

| Beweissatz | Versucht | PASS | FEHLER | GESPERRT | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Standard-HAProxy-Smoke-Test | 55 | 55 | 0 | 0 | 0 |
| HAProxy Force-All | 133 | 104 | 23 | 0 | 6 |

Die Beweise sind zusammengefasst in:

- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/haproxy-summary.json`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `reports/testing/haproxy-poc.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

Phase 4 / RESPONSE_BODY ist `not_implemented` im ausgewählten SPOE/SPOP-Pfad.
Das ehemalige `wait-for-body`-Strict-Abort-Beispiel ist deaktiviert, veraltet und
nichtkanonisch; Es handelt sich nicht um aktuelle Laufzeitbeweise.

## Über den gesamten Lebenszyklus ausgewählter nativer HTX-Transport-Build

Das Full-Lifecycle-Profil wählt diesen separaten nativen Precommit-Pfad aus
`full-lifecycle-haproxy-htx`. Es erstellt einen verfügbaren, gepatchten HAProxy 3.2.21
Arbeitsbaum und ersetzt nicht die SPOE/SPOP-Binärdatei:

```sh
HAPROXY_HTX_SOURCE_DIR=/absolute/path/to/haproxy-3.2.21 \
  MODSECURITY_INCLUDE_DIR=/absolute/path/to/include \
  MODSECURITY_LIB_DIR=/absolute/path/to/lib \
  BUILD_ROOT=/srv/modsecurity-work/haproxy-htx-smoke \
  make -C connectors/haproxy runtime-smoke-haproxy-htx
```

Das Ziel prüft die Quellversion und wendet den Patch nur in der verfügbaren Version an
Arbeitsbaum, schreibt Overlay/Binär-SHA-256-Herkunft, validiert ein generiertes
Die `filter modsecurity-htx`-Konfiguration lädt das kanonische No-CRS des Frameworks
Regeln und startet HAProxy gegen einen lokalen Upstream. Es beweist, dass es sich um einen echten Kunden 403 handelt
und 429 P1-Antworten (`1100001`/`1100002`) und eine echte P3 403-Antwort (`1100201`)
ohne Pufferkörper. P2/P4 bleiben nur der Beobachtung vorbehalten. Der Lauf ist still
explizit nicht hochgestuft: keine Umleitung, Post-Commit-Abbruch, Common-Runtime-Brücke,
oder die Selected-Path-Fähigkeit beansprucht wird. Verwenden Sie ein frisches `BUILD_ROOT`; die Überlagerung
Der Builder weigert sich, einen Arbeitsbaum wiederzuverwenden.
