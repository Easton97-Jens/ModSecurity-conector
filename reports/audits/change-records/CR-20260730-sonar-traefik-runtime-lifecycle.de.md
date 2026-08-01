# Change Record: Parent-Traefik-Runtime- und Lifecycle-Remediation

**Sprache:** [English](CR-20260730-sonar-traefik-runtime-lifecycle.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260730-sonar-traefik-runtime-lifecycle` |
| Datum (UTC) | 2026-07-30 |
| Basis-Revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | `FND-SONAR-0016`; der SonarQube-Cloud-Follow-up des exakten PR-#203-Heads wird als Parent-Draft-PR-New-Code-Remediation getrackt. |
| Grenze | Nur Parent `connectors/traefik/` und direkte Parent-Tests. |

## Motivation und Problemstellung

Der ForwardAuth-Runner löscht und erzeugt Ergebnis-Pfade jetzt nur noch als
Nicht-Root-Nachfolger des verifizierten `BUILD_ROOT`. Der Native-Runner
validiert einen besitzergesteuerten, nicht ersetzbaren Output-Vorfahren.
Native Literal-/Parser-, Go-Stream-/UDS- und C17-Engine-Kontrollfluss wurden
ohne Änderung des Wire- oder Lifecycle-Vertrags zerlegt. Der PR-Follow-up
ersetzt direkte `context.Context`-Felder in den Request-Wrappern durch einen
unveränderlichen Request-Lifetime-Provider, trennt CLI-Option-Consumption von
der Schleifensteuerung und teilt die Testmodul-Import-Assertions auf.
Framework, MRTS, Gitlinks, Workflows, Sonar-Regeln, Exclusions, Suppressions
und Quality Gates bleiben unverändert.

Frische CodeQL-Evidenz zeigte ein zweites, enges Vertragsproblem: Der
produktive UDS-Framer akzeptierte einen generischen `io.Writer`, obwohl der
reale Engine-Austausch nur über seine private bidirektionale `net.Conn` gültig
ist. Der produktive Framer ist jetzt connection-typisiert; die Byte-Buffer-
Konstruktion bleibt test-only.

## Implementierungsentscheidung und Begründung

Die Reparatur erzwingt bestehende Private-Root-Trust-Boundaries vor
zustandsändernden Operationen und extrahiert unabhängige Lifecycle-Aufgaben in
kleine Helper. Das `http.ResponseWriter`-Interface besitzt keinen
Context-Parameter; deshalb bewahrt ein pro Request unveränderlicher Provider
die Cancel-/Deadline-Propagation für Engine-Callbacks ohne Speicherung eines
direkten `context.Context`-Feldes. Dies bewahrt Output und Protokoll ohne
Suppressions. Die UDS-Änderung macht die bestehende Socket-Trust-Boundary im
Go-Typvertrag explizit und bewahrt dabei Binary-Frame- und Full-Write-Semantik.

## Akzeptanzkriterien

Unsichere Output-Roots scheitern vor Zustandsänderungen, legitime private Roots
bleiben gültig, Engine-Callbacks behalten den Request-Context, eine
Header-Rejection emittiert nur das feste Response-Literal, UDS-Frames werden
nur über die lokale Engine-Connection gesendet und der exakte PR-Head muss null
New Issues, Duplikatzeilen und CodeQL-Alerts haben.

## Geänderte Dateien

`runtime_smoke.py`, `runtime_native_smoke.py`, native Middleware-Go-Quellen und
Tests, `traefik_engine_service.c`, direkte Python-Tests sowie dieses gepaarte
Record/Index änderten sich; keine andere Repository-Grenze änderte sich.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `python3 -m unittest tests.test_traefik_runtime_smoke_security` | bestanden: 6 Tests. |
| `python3 -m unittest tests.test_sonar_reliability_contract` | bestanden: 12 Tests einschließlich des Traefik-C-Source-Contracts. |
| Vollständiger Native-Middleware-Pakettest mit task-eigenem Go-1.26.5-Cache | initial und nach dem UDS-Vertrags-Follow-up bestanden, mit einem kurzen task-eigenen Unix-Socket-Temp-Pfad. |
| `make check-remaining-connectors-c17-lint` | bestanden. |
| Traefik-Common-Adoption- und C-Standard-Wiring-Checks | bestanden. |
| `TestWriteUDSConnectionFrameUsesDuplexConnection` | bestanden gegen ein echtes In-Memory-`net.Conn`-Paar. |
| Go-1.26.5-Task-Cache: `FuzzUDSFrameAndResult` für 15 Sekunden | bestanden: 95.482 Ausführungen, kein neuer interessanter Input. |
| `git diff --check` | bestanden; erneute Ausführung vor Delivery erforderlich. |
| Vollständiger Host-Lifecycle und gelinkter C17-Engine-Build | nicht ausgeführt / blockiert: Die Sandbox stellt die nötigen libmodsecurity-Entwicklungsheader/-Library nicht bereit. |

## Security-Auswirkung

Die Output-Root-Änderungen begrenzen Pfade vor rekursivem Löschen, Plugin-Kopie,
Evidence-Erzeugung und Builds; private legitime Roots bleiben zulässig. Die
neue Rejection-Regression beweist, dass ein feindlicher Request-Header-Wert
nicht in den von der Middleware erzeugten Denial-Body reflektiert wird, während
die Context-Regression den Request-Scope in Engine-Callbacks beweist. Der
CodeQL-Reflected-XSS-Kandidat wurde von einem Request-Header über generischen
UDS-Writer-Dispatch bis zum Response-Sink verfolgt. Der produktive Austausch
akzeptiert jetzt nur `net.Conn`, während der generische Byte-Buffer-Writer
test-only bleibt. Der fokussierte Duplex-Test beweist, dass legitimes
Local-Engine-Framing Opcode und Payload weiter bewahrt; vollständiger Paket-
und Parser-Fuzz-Control bestehen ebenfalls. Der Kandidat wird weder verworfen
noch suppressed: Eine frische Hosted-CodeQL-Analyse des neuen exakten Heads
muss zeigen, dass der Source-to-Sink-Pfad fehlt. Es werden keine Host-Runtime,
CI, Review, Sonar-Reanalyse, PR-Delivery oder Merge behauptet.

## Runtime-Evidence

Fokussierte Controls liefern nur Source-Level-Evidence; kein Host-Runtime-
Ergebnis wird behauptet, weil die nötigen lokalen Voraussetzungen fehlen.

## Bekannte Einschränkungen

Der vollständige Host-Lifecycle und der gelinkte C17-Engine-Build benötigen
libmodsecurity-Entwicklungsheader/-Library, die in dieser Sandbox fehlen.

## Verbleibende Risiken

Der vorherige exakte Head hat ein SonarQube-Cloud-Quality-Gate `OK` mit null
offenen New Issues und null New-Code-Duplikatzeilen. Dieser UDS-Follow-up
benötigt weiterhin eine frische Exact-Head-SonarQube-Cloud- und CodeQL-Analyse.
Keine Risikoakzeptanz ist dokumentiert.

## Nicht ausgeführte Prüfungen mit Begründung

Der vollständige Host-Lifecycle und der gelinkte C17-Engine-Build benötigen die
fehlenden libmodsecurity-Entwicklungsheader/-Library. Hosted-Exact-Head-
Verifikation einschließlich unabhängiger CodeQL- und SonarQube-Cloud-Analysen
steht bis zum Draft-PR aus.

## Finaler Diff- und Review-Status

Draft-PR [#203](https://github.com/Easton97-Jens/ModSecurity-conector/pull/203)
wurde aus `agent/traefik-sonar-remediation-20260730` eröffnet; sein initialer
Implementierungscommit war `e5fa1aa8f69fe9d088b661eba80b296bc845870a`. Der
Branch-Head vor dem UDS-Vertrags-Follow-up war
`4a9fb8175e0f07ad9f876c159420da0b817e57e4`. Hosted-Review, frische
Exact-Head-Checks, SonarQube-Cloud-Reanalyse und CodeQL-Reanalyse stehen aus;
kein Merge und keine `master`-Änderung werden behauptet.
