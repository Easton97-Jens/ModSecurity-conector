# Change Record CR-20260826: P1–P4-Connector-Paritätsbaseline

**Sprache:** [English](CR-20260826-p1-p4-connector-parity-baseline.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260826-p1-p4-connector-parity-baseline` |
| Datum (UTC) | `2026-08-26` |
| Basis-Revision | `6ccfd8de555855ac540fc4d3d9e330f82d5e8cff` |
| Scope | Nur Parent: code-naher Baselinebericht, sein deutscher Begleiter, dieser gekoppelte Change Record und die zweisprachigen Change-Record-Archivindizes. Keine Connector-Source-, Framework-/MRTS-Source-, Gitlink-, Dependency-, CI-/Workflow-, Branch-Rule-, Required-Check- oder Hosted-Testkonfigurationsänderung. |

## Motivation und Problemstellung

Der Benutzer verlangte ein schrittweises P1–P4-Paritätsprogramm für zehn
genannte Connectorpfade aus einem separaten Worktree mit regelmäßig
aktualisiertem PR. Das erste Deliverable ist eine wahrheitsgemäße
Current-Master-Gap-Analyse und ein Ausführungsplan, keine spekulative Behauptung
von Runtime-Parität.

Dieser Dokumentationsmeilenstein liefert die erforderliche, evidenzbegrenzte
Prompt-1-Baseline.

## Akzeptanzkriterien

Seine konkreten Akzeptanzkriterien sind:

- P1–P4 aus Common-Source und Vektoren ableitet statt sie neu zu definieren;
- für alle zehn Pfade Source-/Harness-Einstiegspunkte, aktuellen Phasenstatus
  und konkrete Lücken festhält;
- Response-Phasenlücken bei ext_authz und forwardAuth als erforderliche
  Architekturarbeit statt als `not_applicable`-Ausnahmen behandelt;
- Source-Wiring von Real-Host-Evidenz trennt und die nötige
  Promotionsmatrix aufführt;
- Ownership überlappender Draft-PRs dokumentiert, ohne einen fremden Branch
  zu kopieren, mergen oder abzulösen; und
- CI sowie alle Security-Controls unverändert erhält.

## Implementierungsentscheidung und Begründung

- Der Bericht basiert auf aktuellem Parent-`master`, nicht auf den
  überlappenden, nicht gemergten Draft-PRs #344, #345 und #346.
- Er benennt eine ausdrückliche Benutzerentscheidung als nächstes
  Source-Ausführungsgate, um konkurrierende Implementierungen oder eine nicht
  autorisierte Integration dieser Branches zu vermeiden.
- Er behält `FND-PARENT-0234` als bestehendes release-blockierendes Finding
  bei und bezeichnet neue SPOP-Beobachtungen nur als plausible statische
  Kandidaten bis zur Runtime-Validierung.
- Der Bericht besitzt ein deutsches Gegenstück und wird mit diesem gekoppelten
  Change Record gemäß der ausdrücklichen Traceability-Policy des Repositorys
  und der vom Benutzer verlangten PR-Auslieferung aufbewahrt.

## Security-Auswirkung

Diese Baseline betrifft nicht vertrauenswürdige Request-/Response-Verarbeitung,
lokale Sockets, Prozesslebenszyklus und Eventintegrität. Sie ändert nur
Dokumentation und keine Security-Grenze. Sie erhält begrenzte
Event-Metadaten, den Ausschluss von Body-Payloads, Loopback-/TLS-/UDS-Defaults,
Validierung, Fail-Modi und Cleanup-Anforderungen. Kein Kandidat wird als
validiertes Finding oder als abgeschlossene Reparatur dargestellt.

## Geänderte Dateien

- `reports/audits/p1-p4-connector-parity-baseline.md`
- `reports/audits/p1-p4-connector-parity-baseline.de.md`
- `reports/audits/change-records/CR-20260826-p1-p4-connector-parity-baseline.md`
- `reports/audits/change-records/CR-20260826-p1-p4-connector-parity-baseline.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Inspektion von Code, Capabilities, Harnesses und Dokumentation für die zehn Pfade | Als schreibgeschützte Baseline-Review bestanden; die detaillierten Sources und Lücken stehen im gekoppelten Bericht. |
| `make check-bilingual-docs` | Nach Korrektur der Pflichtüberschriften des Records durch fehlenden Framework-Gitlink-Inhalt im Task-Worktree blockiert (Exit `2`). Die Wiederholung nannte nur bestehende fehlende Framework-Ziele, nicht die beiden neuen Baseline- oder Change-Record-Dateien. |
| `make check-doc-links` | Durch denselben fehlenden Framework-Gitlink-Inhalt blockiert (Exit `2`); die Repository-Path-Reference-Validierung meldete nur bestehende Framework-Ziele außerhalb dieser Änderung. |
| `git diff --check` | Nach der finalen Dokumentationskorrektur bestanden. |
| Connector-Build, Konfigurationsvalidierung oder Real-Host-P1–P4-Matrix | Nicht ausgeführt: Dies ist der bewusst dokumentationsbasierte Prompt-1-Meilenstein; Source-Implementierung wartet auf die Ownership-Entscheidung zu den überlappenden PRs. |

## Runtime-Evidence

Ein isolierter task-eigener Storage-Preflight für spätere lokale Builds und
Runtime-Evidenz bestand. Für diese reine Dokumentationsänderung wurde kein
Build, kein realer Host, kein Netz-Listener, keine Connector-Engine und keine
Runtime-Matrix gestartet. Dieser Record liefert deshalb keinen neuen
Runtime-Claim, keine Connector-Promotion und kein Hosted-Check-Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

- Connector-Build, Konfigurationsvalidierung und die Real-Host-P1–P4-Matrix
  werden in diesem reinen Prompt-1-Dokumentationsmeilenstein bewusst nicht
  ausgeführt. Sie benötigen Source-Implementierung und eine Ownership-
  Entscheidung zu den überlappenden Drafts.
- `make check-bilingual-docs` und `make check-doc-links` erreichten beide den
  fehlenden Framework-Gitlink-Inhalt und endeten mit Exit `2`. Ihre Ausgaben
  nannten nach der Korrektur der Pflichtüberschriften des neuen Change Records
  ausschließlich bestehende fehlende Framework-Ziele. Das Initialisieren oder
  Ändern von Framework-/Gitlink-Inhalt liegt außerhalb des gewählten
  Parent-only-Scopes; der Fehler wird deshalb als Umgebungseinschränkung
  dokumentiert, nicht umgangen.

## Bekannte Einschränkungen

Der isolierte Storage-Preflight ist eine Voraussetzung, keine Runtime-Evidenz.
Diese Änderung hat weder einen Connector promoted noch einen Ersatz für die
erforderlichen Real-Host-Ergebnisse je Pfad erstellt. Der Record kann weder
die Ownership der überlappenden Draft-PRs auflösen noch deren Code als Teil
dieses Branches beanspruchen.

## Verbleibende Risiken

Die bekannten P1–P4-Lücken, `FND-PARENT-0234` und die nicht validierten
SPOP-Kandidaten bleiben bestehen. Ein reiner Dokumentations-PR kann die in der
Baseline festgestellten Source-, Transport-, Ressourcen- oder
Eventintegritätsrisiken nicht reduzieren; spätere Änderungen müssen die
genannten Controls erhalten und jedes Ergebnis am exakten Delivery-Head
verifizieren.

Die Gesamtaufgabe verlangt ein frisches, laufgebundenes Evidenzbundle für jeden
genannten Pfad. Der für diesen Meilenstein erstellte PR bleibt ein Draft; kein
Merge, kein direkter `master`-Push, keine Framework-/MRTS-Modifikation, kein
Gitlink-Update, keine CI-Änderung und kein manueller Hosted-Check-Trigger sind
autorisiert oder werden behauptet.

## Finaler Diff- und Review-Status

Der Baselinebericht und dieser Record sind bereit für lokale
Dokumentationsvalidierung und eine enge Prüfung ihres finalen Diffs. Das
breitere Paritätsprogramm bleibt in Arbeit und darf erst als abgeschlossen
gemeldet werden, wenn alle zehn Pfade die angegebene Real-Host-
Akzeptanzmatrix erfüllen.
