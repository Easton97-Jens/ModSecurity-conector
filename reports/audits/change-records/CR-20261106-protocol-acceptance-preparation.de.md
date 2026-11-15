# Change Record: CR-20261106-protocol-acceptance-preparation

**Sprache:** [English](CR-20261106-protocol-acceptance-preparation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261106-protocol-acceptance-preparation |
| Datum (UTC) | 2026-11-06 |
| Basis-Revision | `a5f697c35acb5386d2037f91dfed10ad4b469cd9` |
| Parent zu Follow-up-Beginn | `adf75d05ced37ccab066b8608aed1ce297be84e3` |
| Framework zu Follow-up-Beginn | `b5d8d9442d7751c04ee84f478f594fc84a236e3b` |
| Lieferung | [Parent-Draft-PR #445](https://github.com/Easton97-Jens/ModSecurity-conector/pull/445), [Framework-Draft-PR #169](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/169) |

## Motivation und Problemstellung

Abnahmevorbereitungsfehler durch echte Hostnachweise schließen, vorhandene
Regressionen und 100 Standardfälle erhalten und das korrigierte Framework über
konsistente native Pins/Projektionen auswählen. Die Fortsetzung erlaubt
nachgewiesene Produkt- und Abhängigkeitskorrekturen. Die Gesamtabnahme bleibt NOT_RUN.

## Akzeptanzkriterien

Die vier erhaltenen H2-Regressionen benötigen ursächlichen Vorher-/Nachher-
Nachweis; Apache-, lokale HTX-, SPOP/HTX-Companion- und ext_proc-H2-Pfade
benötigen ausführbare unabhängige Leser. Gezielte Läufe am finalen Commitpaar,
frisches Apache-CRS und Aggregate, aktuelle gehostete Checks, native Policy/
Inheritance sowie Integrität/Cleanup sind vor READY_FOR_FULL_ACCEPTANCE
abzugleichen. Kandidatennachweise allein erfüllen die finalen Lieferkriterien nicht.

## Implementierungsentscheidung und Begründung

NGINXs eingereihter H2-Reset wartete bei weiter aktivem Peer auf einen nicht
geplanten Schreibpfad der echten Verbindung. Das Framework versioniert einen
minimalen nativen Quellpatch ohne Fuzz und bindet ihn in Buildcache/Provenienz.
Ein unabhängiges TLS/H2-Frameexperiment trennt Serverqueueing von Client-
Verarbeitung. Bestehende Assertions und Timeouts bleiben unverändert.

Apaches H2-Strict-Pfad markierte die sekundäre Verbindung als abgebrochen,
ohne terminale Metadaten über ihre native Verbindungsausgabekette zu senden.
Ein gehaltener Peer und eine unabhängige Frameprobe belegten den fehlenden
Reset. Die begrenzte Korrektur sendet ERROR/FLUSH-Metadaten vor dem Abbruchflag
über diese Kette; der versiegelte Request-Producer-Guard und das bisherige
HTTP/1-Verhalten bleiben erhalten. Die native Beam-Verarbeitung des gepinnten
HTTPD übernimmt Metadatenkopie zwischen Threads und Streamreset.

Eine gehärtete Wiederholung zeigte nach dem Reset zusätzlich ein Purge-Rennen
im gepinnten HTTPD. Eine native APR-Interleavingkontrolle belegt, dass weder der
Originalpfad noch Wakeup allein den abgeschlossenen Stream zeitnah bereinigen.
Das Framework versioniert die zweiteilige Wakeup-/Pending-Purge-Korrektur am
sicheren äußeren Cleanuppunkt, erhält Shutdown-/Abort-Priorität und bindet die
Patchbytes in Apaches native Cacheidentität. Frischer Build und finaler echter
Cleanupnachweis bleiben erforderlich.

Envoy ext_proc Strict sendet nun eine späte ImmediateResponse über den
angehefteten Host. Im gemeinsamen Profilregister ändert sich nur das
Strict-Aktionsbit dieses Profils. Der Dienst erfasst erfolgreichen gRPC-Send
getrennt vom tatsächlichen Downstreamreset; ausgewählte native Envoy-Client-/
Accessnachweise belegen Targetstream und gesunden Peer/Folgezugriff. Die
Runtimekonfiguration akzeptiert explizit off/safe/strict. Das ext_authz-
Basisprofil erbt diese Aussage nicht.

Der native Framework-Synchronisierer besitzt Parent-Gitlink/Lock/Workflow-
Projektionen. MRTS bleibt `ee2174431c4edf97e66afe32558ce8454deb2397`;
geschützte Provenienz-, Python-/Go- und sonstige Toolchainpins bleiben unverändert.
Es erfolgt kein Merge.

Die geprüfte ignorierte lokale LLM-Notiz bleibt byteidentisch archiviert und
als lokales nicht normatives Material klassifiziert. Die 27 Parent-,
21 Framework- und 12 MRTS-Policydigests bleiben unverändert. Die getrennten
84 Legacyinventarbefunde bleiben sichtbar; kein ungeprüfter Digestrefresh
beseitigt sie.

## Geänderte Dateien

- Ausgewählter Framework-Gitlink, zentrale Versionslockdatei und 22 native Workflowprojektionen.
- Apaches terminaler H2-Metadatenversand, profilbezogene Capabilities und gepaarter Guide.
- Envoy-ext_proc-Prozessor, exakte Profilzulassung, Runtimekonfigurationsmaterialisierung,
  profilbezogene Capabilitymetadaten und gepaarte Source-/Connectorguides.
- Generierte Konfigurationsreferenz über ihren Framework-eigenen Generator.
- Dieses Change-Record-Paar; lokale Pläne und externe Nachweise werden nicht committet.

## Ausgeführte Befehle

Befehle verwenden RTK und explizite ausgewählte Parent-/Frameworkwurzeln und
Revisionen. Exakte Befehle, vollständige Ausgaben, Laufidentitäten und absolute
Nachweispfade stehen im externen Follow-up-Bericht.

| Verfahren | Beobachtetes Ergebnis |
| --- | --- |
| Vier unveränderte H2-Regressionen am Startpaar | 4 FAIL als Vorher-Nachweis erhalten |
| Unabhängige verifizierte TLS/H2-Frameprobes ohne/mit PING | Serverqueueing bewiesen; Reset ohne PING vorher etwa 12 s, nachher etwa 15 ms |
| Frische gepatchte native H2/H3-Builds | PASS; vier Regressionen und acht Nachbarn in gezielten Kandidatenläufen PASS |
| Envoy-Go-Suites ohne Tags und mit echtem libmodsecurity-Tag | Jeweils alle acht Pakete PASS |
| Echte Envoy-H2-Kandidatenfälle | 8 PASS / 24 Transaktionen; natives Targetcleanup vor Peerfreigabe |
| Echte lokale HTX-H2-Kandidatenfälle | 8 PASS; Writerfehler-Cleanup und Negativkontrollen PASS |
| Echte SPOP/HTX-Companion-H2-Kandidatenfälle | 8 PASS; originale Owner-EOS-Regel und native Streamaktion ohne erfundene MRC1-Felder verknüpft |
| Profilmetadatenverträge | 39 Tests PASS |
| Frischer Apache-Build, CRS und Aggregate | Finale native Ergebnisse im Follow-up-Bericht; nicht aus Failure-Artefaktupload abgeleitet |
| Finale Pins, Policy/Inheritance, Units/Generatoren und aktuelle CI | Erforderlicher finaler Readback extern erhalten |

## Security-Auswirkung

Strict bleibt auf ausgewähltes Profil und tatsächliche Hostaktion begrenzt.
Originale Engineentscheidungen, erfolgreiche Service-Sends und Wirebeobachtungen
bleiben getrennt. TLS-Verifikation, Nachweisgrenzen, Quellenzulassung, UDS-
Ownership, Prozessisolation, Compilerwarnungen, Scannerumfang und Gateregeln
bleiben erhalten. Keine administrativen Regeländerungen, lokale Sonareinrichtung/
Scans oder MRTS-Schreibzugriffe.

## Runtime-Evidence

Der frühere versiegelte 21-PASS/4-FAIL-Nachweis bleibt unverändert. Die neue
Follow-up-Wurzel erhält Baselinereproduktion, native Patch-/Buildidentitäten,
unabhängige Framebeweise, profilbezogene Access-/Common-/Cleanup-Beobachtungen,
Apache-Fehlerdiagnosen und frische Buildreceipts. Finale Quellpaarhashes, Zahlen,
Cleanup, CI und Integritätsmanifest stehen im externen Bericht statt eines
selbstreferenziellen Commit-SHA in diesem versionierten Record.

## Bekannte Einschränkungen

Ext_authz, ForwardAuth und native Profile bleiben getrennte Aussagen. Die
aktuelle SPOP-NOTIFY-ABI benötigt explizite Null-Content-Length für diese leere
H2-Bodyfixture; weitergeleitete Regelmetadaten werden nicht erfunden. Moderne/
Strict-Traefik-Pfade benötigen eigene Qualifizierung. Stock-/Patched-lighttpd
behalten ihren H1-Vertrag.

## Verbleibende Risiken

Aktuelle erforderliche gehostete Sonarbewertungen und Gateergebnisse müssen
am exakten gelieferten Frameworkhead gelesen werden. Einzelne lokale Prüfungen
ändern keine Serverbewertung. Bestehende unabhängige C++20-/C++23-Advisoryfehler
und 84 Legacybefunde bleiben getrennt von neuen Regressionen sichtbar.

## Nicht ausgeführte Prüfungen mit Begründung

Die Gesamtabnahme bleibt auf Benutzeranweisung NOT_RUN. Kein Merge, keine
administrativen Änderungen, lokale Sonarinstallation/Start/Authentifizierung/
Scans oder MRTS-Mutation. Dieser Quellrecord begründet keine globale Bereitschaft.

## Finaler Diff- und Review-Status

Gezielte normale Commits setzen die bestehenden Draft-PRs fort. Die finale
Prüfung kontrolliert Produktumfang, generierte Pins/Referenzausgaben, unveränderte
Standardauswahl, geschützte Pins und Policylösung. Tatsächliche finale volle SHAs,
terminale CI und Anforderungsbewertungen stehen im abgeglichenen externen Bericht.
