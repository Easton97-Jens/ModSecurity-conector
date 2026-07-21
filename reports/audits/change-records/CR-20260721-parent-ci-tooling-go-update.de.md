# Change Record: Parent-CI-Tooling- und Go-1.26.5-Update

**Sprache:** [English](CR-20260721-parent-ci-tooling-go-update.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260721-parent-ci-tooling-go-update` |
| Datum (UTC) | `2026-07-21` |
| Basis-Revision | `5fa90474a79eaee2df034bf1c4389572fdcca42f` |
| Grenze | Nur Parent-CI-Workflows, Locks/Updater, die zwei Parent-Go-Module, ihre EN/DE-Dokumentation/Tests und dieses Record-Paar. Der Framework-Gitlink bleibt `784977615acfc55567e37b863309abc4a38ac877`; Framework und MRTS sind unverändert. |

## Motivation und Problemstellung

Das Parent-Repository benötigte aktuelle unveränderliche Action-Provenienz und
eine aktuelle Go-Basis, jedoch nur mit Maintenance-Automatisierung, die weder
den Default-Branch beschreibt noch force-pusht, merged, einen Draft in einen
Nicht-Draft verwandelt oder einen veralteten Kandidaten auf eine neuere
Default-Revision anwendet. Die vorherige Go-Direktive war in beiden echten
Modulen `1.24.13`; Checkout- und Python-Setup-Pins lagen hinter den überprüften
Stable-Releases.

## Akzeptanzkriterien

- Geänderte Action-Referenzen sind vollständige SHAs in Kleinschreibung mit
  passenden Release-Kommentaren und offizieller Tag-/Release-zu-Commit-
  Provenienz.
- Generische Action-/Tool-, Go-, Python- und Submodule-Publisher sind
  Draft-only, Normal-Push-only, Default-Branch-begrenzt und vor
  Rekonstruktion/Commit/Push an eine exakte frische Default-Basis gebunden.
- Resolver-/Validator-Ausgaben sind begrenzt; Candidate-Tool-Assets werden per
  SHA-256 und Archivlayout geprüft und erst dann begrenzt 30 Sekunden über
  Versions-Smokes ausgeführt.
- Beide Parent-Go-Module und CodeQL-Go-Jobs wählen `go 1.26.5`; Dependency-
  Auswahl und `go.sum` bleiben unverändert.
- EN/DE-Guides und dieses Record nennen beobachtete Evidenz, Grenzen und die
  Parent-/Framework-/MRTS-Grenze ohne Hosted-Ergebnisse zu behaupten.

## Implementierungsentscheidung und Begründung

Die Go-Basis wechselt in `connectors/envoy/ext_proc/go.mod`,
`connectors/traefik/native_middleware/go.mod` und beiden CodeQL-Go-Jobs von
`1.24.13` zu `1.26.5`. Das für die lokale Validierung geprüfte offizielle Archiv
war `go1.26.5.linux-amd64.tar.gz`, SHA-256
`5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053`, aus
den offiziellen [Go-Download-Metadaten](https://go.dev/dl/?mode=json&include=all)
und dem [Archiv](https://go.dev/dl/go1.26.5.linux-amd64.tar.gz).
`GOTOOLCHAIN=local` bindet CodeQL an die setup-go-Auswahl.

Workflow-Lock und passende Referenzen werden aktualisiert, darunter
`actions/checkout` v7.0.1 bei
`3d3c42e5aac5ba805825da76410c181273ba90b1` und
`actions/setup-python` v7.0.0 bei
`5fda3b95a4ea91299a34e894583c3862153e4b97`. Neue generische Action-/Tool-
und Go-Updater trennen öffentliche Auflösung, isolierte Validierung und eng
profilierten Publisher. Bestehende Python- und Submodule-Updater erhalten
dieselben No-Force-/Draft-/Base-Binding-Kontrollen.

Der Python-Vertrag traversiert nun YAML-Semantik statt brüchigem Textlayout. In
einem inventarisierten Python-Job erlaubt er genau ein kanonisches gepinntes
Setup und weist Interpreterauswahl über andere Shells, PATH-, Environment-
Datei- oder `tee`-Writes, dynamische Ausgabeziele, alternative Setups und
dynamische Launcher zurück. Publisher-Kandidaten erfassen und prüfen eine
Default-Base-SHA nach jedem relevanten Fetch erneut; neue Branches starten
explizit an dieser Remote-Tracking-Revision.

## Security-Auswirkung

Dies ist CI-Supply-Chain- und Delivery-Hardening. Es verhindert mutable Pins,
ungeprüfte Redirects/Assets, Mischung aus veralteten Kandidaten und Default-
Basis, Force-/Default-Pushes, Auto-Merge-/Nicht-Draft-Maintenance-Lieferung
sowie getestete Python-Interpreterauswahl-Umgehungen. Es fügt keinen direkten
Default-Branch-Schreibpfad hinzu und ändert keinen Framework-Gitlink oder
MRTS-Inhalt.

## Geänderte Dateien

- Parent-GitHub-Workflows, insbesondere generische Action-/Tool-, Go-, Python-
  und Submodule-Maintenance-Publisher sowie CodeQL-Selektoren und volle SHA-Pins.
- `scripts/update-github-actions-versions.py`, `scripts/update-go-version.py`,
  sicherer Tool-Fetcher, Workflow-Verträge, Lock-Daten und fokussierte
  Fixtures/Tests.
- Nur die beiden Parent-Go-Moduldeklarationen; kein Dependency-, Source- oder
  `go.sum`-Update ist beabsichtigt.
- EN/DE-CI-Tooling- und Compiler-/Build-Guides, Generatoren/Tests und dieses
  englische/deutsche Record-Paar mit Index.

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Go 1.26.5 `go mod verify` und `go mod tidy -diff` in beiden echten Modulen | bestanden; kein tidy- oder `go.sum`-Drift. |
| Go 1.26.5 `go test -mod=readonly ./...`, `go vet ./...` und `go build -mod=readonly ./...` | für direkte Module bestanden; Envoy nutzt im isolierten Worktree dokumentiert `-buildvcs=false`. |
| Go 1.26.5 `go list -m all` und `go mod graph` | bestanden; ausgewählte Dependencies bleiben unverändert, Root-Go wird 1.26.5. |
| Go 1.26.5 `govulncheck` für Envoy | Exit 0, keine code-reachable Vulnerabilities; zwei Import- und sechs Required-Module-Advisories wurden nicht aufgerufen und bleiben explizite Evidenz. |
| Go 1.26.5 `govulncheck` für Traefik | Exit 0, keine Vulnerabilities gefunden. |
| Traefik-Native-Middleware-Script-Test/-Build mit Go 1.26.5 | bestanden. |
| `tests.test_python_version_contract` und realer Python-Contract-Checker | 30/30 bestanden; 30 Jobs, null Violations. |
| CI-Security-, Action-/Go-/Python-Updater-, Bilingual-Doku- und semantische Publisher-/TOCTOU-Tests | fokussierte Läufe bestanden: 51 Action/Go/CI-Security, 22 Python-Updater und 48 Doku/CI-Security/Action-Updater-Tests. |
| Vollständiges `unittest discover -s tests -q`, Actionlint für alle vier Publisher, Action-Version-Verifier und `git diff --check` | bestanden; Discovery gab nur die erwartete connector-capabilities usage diagnostic aus. |

## Runtime-Evidence

Direkte Modul- und Traefik-Native-Middleware-Ergebnisse belegen nur Build-/
Testverhalten. Dieses CI-/Toolchain-Change behauptet keine Connector-Request-,
Protokoll-, CRS-, Framework- oder MRTS-Runtime.

## Nicht ausgeführte Prüfungen mit Begründung

- `make check-bilingual-docs` wurde ausgeführt, gibt aber nur die bestehenden
  fehlenden Framework-Linkziele aus, weil dieser Worktree den Framework-Gitlink
  absichtlich uninitialisiert lässt. Das neue Change-Record-Paar selbst besteht
  den Checker; weder Gitlink noch Framework-Dateien wurden initialisiert oder
  geändert, um diesen Check künstlich bestehen zu lassen.
- Envoy-Native-Bridge/-Runtime lief nicht, weil der isolierte Parent-Worktree
  keinen initialisierten Framework-Gitlink oder libmodsecurity-/Host-
  Voraussetzungen besitzt. Sie wird nicht aus dem direkten Envoy-Modulresultat
  abgeleitet.
- Exakte-Draft-PR-Head-CodeQL-, OSV-, Gitleaks-, Scorecard-, SonarQube-Cloud-
  und weitere Hosted-Checks sind Evidenz nach Veröffentlichung.
- Kein Dependabot-Alert und kein Dependency-Graph wurde durch diese Änderung
  revalidiert, geschlossen oder verworfen; das exakte OSV-Ergebnis für den
  PR-Head ist ebenfalls noch nicht beobachtet.
- Kein Dependency-Upgrade, kein `go.sum`-Rewrite, kein Framework-Gitlink-
  Update, keine MRTS-Initialisierung und kein automatischer Merge sind im Scope.

## Bekannte Einschränkungen

Updater-Profile unterstützen absichtlich nur überprüfte Pfade, Workflow-Shapes,
Asset-Layouts und Shell-Policy. Ein neuer Action-/Tool-Typ oder eine neue
Maintenance-Datei braucht einen expliziten Profile-/Contract-Review. Der
statische Workflowvertrag kann Runtime-Verhalten beliebiger Drittanbieter-
Actions oder opaker Executables nicht beweisen; seine Grenze sind gepinnte
Workflow-Quellen und getestete Interpreter-/Pfad-Oberflächen.

## Verbleibende Risiken

Die nicht code-reachable Envoy-`govulncheck`-Advisory-Zeilen bleiben Dependency-
und Import-Evidenz. Hosted-PR-Head-Sicherheitschecks und die nicht verfügbare
Envoy-Native-Runtime benötigen weiter getrennte beobachtete Evidenz. Keines
wird verworfen, verborgen oder als Merge-Autorisierung behandelt.

## Finaler Diff- und Review-Status

Dieses Record wird vor Parent-Staging, Commit, Push, PR-Erstellung und Hosted-
Check-Evidenz geschrieben. Es hält nur beobachtete lokale Evidenz fest und
reserviert die verlangte Draft-only-Lieferung und Exact-Head-Prüfung für die
nachfolgenden kontrollierten Schritte.
