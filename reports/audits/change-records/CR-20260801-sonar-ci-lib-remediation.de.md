# Change Record: SonarQube-Cloud-Behebung der Parent-CI-Bibliothek

**Sprache:** [English](CR-20260801-sonar-ci-lib-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-sonar-ci-lib-remediation` |
| Datum (UTC) | `2026-08-01` |
| Basis-Revision | `6b4aca18d390363764b96d85cd31969b9bb114a1` |
| Grenze | Ausschließlich Parent `ci/lib/generated_report_utils.py`, `ci/lib/runtime_path_utils.py`, ein direkter Parent-Regressionstest, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Framework- und MRTS-Quelle, Gitlinks, `.github/`, SonarQube-Cloud-Regeln, Exclusions, Suppressions, Quality Gates und `master` bleiben unverändert. |
| SonarQube-Cloud-Verknüpfung | Das aktuelle `ci/lib`-Inventar enthielt 19 offene Einträge: `python:S5443` in `generated_report_utils.py` Zeilen 61–73 und `runtime_path_utils.py` Zeilen 26, 31–32; `python:S3776` in `generated_report_utils.py` Zeilen 49, 1098, 1538 und `runtime_path_utils.py` Zeile 235; sowie `python:S1192` in `generated_report_utils.py` Zeilen 1051, 1071, 1136 und 1420. |

## Motivation und Problemstellung

Die Parent-CI-Bibliothek enthielt wiederholte Pfad-, Suffix- und
Referenzpräfixliterale sowie zwei große Entscheidungspfade für Report-
Provenance und Runtime-Root-Auswahl. SonarQube Cloud meldete 19 offene
Maintainability- und Security-Rule-Einträge in diesem engen Verzeichnis. Die
Runtime-Policy nutzt den festen temporären Fallback bewusst nur zur Ableitung
eines privaten, geprüften Child-Verzeichnisses; sie darf nicht allein für ein
statisches Analyseergebnis abgeschwächt werden.

## Implementierungsentscheidung und Begründung

Der Report-Helper besitzt portable Pfad-, Suffix- und Source-Reference-
Konstanten jetzt zentral. Kleine Helper bewahren die bisherige Reihenfolge der
Pfadredaktion und trennen Report-Metadaten, Provenance, Stale-Status,
Regular-File- und Directory-Input-Entscheidungen. Der Runtime-Helper verwendet
einen Resolver für Environment-oder-Default-Pfade und eine Darstellung für den
festen Policy-Parent, während Allowlist, private Leaf-, Owner-, Sticky-Parent-
und No-Follow-Prüfungen unverändert erhalten bleiben.

Der ergänzte Regressionstest deckt sowohl Verified-Run- als auch allgemeine
temporäre Pfaddarstellung ab. Er prüft ausschließlich die Darstellung;
Runtime-Writes laufen weiter durch die bestehenden descriptor-basierten
Schutzmechanismen.

## Akzeptanzkriterien

- Bestehende Report-Input-Status- und Framework-Provenance-Ergebnisse bleiben
  unverändert, einschließlich stale, blocked, missing und fail-closed.
- Verifizierte Runtime-Pfade lehnen weiterhin breite, systembeschreibbare,
  unsichere und symlinked Roots ab und akzeptieren den engen verifizierten
  externen Child-Root.
- Temporäre Pfade werden portabel dargestellt, ohne dass der Report-
  Präsentations-Helper auf das Dateisystem zugreift.
- Ein zukünftiger exakter PR-Head muss null neue SonarQube-Cloud-Issues und
  null neue Duplikatzeilen ohne Regeländerung, Exclusion, Suppression oder
  Abschwächung einer Sicherheitskontrolle zeigen.

## Geänderte Dateien

- `ci/lib/generated_report_utils.py`
- `ci/lib/runtime_path_utils.py`
- `tests/test_generated_report_evidence_integrity.py`
- `reports/audits/change-records/CR-20260801-sonar-ci-lib-remediation.md`
- `reports/audits/change-records/CR-20260801-sonar-ci-lib-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Python `py_compile` für beide geänderten Parent-CI-Bibliotheksmodule | bestanden. |
| Fokussierte Parent-`unittest`-Auswahl | bestanden: 98 Tests in 14,445 Sekunden. Sie enthält alle Generated-Report-Evidence-Integrity-Tests, alle Runtime-Path-Security-Tests und die ausgewählten Runtime-Path-Policy-Controls. |
| `check-generated-report-layout`, aufgerufen durch die fokussierte Generated-Report-Test-Suite | bestanden. |
| `tests.test_bilingual_docs` | bestanden: 22 Tests in 0,280 Sekunden. |
| `make check-bilingual-docs` | ausschließlich durch den absichtlich nicht materialisierten Framework-Checkout blockiert; nach der task-eigenen Überschriftenkorrektur betreffen alle verbleibenden Diagnosen fehlende Framework-Link-Ziele. |
| Finales `git diff --check` vor den Dokumentationsupdates | bestanden. Es wird vor der Auslieferung für den vollständigen Task-Diff erneut ausgeführt. |
| Fokussierter Codex-Security-Scan aller acht `ci/lib`-Module | bestanden ohne neu entdecktes reportable Finding. Er prüfte Dateisystem-Writes, descriptor-relative Artifact-Accesses, Report-Output-Pfade, Subprocess-Konstruktion und Temporary-Root-Handling. |

## Security-Auswirkung

Der Runtime-Path-Code ist sicherheitsrelevant, weil CI-Pfade und temporäre
Roots durch Environment-Werte oder angreifersteuerbaren Dateisystemzustand
beeinflusst sein können. Der Refactor ändert weder die feste Fallback-Auswahl
noch die Ablehnung breiter/System-Pfade noch die descriptor-basierten
`O_NOFOLLOW`-, Owner-, Mode- und Sticky-Parent-Schutzmaßnahmen. Er fügt keine
Kommando-Konstruktion, keinen Netzwerkzugriff, kein Credential-Handling,
keine Permission-Änderung und keinen neuen beschreibbaren Ort hinzu.

Dieses Change Record unterdrückt, akzeptiert oder schließt kein Security-
Finding.

## Runtime-Evidence

Die fokussierten Tests üben die Policy- und Artifact-Safety-Kontrollen aus,
ohne einen Connector zu provisionieren oder Framework/MRTS-Inhalte zu ändern.
Sie beanspruchen keine vollständige Connector-Runtime-Matrix.

## Nicht ausgeführte Prüfungen mit Begründung

- Das vollständige Modul `tests.test_runtime_path_policy` kann im isolierten
  Task-Worktree nicht abschließen, weil seine subprocess-basierte Framework-
  Kontrolle einen absichtlich nicht materialisierten Framework-Checkout
  benötigt. Die ausgewählten Parent-Policy-Controls und die vollständige
  Runtime-Path-Security-Suite bestanden; keine Framework-Quelle wurde als
  Workaround initialisiert oder geändert.
- `make check-bilingual-docs` wurde ausgeführt, aber sein repositoryweiter
  Local-Link-Scan kann in diesem Task-Worktree wegen des absichtlich nicht
  materialisierten Framework-Checkouts nicht abschließen. Die direkte
  Bilingual-Test-Suite bestand, und der Checker meldet keinen verbleibenden
  task-eigenen Record-Fehler.
- Es wurde keine lokale SonarQube-Cloud-Analyse ausgeführt, weil diese
  Task-Umgebung keinen konfigurierten Scanner-Credential besitzt. Der exakte
  gehostete PR-Head muss das autoritative SonarQube-Cloud-Ergebnis liefern.
- Keine Connector-Matrix, kein Download, keine Package-Installation, keine
  Framework-/MRTS-Aktion, keine Gitlink-Änderung, keine `.github/`-Aktion und
  keine `master`-Integration wurden ausgeführt, weil der angeforderte Scope
  ausschließlich die Parent-`ci/lib`-Behebung umfasst.

## Bekannte Einschränkungen

Das aktuelle SonarQube-Cloud-Inventar ist ein zeitpunktbezogenes
Server-Ergebnis. Seine Schließung und das Ausbleiben neuer Befunde bleiben
offen, bis die gehostete Analyse auf dem exakten veröffentlichten PR-Head
läuft.

## Verbleibende Risiken

Das verbleibende Risiko liegt in einer Regression der Report-Status-Reihenfolge
oder der Runtime-Root-Auswahl. Die fokussierte Regression-Suite deckt die
bestehenden Sicherheitskontrollen und die Darstellungsreihenfolge ab; die
gehostete SonarQube-Cloud-Analyse bleibt die finale Static-Analysis-Evidence.

## Finaler Diff- und Review-Status

Die Aufgabe ist noch nicht ausgeliefert. Ein task-owned Branch wird erst nach
bestandenen finalen Full-Diff-, Dokumentations- und Security-Contract-Checks
committet und als Draft-PR veröffentlicht. Ein Merge nach `master` ist weder
autorisiert noch beansprucht.
