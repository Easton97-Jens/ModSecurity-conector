# Herkunft der Apache-Connector-Lizenz

**Sprache:** [English](ORIGIN.md) | Deutsch

Status: implemented

Dieses Verzeichnis spiegelt die Upstream-Lizenz- und Attributionsdateien für
den kontrollierten Apache-Connector-Quellimport. Phase 11 migrierte den
aktiven Build-Source nach `connectors/apache/src/` und entfernte den früheren
`connectors/apache/upstream/`-Referenzbaum, nachdem ein materialisierter
Apache-Build und Smoke-Run erfolgreich waren. Phase 12 entfernte doppelte
Attributions-/Historien-Dateien aus dem aktiven Source-Baum; dieses Verzeichnis
ist nun der dauerhafte Ort für diese Dateien.

Lokale Repository-Referenz: `connectors/apache/`, `licenses/apache/`
Upstream-Source: https://github.com/owasp-modsecurity/ModSecurity-apache
Source-Branch: `master`
Source-Commit: `0488c77f69669584324b70460614a382224b4883`
Source-Describe: `v0.0.9-beta1-26-g0488c77`
Lizenz: Apache-2.0

| Repository | Lokale Repository-Referenz | Upstream | Beobachteter Commit | Beobachtete Version/Tag | Lizenz |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-apache | `connectors/apache/`, `licenses/apache/` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |

## Dateien

| Zentraler Pfad | Source-Pfad | Zweck |
| --- | --- | --- |
| `licenses/apache/LICENSE` | Upstream `LICENSE` | Apache-2.0-Lizenztext für adaptereigenen Apache-Connector-Source |
| `licenses/apache/AUTHORS` | Upstream `AUTHORS` | Upstream-Attribution |
| `licenses/apache/CHANGES` | Upstream `CHANGES` | Upstream-Änderungskontext |

## Importierte Source-Zuordnung

Die vollständige Dateifür-Datei-Source-Zuordnung bleibt in
`connectors/apache/ORIGIN.md` und `connectors/apache/SOURCE_MAP.json`.
Dieses zentrale Lizenzverzeichnis ist ein Attributionsindex und ersetzt nicht
die funktionalen Apache-Source-Dateien, die für den adaptereigenen
Apache-Autotools-Source-Baum benötigt werden.
