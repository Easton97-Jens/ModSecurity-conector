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

Die Workflow-Wartung hat genau einen Besitzer: Dependabot verwaltet hier keine
`github-actions`. Der Updater löst jeden Lock-Eintrag als Einheit auf,
aktualisiert jeden passenden Action-Suffix (einschließlich aller
`github/codeql-action`-Komponenten) und die zentrale Lockdatei in einem
Kandidaten, validiert den vollständigen Proposed Tree und erstellt höchstens
einen passenden Parent-Draft-Pull-Request. Alle Checkout-Schritte verwenden
`submodules: false`; Framework-/MRTS-Quellen und Gitlinks liegen außerhalb des
Scopes dieses Workflows.

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
| `google/osv-scanner-action` | `v2.5.1` | `6e4298ebc4db23e847df9b2e2de2939d6f066c67` |
| `ossf/scorecard-action` | `v2.4.4` | `2d1146689b8cda280b9bc96326124645441f03bc` |

Für die gehostete Ausführung konfigurieren Sie die Repository-Variable
`WORKFLOW_UPDATER_APP_CLIENT_ID` und das Repository-Secret
`WORKFLOW_UPDATER_APP_PRIVATE_KEY`. Keiner der beiden Werte gehört in das
Repository. Die GitHub App muss auf dieses Repository begrenzt sein und darf
nur `Contents: write`, `Pull requests: write` und `Workflows: write` erhalten.

Der normale CI-Sicherheitsvertrag prüft, dass jeder eingecheckte Workflow durch
die explizite Publisher-Allowlist und die Staging-Liste abgedeckt ist. Ein neuer
Workflow erfordert die Aktualisierung beider Listen. Die Proposed-Tree-Prüfung
kopiert die vollständigen registrierten Vertragseingaben einschließlich ihrer
Offline-Test-Fixtures; diese read-only-Eingaben erweitern die erlaubten
Änderungen des Publishers nicht.

## Zentrale gewöhnliche Revisions- und Toolchain-Pins

`ci/tooling/project-versions.lock.json` ist die einzige gepflegte Parent-
Konfiguration für gewöhnliche Framework-/MRTS-Revisionen und Python-/Go-
Toolchains. Ihre generierten Setup-Action-Ansichten bleiben `.python-version`
und `.go-version`. Gewöhnliche Revisionsconsumer prüfen den exakten Parent-
Lock-Blob, unabhängig aufgezeichnete Gitlinks und materialisierte Repository-
HEADs bei deaktivierten Git-Replacements. Komponenten bleiben in der
`ci/lib/common.sh` des ausgewählten Frameworks definiert; Action-/Sicherheits-
Tool-Pins behalten ihre getrennte Lockdatei. Geschützte Broker-Tupel bleiben
unabhängig geprüft. [Projekt-Versionspins](../reference/version-pins.de.md)
erläutern Zuständigkeit, Synchronisierung und Fehlersemantik.

## Framework-Submodul-Wartung und Artefaktbereinigung

`update-submodules.yml` unterscheidet offene Wartungsbranches von Branches, die
nach einem geprüften Merge übrig bleiben. Ein offener Branch muss weiterhin
genau einen vertragskonformen Updater-Commit enthalten. Ein verbleibender
gemergter Branch darf geprüfte menschliche Reparatur-Commits enthalten, wenn
ein Same-Repository-PR mit exakt diesem Head, App-Autor, festem Titel und Marker
gemergt wurde und sein Merge-Commit vom aktuellen `origin/master` erreichbar
ist. Nicht gemergte, fremde, mehrdeutige oder veraltete Identitäten bleiben
Fehler. Die Veröffentlichung baut weiterhin vom aktuellen `master` neu auf,
validiert den Kandidaten, prüft Branch-Races und erstellt einen Draft PR ohne
automatischen Merge.

Die zeitgesteuerte Action in `cleanup-artifacts.yml` wiederholt vorübergehende
GitHub-API-Fehler bis zu dreimal mit dem begrenzten Backoff der gepinnten Action.
Dauerhafte Berechtigungsfehler und nach den Wiederholungen verbleibende
Löschfehler lassen den Job weiterhin scheitern; Aufbewahrungsregeln und
Job-Berechtigungen bleiben gleich.

## Zulassung von Runtime-Pfaden

Envoy- und Traefik-Kompatibilitäts-Stages erzeugen Invocation-eigene Unix-Sockets
über `ci/runtime/lifecycle/with-private-sockets.py` in einem kurzen privaten
Verzeichnis. Evidence- und Build-Artefakte behalten ihre an Revisionen gebundenen
Pfade. Die CLI wählt ausschließlich feste Envoy-/Traefik-Lifecycle-Einstiegspunkte
und deren geprüfte Stage-Argumente. Der Shell-Aufrufer übergibt den aus
`RUNNER_TEMP`/`TMPDIR` ausgewählten Socket-Elternpfad ausdrücklich; der Wrapper
prüft Eigentümer, sichere Vorfahren, den Modus `0700` des privaten Verzeichnisses
und die Unix-Socket-Pfadgrenze von 108 Bytes vor dem Start der ausgewählten Stage. Beliebige Befehlsausführung
ist nicht über die CLI verfügbar. Der Wrapper prüft den temporären Elternpfad, leitet Beendigungssignale
weiter, weist verbliebene laufende Prozesse zurück und prüft das Prozessende,
bevor er Socket-Dateien löscht. Das Verzeichnis bleibt erhalten, wenn sicheres
Prozessende oder sichere Bereinigung nicht feststeht. Direkte Harness-Aufrufe mit kurzen Pfaden
behalten ihr privates Fallback-Verzeichnis. Der Traefik-Runner lässt den exakten
vorbereiteten Pfad `BUILD_ROOT/traefik-connector/bin/traefik` mit denselben
Eigentümer-, Modus-, Vorfahren- und Symlink-Prüfungen wie bei gecachten Binaries
zu; andere Executables im Build-Baum bleiben unzulässig.

## Zulassung des Traefik-Response-Observer-Loaders

Der feste eingecheckte `modsecurityResponseObserver` verwendet Linux
`SO_PEERCRED`, um den Response-Companion-Peer zu authentifizieren. Yaegi muss
für diese Prüfung den eingeschränkten `syscall`-Import bereitstellen. Die
`.traefik.yml` des Observers deklariert `useUnsafe: true`; die
Betreiberkonfiguration aktiviert dies ausschließlich für dieses lokale Plugin
über `experimental.localPlugins.modsecurityResponseObserver.settings.useUnsafe`.
Beide Deklarationen sind erforderlich. Das statische Beispiel und beide
Smoke-Einstiegspunkte aktivieren außerdem `experimental.abortOnPluginFailure`,
damit ein Observer-Ladefehler den Start abbricht, statt seine Route unverfügbar
zu lassen. Passende ältere Build-Constraints
`// +build linux` / `// +build !linux` ergänzen die modernen
`//go:build`-Constraints, damit Yaegi unter Linux die Linux-Credential-
Implementierung auswählt und anderswo den fehlgeschlossenen Stub erhält.

Diese Aktivierung gilt nur für die feste Repository-eigene Observer-Quelle,
die ohne Symlinks im privaten Smoke-Arbeitsverzeichnis bereitgestellt wird.
Sie ist keine globale Aktivierung oder Erlaubnis zum Laden anderer Plugins.
Die bestehende Peer-UID-/GID-Authentifizierung und private Socket-Zulassung
bleiben erforderlich; das Abschalten von `SO_PEERCRED` zur Vermeidung eines
Interpreter-Importfehlers würde diese Authentifizierungsgrenze entfernen.

## Wiederherstellung gepinnter Apache-HTTPD-Quellen

Die Parent-Runtime-Bereitstellung aktiviert eine eng begrenzte Wiederherstellung
für gepinnte HTTPD-Quellarchive: Nur eine direkte `404`-Antwort der exakten
kanonischen URL `https://downloads.apache.org/httpd/httpd-<version>.tar.bz2`
erlaubt einen Abruf unter `https://archive.apache.org/dist/httpd/` mit demselben
Dateinamen. Version und konfigurierter literaler SHA-256 bleiben unverändert.
Redirects, Berechtigungsfehler, Zeitüberschreitungen, fremde Hosts und andere
Komponenten lösen diese Wiederherstellung nicht aus. Der Digest wird vor
Archivauflistung oder Extraktion geprüft. Die Cache-Identität bleibt an das
kanonische Quelltupel gebunden; Metadaten erfassen die tatsächliche Download-URL
und den ausdrücklichen Wiederherstellungsgrund.

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
Projekt-Lockdatei samt geprüfter `.python-version`-Ansicht und `scripts/update-python-version.py --check --json`, um
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
`origin/master` neu auf, ändert nur das Lock-Feld `python_version` samt
`.python-version`-Ansicht, staged nur diese beiden Dateien
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

Das wiederverwendbare Fünf-Connector-Profil prüft seinen No-CRS-Workflow-Vertrag
vor der Matrixauflösung und verlangt Workflow-weites `permissions: {}` samt
nur den festen Job-Lesegrants. Dies erkennt Berechtigungs-/Wiring-Drift früh.

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

CodeQL analysiert Actions, beide Go-Module über die jeweils neueste stabile
Go-Release, die die trusted-base-Kopie des begrenzten Go-Updaters auflöst,
und einen begrenzten C/C++-Scope. Die Root-<code>.go-version</code> bleibt der
geprüfte aktuelle Selector und die monotone Untergrenze; sie ist kein
PR-kontrollierter CodeQL-Toolchain-Input. Bevor einer der Go-Jobs startet,
löst und validiert die trusted base die offiziellen Release-Metadaten und gibt
nur das exakte numerische Ergebnis an das gepinnte
<code>actions/setup-go</code> weiter. Dieser Scope führt
<code>make check-common-helpers-c17</code> sowie einen begrenzten
15-Sekunden-libFuzzer-Lauf für den Common-HTTP-Header-Parser mit C17,
AddressSanitizer und UndefinedBehaviorSanitizer aus. Die <code>go.mod</code>
jedes Moduls behält seine Go-Sprachbaseline. Bei seiner begrenzten planmäßigen
Auflösung wählt der Updater die höchste stabile numerische Go-Release und
schlägt sie nach read-only-Candidate-Validierung in einem Draft PR vor. Er darf
nur das Feld <code>go_version</code> der Projekt-Lockdatei,
<code>.go-version</code> und das feste, unabhängig validierte Envoy-
Komponenten-Bundle ändern; beliebige Modul- oder Dependency-Dateien kann er
nicht ändern. Das C/C++-Ergebnis beansprucht keine vollständige
Connector-Abdeckung; eine Erweiterung erfordert reproduzierbare Builds für den
ausgewählten Connector-Scope.

Scorecard nutzt Read-only-Berechtigungen für Same-Repository-Pull-Requests und
checkt den exakten Pull-Request-Head aus. Fork-Pull-Requests analysiert dieser
Job absichtlich nicht, weil ihr Head kein vertrauenswürdiger
Same-Repository-Ref ist. Die Default-Branch-Scorecard lädt SARIF nur mit der
separaten Berechtigung `security-events: write` hoch.

## Report-Scope des sequenziellen Smokes

`test-full-smoke-sequential.yml` verwendet die dedizierten Ziele
`test-smoke-sequential-no-crs` / `test-smoke-sequential-with-crs`.
Sein nativer Producer liefert Apache-/NGINX-Smoke-Ergebnisse, nicht die Full-
Matrix-, MRTS- und weiteren Runtime-Eingaben der allgemeinen Report-Aktualisierung.
Das Profil `bounded-smoke` entspricht diesem tatsächlichen Producer-Scope;
das Verhalten von allgemeinem `test-no-crs`, `test-with-crs` und
`refresh-all-reports` (`--strict-inputs`) bleibt unverändert.

Das begrenzte Profil verlangt frische Coverage- und Runtime-Cache-Reports aus
demselben Run. Ein privater Beleg bindet den exakten Parent-Commit, verifizierte
Framework-/MRTS-Gitlinks und Checkouts, festen Framework-Pfad, Variante, Build-
Root und native Fallauswahl. Jede ausgewählte Apache-/NGINX-Zeile muss richtige
Variante und Connector ausweisen, live ausgeführt sein und bestehen; fehlende
oder zusätzliche Fälle sind unzulässig. Die Produktions-CLI lässt nur ihre festen Parent-/Framework-Roots zu; native
Fallermittlung ist zeitlich begrenzt und leert geerbte Scope-Steuerungen.
Fehlgeschlagener/blockierter Producer-Status, veraltete oder symlinkbasierte
Eingaben, Identitätsdrift und beibehaltene Ausgaben lassen die Validierung scheitern. Der Snapshot-Generator muss frische
Parent-eigene Ausgabe für diesen Run schreiben, bevor beide verpflichtenden
Reports erfolgreich sind. Generierte Ausgabe ist Runtime-Evidence und keine
gestagte Quelländerung. Dieses Smoke-Profil erhöht keine Full-Matrix-, MRTS-
oder Response-Body-Coverage-Claims.

## Gewöhnlicher NGINX-Funktionskatalog und Host-Inventar

Der sequenzielle Apache-/NGINX-Producer verwendet
`ci/runtime/lifecycle/run-bounded-nginx-cases.py` für den gewöhnlichen NGINX-
Katalog. Er verwendet die bestehende typisierte Functional-A-Runtime je Fall,
mit festem `sudo`-/`env -i`-Einstiegspunkt, exakten Prüfungen committeter
Revisionen/Kataloge/Artefakte, einem getrennten Nicht-Root-NGINX-Worker und
einem Root-eigenen Traversal-Namespace. Builds, Downloads, CRS-Bereitstellung
und native Normalisierung bleiben unprivilegiert. Vor der privilegierten Fall-
Runtime werden vorbereitete CRS-Quelle und Preamble gegen die exakte Framework-
Release-Identität geprüft. Jeder Fall erhält frische Runtime-Pfade; begrenzte
normalisierte Ergebnisrecords werden in einen privaten Runner-eigenen Beleg
projiziert. Die vollständige native Fallmenge muss übereinstimmen, live laufen
und bestehen, bevor eine erfolgreiche Zusammenfassung geschrieben wird. Der
Harness bindet natives `case-info --output-root` ausdrücklich an seinen
validierten privaten Work-Root.

Diese Candidate-eigene Functional-A-Route belegt gewöhnliche funktionale
Ergebnisse. Sie aktiviert den unveränderlichen geschützten Broker nicht und
liefert keine adversariale Broker-Attestierung.
`make check-bounded-smoke-runtime-contract` führt die zuständigen Runtime-
Testmodule in diesem initialisierten Framework-Kontext aus. Die CI-Sicherheits-
Baseline des kopierten Updater-Baums bleibt getrennt und materialisiert weder
Framework-Quellen noch Git-Metadaten.

Beendet sich ein nativer NGINX-Fall vor der Erzeugung eines gültigen Ergebnisses,
erhält der Coordinator seinen tatsächlichen Exit-Code und projiziert Diagnose-
JSON in den vorhandenen privaten Runner-Beleg. Er liest nur das feste Root-
eigene, einfach verlinkte reguläre Harness-Log des Falls mit Modus `0600` über
einen No-Follow-Descriptor, mit einer Grenze von 131072 Bytes und stabiler
Dateiidentität. Der begrenzte Auszug ist JSON-escaped und enthält den Digest
des vollständigen Logs sowie die aktuelle Revisions-/Fall-/Variantenidentität.
Diese Diagnose ist kein normalisiertes Ergebnis und belegt keinen Fall-Pass.

Der Apache-Prozessguard durchquert Vorfahren mit ausschließlich Ausführungsrecht
über `O_PATH|O_DIRECTORY|O_NOFOLLOW` und erhält `O_RDONLY` für den privaten Leaf.
Descriptor-relative Eigentümer-, Modus-, Identitäts- und Symlink-Prüfungen bleiben
verbindlich; der gemeinsame Root-Namespace bleibt `0711` und der Runner-Workspace
bleibt `0700`.

Das generische Traefik-No-CRS-Host-Inventar löst ausschließlich das exakt
bereitgestellte Binary unter dem aktuellen Connector-Build-Root über
`ci/runtime/lifecycle/resolve-traefik-host-binary.py` auf. Eigentümer-, Dateityp-,
Link-, Schreibmodus-, Ausführbarkeits- und Containment-Prüfungen weisen ein
unsicheres Staging zurück. Geerbtes `TRAEFIK_BIN` und Shared-Cache-Pfade können
diesen Host nicht ersetzen; fehlendes/unsicheres Staging belässt das Inventar
bei `not_provisioned` und umgeht das Gate für konkrete Versions-Evidence nicht.
Das native Full-Lifecycle-Profil behält seinen getrennten Vertrag zur
Binary-Auswahl.

Das Apache-Host-Inventar verlangt einen erfolgreichen nativen Versionsbefehl
und genau eine gültige `Server version: Apache/`-Zeile aus stdout mit ASCII-
Versionsziffern. Stderr-Warnungen bleiben auf stderr sichtbar und werden nicht
zur Hostversion. Leere, reine Warnungs-, doppelte und gemischte Produktfamilien-
Ausgaben werden abgelehnt; weder Warnungen noch fehlgeschlagene Befehle belegen
eine konkrete Version.

## Validierung und Einschränkungen

Führen Sie `make check-ci-security-contract` für fokussierte statische Verträge
und die Validierung der Lock-Einträge aus. GitHub Actions-, CodeQL-, OSV-,
Gitleaks- und Scorecard-Ergebnisse sind nur Evidenz für Workflow, Event,
exakten SHA und Berechtigungen. Sie erzeugen keine automatischen Fixes,
ändern keinen Branch-Schutz, umgehen keine Reviews und ersetzen keine
Connector-/Runtime-Tests.
