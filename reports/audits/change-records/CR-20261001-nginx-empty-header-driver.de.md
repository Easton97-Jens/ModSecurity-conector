# Change Record: NGINX-Treiber für vorhandene Leerheader

**Sprache:** [English](CR-20261001-nginx-empty-header-driver.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261001-nginx-empty-header-driver` |
| Datum (UTC) | `2026-10-01` |
| Basis-Revision | `e9d022ed16d9df469baa9b12070786468706ced7` |

## Motivation und Problemstellung

Der Host-Request-Treiber übergab generiertes `Header: ` direkt an Curl. Curl
unterdrückt damit den Header, statt einen vorhandenen Leerwert zu senden.
Das ausgewählte Pflichtszenario erhielt deshalb seinen echten Stimulus nicht.

## Akzeptanzkriterien

Ein echter Loopback-Request beobachtet einen vorhandenen Leerheader. Fehlende
Header bleiben fehlend; nichtleere Werte mit Doppelpunkt und doppelte Header
bleiben erhalten. H1-Forcing, Body-/Output-Kontrollen und Containment bleiben.

## Implementierungsentscheidung und Begründung

Nur an der Curl-Grenze leere oder ein Leerzeichen umfassende Werte nach dem
ersten Doppelpunkt in `Header;` umwandeln. Das Framework-Header-Dateiformat
bleibt gleich. Kein Fixture-Sonderfall, neuer Result-Writer, Event-Produzent,
C-/Common-Eingriff oder automatischer Commit des vorbereiteten Protocol-Wirings.

## Security-Auswirkung

Der echte Stimulus entspricht dem Fixture, statt eine falsche Abwesenheit zu
erzeugen. Treiber schreiben keine nativen/kanonischen Events. Root-/nobody-
Ownership, geprüfte Pfade, native Evidence-Validierung und Payload-/Privacy-
Kontrollen bleiben unverändert.

## Geänderte Dateien

- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_empty_header_driver.py`
- `connectors/nginx/README.md` / `.de.md`
- Dieses EN/DE-Change-Record- und Archivindex-Paar

Die begleitende Framework-Runner-/Katalogänderung hat getrennte Repository-
Ownership und Delivery. Parent-Framework-/MRTS-Gitlinks bleiben unverändert.

## Ausgeführte Befehle

Alle Befehle verwendeten RTK. Drei echte Loopback-Kontrollen ergaben zunächst
einen erwarteten Fehler: Der Leerheader fehlte. Nach dem Treiberfix bestehen
alle drei; mit H1-Kommando-Regression bestehen fünf Tests. Der korrigierte
breite Parent-Fokuslauf besteht 103 Tests (Exit0), darunter Runtime-Pfad-
Resolver, Security, Lifecycle/Projection und Native-Sink, am unveränderten
alten physischen Framework-Pin. `sh -n`, `shellcheck -S error`, `git diff --check`
und `make check-bilingual-docs check-doc-links` bestehen. Anfänglich falsch
benannte Module und Record-Überschriften scheiterten und wurden korrigiert;
ihre Fehlprotokolle zählen nicht als PASS. Der vollständige ShellCheck behält
bestehende Warnungen an unveränderten Zeilen; keine Warnkontrolle wurde entfernt
oder unterdrückt.

## Runtime-Evidence

Ein isolierter Netzwerk-Namespace-Probe verwendete den vorhandenen C-Build
ohne Downloads: `nginx-empty_header_value-MKUpI7qd`. Task-Harness und externes
Framework-Fixture beobachteten HTTP 200, native Phase-1-Regel 1100503,
Master-UID 0, Worker-UID/GID 65534 und einen Ersatzworker nach Reload. Der
Port-Cleanup-Probe meldete freed. Der unveränderte offizielle Collector sah
das native Event; unveränderte Framework-Normalisierung akzeptierte den
einzelnen Source-Case. Das Ein-Case-Source-Aggregat ist FAIL, weil andere
Pflichtszenarien nicht liefen. Dies ist Diagnose-Evidence, kein neuer
Exact-Head-Canonical-PASS.

Die isolierte Nichtleerheader-Kontrolle `nginx-empty_header_value-pvB0el3W`
antwortete HTTP200, aber Harness-Exit1/Source-Case FAIL, ohne Zielregel oder
natives Event. Beide Attempts gaben ihre Ports frei. Unveränderter kanonischer
Normalizer und individuelle PASS-Completeness-Prüfung akzeptieren nur den
positiven Case. Die unveränderte Coverage-Diagnose meldet 53 fehlende Pfade
nach zuvor 54; die Auswahl bleibt 97. Dies sind lokale Pfadzahlen, keine
frische Full-E2E-Coverage.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Full-E2E, Gitlink-Update, Remote-CI, Push, PR-Eingriff oder Merge. Required-
Coverage bleibt rot; kein vollständiger kanonischer PASS oder E2E-SHA256SUMS.

## Bekannte Einschränkungen

Framework verlangt Präsenz und Leerwert gemeinsam für Regel 1100503; HTTP
200 allein beweist dies nicht. Einer der ursprünglich 54 fehlenden Pfade
hat einen lokalen echten Trigger; weitere Pfade brauchen getrennte Treiber/Evidence.

## Verbleibende Risiken

Eigene Curl-Wrapper müssen `Header;`-Semantik erhalten. Ein vollständiger
Lifecycle am neuen Exact Head bleibt notwendig; der vorhandene Build ist
nur diagnostisch.

## Finaler Diff- und Review-Status

Eine unabhängige Read-only-Prüfung fand keinen Blocker in diesem begrenzten
Treiber, Fixture und den Negativkontrollen. Die begrenzte Diff-/Whitespace-
Prüfung erhält die zwei vorbereiteten uncommitteten Protocol-Dateien außerhalb
dieses Teils. Der separate Parent-Commit ist nur lokal; keine Remote- oder
Gitlink-Aktion ist enthalten. Finale Dokumentationsprüfungen werden vor dem
Commit erneut ausgeführt. Keine Secrets oder fremden Änderungen.
