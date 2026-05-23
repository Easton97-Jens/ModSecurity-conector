# HAProxy SPOE/SPOA External Evidence

## Status

evidence_status: external_initial
decision_status: undecided
implementation_status: not_started
runtime_verified: false
promoted: false

## Zweck
Dieses Dokument sammelt externe HAProxy-Dokumentationsbelege für die
SPOE/SPOA-Prüfspur. Es ist kein Implementierungsplan und kein
Funktionsnachweis.

## Quellen

| Quelle | URL | Abrufdatum | Relevanz |
|---|---|---|---|
| HAProxy Configuration Manual (latest) | https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/ | 2026-05-24 | Externe SPOE/SPOP-Konfigurations- und Mechanismusbelege |
| HAProxy-Doku-Hinweis auf `doc/SPOE.txt` | https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/ | 2026-05-24 | Verweis auf vertiefende SPOE/SPOP-Details |
| Repository: SPOE-PoC-Plan | `connectors/haproxy/docs/spoe-poc-plan.md` | 2026-05-24 | PoC-Fragen und Scope im Projektkontext |
| Repository: Evidence Findings | `connectors/haproxy/docs/evidence-findings.md` | 2026-05-24 | Erste Belegklassifikation im Projekt |
| Repository: Evidence Questionnaire | `connectors/haproxy/docs/evidence-questionnaire.md` | 2026-05-24 | Standardisierter Fragenkatalog |
| Repository: Integration Decision | `connectors/haproxy/docs/integration-decision.md` | 2026-05-24 | Entscheidung bleibt unentschieden |

## Extern belegte SPOE/SPOA-Fakten

| Aussage | Status | Quelle | Bedeutung für PoC | Grenze |
|---|---|---|---|---|
| HAProxy kennt den Konfigurationspunkt `filter spoe [engine <name>] config <file>`. | Extern belegt | HAProxy Configuration Manual (latest), Abruf 2026-05-24 | Zeigt einen offiziellen Einstiegspunkt für SPOE in HAProxy-Konfigurationen. | Kein Beweis für vollständige ModSecurity-Semantik. |
| SPOE ist ein HAProxy-Filter. | Extern belegt | HAProxy Configuration Manual (latest), Abruf 2026-05-24 | Belegt, dass SPOE als Filtermechanismus gedacht ist. | Kein Beweis für konkrete Policy-/Interventionstreue. |
| SPOE kommuniziert mit externen Komponenten. | Extern belegt | HAProxy Configuration Manual (latest), Abruf 2026-05-24 | Unterstützt die PoC-Idee einer externen Prüfinstanz (SPOA). | Datenvollständigkeit für ModSecurity bleibt offen. |
| SPOE nutzt das Stream Processing Offload Protocol (SPOP). | Extern belegt | HAProxy Configuration Manual (latest), Abruf 2026-05-24 | Belegt das Protokollfundament zwischen HAProxy und externer Komponente. | Konkrete Feld-/Event-Abdeckung für ModSecurity: Noch zu prüfen. |
| SPOE benötigt eine eigene Engine-Konfigurationsdatei. | Extern belegt | HAProxy Configuration Manual (latest), Abruf 2026-05-24 | Belegt ein minimales Artefakt, das ein PoC berücksichtigen muss. | Inhaltliche Mindestanforderungen im Projektkontext: Noch zu prüfen. |
| SPOE benötigt dedizierte Backends in der HAProxy-Konfiguration. | Extern belegt | HAProxy Configuration Manual (latest), Abruf 2026-05-24 | Belegt eine notwendige Anbindung externer Komponenten für den PoC. | Betriebs-/Failover-/Timeout-Verhalten: Noch zu prüfen. |
| HAProxy verweist für vollständige SPOE/SPOP-Details auf `doc/SPOE.txt`. | Extern belegt | HAProxy Configuration Manual (latest), Abruf 2026-05-24 | Markiert die primäre Detailquelle für vertiefte externe Prüfung. | Keine unmittelbare Aussage zur ModSecurity-Eignung im Repo. |

## Gegen den PoC-Plan gemappt

| PoC-Frage | Externer Beleg vorhanden? | Status | Kommentar |
|---|---|---|---|
| Kann HAProxy eine Anfrage an eine externe SPOA-Komponente übergeben? | Ja (mechanistisch) | Extern belegt | SPOE-Filter + externe Kommunikation sind dokumentiert; konkrete Request-Felder: Noch zu prüfen. |
| Kann eine externe Komponente grundsätzlich angebunden werden? | Ja | Extern belegt | Dedizierte Backends + SPOE-Mechanismus belegt. |
| Ist klar, welche Engine-Konfigurationsdatei nötig ist? | Teilweise | Extern belegt | Notwendigkeit belegt; konkrete Projektstruktur/Parameter: Noch zu prüfen. |
| Ist klar, welches Backend nötig ist? | Teilweise | Extern belegt | Notwendigkeit dedizierter Backends belegt; konkrete Backend-Topologie: Noch zu prüfen. |
| Ist Request-Metadatenumfang vollständig belegt? | Nein | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. |
| Ist Request-Body-Verfügbarkeit vollständig belegt? | Nein | Noch zu prüfen | Extern zu verifizieren. |
| Ist Response-Header-Inspection belegt? | Nein | Noch zu prüfen | Extern zu verifizieren. |
| Ist Response-Body-Inspection belegt? | Nein | Noch zu prüfen | Extern zu verifizieren. |
| Ist Intervention-Mapping belegt? | Nein | Noch zu prüfen | Nicht belegbar aus dem aktuellen Repository. |
| Ist Fail-open/Fail-closed-Verhalten belegt? | Nein | Noch zu prüfen | Extern zu verifizieren. |
| Ist Logging/Report-Erzeugung belegt? | Teilweise | Abgeleitet | Repository fordert Logs/Report als Validierung, aber SPOE-spezifische Belegkette fehlt noch. |

## Was dadurch stärker wird

- SPOE/SPOA bleibt eine starke erste Prüfspur, weil HAProxy den Mechanismus
  offiziell dokumentiert. (Extern belegt)
- Eine externe Komponente ist konzeptionell belegt. (Extern belegt)
- Engine-Konfiguration und Backend-Anbindung sind als notwendige Artefakte
  belegt. (Extern belegt)

## Was weiterhin nicht bewiesen ist

- vollständige ModSecurity-Semantik (Nicht belegbar aus dem aktuellen Repository)
- Request-Body-Abdeckung (Noch zu prüfen)
- Response-Header-Abdeckung (Noch zu prüfen)
- Response-Body-Abdeckung (Noch zu prüfen)
- Block/deny/redirect-Mapping (Noch zu prüfen)
- Fail-open/fail-closed (Noch zu prüfen)
- Performance/Latenz (Noch zu prüfen)
- konkretes SPOA-Agent-Design (Noch zu prüfen)
- konkrete Build-Artefakte (Nicht belegbar aus dem aktuellen Repository)
- Runtime-Harness (Noch zu prüfen)

## Lua-Abgrenzung

HAProxy dokumentiert `lua-load` und `lua-load-per-thread`. Das belegt
Lua-Unterstützung (Extern belegt), aber nicht, dass Lua für vollständige
ModSecurity-Integration geeignet ist (Noch zu prüfen). Lua bleibt daher eine
separate Prüfspur und ist nicht Teil dieses SPOE/SPOA-PoC-Belegs.

## Vorläufige Bewertung

SPOE/SPOA ist ausreichend belegt, um als erste PoC-Prüfspur geplant zu werden.
SPOE/SPOA ist nicht ausreichend belegt, um als fertige
Integrationsentscheidung oder Implementierung zu gelten.

## Nächster Schritt

Einen nicht-ausführenden Minimal-Artefaktplan für den SPOE/SPOA-PoC erstellen:
welche Dateien später nötig wären, ohne sie jetzt anzulegen.
