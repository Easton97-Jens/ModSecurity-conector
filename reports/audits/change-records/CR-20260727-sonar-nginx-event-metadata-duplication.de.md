# Change Record: Parent-NGINX-Event-Metadaten- und JSONL-Writer-Deduplizierungs-Korrekturbatch

**Sprache:** [English](CR-20260727-sonar-nginx-event-metadata-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260727-sonar-nginx-event-metadata-duplication` |
| Datum (UTC) | `2026-07-27` |
| Basis-Revision | `1b0f8825f3510b99b603bb6cd6f0777e1710358e` |
| Korrekturbasis-Revision | `30bd39faf4214dd27f5fd095def71b07d97ccd3b` |
| Zweiter Korrektur-Head | `116a50d0abd7c36471868e7b77d533d1a78ebda5` |
| Tracking | Das frühere Quality Gate an der Korrekturbasis schlug mit `8.6%` New-Code-Duplizierung, zwei S1192-Literal-Kandidaten (`AZ-l0E9Sjq1bd7qgEUwj` und `AZ-l0E9Sjq1bd7qgEUwk`) und einem verbleibenden 22-Zeilen-JSONL-Serializer/Write-Tail-Clone fehl. Der exakte zweite Korrektur-Head hat das beobachtete Quality Gate `OK`, `0` neue duplizierte Zeilen und `0.0%` New-Code-Duplizierung, aber ein neues task-eigenes `python:S1192`-Issue (`AZ-l_JOYhdUH4Iu4ldmS`) in `ci/checks/connectors/nginx/check-nginx-common-adoption.py:68` für die drei Vorkommen von `"msconnector/event_jsonl.h"`. |
| Grenze | Parent-NGINX-Request-Event-Metadaten- und JSONL-Writer-Quelltext, sein Parent-Source-Contract-Checker sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework- und MRTS-Quelltext und Gitlinks, Scanner-Konfiguration, Quality Gates, Remote-Analyse und Delivery bleiben unverändert. |
| Delivery-Status | Der exakte zweite Korrektur-Head hat das oben dokumentierte beobachtete Remote-Quality-Gate `OK`. Zum Zeitpunkt der Erstellung dieses Third-Follow-up-Records war die minimale reine Checker-Korrektur lokal validiert und für den autorisierten normalen Commit-/Draft-PR-Zyklus gestaged. Zu diesem Zeitpunkt war kein dritter Korrektur-Head erzeugt oder gepusht; daher behauptet dieser Record keinen Third-Head-Remote-Erfolg, keine Duplizierungsmetrik, keinen SonarQube-Issue-Abschluss, keinen Push und keinen Merge. |

## Motivation und Problemstellung

Der Intervention-Request-Emitter und der native Rule-Match-Emitter konvertierten
jeweils dieselben drei Request-Werte: `r->method_name`, die Raw-URI
`r->unparsed_uri` und `r->headers_in.content_type->value`. Der Source-Review
identifizierte einen statischen Kandidaten mit `22+22` duplizierten Zeilen: 22
Zeilen in jedem Konvertierungsblock der Emitter. Dies ist Kandidaten-Evidence,
kein frischer SonarQube-Cloud-Duplikatwert, keine Issue-Disposition und kein
Quality-Gate-Ergebnis.

Die begrenzte Remediation entfernt nur diese wiederholte Konvertierung und
erhält die bestehenden eventspezifischen Entscheidungen und JSONL-Schreibpfade.

Das Exact-Quality-Gate von Draft PR #144 für die Korrekturbasis
`30bd39faf4214dd27f5fd095def71b07d97ccd3b` schlug anschließend mit `8.6%`
New-Code-Duplizierung fehl. Seine retained Failure-Evidence besteht aus den
beiden S1192-String-Kandidaten `AZ-l0E9Sjq1bd7qgEUwj` und
`AZ-l0E9Sjq1bd7qgEUwk` sowie dem verbleibenden 22-Zeilen-Serializer/Write-
Tail-Clone. Diese Fakten beschreiben den früheren Remote-Head; sie bewerten
nicht die damalige lokale dritte Korrektur.

Der exakte zweite Korrektur-Head
`116a50d0abd7c36471868e7b77d533d1a78ebda5` erhielt danach das beobachtete
SonarQube-Cloud-Quality-Gate `OK`, `0` neue duplizierte Zeilen und `0.0%`
New-Code-Duplizierung. Dieselbe Analyse eröffnete ein neues task-eigenes
`python:S1192`-Issue, `AZ-l_JOYhdUH4Iu4ldmS`, in
`ci/checks/connectors/nginx/check-nginx-common-adoption.py:68`: Das Literal
`"msconnector/event_jsonl.h"` kam dreimal vor. Die minimale dritte Korrektur
ist ausschließlich lokal; sie hat kein Third-Head-Remote-Ergebnis und keinen
Issue-Abschluss.

## Akzeptanzkriterien

- Nur Method-, Raw-URI- und Content-Type-Konvertierung über einen
  header-lokalen Helper teilen.
- Die etablierten Empty-String-Fallbacks für fehlende, leere, `NULL`- und
  `(char *)-1`-Konvertierungsergebnisse erhalten.
- Event-Ausgabe ausschließlich als Metadaten belassen; keine Request-Body-Daten
  zu einem der JSONL-Events hinzufügen.
- Intervention- und Rule-Match-IDs, Statuswerte, Entscheidungen, Guards,
  Rule-ID-Behandlung und die vorhandenen JSONL-Schreibvorgänge erhalten.
- Tatsächliche fokussierte Source-Check-Ergebnisse, die bestandene isolierte
  C17-Kompilierung gegen das digest-gebundene NGINX-Release-Asset und das
  Fehlen von Modul-Build- und nativer Host-Runtime-Evidence wahrheitsgemäß
  festhalten.
- Nur den gemeinsamen JSONL-Serializer/Write-Tail in einen header-lokalen
  Helper extrahieren und dabei caller-spezifische Guards, Event-Konstruktion,
  diagnostische Meldungen, Return-Verhalten und Warning-Only-Short-Write-
  Verhalten erhalten.
- Die zwei S1192-Python-Literal-Kandidaten ohne Suppressions, Exclusions oder
  Quality-Gate-Änderungen durch benannte Konstanten ersetzen.
- Das exakte Second-Head-Quality-Gate `OK`, `0` neue duplizierte Zeilen,
  `0.0%` New-Code-Duplizierung und das task-eigene `python:S1192`
  `AZ-l_JOYhdUH4Iu4ldmS` wahrheitsgemäß festhalten.
- Nur das neu gemeldete Checker-Literal lokal mit `EVENT_JSONL_HEADER` in
  seiner einen Header-Ownership-Assertion korrigieren, ohne Suppression,
  Exclusion oder Quality-Gate-Änderung.
- Keinen Third-Head-Remote-Erfolg, keine Duplizierungsmetrik, keinen
  SonarQube-Issue-Abschluss, keinen Push, Pull Request oder Merge behaupten,
  bevor Exact-Head-Evidence vorliegt.

## Implementierungsentscheidung und Begründung

`connectors/nginx/src/ngx_http_modsecurity_common.h` enthält nun das
header-lokale `ngx_http_modsecurity_event_request_metadata_t` und den privaten
`static ngx_inline ngx_http_modsecurity_event_request_metadata(...)`-Helper.
Er initialisiert alle drei Felder mit `""`, liefert diese Fallbacks bei `r ==
NULL`, konvertiert nichtleere NGINX-Strings mit `ngx_str_to_char` und übernimmt
einen konvertierten Wert nur, wenn er weder `NULL` noch `(char *)-1` ist. Der
Content Type bleibt an ein vorhandenes, nichtleeres
`r->headers_in.content_type->value` gebunden.

Der Access-/Intervention-Emitter und der native Rule-Match-Emitter rufen den
Helper nur für `event.request.method`, `event.request.uri` und
`event.body.content_type` auf. Die gemeinsame Ausgabe enthält damit nur
Metadaten: Keiner der Emitter fügt `event.body.bytes_seen`,
`event.body.bytes_inspected` oder `r->request_body`-Behandlung hinzu. Die
spätere Writer-Korrektur verschiebt nur ihren identischen Serializer/Write-Tail;
sie erweitert den Metadaten-Helper nicht.

Die Event-Konstruktion bleibt quellspezifisch. Der Intervention-Emitter
verwendet weiterhin `MSCONN_EVENT_REQUEST_BLOCKED`,
`MSCONNECTOR_STATUS_BLOCKED` und seine vorhandene `wanted`-Entscheidung. Der
Rule-Match-Emitter verwendet weiterhin `MSCONN_EVENT_RULE_MATCHED`,
`MSCONNECTOR_STATUS_OK`, die `"pass"`-Entscheidung und seine validierte
`rule_id`. Ihre unterschiedlichen Guards bleiben erhalten. Dies ist ein
header-lokales Implementierungsdetail, keine Änderung einer öffentlichen API
oder des Event-Schemas.

### Lokaler JSONL-Writer-Korrekturbatch

`connectors/nginx/src/ngx_http_modsecurity_common.h` inkludiert nun direkt
`msconnector/event_jsonl.h` und definiert nach dem Metadaten-Helper den
header-lokalen `static ngx_inline int ngx_http_modsecurity_write_event_jsonl(...)`-
Helper. Er besitzt genau einen `char line[4096]`-Serializer/Write-Tail. Er ruft
`msconnector_event_write_jsonl_line` einmal auf; bei einem Serializer-Fehler
behält er die `%s%s`-Warnung einschließlich des Suffixes ` (truncated)` und
liefert `0` zurück. Bei erfolgreicher Serialisierung berechnet er
`ngx_strlen(line)`, ruft `ngx_write_fd` einmal auf, erhält
`written < 0 || (size_t)written != line_length` und die Fehlerauswahl
`written < 0 ? ngx_errno : 0`, loggt die übergebene Literal-Meldung über `%s`
und liefert auch bei negativem oder kurzem Write `1` zurück.

Der Access-Emitter behält seinen `r`/`mcf`/Log-File/fd-Guard, Context-Lookup,
Redirect-versus-Deny-Auswahl, Blocked-Event/-Status und die `wanted`-
Entscheidung. Der native Rule-Match-Emitter behält Rule-ID-Validierung vor dem
Context-Lookup, seinen unterschiedlichen Guard, Matched-Event, `"pass"`-
Entscheidung und validierte `rule_id`. Beide übergeben ihre vorhandenen
Serializer- und Write-Fehler-Literale an den Helper und behalten
`if (!ngx_http_modsecurity_write_event_jsonl(...)) return;`. Damit kehrt nur
ein Serializer-Fehler aus dem Caller zurück; das vorhandene Warning-Only-
Negative-/Short-Write-Verhalten bleibt unverändert. Keiner der Caller
inkludiert nun direkt `msconnector/event_jsonl.h`, ruft Serializer/Writer,
oder besitzt lokale Line-, Truncation-, Length- oder Write-Variablen.

`ci/checks/connectors/nginx/check-nginx-common-adoption.py` ersetzt die zwei
S1192-Body-Counter-Literal-Kandidaten durch `EVENT_BODY_BYTES_SEEN` und
`EVENT_BODY_BYTES_INSPECTED`. Zusätzlich benennt es die vorhandene
No-Request-Body-Assertion `REQUEST_BODY_ACCESS` und prüft den neuen Writer mit
einem Serializer/Write, erhaltenem Warning-/Return-Vertrag, Metadaten-Only-
Umfang, quellspezifischen Guards/Meldungen/Rule-Semantik und Entfernung beider
direkter Caller-Tails. Die exakte Second-Head-Remote-Beobachtung meldete dann
das separate `python:S1192`-Issue `AZ-l_JOYhdUH4Iu4ldmS` in Zeile `68` für
die drei `"msconnector/event_jsonl.h"`-Vorkommen. Die aktuelle minimale dritte
lokale Korrektur definiert
`EVENT_JSONL_HEADER = '"msconnector/event_jsonl.h"'` und verwendet diese
Konstante in der einen Header-Ownership-Assertion. Sie entfernt die drei
gemeldeten Assertion-Vorkommen aus dem aktuellen lokalen Source, behauptet
jedoch keine Remote-Third-Head-Analyse oder keinen Issue-Abschluss.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_log.c`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

Der zweite Korrektur-Head ändert keinen zusätzlichen Product-Pfad: Dieselben
drei NGINX-Dateien enthalten den header-lokalen Writer und seine zwei Caller-
Delegationen, während der vorhandene Source-Contract-Checker die Writer-Grenze
und die zwei früheren S1192-Konstanten abdeckt. Die aktuelle dritte lokale
Korrektur ändert nur
`ci/checks/connectors/nginx/check-nginx-common-adoption.py`; sie fügt
`EVENT_JSONL_HEADER` hinzu und verwendet es in der einen Header-Ownership-
Assertion. Sie verändert weder C-Source noch die reine C17-Source-Evidence-
Grenze oder den NGINX-Runtime-Umfang.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `rtk proxy make check-nginx-common-adoption` | bestanden nach der minimalen dritten lokalen `EVENT_JSONL_HEADER`-Checker-Korrektur; die Prüfung deckt Header-Ownership, einen Serializer/Write-Tail, die No-Body-Grenze, Entfernung direkter Tails und quellspezifische Guards/Meldungen/Rule-Semantik ab. |
| `rtk proxy make check-nginx-c-standard-wiring` | bestanden nach der lokalen Korrektur. |
| `rtk proxy make check-common-helpers` | bestanden: `common_helper_smoke`. |
| `rtk proxy make --no-print-directory check-nginx-c17` | bestanden (Exit `0`): `PASS: nginx_c_standards c17 compile completed` gegen den isolierten, digest-verifizierten NGINX-`release-1.31.2`-Header-Source. Alle Source-, Build- und Include-Roots waren explizit, einschließlich des vertrauenswürdigen bestehenden ModSecurity-Include-Roots. Der Lauf verwendete nur header-only `./configure --with-compat`; NGINX wurde weder gebaut noch installiert oder gestartet. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs` | bestanden: 14 Tests in 0,036 s für dieses reine Korrektur-Update. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs check-doc-links` | bestanden nach diesem englisch/deutschen Second-Head/Third-Local-Evidence-Update: zweisprachige Dokumentation, Repository-Pfadreferenzen und Dokumentationslinks bestanden sämtlich. |
| `rtk git diff --check` | bestanden nach der dritten lokalen Checker-Korrektur und diesem englisch/deutschen Second-Head/Third-Local-Record- und Index-Update. |

## Security-Auswirkung

Request-Methode, Raw-URI und Content Type sind request-abgeleitete Metadaten,
daher wurde die bestehende Logging-Grenze bewertet. Der Helper behält die alten
Fallbacks für fehlende, leere, `NULL`- und `(char *)-1`-Werte und fügt keinen
Parser, keine Allokationsrichtlinie, keine Request-Body-Erfassung, kein
Event-Feld und keinen Sink hinzu. Die Source-Contract-Kontrollen erhalten die
reine Metadatengrenze und die quellspezifische Event-Semantik. Keine
Sicherheitskontrolle wurde geschwächt; dieser Record erstellt, schließt oder
löst kein Security- oder SonarQube-Cloud-Issue.

Ein unabhängiger fokussierter Security-Review fand keine durch dieses reine
Metadaten-Refactoring verursachte Kandidatenregression. Ein bestehender, nicht
validierter Non-UTF8-Assurance-Hinweis bleibt außerhalb des geänderten Umfangs
und wird nicht als Finding oder Remediation-Ergebnis dargestellt.

Die Writer-Korrektur behält dieselbe begrenzte JSONL-Serializer- und
Escaping-Grenze: Ein Serializer-Fehler kehrt zurück, bevor eine Zeile
geschrieben wird, und es kommen weder Request Body noch Event-Feld hinzu. Das
Warning-Only-Handling eines negativen oder kurzen `ngx_write_fd` bleibt
absichtlich erhaltenes Caller-Verhalten, keine neue Availability-/Security-
Behauptung. Der fokussierte Korrektur-Review fand keinen
refactor-eingeführten Security-Kandidaten; der frühere Non-UTF8-Assurance-
Hinweis bleibt außerhalb dieses Batches.

Die dritte Korrektur ändert nur ein Source-Contract-Checker-Literal in die
benannte Konstante `EVENT_JSONL_HEADER`. Sie liest weder Request-Daten noch
ändert sie JSONL-Sink, Parser, Serializer, Allokation, Event, Guard oder die
Logging-Sicherheitsgrenze.

## Runtime-Evidence

Es wurde kein nativer NGINX/libModSecurity-Host-Request ausgeführt. Die
bestandenen fokussierten Prüfungen sind ausschließlich Source-Contract- und
Helper-Evidence; sie beweisen weder ausgerolltes Host-Verhalten, eine
Rule-Entscheidung, client-sichtbare Ausgabe noch Transportkompatibilität.

Die lokalen Writer-Helper-Checks ergänzen keine Host-Runtime-Evidence. Sie
belegen nur Source-Struktur und erhaltene Verträge.

Der isolierte C17-Pass ergänzt ausschließlich Compiler-Evidence; er verändert
die Host-Runtime-Grenze nicht.

## Bekannte Einschränkungen

Der isolierte C17-Check bestand gegen das digest-gebundene NGINX-Release-Asset
`release-1.31.2`, das unter
`/var/tmp/codex/ModSecurity-conector/runs/sonar-open-1022-20260727/nginx-c17`
aufbewahrt wird. Das SHA-256 des Assets
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`
entsprach dem festgelegten Release-Digest. Die Header-Vorbereitung war auf
`./configure --with-compat` mit einem expliziten vertrauenswürdigen bestehenden
ModSecurity-Include-Root beschränkt.

Dies ist ausschließlich Kompilierungs-Evidence: Sie kompiliert die
ausgewählten C-Quellen unter C17, baut oder linkt jedoch weder NGINX noch ein
NGINX-Modul, installiert NGINX nicht, testet keine NGINX-Konfiguration,
startet keinen Service, lädt den Connector nicht, führt keinen Request oder
keine Rule aus und belegt keine Host-, Transport- oder Runtime-Kompatibilität.

Die statischen Source-Contract-Prüfungen prüfen die beabsichtigte
Helper-Adoption und erhaltene Source-Semantik. Sie ergänzen die C17-
Kompilierung, bauen oder starten das NGINX-Modul jedoch nicht gegen eine native
Host-Integration.

Die bestandenen Source-Contract-, C-Standard-Wiring- und Common-Helper-Checks
ersetzen keinen Modul-Build und keinen nativen Host-Request.

## Verbleibende Risiken

Die Zahl `22+22` ist statische Kandidaten-Evidence für die frühere Korrektur,
keine Vorhersage einer zukünftigen Analyse. Der exakte zweite Korrektur-Head
`116a50d0abd7c36471868e7b77d533d1a78ebda5` hat das beobachtete Quality Gate
`OK`, `0` neue duplizierte Zeilen und `0.0%` New-Code-Duplizierung. Diese
Evidence ist auf genau diesen Remote-Head begrenzt und belegt kein Ergebnis für
die aktuelle lokale dritte Korrektur.

Die Second-Head-Analyse eröffnete das task-eigene `python:S1192`
`AZ-l_JOYhdUH4Iu4ldmS` in
`ci/checks/connectors/nginx/check-nginx-common-adoption.py:68` für drei
`"msconnector/event_jsonl.h"`-Literale. `EVENT_JSONL_HEADER` adressiert diese
Assertion-Vorkommen lokal, das Issue bleibt jedoch remote offen, bis ein neuer
exakter dritter Head ausgeliefert und zurückgelesen wird. Der frühere
`8.6%`-Fehler von Draft PR #144 und
`AZ-l0E9Sjq1bd7qgEUwj`/`AZ-l0E9Sjq1bd7qgEUwk` bleiben historische Evidence
für ihren vorherigen exakten Head.

Eine native Integration könnte einen NGINX-Allokations- oder
Lifecycle-Unterschied zeigen, der in den Source-Contracts nicht enthalten ist.
Die erhaltene Fallback-Semantik und der reine Metadatenumfang begrenzen dieses
Risiko, ersetzen jedoch keine native NGINX/libModSecurity-Runtime-Kontrolle.

## Nicht ausgeführte Prüfungen mit Begründung

- Ein nativer NGINX/libModSecurity-Host-Runtime-Request wurde nicht ausgeführt.
  Der isolierte C17-Check endete absichtlich nach der Header-only-
  Konfiguration und Source-Kompilierung; es wurde weder ein NGINX-/Modul-Build
  noch Link, Installation, Service-Start, Connector-Load oder Request-Pfad
  ausgewählt. Er wird nicht aus Compile- oder Source-Contract-Checks
  abgeleitet.
- Frische Third-Head-SonarQube-Cloud- und GitHub-CI-Evidence wurde nicht
  ausgeführt. Die Second-Head-Fakten Quality Gate `OK`, `0` neue duplizierte
  Zeilen und `0.0%` gehören nur zu
  `116a50d0abd7c36471868e7b77d533d1a78ebda5`; zum Zeitpunkt der
  Record-Erstellung war die dritte reine Checker-Korrektur noch nicht
  committed oder gepusht und musste für ihren eigenen exakten Head
  zurückgelesen werden. Aus der lokalen Konstantensubstitution
  wird kein Issue-Abschluss abgeleitet.
## Finaler Diff- und Review-Status

Der zweite Korrektur-Head erhält den Request-Event-Metadaten-Helper und die
Empty-Fallbacks und faktorisiert dann nur den identischen JSONL-Serializer/
Write-Tail in einen header-lokalen Helper. Caller-spezifische Guards,
Meldungen, Returns, Short-Write-Warnungen, Intervention-/Rule-Match-Semantik
und reine Metadatenausgabe bleiben wie festgehalten erhalten. Seine exakte
Remote-Analyse hat Quality Gate `OK`, `0` neue duplizierte Zeilen und `0.0%`
New-Code-Duplizierung, während sie das eine neue reine Checker-
`python:S1192`-Issue identifizierte. Die aktuelle dritte lokale Korrektur
benennt nur `EVENT_JSONL_HEADER` und verwendet es in der einen Header-
Ownership-Assertion. Die fokussierten Source-Checks und die isolierte C17-
Kompilierung bestanden in ihrem angegebenen Umfang; Modul-Build- und native
Runtime-Evidence bleiben wie dokumentiert eingeschränkt.

Dieser Record, seine englische Begleitfassung und ihre Index-Einträge sind für
lokale Prüfung aktualisiert. Zum Zeitpunkt der Record-Erstellung waren die
dritte Checker-Korrektur und die Dokumentationsänderungen gestaged, aber
uncommittet. Dieser Record behauptet keinen dritten Korrektur-Head, keinen
Third-Head-Remote-Erfolg oder keine -Metrik, keinen SonarQube-Cloud-Issue-
Abschluss, keinen Push und keinen Merge.
