# Stack-Checkliste für Request-/Response-Body-Limits

**Sprache:** [English](response-limit-stack-checklist.md) | Deutsch

## Stack-Identität

Der bestehende [Draft-PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
bleibt auf [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) gestapelt.
Branch: `fix/engine-owned-response-limits-stack-20261011`.
Basis-Branch: `fix/unified-native-results-events-20260921`.
Exakte Basis: `492663334d89428dce084792145ef94e91579788`.
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

- [x] Echte Request-/Response-Prüfungen unter/exakt/über Limit, Aktionen, Chunks/Dateien, unterschiedliche Limits, DetectionOnly und Marker jenseits früherer Connectorgrenzen.
- [x] Echter 2-MiB-Autorisierungssocket-Lebenszyklus ohne doppelten Präfix.
- [x] Ausgewählte Komponentenbuilds, Verträge, Sicherheits-/Konfigurations- und Dokumentationsprüfungen.
- [x] Abschließender vollständiger `quick-check` und finaler nativer Testabgleich.
- [ ] CI/Sonar des aktuellen geänderten Heads: keine neuen Issues, Hotspots oder Duplikate.

Aktuelle Common-Validierung mit echter Library bestand neun Methoden: 112 native
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

Die Basis ist auf `492663334d89428dce084792145ef94e91579788` (I09) vorgerückt. Typisierte native Fehler,
operationsspezifische Ergebnisse, erhaltene Fehlerphase, einmaliges Cleanup und
kompilierte Regressionen werden mit der Entfernung eigener Body-Policy verbunden.
Common-Abgleich bestand 30 gezielte Tests einschließlich 13 echter Engine-Tests.
Traefik-Native-/Composite-/Observer-Go-Packages, I09-lighttpd-/Traefik-Tests und
beide C-Builds bestanden. Der Stock-RST-Event-Gap bleibt bei 35/36; der neu
gebaute ältere Common-Lossy-Eventtest endet weiter mit 134 an Assertion 209.
Dies sind Beobachtungen der aktuellen Basis. Whole-Tree-quick-check und nativer
I09-Abgleich müssen nach dem Basis-Merge erneut laufen; frühere quick-check-
Nachweise gelten für den Stand vor Integration. PR #382 wird während der Arbeit
wiederholt geprüft.

## Grenze historischer Nachweise

Frühere Response-only-Prüfungen und abgeschlossene Sonar-Ergebnisse einschließlich
des Startheads belegen nur jene Revisionen. Sie verifizieren nicht den erweiterten
aktuellen Diff. Siehe [Zuständigkeitsvertrag](phase4-mode-budget.de.md) und
[Change Record](../reports/audits/change-records/CR-20261011-response-limit-policy-removal.de.md).
