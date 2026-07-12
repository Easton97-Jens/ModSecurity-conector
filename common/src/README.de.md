# common/src

**Sprache:** [English](README.md) | Deutsch

Status: Konservative Hilfsschicht implementiert

Dieses Verzeichnis enthält nur Connector-neutrale Implementierungsdateien. Die Phase 3
Helfer sind ein C-First-Referenzmodell für Metadaten/Statusformen, die die
Python/Shell nutzt Spiegelung in JSON ohne FFI.

Hier erlaubt:

- Helfer, die nur für `common/include/msconnector/*`-Typen funktionieren.
- Reiner Parsing-, Normalisierungs- oder Formatierungscode, der keine Server- oder Proxy-Header enthält.
- Code, der ohne connector-spezifisches SDK erstellt werden kann.
- Kleine neutrale Konstruktoren für gemeinsame Status-/Interventions-/Entscheidungswerte.

Hier nicht erlaubt:

- Server-/Proxy-Hook-Code.
- Kleber für eine bestimmte Laufzeit erstellen.
- Beinhaltet alle Connector-Implementierungen.

Offene Arbeiten werden in `docs/roadmap/todo-inventory.md` verfolgt:

- Beschränken Sie diese Helfer auf Metadaten und Datentypen.
- Fügen Sie keinen Serverlebenszyklus, Anforderungstext, Antwortfilter oder libmodsecurity hinzu
  Eigentumscode hier.
- Verwenden Sie `ci/checks/common/check-common-helpers.sh`, um den isolierten C-Smoke unter zu kompilieren und auszuführen
  `BUILD_ROOT`.
