# Change Record: GitHub-Actions-checkout-v7.0.1-Immutable-Lock-Synchronisierung

**Sprache:** [English](CR-20260721-actions-checkout-v7-lock.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260721-actions-checkout-v7-lock |
| Datum (UTC) | 2026-07-21 |
| Basis-Revision | 5c26ffb698a892ffe83b7aa1749a456eae10b956 |
| Grenze | Nur Parent-GitHub-Actions-CI-Security und Nachvollziehbarkeit; Framework, MRTS, Gitlinks, Connector-Source und historische Change Records bleiben unverändert. |

## Motivation und Problemstellung

Dependabot-PR #68 aktualisierte alle actions/checkout-Workflow-Referenzen auf
v7.0.1, jedoch nicht den zugehörigen geprüften Eintrag in
ci/tooling/security-tools.lock.yml. Der Immutable-Action-Vertrag lehnte den
ansonsten vollständig gepinnten offiziellen SHA korrekt ab. Dieser Ersatz
enthält die aktuelle Bot-Workflow-Aktualisierung und den einen passenden
Lock-Eintrag atomar.

## Akzeptanzkriterien

- Jede Parent-actions/checkout-Referenz löst auf den vollständigen Commit
  3d3c42e5aac5ba805825da76410c181273ba90b1 mit ihrem v7-Kommentar auf.
- ci/tooling/security-tools.lock.yml enthält für actions/checkout denselben
  v7.0.1-Commit.
- Im abgegrenzten Workflow-Diff bleibt kein älterer checkout-SHA, kein
  veränderliches Action-Tag, keine unerwartete Action-Quelle,
  Permissions-Änderung, Trigger-Änderung, Matrix-Änderung oder abgeschwächte
  Immutable-Pin-Kontrolle zurück.
- Fokussierte lokale Verträge sowie die resultierenden exakten
  Replacement-PR- und master-Checks bestehen, bevor die geschützte Delivery
  finalisiert wird.

## Implementierungsentscheidung und Begründung

Die offizielle actions/checkout-Tag-API ordnet v7.0.1 dem Commit
3d3c42e5aac5ba805825da76410c181273ba90b1 zu. Die 36 aktuellen
Workflow-Referenzen in 23 Parent-Workflow-Dateien und der eine passende
Lock-Eintrag werden gemeinsam verschoben. Eine Lock-only-Korrektur wurde
verworfen: Der Vertrag bildet eine Menge aller eingetragenen Lock-SHAs; das
Entfernen des alten SHA bei weiterhin verwendeten Workflows würde daher korrekt
fail-closed scheitern.

Nach dem sicheren Merge von #67 aktualisierte Dependabot #68 auf diesen
resultierenden Master. Der aktuelle Bot-Head ist
d7ceb21aed63e7ca7257a5f247825bb02c826b30; sein aktueller Diff enthält nur die
beabsichtigten checkout-Pin-Substitutionen. Der originale Bot-PR bleibt
aufbewahrt; sein nicht modifizierbarer Branch wird für diese Korrektur nicht
verwendet.

## Geänderte Dateien

- Dreiundzwanzig abgegrenzte Parent-Dateien unter .github/workflows/ mit den 36
  actions/checkout-Referenzen.
- ci/tooling/security-tools.lock.yml
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Befehl oder Evidence | Ergebnis |
| --- | --- |
| Offizieller GitHub-Tag-API-Readback für actions/checkout v7.0.1 | bestanden: offizieller Commit ist 3d3c42e5aac5ba805825da76410c181273ba90b1. |
| gh run view 29811489361 --repo Easton97-Jens/ModSecurity-conector --log-failed | als Evidence-Abruf bestanden: exakter Dependabot-#68-Head reproduzierte nur den Immutable-Lock-Membership-Fehler. |
| Exakter Source-Head-Check für #68 | bestanden: abgerufener aktueller Head war d7ceb21aed63e7ca7257a5f247825bb02c826b30; sein Diff enthält nur 36 checkout-Substitutionen in 23 Workflow-Dateien. |
| git diff --check 5c26ffb698a892ffe83b7aa1749a456eae10b956 FETCH_HEAD | für den abgerufenen aktuellen Dependabot-Diff bestanden. |
| Aufbewahrter Preflight-Receipt | bestanden: pr68-current-head-lock-preflight-20260721T074704Z.json, SHA-256 52e4b85a142f2d850cbdb4b6ba552a1538c7f386296ce1728bb9f89e78338f5a. |
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
