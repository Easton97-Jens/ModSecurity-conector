# Change Record: GitHub-Actions-setup-python-v7-Immutable-Lock-Synchronisierung

**Sprache:** [English](CR-20260721-actions-setup-python-v7-lock.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260721-actions-setup-python-v7-lock |
| Datum (UTC) | 2026-07-21 |
| Basis-Revision | 1fa024ca6ec97023ea5b6f7dff5215e43f10b74c |
| Grenze | Nur Parent-GitHub-Actions-CI-Security und Nachvollziehbarkeit; Framework, MRTS, Gitlinks, Connector-Source und historische Change Records bleiben unverändert. |

## Motivation und Problemstellung

Dependabot-PR #67 aktualisierte alle actions/setup-python-Workflow-Referenzen
von v6.3.0 auf v7.0.0, jedoch nicht den zugehörigen geprüften Eintrag in
ci/tooling/security-tools.lock.yml. Der Immutable-Action-Vertrag lehnte den
ansonsten vollständig gepinnten offiziellen SHA korrekt ab. Dieser Ersatz
enthält dieselbe aktuelle Workflow-Aktualisierung und den einen passenden
Lock-Eintrag atomar.

## Akzeptanzkriterien

- Jede Parent-actions/setup-python-Referenz löst auf den vollständigen Commit
  5fda3b95a4ea91299a34e894583c3862153e4b97 mit ihrem v7.0.0-Kommentar auf.
- ci/tooling/security-tools.lock.yml enthält für actions/setup-python denselben
  v7.0.0-Commit.
- Im abgegrenzten Workflow-Diff bleibt keine setup-python-Referenz v6.3.0, kein
  veränderliches Action-Tag, keine unerwartete Action-Quelle,
  Permissions-Änderung, Trigger-Änderung, Matrix-Änderung oder abgeschwächte
  Immutable-Pin-Kontrolle zurück.
- Fokussierte lokale Verträge sowie die resultierenden exakten
  Replacement-PR- und master-Checks bestehen, bevor die geschützte Delivery
  finalisiert wird.

## Implementierungsentscheidung und Begründung

Die offizielle actions/setup-python-Tag-API ordnet v7.0.0 dem Commit
5fda3b95a4ea91299a34e894583c3862153e4b97 zu. Die 25 aktuellen
Workflow-Referenzen in 19 Parent-Workflow-Dateien und der eine passende
Lock-Eintrag werden gemeinsam verschoben. Eine Lock-only-Korrektur wurde
verworfen: Der Vertrag bildet eine Menge aller eingetragenen Lock-SHAs; das
Entfernen des alten SHA bei weiterhin verwendeten Workflows würde daher korrekt
fail-closed scheitern.

Der Ersatz schließt bewusst zwei historische Change Records aus, die auf dem
veralteten Dependabot-Branch verändert wurden. Diese Dokumente enthalten
Delivery-Fakten ohne Bezug zu diesem Action-Update und müssen ihre bereits
beobachtete Historie behalten.

## Geänderte Dateien

- Neunzehn abgegrenzte Parent-Dateien unter .github/workflows/ mit den 25
  actions/setup-python-Referenzen.
- ci/tooling/security-tools.lock.yml
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Befehl oder Evidence | Ergebnis |
| --- | --- |
| Offizieller GitHub-Tag-API-Readback für actions/setup-python v7.0.0 | bestanden: offizieller Commit ist 5fda3b95a4ea91299a34e894583c3862153e4b97. |
| gh run view 29806178964 --repo Easton97-Jens/ModSecurity-conector --log-failed | als Evidence-Abruf bestanden: exakter Dependabot-#67-Head reproduzierte nur den Immutable-Lock-Membership-Fehler. |
| Exakter Source-Head-Check für #67 | bestanden: abgerufener Head war d09a47e19cbe2888dfaca83267513a8ba7722068; seine Workflow-Substitutionen wurden vor der erneuten Anwendung nur ihres aktuellen Parent-Workflow-Scopes geprüft. |
| git diff --check 1fa024ca6ec97023ea5b6f7dff5215e43f10b74c FETCH_HEAD | für den abgerufenen Dependabot-Diff bestanden. |
| Aufbewahrter Preflight-Receipt | bestanden: action-pin-lock-preflight-20260721T072315Z.json, SHA-256 01e11033d3ccbe1c3a9aa0f60e99e28116d35ae232970520997bd1913fc30e33. |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract | bestanden: alle 15 CI-Security-Workflow-Tests sowie die Lock-Record-Validierungen für actionlint, zizmor und gitleaks bestanden. |
| git diff --check im Replacement-Worktree | bestanden. |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs | blocked_environment: der absichtlich nicht ausgefüllte Framework-Gitlink verursachte nur bereits bestehende Missing-Link-Meldungen; kein neuer Change-Record-Schema- oder Paritätsfehler wurde gemeldet. |

Der fokussierte lokale CI-Security-Vertrag und der Scoped-Diff-Check bestanden.
Der vollständige Dokumentationscheck ist nur wegen bereits bestehender
Framework-Links umgebungsblockiert. Exakte Replacement-PR-, Review-,
SonarQube-Cloud-, Protected-Merge- und resultierende-master-Checks stehen noch
aus und werden nicht als bestanden dargestellt.

## Security-Auswirkung

Dies ist eine Änderung der CI-Supply-Chain-Integrität. Jede betroffene Action
bleibt ein offizieller vollständiger unveränderlicher Commit, und der geprüfte
Lock bewahrt die von dem bestehenden CI-Security-Test erzwungene
Allowlist-Beziehung. Bestehende Permissions, Trigger, Action-Quellen, Scanner,
Branch-Protections und Quality Gates bleiben unverändert. Keine
Sicherheitskontrolle wird abgeschwächt und kein Risiko akzeptiert.

## Runtime-Evidence

Es ändert sich kein Connector-Runtime-Verhalten. Der exakte fehlgeschlagene
Dependabot-Run belegt die legitime Block-Kontrolle: Ein ungeprüfter Workflow-SHA
wird auch dann abgelehnt, wenn er unveränderlich ist. Das gepaarte Lock-Update
ist notwendig, damit das offiziell verifizierte Release unter dieser
unveränderten Kontrolle zulässig wird.

## Bekannte Einschränkungen

Der task-eigene Worktree enthält absichtlich einen nicht ausgefüllten
Framework-Gitlink. Vollständige Dokumentationslink-Checks können daher nur
durch bestehende Framework-Links blockiert sein; kein Framework-Inhalt, Gitlink
oder MRTS-Pfad ist Teil dieser Änderung.

## Verbleibende Risiken

Das Pinnen eines verifizierten offiziellen Upstream-Commits beseitigt kein
Upstream-Action-Risiko. Unveränderliches Pinnen, aufbewahrte Tag-Evidence, der
geprüfte Lock, Exact-Head-CI und geschützte Delivery begrenzen dieses
Dependency-Risiko. Es wird kein Risiko akzeptiert.

## Nicht ausgeführte Prüfungen mit Begründung

Exakte Replacement-PR-Checks, Review-/Thread-Status, SonarQube-Cloud-Evidence,
geschützter Squash-Merge und resultierende-master-Workflows haben noch nicht
stattgefunden. Sie bleiben erforderlich; kein Check wird umgangen. Breite
Connector-Runtime-Checks sind für eine Workflow-Pin- und Lock-only-Änderung
nicht anwendbar. Der vollständige bilinguale/Dokumentationscheck ist nur wegen
des absichtlich nicht ausgefüllten Framework-Gitlinks blocked_environment.

## Finaler Diff- und Review-Status

Dies ist ein laufender Traceability-Record. Die abgegrenzte Source-Entscheidung,
offizielle Tag-Zuordnung, der ursprüngliche Fehler, der fokussierte lokale
CI-Security-Vertrag und der Scoped-Diff-Review wurden aufbewahrt. Remote-
Validierung, geschützte Delivery, die Aktualisierung der bestehenden
FND-PARENT-0018-Evidence-Historie und sichere Parent-Workspace-Reconciliation
stehen noch aus.
