# Prüfmatrix zur Body-Inspection

**Sprache:** [English](body-inspection-review-matrix.md) | Deutsch

Diese Matrix gehört zu [PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407), gestapelt auf #382. I09/#408 und I11/#406 sind in die geprüfte Basis integriert; I10/#409 und die vollständige I12/#410-/V08–V10-Hostabnahme bleiben getrennt. Quellanbindung, ausführbare Contracts, ausgewählte Hostproben und vollständige Protokollabnahme sind unterschiedliche Evidenzschichten. Keine Zeile behauptet eine vollständige I12-Matrix.

## Request- und Response-Routen

Alle Streaming-Zeilen beschreiben den vorhandenen Datenpfad, keine unbegrenzte Hostzustellung oder abgeschlossene HTTP/1–HTTP/3-Abnahme. Jede Richtung verwendet in ihren Inspection-Fixtures ausdrückliche native Direktiven.

| Profil | Request-Pfad und Umfang | Response-Pfad und Umfang | Prüfnachweise und verbleibende Hostarbeit |
| --- | --- | --- | --- |
| Apache native | Native Request-Zufuhr bietet Speicher-/Dateichunks für P2 mit geprüften Zählern und Dateizugriff an. | `connectors/apache/src/msc_filters.c` bietet APR-Brigaden an; natives Reject beendet bei Append und bleibt bis EOS erhalten. Nach Commit versiegelt es die Ausgabe und bricht die tatsächliche Verbindung vor Weitergabe der zurückgewiesenen Brigade ab. | Echte libModSecurity-/APR-Regression: 9 Tests, Exit 0; striktes C17 Exit 0. Echte httpd-/Protokoll-/Commit-Matrix weiterhin not_run; APR-Aufrufernachweis ist kein httpd-Hostlauf. |
| NGINX native | `connectors/nginx/src/ngx_http_modsecurity_access.c` verarbeitet Speicher-/Dateieingaben inkrementell mit Descriptor-/Bereichsprüfungen. | Nativer Bodyfilter erhält native Ergebnisse und einmaliges P4 bei EOS; native Body-Limit-Terminalbehandlung unterscheidet sich von gewöhnlicher Safe-Late-Rule-Behandlung. | Quell-/Contractprüfung; frische vollständige Hostmatrix für Speicher/Dateien und späten Abbruch not_run. |
| HAProxy native HTX | Geliehene HTX-Blöcke erreichen natives P2; keine SPOP-Vollsample-Grenze gilt. | Native HTX-Response-Blöcke und EOS erreichen P4; gemeinsame Terminalentscheidungen steuern Commit. | Ausgewählter echter kombinierter HTX-/SPOP-Companion-Lauf bestanden. Vollständige HTX-Request-/Response-/Protokoll-/Strict-Matrix not_run. |
| HAProxy SPOE/SPOP + Response-Companion | Ein vollständiges, frame-darstellbares Request-Sample. Producer senden `req.body_size` und `http_version=req.ver`; typisierte Gesamtlänge, ausdrückliches Framing und Samplelänge müssen vor P2 übereinstimmen. | Separater nativer HTX-Companion liefert den tatsächlichen Response-Stream; SPOP-Response-Headernachrichten allein liefern keinen Response-Body. | Echter kombinierter HAProxy-3.2.25-Harness und 28 Hostassertions bestanden, einschließlich On/DetectionOnly, großer unvollständiger Samples und kleiner Kontrollen. Unbekanntes/chunked Framing und ungerahmtes HTTP/2 bleiben nicht unterstützt (Kategorie 4); natives HTX ist die vollständige Streaming-Alternative. |
| Envoy ext_proc | Gestreamte Bodynachrichten erreichen Common-Bridge-P2; Nachrichtenkapazität gilt je Nachricht. | Gestreamte Responsenachrichten und EOS erreichen P4; kein kumulatives Connectorbudget. | Quell-/Contracts und echte CGo-/Native-Ausführung von acht Paketen bestanden. Vollständige ext_proc-Host-/Protokoll-/Late-Commit-Matrix not_run. |
| Envoy ext_authz + Observer | Host puffert ein vollständiges Authorization-Sample; `max_request_bytes=4096/33` bleibt Kategorie 3. Partielle/mehrdeutige Metadaten werden vor nativer Transaktions-/Lease-Erstellung abgelehnt. | Unabhängiger Response-Observer liefert MRC1-Response-Chunks und EOS an Common. | Erhaltener Envoy-1.39.1-HTTP/1-Teilnachweis: 14 Fälle und 14 Terminal-Cleanups; neun Verifierfälle LIFECYCLE_ONLY und p4_strict NOT_RUN. Host-413 ohne native Events unterscheidet sich von nativem 403 für ein vollständiges Sample über dem Engine-Limit. Vollständige Matrix not_run. |
| Traefik native UDS middleware | Native Middleware und Engine-UDS-Protokoll bieten inkrementelle Request-Chunks für P2 an. | Inkrementelle Anwendungsresponse-Chunks und EOS laufen über den UDS-Engine-Pfad. | Go/vet, C-Selftest, Protokollruntime und sieben API-Contracts bestanden; echte Common-/UDS-Tests prüfen Enginezustellung jenseits früherer Grenzen. Vollständige Traefik-Host-/Protokoll-/Commit-Matrix not_run. |
| Traefik forwardAuth + Observer | Host puffert Authorization-Request vollständig, `maxBodySize=4096/33` (Kategorie 3); Response-Observer macht Request-Eingang nicht streamend. | Observer liefert Anwendungsresponse unabhängig von der Authorization-Antwort. `maxResponseBodySize=32768` schützt nur Letztere. | Quell-/Contractprüfung; aktuelle vollständige Traefik-Authorization-/Observer-Hostmatrix not_run. Host-Sample-Ablehnung ist kein Nachweis nativer Engine-Limits. |
| lighttpd Stock sidecar | Inkrementeller HTTP-Eingang/natives P2; privater Diskspool mit begrenztem RAM, Replay erst nach nativem Allow. | Inkrementeller Upstream-Eingang/natives P4 mit technischem Fehler-/No-Replay-Terminalverhalten. | 37 ausgeführte Tests: 36 bestanden, ein RST-Delivery-Basisfehler (FU-STOCK-RST-DELIVERY), keine Skips. Vollständige Hostmatrix und Foreign-UID-/Read-only-Mount-Proben not_run/blocked. |
| lighttpd patched native | Validierte native Speicher-/Dateichunks werden inkrementell für P2 angeboten. | Native Response-Chunks/EOS werden für P4 angeboten; Descriptor-/Bereichs-/Scratchprüfungen bleiben. | Quell-/Contractprüfung; vollständige frisch gebaute Patched-Host-/Protokoll-/Commit-Matrix not_run. |

## Entscheidungs-, Abschluss- und Sicherheitsvertrag

Common zeichnet tatsächliche Append-Ergebnisse und native Interventionen auf, schließt P2/P4 einmalig ab, erhält den ersten technischen Fehler und lehnt Wiedereintritt nach Terminalfehler ab. Für Requests zählt `bytes_seen` angebotene Bytes und `bytes_retained` das SDK-eigene Präfix. Request-`bytes_inspected` bleibt null und bedeutet unbekannt/unbelegt, weil Speicherung und erfolgreiches P2/EOS keine Body-Inspection beweisen: Auch `SecRequestBodyAccess Off` kann den Body speichern. Inspection-Aussagen benötigen unabhängige Source-/Runtime-Evidence. Natives Append `0` begründet ProcessPartial-Telemetrie; eine abweichende gespeicherte Länge allein genügt nicht. Für Responses zählt `bytes_inspected` weiterhin angebotene Bytes, nicht das ProcessPartial-Präfix der Engine. Reject/ProcessPartial und DetectionOnly folgen libModSecurity; der Connector leitet weder Limits aus Regeln ab noch schleust er Direktiven ein oder wählt ein Präfix. Off/Safe/Strict sind Host-Response-Behandlungsmodi. Apache darf natives Body-Limit-Reject nicht zu gewöhnlichem Safe-Late-Rule-log_only herabstufen.

DetectionOnly behauptet nicht, dass Response-Reject zu ProcessPartial wird:
Die native Engine kann ein überlaufendes Append ohne disruptives Ergebnis verwerfen.
Tests müssen angebotene Bytes, tatsächlich inspizierten Inhalt und Interventionsergebnis
unterscheiden. Native terminale Phasenfinalisierung vor HTTP-EOS darf EOS nur erfassen,
wenn der Host es tatsächlich geliefert hat.

Pointer-/Overflow-/Dateibereichs-/Descriptorprüfungen, einzelne Frames/Nachrichten, Metadaten-/Event-/Headergrenzen, Timeouts und Korrelationscleanup bleiben technische Schutzmechanismen. Wiederverwendete 16/32-KiB-Arbeitsbuffer und MRC1-32-KiB-Chunks/64-KiB-Frames sind Kategorie 2, keine Gesamtbodybudgets. Stockspooldateien sind exklusive, Effective-UID-eigene reguläre 0600-Dateien, sofort entlinkt in einem kanonischen privaten 0700-Verzeichnis. Gepinnte Descriptoren, Vorfahrenprüfungen, begrenzte Read-/Write-Schleifen und Fehlercleanup bleiben; kein öffentlicher/TMPDIR-Fallback oder unbegrenzter RAM-Vollbodybuffer entsteht. Root-only-UID-Maps, Foreign-UID-chown-EINVAL und Namespace-EPERM blockieren hier adversariale Deploymentproben.

## Klassifikation der vier verbleibenden Limits

| Limit | Kategorie | Tatsächliche Wirkung und Behandlung |
| --- | --- | --- |
| SecRequestBodyLimit / SecRequestBodyNoFilesLimit / SecRequestBodyLimitAction; SecResponseBodyLimit / SecResponseBodyLimitAction | 1 | Native Engine-Inspection-Policy; ausgelassene Werte behalten natives Verhalten. |
| Envoy ext_authz max_request_bytes | 3; vollständiges Streaming bleibt 4 | Hostgrenze für vollständiges Sample; ext_proc für vollständiges Request-Streaming verwenden. |
| Traefik forwardAuth maxBodySize | 3; vollständiges Streaming bleibt 4 | Hostgrenze des vollständigen Request-Buffers; native UDS-Middleware für Streaming verwenden. |
| Traefik maxResponseBodySize=32768 | 2, vom Host konfiguriert (3) | Erhaltener Speicherschutz der Authorization-Antwort; Anwendungsresponse-Inspection bleibt nativ. |
| HAProxy SPOE/SPOP einzelner Frame/Nachricht | 2; nicht unterstütztes Framing/vollständiges Streaming bleibt 4 | Nur begrenztes vollständiges Sample; bei unvollständigen/widersprüchlichen Metadaten vor Engine ablehnen. Kategorie 4 niemals vollständig implementiert nennen. |

Traefik 3.7.10 `readResponseBodyBytes` allokiert `maxResponseBodySize+1` und nutzt `io.ReadFull`; fehlendes/negatives Limit nutzt `io.ReadAll`. Die erhaltenen 32768 begrenzen diesen Authorization-Buffer auf 32769 Bytes. Request-Authorization puffert ebenfalls. Zu große Authorization-Eingaben/-Antworten ergeben in diesem Pin Host-401, kein natives Inspection-Ergebnis. [Gepinnte Traefik-Quelle](https://raw.githubusercontent.com/traefik/traefik/v3.7.10/pkg/middlewares/auth/forward.go).

Unabhängige Hostkontrollen einschließlich lighttpd `server.max-request-size` bleiben Kategorie 3. Keine Route behauptet, dass alle HTTP-Bodys automatisch vollständig die Engine erreichen.

## Ausgeführte Nachweise und unabhängige Follow-ups

Aktuelle Abnahmenachweise liegen unter Run `pr407-review-ready-20261012`. Echte native Common-Tests bestanden 13 Methoden/207 Szenarien, Exit 0. Wiederherstellung der früheren 1-MiB-Response-Grenze ausschließlich in einem externen Testbuild ließ die vorhandene echte Marker-Fixture bei Assertion 407 scheitern, Exit 1; Compilation bestand und die unveränderte Suite bestand. Diese Negativkontrolle erkennt wieder eingeführte Connector-Policy.

Die echte Suite prüft Request/Response unter, an und über expliziten Engine-Limits,
Reject/ProcessPartial, DetectionOnly, mehrere Chunks, Dateien, Bodys und Marker
jenseits früherer Grenzen sowie dieselbe Payload mit unterschiedlichen Engine-Limits.
Request-Adapter erhalten den rohen nativen Status einschließlich tatsächlichem 403;
veraltete Erwartungen eines Connector-Remappings auf 413 werden ohne Produktremap korrigiert.

Apache-Early-Native-Reject gegenüber tatsächlichem HTTP-EOS wurde unabhängig reproduziert: Drei Fälle scheiterten vor Korrektur, anschließend bestanden neun echte libModSecurity-/APR-Tests mit Exit 0 und striktes C17 mit Exit 0. Native terminale Finalisierung erfindet kein empfangenes HTTP-EOS. Jedes Limit-/Aktions-Helperargument ist explizit. Unabhängige Prüfung meldete keinen neuen ungeklärten Blocker; breite Host-/Deploymentabnahme bleibt getrennt.

Frische SPOP-Evidenz: 64 Tests ohne Skips, Exit 0; striktes C17/Runtime-Selftest, fünf gepinnte HAProxy-3.2.25-Konfigurationschecks und beide Shellsyntaxprüfungen Exit 0. Integrierter echter Hostharness bestand mit Exit 0 und 28 Assertions gegen unveränderte Runtimequelle. Der überholte Fixture-Extraktionsfehler wurde ohne Abschwächung von Assertions korrigiert.

Envoy bestand alle acht unterschiedlichen Go-Pakete zweimal einschließlich echter CGo-/Native-Tests mit Exit 0; vier fokussierte Tests plus vier Unterfälle prüfen Marker jenseits 1 MiB/natives 451, ersten technischen Fehler und physische Senke. Traefik-Go-Tests/vet und C-Selftest bestanden mit Exit 0; sieben API-Quellcontracts bestanden mit Exit 0. Korrigierte Protokoll-Runtimetests bestanden auf aktueller und Basisproduktion mit Exit 0, einschließlich Oversized-Frame-Terminal-STATE2/EOF/kein Wiedereintritt, ungültigem OUTCOME, Safe-/EOS-/P3-/P4-Kontrollen, unabhängigen Peers, 64 langsamen Peers und Socketcleanup.

Stock führte 37 Tests aus: 36 bestanden, ein unveränderter RST-Basisfehler, keine Skips. Private-Spool-, Large-Replay- und Sicherheitsfälle bestanden; dies ist keine insgesamt bestandene Suite. Drei Foreign-UID-Setupproben bleiben durch chown EINVAL/Root-only-UID-Maps umgebungsbedingt blockiert; sie werden weder erlassen noch bestanden genannt. Alle 21 generierten Ausgaben sind aktuell. Der finale lokale quick-check nutzte das gepinnte Parent-CPython 3.14.7 mit vorhandenem PyYAML 6.0.3 und bestand mit 304 gemeldeten Tests, Exit 0. Die kombinierte Common-/Native-/Adapter-Suite bestand mit 69 Methoden, Exit 0. Die breite Apache-Discovery führte 237 Tests aus: 234 bestanden, drei Foreign-UID-Setupfehler blieben blockiert, Gesamt-Exit 1. Diese Resultate belegen ihre Schichten, weder zukünftige Final-Head-CI-/Sonar-/Secretscan-Erfolge noch vollständige I12-Abdeckung.

| Follow-up / Owner | Exakter Basisvergleich | Erforderliche Arbeit |
| --- | --- | --- |
| FU-COMMON-LOSSY-CONTRACT / Common tests | Aktueller Legacytest beendet mit 134 bei Lossy-Assertion 209. Exakter Basis-Legacytest endet mit 134 früher bei Config-Assertion 366, weil er entfernte Optionen verwendet. Die unveränderte gültige aktuelle Fixture gegen unveränderliche Basisproduktion scheitert ebenfalls bei 209. UTF8-Serializer-Smoke besteht auf beiden. | Verlustfreies Escaping ungültiger Bytes mit tatsächlicher Lossy-/Truncated-Klassifikation abstimmen; veraltete Fixturekonfiguration aktualisieren. Overflow-/Chaining-Assertions erhalten. |
| FU-STOCK-RST-DELIVERY / Stock + Common runtime | Exakter RST-Test endet mit 1 auf aktuellem Stand und unveränderlicher Basis mit leerem Eventlog. Gestufte Header-/Bodyzustellung endet weiter auf beiden mit 1: P2-Regelblock erscheint, technisches Delivery-Fehlerevent fehlt. | Deterministische Admission-Barriere und wahrheitsgetreues technisches Delivery-Fehlerevent hinzufügen; keinen Abort erfinden oder Assertions abschwächen. |

Diese IDs sind dauerhafte Follow-up-Referenzen, keine Behauptung erstellter GitHub-Issues. Basisproduktion wurde mit `2619b20b9d2e70fa07cbe71f664b48ff3c105380` verglichen. Die mögliche Request-only-SPOP-Logging-/Phasenabschluss-Basislücke hat nur Quellnachweis; die akzeptierte Vollständigkeits-Hostprobe nutzt den tatsächlichen Response-Companion.

## Review- und Merge-Nachweise

Ein Exact-Head-Sonar-Readback zeigte ein `c:S3776`-Issue in SPOP
`parse_headers_text` (Komplexität 26, Schwelle 25), trotz Quality Gate OK.
Die strengere Null-Neu-Issue-Abnahme erforderte deshalb eine Korrektur. Extraktion
von `parse_header_text_line` erhält Statementverhalten, Framing-/Längenprüfungen
und vollständige Headerterminatoren; unabhängige Prüfung fand keinen neuen
Securitybefund. Nach Extraktion bestanden breite SPOP-Suite mit 64 Tests, echter
kombinierter HAProxy-/HTX-Harness und 28 integrierte Hostassertions erneut mit
Exit 0. Frischer Final-Head-CI-/Sonar-Readback bleibt verpflichtend; das frühere
Quality Gate ist dieser Nachweis nicht.

Der fokussierte Reliability-Boundary-Test kompiliert die produktive Parser-
Translation-Unit mit tatsächlichem `error.c` und geprüftem Eventproducer.
Veraltete I09-/I11-Mocks wurden an diese Contracts angepasst, Assertions erhalten
und Kontrollen für ungültiges BOOL, unvollständiges Sample und widersprüchliche
Header ergänzt; der fokussierte Test bestand mit Exit 0. Der untere JSON-Writer
bleibt gestubbt: Dies belegt Parser-/Checked-Producer-Verhalten, keine physische
Event-Sink-Zustellung. Nach Anpassung der Traefik-Fixture an die tatsächliche
`begin_request_stream`-API bestand das vollständige Reliability-Modul 15 Tests
mit Exit 0 in 7.936 Sekunden. Assertions bleiben erhalten, mit stärkerer
`lock < stream_begin < unlock`-Reihenfolge. Unabhängiger finaler Diffreview fand
keinen Blocker im Scope. Der Runtimehelper blieb bei Fixturekorrektur unverändert;
frischer Final-Head-CI-/Sonar-Readback bleibt getrennt.

Final-Head-Quickchecks, betroffene Regressionen/Builds/Generatoren/Docs, eine empfindliche Mutationskontrolle früherer Limits, unabhängiger redigierter Secretscan und Exact-Head-CI-/Sonar-Readback sind vor Ready verpflichtend. Null neue offene/akzeptierte Issues, Hotspots und Duplikation müssen ohne Ausnahmen beobachtet werden. Sonar ohne gemessene Coverage belegt keine ausführbare Testcoverage. Vollständige I12-/V08–V10-Matrix und blockierte Deploymentproben bleiben getrennt von Reviewbereitschaft. Tatsächlichen Lieferstand aus [PR-Checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407/checks) lesen, nicht aus altem Quelldokument-SHA. Siehe [Stackcheckliste](response-limit-stack-checklist.de.md).

Der unabhängige redigierte Gitleaks-Scan des vollständigen Worktrees lieferte Exit 1 für 47 Kandidaten. Die schreibfreie Einordnung bestätigte 44 Cache-Hashes, eine öffentliche Action-Commit-SHA, einen Report-Identifier und einen Audit-Texttreffer, jeweils unverändert gegenüber unveränderlicher Basis und bisherigem Head. Keine Scanner-Ausnahme, Unterdrückung oder Risikoannahme wurde ergänzt. Dies macht den Tree-Scan nicht erfolgreich; der finale Commit-Range-Scan benötigt seinen eigenen Nachweis.
