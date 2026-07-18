# Change Record: Sicherheitsrichtlinie und Governance-Baseline

**Sprache:** [English](CR-20260718-security-policy-governance.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-security-policy-governance` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Grenze | Nur Parent-Dokumentation und GitHub-Repository-Governance; Produktquellcode, Produkttests, Framework, MRTS, Gitlinks und `master` bleiben unverändert. |

## Motivation und Problemstellung

Das Repository hatte keine von GitHub erkannte `SECURITY.md`, obwohl Private
Vulnerability Reporting verfügbar war. Dem aktuellen Scorecard-Finding
Security-Policy fehlte damit ein auffindbarer vertraulicher Meldeweg. Diese
Änderung fügt eine wahrheitsgemäße öffentliche Richtlinie hinzu, die Berichte
ohne Veröffentlichung privater Kontaktdaten oder Secrets an GitHub Private
Vulnerability Reporting leitet.

## Akzeptanzkriterien

- Root-`SECURITY.md` und `SECURITY.de.md` liefern gleichwertigen englischen und
  deutschen Richtlinieninhalt mit wechselseitigen Sprachlinks.
- Die Richtlinie leitet Meldende auf die GitHub-Private-Reporting-URL des
  Repositorys, rät von einer öffentlichen Offenlegung sensibler Details ab und
  enthält keine privaten Kontaktdaten, Zugangsdaten oder Secrets.
- Die Dokumentation wird nur auf diesem dedizierten Branch und Pull Request
  erstellt.
- Bilinguale Dokumentations-, Link-, Whitespace- und Scoped-Diff-Kontrollen
  bestehen, bevor der Pull Request als lokal validiert berichtet wird.

## Implementierungsentscheidung und Begründung

Der Root-Dateiname ist GitHubs auffindbarer Ort für Sicherheitsrichtlinien. Die
Richtlinie bleibt absichtlich knapp: Sie beschreibt den privaten Meldekanal,
die Grenze unterstützter Versionen, den Umfang sicherer Forschung sowie
Erwartungen an Reaktion und Offenlegung, ohne eine erfundene Service-Level-Zusage
zu machen. Die vollständige deutsche Begleitfassung folgt der Richtlinie für
benutzergerichtete Repository-Dokumentation.

## Geänderte Dateien

- `SECURITY.md`
- `SECURITY.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- Dieses englische/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `git status --short --branch` im dedizierten temporären Clone | vor der Bearbeitung bestanden: sauberes `master...origin/master`. |
| `git switch -c codex/security-policy-20260718` im dedizierten temporären Clone | bestanden: Task-eigenen Branch von Basis-Revision `c8ca0d92b630c18232b881855c4f5d1482568ea6` angelegt. |
| GitHub-Repository-Governance-Readback | vor der Dokumentationsarbeit bestanden: Private Vulnerability Reporting ist aktiviert, das aktive Ruleset `Protect master` hat keine Bypass-Akteure, und das Required-Check-PR-Verhalten wartet auf diesen Pull Request. |
| `git diff --cached --check` | bestanden: kein Whitespace-Fehler in den sechs Task-eigenen Dokumentationsdateien. |
| Zielgerichtete bestehende Bilingual-/Link-Kontrolle | bestanden: Die Pair- und Link-Funktionen des Repository-`check-bilingual-docs.py` melden keinen Fehler für `SECURITY.md`, `SECURITY.de.md` oder dieses Change-Record-Paar. |
| `make check-bilingual-docs` | blockiert: Der Full-Tree-Checker lief, meldete aber nur vorbestehende fehlende Framework-Gitlink-Ziele im isolierten Clone; kein Task-eigener Dokumentationsfehler wurde gemeldet. |
| `make check-doc-links` | durch denselben nicht populierten Framework-Gitlink blockiert; seine gemeldeten Pfade enthalten kein Task-eigenes Dokument. |

## Security-Auswirkung

Dies ist eine Dokumentations- und Governance-Härtung. Sie gibt Meldenden einen
vertraulichen, von GitHub gehosteten Kanal und warnt vor der öffentlichen
Offenlegung von Secrets oder Exploit-Details. Sie ändert weder Connector-
Runtime-Verhalten, Authentifizierung, Autorisierung, Kryptographie,
Abhängigkeitsversionen noch Scanner-Konfiguration.

## Runtime-Evidence

Es ändert sich kein Connector-Runtime-Verhalten. Dieser PR ist die geplante
Kontroll-Evidence für GitHubs `pull_request`-Regel und die sechs exakten
Required Checks; Runtime-Evidence ist nicht anwendbar.

## Bekannte Einschränkungen

Das Repository hat einen direkten Administrator und keinen unabhängigen
Reviewer. Daher wird keine One-Approval-Anforderung ohne automatischen Bypass
eingeschaltet. Der aktuelle SonarCloud-Check ist fehlgeschlagen und kein
Required Check. Automatisierte Security Fixes bleiben aufgrund einer bewussten
Scope-Entscheidung deaktiviert.

## Verbleibende Risiken

Die Richtlinie kann keine Antwortzeit garantieren und nicht jeden Bericht
beheben. Ein Collaborator mit Review-Berechtigung wird weiterhin benötigt,
bevor eine One-Human-Review-Regel ohne Aussperrung aktiviert werden kann.
Fuzzing, erweiterte C/C++-SAST, CII-Badge-Registrierung und die Triage von
Scorecard-Vulnerability-Leads erfordern getrennte evidenzbasierte Arbeit.

## Nicht ausgeführte Prüfungen mit Begründung

Full-Tree-Dokumentations-Checks können in diesem isolierten Clone nicht
bestehen, bis der vorbestehende Framework-Gitlink populiert ist; eine
Framework-Materialisierung gehört nicht zum Scope dieser Aufgabe. Die
Pull-Request-Erstellung, die exakten Required-Check-Läufe, der Review-/Thread-
Status und die SonarCloud-Dispositon sind noch offen und werden erst erfasst,
wenn sie auf dem relevanten Branch oder Pull Request beobachtet wurden.

## Finaler Diff- und Review-Status

Die zielgerichtete Bilingual-/Link-Kontrolle und der staged Scoped-Diff-
Whitespace-Review bestanden. Die Full-Tree-Dokumentations-Checks sind nur
durch den nicht populierten Framework-Gitlink umgebungsbedingt blockiert. Bis
zu diesem Zeitpunkt ist keine `master`-Änderung, kein Merge, kein Bypass und
kein Pull Request erfolgt; der dedizierte Branch ist für seinen ersten Push
bereit.
