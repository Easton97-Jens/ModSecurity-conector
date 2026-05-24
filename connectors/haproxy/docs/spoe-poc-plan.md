# HAProxy SPOE/SPOA Proof-of-Concept Plan

## Status
poc_status: planned
implementation_status: not_started
runtime_verified: false
decision_status: undecided
promoted: false

## Zweck
Dieser Plan beschreibt nur, welche minimale Evidenz ein SPOE/SPOA-PoC liefern
müsste. Er implementiert nichts und beweist noch keine Funktionsfähigkeit.

## Warum SPOE/SPOA als erste Prüfspur?
SPOE/SPOA ist eine sinnvolle erste Prüfspur, weil HAProxy SPOE als Filter für
externe Komponenten dokumentiert (Extern zu verifizieren) und das Repository
HAProxy als erwartetes Modell mit SPOE oder nativer Extension erwähnt (Belegt
durch Repository).

Die Eignung für vollständige ModSecurity-Semantik ist noch nicht bewiesen.
Noch zu prüfen.

## Nicht-Ziele
- Keine produktive Integration.
- Keine vollständige ModSecurity-Parität.
- Keine Response-Body-Garantie.
- Kein Performance-Versprechen.
- Keine CI-Promotion.
- Keine Änderung an Apache/NGINX.
- Keine Änderung am Makefile.

## Minimale PoC-Fragen
Der PoC muss mindestens beantworten:

1. Kann HAProxy eine Anfrage an eine externe SPOA-Komponente übergeben? (Extern zu verifizieren.)
2. Kann die externe Komponente Request-Metadaten empfangen? (Extern zu verifizieren.)
3. Kann eine harmlose Anfrage erlaubt werden? (Noch zu prüfen.)
4. Kann eine bösartige Anfrage blockiert oder als block-würdig markiert werden? (Noch zu prüfen.)
5. Kann das Ergebnis nachvollziehbar geloggt werden? (Noch zu prüfen.)
6. Kann ein reproduzierbarer Report erzeugt werden? (Noch zu prüfen.)
7. Welche Daten fehlen für ModSecurity? (Noch zu prüfen.)
8. Ist Response-Header-Inspection möglich? (Extern zu verifizieren.)
9. Ist Response-Body-Inspection möglich oder explizit nicht im Scope? (Extern zu verifizieren.)
10. Wie sähe ein Fail-open/Fail-closed-Verhalten aus? (Extern zu verifizieren.)

## Minimaler Scope
In Scope:
- HAProxy startet mit minimaler Testkonfiguration. (Noch zu prüfen.)
- Eine externe SPOA-/Prüfkomponente startet. (Noch zu prüfen.)
- Ein benign request wird erlaubt. (Noch zu prüfen.)
- Ein malicious request wird blockiert oder eindeutig als block-würdig signalisiert. (Noch zu prüfen.)
- Logs werden gesammelt. (Noch zu prüfen.)
- Ein Report wird erzeugt. (Noch zu prüfen.)

Out of Scope:
- Produktionsreife.
- Vollständige CRS-Abdeckung.
- Vollständige Response-Body-Prüfung.
- Performance-Benchmark.
- Packaging.
- CI-Promotion.
- Makefile-Integration.

## Erwartete Harness-Hooks

| Hook | Zweck | Minimaler Erfolg | Offene Punkte |
|---|---|---|---|
| prepare | Testumgebung vorbereiten | Noch zu prüfen. | Noch zu prüfen. |
| start | HAProxy und externe Komponente starten | Noch zu prüfen. | Noch zu prüfen. |
| send_request | Benign/malicious Requests senden | Noch zu prüfen. | Noch zu prüfen. |
| collect_logs | Logs einsammeln | Noch zu prüfen. | Noch zu prüfen. |
| stop | Prozesse stoppen | Noch zu prüfen. | Noch zu prüfen. |
| cleanup | Umgebung bereinigen | Noch zu prüfen. | Noch zu prüfen. |

Hinweis: Hook-Namen sind als allgemeine Harness-Aufgaben im Repository belegt,
aber die HAProxy-spezifische Umsetzung ist extern zu verifizieren.

## Minimaltests

| Test | Zweck | Erwartetes Ergebnis | Status |
|---|---|---|---|
| haproxy_config_syntax | Prüfen, ob Testkonfiguration gültig ist | Noch zu prüfen. | planned |
| haproxy_startup | Prüfen, ob HAProxy startet | Noch zu prüfen. | planned |
| spoa_component_startup | Prüfen, ob externe Komponente startet | Noch zu prüfen. | planned |
| benign_request_allowed | Harmlose Anfrage wird erlaubt | Noch zu prüfen. | planned |
| malicious_request_block_signal | Bösartige Anfrage wird blockiert oder markiert | Noch zu prüfen. | planned |
| logs_emitted | Logs entstehen | Noch zu prüfen. | planned |
| report_generated | Report wird erzeugt | Noch zu prüfen. | planned |

## Evidenzformat
Definiere ein minimales Report-Format als Dokumentation:

```json
{
  "connector": "haproxy",
  "integration_model": "spoe_spoa",
  "validation_mode": "poc",
  "runtime_verified": false,
  "tests": [],
  "open_questions": []
}
```

## Beleglage und Grenzen
- SPOE/SPOA als HAProxy-Mechanismus: Extern zu verifizieren.
- Erwartungsmodell "SPOE oder native extension" im Repository: Belegt durch Repository.
- Vollständige ModSecurity-Semantik über SPOE/SPOA: Nicht belegbar aus dem aktuellen Repository.
- Response-Header/Response-Body-Inspektion im Zielbild: Noch zu prüfen.
- Konkrete Build-Artefakte/Deployment-Details: Nicht belegbar aus dem aktuellen Repository.

## Nächster Schritt
Für SPOE/SPOA die externen HAProxy-Dokumentstellen und einen kleinen
Dokument-Proof gegen diesen Plan erfassen, ohne Code zu schreiben.
