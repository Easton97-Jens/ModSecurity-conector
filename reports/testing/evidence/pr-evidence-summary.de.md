# PR Zusammenfassung der Nachweise

**Sprache:** [English](pr-evidence-summary.md) | Deutsch

Status: umgesetzt

Dieses Repository speichert aus der Quelle stammende Smoke-Nachweise für den ModSecurity-Connector
Kompatibilitätsthemen. Die relevanten Upstream-Diskussionen sind:

| Topic | Upstream PR | Repository |
| --- | --- | --- |
| RAW argument collections | https://github.com/owasp-modsecurity/ModSecurity/pull/3564 | https://github.com/owasp-modsecurity/ModSecurity |
| NGINX phase-4 / `RESPONSE_BODY` behavior | https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377 | https://github.com/owasp-modsecurity/ModSecurity-nginx |

## Realer Verbindungspfad

Connector-Nachweise werden nur gezählt, wenn die Anfrage über Folgendes übermittelt wird:

```text
Client -> Apache/NGINX -> connector module -> libmodsecurity -> rule variables -> HTTP response
```

Der steckerfreie v3 API Smoke-Test unter `framework v3 API smoke helper/` ist nützlich API
Nachweis, aber es ist kein Apache- oder NGINX-Connector-Nachweis.

## Aktuelle evidenzbasierte Variablenfamilien

Die aktuelle lokale Standard-Connector-Zusammenfassung listet diese Familien auf
`verified_variables` für Apache und NGINX. Dies ist ein realer Connector
Zusammenfassende Nachweise nur für die standardmäßig ausführbaren Fälle. Es fördert nicht
xfail, „mapped-only“, „Future“, „connector-gap“, „runtime-difference“ oder „force-all“.
FAIL Fälle, und dies bedeutet nicht, dass die verfolgte Laufzeitmatrix `smoke-all`
Eintrag bestanden.

- `ARGS`
- `ARGS_NAMES`
- `REQUEST_HEADERS`
- `REQUEST_BODY`
- `REQUEST_COOKIES`
- `REQUEST_URI`
- `FILES`
- `XML`
- `AUDIT_LOG`
- `RESPONSE_HEADERS`

`RESPONSE_BODY` ist nicht verifiziert. Es bleibt xfail/mapped-only; siehe
`../../../modules/ModSecurity-test-Framework/docs/testing/response-body-blocking-investigation.md`
und `../generated/runtime/runtime-matrix.generated.md`.

## PR #377 Quellstatus

ModSecurity-nginx PR #377 wurde nur unter `$BUILD_ROOT` zur Überprüfung abgerufen.
Beobachteter PR Kopf: `3d72b004ff27a78ea19c6b945870e2cae62a97ac`.

Relevante Quelländerungen werden auf Adapter-eigene NGINX-Dateien angewendet:

- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`

Die Quellaufnahme PR wird nicht als Antworttextvalidierung gezählt. Aktiv
Der Erfolg des Connectors erfordert immer noch echtes HTTP-Verhalten durch Apache und NGINX.
und `RESPONSE_BODY` fehlt in `verified_variables`.

Phase 10 Quellabgeleitete PR #377 Testzuordnung in den Framework-Dokumenten hinzugefügt unter
`../../../modules/ModSecurity-test-Framework/docs/testing/pr377-test-import-map.md`.
Die importierten Nur-NGINX-Probes decken ab
minimal/safe/out-of-scope Phase-4-Protokollverhalten mit HTTP 200 Passthrough.
Strikte Abbrüche, ungültige Konfiguration, große Antworten und Blockierung gemeinsamer Antworttexte
bleiben xfail oder mapped-only.

## Reproduktion

```sh
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-all
BUILD_ROOT=/src/ModSecurity-conector-build make probe-response-body || true
```

Generierte Build-, Laufzeit-, Protokoll- und Ergebnisartefakte müssen unter bleiben
`BUILD_ROOT`.
