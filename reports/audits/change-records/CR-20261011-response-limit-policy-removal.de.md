# Change Record: CR-20261011-response-limit-policy-removal

**Sprache:** [English](CR-20261011-response-limit-policy-removal.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261011-response-limit-policy-removal |
| Datum (UTC) | 2026-10-11 |
| Basis-Revision | `492663334d89428dce084792145ef94e91579788` |

## Motivation und Problemstellung

Die aktuelle Nutzeranweisung erweitert bestehenden Draft-PR #407 auf beide
Bodyrichtungen und hebt den Erhalt der Request-Policy ausdrücklich auf.
Connector-Policy konnte vor nativer Inspektion ablehnen/kürzen. Request-Policy
gehört zu `SecRequestBodyLimit`, `SecRequestBodyNoFilesLimit` und
`SecRequestBodyLimitAction`; Response-Policy gehört zu `SecResponseBodyLimit`
und `SecResponseBodyLimitAction`. Vollständige Entfernung wird nicht behauptet,
solange die unten aufgeführten aktiven Autorisierungs-/Sample-Grenzen bestehen.

## Akzeptanzkriterien

Connector-Request-/Response-Optionen, Defaults, Merge-/Parserlogik, Fallbacks
und kumulative Vorentscheidungen vor der Engine entfernen. Keine Engine-Limits
ableiten, Regeln injizieren, Aktionen wählen, kürzen oder Grenzen durch
unbegrenzte Vollbody-Allokation ersetzen. Native Operationsergebnisse,
Interventions-/Phasenabschluss, DetectionOnly, Fehlerweitergabe und Cleanup
erhalten. Inspektionsfixtures liefern Engine-Limits/-Aktionen ihrer Richtung
explizit; Helper haben keine Policydefaults. Grenzen, Aktionen, Chunks/Dateien,
identische Payloads unter verschiedenen Limits und Marker jenseits früherer
Grenzen nachweisen. Entfernte Optionen ablehnen; EN/DE-Quellen und generierte
Referenzen pflegen. Technische Schutzmaßnahmen und Sonar-Gates ohne neuen Code-
Befund erhalten. Aktive Grenzen und fehlende Hosts getrennt melden; bestehenden
#407 erweitern ohne Force-Push, History-Rewrite oder PR-/master-Merge. Eine spätere ausdrückliche
Nutzerfreigabe erlaubt reguläre #382-Basis-Merges in den bestehenden #407-Branch.

## Implementierungsentscheidung und Begründung

`MSCONNECTOR_DEFAULT_REQUEST_BODY_LIMIT`, `request_body_limit`,
`body_limit_action`, entsprechende Adapteroptionen, HAProxy `request-body-limit`,
Envoy `max_request_body_bytes` und Traefik `maxRequestBodyBytes` zusammen mit
der zuvor entfernten Response-Policy entfernen. Native Ergebnisse bestimmen
P2/P4 einschließlich Append null bei gültigem nativem ProcessPartial und
bewahrter disruptiver Ergebnisse bis EOS; tatsächlicher nativer Status bleibt
erhalten. `bytes_inspected` zählt der Engine angebotene Bytes, nicht ihren
internen Teilpräfix. Inkrementelle Socket-/Dateiverarbeitung und private
Sidecar-Dateipufferung ersetzen Vollbody-Fallbacks. Tests ohne Body-Inspektion
benötigen keine künstliche native Policy.

## Geänderte Dateien

Common-Konfigurations-/Body-/Resource-/Mapper-/Transaktionsverträge, native
Runtime und Autorisierungstransport; Apache-/NGINX-/HAProxy-/Envoy-/Traefik-/
lighttpd-Eingabe, Services, Middleware, Harnesses, Fixtures und Tests;
Konfigurationsreferenz-/Compilerleitfadengeneratoren mit generierter EN/DE-
Ausgabe; Beispielkonfiguration, Connector-README-Paare und Body-Zuständigkeits-
dokumentation. Stack-Checkliste und Change-Record-Paar erfassen aktuellen Umfang.
Keine Framework-/MRTS-Quellen oder Dependency-Manifeste werden geändert.

## Ausgeführte Befehle

Beobachtete aktuelle Prüfungen und erhaltene Artefakte liegen unter `/var/tmp/codex/ModSecurity-conector/runs/body-policy-removal-20261011/`:
`common/real-engine.log` (neun Methoden, 193 Szenarien), kombinierter finaler
Common-Lauf (30 Tests), `root-checks/common-contracts.log` (alle ausgewählten
Common-Targets) und `root-checks/docs.log` (21 generierte Referenzen, EN/DE-/Pfad-/
Linkprüfungen und 22 Compilertests). Sieben Konfigurationsreferenz-Unittests
bestanden. Komponentenbuild-/Testergebnisse stehen unten. Der erneute
`root-checks/quick-check.log` belegt `make quick-check` mit Exit 0: zehn
Unittest-Gruppen mit 302 Tests sowie Lint, Verträge, Security, Speicher,
Dokumentation, generierte Referenzen, Helper, actionlint und Diffprüfungen.

Dokumentationsvalidierung verwendet Repository-Payloads über RTK:

```sh
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check
rtk proxy make check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
rtk proxy git diff --check
```

## Security-Auswirkung

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

Authentifizierung, Isolation, Warnungen, Assertions, Scanner-Ausnahmen oder
Quality Gates werden nicht abgeschwächt. Native Konfiguration behält bei
Auslassung native Defaults; der Connector setzt keine. Autorisierungshostpuffer
bleiben konkrete Grenzen mit Migrations-/Nachweisbedarf und werden nicht als
technische Kapazität umbenannt. Unabhängiger gezielter Quellcode-Sicherheitsreview
fand keinen konkreten Befund; das belegt keine gehostete Runtime-Sicherheit.

## Runtime-Evidence

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

Die nativen Common-Tests verwenden explizite Grenzen 128/1024, Reject/ProcessPartial,
Request-On/DetectionOnly mit Buffered-/Streamingmodi und Speicher-/Dateieingabe;
Response-Fälle `off`/`safe`/`strict` bleiben enthalten. Explizite 1,5-/3-MiB-Policies
mit 2-MiB-Bodies prüfen Marker jenseits der früheren 1-MiB-Connectorgrenze.
Gleiche Payloads unter zwei nativen Limits unterscheiden erlaubte Inspektion
von nativem Teilverhalten; kein Connector wählt Aktion/Präfix. Alle Ergebnisse
oben sind Engine-/Socket-/Komponentennachweise statt einer aktuellen Zehn-Host-Matrix.

## Bekannte Einschränkungen

| Aktive Route | Verbleibende Grenze und tatsächlicher Wirkungsbereich |
| --- | --- |
| Envoy ext_authz | Host-`max_request_bytes=4096/33` begrenzt das vollständige an die Autorisierung gesendete Request-Sample; sein Response-Observer macht die Request-Eingabe nicht inkrementell. |
| Traefik forwardAuth | Host-`maxBodySize=4096/33` begrenzt den gepufferten Autorisierungsrequest. |
| Composite-Traefik-Autorisierungsantwort | Host-`maxResponseBodySize=32768` begrenzt die Autorisierungsantwort, nicht die Response der Upstream-Anwendung. |
| HAProxy SPOE/SPOP | Ein Request-Sample je begrenzter Protokollnachricht/Frame; ein unvollständiges Sample scheitert vor der Engine mit Admission-Status 503, nicht nativem `BODY_LIMIT`. Natives HTX ist separat. |

Diese aktiven Sample-/Vollbody-Grenzen verhindern die Behauptung vollständiger
Entfernung über alle Profile. Unabhängige Hostkonfiguration einschließlich
lighttpd `server.max-request-size` bleibt ebenfalls getrennt. Stock-RST-
Eventdefekt und Common-Lossy-Eventfehler bleiben Basisdefekte. Die zwei historischen
SPOP-Quellcode-Assertionfehler sind durch die I09-Basis-Fixes gelöst; Assertions
sind nicht abgeschwächt.

## Verbleibende Risiken

Die aktiven Autorisierungsprofile bieten keine uneingeschränkt inkrementelle
Request-Eingabe. Gepinnte aktuelle Hostnachweise fehlen für alle zehn Profile,
einschließlich Buffer-Ownership, Protokolllebenszyklus und später Interventionen.
Lokaler nativer Testabgleich und vollständiger quick-check bestanden. CI/Sonar
des geänderten Heads und Verifikation der erweiterten PR-Auslieferung bleiben offen. Gesamtverifikation
ist teilweise.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige aktuelle gehostete Request-/Response-Zehn-Profil-Matrix wurde
ausgeführt; erforderliche gepinnte Hostumgebungen und Laufnachweise fehlen.
Der erneute vollständige quick-check bestand nach Checkerreparaturen.
CI/Sonar des aktuellen geänderten Heads ist offen. Historische Response-only-
Prüfungen und Sonar-Ergebnisse des Startheads gelten nur für ihre Revisionen
und belegen nicht den aktuellen erweiterten Diff.

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

## Finaler Diff- und Review-Status

Bestehender [Draft-PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
bleibt auf `fix/engine-owned-response-limits-stack-20261011`, gestapelt auf #382.
Die Erweiterung startet bei `6576661724841e26802a93b19d8bbfbdb5c8235a` und integriert die vorgerückte Basis oben.
Ihre erweiterten Änderungen sind zum Stand dieses Snapshots noch nicht gepusht.
Kein neuer PR, Force-Push, History-Rewrite oder PR-/master-Merge erfolgt.
Reguläre Basisintegration in #407 ist ausdrücklich freigegeben. Abschließender
Scoped-Review/Diffvalidierung und aktueller Head-Readback bleiben Voraussetzungen
der Auslieferung. Siehe
[Stack-Checkliste](../../../docs/response-limit-stack-checklist.de.md) und
[Zuständigkeitsvertrag](../../../docs/phase4-mode-budget.de.md).
