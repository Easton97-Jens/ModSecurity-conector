# HAProxy SPOE/SPOA Harness Design Plan

**Sprache:** [English](design.md) | Deutsch

## Status

documentation_only: true
implementation_status: not_started
runtime_verified: false
harness_executed: false
decision_status: undecided
promoted: false

## Zweck
Dieses Dokument beschreibt nur, welche Aufgaben ein späterer Harness für den
HAProxy SPOE/SPOA-PoC erfüllen müsste. Es enthält keine Implementierung und
beweist keine Laufzeitfähigkeit.

## Rolle des Harness
- Der Harness würde später die PoC-Umgebung vorbereiten.
- Er würde später HAProxy und eine externe SPOA-Komponente starten.
- Er würde später Testrequests senden.
- Er würde später Logs sammeln.
- Er würde später einen Report erzeugen.
- Alles ist planned only / Noch zu prüfen.

The harness contract would be consumed by the central ModSecurity-test-Framework; no tests are stored here.

## Nicht-Ziele
- Kein ausführbarer Harness.
- Keine Prozesssteuerung.
- Kein Netzwerktest.
- Kein HAProxy-Start.
- Kein Agent-Start.
- Kein Request-Test.
- Kein Block/Allow-Nachweis.
- Kein Runtime-Report.
- Keine CI-Integration.

## Geplante Harness-Hooks

| Hook | Zweck | Geplante Inputs | Geplante Outputs | Erfolgskriterium | Status |
|---|---|---|---|---|---|
| prepare | PoC-Verzeichnisse/Platzhalterzustand vorbereiten | Geplante Pfade, geplante Konfig-Platzhalter | Geplanter Arbeitsbereich | Noch zu prüfen. | planned only |
| start | Geplante Startphase für HAProxy und SPOA-Komponente | Geplante Konfigpfade, geplante Prozessparameter | Geplante Prozesszustände | Noch zu prüfen. | planned only |
| send_request | Framework-seitig auszulösende benign/malicious Requests | Geplante Requestdefinitionen aus zentralem Framework | Geplante allow/block-Signale | Noch zu prüfen. | planned only |
| collect_logs | Geplante Logsammlung für Framework-Evidenz | Geplante Logquellen | Geplante Logartefakte | Noch zu prüfen. | planned only |
| stop | Geplantes Stoppen der Prozesse | Geplante Prozessreferenzen | Geplanter Stoppzustand | Noch zu prüfen. | planned only |
| cleanup | Geplantes Aufräumen temporärer Artefakte | Geplante Artefaktliste | Geplanter bereinigter Zustand | Noch zu prüfen. | planned only |
| generate_report | Framework-seitige Reportgenerierung | Geplante Testergebnisse/Logreferenzen | Geplanter Reportpfad im zentralen Framework | Noch zu prüfen. | planned only |

## Hook-Details

### prepare
- Zweck: Geplante Vorbereitungsphase für PoC-Arbeitsbereiche.
- Benötigte Artefakte: Noch zu prüfen.
- Offene Punkte: Pfadmodell, Mindestvoraussetzungen, Fehlerverhalten. Noch zu prüfen.
- Status: planned only.

### start
- HAProxy Start geplant, aber nicht implementiert.
- SPOA-Agent Start geplant, aber nicht implementiert.
- Prozess-/Port-/Timeout-Verhalten: Noch zu prüfen.
- Exakte Startreihenfolge und Abhängigkeiten: Extern zu verifizieren.
- Status: planned only.

### send_request
- benign request geplant.
- malicious request geplant.
- erwartete Ergebnisse: allow/block-signal planned only.
- keine Verifikation aktuell.
- Request-Metadatenvollständigkeit: Nicht belegbar aus dem aktuellen Repository.
- Status: planned only.

### collect_logs
- HAProxy logs planned only.
- Agent logs planned only.
- Korrelation über transaction_id planned only.
- noch kein Log-Schema bewiesen.
- Logfeld-Semantik und Vollständigkeit: Noch zu prüfen.
- Status: planned only.

### stop
- Prozess-Stopp planned only.
- Fehlerverhalten offen.
- Fail-open/fail-closed-relevante Stoppszenarien: Extern zu verifizieren.
- Status: planned only.

### cleanup
- temporäre Dateien/Prozesse planned only.
- offen.
- Grenzen zwischen PoC-Artefakten und externen Ressourcen: Noch zu prüfen.
- Status: planned only.

### generate_report
- geplanter Report liegt ausschließlich im zentralen Test-Framework.
- aktuell nicht vorhanden.
- runtime_verified muss false bleiben, bis echte Ausführung erfolgt.
- Reportfeld-Semantik: Noch zu prüfen.
- Status: planned only.

## Geplantes Report-Schema
Nur planned only; die konkrete Erzeugung erfolgt zentral im
ModSecurity-test-Framework.

## Grenzen / Nicht belegt
- Dass dieser Harness lauffähig ist: Nicht belegbar aus dem aktuellen Repository.
- Dass HAProxy/SPOA mit diesen geplanten Schritten korrekt interagiert: Extern zu verifizieren.
- Dass Block/Allow/Redirect-Semantik vollständig abgedeckt wird: Noch zu prüfen.
- Dass Response-Header/Response-Body zuverlässig verifizierbar sind: Noch zu prüfen.
