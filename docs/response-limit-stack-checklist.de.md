# Stack-Checkliste für Request-/Response-Body-Limits

**Sprache:** [English](response-limit-stack-checklist.md) | Deutsch

## Stack und Auslieferung

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

## Implementierung und erhaltene Verifikation

- [x] Alle zehn logischen Profile verfolgen; Common-/Adapter-/Service-Bodypolicy für Request/Response, Defaults, Parser-/Merge-/Fallbackentscheidungen und Connector-`body_limit_action` entfernen.
- [x] Limits/Aktionen nativ belassen, entfernte Schlüssel ablehnen; operationsspezifische Ergebnisse, DetectionOnly, Pending-Interventionen und einmaligen Abschluss/Cleanup erhalten.
- [x] Vollbody-Allokation/Fallbacks durch inkrementelle Verarbeitung/private Dateipufferung ersetzen und technische Guards erhalten.
- [x] Explizite richtungsspezifische Engine-Policy in Inspektionsfixtures, EN/DE-Quellen, Beispielen und generierten Referenzen pflegen.
- [x] Exakte Head-Gates ohne neue Issues/Hotspots/Duplikation erhalten und erzwingen; dieser Punkt bezeichnet Kontrollen, keinen aktuellen bestandenen Scan.
- [ ] Alle aktiven Vollbody-/Sample-Grenzen entfernen: Die konkreten Einschränkungen unten bleiben bestehen.

## Verifizierte lokale und ausgewählte Hostnachweise

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

## Aktive Einschränkungen

Vollständige Entfernung über alle aktiven Profile wird nicht behauptet. Envoy-
Composite-Samples erfordern `allow_partial_message: false`; partielle/fehlerhafte/
mehrdeutige Vollständigkeitsmetadaten werden vor Common-Open/Body/EOS/Lease-
Erzeugung abgelehnt, ohne Adapter-Größenschwelle oder gewählte native Aktion.

| Aktive Route | Verbleibende Grenze und tatsächlicher Wirkungsbereich |
| --- | --- |
| Envoy ext_authz | Host-`max_request_bytes=4096/33` begrenzt das vollständige an die Autorisierung gesendete Request-Sample; sein Response-Observer macht die Request-Eingabe nicht inkrementell. |
| Traefik forwardAuth | Host-`maxBodySize=4096/33` begrenzt den gepufferten Autorisierungsrequest. |
| Composite-Traefik-Autorisierungsantwort | Host-`maxResponseBodySize=32768` begrenzt die Autorisierungsantwort, nicht die Response der Upstream-Anwendung. |
| HAProxy SPOE/SPOP | Ein Request-Sample je begrenzter Protokollnachricht/Frame; ein unvollständiges Sample scheitert vor der Engine mit Admission-Status 503, nicht nativem `BODY_LIMIT`. Natives HTX ist separat. |

Unabhängige Hostpolicies wie lighttpd `server.max-request-size` bleiben ebenfalls.

## Technische Sicherheit und Deployment-Lücken

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

Tatsächliche Fremd-UID- und Read-only-Mount-Prüfungen blockiert diese Umgebung:
UID/GID-Mappings enthalten nur root, Fremd-UID-`chown` liefert EINVAL und isolierte
User-/Mount-Namespaces liefern EPERM. Vorhandene gecachte Host-Binaries belegen
weder aktuelle Modulprovenienz noch die vollständige Laufzeitmatrix.

## Fehlende vollständige Hostmatrix

Allen zehn Profilen fehlt weiterhin die vollständige aktuelle Request-/Response-
Limitmatrix einschließlich Protokolllebenszyklus, Host-Ownership/Commit-Zeitpunkt
und Late-Abort-Nachweis. Die 14 ausgewählten Envoy-HTTP/1-Fälle schließen diese
breiteren Kriterien nicht.

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

## Sonar- und Nachweisgrenzen

Historische Analysen gelten für ihre Revision: `cec340f3` meldete 32 Issues
und sieben Duplikationsblöcke/65 Zeilen; `dc33ffef` behielt sechs Smells;
`ef4e90dc` behielt ein Issue bei null Hotspots und Duplikation. Diese erfüllen
die strikte Null-Neuissue-Vorgabe nicht. Reparaturen erhalten Prüfungen/Assertions
und führen keine Scanner-Ausnahmen oder schwächeren Gates ein. Frühere bestandene
Heads verifizieren keine späteren Änderungen. Neuester exakter Head-Status steht
in den Live-PR-Checks.

Erhaltene externe Nachweise: `common/sonar-cec/`, `native/sonar-cec/`,
`remaining/sonar-cec/`, `root-checks/ci-fixture-repairs-final.log` und
`root-checks/envoy-completeness/` einschließlich
`host/restart-final-validation-status.json`. Siehe
[Zuständigkeitsvertrag](phase4-mode-budget.de.md) und
[Change Record](../reports/audits/change-records/CR-20261011-response-limit-policy-removal.de.md).
