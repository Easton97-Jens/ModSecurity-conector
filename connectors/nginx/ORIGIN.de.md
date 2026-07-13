# Ursprungsübersicht des NGINX-Connectors

**Sprache:** [English](ORIGIN.md) | Deutsch

Status: adapter-owned source migration complete

Lokale Referenz: `<external-source-root>/ModSecurity-nginx`
Upstream-Quelle: https://github.com/owasp-modsecurity/ModSecurity-nginx
Source-Branch: `master`
Source-Commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
Source-Beschreibung: `v1.0.4-14-g9eb44fd`
Lizenz: Apache-2.0, aufbewahrt in `licenses/nginx/LICENSE`
Standard-Importpfad: `connectors/nginx`

| Repository | Lokale Referenz | Upstream | Beobachteter Commit | Beobachtete Version/Tag | Lizenz |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `<external-source-root>/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

Zentrale Attribution: `licenses/nginx/`

## Adapter-eigener Quellcode

NGINX baut nun aus einem materialisierten Quellbaum, der unter
`$BUILD_ROOT/nginx-build/connector-src` erzeugt wird. Das Modul `config` ist
adapter-eigen unter `connectors/nginx/config`, und produktiver Modulquellcode
ist adapter-eigen unter `connectors/nginx/src/`. Der frühere Referenzbaum
`connectors/nginx/upstream/` wurde in Phase 10 entfernt, nachdem die
Quellmigration, der Build des materialisierten Quellcodes und reale
NGINX-Smokes bestanden hatten.

| Adapter-eigener Pfad | Ursprünglicher Upstream-Pfad | Repository | Basis-Commit | Zusätzliche Provenienz | Lizenz | Importgrund |
| --- | --- | --- | --- | --- | --- | --- |
| `connectors/nginx/config` | `config` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX-Dynamic-Module-Build-Metadaten |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | `src/ngx_http_modsecurity_access.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX-Integration in der Access-Phase |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | `src/ngx_http_modsecurity_body_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` | Apache-2.0 | NGINX-Integration für Response-/Body-Filter plus Late-Intervention-Änderungen der Phase 4 |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | `src/ngx_http_modsecurity_common.h` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` | Apache-2.0 | Gemeinsame NGINX-Connector-Deklarationen plus Phase-4-Modus-/Konfigurationsfelder |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | `src/ngx_http_modsecurity_header_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX-Header-Filter-Integration |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | `src/ngx_http_modsecurity_log.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX-Integration in der Log-Phase |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | `src/ngx_http_modsecurity_module.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` | Apache-2.0 | NGINX-Modul-Einstiegspunkt/Konfiguration plus Phase-4-Direktiven |
| `connectors/nginx/src/ddebug.h` | `src/ddebug.h` | repository-eigener Kompatibilitäts-Header | n/a | ersetzt importierten Upstream-Debug-Helper | Apache-2.0-kompatibler Projektcode | Hält die NGINX-Modul-Build-Abhängigkeit erfüllt, ohne den importierten Debug-Helper in `upstream/` aufzubewahren |
| `connectors/nginx/metadata.c` | n/a | repository-eigene Adapter-Metadaten | n/a | none | Apache-2.0-kompatibler Projektcode | Ursprungsmetadaten für Report-/Build-Zusammenfassungen |
| `connectors/nginx/metadata.h` | n/a | repository-eigene Adapter-Metadaten | n/a | none | Apache-2.0-kompatibler Projektcode | Ursprungsmetadaten für Report-/Build-Zusammenfassungen |
| `connectors/nginx/SOURCE_MAP.json` | n/a | repository-eigenes Provenienzmanifest | n/a | zeichnet Basis- und PR-#377-Provenienz auf | Apache-2.0-kompatible Projektmetadaten | Quellmigrations- und PR-Provenienzübersicht |

## Layout-Verschiebungen in Phase 13

| Früherer Pfad | Aktueller Pfad | Materialisierter Pfad |
| --- | --- | --- |
| `connectors/nginx/src/config` | `connectors/nginx/config` | `config` |
| `connectors/nginx/src/metadata.*` | `connectors/nginx/metadata.*` | not materialized |
| `connectors/nginx/src/SOURCE_MAP.json` | `connectors/nginx/SOURCE_MAP.json` | not materialized |
| `connectors/nginx/src/README.md` | `connectors/nginx/README.md` und Dokumentation | not materialized |

## Aufnahme von PR #377

PR: https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377

Beobachteter PR-Head-Commit: `3d72b004ff27a78ea19c6b945870e2cae62a97ac`

Die PR-Quelländerungen wurden nur auf adapter-eigene NGINX-Quelldateien
angewendet:

- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`

Die importierten PR-Tests/-Dokumentation wurden nicht in die aktive Smoke-Suite
kopiert. Das Verhalten von Phase 4 / `RESPONSE_BODY` bleibt evidenzbasiert;
`RESPONSE_BODY` wird nicht zu `verified_variables` hinzugefügt, bis eine
separate Apache+NGINX-Real-World-Promotion stabiles HTTP-Verhalten beweist.

## Dauerhafte Attributionsdateien

| Attributionspfad | Ursprünglicher Pfad | Repository | Commit | Lizenz | Importgrund |
| --- | --- | --- | --- | --- | --- |
| `licenses/nginx/LICENSE` | `LICENSE` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Lizenztext für von NGINX abgeleiteten Adapter-Quellcode |
| `licenses/nginx/AUTHORS` | `AUTHORS` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream-Attribution |
| `licenses/nginx/CHANGES` | `CHANGES` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream-Änderungskontext |

## Ausgeschlossene Upstream-Dateien

Das NGINX-Test-Harness, `.git`, `.github`, CI-Dateien, Release-Skripte,
Windows-Build-Dateien, rohe Upstream-Tests und Build-/Runtime-Artefakte werden
nicht importiert. Die früheren Upstream-Dateien `config` und `src/*` wurden
nach `connectors/nginx/src/` migriert; das frühere Verzeichnis
`connectors/nginx/upstream/` wurde entfernt, nachdem Smokes des materialisierten
NGINX-Quellcodes bestanden hatten.

## Zentrale Attributionskopien

Die Upstream-Dateien `LICENSE`, `AUTHORS` und `CHANGES` von NGINX werden unter
`licenses/nginx/` für die repositoryweite Lizenzprüfung gespiegelt. Das
zentrale Lizenzverzeichnis ist die dauerhafte Attributionsquelle; diese
Ursprungsübersicht zeichnet auf, wie diese Dateien zum adapter-eigenen
Quellbaum gehören.

## Bereinigungsprüfung

Der aktuelle [Connector-Integrationsleitfaden](../../modules/ModSecurity-test-Framework/docs/connector-integration.de.md)
des Frameworks dokumentiert die anwendbare Quell-/Kataloggrenze.

`connectors/nginx/upstream/` wurde in Phase 10 entfernt. Künftige
NGINX-Quellreduktionen sollten `connectors/nginx/SOURCE_MAP.json`,
`licenses/nginx/` und diese Ursprungsübersicht aktualisieren und dann
nachweisen, dass `smoke-nginx` und `smoke-all` weiterhin bestehen.
