# CI-Sicherheitswerkzeuge

**Sprache:** [English](ci-security-tooling.md) | Deutsch

## Geltungsbereich

Dieses Dokument beschreibt CI-Kontrollen des Repositorys. Es belegt keine
Runtime-Sicherheit, Connector-Korrektheit oder Produktions-Sicherheitszertifizierung.

## Unveränderliche Action- und Tool-Provenienz

Jede Remote-Action-Referenz in `.github/workflows/` ist auf einen
unveränderlichen Commit-SHA festgelegt; der stabile Release-Tag steht als
Kommentar dabei. Revalidierungsdatum, offizieller Upstream, Release-Version,
unveränderlicher Commit, Binary-Release-Asset, SHA-256-Digest, Lizenz,
Zweck und minimale Berechtigungen stehen in `ci/tooling/security-tools.lock.yml`.

`ci/tools/fetch_security_tool.py` akzeptiert nur das festgehaltene offizielle
Release-Asset, prüft den SHA-256-Digest vor dem Entpacken, weist absolute und
Traversal-Archivpfade zurück und extrahiert genau eine deklarierte Executable.
Das Tool installiert keine Abhängigkeiten und verändert keine Repository-Dateien.

## Workflow-Linting

`ci-security-workflow-lint.yml` führt checksum-verifiziertes `actionlint` aus
und übergibt den `ShellCheck`-Pfad des Runners, wenn er verfügbar ist. Zudem
läuft checksum-verifiziertes `zizmor` offline gegen alle Workflow-Dateien. Eine
absichtlich unsichere Fixture muss fehlschlagen und eine sichere Fixture muss
bestehen; beide Fixtures sind keine ausführbare Produktkonfiguration.

## Secret- und Dependency-Scanning

Für einen Pull Request berechnet Gitleaks `git merge-base` aus den exakten
Base- und Head-SHAs, scannt nur diesen Commit-Bereich und aktiviert Redaction.
Zeitgesteuertes und manuell ausgelöstes Full-History-Gitleaks-Scanning ist
advisory, bis historische Findings triagiert sind; es darf andere Arbeit nicht
stillschweigend blockieren.

OSV scannt den exakten Pull-Request-Base-SHA und den exakten
Pull-Request-Head-SHA, vergleicht die Resultate und meldet neu eingeführte
Findings. Es führt weder automatische Dependency-Updates noch automatische
Dependency-Remediation aus. Der zeitgesteuerte Scan ist ebenfalls advisory,
damit ein repositoryweites historisches Dependency-Finding triagiert werden
kann, bevor es zur blockierenden Regel wird.

## CodeQL- und Scorecard-Grenzen

CodeQL analysiert Actions, beide Go-Module mit festem Go `1.24.0` und einen
begrenzten C/C++-Scope, der auf `make check-common-helpers-c17` beschränkt ist.
Das C/C++-Ergebnis beansprucht keine vollständige Connector-Abdeckung; eine
Erweiterung erfordert reproduzierbare Builds für den ausgewählten Connector-Scope.

Scorecard nutzt Read-only-Berechtigungen für Same-Repository-Pull-Requests und
checkt den exakten Pull-Request-Head aus. Fork-Pull-Requests analysiert dieser
Job absichtlich nicht, weil ihr Head kein vertrauenswürdiger
Same-Repository-Ref ist. Die Default-Branch-Scorecard lädt SARIF nur mit der
separaten Berechtigung `security-events: write` hoch.

## Validierung und Einschränkungen

Führen Sie `make check-ci-security-contract` für fokussierte statische Verträge
und die Validierung der Lock-Einträge aus. GitHub Actions-, CodeQL-, OSV-,
Gitleaks- und Scorecard-Ergebnisse sind nur Evidenz für Workflow, Event,
exakten SHA und Berechtigungen. Sie erzeugen keine automatischen Fixes,
ändern keinen Branch-Schutz, umgehen keine Reviews und ersetzen keine
Connector-/Runtime-Tests.
