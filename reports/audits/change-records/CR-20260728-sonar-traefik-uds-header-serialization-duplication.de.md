# Change Record: Traefik-UDS-Header-Serialisierungs-Deduplizierung für SonarQube Cloud

**Sprache:** [English](CR-20260728-sonar-traefik-uds-header-serialization-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-traefik-uds-header-serialization-duplication |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Grenze | Ausschließlich Parent-Traefik-Native-Middleware-UDS-Header-Serializer und fokussierte Source-Tests sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework, MRTS, beide Gitlinks, Workflow, Scanner-Policy und generierte Reports bleiben unverändert. |
| Finding-Verknüpfung | Parent-SonarQube-Cloud-Remediation der Duplikatzeilendichte. Dieser Source-Refactor schließt vor einer Exact-Head-Analyse keinen einzelnen externen Befund. |

## Motivation und Problemstellung

Die Request- und Response-Header-UDS-Payload-Builder enthielten jeweils
dieselbe Serialisierung aus Header-Anzahl und geordneten Name/Wert-Paaren. Die
getrennten Kopien vergrößerten die Parent-Duplikatkennzahl und erhöhten das
Risiko, dass eine spätere Protokolländerung nur einen Pfad erreicht.

Die Werte sind an dieser Grenze sicherheitsrelevant: HTTP-Request- oder
Upstream-Response-Header werden zu Bytes für den privaten Local-Engine-
Unix-Socket. Die Behebung teilt deshalb nur den byte-identischen
Serialisierungskern. Sie darf weder Validierung verbreitern noch Frame-Format
oder caller-eigene Lifecycle- und Vorbedingungslogik verschieben.

## Akzeptanzkriterien

- Ein privater Helper hängt für beide Builder exakt die bestehende
  uint16-Headeranzahl und die geordneten validierten Name/Wert-Paare an.
- `buildUDSBegin` behält seine frühe Headeranzahlprüfung, Metadatenkodierung,
  HTTP-Standardversion und finale Payloadgrößenprüfung.
- `buildUDSResponseHeaders` behält Status-/Anzahlprüfungen, HTTP-
  Standardversion und finale Payloadgrößenprüfung.
- Direkte Tests belegen das bytegenaue Request- und Response-Layout mit dem
  Fallback `HTTP/1.1` sowie fail-closed Rejection beider Builder für zu viele
  Header, leere/NUL-/zu lange Felder und eine zu große Gesamtpayload.
- Isolierte Go-1.26.5-Tests, Race-Check, begrenztes Fuzzing, Modultest, Vet,
  Build, Formatierung, Whitespace und fokussierte Sicherheitsreview bestehen.
- Es werden weder gehostete Alert-Closure noch Ready-for-review, Merge,
  Master-Update, Framework-/MRTS-Änderung oder Scanner-Policy-Änderung
  behauptet.

## Implementierungsentscheidung und Begründung

`appendUDSHeaderPairs` besitzt nur die bereits beiden Callern gemeinsame
Sequenz:

1. `uint16(len(headers))` anhängen;
2. für jeden Eingabeheader in Reihenfolge den erforderlichen begrenzten Namen
   anhängen;
3. den optionalen begrenzten Wert anhängen.

Alle Feldprüfungen bleiben in unverändertem `appendUDSText`. Der Helper
validiert keine Headeranzahl-Policy, wählt keinen Opcode, allokiert keinen
Frame, setzt keine Default-Version, serialisiert weder Request-Metadaten noch
Response-Status, schreibt nicht zum Socket und mutiert keinen
Transaktionszustand. Beide Caller behalten ihre bisherigen frühen Prüfungen
und das Payloadlimit nach der Serialisierung; damit bleiben Fehlerreihenfolge
und fail-closed Verhalten erhalten.

## Geänderte Dateien

- `connectors/traefik/native_middleware/engine_uds.go`
- `connectors/traefik/native_middleware/engine_uds_test.go`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Offizielle task-lokale Go-1.26.5-Provenance-, SHA-256-, Archivlayout- und exakte Versionsprüfung | bestanden; das offizielle Linux-AMD64-Archiv entsprach SHA-256 `5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053`. |
| `go mod verify` mit isolierter No-Network-/Read-only-Module-Toolchain | bestanden. |
| Fokussierte `TestUDS` und `-race` `TestUDS` | bestanden. |
| `FuzzUDSFrameAndResult`, 15 Sekunden, ein Worker | bestanden; 93.578 Ausführungen und keine neue interessante Eingabe. |
| `go test -mod=readonly ./...`, `go vet ./...` und `go build -mod=readonly ./...` | bestanden. |
| `gofmt -d engine_uds.go engine_uds_test.go` und `git diff --check` | bestanden; keine Ausgabe. |
| Unabhängige fokussierte Post-Diff-Sicherheitsreview | bestanden; keine plausible Regression und kein berichtspflichtiger Befund. |
| Repository-Bilingual-Dokumentations-, Repository-Pfad- und Linkprüfungen | nach read-only Initialisierung des Parent-gebundenen Framework-Commits bestanden; das Framework blieb sauber und unverändert. |

## Security-Auswirkung

Der Refactor erhält die bestehende Defense-in-Depth vor jedem UDS-Write:
caller-eigene Anzahlgrenzen, erforderliche nichtleere Namen,
Byte-Feldgrenzen, uint16-Darstellbarkeit, NUL-Rejection, finale Builder-
Payloadgrenzen sowie die unabhängigen Prüfungen in `exchangeLocked` und
`writeUDSFrame`. Request-Metadaten, Response-Status-/Versionsbehandlung,
Opcode-Wahl, Socket-Deadlines, Sessionzustand und Lifecycle liegen außerhalb
des gemeinsamen Helpers und bleiben unverändert.

Die fokussierte Review fand keine Evidenz dafür, dass ein fehlerhafter Header
über den neuen Helper zum Socket gelangt. Die direkten Tests prüfen gültiges
Byte-Layout und das Verhalten beider Builder bei Fehlern; vorhandene
Lifecycle-Tests decken weiterhin die UDS-Opcode-Reihenfolge einer einzigen
Session ab.

## Runtime-Evidence

Die neuen direkten Serializer-Tests sind Source-Level-Bytevertrags-Evidence.
Die gleiche fokussierte Go-Suite führt auch die bestehenden lokalen
Unix-Socket-Lifecycle-Tests aus, startet aber weder Traefik noch lädt sie ein
Plugin, ruft Common/libmodsecurity oder CGo auf oder behauptet eine native
Host-Runtime-Capability.

## Bekannte Einschränkungen

Der Helper verlässt sich absichtlich auf seine zwei privaten vorvalidierten
Caller für die `udsMaxHeaders`-Policy. Sein aktueller Aufrufgraph beschränkt
sich auf diese Caller; ein künftiger Caller muss die explizite Anzahlprüfung
vor der Übergabe eines Slice an den Helper beibehalten. Die Änderung beweist
nicht die vollständige Abwesenheit weiterer UDS- oder Hostfehler.

## Verbleibende Risiken

Die Änderung beweist nicht das Verhalten eines externen UDS-Peers oder einer
vollständigen Traefik/Common-Installation.

## Nicht ausgeführte Prüfungen mit Begründung

- Exakte PR-Head-Hosted-Checks und SonarQube-Cloud-Analyse erfordern den
  normalen task-eigenen Draft-PR-Delivery-Zyklus und stehen auf dieser
  Record-Stufe noch aus.
- Vollständige Traefik-Host-/Plugin- und Private-Engine-Runtime-Tests benötigen
  getrennte native Voraussetzungen und werden nicht als lokale Source-Test-
  Evidence dargestellt.

## Finaler Diff- und Review-Status

Dieser Record wird vor Staging, Commit, Push, Pull-Request-Erstellung und
externer Analyse für diesen Kandidaten geschrieben. Die lokale Source-
Validierung und die fokussierte Sicherheitsreview bestehen. Eine
Duplikatcode-Reduktion wird erst nach einer frischen Exact-Head-SonarQube-
Cloud-Analyse behauptet.
