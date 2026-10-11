# Stack-Checkliste für Response-Limits

**Sprache:** [English](response-limit-stack-checklist.md) | Deutsch

## Stack-Identität

Basis-PR: [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382).
Basis-Branch: `fix/unified-native-results-events-20260921`.
Exakte Basis: `498653c2a193d34b7b25b2903b1e4db1c45e7f73`.
Neuer Branch: `fix/engine-owned-response-limits-stack-20261011`.
Der neue Draft-PR richtet sich gegen den Basis-Branch; kein Merge ist autorisiert.

## Implementierung

- [x] Common und alle zehn tatsächlichen logischen Adapterprofile inventarisiert.
- [x] Response-Optionen/-Defaults, Metadatengrenzen, SIZE_MAX-Policy-Helper,
  kumulative Byteablehnung und Connector-Kürzung aus Response-Eingabe entfernt.
- [x] Request-Policy, Engine-Access-/MIME-Konfiguration und Hostmodi erhalten.
- [x] Native Response-BODY_LIMIT-Erkennung und erhaltene Interventionen geprüft.
- [x] Technische Frame-/Chunk-/Scratch-/Buffer-/Descriptor-/Header-/Eventgrenzen erhalten.
- [x] Generierte Konfigurationsreferenzen, Beispiele und EN/DE-Zuständigkeitsdokumente aktualisiert.

## Ausführbare Tests

- [x] Konfigurationsinventare und entfernte Optionen; explizite versionierte Fixtures.
- [x] Echte libModSecurity unter/exakt/über Limit, Reject/ProcessPartial, mehrere Chunks,
  unterschiedliche explizite Limits, unterstützte Modi und Payloads über früherem 1 MiB.
- [x] Dateibasierte HAProxy-Binding-Komponententests; gehosteter Adapternachweis bleibt offen.
- [x] Ausgewählte integrierte Common-/Connector-/Sicherheits-/Regressionstests und Dokumentationsprüfungen; Basisfehler unten separat ausgewiesen.
- [ ] Abgeschlossene Sonar-Analyse des neuen PR-Heads: keine neuen Issues/Hotspots und
  keine New-Code-Duplikation; keine Scanner-Ausnahmen oder abgeschwächten Prüfungen.

Common-Validierung mit echter Library bestand 81 Szenarien; HAProxy-Binding-
Validierung bestand 16 Fälle. Envoy bestand acht echte CGo-/libModSecurity-
Packages und den Binary-Build. MRC1-/Observer-Komponentenprüfungen und 31
lighttpd-Gate-/Supervisor-/Namespace-Tests bestanden. Die Stock-Sidecar-Suite
bestand 33/34; ihr RST-Eventfehler und die ältere Common-Lossy-Event-Assertion
wurden auf der Basis reproduziert. Ihre Assertions bleiben erhalten. Der integrierte 57-Test-Lauf im frischen Worktree bestand in 22,053 Sekunden,
einschließlich 81 nativer Common-Szenarien und passender Phase-4-Regel. Der
frische nativ zugeordnete 136-Test-/174-Subtest-Lauf bestand in 44,77 Sekunden.
Common-Verträge, Sicherheitsprüfungen, 21 generierte Referenzen, bilinguale
Dokumentation, Pfade und Links bestanden abschließend. Zwei weitere
native Binding-Erwartungen schlugen unverändert auf der Basis fehl. Ein breiterer
abgebrochener Lauf gilt nicht als bestanden. Apache-C17-
Syntaxprüfung bestand; nativen NGINX-/HAProxy-Prüfungen fehlen Hostartefakte.

## Fehlende echte Hostnachweise

Frische gehostete Lifecycle-Evidence bleibt für jedes folgende Profil getrennt.
Builds, Quellverdrahtung, Stubs und Common-Engine-Tests erfüllen diese Punkte nicht.

- [ ] Apache native gehosteter Lebenszyklus.
- [ ] NGINX native gehosteter Lebenszyklus und Speicher-/Dateibuffer-Auslieferung.
- [ ] HAProxy native HTX gehosteter Lebenszyklus.
- [ ] HAProxy SPOE/SPOP mit native-HTX-Response-Companion gehosteter Lebenszyklus.
- [ ] Envoy ext_proc gehosteter Lebenszyklus.
- [ ] Envoy ext_authz mit Response-Observer gehosteter Lebenszyklus.
- [ ] Traefik native UDS-Middleware gehosteter Lebenszyklus.
- [ ] Traefik forwardAuth mit Response-Observer gehosteter Lebenszyklus.
- [ ] lighttpd Stock-Sidecar gehosteter Lebenszyklus.
- [ ] lighttpd patched native gehosteter Lebenszyklus.

## Sicherheits- und Nachweisgrenzen

Feste Arbeitsbufferkapazität ist kein Engine-Limit. Der aktive lighttpd-Sidecar
streamt feste Scratch-Chunks. Sein gepufferter Legacy-Austausch ist unter
`#if 0` auskompiliert; dessen erhaltene 1-MiB-Kapazität ist keine aktuelle
Response-Grenze der Runtime.
NGINX-Datei-Scratch, MRC1-Frames/Body-Chunks, Envoy-gRPC-Nachrichten, Traefik-UDS,
HAProxy-SPOP-/HTX-Frames, Header-/Eventmetadaten, Overflowprüfungen und
Transporttimeouts bleiben aktiv. Kein historischer Runtime-Bericht gilt für diesen Head.

Siehe [Zuständigkeitsvertrag](phase4-mode-budget.de.md) und
[Change Record](../reports/audits/change-records/CR-20261011-response-limit-policy-removal.de.md).
