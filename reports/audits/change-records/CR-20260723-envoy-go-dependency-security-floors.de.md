# Change Record: Envoy-Go-Dependency-Sicherheitsgrenzen

**Sprache:** [English](CR-20260723-envoy-go-dependency-security-floors.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260723-envoy-go-dependency-security-floors` |
| Datum (UTC) | `2026-07-23` |
| Basis-Revision | `a308d7b414f0859490fe7253e0683a4bde80b563` |
| Grenze | Ausschließlich Parent-Envoy-`ext_proc`-Modul, zugehöriger Parent-Test und Leserdokumentation sowie dieses Change-Record-Paar/Index; Framework, MRTS und beide Gitlinks bleiben unverändert. |
| Finding-Verknüpfung | Dependabot-Alerts #1/#2; Scorecard `VulnerabilitiesID` #12; `FND-GITHUB-0001` und `FND-PARENT-0001`. |

## Motivation und Problemstellung

Der aktuelle Master wählte im Envoy-`ext_proc`-Modul gRPC `v1.79.3`, x/net
`v0.48.0`, x/sys `v0.39.0` und x/text `v0.32.0`. Frische Dependabot-, OSV- und
govulncheck-Evidence identifizierte offene gRPC-/x/net-Alerts sowie weitere
Scorecard-Dependency-Zeilen. Die vorhandene Go-1.26.5-Modulbaseline unterstützt
die veröffentlichten gefixten Modulversionen.

## Akzeptanzkriterien

- Das Envoy-`ext_proc`-Modul wählt gRPC `>=v1.82.1`, x/net `>=v0.56.0`,
  x/sys `>=v0.46.0` und x/text `>=v0.39.0`, ohne seine Go-Baseline zu ändern.
- Resolver-erforderliche indirekte Updates und `go.sum`-Änderungen sind tidy und
  verifiziert.
- Ein fokussierter statischer Vertrag verhindert Downgrades unter jede Grenze,
  lässt jedoch spätere stabile Sicherheitsversionen zu.
- Englisch/deutsche Leserdokumentation und dieses Change-Record-Paar beschreiben
  dieselben Grenzen und Einschränkungen.
- Go-Modultests, Vet, Build und aktuelles Vulnerability-Scanning bestehen mit
  der task-lokalen Go-1.26.5-Toolchain.
- Es werden weder Alert-Closure, Merge, direkter `master`-Push, Framework- oder
  MRTS-Änderung noch eine PyYAML-Suppression behauptet.

## Implementierungsentscheidung und Begründung

Der Fix aktualisiert über den Go-Resolver das einzige betroffene Parent-Modul.
Er pinnt die beiden Dependabot-Fixes und die Mindestversionen, die die aktuellen
x/sys- und x/text-Scorecard-Findings entfernen. x/net `v0.56.0` verlangt x/sys
`v0.46.0`; deshalb ist die resolver-ausgewählte x/sys-Version absichtlich höher
als die minimale gefixte Advisory-Version. Die resultierenden xDS-,
protoc-gen-validate- und genproto-Inkremente sind Resolver-Closure, keine
unabhängigen Updates.

Der Regressionstest parst stabile `go.mod`-Requirements und vergleicht
numerische SemVer-Tupel. Er schlägt für fehlende, fehlerhafte oder
Pre-Release-Target-Requirements fehl, lässt aber spätere stabile Patch-/Minor-
Sicherheitsupdates zu.

## Geänderte Dateien

- `connectors/envoy/ext_proc/go.mod` und `go.sum`
- `tests/test_ci_security_workflows.py`
- `connectors/envoy/ext_proc/README.md` und `README.de.md`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Offizielle Go-1.26.5-Release-Index-/Hash-Verifikation im registrierten privaten Task-Run | bestanden; Archiv-SHA-256 stimmte mit `5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053` überein. |
| Baseline-`go mod graph`, `go mod verify`, Test, Vet und Build mit isoliertem Go 1.26.5 | bestanden vor der Remediation; die aktuellen Auswahlen lagen unter den notwendigen Grenzen. |
| `go get google.golang.org/grpc@v1.82.1 golang.org/x/net@v0.56.0 golang.org/x/sys@v0.46.0 golang.org/x/text@v0.39.0` | bestanden; der erste `x/sys@v0.44.0`-Kandidat wurde abgelehnt, weil x/net `v0.56.0` `v0.46.0` verlangt. |
| Kandidat `go mod tidy`, `go mod tidy -diff` und `go mod verify` | bestanden. |
| Kandidat `go test -mod=readonly ./...` und `go vet ./...` | bestanden. |
| Kandidat `go build -buildvcs=false -mod=readonly ./...` | bestanden; der ungeflagte isolierte-Worktree-Build ist unten dokumentiert. |
| Kandidat `govulncheck -show verbose ./...` mit task-lokalem Go zuerst in `PATH` | bestanden: keine Vulnerabilities gefunden. |
| Fokussierter Dependency-Floor-Vertrag | bestanden; 17 Unit-Tests sowie die actionlint-, zizmor- und gitleaks-Validate-only-Kontrollen bestanden. |
| Repository-Bilingual-Dokumentationsprüfung | nur durch 20 bereits bestehende fehlende Framework-Gitlink-Linkziele in diesem isolierten Worktree blocked_environment; keine Diagnose nannte ein geändertes englisches/deutsches Paar. |

## Security-Auswirkung

Dies ist eine Supply-Chain-Dependency-Remediation für das Netzwerk-bedienende
gRPC-`ext_proc`-Modul des Parent. Sie entfernt die aktuellen von govulncheck
gemeldeten Modul-/Paketresultate und wählt Dependabots veröffentlichte gefixte
gRPC-Version plus die vollständige x/net-Grenze. Der aktuelle Scan fand vor dem
Update kein direkt aufgerufenes verwundbares Symbol; diese
Erreichbarkeits-Gegen-Evidence ist keine Alert-Dismissal und schwächt die
Versionsremediation nicht.

Die zwei historischen PyYAML-IDs in der aggregierten Scorecard-Meldung sind
unter deklariertem `PyYAML>=6,<7` und dem exakten CI-Lock `6.0.3` bereits sicher.
Es wird keine unnötige Python-Änderung oder Suppression aufgenommen.

## Runtime-Evidence

Das Update ändert keinen Connector-Protokoll-, Konfigurations- oder
Anwendungscodepfad. Parent-Go-Unit-, Vet-, Build-, Modulintegritäts- und
Vulnerability-Scanner-Kontrollen belegen nur Modulkompatibilität. Die optionale
Common/libmodsecurity-Bridge bleibt übersprungen, da keine expliziten nativen
Include-/Library-Pfade bereitgestellt wurden.

## Bekannte Einschränkungen

Der isolierte Worktree materialisiert nicht die Parent-relative Framework-
Rules-Fixture, welche der Runtime-Config-Teil von `make test-envoy-ext-proc`
nutzt; dieser Teil ist `blocked_environment`. Die direkten Envoy-Modultests
bestanden, und die unveränderte Parent-Baseline absolvierte das Config-Segment.
Das ersetzt keinen späteren echten Envoy/Common-Runtime-Smoke-Run mit seinen
expliziten Voraussetzungen.

## Verbleibende Risiken

Dependabot und Scorecard bleiben offen, bis ihre gehosteten Scans auf der
resultierenden Default-Branch-Revision aktualisiert wurden. Diese Änderung löst
nicht die getrennten Scorecard-Ursachen BranchProtectionID, CodeReviewID,
MaintainedID, CIIBestPracticesID oder FuzzingID. Es wird weder eine externe
Governance-Einstellung, Reviewer-Evidence, OpenSSF-Registrierung noch
Alert-Dismissal versucht.

## Nicht ausgeführte Prüfungen mit Begründung

- Exakte PR-Head-CodeQL-, OSV-, Scorecard-, Dependabot-Refresh-, Gitleaks-Range-,
  SonarQube-Cloud- und GitHub-Review-Evidence existiert vor dem Draft PR nicht
  und kann lokal nicht abgeleitet werden.
- Der ungeflagte `go build -mod=readonly ./...` in diesem isolierten Worktree
  ist durch VCS-Stamping blockiert; `-buildvcs=false` ist das dokumentierte
  lokale Äquivalent und bestand.
- Voller nativer Envoy/Common-Runtime-Smoke benötigt explizites libmodsecurity,
  Envoy und vorbereitete Host-Voraussetzungen, die für diese Dependency-only-
  Änderung nicht ausgewählt sind.

## Finaler Diff- und Review-Status

Dieser Record ist vor Staging, Commit, Push, Pull-Request-Erstellung und
externer Check-/Review-Evidence geschrieben. Die lokale Validierung ist
abgeschlossen. Ein unabhängiger fokussierter Security-Review fand keinen neuen
berichtspflichtigen Security-Befund; er dokumentierte einen optionalen künftigen
Guard gegen Repository-kontrollierte Go-replace-/Workspace-Auflösung als im
geprüften Zustand nicht anwendbar. Finale Delivery-Evidence steht noch aus; es
wird keine Alert-Closure behauptet.
