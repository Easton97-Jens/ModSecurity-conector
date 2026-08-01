# Change Record: Vollständige Parent-Traefik-SonarQube-Cloud-Remediation

**Sprache:** [English](CR-20260801-sonar-traefik-complete-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | \`CR-20260801-sonar-traefik-complete-remediation\` |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | \`c3319575ae86d9810da8b5428590336d60cd3daf\` |
| Tracking | \`FND-SONAR-0016\` — aktuelles \`connectors/traefik/\`-Inventar. |
| Grenze | Nur Parent \`connectors/traefik/\` und direkte Parent-Tests. |

## Motivation und Problemstellung

Das aktuelle Traefik-Verzeichnisinventar enthält acht Security- und zwei
Maintainability-Befunde. Die Python-Smoke-Runner verarbeiten aus der Umgebung
abgeleitete Pfade und Executable-Namen, bevor sie Runtime-Artefakte erzeugen
oder lokale Prozesse starten. Der Native-Runner bündelte außerdem Setup,
Host-Ausführung, Beobachtungen, Outcome-Validierung und Cleanup in einer
komplexen Funktion. Die Go-Middleware stellte ein Single-Method-Interface unter
einem generischen Namen bereit.

## Implementierungsentscheidung und Begründung

Der ForwardAuth-Runner führt ein validiertes, unveränderliches lokales
Executable-Objekt bis zur Kommandoerzeugung. Er weist Steuerzeichen vor dem
Prozessstart zurück, behält erzeugte Runtime-Artefakte unter festen Namen in
validierten Verzeichnissen und akzeptiert keinen Shell-Kommando-String. Die
Native-Runtime-Root behält ihre Owner- und Ancestor-Prüfungen; gemeinsame
temporäre Roots werden über diese echten Rechteprüfungen statt über eine
fragile Literal-Deny-List zurückgewiesen.

Der Native-Lifecycle ist in Input-Sammlung, Staging, privaten UDS- und
Loopback-Setup, Request-Ausführung, Live-Beobachtung, Outcome-Finalisierung,
Result-Schreiben und Cleanup geteilt. Dies bewahrt den bestehenden Protokoll-
und Nicht-Promotion-Vertrag und hält einzelne Verantwortlichkeiten innerhalb
wartbarer Komplexität. Das Go-Single-Method-Interface heißt
\`TransactionOpener\`; \`Engine\` bleibt ein quellkompatibler Alias.

Keine SonarQube-Cloud-Regel, Exclusion, Suppression, \`NOSONAR\`, Quality Gate,
Workflow, Framework, MRTS, Gitlink oder \`master\`-Status ändert sich.

## Akzeptanzkriterien

Alle zehn aufbewahrten Issue-Keys besitzen eine konkrete Source-Disposition;
fehlerhafte, entweichende, symlinked, cross-user-replaceable oder
steuerzeichenhaltige Command-Inputs scheitern vor einem Filesystem- oder
Process-Sink; legitime private Roots und reguläre lokale Executables bleiben
gültig; Native-Host-Lifecycle-Output und Safe-Cleanup-Verträge bleiben intakt;
und der exakte PR-Head muss null New Issues und null New-Code-Duplikation ohne
Scanner-Control-Änderung besitzen.

## Geänderte Dateien

Die Änderung beschränkt sich auf Traefik-Python-Smoke-Runner,
Native-Middleware-Go-Quellen, ihre direkten Parent-Python-Tests sowie dieses
englisch/deutsche Change-Record-Paar und die Indizes. Keine andere
Repository-Grenze ändert sich.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Gewähltes Parent-Python 3.14: \`python -m py_compile connectors/traefik/scripts/runtime_native_smoke.py connectors/traefik/scripts/runtime_smoke.py\` | bestanden. |
| Gewähltes Parent-Python 3.14: \`python -m unittest -v tests.test_traefik_runtime_smoke_security tests.test_traefik_native_local_plugin\` | bestanden: 26 Tests. |
| Task-eigener Go-1.26.5-Cache: \`go test -mod=readonly ./...\` in \`connectors/traefik/native_middleware\` | bestanden. |
| \`gofmt -d\` für die geänderten Go-Dateien | bestanden: keine Ausgabe. |
| \`git diff --check\` | vor dem Final Review bestanden; erneute Ausführung vor der Auslieferung erforderlich. |
| Vollständiger Native-Host-Lifecycle und gelinkter C17-Engine-Build | nicht ausgeführt: Diese isolierte Sandbox besitzt kein task-provisioniertes Traefik-Binary und keine libmodsecurity-Entwicklungsheader/-Library. Eine globale Installation wird nicht als Ersatz verwendet. |

## Security-Auswirkung

Die Executable- und Artefaktänderungen verengen bestehende Path- und
Process-Trust-Boundaries: Kommandoargumente dürfen keine Steuerzeichen
enthalten, feste Output-Namen bleiben unter validierten Roots und gemeinsame
temporäre Verzeichnisse werden weiter anhand tatsächlicher Ownership und
Permissions zurückgewiesen. Regression-Controls decken legitime private Roots
und Executables sowie Symlink-, Public-Root-, Cross-User-Replacement- und
Steuerzeichen-Negative ab. Der Lifecycle-Refactor bewahrt Socket-Identity-
Checks, Process-Cleanup, Loopback-only-Binding, Host-Outcome-Causality und
Capability-Nicht-Promotion. Er beansprucht keine Hosted-Security-Analyse oder
ein vollständiges Native-Runtime-Ergebnis.

## Verbleibende Risiken und Verifikationsstatus

Die Source- und fokussierten Controls sind lokal vollständig. Vollständige
Native-Host-Runtime-Evidence ist aus dem genannten Voraussetzungengrund nicht
verfügbar. Der angeforderte Draft-PR benötigt weiterhin SHA-gebundene Hosted
Actions-, CodeQL- und SonarQube-Cloud-Verifikation; dieser Record beansprucht
weder PR-Erstellung, Review, Merge noch eine \`master\`-Änderung.

## Runtime-Evidence

Die fokussierten Source-Controls belegen die Executable-, Artefakt-, Root-,
Socket- und Lifecycle-Helper-Verträge, beanspruchen aber keine vollständige
Native-Host-Runtime.

## Bekannte Einschränkungen

Der isolierten Task-Umgebung fehlen die task-provisionierten Traefik- und
libmodsecurity-Inputs für den vollständigen Native-Host-Lifecycle und den
gelinkten C17-Build.

## Nicht ausgeführte Prüfungen mit Begründung

Der vollständige Native-Host-Lifecycle und der gelinkte C17-Engine-Build
benötigen ein task-provisioniertes Traefik-Binary sowie libmodsecurity-
Entwicklungsheader und -Library, die in der isolierten Task-Umgebung fehlen.
Hosted-Exact-Head-Verifikation steht bis zum Draft-PR aus.

## Finaler Diff- und Review-Status

Der finale Security-sensitive Diff-Review und der Delivery-Status werden erst
nach Abschluss ihrer jeweiligen Befehle erfasst. Dieser Record beansprucht
bewusst keinen Commit, Push, PR-Nummer, Hosted-Check, SonarQube-Cloud-Analyse
oder eine \`master\`-Integration.
