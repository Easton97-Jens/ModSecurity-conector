# HAProxy SPOE/SPOA Example Syntax Validation

## Status
validation_status: documentation_only
runtime_verified: false
syntax_executed: false
decision_status: undecided
promoted: false

## Zweck
Dieses Dokument prüft nur dokumentarisch, welche Beispielzeilen durch externe
HAProxy/SPOE-Dokumentation gestützt sind. Es führt keine Konfiguration aus und
beweist keine Laufzeitfähigkeit.

## Quellen

| Quelle | URL/Pfad | Abrufdatum | Relevanz |
|---|---|---|---|
| HAProxy Configuration Manual (latest) | https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/ | 2026-05-24 | Externe Einordnung der HAProxy-Directive-Struktur inkl. SPOE-Filterform |
| HAProxy SPOE/SPOP Referenz (via HAProxy-Doku referenziert) | https://raw.githubusercontent.com/haproxy/haproxy/master/doc/SPOE.txt | 2026-05-24 | Externe Detailreferenz für SPOE/SPOP-Syntax und Begriffe |
| Lokale Beispielkonfiguration | connectors/haproxy/poc/spoe/haproxy.cfg.example | 2026-05-24 | Zu validierende example-only HAProxy-Platzhalter |
| Lokale SPOE-Agent-Beispieldatei | connectors/haproxy/poc/spoe/spoe-agent.conf.example | 2026-05-24 | Zu validierende example-only SPOE/SPOA-Platzhalter |
| Lokale Einordnung | connectors/haproxy/poc/spoe/README.md | 2026-05-24 | Dokumentiert example-only/not runtime verified Rahmen |
| Lokale Evidenz | connectors/haproxy/docs/spoe-external-evidence.md | 2026-05-24 | Bereits dokumentierte externe SPOE-Fakten im Repository |

## Validierungsregeln
Jede Zeile/Directive wird mit einem Status markiert:
- externally documented
- repo documented
- illustrative placeholder
- needs external verification
- not proven

## haproxy.cfg.example Abschnittsprüfung

| Abschnitt/Directive | Status | Beleg | Kommentar |
|---|---|---|---|
| `global` | externally documented | HAProxy Configuration Manual (latest) | Abschnittstyp ist extern dokumentiert; konkrete Werte im Beispiel bleiben Platzhalter. |
| `defaults` | externally documented | HAProxy Configuration Manual (latest) | Abschnittstyp extern dokumentiert; Semantik der Beispielwerte nicht runtime-verifiziert. |
| `frontend` | externally documented | HAProxy Configuration Manual (latest) | Abschnittstyp extern dokumentiert. |
| `backend` | externally documented | HAProxy Configuration Manual (latest) | Abschnittstyp extern dokumentiert. |
| `filter spoe [engine <name>] config <file>` (kommentierte Form) | externally documented | HAProxy Configuration Manual (latest) | Nur diese Form ist extern belegt; konkrete Engine-/Pfadwerte im Beispiel sind nicht belegt. |
| SPOE backend (`be_spoe_agent_poc`) | needs external verification | HAProxy Manual + SPOE external evidence (repo) | Dedizierte Backends sind extern erwähnt; konkrete Backend-Topologie im Beispiel bleibt offen. |
| Beispiel-Ports (`:8080`, `:18080`, `:19090`) | illustrative placeholder | Lokale Datei `haproxy.cfg.example` | Platzhalterwerte ohne Produktionsaussage. |
| Timeouts (`5s/30s`) | illustrative placeholder | Lokale Datei `haproxy.cfg.example` | Beispielwerte; Eignung noch zu prüfen. |
| Logging (`log stdout format raw local0`) | needs external verification | HAProxy Manual (allgemein) + lokale Datei | Direktive-Interpretation im konkreten PoC-Kontext nicht bewiesen. |
| Kommentarwarnungen (`example_only`, `runtime_verified: false`, externe Prüfhinweise) | repo documented | `connectors/haproxy/poc/spoe/haproxy.cfg.example` | Konsistent mit lokalem documentation-only Rahmen. |

## spoe-agent.conf.example Abschnittsprüfung

| Abschnitt/Directive | Status | Beleg | Kommentar |
|---|---|---|---|
| Engine/Agent-Abschnitt (`[spoe-engine placeholder]`, `spoe-agent backend ...`) | needs external verification | SPOE/SPOP Referenz + lokale Datei | Als illustrative Struktur angelegt; exakte Syntaxkompatibilität nicht bewiesen. |
| Messages/Events (`[spoe-message ...]`, `event on-frontend-http-request`) | needs external verification | SPOE/SPOP Referenz + lokale Datei | Event-/Message-Form im Beispiel ist nicht runtime-getestet. |
| Request-Metadatenfelder (method/path/query/headers als Kommentar) | illustrative placeholder | Lokale Datei `spoe-agent.conf.example` | Geplante Felder, keine bestätigte Vollständigkeit. |
| Response-Felder | not proven | Lokale Datei + SPOE external evidence | Response-Feldabdeckung im Beispiel nicht belegt. |
| Intervention-Ergebnisfelder (`allow|block|log` placeholder) | illustrative placeholder | Lokale Datei `spoe-agent.conf.example` | Mapping-Semantik ausdrücklich offen; keine Laufzeitbestätigung. |
| Fehler-/Timeout-Verhalten | not proven | Lokale Datei + externe Quellen | Nicht konkretisiert, daher unbewiesen. |
| Kommentare zu Response Body (`Noch zu prüfen.`) | repo documented | `spoe-agent.conf.example` | Korrekt als offen markiert; keine Availability-Behauptung. |
| Kommentare zu Intervention Mapping (`Noch zu prüfen.`) | repo documented | `spoe-agent.conf.example` | Korrekt als offen markiert; kein finales Mapping behauptet. |

## Ergebnis
- Extern dokumentiert sind vor allem die grundlegenden HAProxy-Abschnittstypen
  (`global/defaults/frontend/backend`) und die SPOE-Filterform
  `filter spoe [engine <name>] config <file>`. (Extern belegt)
- Teile mit konkreten Namen, Ports, Timeout-Werten und lokalen Pfaden sind nur
  illustrative placeholders. (Abgeleitet)
- Exakte SPOE-Agent-Syntax, vollständige Feldabdeckung und konkrete
  Laufzeitsemantik bleiben unbewiesen. (Noch zu prüfen / not proven)
- Die Dateien müssen weiterhin klar als example-only/not runtime verified
  behandelt werden. (Belegt durch Repository)

## Nicht bewiesen
- Die Beispielkonfiguration wurde nicht ausgeführt.
- HAProxy wurde nicht gestartet.
- Kein SPOA-Agent wurde gestartet.
- Keine Request-Prüfung wurde durchgeführt.
- Keine Block-/Allow-Entscheidung wurde verifiziert.
- Kein Response-Header-/Response-Body-Verhalten wurde verifiziert.
- Kein Runtime-Report wurde erzeugt.

## Nächster Schritt
Erstelle danach einen documentation-only Agent-Design-Plan unter
`connectors/haproxy/poc/spoe/agent/design.md`, ohne Code zu schreiben.
