# HAProxy SPOE/SPOA Minimal Artifact Plan

## Status
artifact_plan_status: planned
implementation_status: not_started
runtime_verified: false
decision_status: undecided
promoted: false

## Zweck
Dieses Dokument beschreibt nur, welche minimalen Artefakte später für einen
SPOE/SPOA-PoC nötig wären. Es erstellt keine Artefakte außer diesem Plan und
beweist keine Funktionsfähigkeit.

## Grundlage
- SPOE/SPOA ist eine erste Prüfspur. (Belegt durch Repository)
- Extern belegt ist nur, dass HAProxy SPOE als Filter für externe Komponenten
dokumentiert. (Extern belegt)
- Nicht belegt ist vollständige ModSecurity-Semantik. (Nicht belegbar aus dem
aktuellen Repository)

## Geplante Minimal-Artefakte

| Geplantes Artefakt | Typ | Zweck | Status | Warum nötig | Offene Punkte |
|---|---|---|---|---|---|
| `connectors/haproxy/poc/spoe/README.md` | Dokumentation | Erklärt den PoC-Scope und Nicht-Ziele. | planned only | Scope-/Grenzdefinition vor jeder Umsetzung. | Noch zu prüfen. |
| `connectors/haproxy/poc/spoe/haproxy.cfg.example` | Beispielkonfiguration | Minimale HAProxy-Konfiguration mit SPOE-Filter und dediziertem Backend. | planned only | Belegt später die geplante Verdrahtung für den PoC. | Exakte Syntax extern zu verifizieren. |
| `connectors/haproxy/poc/spoe/spoe-agent.conf.example` | Beispielkonfiguration | Engine-/SPOE-Agent-Konfiguration. | planned only | Belegt später die notwendigen SPOE-Engine-/Agent-Parameter. | Exakte Direktiven extern zu verifizieren. |
| `connectors/haproxy/poc/spoe/agent/README.md` | Dokumentation | Platzhalter für externe SPOA-Komponente. | planned only | Dokumentiert, welche Agent-Rolle im PoC erwartet wird. | Sprache/Implementierungsmodell noch zu prüfen. |
| `connectors/haproxy/poc/spoe/harness/README.md` | Dokumentation | Geplante Harness-Hooks dokumentieren. | planned only | Align mit Hook-Modell (`prepare/start/send_request/...`). | HAProxy-spezifische Exit-Kriterien noch zu prüfen. |
| `connectors/haproxy/poc/spoe/reports/README.md` | Dokumentation | Ownership-Hinweis für Framework-seitige Reports. | planned only | Trennt Connector-Doku von zentraler Report-Erzeugung. | Framework-Schema noch zu prüfen. |
| Framework-side tests | Zentraler Framework-Inhalt | Framework-side tests: planned in ModSecurity-test-Framework, not in this repository. | planned only | Connector-Repo enthält keine Tests. | Extern zu verifizieren. |
| Framework-side report output | Zentraler Framework-Inhalt | Geplanter Evidenzreport aus zentralem Framework. | planned only | Reports gehören nicht ins Connector-Repo. | Erst nach echter Runtime-Ausführung erzeugen. |

## Nicht jetzt erstellen
- keine lokalen Testdateien
- keine lokalen Testpläne
- keine lokalen Test-READMEs
- keine lokalen Reports
- keine Makefile-Targets
- keine CI-Workflows

## Minimale spätere Ausführungsreihenfolge
Alle Schritte: **planned only**

1. PoC-Verzeichnis anlegen. (planned only)
2. README mit Scope erstellen. (planned only)
3. HAProxy-Beispielkonfiguration entwerfen. (planned only)
4. SPOE-Agent-Konfiguration entwerfen. (planned only)
5. Stub-Agent-Design dokumentieren. (planned only)
6. Harness-Hooks dokumentieren. (planned only)
7. Framework-side tests im ModSecurity-test-Framework planen. (planned only)
8. Erst danach entscheiden, ob Code geschrieben werden darf. (planned only)

## Akzeptanzkriterien für diesen Artefaktplan
Dieser Plan ist akzeptiert, wenn:
- alle Artefakte nur geplant sind,
- keine ausführbaren Dateien erstellt wurden,
- keine Funktionsfähigkeit behauptet wird,
- offene HAProxy/SPOE-Fragen klar markiert sind,
- lokale Tests und lokale Reports nicht als vorhanden dargestellt werden.

## Risiken

| Risiko | Status | Bedeutung |
|---|---|---|
| SPOE-Syntax unvollständig verstanden | open | Extern zu verifizieren. |
| SPOA-Agent-Design unklar | open | Noch zu prüfen. |
| Request Body unklar | open | Noch zu prüfen. |
| Response Header/Body unklar | open | Noch zu prüfen. |
| Intervention Mapping unklar | open | Noch zu prüfen. |
| Runtime-Harness noch nicht vorhanden | open | Nicht belegbar aus dem aktuellen Repository. |

## Nächster Schritt
Den Minimal-Artefaktplan reviewen; danach entscheiden, ob ein rein
dokumentarischer PoC-Ordner mit README-Dateien angelegt werden darf.
