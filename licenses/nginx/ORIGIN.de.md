# Herkunft und Lizenzreferenz des NGINX-Connectors

**Sprache:** [English](ORIGIN.md) | Deutsch

## Herkunft

| Feld | Referenz |
| --- | --- |
| Upstream-Repository | https://github.com/owasp-modsecurity/ModSecurity-nginx |
| Branch | `master` |
| Source-Basis | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` |
| Beobachtete Version | `v1.0.4-14-g9eb44fd` |
| Beobachtete Upstream-Lizenz | Apache-2.0 |

Der lokale NGINX-Connector verwendet diese Upstream-Quelle als
Basis-Provenienz. Zusätzliche upstream-abgeleitete Änderungen und
repository-lokale Anpassungen werden getrennt im Source-Map festgehalten.

## Was hier aufbewahrt wird

| Datei | Herkunft | Zweck |
| --- | --- | --- |
| `licenses/nginx/LICENSE` | Upstream-`LICENSE` | Upstream-Apache-2.0-Lizenztext aufbewahren |
| `licenses/nginx/AUTHORS` | Upstream-`AUTHORS` | Upstream-Attribution aufbewahren |
| `licenses/nginx/CHANGES` | Upstream-`CHANGES` | Upstream-Änderungshistorie/-kontext aufbewahren |

## Unterschied zum lokalen Repository

Der NGINX-Connector unter `connectors/nginx/` ist kein unveränderter Checkout
von ModSecurity-nginx. Der lokale Baum enthält upstream-abgeleiteten Source,
ausgewählte zusätzliche Upstream-Änderungen, repository-lokales
Hardening/Anpassungen und repository-eigene Support-Dateien.

Die verbindliche Herkunft auf Dateiebene steht in
`connectors/nginx/SOURCE_MAP.json`. Dort werden die Basis-Quelle und zusätzliche
Source-/Patch-Provenienz für einzelne Dateien festgehalten.

Die Dateien in diesem Verzeichnis dokumentieren Upstream-Herkunft und
Upstream-Lizenzbasis für das relevante Material. Sie definieren keine Lizenz
für nicht zugehörige Dateien oder für das Repository als Ganzes.
