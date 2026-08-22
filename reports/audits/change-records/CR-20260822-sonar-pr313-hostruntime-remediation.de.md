# Change Record CR-20260822: PR-#313-Hostruntime-Sonar-Remediation

**Sprache:** [English](CR-20260822-sonar-pr313-hostruntime-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260822-sonar-pr313-hostruntime-remediation` |
| Datum (UTC) | `2026-08-22` |
| Basis-Revision | `9b26e55059783ea97a304c94bb62dc0c0f2b0554` |
| Scope | Nur Parent-Repository: Hostruntime-Manifest-Projektion, fokussierte Regressionstests und gekoppelte Nachvollziehbarkeit. Keine Framework-, MRTS-, Gitlink-, Sonar-Suppression-, Exclusion- oder Quality-Gate-Konfigurationsänderung. |

## Motivation und Problemstellung

Der bereits gemergte Parent-PR [#313](https://github.com/Easton97-Jens/ModSecurity-conector/pull/313)
hat eine unveränderliche historische SonarCloud-Analyse. Seine öffentliche
Exact-PR-Issue-Abfrage meldete vier offene New-Code-Code-Smells in
`ci/runtime/lifecycle/write-hostruntime-record.py`: drei
`python:S1192`-Duplicate-Literal-Instanzen und eine
`python:S3776`-Cognitive-Complexity-Instanz. Alle vier sind direkt dem
Source-Diff von PR #313 zugeordnet.

Diese Nachfolgeänderung behebt die Implementierung, statt die Findings zu
unterdrücken. Das sachliche Null-Ziel ist die eigene Exact-Head-SonarCloud-
Abfrage des Nachfolge-PRs; kein Follow-up kann die historische #313-Analyse
umschreiben.

## Akzeptanzkriterien

- Alle vier direkt zugeordneten Code-Smell-Instanzen ohne `NOSONAR`,
  Exclusions, Suppressions, Testlöschung oder Quality-Gate-Änderungen beheben.
- Fail-Closed-Artifact-Map-Validierung vor jeder Projektionsmutation erhalten.
- Runtime-Root-Containment, No-Symlink-/Regular-File-Checks, kanonische
  Self-Artifact-Pfade, Reserved-Path-Rejection, Artifact-State-Validierung
  und Checksum-Verifikation erhalten.
- Fokussierte Regressionsabdeckung für die refaktorierten
  Validierungszweige ergänzen.
- Eine Exact-Head-SonarCloud-Issue-Abfrage des Nachfolge-PRs mit `total: 0`
  für offene oder bestätigte New-Code-Issues erhalten.
- Framework, MRTS, Gitlink und NGINX-spezifische Konfiguration nicht ändern.

## Implementierungsentscheidung und Begründung

- Die wiederholten Literale `manifest.json`, `hostruntime record` und
  `hostruntime summary` als benannte Konstanten zentralisiert.
- Den bisherigen Validator mit hoher Komplexität in kleine Helper für
  Map-/Name-Validierung, Self-Artifacts, nicht produzierte Artifacts,
  produzierte Artifacts, Checksums und Reserved Paths geteilt. Die
  Caller-Reihenfolge bleibt unverändert: Result-Artifacts werden vor
  Manifest-Artifacts validiert.
- `preflight_manifest_projection()` und `project_manifest()` als die beiden
  Caller beibehalten, sodass Validierung vor Output-Erzeugung und unmittelbar
  vor Result-/Manifest-Projektion erfolgt.
- Regressionen für nichtkanonische Self-Pfade, Reserved Lifecycle Paths in
  beiden Artifact-Maps und ungültige Checksum-/State-Werte produzierter
  Artifacts ergänzt.

## Security-Auswirkung

Obwohl die Sonar-Findings Maintainability-Code-Smells sind, schützt die
betroffene Funktion eine sicherheitsrelevante Path- und Manifest-Grenze. Ein
fokussiertes Review des Successor-Diffs fand keine Abschwächung der
Containment-, Symlink-, Checksum-, State- oder Pre-Mutation-Controls. Der
Refaktor bleibt bei fehlerhaften Artifact-Deklarationen fail closed.

## Geänderte Dateien

- `ci/runtime/lifecycle/write-hostruntime-record.py`
- `tests/test_hostruntime_record.py`
- `reports/audits/change-records/CR-20260822-sonar-pr313-hostruntime-remediation.md`
- `reports/audits/change-records/CR-20260822-sonar-pr313-hostruntime-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Check | Tatsächliches Ergebnis |
| --- | --- |
| `python -B -m unittest tests/test_hostruntime_record.py` | Bestanden: 23 Tests, einschließlich der neuen Pfad-/State-/Checksum-Regressionen. |
| `python -B -m unittest tests/test_hostruntime_workflow_evidence_contract tests/test_collect_hostruntime_preflight_evidence` | Bestanden: 9 Workflow-/Evidence-Contract- und Fail-Closed-Collector-Tests. |
| `python -B -m unittest tests/test_hostruntime_preflight tests/test_ci_security_workflows` | Bestanden: 55 Preflight- und CI-Security-Contract-Tests. |
| `git diff --check` | Für Source- und Test-Refaktor bestanden; auf dem final gestagten Delivery-Diff erneut auszuführen. |
| Fokussiertes Source-/Security-Review | Bestanden: Keine semantische oder sicherheitsrelevante Regression in den Artifact-Validation-Invarianten gefunden. |

## Runtime-Evidence

Die fokussierte Test-Suite ruft den Projektionsbefehl gegen temporäre
Runtime-Root-Fixtures auf. Ihre negativen Controls beobachten den Fail-Closed-
Exit-Status des Befehls, bevor eine verbotene Artifact-Deklaration projiziert
werden kann.

## Nicht ausgeführte Prüfungen mit Begründung

- Die vollständige Repository-Suite wurde nicht ausgeführt: Die Änderung ist
  auf den Hostruntime-Writer und seine dedizierte Test-Suite begrenzt.
- Ruff und ein lokaler Sonar-Scanner sind nicht installiert oder konfiguriert.
  Es wurde kein Tool installiert und kein Gate umgangen; die gehostete
  SonarCloud-Analyse des Nachfolge-PRs ist die autoritative Messung.
- `make check-bilingual-docs` wurde durch bereits bestehende fehlende Links in
  den nicht materialisierten Framework-Gitlink des externen Worktrees
  blockiert. Der Fehler listet ausschließlich diese unabhängigen
  Framework-Pfade, nicht einen der neuen Change Records.
- Keine Host-Runtime-Matrix wurde gestartet, weil diese Änderung weder eine
  Connector-Konfiguration noch ein Runtime-Protokoll verändert; relevantes
  Verhalten ist die Fail-Closed-Artifact-Validierung des Writers.

## Bekannte Einschränkungen

Die historische Issue-Anzahl von PR #313 bleibt nach seinem Merge sichtbar und
unveränderlich. Dieser Nachfolge-Record und -PR können nur eine Null-Anzahl
für den Successor-Head und später für dessen resultierenden `master`-Stand
belegen.

## Verbleibende Risiken

Lokale Evidence belegt Source und fokussierte Verhaltensabdeckung, aber die
vier Issue-Instanzen sind erst verifiziert, wenn SonarCloud den exakten
Successor-PR-Head analysiert hat. Dieser Record autorisiert keinen Merge des
Nachfolge-PRs.

## Finaler Diff- und Review-Status

Die Parent-only-Code- und Teständerung ist bereit für finale Dokumentations-
und Git-Prüfung und danach für einen Nachfolge-Draft-PR. Sie autorisiert keinen
Merge, keine Framework-/MRTS-Änderung, kein Gitlink-Update und keine
Sonar-Konfigurationsänderung.
