# Apache-Architektur

**Sprache:** [English](architecture.md) | Deutsch

Status: Laufzeitpfad im Besitz des Adapters, evidenzbezogen

Der Apache-Connector ist ein Apache-httpd-Modul, das libmodsecurity v3 public C verwendet
APIs. Produktive Quelle steht unter `connectors/apache/src/`; Metadaten erstellen und
Autotools/APXS-Eingaben live unter `connectors/apache/`.

## Laufzeitform

```text
HTTP client -> Apache httpd -> mod_security3.so -> libmodsecurity -> HTTP response
```

Apache besitzt serverspezifisches Verhalten:

- Pre/Post-Konfigurations-Hooks
- Fordern Sie frühe und späte Hooks an
- Eingabefilter
- Ausgabefilter
- Transaktions-Hook protokollieren
- Konfiguration und Zusammenführung pro Verzeichnis
- Interventionskartierung
- Inkrementelle Phase-4-Bucket-Aufnahme, EOS-Finalisierung und strikte Abbruch-Quellenverkabelung

Diese Flächen sind nicht connector-neutral und müssen darunter bleiben
`connectors/apache/`.

## Aktuelle Beweise

- Standard-Laufzeitrauch: `54/54 PASS`.
- Alle Laufzeitbeweise erzwingen: `133 Versuche / 100 PASS / 27 FAIL /
  0 BLOCKIERT / 6 NOT_EXECUTABLE`.
- Aufbau und Smoke-Testfluss: `docs/build/compilers/apache.md`.
- Generierter Detailbericht:
  `reports/testing/generated/apache-runtime-results.generated.md`.

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft. Der Ausgabefilter leitet jeweils weiter
aktuelle Brigade vor EOS und verfügt über keine connector-eigene Gegenrufreaktion
Puffer; Das sichere/strikte Verhalten bleibt so lange auf die Quelle beschränkt, bis ein echter Host-Lauf dies beweist
das für den Kunden sichtbare Transportergebnis.

## Grenzen

Die gemeinsam genutzte Ebene `common/` kann Direktivennamen, Optionsstandards usw. enthalten
Datenformen. Es verfügt nicht über Apache-Hooks, Filter, Bucket-Brigaden und Anfragen
Körperbehandlung, Antwortkörperbehandlung, Transaktionseigentum oder Server
Lebenszyklusverhalten.

## Gemeinsame SDK-Einführungsgrenze

Der Apache-Connector übernimmt das Common SDK für die semantische Konfigurationsspeicherung
und Zusammenführung/Validierung (`msconnector_config`), Direktivennamen/Parserverträge,
Request/Response-Mapper-Verträge, Regelladestatistiken und reine Metadaten-Phase-4
Ereignis-JSONL-Emission. Der Apache-Code bleibt für die Übersetzung von Apache verantwortlich
APIs in diese allgemeinen Modelle.

Immer noch Apache-spezifisch: `command_rec`, `request_rec`, Hooks, Filter, APR-Pools,
Bucket Brigades, APLOG, Apache-Rückgabecodes und APXS/Autotools-Build-Verkabelung.
Dieser Architekturhinweis erhebt keinen Anspruch auf Produktionsbereitschaft, CRS-Abdeckung,
vollständige Matrixabdeckung oder zusätzliches Laufzeitüberprüfungsverhalten.

## C-Standard-Kompilierungsgrenze

Die Apache/Common-Adoption-Schicht wird durch nur kompilierbare C-Standard-Smokes abgedeckt:
C17 ist obligatorisch, während C23 und Future-C optional sind, wenn der Compiler dies unterstützt
diese Modi. Diese Prüfungen kompilieren die Apache-Einführungsquellen und die allgemeinen Quellen
Sie werden als Objekte über die APXS/APR-Einbindungserkennung genutzt. Fehlendes APXS bzw
Apache/APR/libmodsecurity-Header sind eine `BLOCKED`-Bedingung mit dem Exit-Code `77`.
Dies bleibt nur ein Kompilierungs-/Strukturbeweis und ändert nichts an der Apache-Laufzeit.
Produktions-, CRS- oder Vollmatrix-Ansprüche.

## Überprüfen Sie die Grenzen

Der Antwort-Mapper spiegelt jetzt Apache-Antwortmetadaten von `err_headers_out` wider.
`headers_out` und `content_type` in das Common-Response-Modell integrieren, ohne sie zusammenzuführen
mehrwertige Header oder das Hinzufügen von Body-Payloads. Interventionsereignisse der Phase 4 verwenden a
nicht-OK-Common-Status und halten Sie die Kürzung des Textkörpers als Metadaten getrennt von JSON
Schreiberkürzung. Diese Korrekturen erweitern keine Laufzeitansprüche.
