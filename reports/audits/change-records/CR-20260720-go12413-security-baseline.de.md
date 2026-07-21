# Change Record: Go-1.24.13-Sicherheitsbaseline

**Sprache:** [English](CR-20260720-go12413-security-baseline.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260720-go12413-security-baseline` |
| Datum (UTC) | `2026-07-20` |
| Basis-Revision | `f2376bb3e39ffbe9d36faca8bcd7397477eadd10` |
| Grenze | Ausschließlich Parent-Go-Moduldeklarationen, Parent-CodeQL-Workflow, Parent-Generator/Tests/Dokumentation und dieses Change-Record-Paar; Framework, MRTS und beide Gitlinks bleiben unverändert. |
| Finding-Verknüpfung | Exact-Master-OSV-Run `29780297716`, Job `88479684583`; `FND-PARENT-0001` und `FND-GITHUB-0001`. |

## Motivation und Problemstellung

Der Exact-Master-OSV-Advisory-Workflow meldete 33 behebbare
Go-Standardbibliotheksvorkommen aus den beiden Parent-Moduldeklarationen mit
`go 1.24.0`. Achtzehn dieser Vorkommen haben veröffentlichte Fixes bei oder
unter Go `1.24.13`. Die verbleibenden fünfzehn benötigen Go `1.25.8` oder
später; auch die sichere Version `golang.org/x/net v0.55.0` für Dependabot
Alert #1 verlangt Go `1.25`. Diese Punkte bleiben bewusst außerhalb dieses
engen Patches.

## Akzeptanzkriterien

- Beide Parent-Go-Module deklarieren das gepatchte Minimum `go 1.24.13`.
- Beide CodeQL-Go-Jobs wählen `go-version: '1.24.13'`.
- Generierte EN/DE-Compiler-Guides, CI-Sicherheitsdokumentation und fokussierte
  Tests beschreiben dieselbe Baseline.
- Der gelockte Modulgraph und beide `go.sum`-Dateien bleiben unverändert.
- Jedes Modul besteht `go mod verify`, `go mod tidy -diff`, `go test` und
  `go vet` mit Go `1.24.13`; die CodeQL-äquivalenten Builds werden soweit wie
  der isolierte Worktree erlaubt geprüft.
- Die Änderung behauptet nicht, die Go-1.25-only-OSV-Zeilen, Dependabot #1,
  die 83 historischen Gitleaks-Kandidaten oder Framework-/MRTS-Arbeit zu lösen.

## Implementierungsentscheidung und Begründung

Die kleinste vollständige Parent-Änderung hebt nur die beiden `go`-Direktiven
und die beiden CodeQL-`actions/setup-go`-Eingaben an. Sie ändert die
Generatorquelle, regeneriert deren englische/deutsche Compiler-Guide-Ausgaben
und aktualisiert die fokussierten Tests für die exakten Pins. Sie fügt bewusst
keine `toolchain`-Direktive hinzu, führt kein `go get` aus und nimmt keine
Dependency-, `go.sum`-, `x/net`- oder Traefik-Host-Source-Änderung vor.

Die Sicherheitsinvariante ist, dass unterstützte Parent-Go-1.24-Builds und die
zugehörigen CodeQL-Jobs keine ungepatchte Go-`1.24.0`-Standardbibliotheksbaseline
auswählen. Vorhandene Modul-APIs, Imports, ausgewählte Dependency-Versionen und
legitimes Go-Build-/Testverhalten bleiben unverändert.

## Security-Auswirkung

Dies ist eine Supply-Chain-/Toolchain-Baseline-Remediation und keine Behauptung,
dass jede zugrunde liegende Standardbibliotheks-Advisory von einer
Connector-Anfrage erreichbar ist. Das Scanner-Signal vor der Änderung führt
von der `go 1.24.0`-Deklaration jedes Moduls zur Go-Standardbibliotheksauswertung
von OSV; CodeQL wählte getrennt dieselbe alte Toolchain. Das Anheben von
Deklaration und CI-Selektoren schließt den Go-1.24-Patch-Line-Anteil, ohne
Scanner-Output zu verbergen. Ein direkter
`go list -buildvcs=false -deps`-Check fand weiterhin keinen
`golang.org/x/net/html`-Import im Envoy-Modul. Das ist Gegen-Evidence für den
spezifischen Dependabot-Parserpfad, aber keine Alert-Disposition.

## Geänderte Dateien

- `.github/workflows/ci-security-codeql.yml`
- `connectors/envoy/ext_proc/go.mod`
- `connectors/traefik/native_middleware/go.mod`
- `scripts/generate_compiler_guides.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_compiler_guides.py`
- `docs/build/compilers/envoy.md` und `docs/build/compilers/envoy.de.md`
- `docs/build/compilers/traefik.md` und `docs/build/compilers/traefik.de.md`
- `docs/security/ci-security-tooling.md` und
  `docs/security/ci-security-tooling.de.md`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| `rtk make check-ci-security-contract` | bestanden: 13 fokussierte Workflow-/Sicherheits-Contract-Tests einschließlich beider exakter CodeQL-Go-Pins. |
| `rtk make check-compiler-guides` | bestanden: 19 Generator-, EN/DE-Paritäts-, Link-, Shell-Syntax- und Current-Output-Tests. |
| Go `1.24.13` mit `go mod verify` und `go mod tidy -diff` in jedem tatsächlichen Modul | bestanden: Beide Modulgraphen verifizieren und keine der beiden Tidy-Prüfungen gibt einen Diff aus. |
| Go `1.24.13` mit `go test -mod=readonly ./...` und `go vet ./...` in jedem tatsächlichen Modul | bestanden: Envoy-Processor-Tests und Traefik-Middleware-Tests bestehen; Vet gibt keine Diagnosen aus. |
| Go `1.24.13` mit `go build -mod=readonly ./...` | für Traefik bestanden. Der ungeflagte lokale Envoy-Build ist durch VCS-Stamping im isolierten Worktree blockiert; `go build -buildvcs=false -mod=readonly ./...` bestand als dokumentiertes lokales Äquivalent. |
| `go mod graph` für Envoy | bestanden: Der Graph wählt weiter `golang.org/x/net@v0.48.0`, `golang.org/x/sys@v0.39.0` und `golang.org/x/text@v0.32.0`; nur die Root-Zeile `go@1.24.13` änderte sich. |
| `go list -buildvcs=false -deps`-Exaktcheck für `golang.org/x/net/html` | bestanden ohne passenden Importpfad. |
| `rtk git diff --no-ext-diff --exit-code -- connectors/envoy/ext_proc/go.sum connectors/traefik/native_middleware/go.sum` und `rtk git diff --no-ext-diff --check` | bestanden: kein Prüfsummen- oder Whitespace-Drift. |

## Runtime-Evidence

Nicht anwendbar. Die Änderung ist ein Minimum-Toolchain- und
CI-Selector-Update; sie verändert keinen Connector-Protokollpfad, keine
Host-Konfiguration, kein HTTP-Verhalten, kein CRS, kein MRTS und keine native
Runtime. Die obigen Modul-Unit-/Build-Ergebnisse belegen nur das angegebene
Go-Modulverhalten.

## Nicht ausgeführte Prüfungen mit Begründung

- Ein neuer Exact-PR-Head-CodeQL-Run, OSV-Vergleich, Gitleaks-Pull-Request-Range,
  Scorecard- und SonarQube-Cloud-Ergebnis existieren noch nicht. Sie sind für
  den späteren exakten PR-Head erforderlich und werden nicht aus lokalen Checks
  abgeleitet.
- `rtk make check-bilingual-docs` wurde ausgeführt, ist aber durch den nicht
  initialisierten Framework-Gitlink im isolierten Worktree blockiert: Es gab
  `2` ausschließlich für bestehende fehlende Framework-Link-Targets zurück,
  nicht für eines der geänderten EN/DE-Paare.
- Native Envoy- und Traefik-Host-Builds/Runtimes benötigen libmodsecurity und
  vorbereitete Host-Voraussetzungen, die in diesem isolierten Parent-Worktree
  nicht vorhanden sind.
- Keine Go-`1.25`-Migration, kein `golang.org/x/net`-Update, kein
  Dependabot-Closure und keine individuelle historische Gitleaks-Triage wurden
  versucht, weil jede davon eine getrennte Entscheidung oder sichere
  Occurrence-Evidence benötigt.

## Bekannte Einschränkungen

Das OSV-Ergebnis behält nach diesem engen Patch fünfzehn Go-1.25-only-Vorkommen.
Eine zukünftige koordinierte Go-1.25-Baseline-Entscheidung muss Modul, CI,
Dokumentation und Dependency-Graph gemeinsam aktualisieren und danach alle
Exact-Head- und Resulting-Master-Controls wiederholen. Der vollständige
Bilingual-Checker kann in diesem Worktree nicht abschließen, bis sein fremder
Framework-Inhalt ohne Änderung initialisiert ist.

## Verbleibende Risiken

Dependabot Alert #1 bleibt offen, weil die kompatible sichere `x/net`-Version
Go `1.25` verlangt. Die 83 historischen Gitleaks-Signale bleiben untriagierte
Kandidaten, weil der Advisory-Workflow kein payload-sicheres,
Occurrence-Level-Manifest bereitstellt. Keines der Risiken wird durch diese
Änderung akzeptiert, dismissed oder verborgen.

## Finaler Diff- und Review-Status

Fokussierte lokale Validierung, Generator-Review, Dependency-Drift-Review und
Whitespace-Review bestanden. Dieser Record wird vor Staging, Commit, Push,
Pull-Request-Erstellung oder externer Check-/Review-Evidence geschrieben; es
wird keine Delivery oder Alert-Closure behauptet.
