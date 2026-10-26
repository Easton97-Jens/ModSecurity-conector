# Change Record: CR-20261026-ubuntu26-workflow-migration

**Sprache:** [English](CR-20261026-ubuntu26-workflow-migration.md) | Deutsch



## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261026-ubuntu26-workflow-migration |
| Datum (UTC) | 2026-10-26 |
| Basis-Revision | `542a98bc20a16f885f114375bfa5225a9364dcf2` |

## Motivation und Problemstellung

Der Benutzer verlangt Ubuntu 26 für Connector- und Framework-Actions. Hosted-Runner-Labels explizit pinnen und geschütztes Self-hosted-Routing erhalten.

## Akzeptanzkriterien

Alle aktiven Hosted-Runner-Felder in Parent und Framework deklarieren ubuntu-26.04; geschützte Self-hosted-Runner behalten ihre expliziten Labels. Gates, unveränderliche Vertrauens-Pins und begrenzte Connector-E2E erhalten. Frische Hosted-CI muss vor Abschluss die Kompatibilität belegen.

## Implementierungsentscheidung und Begründung

Der aktuelle Parent-Baum enthält 66 tatsächliche runs-on-Felder in 34 Workflow-Dateien: 64 ubuntu-26.04 und zwei geschützte Self-hosted-Listen. Der neue native Security-Workflow ergänzt zwei Hosted-Felder. Die getrennt veröffentlichte Framework-Revision `5ef4dc3c815c97121578cd34382b80088b9c61ec` enthält 31 ubuntu-26.04-Felder in 18 Workflows. Der Parent-Framework-Gitlink bleibt unverändert. Exakte ergänzende actionlint-Labels und gezielte Runner-Vertragserwartungen folgen dieser Migration.

## Geänderte Dateien

Parent-Runner-Deklarationen in `.github/workflows/`, `.github/actionlint.yaml`, gezielte Workflow-/Toolchain-Verträge samt Fixtures sowie zweisprachige Sonar-Analyse-/Native-Leitfäden. Framework-Änderungen gehören zum getrennten PR #138. Dieser Record dokumentiert die Integration und beansprucht keine Ownership der übrigen nativen Security-Implementierung.

## Ausgeführte Befehle

Tatsächliche runs-on-Felder beider aktiver Worktrees mit schreibgeschützter Python-Auswertung über RTK gezählt. Native Change-Record-Vorlage mit ci/tools/new-change-record.py erzeugt. Für diese Dokumentationsänderung keine funktionalen Tests ausgeführt.

Die zugelassene integrierte Auswahl bestand **79 Ausführungen / 298 expandierte Fälle ohne Skips**, beim Inventar `06286b9ae1d1bac124a73c247893c2d522c15cce2dd52089a49f1bb7bd8759be`. Dieses deklariert 1956 Fälle / 911 Ausführungen: 97 Kernfälle / 77 Ausführungen plus 1859 autorisierte Offline-Fälle / 834 Ausführungen, mit 613 Quellbindungen und 1.654.103 Bytes. Die aufbewahrte Zusammenfassung ist `targeted-offline/active-tests-v3oeoia0/summary.json` im externen Lauf `parent-ubuntu26-20261026`. Enthalten sind der korrigierte NGINX-Test zum veralteten archivierten Vertrag unter Erhalt der Isolation und 97 statische Lighttpd-Grenzvarianten. Die Prüfung reproduzierte einen echten Helper-Fehler: Der Validator lehnte dessen nicht unterstütztes Capture-Schema ab; nach Korrektur des Capture-Pfads bestand die zugelassene Ein-Fall-Regression. Unabhängige Prüfung fand keinen weiteren konkreten Befund. Das erste Teilergebnis 78/297 und der frühere Native12-Zwischenstand 34/98 bei `f1df7bc865daa8863bf98e0afdd758e7b0a8298570ae2721d484c49badafc578` bleiben historisch und sind keine aktuellen Fehler. Statische AST-Prüfungen für 14 Dateien, Zweisprachigkeits-/Pfadprüfungen und natives actionlint bestanden; zizmor meldete keine Findings. Das sind lokale Nachweise, keine Hosted-Native12-Analyse.

## Security-Auswirkung

Runner-Labels ändern Buildumgebungen, keine Berechtigung. Gates, Berechtigungen, unveränderliche Revisions-Pins und geschützte Self-hosted-Grenzen bleiben erhalten. Der unveränderliche alte NGINX-Broker `49c40779a7b6de9f699391bcd524ea069787df42` akzeptiert nur ubuntu-latest und lehnt daher den migrierten Aufrufer ab. Die Kompatibilitätsvorbereitung liegt isoliert auf `fix/nginx-broker-ubuntu26-20261026`; geprüfte Master-Integration und anschließend ein geprüfter unveränderlicher Aufrufer-Pin bleiben erforderlich. Dieser Record autorisiert keinen Merge.

## Runtime-Evidence

Keine neuen Parent-Hosted-Ubuntu-26-Laufzeitnachweise. Zwölf native Entwicklungs-Captures enthalten zusammen 611 Parent-TU-Kompilierungen, keine eindeutigen Dateien oder Hosted-Analyse. Der Koordinator meldet 34 lokale Ausführungen / 98 expandierte Fälle erfolgreich beim Vor-Ubuntu-Inventar `f1df7bc865daa8863bf98e0afdd758e7b0a8298570ae2721d484c49badafc578`. Diese Ergebnisse übertragen sich nicht auf die geänderte Runner-Umgebung.

[Framework-Draft-PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138) ist getrennt bei `5ef4dc3c815c97121578cd34382b80088b9c61ec` veröffentlicht, mit 31 Ubuntu-26.04-Runner-Feldern. Tatsächlicher SDK-/Native-Build, Scanner-/JRE-Authentifizierung und Analyse waren erfolgreich: Eine C-TU mit acht Taint-Regeln sowie Python mit 32 Taint-Regeln wurden analysiert. CE-Task `AaF5sxOo8Px5fiPcdsNi` und Analyse `eb2599ca-c449-4e33-8cb3-e643eb0b593d` endeten mit `SUCCESS`. Das Gate ist ausschließlich wegen Security-Rating 3 `ERROR`; vier CLI-Flow-Behauptungen werden triagiert, Qualitätskorrekturen sind getrennte Arbeit. Elf andere CI-Workflows bestanden. Das ist echter Framework-Analyzer-Nachweis, kein bestandenes Security-Gate oder importierter Parent-Gitlink-Nachweis.

## Bekannte Einschränkungen

Der aktuelle uncommittete Ubuntu-/Native12-Stand besitzt keinen Hosted-Nachweis am veröffentlichten Head. Framework-Lieferung bleibt getrennt und wird durch den unveränderten Parent-Gitlink nicht importiert. Historische I12-Host-, Matrix- und Oracle-Kampagnen bleiben geschlossen.

## Verbleibende Risiken

Abweichende Ubuntu-Images und Toolchains können Build- oder Analyzer-Regressionen aufdecken. Der geschützte Aufrufer bleibt durch seinen unveränderlichen alten Broker-Vertrag blockiert. Die Benutzerfreigabe erlaubt jetzt ausschließlich PR #422 nach grünen Prüfungen und finalem Review, danach den geprüften Aufrufer-Pin; kein Merge ist erfolgt. Der neue Head `3d633ee27b48b64b940042e278c157f1aa629679` wartet nach Anwendung ausschließlich der geltenden Coverage-Abwahl auf CI. Lokale Konfigurationszählungen belegen keine Hosted-Runner-Verfügbarkeit oder erfolgreichen Scanner.

## Nicht ausgeführte Prüfungen mit Begründung

Frische Parent-Ubuntu-26-Hosted-Workflows, Native12-Analyzer-/Serverabschluss und geschützte Broker-Ausführung stehen aus. Der Dokumentationsagent führte keine funktionalen Tests, Dienste, Host-/Matrix-/Oracle-/I12-Kampagnen oder Provider-Schreibzugriffe aus.

## Finaler Diff- und Review-Status

Die Dokumentation ist für Roots Prüfung zusammen mit dem aktuellen Integrationsdiff vorbereitet. Der Abschluss bleibt von frischer einschlägiger Validierung und der Auflösung der vertrauenswürdigen Broker-Abhängigkeit abhängig.
