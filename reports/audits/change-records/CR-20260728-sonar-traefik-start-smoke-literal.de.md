# Change Record: Parent-Traefik-Start-Smoke-Diagnostikliteral-Bereinigung für SonarQube Cloud S1192

**Sprache:** [English](CR-20260728-sonar-traefik-start-smoke-literal.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-traefik-start-smoke-literal |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Grenze | Ausschließlich Parent-Traefik-Start-Smoke-Runner und sein direkter statischer Wiring-Checker sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework, MRTS, beide Gitlinks, Workflow, Scanner-Policy und generierte Reports bleiben unverändert. |
| Finding-Verknüpfung | SonarQube-Cloud-Item AZ9Mwiwj-bUaKQ_zSGA2, Regel shelldre:S1192, meldet das Diagnostikliteral 1,160p viermal in connectors/traefik/scripts/start-smoke.sh. Dieser lokale Kandidat schließt den externen Befund vor einer frischen Exact-Head-Analyse nicht selbst. |

## Motivation und Problemstellung

Der prozessorientierte Traefik-Start-Smoke verwendete das unveränderliche
Diagnostik-sed-Programm 1,160p in vier getrennten Fehlerzweigen. Das
wiederholte Literal ist der abgegrenzte SonarQube-Cloud-Maintainability-Befund;
vier unabhängig änderbare Kopien würden eine künftige Änderung des
Diagnostikbereichs leichter inkonsistent machen.

Der Runner verwaltet Pfade, Subprozesse, Liveness-Prüfungen und Cleanup. Die
Änderung darf deshalb ausschließlich das feste Diagnostikprogramm
zentralisieren und muss jeden Branch-Prädikatswert, STDERR-Operand,
Fehlermeldung, Exit-Status, Trap und jedes Cleanup-Verhalten unverändert
lassen.

## Akzeptanzkriterien

- connectors/traefik/scripts/start-smoke.sh enthält genau eine
  bedingungslose, nicht exportierte Deklaration
  TRAEFIK_DIAGNOSTIC_SED_RANGE='1,160p' nach dem Cleanup-Trap und vor der
  ersten Diagnostikverwendung.
- Die vier bestehenden Fehlerdiagnostiken verwenden die quotierte Deklaration
  mit ihren unveränderten quotierten Operanden: "$CONFIG_STDERR",
  "$SERVICE_STDERR" und zweimal "$TRAEFIK_STDERR".
- Der direkte statische Wiring-Checker verwirft eine exportierte, duplizierte,
  alte oder falsch angeordnete Range und fixiert die betroffenen
  Fehlerzweigkontrollen.
- Shell-Syntax, der fokussierte Start-Wiring-Check und das scoped
  Whitespace-Checking bestehen; die bekannte ShellCheck-Baseline wird nicht
  als sauberes Ergebnis dargestellt.
- Es werden weder Traefik-Host-Runtime noch Commit, Push, Pull Request,
  Hosted-Analyse, Ready-for-review-Übergang, Merge, Master-Update,
  Framework-/MRTS-Aktion oder Scanner-Policy-Änderung behauptet.

## Implementierungsentscheidung und Begründung

Die gewählte Deklaration ist eine bedingungslose Shell-Zuweisung und kein
Defaulting oder übernommener Umgebungswert. Sie wird absichtlich nicht
exportiert, damit ein Aufrufer das sed-Programm nicht wählen kann und
Child-Process-Umgebungen unverändert bleiben. Jeder der vier bestehenden
sed -n-Aufrufe übergibt jetzt denselben festen Wert und seine bestehende
STDERR-Datei als getrennte quotierte Argumente.

Der direkte Source-Vertrag prüft eine Deklaration, vier direkte Verwendungen,
das Fehlen des alten Literalaufrufs, die unveränderten Operanden pro Zweig und
die vorhandenen Lifecycle-Guards. Er ändert weder den separaten
Template-Rewrite-sed -e-Aufruf noch Start-Root-Validierung,
Loopback-Prüfungen, Prozessstarts, Wait-/Exit-Reihenfolge, Traps oder Cleanup.

## Erhaltene Diagnostikaufrufe

| Fehlerzweig | Erhaltener Diagnostikbefehl |
| --- | --- |
| Config-Check | sed -n "$TRAEFIK_DIAGNOSTIC_SED_RANGE" "$CONFIG_STDERR" >&2 |
| Service-Liveness | sed -n "$TRAEFIK_DIAGNOSTIC_SED_RANGE" "$SERVICE_STDERR" >&2 |
| Traefik-Liveness | sed -n "$TRAEFIK_DIAGNOSTIC_SED_RANGE" "$TRAEFIK_STDERR" >&2 |
| Nichtleeres Traefik-STDERR | sed -n "$TRAEFIK_DIAGNOSTIC_SED_RANGE" "$TRAEFIK_STDERR" >&2 |

## Geänderte Dateien

- connectors/traefik/scripts/start-smoke.sh
- ci/checks/connectors/all/check-remaining-connectors-start-wiring.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| sh -n connectors/traefik/scripts/start-smoke.sh | bestanden; reine Syntaxvalidierung ohne Start eines Hostprozesses. |
| make check-remaining-connectors-start-wiring | bestanden; der fokussierte statische Vertrag meldete remaining connectors start wiring: ok. |
| Scoped git diff --check für Runner und direkten statischen Checker | bestanden. |
| ShellCheck des Ziel-Runners | nicht als sauberer Check bestanden: Es wurden nur drei unveränderte SC1007-Diagnosen auf den Zeilen 4–6 gemeldet. Dieser Record behandelt diese Baseline nicht als bestandenes Ergebnis. |
| Scoped Prüfung der englisch/deutschen Change-Record- und Index-Struktur, technischen Literale, wechselseitigen Links und abschließenden Whitespaces | bestanden. |

## Security-Auswirkung

Dies ist eine Code-Quality-Remediation und kein validiertes Security-Finding.
Die fokussierte Shell-/Prozess-/Pfad-Review klassifizierte die
Fixed-Literal-Bedingung als already_safe: Kein Umgebungs-, Request-,
Response-, Log-, Pfad-, Prozess- oder Konfigurationswert kontrolliert das
sed-Programm. Die bedingungslose lokale Zuweisung überschreibt jeden
übernommenen Wert, bleibt nicht exportiert und die vier STDERR-Operanden
bleiben quotiert.

Die Remediation erhält set -eu, Start-Root- und Loopback-Guards, quotierte
Diagnostikpfade, kill -0- und wait-Reihenfolge, trap cleanup EXIT HUP INT TERM,
die ursprünglichen Fehlerzweige und ihre Exits. Kein Security-Control wird
abgeschwächt.

## Runtime-Evidence

Es wurde keine reale Traefik-, Connector-, Common/libmodsecurity- oder
Host-Runtime ausgeführt. Die bestandenen Syntax- und direkten statischen
Wiring-Checks sind ausschließlich Source-Contract-Evidence; sie belegen keine
Host-Runtime-Capability.

## Nicht ausgeführte Prüfungen mit Begründung

- Der reale Traefik-Start-Smoke ist für diese reine Literaländerung bewusst
  nicht Teil des Ziels und bleibt not_run.
- Repository-weite Bilingual-Dokumentations- und Linkchecks werden in diesem
  Agent-Scope nicht ausgeführt. Der Kandidaten-Worktree enthält einen leeren
  Parent-gebundenen Framework-Gitlink; root führt diese Checks deshalb in einem
  wegwerfbaren Exact-Revision-Overlay aus, statt diese lokale Voraussetzung als
  Produktfehler zu behandeln.
- Exact-PR-Head-GitHub-Checks und SonarQube-Cloud-Analyse benötigen den
  normalen task-eigenen Draft-PR-Delivery-Zyklus und existieren noch nicht.

## Bekannte Einschränkungen

Der direkte Checker ist absichtlich statisch. Er belegt Literal-Ownership,
quotierte Diagnostikoperanden und erhaltene Branch-Controls, startet aber
weder einen Service noch validiert er eine vollständige Traefik-Deployment.
ShellCheck behält die oben genannten drei vorbestehenden SC1007-Diagnosen.

## Verbleibende Risiken

Dieser Kandidat beweist kein Verhalten unter einer realen Host-, Plugin- oder
Common/libmodsecurity-Installation. Bestehende weitergehende Trust-Annahmen
zur Prozessumgebung und zu Diagnostik-Log-Inhalten liegen außerhalb dieser
reinen SonarQube-Cloud-Literalremediation und wurden durch sie nicht erweitert.

## Finaler Diff- und Review-Status

Dieser Record wird vor Staging, Commit, Push, Pull-Request-Erstellung und
Hosted-Analyse geschrieben. Die aufgezeichnete lokale Source-Validierung und
fokussierte Sicherheitsreview sind innerhalb ihrer angegebenen Scopes positiv.
Eine globale Duplikatzeilenreduktion oder externe Finding-Closure wird erst
nach einer frischen SonarQube-Cloud-Analyse des finalen exakten PR-Heads
behauptet.
