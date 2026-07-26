# Change Record: OpenSSF-Scorecard-Action-v2.4.4-Immutable-Lock-Synchronisierung

**Sprache:** [English](CR-20260726-scorecard-action-v2-4-4-lock.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260726-scorecard-action-v2-4-4-lock |
| Datum (UTC) | 2026-07-26 |
| Basis-Revision | 53f0937b377e2e2b2e33e58c87d4034f78587608 |
| Grenze | Nur Parent-CI-Workflow, geprüfter Action-Lock und dieses englisch/deutsche Change-Record-Paar samt Index. Framework, MRTS, Gitlinks, Connector-Source, Workflow-Berechtigungen, Trigger und bestehende Findings bleiben unverändert. |
| Finding-Verknüpfung | FND-PARENT-0028 bleibt offen und wird durch dieses äußere Git-Action-Pin-Update nicht behoben. |

## Motivation und Problemstellung

Dependabot-PR #121 aktualisierte beide `ossf/scorecard-action`-Verwendungen
auf den offiziellen v2.4.4-Commit, ließ aber
`ci/tooling/security-tools.lock.yml` auf v2.4.3. Der Immutable-Action-Vertrag
des Repositorys schlug korrekt fail-closed fehl, weil die neue Workflow-SHA
nicht im geprüften Action-Lock stand. Der ursprüngliche Dependabot-Branch ist
nicht maintainer-modifizierbar; deshalb trägt dieser Parent-eigene
Ersatzkandidat den gewünschten Pin und den passenden Lock-Eintrag atomar.

## Akzeptanzkriterien

- Beide Scorecard-Workflow-Referenzen verwenden den offiziellen vollständigen
  v2.4.4-Commit `2d1146689b8cda280b9bc96326124645441f03bc` mit passendem
  Versionskommentar.
- `ci/tooling/security-tools.lock.yml` erfasst v2.4.4 und dieselbe Commit-SHA.
- Der bestehende Immutable-Action-Test akzeptiert die geprüfte SHA, ohne
  Membership-Control, Berechtigungen, Trigger, Action-Quellen oder Job-Scope
  zu lockern.
- Die fokussierten lokalen Verträge des Kandidaten und spätere gehostete
  Exact-Head-Checks bestehen vor jeder geschützten Integration.
- Es wird keine Framework-, MRTS-, Gitlink-, Connector-Runtime- oder
  Sicherheitsfinding-Schließung behauptet oder durchgeführt.

## Implementierungsentscheidung und Begründung

Das offizielle signierte annotierte Tag `v2.4.4` von
`ossf/scorecard-action` löst auf den verifizierten Commit
`2d1146689b8cda280b9bc96326124645441f03bc` auf; die offiziellen Release- und
Commit-Metadaten kennzeichnen ihn als v2.4.4-Release. Identische Workflow-SHA
und geprüfter Lock-Eintrag bewahren den bestehenden fail-closed-Vertrag. Ein
Lock-only-Merge wurde verworfen, weil er das verlangte Action-Upgrade nicht
trägt; eine Änderung des Dependabot-Branches wurde verworfen, weil er nicht
maintainer-modifizierbar ist.

## Geänderte Dateien

- `.github/workflows/ci-security-scorecard.yml`: die zwei bestehenden
  Scorecard-Action-Pins wechseln von v2.4.3 auf v2.4.4.
- `ci/tooling/security-tools.lock.yml`: geprüfte Scorecard-Action-Version,
  SHA und Prüfdatum entsprechen dem Workflow.
- `reports/audits/change-records/README.md` und `README.de.md`.
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Befehl oder Evidence | Ergebnis |
| --- | --- |
| Offizieller GitHub-Tag-, Tag-Objekt-, Release- und Commit-API-Readback für `ossf/scorecard-action` v2.4.4 | bestanden: signiertes Tag `v2.4.4` löst auf verifizierten Commit `2d1146689b8cda280b9bc96326124645441f03bc` auf. |
| Exakte PR-#121-Prüfung bei Head `1dd0077b6297416222ad8d130dc6997956d74757` | erwartungsgemäß fehlgeschlagen: der verpflichtende `actionlint`-Job meldete den Immutable-Lock-Membership-Fehler. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_ci_security_workflows` auf der unkorrigierten PR-#121-Quelle | erwartungsgemäß fehlgeschlagen: die neue Scorecard-SHA fehlte im Lock. |
| `git diff --check` für den Ersatzkandidaten | bestanden. |
| `make PYTHON=python3 check-ci-security-contract` | bestanden: alle 18 CI-Security-Workflow-Tests und alle drei Security-Tool-Lock-Validatoren bestanden unter Python 3.14.4. |
| Checksum-verifiziertes actionlint über alle Workflows und Permission-Fixtures | bestanden. |
| Checksum-verifiziertes `zizmor --offline .github/workflows` | bestanden: keine Findings; 80 bestehende Suppressions gemeldet. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs` | bestanden: 11 Tests. |
| Vollständiges `check-bilingual-docs.py` | blocked_environment: exakt 20 bestehende fehlende Ziele unterhalb des bewusst nicht populierten Framework-Gitlinks; keine Diagnose nannte einen geänderten Change Record oder Index. |

Gehostete Exact-Head-Validierung steht noch aus und wird nicht als bestanden
dargestellt.

## Security-Auswirkung

Dies ist eine CI-Supply-Chain-Integritätskorrektur. Die externe Action bleibt
auf eine offizielle vollständige Commit-SHA gepinnt, und der geprüfte Lock
erhält die erzwungene Beziehung zwischen Workflow-Action-SHAs und ihrer
Herkunft. Keine Berechtigung, Secret-Exposition, kein Trigger,
Upload-Verhalten, keine Scanner-Konfiguration, kein Quality Gate und kein
Branch-Schutz werden geschwächt. FND-PARENT-0028 dokumentiert die separate
geerbte mutable verschachtelte Container-Image-Grenze; diese Änderung schließt
oder verschlechtert das Finding nicht.

## Runtime-Evidence

Nicht anwendbar. Diese Änderung betrifft nur Parent-CI-Konfiguration und
Lock-Provenienz; sie startet keinen Connector, Service, HTTP-Listener,
Protokolltest, Framework-Test oder MRTS-Test.

## Bekannte Einschränkungen

Der isolierte Parent-Worktree initialisiert oder inspiziert bewusst weder den
Framework-Gitlink noch MRTS. Vollständige Dokumentationsprüfungen können
bereits vorhandene Links unterhalb dieser nicht populierten Grenze melden.
Gehostete Ergebnisse müssen nach Veröffentlichung für den Exact Head des
Ersatz-PR erneut gelesen werden.

## Verbleibende Risiken

Ein unveränderlicher äußerer Git-Action-Commit bindet nicht den Docker-Image-
Tag, den die Upstream-Scorecard-Action-Metadaten auflösen. Diese geerbte
Hardening-Lücke mittlerer Priorität ist bereits als FND-PARENT-0028 erfasst und
benötigt eine separat autorisierte Remediation; hier wird kein Risiko akzeptiert.

## Nicht ausgeführte Prüfungen mit Begründung

- Exact-Head-Checks des Ersatz-PR, SonarQube Cloud, CodeQL/OSV/Secret-Scanning,
  Review-, Thread- und Protected-Merge-Evidence benötigen einen veröffentlichten
  Kandidaten und eine frische Exact-Head-Prüfrunde.
- Connector-Runtime-, Protokoll-, Framework- und MRTS-Tests sind für diesen
  Parent-Workflow-Pin-und-Lock-only-Scope nicht anwendbar.
- Nested-Image-Hardening wird nicht versucht, weil FND-PARENT-0028 eine
  separat autorisierte Remediation-Entscheidung erfordert.

## Finaler Diff- und Review-Status

Dieser Ersatzkandidat hat fokussierte lokale Workflow-, Lock-, actionlint-,
zizmor-, Whitespace- und zweisprachige Record-Validierung bestanden. Er
benötigt weiterhin unabhängiges Review und frische gehostete Exact-Head-
Evidence, bevor ein geschützter Merge möglich ist. Der ursprüngliche
Dependabot-PR #121 bleibt offen und unverändert.
