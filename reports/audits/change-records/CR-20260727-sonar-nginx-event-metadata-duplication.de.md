# Change Record: Parent-NGINX-Event-Metadaten-Deduplizierungs-Kandidatenremediation

**Sprache:** [English](CR-20260727-sonar-nginx-event-metadata-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260727-sonar-nginx-event-metadata-duplication` |
| Datum (UTC) | `2026-07-27` |
| Basis-Revision | `1b0f8825f3510b99b603bb6cd6f0777e1710358e` |
| Tracking | Statischer Kandidat mit `22+22` duplizierten Zeilen in der Parent-NGINX-Request-Event-Metadatenkonvertierung; es wurde kein SonarQube-Cloud-Ergebnis für einen exakten Head beobachtet. |
| Grenze | Parent-NGINX-Request-Event-Metadatenquelltext und sein Parent-Source-Contract-Checker sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework- und MRTS-Quelltext und Gitlinks, Scanner-Konfiguration, Quality Gates, Remote-Analyse und Delivery bleiben unverändert. |
| Delivery-Status | Dieser Record behauptet selbst weder Staging, Commit, Push, Pull Request, Merge, SonarQube-Issue-Abschluss noch Remote-Analyse. Draft-Delivery und Exact-Head-Verifikation sind getrennte ausstehende Lifecycle-Schritte. |

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

## Akzeptanzkriterien

- Nur Method-, Raw-URI- und Content-Type-Konvertierung über einen
  header-lokalen Helper teilen.
- Die etablierten Empty-String-Fallbacks für fehlende, leere, `NULL`- und
  `(char *)-1`-Konvertierungsergebnisse erhalten.
- Event-Ausgabe ausschließlich als Metadaten belassen; keine Request-Body-Daten
  zu einem der JSONL-Events hinzufügen.
- Intervention- und Rule-Match-IDs, Statuswerte, Entscheidungen, Guards,
  Rule-ID-Behandlung und die vorhandenen JSONL-Schreibvorgänge erhalten.
- Tatsächliche fokussierte Source-Check-Ergebnisse, die blockierte
  C17-Host-Kompilierung und das Fehlen nativer Host-Runtime-Evidence
  wahrheitsgemäß festhalten.
- Keine SonarQube-Cloud-Duplikatreduktion, Issue-Auflösung, Quality Gate,
  Remote-Analyse, Pull Request oder Merge behaupten, bevor Exact-Head-Evidence
  vorliegt.

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
`event.body.bytes_inspected` oder `r->request_body`-Behandlung hinzu. Beide
behalten ihre vorhandenen JSONL-Schreibpfade
`msconnector_event_write_jsonl_line` und `ngx_write_fd`.

Die Event-Konstruktion bleibt quellspezifisch. Der Intervention-Emitter
verwendet weiterhin `MSCONN_EVENT_REQUEST_BLOCKED`,
`MSCONNECTOR_STATUS_BLOCKED` und seine vorhandene `wanted`-Entscheidung. Der
Rule-Match-Emitter verwendet weiterhin `MSCONN_EVENT_RULE_MATCHED`,
`MSCONNECTOR_STATUS_OK`, die `"pass"`-Entscheidung und seine validierte
`rule_id`. Ihre unterschiedlichen Guards bleiben erhalten. Dies ist ein
header-lokales Implementierungsdetail, keine Änderung einer öffentlichen API
oder des Event-Schemas.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_log.c`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `rtk proxy make check-nginx-common-adoption` | bestanden, einschließlich der Fallback-/Adoptions-, Metadaten-Only-Request-Body-Exclusion-, quellspezifischen Semantik- und JSONL-Schreibverträge. |
| `rtk proxy make check-nginx-c-standard-wiring` | bestanden. |
| `rtk proxy make check-common-helpers` | bestanden: `common_helper_smoke`. |
| `rtk proxy env BUILD_ROOT=<task-owned external build root> make check-nginx-c17` | blockiert: NGINX-Header/Source fehlen; die innere Prüfung endete mit 77 und `make` mit 2, daher ist dies kein C17-Kompilierungspass. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs` | bestanden: 14 Tests in 0,033 s. |
| `rtk proxy make check-bilingual-docs check-doc-links` | bestanden nach read-only-Initialisierung des Parent-gepinnten Framework-Gitlinks; Framework-Status blieb sauber. |
| `rtk git diff --check` | bestanden, nachdem das englische/deutsche Change-Record-Paar und die Index-Einträge ergänzt wurden. |

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

## Runtime-Evidence

Es wurde kein nativer NGINX/libModSecurity-Host-Request ausgeführt. Die
bestandenen fokussierten Prüfungen sind ausschließlich Source-Contract- und
Helper-Evidence; sie beweisen weder ausgerolltes Host-Verhalten, eine
Rule-Entscheidung, client-sichtbare Ausgabe noch Transportkompatibilität.

## Bekannte Einschränkungen

Die C17-Host-Kompilierung ist blockiert, weil diese Umgebung die erforderlichen
NGINX-Header/Source nicht bereitstellt. Der innere Checker endete mit 77 und
das Make-Target mit 2; keines der Ergebnisse wird als Kompilierungspass
behandelt. Die für diesen Versuch verwendeten exakten leeren task-eigenen
temporären Build-Verzeichnisse wurden entfernt, sodass kein externes
Build-Artefakt verbleibt.

Die statischen Source-Contract-Prüfungen prüfen die beabsichtigte
Helper-Adoption und erhaltene Source-Semantik, kompilieren oder starten das
NGINX-Modul jedoch nicht gegen eine native Host-Integration.

## Verbleibende Risiken

Die Zahl `22+22` ist statische Kandidaten-Evidence, kein Beweis dafür, wie
eine zukünftige SonarQube-Cloud-Analyse den aktuellen Diff klassifiziert. Keine
New-Duplicate-Reduktion und kein Zero-Duplication-Ergebnis werden behauptet,
bis eine Remote-Analyse für einen exakten Delivery-Head beobachtet wurde.

Eine native Integration könnte einen NGINX-Allokations- oder
Lifecycle-Unterschied zeigen, der in den Source-Contracts nicht enthalten ist.
Die erhaltene Fallback-Semantik und der reine Metadatenumfang begrenzen dieses
Risiko, ersetzen jedoch keine native NGINX/libModSecurity-Runtime-Kontrolle.

## Nicht ausgeführte Prüfungen mit Begründung

- Ein nativer NGINX/libModSecurity-Host-Runtime-Request wurde nicht ausgeführt,
  weil dieser Task-Umgebung NGINX-Header/Source und eine kompatible
  Host-Integration fehlen. Er wird nicht aus den Source-Contract-Prüfungen
  abgeleitet.
- Frische Exact-Head-SonarQube-Cloud- und GitHub-CI-Evidence wurde nicht
  ausgeführt. Sie erfordert einen ausgelieferten Remote-Head und muss für genau
  diesen Head zurückgelesen werden; hier wird kein Remote-Ergebnis behauptet.

## Finaler Diff- und Review-Status

Die begrenzte Source-Änderung teilt nur die Request-Event-Metadatenkonvertierung
und erhält Empty-Fallbacks, reine Metadaten in der JSONL-Ausgabe sowie
quellspezifische Intervention- und Rule-Match-Semantik. Die oben festgehaltenen
fokussierten Source-Checks bestanden in ihrem angegebenen Umfang; C17-Host-
Kompilierung und native Runtime bleiben wie dokumentiert eingeschränkt.

Dieser Record und seine englische Begleitfassung wurden mit ihren Index-Einträgen
vor jedem Delivery-Schritt lokal validiert. Es werden weder Merge,
SonarQube-Cloud-Issue-Abschluss, New-Duplicate-Reduktion, Quality-Gate-Ergebnis
noch Exact-Head-Remote-Analyse behauptet.
