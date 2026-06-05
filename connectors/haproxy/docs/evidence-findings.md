# HAProxy Evidence Findings

## Status

evidence_status: runtime-smoke-verified-single-case
decision_status: partial-diagnostic-spoe-path
implementation_status: diagnostic_runtime_single_case
runtime_verified: true_for_haproxy_phase1_header_block

## Quellen

- Extern belegt: HAProxy Configuration Manual (inkl. SPOE-Filter-Direktive `filter spoe [engine <name>] config <file>`), URL: https://docs.haproxy.org/ , Abrufdatum: 2026-05-24.
- Extern belegt: HAProxy SPOE/SPOP Dokumentation, URL: https://raw.githubusercontent.com/haproxy/haproxy/master/doc/SPOE.txt , Abrufdatum: 2026-05-24.
- Extern belegt: HAProxy Lua-Direktiven (`lua-load`, `lua-load-per-thread`) im HAProxy Manual, URL: https://docs.haproxy.org/ , Abrufdatum: 2026-05-24.
- Belegt durch Repository: HAProxy-Scaffold ist nicht implementiert, URL: `connectors/haproxy/README.md`, Abrufdatum: 2026-05-24.
- Belegt durch Repository: offene HAProxy-Fragen zu Integrationsstrategie/Request-Response/Intervention/Build, URL: `connectors/haproxy/TODO.md`, Abrufdatum: 2026-05-24.
- Belegt durch Repository: standardisierter Fragenkatalog, URL: `connectors/haproxy/docs/evidence-questionnaire.md`, Abrufdatum: 2026-05-24.
- Belegt durch Repository: Integrationsentscheidung bleibt unentschieden, URL: `connectors/haproxy/docs/integration-decision.md`, Abrufdatum: 2026-05-24.

## Kurzfazit

SPOE/SPOA und Lua sind in HAProxy dokumentiert (Extern belegt). Im Repository
existieren inzwischen ein minimaler diagnostic SPOP handshake subset und ein
lokaler libmodsecurity phase-1 Header-Block-Self-Test. Diese Evidenz ist
diagnostisch und self-test-only; HAProxy erzwingt noch keine
ModSecurity-Entscheidung live über SPOA. Native Filter und Sidecar bleiben
Prüfspuren (Noch zu prüfen).

## Findings by Option

### 1. SPOE / SPOA-Agent

| Frage | Status | Evidenz | Offene Punkte |
|---|---|---|---|
| Ist SPOE als Integrationsmechanismus in HAProxy dokumentiert? | Extern belegt | HAProxy dokumentiert `filter spoe [engine <name>] config <file>`. | Keine im Repository aufgelöste Implementierungsableitung; Extern zu verifizieren. |
| Kommuniziert SPOE mit externen Komponenten? | Extern belegt | SPOE wird als Filter mit externer Kommunikation beschrieben. | Konkrete Connector-Architektur für dieses Projekt: Noch zu prüfen. |
| Nutzt SPOE das SPOP-Protokoll? | Extern belegt | SPOE-Doku beschreibt Stream Processing Offload Protocol (SPOP). | Für ModSecurity-Fall benötigte Felder/Vollständigkeit: Noch zu prüfen. |
| Sind alle für ModSecurity nötigen Request-Daten verfügbar? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Ist Response Header Inspection vollständig möglich? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Ist Response Body Inspection möglich/sinnvoll? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Ist vollständiges Intervention-Mapping (deny/block/redirect) möglich? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Welche SPOA-Artefakte sind konkret nötig? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |

### 2. Native Filter / Native Extension

| Frage | Status | Evidenz | Offene Punkte |
|---|---|---|---|
| Sind offiziell unterstützte Filter in HAProxy dokumentiert? | Extern belegt | HAProxy-Dokumentation führt Filterkonzepte/-nutzung auf. | Welche davon für ModSecurity geeignet sind: Noch zu prüfen. |
| Ist ein eigener nativer Filter für dieses Projekt realistisch? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Welche HAProxy-Entwickler-APIs wären nötig? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Ist Neukompilierung oder Modulmechanik nötig? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Ist vollständiges Intervention-Mapping möglich? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |

### 3. Lua

| Frage | Status | Evidenz | Offene Punkte |
|---|---|---|---|
| Ist Lua-Integration in HAProxy dokumentiert? | Extern belegt | HAProxy unterstützt `lua-load` und `lua-load-per-thread`. | Konkrete Eignung für ModSecurity-Lifecycle: Noch zu prüfen. |
| Lädt `lua-load` ein Lua-Programm in gemeinsamen Kontext? | Extern belegt | In HAProxy-Doku als gemeinsamer Kontext beschrieben. | Projektkonkrete Nutzung: Noch zu prüfen. |
| Lädt `lua-load-per-thread` eine Kopie je Thread? | Extern belegt | In HAProxy-Doku als per-thread Kopie beschrieben. | Auswirkungen auf Konsistenz/State: Extern zu verifizieren. |
| Hat Lua Zugriff auf alle nötigen Request-/Response-/Body-Daten? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Ist Lua für Blocking/Intervention geeignet? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Ist Lua für Performance/Produktionsbetrieb realistisch? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |

### 4. Externer HTTP-Service / Sidecar

| Frage | Status | Evidenz | Offene Punkte |
|---|---|---|---|
| Kann HAProxy Requests/Responses in nötiger Form an externen HTTP-Service übergeben? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Sind Sidecar-Latenz und Fehlerverhalten akzeptabel? | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |
| Deckt Sidecar vollständige ModSecurity-Semantik ab? | Nicht belegbar | Nicht belegbar aus dem aktuellen Repository. | Extern zu verifizieren. |

## Auswirkungen auf die Entscheidung

- Keine finale Entscheidung. (Belegt durch Repository)
- SPOE/SPOA ist weiter ein starker Kandidat für Prüfung, weil HAProxy SPOE als
  Filter für externe Komponenten dokumentiert. (Extern belegt)
- Lua ist dokumentiert, aber weiterhin unbewiesen für vollständige
  ModSecurity-Semantik. (Extern belegt + Noch zu prüfen)
- Native Filter bleibt technisch möglich zu prüfen, aber offen. (Extern belegt
  + Noch zu prüfen)
- Sidecar bleibt offen und nicht ausreichend belegt. (Nicht belegbar aus dem
  aktuellen Repository.)

## Nicht belegbar / Noch zu prüfen

- vollständige Request-Body-Verfügbarkeit (Noch zu prüfen)
- Response-Header-Inspection (Noch zu prüfen)
- Response-Body-Inspection (Noch zu prüfen)
- Intervention-Mapping (Noch zu prüfen)
- Build-Artefakte fuer Starter, diagnostic SPOP subset und Binding-Self-Test
  liegen unter `/src/ModSecurity-conector-build`; produktive Build-Artefakte
  bleiben offen.
- Runtime-Harness: `make smoke-haproxy` verifiziert
  `haproxy_phase1_header_block` mit live HAProxy, diagnostic SPOP agent,
  libmodsecurity Entscheidung, set-var ACK, Block-Probe 403 und Pass-Probe
  200.
- Performance/Latenz (Noch zu prüfen)
- Fehlerverhalten (Noch zu prüfen)

## Nächster Schritt

CRS-, RESPONSE_BODY-, negative/pass-through- und Audit/Log-Evidence fuer
HAProxy ergaenzen, bevor ueber den einzelnen Header-Block-Smoke hinaus
promotet wird.
