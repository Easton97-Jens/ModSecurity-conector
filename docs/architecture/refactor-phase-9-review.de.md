# Refactor-Phase-9-Überprüfung

**Sprache:** [English](refactor-phase-9-review.md) | Deutsch

Status: umgesetzt

Phase 9 migriert NGINX-Connector-Build-Eingaben aus der importierten Upstream-Quelle
Baum in eine dem Adapter gehörende Quelle unter Beibehaltung der Apache-, YAML-Semantik,
Die Klassifizierungen `verified_variables` und `RESPONSE_BODY` bleiben unverändert.

## Migrierte Dateien

Diese Dateien wurden von `connectors/nginx/upstream/` nach `connectors/nginx/src/` verschoben:

| Adaptereigener Pfad | Basisquelle | Zusätzliche Provenienz |
| --- | --- | --- |
| `connectors/nginx/config` | ModSecurity-nginx `config` und `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | keiner |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | ModSecurity-nginx `src/ngx_http_modsecurity_access.c` | keiner |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | ModSecurity-nginx `src/ngx_http_modsecurity_body_filter.c` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | ModSecurity-nginx `src/ngx_http_modsecurity_common.h` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | ModSecurity-nginx `src/ngx_http_modsecurity_header_filter.c` | keiner |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | ModSecurity-nginx `src/ngx_http_modsecurity_log.c` | keiner |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | ModSecurity-nginx `src/ngx_http_modsecurity_module.c` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` |

In Phase 10 wurde später die beibehaltene `connectors/nginx/upstream/`-Attribution entfernt
Der Baum nach dem Build wurde aus einer Quelle im Besitz des Adapters nachgewiesen und war dauerhaft
Die Zuordnung blieb in `licenses/nginx/`, `connectors/nginx/ORIGIN.md` und
`connectors/nginx/SOURCE_MAP.json`.

## PR #377 Aufnahme

PR: https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377

Beobachteter PR-Leiter-Commit: `3d72b004ff27a78ea19c6b945870e2cae62a97ac`

Relevante Quelländerungen wurden nur auf adaptereigene NGINX-Dateien angewendet:

- Handhabung des Körperfilters Phase 4;
- gemeinsame Header-Felder für Phase-4 mode/configuration;
- Modulanweisungen einschließlich `modsecurity_phase4_mode`,
`modsecurity_phase4_content_types_file` und `modsecurity_phase4_log`.

Rohe PR-Tests und Dokumentation wurden nicht in die Active Smoke Suite kopiert.

## Eingabe erstellen

Die Monorepo-Standard-NGINX-Quelle ist `connectors/nginx/src`. Der Build-Harness
materialisiert `$BUILD_ROOT/nginx-build/connector-src` aus dem adaptereigenen NGINX
`config` und Quelldateien sowie generierte Manifeste. Nach Phase 10 das Manifest
Es wird erwartet, dass es keine NGINX `upstream-derived`-Einträge enthält.

Externe `MODSECURITY_NGINX_SOURCE_DIR`-Überschreibungen verwenden weiterhin das bereinigte
Kopierpfad der externen Quelle.

## Status des Response Bodyes

Diese Phase fördert `RESPONSE_BODY` nicht. Die PR #377-Quelle kann sich ändern
Verbesserung des NGINX-Phase-4-Verhaltens, aber `RESPONSE_BODY` bleibt der ehemalige expected-failure/mapped-only
bis eine separate Evidencephase ein stabiles Apache- und NGINX-HTTP-Verhalten Evidencet
für einen gemeinsamen Sperrfall.

## Aufgeschoben

- Apache bleibt unberührt.
- Keine gemeinsame Extraktion von NGINX-Hooks, Filtern, Body-Handling, Response-Body
Semantik, Transaktionseigentum oder Interventionsabschluss.
- Es werden keine rohen Upstream- oder PR-Tests kopiert.
- Keine Änderung der YAML-Aktivfall-Semantik.

## Validierung

Die erforderliche Validierung für diese Phase ist:

```sh
REFRESH=1 BUILD_ROOT=/src/ModSecurity-conector-phase9-build make smoke-nginx
BUILD_ROOT=/src/ModSecurity-conector-phase9-build make smoke-all
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-all
BUILD_ROOT=/src/ModSecurity-conector-phase9-build make probe-response-body || true
```

`probe-response-body` dient nur der Evidenz und hat keine Auswirkungen
`verified_variables`.
