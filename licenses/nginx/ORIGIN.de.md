# Herkunft der NGINX-Connector-Lizenz

**Sprache:** [English](ORIGIN.md) | Deutsch

Status: implemented

Dieses Verzeichnis spiegelt die Upstream-Lizenz- und Attributionsdateien für
den kontrollierten NGINX-Connector-Quellimport. Der Standard-NGINX-Build-Source
ist nun adaptereigen unter `connectors/nginx/src`; der frühere
`connectors/nginx/upstream/`-Referenzbaum wurde in Phase 10 entfernt. Dieses
Verzeichnis ist der dauerhafte Attributionsort.

Lokale Repository-Referenz: `connectors/nginx/`, `licenses/nginx/`
Upstream-Source: https://github.com/owasp-modsecurity/ModSecurity-nginx
Source-Branch: `master`
Source-Commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
Source-Describe: `v1.0.4-14-g9eb44fd`
Lizenz: Apache-2.0
Standard-Importpfad: `connectors/nginx/src`

| Repository | Lokale Repository-Referenz | Upstream | Beobachteter Commit | Beobachtete Version/Tag | Lizenz |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `connectors/nginx/`, `licenses/nginx/` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

## Dateien

| Zentraler Pfad | Source-Pfad | Zweck |
| --- | --- | --- |
| `licenses/nginx/LICENSE` | Upstream `LICENSE` | Apache-2.0-Lizenztext für importierten NGINX-Connector-Source |
| `licenses/nginx/AUTHORS` | Upstream `AUTHORS` | Upstream-Attribution |
| `licenses/nginx/CHANGES` | Upstream `CHANGES` | Upstream-Änderungskontext |

## Importierte Source-Zuordnung

Die vollständige Dateifür-Datei-Source-Zuordnung bleibt in
`connectors/nginx/ORIGIN.md`. Die adaptereigene Source-Zuordnung zeichnet auch
die Source-Herkunft des ModSecurity-nginx-PR #377 auf:

- PR: https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377
- PR-Head-Commit: `3d72b004ff27a78ea19c6b945870e2cae62a97ac`
- Betroffene adaptereigene Dateien:
  `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`,
  `connectors/nginx/src/ngx_http_modsecurity_common.h` und
  `connectors/nginx/src/ngx_http_modsecurity_module.c`

Dieses zentrale Lizenzverzeichnis ist der dauerhafte Attributionsindex für
NGINX und ist mit der adaptereigenen `SOURCE_MAP.json` gepaart.
