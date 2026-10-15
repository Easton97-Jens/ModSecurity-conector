# PR #382 / #410: aktuelle I12-Host-Evidenz, 2026-10-13

**Sprache:** [English](pr-382-i12-host-evidence-20261013.md) | Deutsch

**I12_PARTIAL.** Echte isolierte Hosts wurden erneut ausgeführt; kein
Pflichtteil hat vollständige I12-/V08–V10-Abnahme. Aktuelle Beobachtungen,
Fehlversuche und fehlende Anforderungen bleiben unabhängig vom
[historischen Bericht](pr-382-i12-host-evidence-20261011.de.md) erhalten.
I12 und V08–V10 bleiben offen; beide bestehenden PRs bleiben Draft.

## Quell- und Evidence-Identität

Der Task-Run ist
`/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion`
(unten `RUN`). Die Dateien sind lokal erhaltene Artefakte, keine öffentlichen
Downloadlinks. Der alte Run `20261011T063350Z-0df51024008f-i12` wurde erneut
gehasht: Alle 85.108 Einträge stimmen mit dem Originalmanifest
`6672a248716967976992b1d972207c2ad26f51cf2e471f9ccfcacb1e0ed8d124` überein.
Seine 79 ausgewählten Records bleiben 9 PASS, 6 FAIL, 53 BLOCKED und
11 NOT_EXECUTED. Die historischen Statuswerte wurden nicht verändert.

| Identität | Tatsächlicher Scope |
| --- | --- |
| Ausgangs-Parent | `8c574cdf86f10af976297c31d31485b042eba73b` |
| Final veröffentlichter Parent | `a9d48bb58aa948aea7d79e20cdf09d3f239b7808`; tatsächliche HAProxy-e2445-/Envoy6175Runidentitäten samt begrenztem Quellgleichheitsbeleg unten |
| Frühere Kampagnenhostinputs | Echter Snapshot `5939dce7a4cb3572b0244c159e4f98d0b1c28040`; Patched-/Kontrollinputs sind echt `b982c6f35abc47eccddcfded2bfd920f92516d90` |
| Ursprünglicher Native-/Bridge-Buildproducer | `8c574cdf86f10af976297c31d31485b042eba73b`; in jedem Artefaktmanifest erhalten |
| Framework | `99a7985c1be92a2297b1b59208f64df6768f2cbf`; Quellen und Gitlink unverändert |
| MRTS | `8a6bb546c4c81d8ffc7be801dceac60c6925685f`; gepinnt, nicht ausgeführt oder verändert |
| Ausgangs-/aktueller master | `6aae115fff8531eb1e08a4b10745d7ae93550124`; keine Integration |
| libModSecurity | 3.0.14, SHA256 `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407`; Library-Quellcommit nicht verfügbar |
| Hosts | Apache 2.4.66; NGINX 1.31.6; HAProxy 3.2.25; Envoy 1.39.1; Traefik 3.7.13; lighttpd 1.4.85 |
| Toolchain | GCC/G++ 15.2.0; Make 4.4.1; Go 1.27.2; Task-Python 3.14.7 / PyYAML 6.0.3 |

`parent-final-product-equivalence.json`, SHA256
`3adab3818e1b4f5051e4f9ead4cdf3f1061a6473f7963cfe2d2dd9eb7c0c365c`,
prüft 531 ausgewählte Produkt-/Runtime-Gitobjekte zwischen Runtime5939 und
dffac. Nur Tests und Dokumentation unterscheiden sich. Der Receipt erhält
die ursprüngliche Runidentität; er etikettiert keinen Run um und beweist kein
Hostverhalten. Nach den späteren Common-/HAProxy-Runtimekorrekturen belegt
dieser Receipt keine Gesamtgleichheit mit der finalen Quelle. Alle älteren
Runs behalten ihre tatsächlichen Quell-/Buildidentitäten. HAProxy und Envoy
wurden wirklich aus e2445 beziehungsweise 6175 neu gebaut; begrenzte Input-
Gleichheitsbelege zu finalem a9 stehen unten. Blockierte Hostsetups und andere
begrenzte Beobachtungen behalten ihre Originalrevision und werden nicht zur
Abnahme des finalen Heads aufgewertet.

## Pflichtmatrix und Zählregeln

Vor Hoststarts wurden Capabilities, versionierte Framework-Fixtures, native
Operationen sowie explizite historische/Benutzerpflichten für H1 ausgewählt.
`case-catalog/selected-01/selection.json` erhält **1.406 Pflichtanforderungen**
und **78 diagnostische Anforderungen** mit allen Ausschlüssen und Gründen.
Das sind Anforderungs-IDs, keine HTTP-Requestzahl. Runner-Probes, Readiness,
Komponententests und Wiederholungen sind nicht automatisch qualifizierte
kanonische Fälle. `final-reconciliation/` erhält jede ausgewählte ID und die
tatsächlichen Runnerbeobachtungen separat. Fehlende native Zähler,
Backend-Ledger, kausale Zuordnung und Transportbeobachtungen bleiben `null`
mit Begründung.

| Pflichtteil | Anforderungen | Neue echte Hostprüfung | Vollständige Abnahme |
| --- | ---: | --- | --- |
| `apache-native` | 155 | 27 begrenzte Transaktionen; korrigierter Recovery-Rerun | PARTIAL; Lifecycle-/MIME-/EOS-Beleg und 128 weitere Anforderungen fehlen |
| `nginx-native` | 140 | Zwei erhaltene 60-Fall-Batches stoppen vor Host-/Clientausführung | BLOCKED_ENVIRONMENT; Ownership-/Traversal-Voraussetzung |
| `haproxy-native-htx` | 112 | Acht echt neu gebaute e2445-HTX-Probes bestehen | PARTIAL; vollständige unabhängige Lifecycle-/Framing-/Sinkmatrix fehlt |
| `haproxy-spop-request` | 94 | 51 unvollständige Request-Fixture-Fälle; sechs Combined-Probes | PARTIAL; unvollständige Fixture und echter Companionnachweis getrennt |
| `haproxy-spop-htx-response-companion` | 72 | Sechs echt neu gebaute e2445-Combined-Probes bestehen; alte Fehler erhalten | PARTIAL; begrenztes Ergebnis ersetzt vollständigen Lifecycle-/Transportbeleg nicht |
| `envoy-ext-proc` | 117 | Zehn unterschiedliche Funktionsprobes und zwei Transportdiagnosen | PARTIAL; vollständige Backend-/Native-Cleanup-Zähler fehlen |
| `envoy-ext-authz-request` | 94 | Zwei echte Allow-/Deny-Probes | PARTIAL; vollständige Hostbuffer-/Native-Limit-/Ledgermatrix fehlt |
| `envoy-ext-authz-response-companion` | 73 | Zwei separate P3-/P4-Companionprobes | PARTIAL; Strict/Reentry/Lease und vollständiger Lifecycle fehlen |
| `traefik-native-uds` | 118 | Kein aktueller Host gestartet | BLOCKED_ENVIRONMENT; Compiler-Unterprozess und schreibbares Pluginstaging |
| `traefik-forwardauth-request` | 93 | Kein aktueller Host gestartet | BLOCKED_ENVIRONMENT; versioniertes Observersetup benötigt Go |
| `traefik-forwardauth-response-companion` | 69 | Kein aktueller Host gestartet | BLOCKED_ENVIRONMENT; versioniertes Observersetup benötigt Go |
| `lighttpd-stock-sidecar` | 153 | Sieben finale echte Hostfälle, acht zusätzliche Profilcontrols, 17 separate Komponentenchecks | PARTIAL; vollständige Producer-Provenienz und physische Lifecycle-Zähler fehlen |
| `lighttpd-patched-native` | 116 | Zwei echte P1-Kompatibilitätscontrols | PARTIAL; vollständiger Namespace-Launcher/P2-Konfiguration blockiert |
| Diagnose `lighttpd-stock-native-control` | 78 | Zwei echte P1-Controls mit echtem Stock-kompatiblem Modul | Separate PARTIAL-Diagnose; keine Native-Body-Hook-Behauptung |

Kein Pflichtteil ist vollständig PASS. Alle fehlenden IDs und Gründe stehen
im [generierten Missing-Case-Index](pr-382-i12-missing-case-index-20261013.de.md)
und `final-reconciliation/requirements.json`.
Raw-Runnerexits und ihre engeren PASS-Zähler stehen unten; sie ändern weder
den Nenner noch ersetzen sie fehlende Beobachtungen.

Der versiegelte Abgleich erhält 123 unterschiedliche Runner-Fixture-IDs ohne
Retries, Readiness, Follow-ups und gemeinsame Request-/Responseidentitäten.
Semantische Eindeutigkeit bleibt null, weil effektive Fixturegleichheit nicht
belegt ist; die genaue vollständig zugeordnete kanonische Ausführungszahl
bleibt ebenfalls unbekannt. Qualifizierte kanonische PASS-/FAIL-Zähler sind 0/0;
fehlende Qualifikation ergibt 420 BLOCKED_ENVIRONMENT und 1.064
NOT_EXECUTED_UNQUALIFIED. Diese Zahlen behaupten keinen fehlenden tatsächlichen
Verkehr. Das Indexpaar erhält alle 1.484 fehlenden IDs jeweils einmal.
`final-reconciliation/summary.json` hat SHA256
`78e6985a83ba70d4f1dc83dfbcfbba2e459eb192a7b61d69c05bbb016f8ddac6`;
35 Originalquellhashes wurden unabhängig geprüft. `final=true` versiegelt
den Abgleich und bedeutet keine I12-Abnahme.

## Apache und NGINX

Apache-Versuch `1791916326230218540` enthält 27 echte native Transaktionen,
Controller-/Candidate-Exit 0, keine verbliebenen Prozesse/Mounts und ein
beobachtetes `msc_transaction_cleanup`-Enter-/Return-Paar pro Transaktion.
Allow ist 200; P1/P2-Deny 403/Backend 0; P3-Deny 403/Backend 1; Redirect 302;
Safe-Late 200/curl 0; Strict und technische Postcommitfehler erhalten 200
mit curl 18. Physische Closed-FD-/`/dev/full`-Fehler stehen im Original-
Apache-Errorlog. Alle fünf verpflichtenden Sinkfehler liefern technische
500/Backend 0. Der Diagnosewriter scheitert vor der späteren disruptiven
Regel; der alte 403-Oracle war falsch. Keine Produktänderung erforderlich.

Die Response-Limit-Reject-Recovery-Controls lieferten zunächst zehn Bytes
gegen ein natives Acht-Byte-Limit. Ihre berechtigten 403 waren Fixturefehler.
Frischer Versuch `1791916546816730611` verwendet Drei-Byte-Controls: Main
403/Backend 1, Follow-up/Nachbar 200/Backend 1, vollständiges Framing und
saubere Beendigung. Die finalen 27 mechanischen Controls stimmen; alle 27
bleiben für vollständige Lifecycle-Abnahme BLOCKED, weil Common-Finish,
physischer EOS und MIME-Beobachtungen fehlen.
`apache-current-host-v2/summary.json` hat SHA256
`fcaf4dda8482b6d7378de78632d42da12ac71a425ca69fb99c0dee5352ada791`;
das unveränderte Apache-Modul hat SHA256
`908c9e7a7062ada3e36499a69e2c41e17791a36021d5872d0981bfc5864bb5d0`.

NGINXs aktuelle Binary-/Modulprovenienz ist belegt; lokale Hostabnahme bleibt
blockiert. Versuch `1791916064021781516` markiert alle 60 Operationen
NOT_EXECUTABLE, weil der Spec den Harness außerhalb `BUILD_ROOT` ablegte.
Korrigierter Versuch `1791916436174006544` erreicht den Harness, scheitert
jedoch vor HTTP/Configtest an der Worker-Verzeichnisvorbereitung:
`chown nobody`, danach `chmod` unter der zugelassenen
CHOWN-/SETUID-/SETGID-Maske `0xc1`. Letzteres liefert EPERM; privater
Ancestor-Traversal ist ebenfalls nicht möglich. Dies sind Setupfehler,
keine beobachteten Produkt-FAILs. Beide Versuche haben sauberes Outside-
Cleanup. Die erforderliche Root-/nobody-Umgebung muss den versionierten
Ownership-/Traversalvertrag erfüllen; zusätzliche Capabilities wurden nicht
erteilt. Historische R16/R17 und Hosted-CI bleiben getrennte Evidenzscopes.
NGINX-Binary-SHA256:
`b39012fa2158408c55d8506ac1b1254fc712dd471a6137e64264fa42a0504384`;
Modul-SHA256:
`8c807a5ff55d93af63542050928e0158f2c8ec965bb46dba8ec232935f552efe`.

## HAProxy

Direkter HTX-Versuch `1791916380864162400` beobachtet acht erwartete
Funktionsergebnisse, darunter leere Request-/Response-EOS-Controls und
synchronisiertes P4-Safe/log_only. Vollständige physische API-/Destruktor-/
Framing- und Pflichtfallevidenz fehlt. Die ursprüngliche SPOP-Only-Fixture
führt 51 Zeilen aus: 42 Driverexits 0, neun Exits 1. Die neun erwarteten
Allow-Controls erhalten 503, weil der verpflichtende Response-Companion
fehlt. Die unvollständige Fixture wird weder promoted noch als Produktbug
ausgegeben.

Der Combined-Runner akzeptiert vorbereitete Binaries jetzt nur als explizites
Paar mit tatsächlichen Binary-/Libraryhashes, Version und aktuellem
Produktquell-Objektbeleg. Der ursprüngliche Buildweg bleibt verfügbar.
17 fokussierte Tests, Shellsyntax und Diffchecks bestehen. Versuch
`1791917296154368188` führt sechs Combined-Probes/sieben HTTP-Requests mit
Controller-/Driver-Exit 0 und sauberer Beendigung aus. Der alte HTTP-only-PASS
übersah echte Fehler: P3-Deny403 scheitert danach an der Outcomebestätigung;
P4-Safe200 und Verbindungsreuse scheitern beim Terminal-Cleanup, mit physischen
Connector-/Protokollfehlern. Diese Originalbeobachtungen bleiben unverändert.
Diagnose, Reparatur und Hostretest mit neu gebauten Binaries werden unten
bei finaler Revision/Evidenz festgehalten.
`hosts-haproxy-prepared-01/SHA256SUMS` hat SHA256
`f593c9ee648eee9e2f9bb27aeeeddacc00156fe9da0f8cd15a1750a428af36e2`;
alle 2.045 Einträge wurden geprüft.

Native Terminal-Outcome-, P3-Abschluss- und SPOP-Phasenkonvertierungsfehler wurden
reproduziert und korrigiert. Commit `a30fd5e414b35b990355e04fda148dfae7514c21`
erlaubt die tatsächliche Host-OUTCOME-Meldung nach gültigen nativen terminalen
Policyentscheidungen; technische und Loggingfehler bleiben erhalten. Sein
Retest mit echt neu gebauten Binaries `1791918602525320691` besteht acht direkte
HTX-Controls und stoppt dann bei verbliebenem P3-SPOP-`connector_error`; der
Fehlversuch bleibt erhalten. Erfolgreiches P3-Cleanup rief typed CANCEL auf,
weil reguläres RELEASE bisher P4-EOS verlangte.
Common-Abschlusscommit `6175a30d94de66f349c11eb8164b28942e040457` erlaubt das bestehende
MRC1-RELEASE nach bestätigtem passenden disruptiven Precommit-P3-OUTCOME;
HTX führt jetzt OUTCOME→RELEASE→close aus. EOS wird nicht erfunden. Allow/
log_only, unpassende Outcomes und technische Cancellation bleiben geprüft.
Echte native Client-/Servertests und vier Mutationskontrollen, drei Callerchecks,
sechs Buildcontracts und 18 Response-Handle-Checks bestehen. Der Compilerprefix
besteht zusätzlich mit `CC='env cc'`. Native-Validation-Receipt-SHA256:
`73ccabd26af1514570e9f7327812e71c825be858067aed5ce9a47599bf6d2454`.

Sein echt neu gebauter Versuch `1791920706986259057` besteht erneut acht
direkte Controls, scheitert aber beim Combined-P3-Cleanup: Die produktive
SPOP-Konvertierung setzt die native Entscheidungsphase auf Common CONNECTION
zurück. Der RELEASEguard lehnt die fehlenden P3-Metadaten korrekt ab. Finaler
Commit `e2445c781eded55e006f114e981ef841872eb74e` bildet native Phasen nach
Allow-/Deny-/Redirect-Konstruktoren explizit auf benannte Common-Phasen ab.
Der Guard bleibt unverändert. Die sechs produktiven P3/P4-Entscheidungsvarianten
und alle neun Bindingtests bestehen; Auslassungs-/Castmutationen kompilieren
und scheitern dann an der Phasenassertion. Echter C17-/`-Werror`-SPOP-Build
besteht. Receipt-SHA256:
`2e197b9168aacb8e164771b3eae7e0954ffa1cd53f8f908f7c4e91b25813c6f3`.
Alle 12.080 Artefakthashes des fehlgeschlagenen 6175-Runs sind geprüft; Manifest
`7ac95c5fc3208b4becc301d0c7814eec530a4e84e08c355d319bcc884920d5ab`.

Finale echte e2445-SPOP-/HTX-Builds enden beide mit Exit 0. Regulärer Versuch
`1791921462735406083` besteht acht direkte HTX- und sechs Combined-Probes;
separater expliziter ResponseBodyLimit10/Reject-Versuch `1791921552453068894`
besteht sechs Combined-Variantenprobes. Nach Dienstende gibt es keine normalen
physischen Connector-/Protokollfehler; die Missing-Correlation-Negativkontrolle
bleibt erhalten. Beide Controller bestätigen keine verbliebenen Prozesse oder
Outside-Mounts. P4 der Native-Limit-Variante beobachtet requested deny/actual
log_only, Client200/vollständige 23 Bytes; nativer Rawlimit-/APIreturn und kausale
Rule-ID bleiben null. Die sechs Konfigurationsvarianten sind separate
Beobachtungen, keine sechs zusätzlich qualifizierten Anforderungen.
HTX-Binary-SHA256:
`e04d068da23906adf68b9f52019db7be4e8051d6cf10ca9e2ecd080fea17cc20`;
SPOP-Binary-SHA256:
`030f667437964be54655637c7f35751342911efe8cdc2c2da167432e665a30f1`.
Alle 12.247 Artefakthashes stimmen mit dem Manifest
`86073b3fd2ab27d23d75c0c99d756b52e260d147d5995e8c5f8c5ec4fa224e53` überein.
Pakete stehen unter `hosts-haproxy-postfix-01/retry-03/`; native physische API-/
EOS-/Destruktorzähler und unabhängige numerische Clientexitreceipts fehlen
weiterhin für vollständige I12-Abnahme.

## Envoy und Traefik

Envoy ext_procs ursprünglicher Body-Limit-Oracle erwartete 413. Tatsächliche
native Engineentscheidung und Host liefern für die explizite Reject-Fixture
403; die native CGo-Regression bestätigt dies unabhängig. Nur der Oracle
wurde korrigiert. Frischer Versuch `1791916687448257248` besteht zehn
Funktionsprobes: Streamed-Allow, P1/P2/Native-Limit-Deny, P3-Deny/Redirect,
P4-Only und synchronisierte Safe-Late-Response mit Recovery. Zwei Cancel-/
Recovery-Diagnosen bleiben eng begrenzt; Cancellation-Zuordnung ist
`grpc_context_canceled_unattributed`, kein unabhängig belegter Strict-Abbruch.

Request-only-ext_authz-Versuch `1791916573908703091` beobachtet Allow200/Deny403.
Combined-Versuch `1791916466421772127` beobachtet separat P3-Deny403 und
P4-Safe200/log_only. Die leere tatsächliche Aktion im nativen Requestevent
bleibt erhalten; der Client sieht unabhängig 403. Fehlende native Zähler/
vollständige Backend-Ledger und Strict-/Reentry-/Leasefälle halten alle drei
Teile partiell. `hosts-envoy-traefik-01/SHA256SUMS` hat SHA256
`d79696f7df3916d375659668b6722ee2f3d1d39ef065cb84e422ccdd2df28aa6`;
alle 2.010 Einträge wurden geprüft.

Alle drei Envoy-Teile wurden echt aus
`6175a30d94de66f349c11eb8164b28942e040457` neu gebaut und tatsächlich erneut
ausgeführt: Request `1791920841266999968`, Companion `1791920756422928567`,
ext_proc `1791920898020674821`. Alle begrenzten Runner-/Controllerergebnisse
sind Exit 0 mit UID/GID 65534, Capabilities 0 und unabhängig sauberem Outside-
Cleanup. 14 unterschiedliche Funktionsprobes plus zwei Diagnosen bestehen;
wiederholte Request-/Readinesscontrols werden nicht addiert. Beide Builds
kompilieren tatsächlich alle 63 gemeinsamen Common-C-Dateien samt geänderten
MRC1-Dateien. Neue Binaryhashes: ext_authz
`67a93560bf30f9e0197fb25addc956bbcc282d71b9ebb6da15a8eb0463b5a9b2`,
Response-Observer `e21535607f739a8346d513541c05146bb769680332d600d3bb3fa000c583936d`,
ext_proc `67f0f832f76fb68abb1489c9e27ecf9770841b0f3911e767a3a441fc42675b13`.
Alle 4.005 Abnahmeartefakthashes sind geprüft; Manifest
`53d5b3d458007f01a2ac2105dc2c78e946210bf14cf88da65f052adac0eedef7`.
Der spätere e2445Fix ändert produktiv nur HAProxy. Der begrenzte Vergleich
von 172 Envoy-Buildinput-Gitobjekten ist gleich; Receipt-SHA256
`da0fd519cc921568b1bc04cc02746a246b4c0f0f09bed1b67506fabafed7b4dc`.
Tatsächliche Build-/Runidentitäten bleiben 6175; Gesamt-Parent-Gleichheit oder
fehlende Lifecycle-/Strictnachweise werden daraus nicht abgeleitet.

Traefik-Native-Versuch `1791916290959447432` stoppt beim versionierten
Engine-Rebuild, weil `cc1` im festen Namespace fehlt. Read-only-Pluginstaging
verursacht außerdem einen ausdrücklich fehlgeschlagenen lokalen Cleanup-
Receipt. Kein Traefik-Host startet; Outside-Cleanup ist unabhängig sauber.
ForwardAuth-Request `1791916630354113595` und Response `1791916513884787401`
stoppen jeweils vor Hoststart, weil das versionierte Response-Observer-Setup
die Go-Toolchain benötigt. Dies sind separate Umgebungsblockaden. 18 echte
C-/UDS-Komponentensubcases mit Race-Detector und EOS-Verlustmutation sind
separate Belege; sie reproduzieren oder löschen den historischen realen
Host-`protocol_error` nicht.

## lighttpd

Finaler Stock-Versuch `1791916820945011803` besteht sieben echte Hostfälle:
Full-/Empty-Allow200, P1-Deny451, P2-Deny418, natives P2-Limit403, P3-Deny422
und P4-Safe200/log_only. Tatsächliche Clientbytes/Hash/Framing, unabhängige
Stock-Zugriffszähler, physische Events derselben Transaktion und beendete
Listenerprozesse bleiben erhalten. Ursprünglich leere `actual_action` vor
Hostbeobachtung bleibt gültig; ein separates beobachtetes Event ist Pflicht.
Historische Enumablehnung, falscher 413-/Native-Limit-Eventoracle, Safe-
Eventidentität und Snapshot angenommener Requestbytes sind im Harness
korrigiert, ohne eine Aktion zu erfinden. 28 Harnesstests bestehen mit einem
expliziten Native-SDK-Skip; 17 separat ausgeführte native Nonroot-Komponenten-
regressionen bestehen ohne Skips. Acht zusätzliche echte Profil-/Native-
Reject-/ProcessPartial-Controls bestehen. Stricts logisches
HARD_ABORT_AFTER_200 wird nicht zum physischen Abort promoted: Der Client
erhielt den vollständigen 200-Body, unabhängiger TCP-Abortbeleg ist null.
Dem Fullproducer fehlen weiterhin der unveränderte Stock-Host-Provenienzvertrag
und physische EOS-/Destruktorzähler.
`stock-current-host-01/final-report.json` hat SHA256
`27e4657f1087d679cf7885fa35223df6b0dc8b7608796711426b33b69b1d0f80`;
`HANDOFF.json` hat SHA256
`ef8736fce9b254b29e61917bd3a96d625c367b4121964ab17c842e8751d8c7a0`.

Patched-lighttpds vollständiger unveränderter Namespace-Launcher scheitert
in `1791916879454169505` vor Hoststart mit `unshare` EPERM. Ein separater
P2-Gate lehnt den descriptorgebundenen Pfad `/proc/self/fd/5/events.jsonl`
bei der Konfiguration vor Requests ab. Kompatibilitätsversuch
`1791917197697716188` führt dennoch echte native P1-Allow200/Deny403 mit dem
echten Patched-Modul aus. Body-/Strict-Capability wird daraus nicht abgeleitet.
Echter Stock-Diagnoseversuch `1791917386284085054` besteht unabhängig zwei
P1-Controls mit neu gebautem Stock-kompatiblem Modul, SHA256
`560b541c6808035cb8c137cdfec3a3d430d546eb85dfdd8b7791c7627d32c77b`.
Das Patched-ABI wurde nicht substituiert. Alle Versuche haben sauberes
Outside-Cleanup. `hosts-lighttpd-patched-01/summary.json` hat SHA256
`e8d1761d1b0f21d13fba79c2a6a07bab987d071f430e98f1aa05625ec1a631e8`.

## Validierung und Sicherheitsscope

Beobachtete lokale Checks umfassen `make quick-check` (Exit 0, 181,916 Sekunden),
I09/I10 (Exit 0, 294,683 Sekunden), Common-C17-/Memory-/Flow-/Adapter- und
physische Apache-/SPOP-Sinkcontracts (Exit 0), die echte native Body-Suite mit
14 Methoden, natives Envoy/Traefik und Go/Race/Vet, Mutationen, Workflowlint,
EN/DE, Links, Change Record und Whitespace. Frühere Prerequisitefehlversuche
bleiben unter `verification/`; aktuelle Receipts identifizieren den getesteten
Tree. Finale Prüfungen geänderter Pfade stehen unter
`verification/final-evidence-02/results.json`; Remotechecks des exakten Heads
stehen in den PR-Beschreibungen und dem externen Lieferprotokoll.
Native-/Komponentenchecks belegen nur ihre eigene Ebene.

Auf exakt 6175 endet frisches `make quick-check` mit Exit 0 in 228,719 Sekunden,
die kombinierte I09-/I10-/Native-Body-Suite (jetzt 15 Methoden) mit Exit 0
in 413,912 Sekunden. Der frühere a30-Gesamtlauf scheiterte in Envoy Go am zu
langen Task-TMPDIR für UDS; derselbe unveränderte Test besteht mit kurzem
externem Pfad. Der Fehlversuch bleibt erhalten. Auf e2445 bestehen die
geänderte native SPOP-Suite mit neun Tests und der echte Produktbuild.
Unveränderte Off/Safe/Strict-HTX-Callerassertions und 15 Mutationskontrollen
bestehen nach der zusammengehörigen Helperextraktion in 18,816 Sekunden.
PR410s17 HAProxy-Harnesschecks und 28 Stockchecks bestehen mit einem expliziten
Native-SDK-Setup-Skip; 24 Envoy-Receipt-/Verifierchecks bestehen. Separate echte
Native-Stockchecks haben keinen Skip. Diese Ergebnisse gelten für ihre Ebene.
Der Taskinterpreter ist 3.14.7; das separate Framework-Interpretergate für exakt
3.14.8 wurde lokal nicht verifiziert. Uniterfolge beweisen keine Umgebungsgates.

Finaler a9d48 ist ein Test-Statuswerttabellen-/Change-Record-Folgecommit.
Seine zwei produktiven SPOP-/Mutationschecks bestehen in 16,406 Sekunden.
Die 829 ausgewählten Gitobjekte unter Common/connectors/Makefile/ci/Workflows/
modules sind gegenüber e2445 gleich; `parent-a9-final-input-equivalence.json`
hat SHA256 `1ac6bb430bfd2a4739cad1d3f25e7b07c5dbb6a06621362c0039c26b619bccad`.
Dies erhält echte e2445-/6175Runidentitäten und belegt nur unveränderte
ausgewählte Inputs. Eine unabhängige begrenzte Codegegenprüfung findet keine
konkreten Korrektheitsprobleme in Phasenkorrektur oder Callerextraktion.
Providerreviews bleiben wie unten benannt historisch.

Die spätere Benutzeranweisung begrenzt die Sicherheitstiefe. TAC-Advisory
wurde als `tac1/granted` geprüft; dies gilt nicht als pauschale Deep-Scan-
Freigabe. Kein weiterer Deep-Scan oder Security-Review-Trigger wird verwendet.
Bereits geforderte sanitierte Gitleaks-8.30.1-Evidenz bleibt sichtbar: Aktuelle
Blobs/neue Taskcommits bestehen, der vollständige ursprüngliche PR-Bereich
scheitert an genau zwei historischen Prosa-Treffern. Werte werden nicht
reproduziert, Scannerregeln nicht unterdrückt und Historie nicht umgeschrieben.
Dieses Release-Gate bleibt fehlgeschlagen. Frühere Codex-Reviews beziehen
sich auf `4639f982a8`, nicht den finalen Head; ihre drei Threads sind gelöst,
ein Review des aktuellen Heads wird nicht behauptet.

## Reproduktion, Lieferung und offene Entscheidungen

Runspezifische Specs erhalten exaktes argv/cwd, Quell-/Config-Hashes,
Hostbinaries, UID/GID, Clientexits/Signale, native Rawlogs und Cleanup.
Gemeinsamer Ausführungseinstieg:

```sh
rtk proxy /usr/local/bin/python3 RUN/isolation/private-runtime.py SPEC
```

`RUN` und `SPEC` durch die exakten absoluten Werte ersetzen. Beispielspecs
sind `apache-current-host-v2-retry/host-spec.json`,
`hosts-envoy-traefik-01/envoy-ext-proc-fixed-harness.json`,
`hosts-haproxy-prepared-01/spec.json` und die Dateien aus
`hosts-lighttpd-patched-01/HANDOFF.md`. Originalcontroller-Ergebnisse erhalten
Candidate-/Driverstatus und unabhängig beobachtetes Outside-Cleanup.

Finale HAProxy-Specs: `hosts-haproxy-postfix-01/retry-03/spec.json` und
`response-reject-variant/spec.json`; finale Envoy-Specs:
`hosts-envoy-final-01/authz-request.json`, `authz-response.json` und
`ext-proc.json`. Die generierten Missing-ID-Indexe sind exakte Kopien von
`final-reconciliation/pr-382-i12-missing-case-index-20261013.md` und `.de.md`,
SHA256 `cf707a2ec7c4d154b98de5384806c6dff1501ba564902a82bc07a350a4eb6f80`
und `7b7e0aade918b2c645dd4552aa78a44cc1376b9aa5415419d6fc9c8915e8311a`.
Regenerierung: `rtk proxy python3 RUN/final-reconciliation/reconcile.py`;
Generator-SHA256: `7ba941ff929afd91a84498c8eddfb92c4f70a903aea2c47a7245f95f9f86226e`.
Raw-JSON, Konfigurationen, Builds und privates TLS-Material bleiben außerhalb Git.

Der bestehende #410-Branch erhält alten Head
`511c4ac4515f0e515f68b3bbc38274c5a230d903` in normaler Merge-Ancestry.
Nur begrenzte I12-Harness-/Test-/Evidence-/Dokumentationsänderungen unterscheiden
sich vom aktuellen Parent. Der
[konsolidierte Change Record](../reports/audits/change-records/CR-20261013-pr382-consolidated.de.md)
wird ohne Wiederherstellen redundanter Records ergänzt. Finale Parent-/
Evidence-SHAs, Remote-Gleichheit und aktuelle CI-/Sonar-/Secret-/Review-
Readbacks stehen in den PR-Beschreibungen und dem externen Lieferprotokoll.
PR410 bleibt Draft.

Vollständige Abnahme benötigt erlaubte Umgebungen, welche die unveränderten
NGINX-, Traefik- und Patched-lighttpd-Launchervoraussetzungen erfüllen,
vollständige physische Lifecycle-/Korrelations-/Transportproducer und die
nicht ausgeführten ausgewählten Anforderungen. Historische Secret-Range-
Bereinigung benötigt eine separate explizite Entscheidung. Begrenzte
Smoke-Erfolge oder CI alleine schließen I12 nicht.
