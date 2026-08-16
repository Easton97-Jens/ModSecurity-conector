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

## Eingeschränkter Workflow-/Tool-Updater

`.github/workflows/update-workflow-tools.yml` behält `resolver`, `validator`,
`publisher` und `outcome` als getrennte Jobs. Die ersten beiden Jobs sind
read-only; der Publisher erhält erst nach Candidate- und Proposed-Tree-
Validierung einen kurzlebigen, auf das Repository begrenzten GitHub-App-Token.
Er erstellt ausschließlich Draft-Pull-Requests und erst nach expliziten Pfad-,
Symlink-, Staging-Scope- und Candidate-SHA-256-Prüfungen.

Die eingecheckte `ci/tooling/security-tools.lock.yml` bleibt die einzige
Lockdatei und Source of Truth. Ihre On-Disk-`pinned_actions`-Einträge verwenden
`commit_sha` und `upstream`; Tool-Einträge verwenden `release_commit`, `url`
und `upstream`. Der Updater adaptiert diese Felder nur im Speicher, sodass
bestehende Connector-Consumer kein paralleles Lock-Schema benötigen.

| Action | Version | Unveränderlicher Commit |
| --- | --- | --- |
| `actions/checkout` | `v7.0.1` | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| `actions/create-github-app-token` | `v3.2.0` | `bcd2ba49218906704ab6c1aa796996da409d3eb1` |
| `actions/download-artifact` | `v8.0.1` | `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c` |
| `actions/github-script` | `v9.0.0` | `3a2844b7e9c422d3c10d287c895573f7108da1b3` |
| `actions/setup-go` | `v7.0.0` | `b7ad1dad31e06c5925ef5d2fc7ad053ef454303e` |
| `actions/setup-python` | `v7.0.0` | `5fda3b95a4ea91299a34e894583c3862153e4b97` |
| `actions/upload-artifact` | `v7.0.1` | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` |
| `github/codeql-action` | `v4.37.6` | `5595ccaf912efad79be6eef63a5619ff05969be3` |
| `google/osv-scanner-action` | `v2.5.0` | `8deb546fdb875b9996d27d4950be7312dac076a1` |
| `ossf/scorecard-action` | `v2.4.4` | `2d1146689b8cda280b9bc96326124645441f03bc` |

Für die gehostete Ausführung konfigurieren Sie die Repository-Variable
`WORKFLOW_UPDATER_APP_CLIENT_ID` und das Repository-Secret
`WORKFLOW_UPDATER_APP_PRIVATE_KEY`. Keiner der beiden Werte gehört in das
Repository. Die GitHub App muss auf dieses Repository begrenzt sein und darf
nur `Contents: write`, `Pull requests: write` und `Workflows: write` erhalten.

## Eingeschränkter Python-3.14-Patch-Updater

`.github/workflows/update-python-version.yml` hat genau vier Jobs:
`resolve-python-patch`, `validate-python-patch`, `publish-python-update` und
`report-python-update-outcome`. Er wird ausschließlich durch den Montags-
Zeitplan `17 6 * * 1` oder `workflow_dispatch` ausgelöst, serialisiert pro
Repository über
`modsecurity-conector-python-version-maintenance-${{ github.repository }}`
ohne einen laufenden Wartungsversuch abzubrechen und lässt Arbeit nur für die
kanonische Nicht-Fork-Ref `master` von `Easton97-Jens/ModSecurity-conector` zu.

Der Resolver verwendet den exakten vertrauenswürdigen Event-SHA, die kanonische
`.python-version` und `scripts/update-python-version.py --check --json`, um
die typisierten Outputs `status`, `current_version`, `latest_version` und
`update_available` auszugeben. Der Validator installiert und prüft den
Candidate-Patch unabhängig, löst ihn mit `--expected-version` erneut auf,
nutzt hash-gesperrte CI-Abhängigkeiten und führt vor der Veröffentlichung die
Python-/Versions- und CI-Sicherheitsverträge aus. Beide Jobs besitzen nur
`contents: read`.

Das normale `GITHUB_TOKEN` bleibt im Publisher bei `contents: read`. Nur dieser
Job liest die App-Konfiguration, erstellt das vorhandene SHA-gepinnte
GitHub-App-Token und begrenzt dieses Token auf `Contents: write` und
`Pull requests: write`. Er fordert nie Schreibrechte für `Workflows`,
`Actions` oder `Issues`; das weitergehende oben genannte `Workflows: write`
gehört nur zum getrennten Workflow-/Tool-Updater. Der Publisher besitzt keinen
Schreibpfad über `github.token`.

Der Publisher übergibt den Step-Output `changed` vor der Shell-Ausführung über
eine benannte Umgebungsvariable und akzeptiert nur den literalen Wert `true`.
Er interpoliert keine GitHub-Actions-Ausdrücke direkt in einen Shell-Befehl;
dadurch bleibt die Output-Prüfung fehlgeschlossen und vermeidet
Workflow-Template-Injection.

Vor einem Schreibzugriff verlangt der Publisher entweder keinen Wartungs-Branch
und keinen passenden PR oder genau einen Same-Repository-Draft-PR mit festem
Titel und Marker `<!-- modsecurity-conector-python-314-updater -->`, Basis
`master` und deaktiviertem automatischen Merge. Er prüft bei einem bestehenden
Branch dessen historischen Scope, baut danach von aktuellem vertrauenswürdigem
`origin/master` neu auf, ändert nur `.python-version`, staged nur diese Datei
und verwendet beim sicheren Ersetzen des verifizierten Wartungs-Branch nur die
exakte Form
`--force-with-lease=refs/heads/$UPDATE_BRANCH:$EXPECTED_REMOTE_TIP`. Ein
unbedingter Force-Push, ein Default-Branch-Update, Merge oder Auto-Merge ist
nicht erlaubt.

Der resultierende Same-Repository-Draft-PR dokumentiert vorherige/vorgeschlagene
Version, Python.org-Metadaten-URL, Validierungs-Run-URL, Framework-Referenz-SHA
und die Pflicht zu manueller Prüfung/manuellem Merge auf Englisch und Deutsch.
Der `report-python-update-outcome`-Job mit leeren Berechtigungen läuft immer
und weist inkonsistente Resolver-, Validator- oder Publisher-Zustände zurück;
bei einem aktuellen Resultat berichtet er, dass kein Branch, Commit oder PR
geändert wurde.

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

CodeQL analysiert Actions, beide Go-Module über den exakten Root-
<code>.go-version</code>-Selector (aktuell Go <code>1.26.5</code>) und einen
begrenzten C/C++-Scope. Dieser Scope führt
<code>make check-common-helpers-c17</code> sowie einen begrenzten
15-Sekunden-libFuzzer-Lauf für den Common-HTTP-Header-Parser mit C17,
AddressSanitizer und UndefinedBehaviorSanitizer aus. Der zentrale Selector ist
ein CI-Toolchain-Vertrag; die <code>go.mod</code> jedes Moduls behält seine
Go-Sprachbaseline. Der Updater schlägt nur einen stabilen Patch derselben
Minor-Serie erst nach read-only-Candidate-Validierung in einem Draft PR vor und
kann keine Modul- oder Dependency-Dateien ändern. Das C/C++-Ergebnis beansprucht
keine vollständige Connector-Abdeckung; eine Erweiterung erfordert
reproduzierbare Builds für den ausgewählten Connector-Scope.

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
