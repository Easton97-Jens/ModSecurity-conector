# Drittquellen: Herkunft und Lizenzreferenzen

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis dokumentiert, woher ausgewähltes externes Material in diesem
Repository stammt und welche Upstream-Lizenzinformationen für dieses Material
beobachtet wurden.

Es ist **keine** Lizenzdeklaration für das gesamte Repository. Das Repository
enthält aus Upstream-Quellen abgeleiteten Connector-Code, repository-eigenen
Code, lokale Anpassungen, Dokumentation, Tests, CI-Unterstützung, Beispiele und
generiertes Material. Diese Bereiche haben nicht alle dieselbe Herkunft.

## Herkunftsübersicht

| Komponente | Upstream | Referenzbasis | Verhältnis zu diesem Repository | Upstream-Lizenzreferenz |
| --- | --- | --- | --- | --- |
| Apache-Connector | https://github.com/owasp-modsecurity/ModSecurity-apache | `master` bei `0488c77f69669584324b70460614a382224b4883` (`v0.0.9-beta1-26-g0488c77`) | Teile des lokalen Apache-Connectors sind aus diesem Upstream importiert oder abgeleitet und enthalten repository-lokale Änderungen. | Upstream-Apache-2.0-`LICENSE`, aufbewahrt unter `licenses/apache/` |
| NGINX-Connector | https://github.com/owasp-modsecurity/ModSecurity-nginx | `master` bei `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` (`v1.0.4-14-g9eb44fd`) | Teile des lokalen NGINX-Connectors sind aus diesem Upstream importiert oder abgeleitet und enthalten zusätzliche upstream-abgeleitete sowie repository-lokale Änderungen, die im Source-Map festgehalten sind. | Upstream-Apache-2.0-`LICENSE`, aufbewahrt unter `licenses/nginx/` |
| ModSecurity v2 | https://github.com/owasp-modsecurity/ModSecurity | `v2/master` bei `02eed22d74667b32091eece088a8ebdf64b6ba67` (`v2.9.13`) | Schreibgeschützte Engine-Referenz; durch dieses Referenzverzeichnis wird kein Engine-Source in dieses Repository kopiert. | Apache License 2.0 an der referenzierten Upstream-Quelle beobachtet |
| ModSecurity v3 | https://github.com/owasp-modsecurity/ModSecurity | `v3/master` bei `0fb4aff98b4980cf6426697d5605c424e3d5bb60` (`v3.0.15`) | Primäre libmodsecurity-API-/Architekturreferenz; durch dieses Referenzverzeichnis wird kein Engine-Source in dieses Repository kopiert. | Apache License 2.0 an der referenzierten Upstream-Quelle beobachtet |

## Wichtige Abgrenzung

Die Dateien unter `licenses/apache/` und `licenses/nginx/` bewahren
Upstream-Lizenz-, Autoren- und Änderungsinformationen für das Upstream-Material,
das als Source-Basis verwendet wurde.

Die lokalen Connector-Bäume sind **keine identischen Kopien** dieser
Upstream-Repositories. Sie enthalten repository-lokale Anpassungen und teilweise
weitere upstream-abgeleitete Änderungen. Die Herkunft auf Dateiebene steht in:

- `connectors/apache/SOURCE_MAP.json`
- `connectors/nginx/SOURCE_MAP.json`

Bei Dateien in anderen Bereichen dieses Repositorys darf nicht allein deshalb
angenommen werden, dass sie aus diesen Upstreams stammen oder durch diese
Upstream-Lizenzkopien beschrieben werden, weil sie im selben Repository liegen.

Auf diesem Stand gibt es keine Top-Level-Datei `LICENSE` im Repository.
Für die Herkunft einer konkreten Datei sind die passende Origin-/Source-Map und
dateibezogene Informationen maßgeblich.
