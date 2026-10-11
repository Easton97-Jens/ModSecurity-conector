# Change Record: CR-20261011-response-limit-policy-removal

**Sprache:** [English](CR-20261011-response-limit-policy-removal.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261011-response-limit-policy-removal |
| Datum (UTC) | 2026-10-11 |
| Basis-Revision | `2619b20b9d2e70fa07cbe71f664b48ff3c105380` |

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

Beobachtete frühere Erweiterungsprüfungen und erhaltene Artefakte liegen unter `/var/tmp/codex/ModSecurity-conector/runs/body-policy-removal-20261011/`:
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

Eine spätere Prüfung des aktuellen Quellstands fand, dass Envoys Composite-
Template noch partielle Samples erlaubte und der Adapter stets natives EOS
lieferte. Ein erfasstes Präfix konnte dadurch bei höherem Engine-Limit oder
DetectionOnly als vollständiger Body autorisiert werden. Der Folgefix verwendet
eine Hostkonfiguration ausschließlich für vollständige Samples und lehnt
ausdrücklich partielle oder mehrdeutige Metadaten vor dem Öffnen von Common ab.
Vollständige Eingabe hat keine Connector-Schwelle. Das repariert den Vertrag zur
Transportvollständigkeit; die dokumentierte Hostgrenze bleibt erhalten.

Diese aktiven Sample-/Vollbody-Grenzen verhindern die Behauptung vollständiger
Entfernung über alle Profile. Unabhängige Hostkonfiguration einschließlich
lighttpd `server.max-request-size` bleibt ebenfalls getrennt. Stock-RST-
Eventdefekt und Common-Lossy-Eventfehler bleiben Basisdefekte. Die zwei historischen
SPOP-Quellcode-Assertionfehler sind durch die I09-Basis-Fixes gelöst; Assertions
sind nicht abgeschwächt.

## Verbleibende Risiken

Die aktiven Autorisierungsprofile bieten keine uneingeschränkt inkrementelle
Request-Eingabe. Eine vollständige aktuelle Zehn-Profil-Hostmatrix fehlt,
einschließlich Buffer-Ownership, Protokolllebenszyklus und später Interventionen.
Lokaler nativer I09-Abgleich und vollständiger quick-check bestanden. Finaler
betroffener/vollständiger I11-Lauf bestand. CI/Sonar des geänderten Heads und
Verifikation der erweiterten PR-Auslieferung bleiben zum lokalen Snapshot offen. Gesamtverifikation
ist teilweise.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige aktuelle gehostete Request-/Response-Zehn-Profil-Matrix wurde
ausgeführt. Gecachte Host-Binaries existieren, belegen aber weder die Provenienz
aktueller Connector-Module noch Laufzeitergebnisse. Das lokale UID/GID-Mapping
erlaubt nur root; eine Ownership-Probe mit fremder UID scheitert mit `EINVAL`,
eine User-/Mount-Namespace-Probe mit `EPERM`. Vorgeschriebene Übergaben an
Non-root-Worker und tatsächliche Spool-Prüfungen auf Read-only-Mounts bleiben
daher in dieser Umgebung blockiert. Ausgewählte Envoy-Hostläufe werden unten
getrennt dokumentiert.
Der erneute vollständige quick-check bestand nach Checkerreparaturen auf
dokumentierter I09-Basis. Finale betroffene/vollständige I11-Validierung bestand mit Exit 0; der
zusätzliche kombinierte NGINX-/Bounded-URI-/Bridge-Lauf bestand 130 Tests.
CI/Sonar des aktuellen geänderten Heads ist offen. Historische Response-only-
Prüfungen und Sonar-Ergebnisse des Startheads gelten nur für ihre Revisionen
und belegen nicht den aktuellen erweiterten Diff.

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
Review von P2-/P4-EOS und persistentem IO-Fehler fand keinen Befund. Der später analysierte #407-Head ist `cec340f3`; Follow-up-Commit,
Push/Readback und neue exakte Head-CI/Sonar nach dessen Reparaturen bleiben offen.

## Aktueller Sonar-Reparatur-Snapshot

Die erste abgeschlossene Analyse von `cec340f3` meldete 32 Issues (ein Bug,
zwei Vulnerabilities, 29 Code Smells), null Hotspots und sieben neue
Duplikationsblöcke mit 65 Zeilen. Diese Analyse ist kein bestandener Gate-Nachweis.
Die Quellcode-Reparaturen sind lokal eingefroren; sie erhalten Prüfungen und
Assertions und ändern keine Scanner-Ausnahmen oder Gate-Steuerung. Neue exakte
Head-CI/Sonar und Follow-up-Commit/Push bleiben offen; der Live-Status steht in
[PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407).

Aktuelle lokale Wiederholungen bestanden: Common mit 207 nativen Szenarien und
13 echten Methoden, native Auswahl mit 131 Tests/185 Subtests, Go-/C-Builds und
Sicherheitsprüfungen sowie 16 Root-CI-Fixturetests für Pending-Request-Zustand/-
Zähler, Runtime-Konstruktor und modellierte NGINX-Intervention. Die frühere
212-Test-/201-Subtest-Auswahl ist ein eigener Lauf; wiederholte Prüfungen werden
nicht zu einer Gesamttestzahl addiert. Aktueller Stock-Sidecar-Lauf bestand 57/58;
nur der bekannte RST-Fehler mit leeren Events bleibt dort offen. Zusammen mit
der Common-Legacy-Lossy-Event-Assertion bleiben zwei Basisdefekte offen.
Nachweise liegen unter `common/sonar-cec/`, `native/sonar-cec/`,
`remaining/sonar-cec/` und `root-checks/ci-fixture-repairs-final.log` im externen
Task-Laufverzeichnis. Generierte Referenzen erfassen nun 22 lighttpd-Einträge.

Das optionale technische CLI-Argument `--spool-directory` wählt private
Request-Dateipufferung. Standard ist der validierte private Elternpfad von
`--config`. Bei `/etc` oder schreibgeschützter Konfigurationsablage muss ein
bereits existierender kanonischer, vom effektiven Service-UID besessener,
schreibbarer 0700-Pfad explizit angegeben werden. Startup prüft Elternpfade,
No-follow-Directory-Descriptoren und Dateierzeugung vor Bereitschaft. Request-
Dateien sind exklusiv erzeugte 0600-Dateien und sofort entlinkt. Startup-/
Descriptor-/Datenträgerfehler bleiben technische Fehler. Kein `TMPDIR`- oder
öffentlicher Fallback, keine Gesamtbodygrenze und keine unbegrenzte RAM-
Vollbody-Allokation werden eingeführt. Betreiber mit nicht privatem
Konfigurationselternpfad müssen dieses Storage-Argument setzen.

Die anschließende abgeschlossene Analyse auf `dc33ffef` zeigte null Bugs,
Vulnerabilities, Hotspots und duplizierte Zeilen/Blöcke, aber noch sechs
Code-Smells; das grüne Quality Gate erfüllte deshalb die Null-Issue-Vorgabe
noch nicht. Die nächste Korrektur verschiebt das gemeinsame HTTP-Transaktionsmodell
in seinen Header, damit alle drei Fixtures ihn regulär einbinden können,
trennt Spool-Deklarationen und lagert natives NGINX-Fehlerlogging aus.
Guard-Position und Interventions-Ownership bleiben erhalten. Die gezielte
NGINX-Prüfung bestand mit 82 Tests und 154 Subtests sowie tatsächlicher
C17-Kompilierung. Strikte HTTP-Fixture- und Sanitizer-Prüfungen validieren das
gemeinsame Modell. Ein frischer Scan des exakten Heads bleibt erforderlich.

Die ausgewiesenen aktiven Autorisierungs-/Sample-Grenzen und zehn fehlenden
Hostprofile-Nachweise bleiben bestehen; weder vollständige Entfernung noch
vollständig verifizierte Auslieferung wird behauptet.

## Finaler Diff- und Review-Status

Bestehender [Draft-PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
bleibt auf `fix/engine-owned-response-limits-stack-20261011`, gestapelt auf #382.
Die Erweiterung startet bei `6576661724841e26802a93b19d8bbfbdb5c8235a` und integriert die vorgerückte Basis oben.
Die Erweiterung wurde inzwischen bis zum analysierten Head `cec340f3`
ausgeliefert; der anschließende Reparatur-Follow-up ist zum Stand dieses
Snapshots noch nicht committed/gepusht.
Kein neuer PR, Force-Push, History-Rewrite oder PR-/master-Merge erfolgt.
Reguläre Basisintegration in #407 ist ausdrücklich freigegeben. Abschließender
Scoped-Review/Diffvalidierung und aktueller Head-Readback bleiben Voraussetzungen
der Auslieferung. Siehe
[Stack-Checkliste](../../../docs/response-limit-stack-checklist.de.md) und
[Zuständigkeitsvertrag](../../../docs/phase4-mode-budget.de.md).


## Envoy-Vollständigkeit und Folgeprüfung am echten Host

Das Composite-Autorisierungstemplate akzeptiert jetzt nur vollständige Samples.
Der Adapter lehnt partielle, fehlerhafte oder mehrdeutige Vollständigkeitsmetadaten
vor Common-Open/Body/EOS/Lease-Erzeugung ab; vollständige Eingabe erhält keine
Connector-Byteschwelle. Echte Common-/libModSecurity-Tests geben Request- und
Response-Policies ausdrücklich an, inspizieren den Tail-Marker jenseits der
früheren Callback-Grenze und unterscheiden On von DetectionOnly.

Die native Oversize-Hostfixture enthält jetzt exakt 33 Bytes, innerhalb der
Kapazität des ausgewählten Hosts und oberhalb seines expliziten nativen Limits
32. Echtes natives Reject liefert 403. Der gemeinsame Verifier verlangt gleichen
nativen P2-, Deny-Host- und Clientstatus (403 oder 413), den geordneten Lebenszyklus
und keine Upstream-Antwort; eine reine Host-Ablehnung erfüllt seinen nativen
P2-Nachweis nicht.

Eine zweite Reproduktion am echten Host fand, dass der Response-Companion ohne
Lease eine Host-413 vor Autorisierung überschrieb. Die eng begrenzte Fortsetzung
verlangt jetzt typisierte interne Hostattribute, deren exakten Namespace/Detail/
Status, keine ext_authz-Metadaten und kanonische Response-Header. Beliebige
unmarkierte 413, Client-Header und falsche/fehlerhafte Attribute scheitern weiter.
Echte Kontrollen mit gepinntem Envoy 1.39.1 in On und DetectionOnly beobachten
44 Bytes am 33-Byte-Hostbuffer mit 413, null Autorisierungs-/native Events/EOS,
keinen Upstream und einen erfolgreichen kleinen P1–P4-Kontrollrequest im selben
Prozess.

Die erneute Hostmatrix fand außerdem Timeout-Cleanup verwaister Leases ohne
terminalen Übergang an Common. Beobachteter Lease-Ablauf zeichnet jetzt Commons
vorhandenen typisierten Timeout vor geprüftem Abschluss und Freigabe auf.
P3/P4/EOS und Hoststatus werden nicht erfunden. Der kontrollierte Coordinator-
Neustart zeichnet entsprechend den vorhandenen typisierten Connector-Fehler-
Übergang auf. Sein Harness verlangt jetzt die tatsächliche Client-500 des
gepinnten Hosts und genau ein erfolgreiches Neustart-Cleanup; fehlgeschlagene,
abweichende und doppelte Terminalevents werden
abgelehnt. Echte Tests erhalten Phasenfehler gewöhnlicher unvollständiger
Abschlüsse, physische Event-Sink-Fehler, die erste Cleanup-Ursache und einmalige
Freigabe. Die unabhängige Receipt-/Projection-Suite besteht 19 Tests. Der
[Envoy-1.39.1-Vertrag](https://raw.githubusercontent.com/envoyproxy/envoy/v1.39.1/api/envoy/extensions/filters/http/ext_proc/v3/ext_proc.proto)
definiert diesen Host-Transportfehlerstatus; eine vorgeschlagene 503-Assertion
wurde auf exakt 500 korrigiert, ohne Produkt-Fehlermapping zu ändern. Aktuelle native Offline-Builds, alle acht
Go-Pakete, 46 Parent-Vertragsprüfungen und 34 gemeinsame Verifier-Tests bestehen.
Der repository-native `quick-check` besteht mit 233 gemeldeten Unittest-Tests;
separate I09-/Apache-/SPOP-Fehlerprüfungen bestehen mit 33/20/19 (305 kombiniert).
Die Referenzprüfung erhält alle 21 aktuellen generierten Ausgaben.

Dies sind ausgewählte aktuelle Host-/Komponentennachweise statt einer
vollständigen Request-/Response-Limitmatrix für zehn Profile. Die oben genannten
Autorisierungs-/Sample-Grenzen bleiben aktiv. Nach dem Folgepush sind frische
CI-/Sonar-Nachweise für den exakten Head erforderlich; die vollständigen Prüfungen
von `ae865899` gelten nur für diesen vorigen Head. Externe Laufevidenz:
`root-checks/envoy-completeness/` im erhaltenen Tasklauf. Aktueller Lieferstatus:
[PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407).


Die finale Envoy-1.39.1-HTTP/1-Composite-Matrix auf eingefrorenem Quellstand
besteht alle 14 ausgeführten Fälle mit 14 verschiedenen erfolgreichen nativen
Terminal-Cleanups. Neun gemeinsame Verifier-Fälle melden `LIFECYCLE_ONLY`; der
kontrolliert unerreichbare Companion liefert seine native Host-500 und schließt
einmal mit Grund `restart`. Fehlende Response-Metadaten und abgelaufene Leases
behalten 503 und geprüftes Timeout-Cleanup. Die beiden On-/DetectionOnly-
Hostbuffer-Kontrollen bestehen mit denselben aktuellen Binaries. P4-Strict-Reset
bleibt ausdrücklich `NOT_RUN`; eine vollständige Zehn-Profil-Limitmatrix wird
dadurch nicht belegt. Quellhashes, Befehle, Receipts, Terminal-Readbacks und der
Nachweis gestoppter Prozesse bleiben erhalten in
`root-checks/envoy-completeness/host/restart-final-validation-status.json`.
