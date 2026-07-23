# Change Record: Framework-Gitlink-Update auf 935cf14

**Sprache:** [English](CR-20260723-framework-gitlink-935cf14.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-framework-gitlink-935cf14 |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | 91c933e19bb3c87d767c4dad9eb8a1b160d42051 |
| Grenze | Parent-Framework-Gitlink, dieses englische/deutsche Change-Record-Paar und beide Parent-Change-Record-Indizes. Framework-Source, Framework-Delivery, MRTS, Parent-Connector-Source, Workflow-Berechtigungen, Action-Pins, Dependency-Locks, Resolver-Verhalten und Publisher-Verhalten bleiben unverändert. |
| Delivery-Status | Parent-PR #94 ist der ausdrücklich ausgewählte offene PR. Sein ursprünglicher automatisierter Commit 8db42f177dcc28a7cb9fb78c93e46b564aa16410 hebt den Gitlink an; dieser Record ist ein task-eigener Compliance-Folgeumfang auf diesem PR. Der finale exakte PR-Head, Reviews, Checks, das SonarQube-Cloud-Ergebnis, der Merge, der Resulting-Master-SHA und Resulting-Master-Workflows werden in beobachteter PR-/Task-Evidence festgehalten, statt vor ihrem Eintreten behauptet zu werden. |

## Motivation und Problemstellung

Der Parent-Workflow Update submodules löste die offizielle Framework-master-
Revision 935cf14c676a24672be5c336e92cd13457cc35c8 auf, während der Parent
784977615acfc55567e37b863309abc4a38ac877 festhielt. Der Hosted-Run
29996299306 schloss Resolver, read-only-Candidate-Validator und engen
PR-Publisher erfolgreich ab und eröffnete PR #94 mit dem resultierenden
ein-Datei-Parent-Gitlink-Diff.

Der Parent-Gitlink ist eine getrennte Delivery-Grenze. Seine Integration muss
Parent-seitige Scope-, Security-, Validierungs- und Limitierungsfakten
festhalten, auch wenn die Framework-Revision bereits im Framework-Repository
gemergt wurde. Der ursprüngliche automatisierte PR hatte keinen Parent-Change-
Record und keine bilinguale PR-Beschreibung/Record-Verlinkung; dieser
Folgeumfang liefert daher die erforderliche Parent-Traceability, ohne
Framework-Inhalt oder Delivery-State zu verändern.

## Akzeptanzkriterien

- Der Parent-Gitlink ändert sich ausschließlich von
  784977615acfc55567e37b863309abc4a38ac877 auf
  935cf14c676a24672be5c336e92cd13457cc35c8.
- Dieses englische/deutsche Change-Record-Paar und beide Indizes beschreiben
  gleichwertige, beobachtete Parent-Delivery-Fakten.
- PR #94 erhält vor der finalen Verifikation gleichwertige englische/deutsche
  Beschreibungsabschnitte und diesen Change-Record-Link.
- Die vorhandene Trennung von read-only-Validierung/Publisher, Workflow-
  Berechtigungen, Action-Pins, Dependency-Locks, Framework-Source und MRTS
  bleibt unverändert.
- Ein frischer Exact-Head-PR-Check-, Review-/Conversation-, SonarQube-Cloud-,
  geschützter Squash-Merge- und Resulting-Master-Workflow-Zyklus wird
  beobachtet, bevor das Parent-Update als vollständig berichtet wird.

## Implementierungsentscheidung und Begründung

Der Parent hält den exakten Framework-Commit als Gitlink fest, statt
Framework-Dateien zu kopieren oder zu verändern.
935cf14c676a24672be5c336e92cd13457cc35c8 ist der beobachtete Framework-
origin/master-Merge-Commit. Seine Framework-eigenen Source-Änderungen und
Framework-Change-Records bleiben Framework-Evidence; dieser Parent-Record
beschreibt ausschließlich Parent-Pointer und Parent-Delivery-Pflichten.

Der Compliance-Folgeumfang fügt keine ausführbare Source-, Workflow-, Action-,
Package- oder Berechtigungsänderung hinzu. Er korrigiert die Parent-
Traceability-Lücke und macht die PR-Beschreibung bilingual; anschließend wird
der Exact-Head-Verifikationszyklus bewusst neu gestartet. Kein historisches
grünes Ergebnis wird als Evidence für den geänderten PR-Head behandelt.

## Geänderte Dateien

- modules/ModSecurity-test-Framework: Parent-Gitlink von
  784977615acfc55567e37b863309abc4a38ac877 auf
  935cf14c676a24672be5c336e92cd13457cc35c8.
- reports/audits/change-records/CR-20260723-framework-gitlink-935cf14.md und
  .de.md: dieses Parent-Delivery-Record-Paar.
- reports/audits/change-records/README.md und .de.md: passende Index-Einträge.

Keine Framework-Source, kein Framework-Gitlink innerhalb des Frameworks,
kein MRTS-Inhalt, keine Parent-Connector-Source, kein Test, Workflow,
Berechtigung, Action-Pin, Dependency oder generierter Runtime-Report wird
geändert.

## Ausgeführte Befehle

- Bestanden: rtk proxy git diff --no-ext-diff
  91c933e19bb3c87d767c4dad9eb8a1b160d42051
  8db42f177dcc28a7cb9fb78c93e46b564aa16410 --
  modules/ModSecurity-test-Framework. Der ursprüngliche PR-Diff enthält
  ausschließlich das erwartete Gitlink-Update.
- Bestanden: rtk proxy gh run view 29996299306 --repo
  Easton97-Jens/ModSecurity-conector. Resolver, read-only-Validator
  einschließlich make quick-check und PR-Publisher von Update submodules
  endeten erfolgreich für Parent 91c933e19bb3c87d767c4dad9eb8a1b160d42051.
- Bestanden: rtk proxy git -C modules/ModSecurity-test-Framework branch
  --remotes --contains 935cf14c676a24672be5c336e92cd13457cc35c8. Die
  ausgewählte Revision ist im beobachteten Framework origin/master enthalten.
- Bestanden: rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp
  RUNNER_TEMP=<task-run>/tmp make check-bilingual-docs. Der bilinguale
  Dokumentationschecker meldete bilingual docs ok, nachdem das PR-gepinnte
  Framework-Submodul nicht rekursiv im disponiblen Worktree initialisiert war.
- Bestanden: rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp
  RUNNER_TEMP=<task-run>/tmp make check-doc-links. Parent-Repository-Pfad-
  Referenzen und Framework-Dokumentationslinks bestanden beide.
- Bestanden: rtk proxy git diff --cached --check. Für den final gestagten
  Folge-Diff wurde kein Whitespace-Fehler gemeldet.
- Bestanden: rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp
  RUNNER_TEMP=<task-run>/tmp make check-ci-security-contract. Alle 16
  Workflow-Security-Contract-Tests bestanden, einschließlich der Trennung von
  read-only-Update-submodules-Validator und engem Publisher.
- Bestanden: Der fokussierte Security-Review des exakten Gitlink-/Dokumentations-
  Kandidaten fand keine validierte High- oder Critical-Severity-Schwachstelle.
  Er stellt klar, dass read-only die GitHub-Token-/API-Berechtigungsgrenze des
  Validators beschreibt, nicht die Behauptung, sein ephemerer Runner-Workspace
  könne keine temporären Dateien schreiben.
- In diesem Snapshot ausstehend: alle frischen Exact-Head-Hosted-Controls für
  den Compliance-Folgeumfang. Sie werden erst nach der Ausführung gegen seinen
  resultierenden Head erfasst.

## Security-Auswirkung

Dies ist ein Supply-Chain-Grenzupdate: Der Parent hebt einen gepinnten Gitlink
auf einen exakten vollständigen Framework-SHA an, den der Resolver vor der
Veröffentlichung erneut gegen den offiziellen Framework-master validierte.
Candidate-Code wurde im contents: read-Validator geprüft; der enge Publisher
lief erst nach diesem Erfolg. Dieser Record lockert diese Trennung nicht und
führt keinen neuen Download-, Berechtigungs-, Secret-, Pfad-, Archiv-, Action-
oder Runtime-Data-Handling-Pfad ein.

Read-only bezeichnet in diesem Record die GitHub-Token-/API-
Berechtigungsgrenze des Validators. Es wird nicht behauptet, dass make
quick-check im ephemeren Runner-Workspace keine temporären Dateien erstellen
kann.

Die Framework-Revision enthält breite Framework-eigene CI-/Tooling-Änderungen,
doch dieser Parent-Record beansprucht keine unverifizierte Delivery oder
Behavior dafür. Frische Parent-Protection-Branch-Checks und SonarQube-Cloud-
Analyse bleiben für den finalen PR-Head erforderlich.

## Runtime-Evidence

Es wurde keine Runtime-Evidence erhoben oder beansprucht. Der isolierte
read-only-Candidate-Validator und Parent-Dokumentationsprüfungen sind
CI-/statische Validierung und keine Connector-, HTTP-, HTTP/2-, HTTP/3- oder
Production-Runtime-Evidence.

## Bekannte Einschränkungen

Der Parent reproduziert nicht unabhängig jede Framework-interne Validierung von
935cf14c676a24672be5c336e92cd13457cc35c8; Framework-Source und Delivery
bleiben getrennte Ownership. Diese Parent-Integration ist auf den exakten
aufgezeichneten Gitlink, seine isolierte Candidate-Validierung und seine
frische Parent-Protected-Branch-Evidence begrenzt.

## Verbleibende Risiken

Bis der task-eigene Folge-Head alle Protected-Branch-Checks, SonarQube Cloud,
Review-/Conversation-Inspektion und Resulting-Master-Workflows bestanden hat,
ist PR #94 nicht merge-berechtigt. Es wird kein Branch-Protection-Bypass,
keine CI-Schwächung, kein Framework-Merge, keine MRTS-Aktion und keine
Risikoakzeptanz verwendet.

## Nicht ausgeführte Prüfungen mit Begründung

- Es wird keine Parent-Connector-/Runtime-Matrix oder vollständiger lokaler
  make quick-check für diesen Dokumentations-/Gitlink-Folgeumfang behauptet.
  Der Candidate-spezifische make quick-check lief bereits im isolierten
  read-only-Hosted-Validator; finale Berechtigung erfordert weiterhin die
  neuen Exact-Head-Parent-Workflows.
- Kein Framework-Source-Test, Framework-Branch/PR/Merge, Framework-Checkout-
  Wechsel, keine MRTS-Inspektion über die bestehende read-only-Grenze hinaus
  und kein MRTS-Test lief. Nichts davon ist zum Hinzufügen des Parent-
  Traceability-Records erforderlich, und MRTS ist strikt read-only.

## Finaler Diff- und Review-Status

Der Pre-Delivery-Review begrenzt diesen PR auf den exakten Parent-Gitlink und
den erforderlichen Parent-Traceability-/Dokumentations-Folgeumfang. Whitespace-,
bilinguale Dokumentations- und Documentation-Link-Validierung bestanden im
isolierten PR-Worktree. Der lokale CI-Security-Contract bestand alle 16 Tests,
und der fokussierte Security-Review fand keine validierte High-/Critical-
Schwachstelle. Der vorherige automatisierte Head hatte ein bestandenes
SonarQube-Cloud-Quality-Gate mit null neuen Issues und null Security-Hotspots;
dieses Ergebnis wird bewusst nicht als Evidence für den Folge-Head behandelt.
Aktueller Security-Diff-, Review-, Exact-Head-CI-, SonarQube-Cloud-, Merge- und
Resulting-Master-Status steht aus und muss vor Abschluss mit beobachteten
Ergebnissen abgeglichen werden.
