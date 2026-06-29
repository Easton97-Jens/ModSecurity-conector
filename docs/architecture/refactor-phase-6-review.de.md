# Refactor-Phase-6-Überprüfung

**Sprache:** [English](refactor-phase-6-review.md) | Deutsch

Status: umgesetzt

In Phase 6 werden nur Adapter-eigene Quellgerüste eingeführt. Es ersetzt keines
produktiver Apache- oder NGINX-Connector-Pfad.

## Hinzugefügt

| Bereich | Dateien | Grund |
| --- | --- | --- |
| Metadaten des Apache-Adapters | `connectors/apache/metadata.h`, `connectors/apache/metadata.c` | Stabiler Repo-eigener Deskriptor für die Apache-Connector-Quelle und den Lizenzursprung |
| Metadaten des NGINX-Adapters | `connectors/nginx/metadata.h`, `connectors/nginx/metadata.c` | Stabiler Repo-eigener Deskriptor für die NGINX-Connector-Quelle und den Lizenzursprung |
| Validierung des Adapter-Helfers | `ci/check-adapter-helpers.sh` | Kompiliert Adaptermetadaten unter `$BUILD_ROOT` und prüft erforderliche Felder |
| Lint-Integration | `Makefile` | Führt den Adapter-Helfer Smoke als Teil von `make lint` aus |

Nach Phase 13 verbleiben die Adaptermetadaten solange im Connector-Stammverzeichnis
`connectors/nginx/src/ddebug.h` bleibt der Debug-Kompatibilitätsheader
beteiligt sich an generierten NGINX-Build-Kopien.

## Bewusst unverändert

- Apache-Hook-Registrierung.
- Apache-Bucket-Brigaden und Ausgabehelfer.
- Registrierung des NGINX-Moduls.
- NGINX access/header/body-Filter.
- Umgang mit Anfrage- und Response Bodyen.
- Besitz und Lebenszyklus von libmodsecurity-Transaktionen.
- Runtimeinterventionsverhalten.
- YAML-Fälle, frühere expected-failure/mapped-only-Klassifizierungen und `verified_variables`.

## Evidence

Die neuen Adapter-Metadaten werden unabhängig von überprüft
`ci/check-adapter-helpers.sh`. Reale Apache- und NGINX-Smokes bleiben bestehen
RegressionsEvidence, dass sich die unveränderten produktiven Connector-Pfade immer noch so verhalten
vor.

## Risiken

- Metadaten können von `connectors/*/ORIGIN.md` und `licenses/` abweichen. Der Helfer
Smoke fängt leere oder geänderte Pflichtfelder ein, während docs die Quelle bleibt
der detaillierten Zuschreibung.
- Adaptereigene Dateien können mit aktiven Runtimeersetzungen verwechselt werden. Der
Aktuelle Build-Skripte verknüpfen `metadata.c` nicht mit Apache- oder NGINX-Modulen.
- Zukünftige Austauscharbeiten könnten dazu verleitet werden, auch Filter oder Lebenszykluscode zu berühren
früh. Diese Kandidaten bleiben zurückgestellt, bis ein dedizierter Adapter im Besitz ist
Ausführung und Smoke-Nachweis vorhanden.

## Empfehlung für die nächste Phase

Die nächste sichere Phase sollte dafür sorgen, dass die Arbeit des Adapters an Metadaten oder Berichte angrenzt. A
Ein produktiver Ersatz sollte erst versucht werden, nachdem ein enges Verhalten vorliegt:

- eine Repo-eigene Adapterimplementierung;
- Build-Integration isoliert auf `$BUILD_ROOT`;
- before/after reale Apache- und NGINX-Smoke-Evidence;
- Aktualisierte Herkunfts- und Schnittdokumentation.

## Phase 7 Follow-On

Phase 7 ist die erste Verwendung dieser Skelette im Berichtspfad. Es kann serialisiert werden und
Vergleichen Sie Adaptermetadaten in build/runtime-Zusammenfassungen, es darf jedoch immer noch keine Verknüpfung erfolgen
die Metadaten-Helfer in produktive Connector-Module oder Alter Connector
request/response-Verhalten.

## Phase 9 Follow-On

Phase 9 erweitert den NGINX-Adapter-eigenen Baum von metadata/debug-Helfern auf den
vollständige NGINX-Modulquelle. Dieser Nachfolger bleibt NGINX-spezifisch; das tut es nicht
Erstellen Sie die NGINX-Filter, Phasenhandler, das Verhalten des Response Bodys oder die Transaktion
Lebenszyklusteil von Common.
