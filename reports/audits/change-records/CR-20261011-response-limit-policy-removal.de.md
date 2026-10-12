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

Die Abnahmereparatur ändert zusätzlich Apache-`msc_filters.c` und seine echte
Native-Regression, SPOP-Runtime-/Metadatenfixtures, fünf SPOE-Producer-Beispiele und
zwei Harnesskonfigurationen. Die EN/DE-Paare `docs/phase4-mode-budget`,
`docs/response-limit-stack-checklist` und neu `docs/body-inspection-review-matrix`
erfassen aktuellen Vertrag und Grenzen. Beide Versionen dieses Records werden
aktualisiert; Capability-Evidenz wird durch ausgewählte Proben nicht hochgestuft.

## Ausgeführte Befehle

Der neue Review-Run reproduziert auch den Apache-EOS-Provenienzfehler (drei rote Fälle) und besteht nach Korrektur alle neun echten APR-/Native-Regressionen plus striktes C17. Die externe Mutation der früheren 1-MiB-Grenze lässt die unveränderte echte Marker-Fixture bei Assertion 407 mit Exit 1 scheitern; die unveränderte Common-Suite besteht 13 Methoden/207 Szenarien mit Exit 0. SPOP64-, Envoy-Achtpaket-, Traefik-Protokoll-/API- und Stock-Sicherheitsresultate sind in der Matrix getrennt klassifiziert.

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

Die folgenden erhaltenen Resultate gehören zum früheren Policy-Removal-Run.
Frische Abnahme-Reparaturresultate und ihr engerer Evidenzumfang stehen in der
Matrix der zehn Profile; historische Resultate zertifizieren den finalen
reparierten Head nicht.

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

PR #407 erhält bestehenden Branch und #382-Stack. I09/#408 und I11/#406 sind in
der geprüften Basis; I10/#409 und I12/#410 bleiben getrennt. Kein Merge nach #382/master,
Force-Push oder History-Rewrite ist autorisiert. Tatsächlichen Draft-/Head-/Basisstand
und finale Exact-Head-CI/Sonar aus GitHub statt veraltetem eingebettetem SHA lesen.

Die unabhängige Prüfung reproduzierte zwei PR-eigene Fehler: Apache-Native-Response-
Reject konnte eine zurückgewiesene Brigade vor EOS freigeben oder nach Commit
herabstufen; SPOP-req.body_len konnte ein gepuffertes Präfix als vollständig erklären.
Korrekturen erhalten native Entscheidungen und technische Guards. Aktuelle
Abnahmeschichten und die zwei unabhängigen Basis-Follow-ups stehen in der
[Matrix der zehn Profile](../../../docs/body-inspection-review-matrix.de.md).
Ready for review hängt von allen sieben Kriterien, finalen ausführbaren Prüfungen,
unabhängigem Secretscan und Exact-Head-Remote-Readback ab; es ist keine Mergebereitschaft.
Historische Resultate oben gehören zum früheren Removal-Run, nicht zum neuen
Reparaturhead. Aktuelle Lokal-/Hostnachweise und verbleibende not_run-/blocked-Prüfungen
stehen in Matrix und [Stackcheckliste](../../../docs/response-limit-stack-checklist.de.md).

## Abnahmereparatur-Dateien und finaler lokaler Umfang
Der Apache-Responsezustand trennt beobachtetes Host-EOS von nativer P4-Fehlerfinalisierung. Die Reparatur ändert mod_security3.h/msc_filters.c, die echte Regression, ihr Make-Ziel und Apache-CI-Wiring. SPOP-Fixtures und Producer-Argumente bilden tatsächliches vollständiges Framing ab. Traefik-Protokollchecks erhalten terminales Schließen und alle legitimen Kontrollen auf frischen Peers. Überholte Apache-/Native-Adapter-Quellchecks prüfen die tatsächlichen typisierten Fehlerhelper und erhaltenen nativen Status statt des entfernten connectorgewählten 413-Remaps. HAProxy-Capability-Begründungen beschreiben begrenzte Samples ohne Statuspromotion.

Gepinntes CPython-3.14.7-quick-check: 304 gemeldete Tests, Exit 0; kombinierte Native-/Adapter-Suite: 69 Methoden, Exit 0. Breite Apache-Discovery: 237 Tests, 234 bestanden, drei Foreign-UID-Setupfehler, Gesamt-Exit 1. Diese Fehler sind blockierte Deploymentproben, keine abgeschwächten Assertions. Der getrennte Tree-Secretscan mit 47 Kandidaten bleibt Exit 1; alle Kandidaten wurden unabhängig als unveränderte technische Metadaten/Texte eingeordnet, ohne Scanner-Ausnahmen. Finaler Commit-Range- und Remote-Readback bleiben revisionsgebundene unabhängige Nachweise.
