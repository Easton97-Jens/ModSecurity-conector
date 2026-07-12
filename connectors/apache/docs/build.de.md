# Apache-Build

**Sprache:** [English](build.md) | Deutsch

Status: Migration der Adapter-eigenen Quelle abgeschlossen

Der vollständige, vom Repository unterstützte Apache-Kompilierungs- und lokale Verifizierungsablauf ist
dokumentiert im Root-Guide:

- [`docs/build/compilers/apache.md`](../../../docs/build/compilers/apache.de.md)

## Aktueller Build-Pfad

Der Helfer materialisiert die Connector-Quelle in `BUILD_ROOT` und erstellt
libmodsecurity/httpd-Abhängigkeiten auf Anfrage und verwendet die beobachteten
Autotools/APXS-Pfad:

```bash
git submodule update --init --recursive
REFRESH=1 BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

Standardmäßig ist die Connector-Quelle der Adapter-eigene Monorepo-Import:

```bash
MODSECURITY_APACHE_SOURCE_DIR=connectors/apache
```

Legen Sie `MODSECURITY_APACHE_SOURCE_DIR=/path/to/ModSecurity-apache` nur fest, wenn
Testen einer externen schreibgeschützten Kasse.

## Aktueller Laufzeitnachweis

| Beweissatz | Versucht | PASS | FEHLER | GESPERRT | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Standard-Apache-Smoke-Test | 54 | 54 | 0 | 0 | 0 |
| Apache Force-All | 133 | 100 | 27 | 0 | 6 |

Laufzeitnachweise werden unter `/src/ModSecurity-conector-build/results/` geschrieben
und zusammengefasst in:

- `reports/testing/generated/apache-runtime-results.generated.md`
- `reports/testing/test-coverage-overview.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft. Die Quelle leitet nun jeweils weiter
aktuelle Ausgangsbrigade vor EOS und endet bei EOS, aber sicher/strikt
Transportverhalten erfordert immer noch aktuelle Beweise für den realen Wirt.

## Common-Adoption C-Standardprüfungen

Die Apache/Common-Adoption-Kompilierungsschicht wird unabhängig von einem Apache überprüft
Laufzeitstart:

- `make check-apache-c17` ist der obligatorische C17-Smoke-Test.
- `make check-apache-c23` ist optional und wird übersprungen, wenn dem Compiler c23/c2x fehlt.
- `make check-apache-future-c` ist optional und überspringt, wenn der Compiler fehlt
  c2y/gnu2y.
- `make check-apache-c-standards` führt die obligatorischen und optionalen Profile aus.

Die Prüfung erkennt APXS über `APXS`, `apxs` oder `apxs2` und fügt APR-Flags hinzu
`apr-1-config`/`apr-2-config`, sofern verfügbar, und kompiliert nur Objekte. Das tut es
libmodsecurity nicht verknüpfen oder httpd starten. Fehlendes APXS oder Apache/APR/
libmodsecurity-Header werden als `BLOCKED` mit dem Exit-Code `77` gemeldet. Das ist
dient lediglich der Kompilierung/Strukturierung von Nachweisen und erhebt keinen Anspruch auf Produktionsbereitschaft, CRS
Abdeckung, vollständige Matrixabdeckung oder Laufzeitüberprüfung.

## APXS Common SDK-Objekteinbindung

Der APXS-Wrapper hängt die vom Apache benötigten Common SDK C-Quellen an
Adoptionsschicht zum Kompilierungsbefehl des Moduls. Dadurch bleibt der Build-Pfad erhalten
Eigentum von Apache, wobei Aufrufe wie Common Config Merge/Validation,
Mapper-Vertragsvalidierung, JSONL-Schreiben von Ereignissen, Regel-ID-Extraktion, Ressource
Grenzwerte und HTTP-Status-Helfer werden in das Apache-Modul kompiliert. Der Umschlag
fügt weiterhin `common/include` hinzu und fügt keine Apache-Typen zu Common hinzu.
