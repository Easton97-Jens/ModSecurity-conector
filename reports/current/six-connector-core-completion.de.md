# Sechs-Connector-HTTP/1.1-Kernabschluss

**Sprache:** [English](six-connector-core-completion.md) | Deutsch

## Evidenzgrenze

Diese kompakte Matrix umfasst nur die ausgewählten echten HTTP/1.1-Hostpfade
und vorhandenen Kern-Katalogfälle. Sie dokumentiert kanonische Lauf-Evidence;
sie behauptet weder einen vollständigen Katalog noch eine Capability-Promotion
oder ein Production-Ergebnis. Strict-Transportbehandlung, HTTP/2, HTTP/3 und
erweiterte Katalogfälle bleiben getrennte Arbeit.

| Connector | P1 | P2 | P3 | P4-Regel | P4 Safe | Erstes Byte | Kein Full Buffer | Cleanup | Aktueller Blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |
| NGINX | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |
| HAProxy | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |
| Envoy | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |
| Traefik | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |
| lighttpd | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Keiner für den kompakten Kern |

## Kanonische gemeinsame Evidence

- Gemeinsame Run-ID: `six-connectors-core-final-20260712T164725Z-e16e7f1`
- Aggregat-Target `full-lifecycle-all-connectors`: Exit `0`; jeder
  ausgewählte Connector-Runner endete mit `0`.
- `make check-six-connector-core-completion`: `PASS`.
- Jeder Aggregat-Connector-Status bleibt ausschließlich wegen der nicht zum
  Kern gehörenden erweiterten Katalogfälle `NOT_EXECUTED`; die obigen
  Kernzeilen sind `PASS`, und kein Lauf meldete `FAIL` oder `BLOCKED`.

## Ausgewählte echte Hostpfade

| Connector | Ausgewählter HTTP/1.1-Hostpfad | Integrationsmodus | Finale Run-ID | Kern-Evidence |
| --- | --- | --- | --- | --- |
| Apache | natives httpd-Modul | `native-httpd-module` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/Alternative, P2 403, P3 403, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |
| NGINX | natives HTTP-Modul | `native-nginx-http-module` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/Alternative, P2 403, P3 403, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |
| HAProxy | nativer HTX-Filter | `native-htx-filter` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/429, P2 403, P3 403, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |
| Envoy | ext_proc-Listener und -Service | `ext_proc` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403, P2 403, P3 403/302-Redirect, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |
| Traefik | native Local-Plugin-Middleware | `native-traefik-middleware` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/429, P2 403, P3 403, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |
| lighttpd | gepatchter nativer Entity-Body-Host | `patched-native-lighttpd` | `six-connectors-core-final-20260712T164725Z-e16e7f1` | P1 Allow/403/Alternative, P2 403, P3 403, P4-Regel 1100301 Safe, EOS, Barriere, Cleanup |

Für jeden ausgewählten Pfad ist das P4-Safe-Event nach Commit ein angefordertes
`deny` mit tatsächlichem `log_only`, sichtbarem HTTP 200, gesendeten
Headern/Body und ohne Connection-Abort. Das synchronisierte First-Byte-
Artefakt ist ein payloadfreier Real-Host-PASS: Der Client erhielt ein Body-
Byte bei pausiertem Upstream, vor dessen EOS und ohne connector-eigenes
vollständiges Response-Buffering. Lifecycle-Zähler sind ausgeglichen, und die
ausgewählten P2-/P4-EOS-Pfade werden einmal pro Transaktion aufgezeichnet. Die
Evidence enthält begrenzte Transaction- und Rule-IDs, aber keine Body-Payloads.

Das Ergebnis behauptet keine per-Chunk-Phase-4-Entscheidung: Response-Body-
Chunks werden inkrementell ingestiert, und die ausgewählte P4-Regel wird dort
bei End-of-Stream ausgewertet, wo Host/Runtime dies melden.

## Connector-Konfigurationsreferenzen

Dies ist ein Abschlussnachweis für Source-zu-Dokumentation, keine zusätzliche
Runtime-, Lifecycle-, Sicherheits- oder Production-Evidence. Das generierte
[Konfigurationsinventar](../connector-configuration-inventory.json) enthält
aktuell 341 Zeilen. Die sechs lokalen Referenzen sowie die zentralen
[Common Runtime](../../examples/common/common-connector-configuration.de.md),
[ModSecurity Engine](../../examples/common/modsecurity-directives.de.md) und
[Regelbeispiele](../../examples/common/rule-examples.de.md) trennen
Connector-Schalter von Engine-Direktiven.

| Connector | Quellgestützte Befunde und dokumentierter Umfang | Referenz und verbleibende Lücke |
| --- | --- | --- |
| Apache | 11 registrierte Apache-Direktiven; 14 dokumentierte Zeilen einschließlich 3 Host-Beispielfeldern; 12 Engine-Direktiven werden von Beispielregeln verwendet. | [Referenz](../../examples/apache/configuration-reference.de.md); verfügbarer Konfigurationscheck bestanden; 0 nicht dokumentierte registrierte Direktiven. |
| NGINX | 10 `ngx_command_t`-Direktiven; 18 dokumentierte Zeilen einschließlich 8 Host-Beispielfeldern; 4 Phase-4-Direktiven sind von `SecRuleEngine` getrennt. | [Referenz](../../examples/nginx/configuration-reference.de.md); verfügbarer Konfigurationscheck bestanden; 0 nicht dokumentierte registrierte Direktiven. |
| HAProxy | 3 native HTX-Filteroptionen; 30 Compatibility-Zeilen sind getrennt (28 SPOP-Parser-Schlüssel plus Compatibility-Filter und ausgemusterte Legacy-Zeile); insgesamt 41 dokumentierte Zeilen. | [Referenz](../../examples/haproxy/configuration-reference.de.md); verfügbarer Konfigurationscheck bestanden; 0 nicht dokumentierte native oder Compatibility-Optionen. |
| Envoy | 66 ausgewählte `ext_proc`-YAML-Felder, 14 Service-JSON-Felder, 5 Service-CLI-Flags und 5 Materializer-Platzhalter; 51 `ext_authz`-Compatibility-Felder sind getrennt; insgesamt 141 dokumentierte Zeilen. | [Referenz](../../examples/envoy/configuration-reference.de.md); verfügbarer Konfigurationscheck bestanden; 0 nicht dokumentierte extrahierte Felder. |
| Traefik | 16 statische und 25 dynamische/native Felder, darunter 7 native Middleware-Felder; 30 `forwardAuth`-Compatibility-Felder sind getrennt; insgesamt 71 dokumentierte Zeilen. | [Referenz](../../examples/traefik/configuration-reference.de.md); verfügbarer Konfigurationscheck bestanden; 0 nicht dokumentierte extrahierte Felder. |
| lighttpd | 2 registrierte Plugin-Schlüssel, 10 ausgewählte gepatchte Hostfelder und 7 Sidecar-Compatibility-Felder; insgesamt 19 dokumentierte Zeilen. | [Referenz](../../examples/lighttpd/configuration-reference.de.md); verfügbarer Konfigurationscheck bestanden; 0 nicht dokumentierte Plugin-Schlüssel. |
| Common Runtime | 25 aktuelle `key=value`-Parser-Schlüssel, alle 25 mit quellenverifizierten Defaults dokumentiert, sofern Parser-/Konfigurationsquellen einen solchen belegen. | [Referenz](../../examples/common/common-connector-configuration.de.md); 0 nicht dokumentierte Schlüssel. |
| ModSecurity Engine | 12 von eingecheckten Beispielregeln verwendete Direktiven, alle 12 dokumentiert; der Regel-Walkthrough trennt Variable, Operator, Actions und Host-Commit-Grenzen. | [Referenz](../../examples/common/modsecurity-directives.de.md); Connector-/Engine-Trennung verifiziert; 0 nicht dokumentierte verwendete Direktiven. |

| Validierung | Ergebnis und Grenze |
| --- | --- |
| Source-to-Documentation-Checker | `make check-connector-config-reference`: PASS; Parser/Registrierung, Konfigurationsvertrag, Beispiel, generierte Referenz und Inventarparität werden gemeinsam geprüft. |
| Bilingual-Parität | `make check-bilingual-docs` und der Paritätscheck für Konfigurationsreferenzen: PASS; Direktivnamen, Syntax, Werte, Defaults, Kontexte, Beispiele, Pfade, IDs und Targets bleiben technisch gleich. |
| Konfigurations-Parse-Checks | `make check-config-all-connectors`: PASS für die verfügbaren ausgewählten Hostchecks; dadurch werden die Dokumentationsprofile nicht zu neuer Lifecycle-Evidence. |
| Platzhalter-Checker | PASS über den quellenbasierten Envoy-Materializervertrag: alle fünf `@...@`-Platzhalter sind inventarisiert, und nicht aufgelöste Platzhalter bzw. Template-Drift lassen den Check fehlschlagen. |
| Profil- und lokale-Pfad-Checker | PASS: erforderliches Minimal-, Safe-, Strict-Grenz-, DetectionOnly- und Disabled-Profilmaterial ist vorhanden; DetectionOnly-/Off-Regeln werden geprüft; Beispieldateien enthalten keinen geprüften entwicklerlokalen Pfad. |
