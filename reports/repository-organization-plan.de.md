# Plan für die Repository-Organisation

**Sprache:** [English](repository-organization-plan.md) | Deutsch

Dies ist der aus versionierten Dateien erzeugte Vor-Reorganisationsplan. Er dokumentiert vorgeschlagene Verschiebungen vor der Umsetzung und macht keine historischen Berichte zu aktuellen Aussagen.

## Dateien

| Scope | Count |
| --- | ---: |
| Framework | 583 |
| Superproject | 477 |

## Vorgeschlagene Aktionen

| Action | Count |
| --- | ---: |
| `archive` | 45 |
| `generate` | 190 |
| `keep` | 658 |
| `move` | 167 |

## Nächste Schritte

1. Versionierte Dateien mit `git mv` verschieben.
2. Referenzen in Code, Makefiles, Workflows, Tests und Dokumentation reparieren.
3. Generierte Berichte über ihre Source of Truth neu erzeugen.
4. Links, Sprachpartner, Variablen und den Sechs-Connector-Kern validieren.

Das maschinenlesbare Inventar steht in [repository-organization-inventory.json](repository-organization-inventory.json).
