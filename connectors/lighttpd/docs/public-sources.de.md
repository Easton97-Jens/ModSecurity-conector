# lighttpd Öffentliche Quellen

**Sprache:** [English](public-sources.md) | Deutsch

Status: Host-API-Referenzen für ein Repository-eigenes natives Modul
Laufzeitstatus: `minimal_runtime_smoke` für den angehefteten Phase-1-Header-Pfad

Diese öffentlichen Quellen identifizieren die Host-API und das Projekt, die für die Anheftung verwendet werden
Native-Modul-Build. Es gibt keine Upstream-Connector-Implementierung oder Lighttpd-Quelle
in dieses Connector-Verzeichnis kopiert.

- https://raw.githubusercontent.com/lighttpd/lighttpd1.4/master/src/plugin.h
- https://github.com/lighttpd/lighttpd1.4
- https://redmine.lighttpd.net/projects/1/wiki/Docs_ModMagnet

Das Full-Lifecycle-Profil wählt separat einen kopierten, gepatchten 1.4.84-Host aus
bis `full-lifecycle-lighttpd-patched`. Der Patch ist im Besitz des Repositorys und
Der verfügbare Quellbaum ist keine importierte Connector-Implementierung. Es ist
Die Host-Route der Phase 1 wird weiterhin nicht gefördert.

Jeder zukünftige Quellenimport muss durch dokumentiert werden
`connectors/lighttpd/ORIGIN.md`, `connectors/lighttpd/SOURCE_MAP.json` und die
globale Connector-Gates in
`reports/archive/template-verification-nginx-apache/connector-scaffold-decisions.md`.
