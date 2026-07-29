# Change Record: Apache-Smoke-Harness Literal-Ownership und Diagnose-Streams

**Sprache:** [English](CR-20260729-sonar-apache-smoke-harness-maintenance.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-apache-smoke-harness-maintenance` |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `154ee724eba4653fa6378fc3c8729ae433e65697` |
| Tracking | Zehn aktuelle SonarQube-Cloud-Code-Smells in `connectors/apache/harness/run_apache_smoke.sh`: sechs `shelldre:S1192`-Befunde für wiederholte Literale und vier `shelldre:S7677`-Befunde für Diagnose-Streams. |
| Grenze | Parent-Apache-Smoke-Harness, sein fokussierter Source-Contract-Regressionstest und dieses englisch/deutsche Change-Record-/Index-Paar. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Der Apache-Smoke-Harness wiederholte feste Protokoll-, Curl-Format-,
Response-Marker-, Transport-Resultat- und Konfigurationsabschlusswerte an
mehreren Aufrufstellen. Vier branch-lokale Erfolgsmeldungen schrieben zudem auf
Standardausgabe, obwohl sie Diagnosen und keine maschinenlesbaren
Resultat-Payloads sind. Das verursachte die aktuellen SonarQube-Cloud-
Maintainability-Befunde.

## Akzeptanzkriterien

- Jeder der sechs von aktuellen `shelldre:S1192`-Befunden benannten festen
  Werte hat genau einen readonly-Shell-Owner, und alle operativen Nutzungen
  bewahren die bisherigen Bytes und Command-Argumente.
- Die vier `shelldre:S7677`-Phase-4-Erfolgsdiagnosen schreiben nach stderr und
  bewahren Text, Branch-Auswahl und Exit-Status null.
- Phase-4-Marker-Controls bleiben vorhanden und fail-closed; keine Regel, kein
  Test, Scanner oder Quality-Control wird gelockert.
- Fokussierte Shell- und Parent-Contract-Validierung besteht mit generiertem
  Bytecode und temporären Dateien außerhalb des Source-Checkouts.

## Implementierungsentscheidung und Begründung

Der Harness besitzt die betroffenen Werte jetzt in readonly-Variablen:
`PHASE4_RESPONSE_BODY_MARKER`, `APACHE_LOCATION_END`,
`HTTP2_PROTOCOL_LABEL`, `CURL_H2_ALPN_ACCEPT_PATTERN`,
`CURL_HTTP_STATUS_FORMAT` und `OBSERVED_TRANSPORT_HTTP_STATUS`. Curl-, Grep-,
Expected-Body-, generierte Konfigurations- und Evidence-Writer-Stellen
verwenden sie ohne Änderung ihrer Ausgabe.

Der Phase-4-Regression-Contract schützt Marker-Ownership direkt: Der Marker
erscheint einmal in der readonly-Deklaration, Expected-Bodies setzen dieselben
Bytes zusammen, und Marker-Suchen bleiben über die readonly-Variable erhalten.
Die vier Pass-Diagnosen verwenden `>&2`; ihre Meldungen und ihr Kontrollfluss
bleiben unverändert.

## Geänderte Dateien

- `connectors/apache/harness/run_apache_smoke.sh`
- `tests/test_apache_phase4_response_regression_wiring.py`
- `reports/audits/change-records/README.md`, `README.de.md` und dieses
  gepaarte Change Record

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| `sh -n connectors/apache/harness/run_apache_smoke.sh` | bestanden. |
| `shellcheck -S error connectors/apache/harness/run_apache_smoke.sh` | bestanden. |
| `python3 -m unittest tests.test_apache_phase4_response_regression_wiring tests.test_apache_smoke_mime_types tests.test_bilingual_docs` mit temporären Bytecode-/Cache-Pfaden | bestanden: 33 Tests. |
| `make check-apache-common-adoption` | bestanden; Apache/Common-Strukturadoption bleibt intakt. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Keine Netzwerkendpunkt-, Request-Parser-, Dateipfad-Policy-, TLS-Einstellungs-,
Regel-Semantik- oder Executable-Input-Grenze ändert sich. Der Harness nutzt
weiterhin seine bestehenden konfigurierten Runtime-Outputs. Readonly-
Literal-Ownership und Diagnoseumleitung lockern keine Validierungs-, Logging-,
Evidence-, Quality-Gate- oder CI-Kontrolle.

## Runtime-Evidence

Der fokussierte Source-Contract-Test weist nach, dass markertragende
Phase-4-Controls nach der Literalextraktion verbunden bleiben. Shell-Parsing
und ShellCheck prüfen die geänderte Syntax. Dies ist kein vollständiger
Apache-/modsecurity-Runtime-Smoke, und es wird keine Aussage zu HTTP/2, HTTP/3
oder einer vollständigen Connector-Matrix getroffen.

## Bekannte Einschränkungen

Der isolierte Worktree enthält die von der breiteren Response-Header-Suite
benötigte Framework-Runner-Fixture nicht. Apache-Host-Runtime und Framework
werden nicht verändert, um diese fehlende Abhängigkeit zu kompensieren.

## Verbleibende Risiken

Die gehostete Exact-Head-Analyse muss unabhängig bestätigen, dass die zehn
ausgewählten Code Smells ohne New-Code-Issues oder Duplizierung entfernt sind.
Eine spätere vollständige Apache-Runtime bleibt von diesem Source-Maintenance-
Batch getrennte Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

`tests.test_response_header_backend` ist in diesem isolierten Worktree
blockiert: Sein Helper beendet sich, weil
`modules/ModSecurity-test-Framework/tests/runners/runner_core.py` fehlt.
Keine vollständige Apache-Runtime, HTTP/2, HTTP/3 oder Connector-Matrix lief,
weil die nötigen lokalen Framework-/Host-Prerequisites nicht verfügbar sind.
Keine Source-Fixture, Suppression oder gelockerte Kontrolle ersetzt sie.

## Finaler Diff- und Review-Status

Der Kandidat ist auf den Parent-Apache-Harness, einen fokussierten
Regression-Contract und erforderliche bilinguale Traceability begrenzt.
Fokussierte lokale Prüfungen und Whitespace-Validierung bestanden; die breitere
Response-Header-Suite ist oben als blockiert erfasst. Zum Zeitpunkt der
Record-Erstellung werden kein Commit, Push, Pull Request, gehostete Analyse,
Review, Ready-for-Review-Umstellung oder `master`-Merge behauptet.
