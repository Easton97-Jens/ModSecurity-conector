# FND-SONAR-0015 — Der Compile-Database-Input erreicht eine Datei-Lesegrenze ohne Vertrag für eine private Capture-Root

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | security_candidate |
| Repository / Ownership | parent / parent |
| Priorität / Schwere / Confidence | P1 / high / probable |
| Status / Verifikation | closed (archiviert) / closed_by_current_user_after_current_master_compile_database_boundary_validation |
| Feasibility | feasible_now |
| Release-Blocker / sicherheitsrelevant | nein / ja |
| Profil | Parent-CI-Compile-Database-Ingestion |
| Delivery-Status | protected_squash_merged_resulting_master_workflows_verified |

## Zusammenfassung

Vor PR #98 konnte nicht verifizierter CLI-Input load_database(...).read_text nach nur einer grundlegenden Dateiprüfung erreichen, ohne expliziten Vertrag für private Capture-Root-Provenance oder Containment. Der exakte Head a2f2dd1f8bd2c433ee4cb107a0bf94281fbd7640 wurde geschützt per Squash als master 3311f3fd0e6dee01efc905e62f55bbdb3490ad20 gemergt. Alle 14 anwendbaren Master-Push-Workflows bestanden, und die drei zielgerichteten Basis-Sonar-Keys sind CLOSED/FIXED. Das projektweite Quality-Gate-ERROR gehört zu einem getrennten Basis-Backlog und wird dieser Remediation nicht zugerechnet.

## Beobachtetes und erwartetes Verhalten

Auf der Basis vor der Remediation konnte --input den JSON-Lesesink ohne Bindung an eine Capture-Root erreichen. Der Sonar-Key AZ9dWiALxi9ITghe3pzq erfasste einen Kandidaten mit hoher Auswirkung für pythonsecurity:S8707. Die aktuellen Repository-Call-Sites sind CI-eigene Bear-Wrapper; es ist kein Remote-, Cross-Principal- oder untrusted Same-UID-Caller-Pfad belegt.

Der nicht verifizierte Input muss eine absolute vorhandene reguläre Datei außerhalb des Checkouts und unterhalb einer absoluten, nicht verlinkten externen Capture-Root sein, die dem effektiven Benutzer gehört und für Gruppe/Andere nicht zugänglich ist. Root und Input müssen vor dem JSON-Lesen durch load_database validiert werden. Ein gültiger privater Capture muss weiter akzeptiert werden.

## Auswirkung und Security-Bewertung

Ohne den Vertrag konnte ein Aufrufer den CI-Helper zum Parsen einer beliebigen lesbaren Datei veranlassen. Der belegte Scope ist ein CI-lokaler Pfadintegritätskandidat, kein bewiesener Remote-Exploit. Das PR-spezifische Security-Review fand keine validierte Regression mit hoher oder kritischer Auswirkung in der Remediation.

Die Grenze verläuft von --input und --capture-root über external_capture_root, external_capture_input_path und captured_database_entries zu load_database und Path.read_text. Die zwei nicht verifizierten Wrapper erzeugen frische private mktemp-Roots und übergeben feste lokale Dateien. Eine Same-EUID-Replacement-Race wurde betrachtet, aber kein eigenständiger angreiferkontrollierter Writer in der privaten Root ist belegt. Die bereits vorhandene Output-Path-Grenze wird von diesem PR nicht verändert und liegt außerhalb dieses Befunds.

## Betroffene Dateien und Symbole

- ci/checks/analysis/compile_database.py — external_capture_root, external_capture_input_path, captured_database_entries, load_database, parse_arguments und main.
- ci/checks/analysis/compile-db-cpp17.sh und ci/checks/analysis/compile-db-nginx-c17.sh — übergeben die frische private Capture-Root.
- tests/test_c_cpp_diagnostics.py — Regression- und Legitimate-Control-Abdeckung.
- Der Change-Record mit seinem Sprachpaar und die Indizes.

## Voraussetzungen und Reproduktion

Der Pfad vor der Remediation benötigt eine nicht verifizierte Ausführung mit --input, die das JSON-Parsing erreicht. Für eine materielle Sicherheitsauswirkung über den Kandidaten-Scope hinaus wäre zusätzlich ein untrusted Caller oder eine Cross-Principal-Write/Read-Beziehung erforderlich.

Den alten nicht verifizierten Ablauf prüfen, um zu sehen, dass --input ohne Capture-Root-Validierung load_database(...).read_text erreicht. Auf dem exakten PR-Head fehlende Root, relativen Input, Checkout-Input, Escape- und Loop-Symlinks, unsichere Root-Rechte, Root-Symlink und Verify-Only-Missbrauch testen; alle müssen vor Parsing oder Publishing fehlschlagen. Eine gültige JSON-Datei unter einer privaten 0700-Capture-Root ist das Legitimate Control.

## Evidenz und Grenzen

- Task-Run 20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b beobachtete sieben fokussierte Tests in tests/test_c_cpp_diagnostics.py, elf Tests in tests/test_bilingual_docs.py, zwei Wrapper-Shell-Syntaxprüfungen und git diff --check als bestanden auf a2f2dd1f8bd2c433ee4cb107a0bf94281fbd7640.
- Der exakte Head bestand alle sechs verpflichtenden GitHub-Checks, CodeQL, OSV, SonarCloud Code Analysis, Report Governance und alle weiteren nicht übersprungenen PR-Checks. Die SonarCloud-Quality-Gate-API lieferte OK.
- Die PR-Issue-Abfrage lieferte ein Issue, AZ-QC5_F7_w-jke5-e7_, CLOSED/FIXED. Nach dem geschützten Merge erfasst die direkte Master-Key-Abfrage AZ9dWiALxi9ITghe3pzq, AZ9dWiALxi9ITghe3pzp und AZ9dWiALxi9ITghe3pzo am 2026-07-24T08:22:45Z als CLOSED/FIXED.
- Tool-Ausgaben wurden im Task beobachtet, aber kein separater Receipt wurde aufbewahrt. Die fokussierte Suite führt keine vollständige Bear-/Compiler-Capture-Integration aus.
- Es wurde kein Remote-Exploit, kein Cross-Principal-Caller und kein eigenständiger untrusted Same-UID-Writer belegt.

## Root Cause und vorgeschlagene Remediation

Der alte nicht verifizierte Ablauf behandelte den CLI-Wert nach nur einer grundlegenden Dateiprüfung als Datei. Er band ihn vor dem Lesesink nicht an eine private externe Bear-Capture-Root.

PR #98 verlangt --capture-root mit --input, prüft Pfadklasse, Eigentümerschaft und Rechte der Root, löst und begrenzt den Input und übergibt nur den validierten Pfad an load_database. Die zwei CI-Wrapper behalten ihren privaten mktemp-Capture-Ablauf. Diese Prüfungen und das gültige Private-Capture-Control dürfen nicht abgeschwächt werden.

## Akzeptanzkriterien und Validierungsplan

1. Der exakte Head a2f2dd1f8bd2c433ee4cb107a0bf94281fbd7640 weist jeden genannten unsicheren Root-/Input-Fall vor Parsing oder Publishing zurück und akzeptiert den gültigen privaten Capture.
2. Die sieben fokussierten Diagnose-Tests, elf Bilingual-Dokumentationstests, zwei Shell-Syntaxchecks, Diff-Check, Pflicht-Checks, CodeQL, OSV, SonarCloud und Quality Gate bestehen ohne Suppressions oder Control-Änderungen.
3. Der PR wurde geschützt per Squash nur auf dem exakten geprüften Head gemergt; resultierender master 3311f3fd0e6dee01efc905e62f55bbdb3490ad20 und alle 14 anwendbaren Master-Push-Workflows bestanden.
4. Die Sonar-Analyse auf master nach dem Merge dokumentiert die drei Basis-Keys als CLOSED/FIXED.

Der Plan für geschützten Merge, Master-Workflows und Exact-Key-Reanalyse ist abgeschlossen. Nur neu bewerten, wenn dieser CI-Helper später eine unterstützte Cross-Principal-Schnittstelle wird.

## Regression- und Legitimate-Control-Tests

- tests/test_c_cpp_diagnostics.py — sieben fokussierte Tests bestanden.
- tests/test_bilingual_docs.py — elf Tests für das Change-Record-Sprachpaar bestanden.
- Ein gültiger JSON-Capture unter einer externen 0700-Root im Besitz des aktuellen Benutzers wird akzeptiert und publiziert.
- Bestehendes gültiges Merge- und Verify-Verhalten bleibt durch die fokussierte Diagnose-Suite abgedeckt.

## Abhängigkeiten, Blocker und verwandte Befunde

Es gibt keine Framework- oder MRTS-Abhängigkeit. Bear-/Compiler-Integrationsvoraussetzungen sind optional und für diese fokussierte Grenz-Suite nicht erforderlich. Es gibt keinen aktuellen Delivery-Blocker; geschützter Merge und Master-Verifikation bleiben erforderliche Evidenz.

Die getrennte bereits vorhandene Output-Path-Grenze wird von diesem PR nicht verändert und liegt außerhalb dieses Befunds. Aus diesem Worktree wird kein kanonischer verwandter Finding-Record behauptet. Es gibt kein Duplicate.

## Restrisiko und Verlauf

Die Remediation ist auf dem geschützten resultierenden master verifiziert. Ein Same-EUID-TOCTOU-Kandidat ist nach der aktuellen Evidenz nicht reportable, weil kein eigenständiger untrusted Writer auf die private Root zugreifen kann; bei einer späteren Cross-Principal-Schnittstelle neu bewerten. Das getrennte projektweite Sonar-Quality-Gate-ERROR bleibt anderweitig verfolgt.

- 2026-07-24T08:16:22Z: Kanonischer Record als fixed mit Exact-Head-Validierung erstellt; geschützter Merge und Evidenz auf resultierendem master stehen noch aus.
- 2026-07-24T08:28:09Z: PR #98 wurde geschützt per Squash als master 3311f3fd0e6dee01efc905e62f55bbdb3490ad20 gemergt; alle 14 anwendbaren Master-Push-Workflows bestanden und die drei zielgerichteten Basis-Keys sind CLOSED/FIXED.
- 2026-07-26T14:09:02Z: Der aktuelle Nutzer autorisierte Abschluss und Archivierung; die betroffenen Pfade sind bis Parent-Master 6ca7e1536ce7e93da68099db9c586b88852ff13e unverändert und `tests.test_c_cpp_diagnostics` bestand in der 144-Test-Control-Suite.
