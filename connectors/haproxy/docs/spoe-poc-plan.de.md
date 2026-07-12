# HAProxy SPOE/SPOA PoC-Plan

**Sprache:** [English](spoe-poc-plan.md) | Deutsch

Status: Für den aktuellen Produktions-SPOA-Laufzeitbereich implementiert

Der frühere Plan ist von einer rein geplanten Dokumentation zu einer Live-Dokumentation übergegangen
SPOA-Pfad im Produktionsstil. Im restlichen Plan geht es nun um Beförderungsnachweise
und Produktionshärten.

## Implementiert

- HAProxy startet mit der SPOE-Konfiguration.
- `haproxy-modsecurity-spoa` startet als externe SPOA/SPOP-Komponente.
- Gutartige Anfragen können durchgehen.
- Störende Entscheidungen können durch HAProxy-Durchsetzungsregeln blockiert werden.
- `decision.jsonl` zeichnet Laufzeitentscheidungen auf.
- Audit-Log-Installation ist verfügbar.
- Generierte Berichte werden vom Framework-Berichtsfluss erstellt.

## Verbleibender Plan

- Erweitern Sie die Force-All-FAIL-Untersuchung.
- Fügen Sie Beispiele für Produktionsservice-Manager hinzu.
- Beweisen Sie langfristiges Multi-Worker-Verhalten.
- Definieren Sie Beförderungskriterien für vollständige RESPONSE_BODY-Unterstützung.
- Behalten Sie die generierten Root-Zusammenfassungen konnektorneutral und HAProxy-Details auf Zeilenebene bei
  in generierten HAProxy-Detailberichten.

Phase 4 / RESPONSE_BODY ist `not_implemented` im ausgewählten SPOE/SPOP-Pfad.
Das ehemalige `wait-for-body`-Strict-Abort-Beispiel ist deaktiviert, veraltet und
nichtkanonisch; Es handelt sich nicht um aktuelle Laufzeitbeweise.
