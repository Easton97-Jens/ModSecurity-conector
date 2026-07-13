# Ursprungsübersicht des Apache-Connectors

**Sprache:** [English](ORIGIN.md) | Deutsch

Status: adapter-owned source cleanup complete

Lokale Referenz: `<external-source-root>/ModSecurity-apache`
Upstream-Quelle: https://github.com/owasp-modsecurity/ModSecurity-apache
Source-Branch: `master`
Source-Commit: `0488c77f69669584324b70460614a382224b4883`
Source-Beschreibung: `v0.0.9-beta1-26-g0488c77`
Lizenz: Apache-2.0, aufbewahrt in `licenses/apache/`.

| Repository | Lokale Referenz | Upstream | Beobachteter Commit | Beobachtete Version/Tag | Lizenz |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-apache | `<external-source-root>/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |

Zentrale Attribution: `licenses/apache/`
Pro-Datei-Provenienz: `connectors/apache/SOURCE_MAP.json`
Adapter-eigener Build-Quell-Root: `connectors/apache/`
Produktive Quelldateien: `connectors/apache/src/`
Materialisierte Build-Quelle: `$BUILD_ROOT/apache-build/connector-src/`

## Status von Phase 11

Phase 11 verschob die Build-Eingabe des Apache-Connectors vom früheren
Referenzbaum `connectors/apache/upstream/` in den adapter-eigenen Bereich
`connectors/apache/src/`. Ein frischer materialisierter Autotools/APXS-Build
und ein realer Apache-Smoke-Run bestanden, bevor der frühere Upstream-Baum
entfernt wurde.

Dies war ausschließlich eine Migration des Quellstandorts. Apache-Hooks,
Filter, Bucket-Brigades, Interventionsübersetzung, Transaktions-Ownership,
YAML-Smoke-Semantik und die Klassifizierung von `RESPONSE_BODY` wurden nicht
geändert.

## Status von Phase 12

Phase 12 entfernte reine Attributions-/Historien-/Dokumentationsdateien aus
`connectors/apache/src/`, nachdem der Autoconf-Quellanker von `LICENSE` auf die
funktionale Quelldatei `src/mod_security3.c` umgestellt worden war. Der aktive
Apache-Quellbaum ist nun ein Build-/Runtime-Baum; dauerhafte Attribution bleibt
in `licenses/apache/`, dieser Ursprungsübersicht und
`connectors/apache/SOURCE_MAP.json`.

## Status von Phase 13

Phase 13 vereinfachte das adapter-eigene Layout, ohne die Runtime-Semantik zu
ändern. Autotools/APXS-Dateien liegen nun unter `connectors/apache/`,
produktive Apache-C-Quellen direkt unter `connectors/apache/src/`, und die
aufbewahrten Autotools-Testvorlagen liegen unter
`modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/`.
Der Materializer schreibt weiterhin das Upstream-kompatible Build-Layout unter
`$BUILD_ROOT/apache-build/connector-src`.

## Adapter-eigene Dateien

| Adapter-eigener Pfad | Ursprünglicher Pfad | Repository | Commit | Lizenz | Importgrund |
| --- | --- | --- | --- | --- | --- |
| `connectors/apache/autogen.sh` | `autogen.sh` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Autotools-Bootstrap |
| `connectors/apache/configure.ac` | `configure.ac` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Autotools-Configure-Quelle; der lokale Quellanker verweist nun auf `src/mod_security3.c` |
| `connectors/apache/Makefile.am` | `Makefile.am` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Automake-Build-Quelle |
| `connectors/apache/build/apxs-wrapper.in` | `build/apxs-wrapper.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | APXS-Build-Wrapper-Vorlage |
| `connectors/apache/build/ax_prog_apache.m4` | `build/ax_prog_apache.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache-Erkennungsmakro |
| `connectors/apache/build/find_apxs.m4` | `build/find_apxs.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | APXS-Erkennungsmakro |
| `connectors/apache/build/find_libmodsec.m4` | `build/find_libmodsec.m4` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | libmodsecurity-Erkennungsmakro |
| `connectors/apache/src/mod_security3.c` | `src/mod_security3.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache-Modul-Einstiegspunkt |
| `connectors/apache/src/mod_security3.h` | `src/mod_security3.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache-Modul-Header |
| `connectors/apache/src/msc_config.c` | `src/msc_config.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache-Connector-Konfiguration |
| `connectors/apache/src/msc_config.h` | `src/msc_config.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache-Connector-Konfigurations-Header |
| `connectors/apache/src/msc_filters.c` | `src/msc_filters.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache-Eingabe-/Ausgabefilter |
| `connectors/apache/src/msc_filters.h` | `src/msc_filters.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache-Filter-Header |
| `connectors/apache/src/msc_utils.c` | `src/msc_utils.c` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache-Connector-Hilfsfunktionen |
| `connectors/apache/src/msc_utils.h` | `src/msc_utils.h` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Apache-Connector-Hilfsfunktionen-Header |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/t/conf/extra.conf.in` | `t/conf/extra.conf.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | Von Configure-/Build-Eingaben referenziertes Testvorlagen-Layout |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/run-regression-tests.pl.in` | `tests/run-regression-tests.pl.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac`-Ausgabevorlage |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/regression/misc/40-secRemoteRules.t.in` | `tests/regression/misc/40-secRemoteRules.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac`-Ausgabevorlage |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/regression/misc/50-ipmatchfromfile-external.t.in` | `tests/regression/misc/50-ipmatchfromfile-external.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac`-Ausgabevorlage |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/regression/misc/60-pmfromfile-external.t.in` | `tests/regression/misc/60-pmfromfile-external.t.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac`-Ausgabevorlage |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/regression/server_root/conf/httpd.conf.in` | `tests/regression/server_root/conf/httpd.conf.in` | ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | Apache-2.0 | `configure.ac`-Ausgabevorlage |

## Repository-eigene Metadatendateien

| Pfad | Zweck |
| --- | --- |
| `connectors/apache/metadata.c` | Quellmetadaten für Zusammenfassungen/Reports |
| `connectors/apache/metadata.h` | Deklarationen der Quellmetadaten für Zusammenfassungen/Reports |
| `connectors/apache/SOURCE_MAP.json` | Maschinenlesbare Pro-Datei-Provenienz |

## Verschobene Attributionsdateien

| Früherer Quellbaum-Pfad | Dauerhafter Ablageort | Grund |
| --- | --- | --- |
| `connectors/apache/src/LICENSE` | `licenses/apache/LICENSE` | Der Lizenztext ist Attributionsmetadaten und keine Apache-Build-Eingabe, nachdem der Quellanker auf `src/mod_security3.c` verschoben wurde |
| `connectors/apache/src/AUTHORS` | `licenses/apache/AUTHORS` | Die Upstream-Attribution wird zentral aufbewahrt |
| `connectors/apache/src/CHANGES` | `licenses/apache/CHANGES` | Die Upstream-Änderungshistorie wird zentral aufbewahrt |
| `connectors/apache/src/README.md` | `connectors/apache/README.md` und Dokumentation unter `docs/` | Die Übersicht des Quellbaums gehört in die Connector-Dokumentation |

## Layout-Verschiebungen in Phase 13

| Früherer Pfad | Aktueller Pfad | Materialisierter Pfad |
| --- | --- | --- |
| `connectors/apache/src/autogen.sh` | `connectors/apache/autogen.sh` | `autogen.sh` |
| `connectors/apache/src/configure.ac` | `connectors/apache/configure.ac` | `configure.ac` |
| `connectors/apache/src/Makefile.am` | `connectors/apache/Makefile.am` | `Makefile.am` |
| `connectors/apache/src/build/` | `connectors/apache/build/` | `build/` |
| `connectors/apache/src/src/*.c`, `*.h` | `connectors/apache/src/*.c`, `*.h` | `src/*.c`, `*.h` |
| Apache-generierte Quellvorlage `t/conf/extra.conf.in` | `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/t/conf/extra.conf.in` | `t/conf/extra.conf.in` |
| Apache-generierter Quell-Testvorlagenbaum | `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/` | `tests/` |
| `connectors/apache/src/metadata.*` | `connectors/apache/metadata.*` | not materialized |
| `connectors/apache/src/SOURCE_MAP.json` | `connectors/apache/SOURCE_MAP.json` | not materialized |

## Ausgeschlossene Upstream-Dateien

Der vollständige Apache-Regressionsbaum, `.git`, `.travis.yml`, Release-Skripte,
generierte Autotools-Dateien, `.deps` sowie Build-/Runtime-Artefakte werden
nicht importiert. Der frühere Baum `connectors/apache/upstream/` wurde nach dem
Build- und Smoke-Nachweis von Phase 11 entfernt; er ist kein aktiver oder
erforderlicher Pfad mehr.

## Zentrale Attributionskopien

Die Upstream-Dateien `LICENSE`, `AUTHORS` und `CHANGES` von Apache werden unter
`licenses/apache/` für die repositoryweite Lizenzprüfung aufbewahrt. Diese
dauerhaften Kopien bleiben bestehen, obwohl der lokale Upstream-Referenzbaum
und die Duplikate im Quellbaum entfernt wurden.

## Bereinigungsprüfung

Der aktuelle [Connector-Integrationsleitfaden](../../modules/ModSecurity-test-Framework/docs/connector-integration.de.md)
des Frameworks dokumentiert die anwendbare Quell-/Kataloggrenze.

Adapter-eigener Apache-Quellcode darf nur nach einem funktionalen Ersatz,
aktualisierter Ursprungs-/Lizenzdokumentation und bestandener realer Evidenz
für `smoke-apache` und `smoke-all` reduziert werden. Kosmetisches Löschen ist
nicht erlaubt.
