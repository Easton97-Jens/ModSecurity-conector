> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# NGINX Blockierte Laufzeitfälle

**Sprache:** [English](nginx-blocked-runtime-cases.md) | Deutsch

Status: Historischer Blocker im aktuellen `/src`-Lauf behoben

## Aktuelles Ergebnis

Die letzten verifizierten `/src`-Läufe reproduzieren die 11 BLOCKED NGINX nicht mehr.
Laufzeitzeilen.

| Command | Result | Summary |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | NGINX 61 PASS, 0 FAIL, 0 BLOCKED |

Aktuelle Nachweise:

- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/nginx.rc`
- `/src/ModSecurity-conector-build/results/apache.rc`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`

## Historische BLOCKED Fälle

Im Status des vorherigen Berichts wurden NGINX als 43 PASS, 0 FAIL und 11 GESPERRT aufgezeichnet. Die
Aktuelle Ergebnisdateien wurden durch den erfolgreichen Wiederholungslauf überschrieben, also das genaue
Frühere pro-Fall-JSON-Zeilen sind im aktuellen Ergebnisverzeichnis nicht verfügbar.
Die unten aufgeführten historisch gesperrten Fallnamen sind von den früheren erhalten geblieben
`verified-runtime-run.md` Inhalt melden.

| Case | Expected status in current YAML summary | Current NGINX status | Current actual status | Current Apache status | Area | Current path |
| --- | ---: | --- | ---: | --- | --- | --- |
| `pr70_phase3_audit_response_header` | 403 | PASS | 403 | PASS | audit-log, phase3, response-headers | `modules/ModSecurity-test-Framework/tests/cases/audit-log/pr70-phases/pr70_phase3_audit_response_header.yaml` |
| `v2_transformation_url_decode_pass_no_match` | 200 | PASS | 200 | PASS | pass-through, phase1, request-uri, transformations | `modules/ModSecurity-test-Framework/tests/cases/negative-pass-through/v2_transformation_url_decode_pass_no_match.yaml` |
| `v3_args_names_get_pass_no_match` | 200 | PASS | 200 | PASS | args-names, pass-through, phase2, query-args | `modules/ModSecurity-test-Framework/tests/cases/negative-pass-through/v3_args_names_get_pass_no_match.yaml` |
| `v3_request_cookies_names_pass_no_match` | 200 | PASS | 200 | PASS | pass-through, phase1, request-cookies | `modules/ModSecurity-test-Framework/tests/cases/negative-pass-through/v3_request_cookies_names_pass_no_match.yaml` |
| `v3_request_cookies_pass_no_match` | 200 | PASS | 200 | PASS | pass-through, phase1, request-cookies | `modules/ModSecurity-test-Framework/tests/cases/negative-pass-through/v3_request_cookies_pass_no_match.yaml` |
| `v3_request_headers_names_pass_no_match` | 200 | PASS | 200 | PASS | pass-through, phase1, request-headers | `modules/ModSecurity-test-Framework/tests/cases/negative-pass-through/v3_request_headers_names_pass_no_match.yaml` |
| `action_allow_phase1_pass` | 200 | PASS | 200 | PASS | pass-through, phase1 | `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_allow_phase1_pass.yaml` |
| `phase2_args_pass` | 200 | PASS | 200 | PASS | pass-through, phase2, query-args | `modules/ModSecurity-test-Framework/tests/cases/phases/phase2/phase2_args_pass.yaml` |
| `response_body_pass` | 200 | PASS | 200 | PASS | pass-through, phase4, response-body | `modules/ModSecurity-test-Framework/tests/cases/response/body/response_body_pass.yaml` |
| `rule_chain_first_only_pass` | 200 | PASS | 200 | PASS | pass-through, phase2, query-args, rule-parser | `modules/ModSecurity-test-Framework/tests/cases/security/rule-chain/rule_chain_first_only_pass.yaml` |
| `rule_chain_second_only_pass` | 200 | PASS | 200 | PASS | pass-through, phase2, query-args, rule-parser | `modules/ModSecurity-test-Framework/tests/cases/security/rule-chain/rule_chain_second_only_pass.yaml` |

## Muster

Die historische Liste wird von Durchgangsfällen dominiert, die NGINX erfordern
`index.html` aus dem generierten Docroot bereitstellen. Der Blocker war also
Dies deutet eher auf ein Docroot-Leseproblem als auf einen ModSecurity-Regelfehler hin.

Die aktuelle Analyse in `nginx-docroot-permission-analysis.md` zeigt warum:
Wenn `NGINX_HARNESS_PARENT` in dieser Umgebung auf `/tmp` zurückgreift, wird der
Der Arbeiter kann `/tmp` nicht durchlaufen, da es sich um den Modus `700` handelt. Das aktuelle übergeordnete Element
Der Vertrag weist auf `NGINX_HARNESS_PARENT` und `BUILD_ROOT` hin, und die Wiederholungen werden durchgeführt.

## Vergleich mit Apache

Apache war in der Dokumentation nicht von demselben Docroot-Parent-Problem betroffen
laufen. Die neuesten gemeinsamen Zusammenfassungsdatensätze Apache 54 PASS, 0 FAIL, 0 BLOCKIERT.

## Entscheidung

Historische Klassifizierung: environment/docroot Berechtigungsblocker.

Aktuelle Klassifizierung: gelöst für `/src` läuft mit
`NGINX_HARNESS_PARENT=$(BUILD_ROOT)`.

Für den alten Lauf wird kein historischer Sperrfall als PASS gezählt. Der PASS-Status
stammt nur aus den oben aufgeführten neuen Wiederholungen.

Die frühere With-CRS-Erwartungsinkongruenz wird in den aktuellen `/src` behoben.
laufen. Es handelte sich nicht um ein erneutes Auftreten des docroot BLOCKED-Problems.

RESPONSE_BODY Sperrung bleibt bestehen `not verified`: `response_body_pass` ist ein
Pass-Through-Fall, kein blockierender Antworttext-Testfall.
