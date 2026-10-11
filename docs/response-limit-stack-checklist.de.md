# Stack-Checkliste für Request-/Response-Body-Limits

**Sprache:** [English](response-limit-stack-checklist.md) | Deutsch

## Stack-Identität

Der bestehende [Draft-PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
bleibt auf [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) gestapelt.
Branch: `fix/engine-owned-response-limits-stack-20261011`.
Basis-Branch: `fix/unified-native-results-events-20260921`.
Exakte Basis: `2619b20b9d2e70fa07cbe71f664b48ff3c105380`.
Starthead des erweiterten Auftrags: `6576661724841e26802a93b19d8bbfbdb5c8235a`.
Kein neuer PR und kein PR-/master-Merge. Der Nutzer erlaubt reguläre Basis-Merges
von #382 in den bestehenden #407-Branch; veröffentlichte Historie bleibt erhalten.
Die Auslieferung ist zum Stand dieses Dokumentationssnapshots offen.

## Implementierung

- [x] Common und alle zehn logischen direkten/Companion-/Middleware-/Sidecar-Profile verfolgt.
- [x] Common-Request-/Response-Body-Policyfelder, Defaults, Merge-/Parserlogik und Connector-`body_limit_action` entfernt; Adapter-/Service-Policyverbraucher entfernt.
- [x] Native Request-/Response-Direktiven verwenden; keine Connector-injizierten Limits, Regeltextableitung, gewähltes Reject/ProcessPartial oder kumulative Kürzung.
- [x] Native Append-Interventionen/-Ergebnisse bis EOS und Phasenabschluss erhalten, einschließlich tatsächlicher DetectionOnly-Semantik.
- [x] Socket-Vollbody-Allokation und Stock-Sidecar-Fallback durch inkrementelle Verarbeitung/private Dateipufferung ersetzt; technische Schutzmaßnahmen erhalten.
- [x] Entfernte Optionen ablehnen; Beispiele, Generator und EN/DE-Referenzen aktualisieren.
- [ ] Alle aktiven Profil-Gesamtbodygrenzen beseitigen: Die konkreten Autorisierungseinschränkungen unten bleiben bestehen.

## Aktuelle ausführbare Nachweise

Die früheren Komponentenergebnisse unten behalten ihren Revisionsbezug.
Der Basisabgleich dokumentiert den bestandenen aktuellen I11-Gesamtcheck separat.

- [x] Echte Request-/Response-Prüfungen unter/exakt/über Limit, Aktionen, Chunks/Dateien, unterschiedliche Limits, DetectionOnly und Marker jenseits früherer Connectorgrenzen.
- [x] Echter 2-MiB-Autorisierungssocket-Lebenszyklus ohne doppelten Präfix.
- [x] Ausgewählte Komponentenbuilds, Verträge, Sicherheits-/Konfigurations- und Dokumentationsprüfungen.
- [x] Abschließender vollständiger `quick-check` und nativer I09-Abgleich auf dokumentierter I09-Basis.
- [x] Betroffene/vollständige Validierung auf finaler gemergter I11-Basis.
- [ ] CI/Sonar des aktuellen geänderten Heads: keine neuen Issues, Hotspots oder Duplikate.

Frühere Common-Validierung der Erweiterung mit echter Library bestand neun Methoden: 112 native
Request- und 81 Response-Szenarien (193 insgesamt). Ein späterer kombinierter
Lauf bestand 30 Tests. Vier echte Autorisierungssocketfälle verwenden einen
2-MiB-Body: Ein Tail-Marker liefert bei hohem Limit nativ 451, dieselbe Payload
bei niedrigem ProcessPartial-Limit 200, niedriges Reject nativ 403, und ein Body
ohne Marker wird erlaubt. Der Callback schließt P2 vor dem Handoff ab, ohne
einen Präfix doppelt anzubieten.

Common-Helper-/SDK-/Security-/Speicher-/Flow-/Adapter-/Direktivenprüfungen
bestanden. Sieben Konfigurationsreferenztests bestanden; alle 21 generierten
Dateien sind aktuell. EN/DE-, Pfad-/Linkprüfungen und 22 Compilerleitfadentests
bestanden. Apache C17 bestand; HAProxy-Binding-/Selftest-/SPOP-C-Builds und
104 Tests mit 119 Subtests bestanden; die abschließende echte Request-/Response-
Suite bestand 13 Methoden in 13,62 Sekunden. Envoy bestand acht Go-Packages und seinen echten
CGo-Build. Traefik-Go-/C-Builds und Socket-Protokoll-Selftests bestanden.
lighttpd-C-Build, 15 Gate-Tests und zwei isolierte Envoy-Tests bestanden.
Stock-Sidecar-Validierung bestand 35/36; ihr unveränderter RST-Basisdefekt mit
leeren Events bleibt offen. Die ältere Common-Lossy-Event-Assertion bleibt ein Basisfehler. Die zwei alten
SPOP-Quellcode-Assertions bestehen nach Übernahme der I09-Fixes aus der Basis.
Assertions sind erhalten.

Der abgeschlossene native `make quick-check` bestand (Exit 0): zehn Unittest-
Gruppen mit 302 Tests sowie Lint, Verträge, Security, Speicher, Dokumentation,
generierte Referenzen, Helper, actionlint und Diffprüfungen.

Abschließende Common-Nativvalidierung bestand 13 Methoden und 168 Subtests in
14,34 Sekunden (`root-checks/final-common-native.log`) einschließlich der vier
HTTP-Fälle. HAProxys echte Suite bestand 13 Methoden in 13,62 Sekunden; Response-
DetectionOnly erhielt den tatsächlichen nativen 65536-Byte-Präfix eines 120000-
Byte-Bodys in vier Chunks: Reject-Append-Ergebnisse `[1,1,1,1]`, ProcessPartial
`[1,1,0,0]`, EOS `1`. Sieben Konfigurationsreferenztests bestanden einschließlich
strikter Mutationen entfernter Schlüssel. Alle NGINX-Adoptions-/Mutationsprüfungen
bestanden. Ein kombinierter Vier-Datei-Lauf bestand 145 Tests und 163 Subtests
mit zwei veralteten Apache-Planererwartungen; nach deren Korrektur bestanden alle
sechs Apache-Prüfungen und erhalten native Append-`0`-/`1`-Fortsetzung und exakte
EOS-`1`-Guards. Unabhängiger Review fand Akzeptanz entfernter Schlüssel bei
Case-Alias/JSON-null; EqualFold-Abgleich und 24 negative Fälle bestanden nun mit
der gesamten Traefik-Go-Suite. Sieben zusätzliche Traefik-forwardAuth-Tests
bestanden. Kein Reviewbefund bleibt offen.

CI/Sonar für den geänderten aktuellen Head
und Nachweis ohne neue Issues/Hotspots/New-Code-Duplikation sind offen; aktuelle
Ergebnisse sind in [PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407) verlinkt.

## Aktive kumulative/Sample-Einschränkungen

Vollständige Entfernung über alle aktiven Profile wird nicht behauptet.

| Aktive Route | Verbleibende Grenze und tatsächlicher Wirkungsbereich |
| --- | --- |
| Envoy ext_authz | Host-`max_request_bytes=4096/33` begrenzt das vollständige an die Autorisierung gesendete Request-Sample; sein Response-Observer macht die Request-Eingabe nicht inkrementell. |
| Traefik forwardAuth | Host-`maxBodySize=4096/33` begrenzt den gepufferten Autorisierungsrequest. |
| Composite-Traefik-Autorisierungsantwort | Host-`maxResponseBodySize=32768` begrenzt die Autorisierungsantwort, nicht die Response der Upstream-Anwendung. |
| HAProxy SPOE/SPOP | Ein Request-Sample je begrenzter Protokollnachricht/Frame; ein unvollständiges Sample scheitert vor der Engine mit Admission-Status 503, nicht nativem `BODY_LIMIT`. Natives HTX ist separat. |

## Technische Sicherheit

Inkrementelle HTTP-Arbeitspuffer haben 16 KiB; Datei-Lesescratch hat 32 KiB.
MRC1 behält einzelne 64-KiB-Frames und 32-KiB-Body-Chunks. Zähler bleiben durch
ihren Integer-Typ (`SIZE_MAX`, bei signierten Zählern/Dateioffsets `INT64_MAX`)
darstellbar; Überlauf endet als technischer Fehler ohne Engine-Append/Kürzung. Pointer-/Integerprüfungen,
Deskriptoren/Dateibereiche, Nachrichtenkontrollen, Header-/Eventmetadaten und
Timeouts bleiben erhalten. Stock-lighttpd verwendet private entlinkte Dateipufferung
mit begrenztem RAM und hält Upstream-Replay bis zum nativen P2-Allow zurück;
Datenträgerfehler bleiben technische Fehler. Der Legacy-Vollbody-Fallback ist
entfernt. Dies sind Schutzmaßnahmen für einzelne Operationen/Speicherung und
keine Ersatz-Inspektionslimits.

## Fehlende aktuelle Hostnachweise

Keine vollständige aktuelle gehostete Zehn-Profil-Matrix für Request/Response
liegt vor. Engine-, Socket- und Komponentennachweise belegen keine Host-Buffer-
Ownership, HTTP/1/2/3-Lebenszyklen, Commit-Zeitpunkte oder Late-Abort-Verhalten.

- [ ] Apache native.
- [ ] NGINX native einschließlich Speicher-/Dateibuffer.
- [ ] HAProxy native HTX.
- [ ] HAProxy SPOE/SPOP mit native-HTX-Response-Companion.
- [ ] Envoy ext_proc.
- [ ] Envoy ext_authz mit Response-Observer.
- [ ] Traefik native UDS-Middleware.
- [ ] Traefik forwardAuth mit Response-Observer.
- [ ] lighttpd Stock-Sidecar.
- [ ] lighttpd patched native.

## Aktueller Basisabgleich

Die ausgewählte aktuelle #382-Basis ist `2619b20b9d2e70fa07cbe71f664b48ff3c105380` (I11).
Die reguläre I09-Integration ist als `2bb1a1e0` committed; die autorisierte
reguläre I11-Basisintegration ist lokal abgeschlossen und der Quellcode eingefroren.
Veröffentlichte Historie bleibt erhalten; kein PR-/Master-Merge oder Force-Push erfolgt.

Auf integrierter I09-Basis `492663334d89428dce084792145ef94e91579788` bestand
`check-i09-native-routes` 33 Tests und natives `make quick-check` mit Exit 0,
einschließlich zehn Unittest-Gruppen mit insgesamt 302 Tests
(`root-checks/resume-base492-check.log`). Die alten SPOP-Quellcode-Assertions
bestehen mit Upstream-I09-Fixes. Früherer Common-Abgleich bestand 30 gezielte
Tests einschließlich 13 echter Engine-Tests; Traefik-Go-Packages, I09-lighttpd-/
Traefik-Tests und beide C-Builds bestanden. Stock-Sidecar bleibt wegen
unverändertem RST-Verhalten mit leeren Events bei 35/36; neu gebaute Common-
Legacy-Lossy-Eventvalidierung beendet sich bei Assertion 209 mit Exit 134.
Assertions bleiben erhalten.

Auf ausgewählter I11-Basis `2619b20b9d2e70fa07cbe71f664b48ff3c105380`
bestand die finale native Auswahl über 20 Module mit 212 Tests und 201 Subtests
in 58,51 Sekunden einschließlich 13 echter Engine-Methoden. Apache-C17-,
APR-/LTO-Cleanup- und Adoptionsprüfungen sowie echte HAProxy-Binding-/Build-/
Selftest-/SPOP-Protokollprüfungen bestanden. Zusätzliche echte APR-Bucket- und
Production-Append-Regressionsprüfungen für P2/P4 bestanden 20 Methoden und zehn
Subtests: natives Pending-403 bis EOS sowie persistenter `/dev/full`-IO-Fehler
mit 500 ohne Replay. Unabhängiger Review fand keinen Befund. Alle acht Envoy-
Packages bestanden rein in Go sowie mit echter CGo-/libModSecurity-Anbindung;
der Binary-Build bestand. Nachweise: `native/base261/validation-status.json`
und `remaining/base261/validation.md`.

Der abschließende aggregierte native Make-Lauf auf I11 bestand mit Exit 0:
`check-i09-native-routes` mit 33 Tests, `check-apache-event-sink` mit 20 Tests,
`check-haproxy-spop-event-sink` mit 19 Tests und `quick-check` mit zehn Unittest-
Gruppen und 304 Tests. Security-/Speicher-/Flow-/Helper-/Dokumentationsprüfungen,
21 generierte Dateien und Diffprüfung bestanden. Tatsächliche Apache-, NGINX-
und HAProxy-C17-Compileprüfungen bestanden; ältere lokale Compile-Nachweislücken
sind damit geschlossen, nicht die fehlende Hostmatrix. Nachweis:
`root-checks/base261-final-make.log`. Der zusätzliche kombinierte NGINX-Adoptions-/
Bounded-URI-/Envoy-Bridge-Lauf bestand 130 Tests in 694,670 Sekunden
(`root-checks/base261-root-targeted.log`). Die abschließende gezielte Inventur
einschließlich versteckter Dateien unter Common, allen Connectoren und Beispielen
fand keine zusätzliche aktive eigene kumulative Bodygrenze, Direktiveninjektion
oder Fallback außerhalb der ausgewiesenen Autorisierungs-/Sample-Grenzen; kein
verstecktes Pluginmanifest enthält einen entfernten Schlüssel. Unabhängiger
Review von P2-/P4-EOS und persistentem IO-Fehler fand keinen Befund. Push/Readback und CI/Sonar des
aktuellen Heads bleiben offen; #407-Remotehead ist weiterhin
`6576661724841e26802a93b19d8bbfbdb5c8235a`.

## Grenze historischer Nachweise

Frühere Response-only-Prüfungen und abgeschlossene Sonar-Ergebnisse einschließlich
des Startheads belegen nur jene Revisionen. Sie verifizieren nicht den erweiterten
aktuellen Diff. Siehe [Zuständigkeitsvertrag](phase4-mode-budget.de.md) und
[Change Record](../reports/audits/change-records/CR-20261011-response-limit-policy-removal.de.md).
