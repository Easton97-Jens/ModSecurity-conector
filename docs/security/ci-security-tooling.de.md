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

`ci/tools/fetch_security_tool.py` startet ausschließlich mit der exakt
festgehaltenen URL `https://github.com/.../releases/download/...`. Es folgt
höchstens zwei HTTPS-Weiterleitungen: die erste nur von diesem GitHub-Origin
zur expliziten offiziellen Release-Asset-Host-Allowlist, die optionale zweite
nur innerhalb derselben Allowlist (`release-assets.githubusercontent.com` und
der Legacy-Host `github-releases.githubusercontent.com`). Fremde oder
unsichere Weiterleitungen bzw. finale Hosts werden abgewiesen. Vor dem
Entpacken prüft es den festgehaltenen SHA-256-Digest, weist absolute und Traversal-Archivpfade
zurück und extrahiert genau eine deklarierte Executable. Das Tool installiert
keine Abhängigkeiten und verändert keine Repository-Dateien.

Der Workflow-Key-Verifier parst den YAML-Node-Tree jedes Workflows und verlangt
für jeden dekodierten `uses`-Key die kanonische unquotierte Blockschreibweise
`uses:`. Damit können YAML-Quoting, Escapes, Tags, explizite Keys und
Flow-Maps keine Action-Referenz verstecken. Sein Parser-Wheel ist mit einer
exakten SHA-256 in `ci/tooling/python-ci-requirements.lock` festgelegt und
wird mit Hash-Prüfung vom festen PyPI-Index installiert; es wird nicht
implizit vom Hosted Runner übernommen.

Bevor der privilegierte Parent-Tooling-Publisher einen Draft-PR erstellen oder
aktualisieren darf, baut der Read-only-Validator den Kandidaten in einem
disposable vertrauenswürdigen Tree nach und lädt/extrahiert jedes
Kandidat-Sicherheitswerkzeug checksum-verifiziert. Nach SHA-256- und
Extraktionsprüfung führt er ausschließlich begrenzte Version-Smoketests mit
30 Sekunden Timeout aus (`actionlint --version`, `zizmor --version` und
`gitleaks version`). Er verwendet diese heruntergeladenen Binaries weder zur
Analyse von Repository-Inhalten noch zum Veröffentlichen von Änderungen.

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

CodeQL analysiert Actions, beide Go-Module mit dem exakt gepinnten Go-`1.26`-
Patch aus ihrem `go.mod`, der auch im CodeQL-Setup gespiegelt wird, sowie einen
begrenzten C/C++-Scope, der auf `make check-common-helpers-c17` beschränkt ist.
Der Patch-only-Updater akzeptiert nur offizielle stabile Releases dieser
`1.26`-Serie und wechselt nicht schwebend auf eine neue Minor-Version. Sein
maschinenlesbares Ergebnis unterscheidet `current`, `patch_update_available`
und `newer_minor_available`; es bricht mit `blocked_metadata`,
`blocked_network`, `no_stable_release`, `invalid_current_version` oder
`candidate_failed` fail-closed ab. Das C/C++-Ergebnis beansprucht keine
vollständige Connector-Abdeckung; eine Erweiterung erfordert reproduzierbare
Builds für den ausgewählten Connector-Scope.

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
