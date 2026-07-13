# ModSecurity-Engine-Referenzquellen

**Sprache:** [English](README.md) | Deutsch

Status: implemented

Die ModSecurity-Engine-Repositories sind schreibgeschützte Referenzeingaben
für dieses Monorepo. Engine-Source-Dateien werden hier nicht importiert.

## Beobachtete Referenzen

| Repository | Lokale Repository-Referenz | Upstream | Branch | Commit | Describe | Rolle |
| --- | --- | --- | --- | --- | --- | --- |
| ModSecurity v2 | `licenses/modsecurity/` | https://github.com/owasp-modsecurity/ModSecurity | `v2/master` | `02eed22d74667b32091eece088a8ebdf64b6ba67` | `v2.9.13` | Referenz für Regression, Semantik und Kompatibilität |
| ModSecurity v3 | `licenses/modsecurity/` | https://github.com/owasp-modsecurity/ModSecurity | `v3/master` | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` | Primäre Architektur-/API-Referenz für libmodsecurity v3 |

## Lizenzbeobachtung

Beide beobachteten Referenz-Repositories enthalten eine Apache License 2.0
`LICENSE`-Datei.
Dieses Monorepo kopiert keine ModSecurity-Engine-Source-Dateien nach `common/`
oder in Connector-Source-Bäume. Jeder künftige Engine-Source-Import muss eine
Herkunftszuordnung auf Dateiebene hinzufügen, bevor Code kopiert wird.

## Grenze

- V3 ist die primäre API- und Architekturreferenz.
- V2 dient als Referenz für Regression, Semantik, Kompatibilität und Historie.
- Keines der beiden Referenz-Repositories darf durch die Build-, Smoke- oder
  Dokumentations-Workflows dieses Monorepos verändert werden.
