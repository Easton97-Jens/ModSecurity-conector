# Migrationsplan im Besitz des Apache-Adapters

**Sprache:** [English](apache-adapter-owned-migration-plan.md) | Deutsch

Status: umgesetzt bis Phase 12

Apache folgt jetzt demselben materialisierten Adapter-eigenen Quellmodell wie NGINX.
Bei der Migration bleibt das Upstream-Autotools/APXS-Layout im Inneren erhalten
`connectors/apache/src/` und erstellt aus einem verfügbaren, generierten Quellbaum
unter `$BUILD_ROOT/apache-build/connector-src`.

Phase 12 reduziert `connectors/apache/src/` auf funktionsfähige build/runtime-Eingänge.
Attribution/history-Dateien wurden aus dem Quellbaum verschoben und darin beibehalten
`licenses/apache/`; `configure.ac` verankert jetzt `AC_CONFIG_SRCDIR`
`src/mod_security3.c`.

## Aktueller Status

| Bereich | Aktueller Standort | Entscheidung |
| --- | --- | --- |
| Quellen für Apache-Module | `connectors/apache/src/*.c`, `*.h` | Adaptereigener Pfadbesitz; keine semantischen Änderungen |
| Autotools-Einstiegspunkte | `connectors/apache/autogen.sh`, `configure.ac`, `Makefile.am` | Adaptereigene Build-Eingaben unter Beibehaltung des Upstream-Layouts |
| Erstellen Sie macros/templates | `connectors/apache/build/*.m4`-, `.in`-Vorlagen | Adaptereigene Build-Eingaben bleiben erhalten, da `configure.ac` auf sie verweist |
| License/context-Dateien | `licenses/apache/`; `connectors/apache/ORIGIN.md`; `connectors/apache/SOURCE_MAP.json` | Dauerhafte Zuordnung außerhalb des funktionalen Build-Quellbaums |
| Provenienz pro Datei | `connectors/apache/SOURCE_MAP.json` | Maschinenlesbare Quellkarte für materialisierte Manifeste |
| Ehemaliger Upstream-Baum | `connectors/apache/upstream/` | Nach erfolgter Bau- und Smoke-Nachweis entfernt |

## Bewährter Build-Pfad

Monorepo-Standard-Apache-Builds verwenden:

```sh
MODSECURITY_APACHE_SOURCE_DIR=connectors/apache
APACHE_CONNECTOR_BUILD_DIR=$BUILD_ROOT/apache-build/connector-src
```

`modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh` materialisiert den Quellbaum und führt dann den aus
Standard-Autotools/APXS-Sequenz aus dem generierten Verzeichnis:

```sh
./autogen.sh
./configure --with-libmodsecurity=<BUILD_ROOT staging prefix> --with-apxs=<apxs>
make
```

Evidencebefehl:

```sh
REFRESH=1 BUILD_ROOT=/src/ModSecurity-conector-apache-final-build make smoke-apache
```

Dieser Evidence erstellte `mod_security3.so` über APXS und übergab den aktuellen Apache
reale Smoke-Suite, bevor der ehemalige Upstream- Baum entfernt wurde.

## Grenzen

Durch die Migration ändert sich nichts:

- Apache-Hook-Registrierung;
- input/output-Filter;
- Eimerbrigaden oder `send_error_bucket()`;
- request/response-Metadatenzuordnung;
- Besitz der libmodsecurity-Transaktion;
- Runtimesemantik der Intervention;
- YAML-Fallverhalten;
- `RESPONSE_BODY` non-promoted/mapped-only-Status.

## Verbleibendes Risiko

Apache ist immer noch anfälliger als NGINX, da Autotools, APXS-Erkennung,
generierte Vorlagen und das Verhalten von Apache filter/bucket sind eng miteinander verbunden.
Zukünftige Reduzierungen innerhalb von `connectors/apache/src/` erfordern eine dedizierte
before/after Evidence:

```sh
REFRESH=1 BUILD_ROOT=/src/ModSecurity-conector-apache-reduce-build make smoke-apache
BUILD_ROOT=/src/ModSecurity-conector-apache-reduce-build make smoke-all
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-all
```

Keine Quelldatei sollte entfernt werden, nur weil sie unbenutzt aussieht; Die
Materialisiertes Manifest und Smoke-Traces müssen die Reduzierung Evidencen.
