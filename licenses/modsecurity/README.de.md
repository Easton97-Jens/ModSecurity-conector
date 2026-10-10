# Herkunftsreferenzen der ModSecurity-Engine

**Sprache:** [English](README.md) | Deutsch

Die ModSecurity-Engine-Einträge in diesem Verzeichnis sind ausschließlich
Provenienz-/Referenzinformationen. Dieses Verzeichnis enthält keinen kopierten
ModSecurity-Engine-Source-Baum.

## Referenzbasis

| Engine-Referenz | Upstream | Branch | Commit | Beobachtete Version | Beobachtete Upstream-Lizenz |
| --- | --- | --- | --- | --- | --- |
| ModSecurity v2 | https://github.com/owasp-modsecurity/ModSecurity | `v2/master` | `02eed22d74667b32091eece088a8ebdf64b6ba67` | `v2.9.13` | Apache License 2.0 |
| ModSecurity v3 | https://github.com/owasp-modsecurity/ModSecurity | `v3/master` | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` | Apache License 2.0 |

## Verhältnis zu diesem Repository

ModSecurity v3 ist die primäre libmodsecurity-API-/Architekturreferenz des
Connector-Projekts. ModSecurity v2 bleibt als Kompatibilitäts-, Regressions-,
Semantik- und historische Referenz erhalten.

Der referenzierte Engine-Source liegt außerhalb dieses Repositorys. Dass die
referenzierten Upstream-Versionen eine `LICENSE`-Datei mit Apache License 2.0
enthalten, macht diese Lizenz nicht zu einer repository-weiten
Lizenzdeklaration dieses Projekts.

Connector-Code und andere Dateien in diesem Repository haben ihre eigene
Provenienz. Wenn importierter oder abgeleiteter Source vorhanden ist, ist die
jeweilige Connector-Origin-/Source-Map für die Source-Basis maßgeblich.
