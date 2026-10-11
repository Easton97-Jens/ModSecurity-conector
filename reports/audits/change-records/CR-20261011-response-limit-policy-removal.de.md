# Change Record: CR-20261011-response-limit-policy-removal

**Sprache:** [English](CR-20261011-response-limit-policy-removal.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261011-response-limit-policy-removal |
| Datum (UTC) | 2026-10-11 |
| Basis-Revision | `2619b20b9d2e70fa07cbe71f664b48ff3c105380` |


## Motivation und Problemstellung

Der Nutzer erweitert #407 auf beide Richtungen und hebt den Request-Policy-Erhalt ausdrücklich auf. Connector-Größenpolicy darf nicht vor libModSecurity entscheiden. Request-Limits/-Aktionen gehören zu `SecRequestBodyLimit`, `SecRequestBodyNoFilesLimit` und `SecRequestBodyLimitAction`; Response-Policy zu `SecResponseBodyLimit`/`SecResponseBodyLimitAction`.

## Akzeptanzkriterien

Connector-Felder/Defaults/Merge-/Parser-/Fallback-Gates, injizierte Direktiven, abgeleitete Engine-Limits und Connector-Präfix-/Aktionsauswahl entfernen. Native Ergebnisse, DetectionOnly, Phasenabschluss, Cleanup und technische Schutzmaßnahmen erhalten. Fixtures wählen passende Engine-Policy explizit; entfernte Schlüssel lassen Konfiguration fehlschlagen. EN/DE-/generierte Referenzen und strikte exakte Head-Sonar-Gates pflegen. Aktive Grenzen und Hostlücken ohne vollständige Entfernungsbehauptung melden.

## Implementierungsentscheidung und Begründung

Common-`request_body_limit`, `response_body_limit`, `body_limit_action`, Request-/Response-Defaultmakros und entsprechende Adapter-/Serviceoptionen sind entfernt. Native Append-Ergebnisse und Pending-Interventionen überleben EOS; `bytes_inspected` bezeichnet angebotene Bytes statt nativem Teilpräfix. Inkrementelle Socket-/Dateiverarbeitung und privates Spool-Replay ersetzen Vollbody-Fallbacks. Vollständige Autorisierungssamples sind vor nativem P2 erforderlich; typisierte Local-Reply- und Terminalübergänge erhalten tatsächliche Host-Ergebnisse.

## Geänderte Dateien

Common-Verträge/Runtime/Autorisierungstransport; Apache-, NGINX-, HAProxy-, Envoy-, Traefik- und lighttpd-Eingabe/Services/Harnesses/Tests; Konfigurations-/Compilergeneratoren und generierte EN/DE-Referenzen; Beispiele, Connector-README-Paare und Zuständigkeits-/Stackdokumentation. Keine Framework-/MRTS-Quellen oder Dependency-Manifeste werden geändert.

## Ausgeführte Befehle

Repository-native `make quick-check`, `check-i09-native-routes`, `check-apache-event-sink` und `check-haproxy-spop-event-sink` bestanden mit unten genannten Zahlen. Echte Engine-, Go-/C-Build-, Hostharness- und Fixtureprüfungen behalten externe Laufprotokolle. Dokumentationsvalidierung nutzt RTK-gewrapptes `make check-bilingual-docs check-doc-links check-connector-config-reference`, `ci/tools/new-change-record.py check` und `git diff --check`. Wiederholte historische Läufe werden nicht summiert.

## Security-Auswirkung

Inkrementelle HTTP-Puffer haben 16 KiB, Dateiscratch 32 KiB und MRC1-Frames/
Body-Chunks 64/32 KiB. Pointer-/Overflow-/Dateibereichs-/Descriptor-/Nachrichten-/
Header-/Event-/Timeoutprüfungen bleiben; Darstellungs-Overflow ist technischer
Fehler. Stock-lighttpd verwendet begrenztes RAM und private, sofort entlinkte
0600-Spooldateien, deren Replay erst nach nativem P2-Allow erfolgt. Kein
Gesamtbodylimit oder unbegrenzte RAM-Vollbody-Allokation ersetzt entfernte Policy.
`--spool-directory` wählt optional Speicher; Standard ist der validierte private
Elternpfad von `--config`. Für `/etc` oder Read-only-Konfiguration einen
existierenden kanonischen, vom effektiven UID besessenen, schreibbaren 0700-Pfad
angeben. Startup prüft Elternpfade, No-follow-Descriptoren und Dateierzeugung
vor Bereitschaft; kein `TMPDIR`-/öffentlicher Fallback existiert. Adversarielle
UID-/Mount-Deployment-Nachweise fehlen weiterhin.

## Runtime-Evidence

Echte Common-Tests bestanden 207 native Szenarien über 13 Methoden für
Request-/Response-Grenzen, Aktionen, DetectionOnly, Chunks/Dateien, verschiedene
native Limits und Marker jenseits früherer Grenzen. Same-Payload-/Sockettests
erhalten native 451-/403-/Allow-Ergebnisse ohne doppelte P2-Präfixe. Pending-
Ergebnisse, exaktes EOS und persistenter `/dev/full`-Fehler ohne Replay behalten
ihre Assertions.

Aktueller Repository-`quick-check` bestand 304 gemeldete Unittests; separate
I09-/Apache-/SPOP-Prüfungen bestanden 33/20/19, insgesamt 376 Testausführungen
für diese vier Befehle. Frühere wiederholte Läufe werden nicht hinzugerechnet. Alle acht Envoy-
Go-Packages, echte CGo-/libModSecurity-Builds und Binaries bestanden; Apache-/
NGINX-/HAProxy-C17, Traefik-Go-/C-/Socket-, Common-Sicherheits-/Vertrags- und
Referenzprüfungen bestanden. Alle 21 generierten Ausgaben sind aktuell, mit
22 lighttpd-Inventareinträgen.

Gepinnte Envoy-1.39.1-HTTP/1-Compositevalidierung bestand 14 ausgeführte Fälle
mit 14 unterschiedlichen erfolgreichen Terminal-Cleanups. Neun Verifierfälle
sind `LIFECYCLE_ONLY`; `p4_strict` ist `NOT_RUN`. On-/DetectionOnly-Kontrollen
mit Host-Requestkapazität 33 und nativem Limit 4096 lehnen einen 44-Byte-Request
mit Host-413, null Autorisierungs-/Native-/EOS-Events und ohne Upstream ab;
anschließend besteht ein kleiner P1–P4-Request im selben Prozess. Ein vollständiges
33-Byte-Sample oberhalb des expliziten nativen Limits 32 liefert separat nativ
403. Host-only-Ablehnung erfüllt keinen nativen P2-Nachweis. Typisierte interne
Hostattribute authentifizieren Local-Reply-Fortsetzung; Clientheader wählen sie
nicht. Lease-Ablauf erfasst typisierten Timeout; kontrolliert unverfügbarer/
neu gestarteter Companion liefert tatsächliches Host-500 und einen Restart-
Cleanup. Fehlende Response-Metadaten/abgelaufene Leases behalten 503.

Stock-Sidecar-Validierung bestand 57/58; ihr bekannter RST-Empty-Eventfehler und
die ältere Common-Lossy-Event-Assertion (Exit 134) bleiben zwei Basisdefekte.
Assertions sind erhalten. Ausgewählte Hostnachweise bilden keine vollständige
Zehn-Profil-Bodylimit-Matrix.

## Bekannte Einschränkungen

| Aktive Route | Verbleibende Grenze und tatsächlicher Wirkungsbereich |
| --- | --- |
| Envoy ext_authz | Host-`max_request_bytes=4096/33` begrenzt das vollständige an die Autorisierung gesendete Request-Sample; sein Response-Observer macht die Request-Eingabe nicht inkrementell. |
| Traefik forwardAuth | Host-`maxBodySize=4096/33` begrenzt den gepufferten Autorisierungsrequest. |
| Composite-Traefik-Autorisierungsantwort | Host-`maxResponseBodySize=32768` begrenzt die Autorisierungsantwort, nicht die Response der Upstream-Anwendung. |
| HAProxy SPOE/SPOP | Ein Request-Sample je begrenzter Protokollnachricht/Frame; ein unvollständiges Sample scheitert vor der Engine mit Admission-Status 503, nicht nativem `BODY_LIMIT`. Natives HTX ist separat. |

Dies bleiben konkrete aktive Einschränkungen und werden nicht als Arbeitspufferkapazität umbenannt. Envoy-`allow_partial_message: false` und Vollständigkeitsablehnung verhindern den Abschluss unvollständiger Samples als volles P2. Unabhängige Hostkontrollen wie lighttpd-`server.max-request-size` bleiben.

## Verbleibende Risiken

Vollständige aktuelle gehostete Bodylimit-Nachweise aller zehn Profile, `p4_strict` und adversarielle UID-/Mount-Deploymentprüfungen fehlen. Zwei Basisfehler bleiben. Lokaler/Komponenten-/ausgewählter Hosterfolg belegt keine vollständige Entfernung oder vollständig verifizierte Auslieferung.

## Nicht ausgeführte Prüfungen mit Begründung

Historische Analysen gelten für ihre Revision: `cec340f3` meldete 32 Issues
und sieben Duplikationsblöcke/65 Zeilen; `dc33ffef` behielt sechs Smells;
`ef4e90dc` behielt ein Issue bei null Hotspots und Duplikation. Diese erfüllen
die strikte Null-Neuissue-Vorgabe nicht. Reparaturen erhalten Prüfungen/Assertions
und führen keine Scanner-Ausnahmen oder schwächeren Gates ein. Frühere bestandene
Heads verifizieren keine späteren Änderungen. Neuester exakter Head-Status steht
in den Live-PR-Checks.

`p4_strict` ist `NOT_RUN`; neun Hostfälle sind nur `LIFECYCLE_ONLY`. Gecachte
Host-Binaries existieren, aber aktuelle Modulprovenienz und vollständige
Profil-Laufzeitnachweise fehlen. Tatsächliche Fremd-UID-/Read-only-Mount-Prüfungen
blockieren UID/GID-Mappings nur für root, Fremd-UID-`chown` EINVAL und isolierte
User-/Mount-Namespaces EPERM. Neueste exakte Head-CI/Sonar wird aus dem PR gelesen,
statt dieses Quelldokument als Live-Statusfeed zu behandeln.

## Finaler Diff- und Review-Status

[Draft-PR #407](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407)
bleibt auf `fix/engine-owned-response-limits-stack-20261011`, gestapelt auf #382-
Branch `fix/unified-native-results-events-20260921`, exakte Basis `2619b20b9d2e70fa07cbe71f664b48ff3c105380`.
Reguläre Commits/Basismerges erhalten veröffentlichte Historie; kein Force-Push,
Rewrite oder PR-/Master-Merge erfolgte. Ausgelieferter Reparaturhead
`455944cfff472d6cf47b8ff0bb252d262adaf804` folgt `ef4e90dc`; er ändert nur Testkomplexität
über äquivalente Acht-Fall-Helperextraktion, erhält alle Assertions und besteht
echte gezielte Tests. Die [Live-PR-Checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/407/checks)
liefern den neuesten exakten Head-Auslieferungsreadback. Die exakte Quellcode-/Testanalyse dieses Heads vom 2026-10-11T19:13:56Z
bestand: Check `114552418608` erfolgreich mit null Annotationen, null offenen/
akzeptierten Issues und Hotspots, acht Rootmetriken und alle 269 gemessenen
Komponenten-Duplikationswerte null; Quality Gate OK ohne ignorierte Bedingungen.
Vier CI-Prüfungen waren bei Erstellung noch offen. Dies belegt diesen Head;
spätere reine Dokumentationscommits verwenden den Live-Readback statt einer
selbstreferenziellen Statusfortschreibung.

Unabhängige Quellcode-/P2-/P4-/EOS-/Sticky-IO-Reviews fanden keinen konkreten offenen Befund. Finale lokale Validierung bleibt getrennt von exakten Head-Remotechecks. Siehe [Stack-Checkliste](../../../docs/response-limit-stack-checklist.de.md).
