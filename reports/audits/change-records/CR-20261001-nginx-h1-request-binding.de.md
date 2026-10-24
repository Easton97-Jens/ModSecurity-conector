# Change Record: NGINX-H1-Case-Request-Binding

**Sprache:** [English](CR-20261001-nginx-h1-request-binding.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261001-nginx-h1-request-binding` |
| Datum (UTC) | `2026-10-01` |
| Basis-Revision | `75e2a24bcdc3ee97dab0d6f5a0e52e76b0b542c4` |

## Motivation und Problemstellung

Der NGINX-Legacy-Case-Request verwendete Curl ohne ausdrückliche H1-Option
oder Guard innerhalb von `send_case_request`. Allein die Auswahl eines H1-
Profils durch den Caller band den tatsächlichen Client-Befehl nicht, und eine
geerbte `curlrc` konnte ihn verändern.

## Akzeptanzkriterien

Ein H1-Case-Request setzt `-q --http1.1` an den Anfang der Curl-Argumente.
Direkte H2/H3-Aufrufe dieser H1-Funktion enden vor einem Request mit `77`.
Bestehende Header-, Body-, Timeout-, URL-, Response-/Error-Output-Validierung
und Statusbehandlung bleiben erhalten. Es wird keine Protokollversion oder ein
Runtime-Event synthetisiert.

## Implementierungsentscheidung und Begründung

Der Parent-Harness prüft `NGINX_DOWNSTREAM_PROTOCOL` an der Funktionsgrenze
und fügt `-q --http1.1` vor den bisherigen Curl-Argumenten ein. `-q` muss die
erste Curl-Option sein, damit `curlrc` ignoriert wird. Der H2/H3-Hostpfad
kennzeichnet Legacy-Cases bereits als nicht ausführbar; der lokale Guard
verhindert eine versehentliche direkte Wiederverwendung. Das getrennte
Parent-Selection/Init-Protocol-Wiring ist eine andere Änderung.

## Geänderte Dateien

- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_h1_request_protocol.py`
- `connectors/nginx/README.md` und `connectors/nginx/README.de.md`
- Dieses EN/DE-Change-Record-Paar und beide Archive-Index-Einträge.

## Ausgeführte Befehle

Alle Shell-Befehle nutzten RTK. Die Command-Capture-Regression scheiterte
zuerst wegen fehlender `-q --http1.1` und bei beiden direkten H2/H3-Aufrufen.
Nach der Korrektur bestanden ihre zwei Tests. Der kombinierte Parent-Fokuslauf
beendete 65 Tests mit Exit `0`
(`analysis/parent-canonical-protocol-focus-20261001.log`). `sh -n`,
`shellcheck -S error` und `git diff --check` bestanden. Ein vollständiger
ShellCheck-Lauf auf der vorherigen Audit-Pointer-Basis meldete Warnungen an
unveränderten Zeilen. Die erste
Bilingual-Prüfung beanstandete den deutschen Archiv-Link; nach der Korrektur
bestand `make check-bilingual-docs check-doc-links` mit dem Framework-Pin
`cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`.

## Security-Auswirkung

Das Ignorieren der `curlrc` verhindert, dass eine lokale Benutzerkonfiguration
diesen begrenzten Case-Request umleitet oder verändert. Bestehende Verified-
Output-Path-Prüfungen, Root-Master/`nobody`-Worker-Grenze, native Event-
Validierung und Collector-Autorität bleiben unverändert. Ein eigener `CURL`-
Wrapper muss `-q` und `--http1.1` akzeptieren.

## Runtime-Evidence

Die isolierte Diagnose unter
`/var/tmp/codex/ModSecurity-conector/runs/diagnosis/nginx-transaction_id_generated_or_fallback-oQ6cvxLb`
führte einen echten Request mit HTTP `200` aus. Die tatsächliche Audit-Request-
Zeile zeichnete `HTTP/1.1` auf; der Rollenbeleg zeigte Master-UID `0` und
Worker-UID `65534` mit Worker-Ersatz nach Reload. Das native Event enthielt
Regel `1100502`. Der unveränderte offizielle Parent-Collector bewertete
diesen einzelnen Source-Case als PASS, das Ein-Case-Aggregat blieb jedoch
`FAIL`, weil weitere Pflicht-Cases nicht liefen. Diese Diagnose ist kein
kanonischer oder Exact-Head-Lifecycle-PASS.

## Bekannte Einschränkungen

Der H2/H3-Legacy-Case-Pfad erzeugt weiterhin keinen promoteten Case-Request.
Für die verbleibenden 54 H1-Pflicht-Cases fehlen noch echte Runner und
Request-Coverage. Dieser Record umfasst nicht die getrennte Selection/Init-
Protokolländerung.

## Verbleibende Risiken

Der Kommando-Test belegt angeforderte Curl-Optionen, nicht die ausgehandelte
HTTP-Version jedes künftigen Laufs. Eigene `CURL`-Wrapper ohne diese Optionen
schlagen fehl. Für PASS ist weiterhin ein vollständiger Exact-Head-Lifecycle
erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Kein neuer Full-E2E, kanonischer PASS oder SHA256SUMS wird behauptet, solange
die Pflicht-Runner-Coverage rot ist. Remote-CI, Push, PR-Eingriff, Merge,
Framework-/MRTS-Source- oder Gitlink-Änderung gehören nicht zu dieser H1-
Korrektur.

## Finaler Diff- und Review-Status

Der H1-Source-Diff ist auf `send_case_request` begrenzt; dieser Record
dokumentiert den lokalen Nachfolger der Audit-Pointer-Basis.
Review und Delivery der kombinierten Parent-Änderungen verbleiben bei der
koordinierenden Aufgabe.
