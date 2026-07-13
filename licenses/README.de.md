# Zentraler Lizenz- und Attributionsindex

**Sprache:** [English](README.md) | Deutsch

Status: implemented

Dieses Verzeichnis ist ein zentraler Index für die Attribution von
Drittquellen in diesem Repository. Es bewahrt eine dauerhafte Attribution,
auch nachdem ein importierter Upstream-Referenzbaum verkleinert oder entfernt
wurde.

## Enthaltene Quellimporte

| Bereich | Lokale Repository-Referenz | Upstream | Importierter Code im Repository | Lizenz | Details |
| --- | --- | --- | --- | --- | --- |
| Apache-Connector | `connectors/apache/`, `licenses/apache/` | https://github.com/owasp-modsecurity/ModSecurity-apache | `connectors/apache/` mit produktivem Quellcode in `connectors/apache/src/`, Attribution in `licenses/apache/` und Herkunft in `connectors/apache/SOURCE_MAP.json` | Apache-2.0 | `licenses/apache/ORIGIN.md` |
| NGINX-Connector | `connectors/nginx/`, `licenses/nginx/` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `connectors/nginx/` mit produktivem Quellcode in `connectors/nginx/src/`, Attribution in `licenses/nginx/` und Herkunft in `connectors/nginx/SOURCE_MAP.json` | Apache-2.0 | `licenses/nginx/ORIGIN.md` |

## Schreibgeschützte Referenzquellen

| Bereich | Lokale Repository-Referenz | Upstream | Importierter Code im Repository | Lizenzhinweis | Details |
| --- | --- | --- | --- | --- | --- |
| ModSecurity v2 | `licenses/modsecurity/` | https://github.com/owasp-modsecurity/ModSecurity | keiner | Apache-2.0 im Quellcode beobachtet | `licenses/modsecurity/README.md` |
| ModSecurity v3 | `licenses/modsecurity/` | https://github.com/owasp-modsecurity/ModSecurity | keiner | Apache-2.0 im Quellcode beobachtet | `licenses/modsecurity/README.md` |

## Regeln

- Bewahren Sie die ursprünglichen Dateien `LICENSE`, `AUTHORS` und `CHANGES`
  in diesem zentralen Attributionsbaum auf. Behalten Sie für
  Connector-Importe, die weiterhin Upstream-Source-Bäume enthalten,
  Upstream-nahe Kopien bei, wenn der Importplan dies verlangt.
- Aktualisieren Sie dieses Verzeichnis, wenn importierte Source-Dateien
  aktualisiert, entfernt oder hinzugefügt werden.
- Kopieren Sie keine Build-Artefakte, generierten Runtime-Dateien oder
  externen Repository-Metadaten in dieses Verzeichnis.
