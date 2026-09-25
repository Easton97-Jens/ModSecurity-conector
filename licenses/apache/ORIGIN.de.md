# Herkunft und Lizenzreferenz des Apache-Connectors

**Sprache:** [English](ORIGIN.md) | Deutsch

## Herkunft

| Feld | Referenz |
| --- | --- |
| Upstream-Repository | https://github.com/owasp-modsecurity/ModSecurity-apache |
| Branch | `master` |
| Source-Basis | `0488c77f69669584324b70460614a382224b4883` |
| Beobachtete Version | `v0.0.9-beta1-26-g0488c77` |
| Beobachtete Upstream-Lizenz | Apache-2.0 |

Der lokale Apache-Connector verwendet diese Upstream-Quelle als
Provenienzbasis.

## Was hier aufbewahrt wird

| Datei | Herkunft | Zweck |
| --- | --- | --- |
| `licenses/apache/LICENSE` | Upstream-`LICENSE` | Upstream-Apache-2.0-Lizenztext aufbewahren |
| `licenses/apache/AUTHORS` | Upstream-`AUTHORS` | Upstream-Attribution aufbewahren |
| `licenses/apache/CHANGES` | Upstream-`CHANGES` | Upstream-Änderungshistorie/-kontext aufbewahren |

## Unterschied zum lokalen Repository

Der Apache-Connector unter `connectors/apache/` ist kein unveränderter
Checkout von ModSecurity-apache. Er enthält importiertes bzw. abgeleitetes
Upstream-Material zusammen mit repository-lokalen Anpassungen und
repository-eigenen Support-Dateien.

Die verbindliche Herkunft auf Dateiebene steht in
`connectors/apache/SOURCE_MAP.json`. Dort ist festgehalten, welche Dateien auf
der Upstream-Quelle basieren, welche lokalen Änderungen oder zusätzlichen
Source-Basen gelten und welche Dateien repository-eigen sind.

Die Dateien in diesem Verzeichnis dokumentieren Upstream-Herkunft und
Upstream-Lizenzbasis für das relevante Material. Sie definieren keine Lizenz
für nicht zugehörige Dateien oder für das Repository als Ganzes.
