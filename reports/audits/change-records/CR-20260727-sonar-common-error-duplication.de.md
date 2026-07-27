# Change Record: Parent-Common-Refaktorierung doppelter Error-Mappings

**Sprache:** [English](CR-20260727-sonar-common-error-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-common-error-duplication |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Lokaler Parent-Kandidat zur Reduzierung von SonarQube-Cloud-Duplikaten in `common/src/error.c`; es wird kein Sonar-Issue-Key als geschlossen behauptet. |
| Grenze | Parent-Common-Implementierung der Error-Beschreibungen, ihr C-Helper-Smoke-Vertrag, der fokussierte statische Vertrag sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Öffentliche Header, öffentliche API/ABI, Connector-Verhalten, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und der externe Sonar-Issue-Status bleiben unverändert. |

## Motivation und Problemstellung

`common/src/error.c` enthielt zwei parallele `switch`-Mappings für jeden
bekannten `msconnector_error_code`: eines für seinen Namen und eines für seine
Standardmeldung. Der Kandidat entfernt diese doppelten Mapping-Daten, ohne
einen Enum-Wert als Array-Index zu behandeln oder Fehlerklassifizierung,
Event-Konvertierung oder Fallback-Verhalten zu ändern.

## Akzeptanzkriterien

- Jeden Namen und jede Standardmeldung der aktuell bekannten Fehlercodes bytegenau erhalten.
- Nur die doppelten Namen-/Standardmeldungs-Mappings durch einen translation-unit-privaten, schlüsselbasierten Lookup ersetzen; `msconnector_error_descriptions[code]` oder ein anderer Enum-indexierter Zugriff ist untersagt.
- Öffentliche Header, Enum-Werte, exportierte Funktionssignaturen und ABI erhalten.
- Die Verträge für bekannte und unbekannte Fehler inklusive `MSCONNECTOR_ERROR_NONE`, aufruferbereitgestellter Meldungen und fail-sicherer Fallbacks für unbekannte Codes erhalten.
- Fokussierte C17-Helper-Abdeckung mit GCC und Clang, fokussierte/statische Verträge sowie ein vollständiges englisch/deutsches Change-Record-Paar mit Indizes pflegen.
- Keine SonarQube-Cloud-Reduktion oder geschlossenen Issues behaupten, bevor eine neue Analyse den exakten ausgelieferten Kandidaten-Head bewertet.

## Implementierungsentscheidung und Begründung

`common/src/error.c` enthält jetzt eine `static const`
`msconnector_error_descriptions[]`-Tabelle, deren explizites
`msconnector_error_code`-Feld den Schlüssel bildet. Der
translation-unit-private Helper `msconnector_error_description_for_code`
führt eine durch die Tabellenlänge begrenzte lineare Suche aus und gibt bei
einem Fehltreffer `NULL` zurück. `msconnector_error_code_name` und
`msconnector_error_default_message` verwenden jeweils dieses Ergebnis und
behalten ihre vorhandenen festen Fallbacks.

Der Ansatz entkoppelt Fehlercode-Werte von Tabellenpositionen: negative,
außerhalb des Bereichs liegende und künftig nicht gemappte Werte können über
einen Enum-Index keinen Speicher auswählen. `msconnector_error_status`,
`msconnector_error_http_status`, `msconnector_error_is_fatal`,
`msconnector_error_set` und `msconnector_error_to_event` bleiben absichtlich
im Verhalten unverändert.

Für jeden aktuell bekannten Code deckt der Helper-Smoke-Vertrag Name,
Standardmeldung, Status, HTTP-Status, Fatal-Flag, erzeugte Event-ID/Event-Level,
Event-Meldung und Decision-Reason ab. Er deckt separat
`MSCONNECTOR_ERROR_NONE`, eine aufruferbereitgestellte Meldung, null Error/Event
Inputs und drei unbekannte Werte ab: `-1`, den nächsten Wert nach
`MSCONNECTOR_ERROR_INTERNAL` und `INT_MAX`.

## Geänderte Dateien

- common/src/error.c
- ci/checks/common/check-common-helpers.sh
- tests/test_sonar_reliability_contract.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

Der übergebene Implementierungs-Handoff meldet die folgenden Befehle; dort, wo
`BUILD_ROOT` steht, wurde ein task-owned externes Build-Verzeichnis verwendet:

- `env BUILD_ROOT=<task-owned external build directory> CC=gcc make check-common-helpers-c17`
- `env BUILD_ROOT=<task-owned external build directory> CC=clang make check-common-helpers-c17`
- `env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_sonar_reliability_contract`
- `make check-common-security-contract`
- `make check-common-sdk-contract`
- `make check-common-flow-integrity`
- `make check-common-memory-safety`
- `git diff --check`
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_bilingual_docs`
- `rtk proxy make check-bilingual-docs`
- `rtk proxy make check-doc-links`
- `rtk proxy git diff --check`

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| C17-Common-Helper-Smoke mit GCC | laut erhaltenem Implementierungs-Handoff bestanden. |
| C17-Common-Helper-Smoke mit Clang | laut erhaltenem Implementierungs-Handoff bestanden. |
| `tests.test_sonar_reliability_contract` | laut erhaltenem Implementierungs-Handoff bestanden; er prüft, dass die Beschreibungstabelle privat und schlüsselbasiert ist und nicht als `msconnector_error_descriptions[code]` angesprochen wird. |
| `make check-common-security-contract` | laut erhaltenem Implementierungs-Handoff bestanden. |
| `make check-common-sdk-contract` | laut erhaltenem Implementierungs-Handoff bestanden. |
| `make check-common-flow-integrity` | laut erhaltenem Implementierungs-Handoff bestanden. |
| `make check-common-memory-safety` | laut erhaltenem Implementierungs-Handoff bestanden. |
| Source-Kandidat `git diff --check` | laut erhaltenem Implementierungs-Handoff bestanden. |
| `tests.test_bilingual_docs` | bestanden: 14 Tests in 0.035s nach Hinzufügen dieses Change-Record-Paars und der Indizes. |
| `make check-bilingual-docs` | bestanden, nachdem der Parent-festgeschriebene Framework-Gitlink in diesem isolierten Kandidaten-Worktree nur lesend initialisiert wurde. |
| `make check-doc-links` | bestanden, nachdem der Parent-festgeschriebene Framework-Gitlink in diesem isolierten Kandidaten-Worktree nur lesend initialisiert wurde. |
| Dokumentationsinklusiver `git diff --check` | nach Hinzufügen dieses Change-Record-Paars und der Indizes bestanden. |

## Security-Auswirkung

Die Änderung berührt eine öffentliche Common-Error-Code-Grenze: Ein
unerwarteter Wert darf weder zu einem Out-of-Bounds-Lookup werden noch den
vorhandenen fail-sicheren Fehlerpfad abschwächen. Die schlüsselbasierte lineare
Suche verwendet eine tatsächliche statische Tabellenbegrenzung, liefert nur
Strings mit statischer Lebensdauer und ändert weder öffentliche Symbole noch
Header. Bei einem Fehltreffer bleibt das vorhandene sichere Verhalten bestehen:
Name `"internal"`, Standardmeldung `"Internal connector error"`, Status
`MSCONNECTOR_STATUS_ERROR`, HTTP-Status `500`, nicht-fatale Klassifizierung und
bei Konvertierung ein `MSCONN_EVENT_INTERNAL_ERROR`-Event auf Level `"error"`.

Das erhaltene unabhängige Security-Review lautet `PASS`: Es fand keine
validierte neue Security-Regression im Kandidaten. Dies ist keine Behauptung,
dass ein nicht verwandter Sicherheitsbefund oder die gesamte SonarQube-Cloud-
Inventur behoben ist.

## Runtime-Evidence

Die erhaltenen C17-Helper-Checks prüfen den Common-Error-Vertrag mit GCC und
Clang. Sie sind schmale Smoke-Evidence auf Komponentenebene, keine Evidence
für Connector-Hosts, Protokollmatrizen oder Produktions-Runtime. Es wurde
keine Framework- oder MRTS-Runtime ausgeführt oder geändert.

## Bekannte Einschränkungen

Die Beschreibungstabelle und die Erwartungstabelle des Helper-Smokes werden
manuell gepflegt. Eine künftige Ergänzung des öffentlichen Enums muss in beide
aufgenommen werden. Wird sie ausgelassen, degradiert die Implementierung sicher
zum vorhandenen Internal-Error-/500-Fallback; das beabsichtigte semantische
Mapping des neuen Enums wäre dann jedoch unvollständig.

Bei Erstellung dieses Records bleibt der Kandidat lokal und uncommitted. Eine
neue SonarQube-Cloud-Analyse des exakten Heads ist weiterhin nötig, um das
tatsächliche Ergebnis für duplicierte Zeilen und verbleibende Findings zu
messen.

## Verbleibende Risiken

Ein versehentlich ausgelassenes aktuelles Mapping könnte Namen oder
Standardmeldung ändern; der erweiterte C-Helper-Vertrag reduziert dieses Risiko
über alle 16 aktuellen Codes. Der lokale statische Source-Vertrag kann für sich
allein weder gehostete Analyse, alle Compiler-/Toolchain-Kombinationen noch
nachgelagertes Connector-Verhalten beweisen.

Aus diesem Kandidaten folgt keine Aussage über die gemeldete projektweite
Duplikatdichte von `0.4%`, nicht verwandte SonarQube-Cloud-Zeilen oder einen
ausgelieferten PR, bis der exakte Kandidaten-Head frische gehostete Checks und
eine Analyse abgeschlossen hat.

## Nicht ausgeführte Prüfungen mit Begründung

- Für diesen lokalen/uncommitted Kandidaten gibt es keine neue SonarQube-Cloud-Analyse eines exakten Kandidaten-Heads, kein GitHub-CI-Ergebnis, keinen Commit, Push, Pull Request, Review oder Merge; daher wird keine externe Issue-Disposition oder Duplikatreduzierung behauptet.
- Der Parent-festgeschriebene Framework-Gitlink wurde ausschließlich zum Ausführen von `make check-bilingual-docs` und `make check-doc-links` nur lesend auf `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` initialisiert; beide bestanden. Es wurden keine Framework- oder MRTS-Quellen, Branches oder Gitlinks geändert.
- Vollständige Connector-Builds, Connector-Host-Smokes, Protokollmatrizen und Produktions-Runtime-Tests wurden für diese fokussierte Common-Mapping-Refaktorierung nicht ausgeführt; sie liegen außerhalb ihres schmalen Validierungsumfangs.
- Framework- und MRTS-Checks wurden nicht ausgeführt, weil kein Framework-, MRTS- oder Gitlink-Inhalt geändert wurde.

## Finaler Diff- und Review-Status

Der lokale Kandidat im Task-Worktree besteht aus dem schlüsselbasierten
Parent-Common-Beschreibungs-Mapping, dem erweiterten Common-Helper-Smoke-
Vertrag, dem fokussierten statischen Vertrag und diesem erforderlichen
zweisprachigen Traceability-Material. Öffentliche Header, API/ABI,
Status-/HTTP-/Fatal-Klassifizierung, Event-Konvertierung und sämtliche
bekannten/unbekannten Fallback-Semantiken bleiben innerhalb der festgelegten
Erhaltungsgrenze.

Der Kandidat ist keine ausgelieferte Änderung. Sein finaler Source- und
Dokumentationsdiff benötigt weiterhin Exact-Head-Delivery-Validierung,
einschließlich einer neuen SonarQube-Cloud-Analyse, bevor er als Reduzierung der
Duplikatdichte oder Behebung eines externen Issues dargestellt werden darf.
