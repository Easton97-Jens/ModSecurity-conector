# HAProxy SPOA Agent Design Plan

**Sprache:** [English](design.md) | Deutsch

## Status

documentation_only: true
implementation_status: not_started
runtime_verified: false
language_selected: false
decision_status: undecided
promoted: false

## Zweck
Dieses Dokument beschreibt nur, welche Aufgaben ein späterer SPOA-Agent
erfüllen müsste. Es enthält keine Implementierung und beweist keine
Funktionsfähigkeit.

## Rolle des Agenten
- Der Agent wäre eine externe Komponente in der SPOE/SPOA-Prüfspur.
  (Belegt durch Repository)
- Er würde später potenziell SPOE/SPOP-Nachrichten empfangen.
  (Extern zu verifizieren.)
- Er würde später potenziell Request-Daten prüfen.
  (Noch zu prüfen.)
- Er würde später potenziell ein Ergebnis an HAProxy zurückgeben.
  (Extern zu verifizieren.)
- Alles ist planned only / Noch zu prüfen.

## Nicht-Ziele
- Keine produktive Integration.
- Keine Sprache festlegen.
- Kein Protokoll vollständig implementieren.
- Kein ModSecurity-Aufruf implementieren.
- Kein CRS laden.
- Kein Response-Body-Support behaupten.
- Kein Performance-Versprechen.
- Kein Fail-open/fail-closed finalisieren.

## Offene Designentscheidungen

| Entscheidung | Status | Warum relevant | Offene Punkte |
|---|---|---|---|
| Programmiersprache | Noch zu prüfen. | Beeinflusst Tooling, Laufzeitmodell, Wartbarkeit. | Keine Sprache final auswählen. |
| SPOP-Protokollbibliothek oder Eigenimplementierung | Extern zu verifizieren. | Kern der SPOE/SPOA-Kommunikation. | API-Reife, Kompatibilität, Fehlermodi. |
| Request-Feldmodell | Noch zu prüfen. | Definiert verfügbare Prüfgrundlage im Agenten. | Feldvollständigkeit nicht bewiesen. |
| Request-Body-Handling | Noch zu prüfen. | Relevanz für tiefergehende Regelprüfung. | Verfügbarkeit/Größenlimits unklar. |
| Response-Header-Handling | Noch zu prüfen. | Relevanz für spätere erweitere Prüfpfade. | Zeitpunkt/Abdeckung unklar. |
| Response-Body-Handling | Noch zu prüfen. | Relevanz für volle Semantik. | Extern zu verifizieren; nicht Minimal-Scope. |
| ModSecurity/libmodsecurity-Anbindung | Noch zu prüfen. | Zentral für echte WAF-Semantik. | Nicht belegbar aus dem aktuellen Repository. |
| Intervention-Mapping | Noch zu prüfen. | Benötigt für block/allow/redirect/log. | Extern zu verifizieren. |
| Fehlerverhalten | Noch zu prüfen. | Stabilität und Sicherheit im Störfall. | Fail-open/fail-closed nicht finalisiert. |
| Logging | Noch zu prüfen. | Nachvollziehbarkeit und Evidenzführung. | Pflichtfelder/Format extern zu verifizieren. |
| Report-Ausgabe | Noch zu prüfen. | Vergleichbare PoC-Ergebnisse. | Felder/Schema final nicht festgelegt. |
| Testbarkeit | Noch zu prüfen. | Nachweisführung ohne Produktionsclaim. | Harness-Kopplung und Messkriterien offen. |

## Geplantes minimales Datenmodell

| Feld | Zweck | Status | Grenze |
|---|---|---|---|
| method | Request-Methode für Basisprüfung | Noch zu prüfen. | Vollständige Semantik nicht bewiesen. |
| uri | Gesamte Ziel-URI | Noch zu prüfen. | Exakte Normalisierung extern zu verifizieren. |
| path | Pfadbasierte Regeln | Noch zu prüfen. | Ableitung/Normalisierung unklar. |
| query | Query-basierte Regeln | Noch zu prüfen. | Feldabdeckung nicht bewiesen. |
| headers | Header-basierte Regeln | Noch zu prüfen. | Canonicalization/Mehrfachwerte unklar. |
| client_ip | Basis-Kontext | Noch zu prüfen. | Quelle/Vertrauensmodell extern zu verifizieren. |
| request_body | Potenziell für Body-Regeln | Noch zu prüfen. | Verfügbarkeit/Größe/Streaming unklar. |
| transaction_id | Korrelation Logs/Entscheidungen | Noch zu prüfen. | Herkunft/Format nicht final. |
| decision | allow/block/log (planned decision) | Noch zu prüfen. | Mapping nicht finalisiert. |
| status_code | Geplanter Rückgabestatus | Noch zu prüfen. | HAProxy-/SPOE-Semantik extern zu verifizieren. |
| log_message | Nachvollziehbarkeit | Noch zu prüfen. | Mindestinhalt/PII-Regeln offen. |

Zusatz:
- response_body: Nicht im Minimal-Scope / Noch zu prüfen.
- intervention mapping: Noch zu prüfen.

## Geplanter Entscheidungsfluss
(alles planned only)

1. Agent erhält Anfrage von HAProxy/SPOE. (planned only)
2. Agent extrahiert verfügbare Request-Metadaten. (planned only)
3. Agent bewertet minimalen Testfall. (planned only)
4. Agent erzeugt planned decision: allow/block/log. (planned only)
5. Agent gibt Ergebnis an HAProxy zurück. (planned only)
6. Agent schreibt Logs. (planned only)
7. Harness sammelt Logs. (planned only)

## ModSecurity-Anbindung
- Eine echte libmodsecurity-Anbindung ist in diesem PoC noch nicht implementiert.
- Ob und wie libmodsecurity aus einem SPOA-Agenten korrekt aufgerufen werden
  kann, ist noch zu prüfen.
- CRS-Abdeckung ist nicht Teil des Minimaldesigns.
- Vollständige ModSecurity-Semantik ist nicht belegbar aus dem aktuellen
  Repository.

## Intervention Mapping

| ModSecurity-Ergebnis | Geplantes HAProxy/SPOE-Ergebnis | Status | Offene Punkte |
|---|---|---|---|
| allow | pass-through (planned only) | Noch zu prüfen. | Extern zu verifizieren. |
| block/deny | deny/block signal (planned only) | Noch zu prüfen. | Extern zu verifizieren. |
| redirect | redirect signal (planned only) | Noch zu prüfen. | Extern zu verifizieren. |
| log only | log signal (planned only) | Noch zu prüfen. | Extern zu verifizieren. |
| error | error/fallback signal (planned only) | Noch zu prüfen. | Fail-open/fail-closed offen. |

## Logging/Report
- Später nötig wären mindestens:
  - request identifier / transaction_id,
  - decision,
  - status_code,
  - log_message,
  - Zeitpunkt/Korrelation.
  (Noch zu prüfen.)
- Aktuell existiert kein Runtime-Report. (Belegt durch Repository)
- `reports/testing/haproxy-spoe-poc-results.generated.md` ist nur planned only.
  (Belegt durch Repository)

## Risiken

| Risiko | Status | Bedeutung |
|---|---|---|
| SPOP-Protokoll unvollständig verstanden | open | Extern zu verifizieren. |
| Request Body unklar | open | Noch zu prüfen. |
| Response Body unklar | open | Noch zu prüfen. |
| libmodsecurity Lifecycle unklar | open | Noch zu prüfen. |
| Intervention Mapping unklar | open | Noch zu prüfen. |
| Fehlerverhalten unklar | open | Noch zu prüfen. |
| Performance unbekannt | open | Noch zu prüfen. |

## Akzeptanzkriterien für dieses Dokument
- Es enthält keine Implementierung.
- Es wählt keine Sprache final aus.
- Es behauptet keine Laufzeitfähigkeit.
- Es markiert alle offenen Punkte klar.
- Es bleibt kompatibel mit dem SPOE/SPOA-PoC-Plan.

## Nächster Schritt
Einen documentation-only Harness-Design-Plan unter
`connectors/haproxy/poc/spoe/harness/design.md` erstellen, ohne Code zu
schreiben.
