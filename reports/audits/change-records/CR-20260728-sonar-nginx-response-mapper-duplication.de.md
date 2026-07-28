# Change Record: Parent-NGINX-Response-Mapper-Validation-Tail-Deduplizierung

**Sprache:** [English](CR-20260728-sonar-nginx-response-mapper-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-nginx-response-mapper-duplication |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Grenze | Parent-NGINX-Response-Mapper/-Filter-Quelltext und Source-Contract-Checker sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework- und MRTS-Quelltext und Gitlinks, Workflows, Scanner-Konfiguration, Suppressions, Exclusions, Quality Gates und die Default-Branch-Integration bleiben unverändert. |
| Delivery-Status | Nur lokaler Kandidat. Zum Zeitpunkt der Record-Erstellung existieren kein task-eigener Commit, Push, Pull Request, gehostete SonarQube-Cloud-Analyse, gehosteter Check-Abschluss, Ready-for-review-Aktion, Merge oder Master-Integration. |

## Motivation und Problemstellung

Die aktuelle Parent-Duplikatbewertung identifizierte den gemeinsamen
Response-Mapper-Validation-Tail in zwei unterschiedlichen NGINX-Filterpfaden:
18 Zeilen im Body-Pfad und 18 Zeilen im Header-Pfad, also 36 Parent-
Duplikatzeilen. Der gemeinsame Tail initialisiert einen Response-Mapper-
Contract, ruft den bestehenden Mapper auf und gibt eine Warnung aus, wenn das
Mapping nicht validieren kann.

Die Caller sind nicht semantisch austauschbar. Der Body-Pfad besitzt einen
Once-per-Response-Gate, während der Header-Pfad in seinem bestehenden
Header-Filter-Pfad berechtigt bleibt und seine eigene Reihenfolge behalten
muss. Dieser Kandidat extrahiert nur den gemeinsamen Tail; er wandelt keine
lokale Warnung in einen Filterfehler um und behauptet keinen neuen gehosteten
Wert oder Issue-Abschluss.

## Akzeptanzkriterien

- Ein interner NGINX-Mapper-Helper besitzt nur den gemeinsamen Contract-init/
  map/fixed-warning-Tail und hat ein void-, nicht fatales Interface.
- Ein Compile-Time-Header/Body-Enum wählt den bestehenden festen Warnkontext;
  es wird weder ein Caller-bereitgestellter Diagnose-String noch ein neuer
  Error-Propagation-Pfad ergänzt.
- Der Body-Once-Gate, Header-Berechtigung/Reihenfolge, bestehende Caller-Guards
  und Caller-eigene Zustandsübergänge bleiben lokal in ihren Filtern.
- Durch diese Source-Level-Extraktion wird keine Header-, Body-, Filter-Chain-,
  Allocation- oder Response-Mapper-Verhaltensänderung beabsichtigt.
- Der fokussierte Adoption-Check und der eingeschränkte Whitespace-Check
  dokumentieren ihre tatsächlichen erfolgreichen Ergebnisse. Der C17-Control
  wird als blockiert, nicht als Compiler-Pass dokumentiert.
- Das englisch/deutsche Change-Record-Paar und seine Indizes geben lokale
  Delivery- und Runtime-Einschränkungen wahrheitsgemäß an.

## Implementierungsentscheidung und Begründung

Die interne Mapper-Oberfläche deklariert
ngx_http_modsecurity_validate_response_mapper als void-Helper und deklariert
ngx_http_modsecurity_response_mapper_diagnostic_t mit den Compile-Time-Werten
NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_HEADER und
NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_BODY. Der Helper besitzt den
bestehenden stack-lokalen Response-Mapper-Contract, den Mapped-Response-Wert
und den Mapper-Error-Buffer. Er ruft den bestehenden
ngx_http_modsecurity_map_response_from_ctx genau einmal auf.

Bei erfolgreichem Mapping kehrt der Helper normal zurück. Bei nicht
erfolgreichem Mapping wählt das Enum eines der zwei bestehenden festen Header/
Body-Warnformate, gibt NGX_LOG_WARN aus und kehrt ohne Error-Ergebnis zurück.
Der Helper führt weder einen Caller-gesteuerten Format-String noch einen neuen
fatalen Filter-Result ein.

Der Body-Caller behält ctx->common_response_validated als Once-Gate vor dem
Helper, ruft den Helper nach seinen bestehenden Null-Context- und Intervention-
Guards auf, setzt das Flag nach dem Versuch und gibt NGX_OK zurück. Der Header-
Caller behält seine bestehenden Null-Context- und Intervention-Guards, ruft den
Helper auf seinem bestehenden berechtigten Pfad auf, setzt
ctx->common_response_validated nach dem Versuch und behält seine Processed-
State-Reihenfolge. Er erhält keinen Once-Gate.

Der Helper ändert keine Mapper-Eingaben oder Output-Contracts und besitzt keine
Header/Body-Daten, Filter-Chain-Control, Allocation, Enforcement, Intervention,
Processed-State oder Caller-Lifecycle-State.

## Geänderte Dateien

- connectors/nginx/src/ngx_http_modsecurity_mapper.c
- connectors/nginx/src/ngx_http_modsecurity_mapper.h
- connectors/nginx/src/ngx_http_modsecurity_body_filter.c
- connectors/nginx/src/ngx_http_modsecurity_header_filter.c
- ci/checks/connectors/nginx/check-nginx-common-adoption.py
- reports/audits/change-records/CR-20260728-sonar-nginx-response-mapper-duplication.md
- reports/audits/change-records/CR-20260728-sonar-nginx-response-mapper-duplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

Es werden kein Framework- oder MRTS-Quelltext, Gitlink, Workflow, Makefile,
Scanner-Setting, Suppression oder Exclusion geändert.

## Ausgeführte Befehle

| Command oder Verfahren | Ergebnis |
| --- | --- |
| rtk proxy -- make check-nginx-common-adoption | bestanden. Der fokussierte Source-Contract prüft den internen void-Helper, das Compile-Time-Diagnostic-Enum, das warning-only/nicht fatale Ergebnis, das Fehlen direkter Caller-Tails, Body-Once-Gate/Reihenfolge, Header-Berechtigung/Reihenfolge, feste Diagnosen und erhaltene Mapper-Contracts. |
| Eingeschränkter git diff --check über die fünf NGINX-Implementierungspfade | bestanden. Dies ist Whitespace-Evidence für lokale Implementierungspfade, keine Delivery-Evidence. |
| rtk proxy -- env BUILD_ROOT=<task-owned-exact-parent-framework-overlay>/build make check-nginx-c17 | blocked_external_dependency. Das exakte Parent/Framework-gepinnte Overlay erreichte den Repository-C17-Control, aber NGINX-Header/Source fehlen. Das darunterliegende Script stoppte mit blockiertem Exit 77 und make gab Exit 2 zurück. Es wird kein C17-Compile-Pass behauptet. |
| Eingeschränkte Change-Record-Paar- und Index-Whitespace-/Paired-Structure-Validierung | bestanden. In den vier eigenen Dokumentationspfaden wurde kein Trailing-Whitespace gefunden; die englischen/deutschen Records haben jeweils die entsprechenden 12 Pflichtabschnitte, reziproke Sprachlinks, dieselben technischen Literale und gepaarte Indexziele. Diese eingeschränkte Validierung ersetzt nicht die root-eigene Exact-Overlay-Dokumentations-/Link-Validierung. |

## Security-Auswirkung

Der Response-Mapper verarbeitet Response-Metadaten an einer Filtergrenze,
deshalb ist die Extraktion darauf begrenzt, seine bestehenden Controls zu
erhalten. Der Helper nimmt nur den bestehenden Context, Request-Pointer und ein
Compile-Time-Enum entgegen. Er akzeptiert keinen dynamischen Diagnose-String,
erstellt keinen neuen Sink, verarbeitet keine Header/Body-Daten, alloziert
nicht, ändert keine Mapper-Validierung, ordnet kein Enforcement neu und macht
eine Mapper-Warnung nicht fatal.

Der fokussierte Response-Filter-Review stufte den bestehenden Pfad als
already_safe und die enge Extraktion als feasible ein, wenn die Caller-
Lifecycle-Controls lokal bleiben. Der Adoption-Contract kodiert diese
Schutzmaßnahmen. Dies ist Source-Level-Evidence; sie belegt kein Host-Runtime-
Ergebnis und schließt keinen Sicherheitsbefund.

## Runtime-Evidence

Es wurde keine NGINX/libModSecurity-Host-Runtime, kein Connector-Load, Request,
Response, Transport, Service-Start oder Allocation-Fault-Szenario ausgeführt.
Der verfügbare bestandene Check ist nur Source-Contract-Evidence. Der
versuchte C17-Control kompilierte nicht, weil seine externe NGINX-Source/
Header-Voraussetzung fehlte.

## Nicht ausgeführte Prüfungen mit Begründung

- Ein nativer NGINX/libModSecurity-Runtime-Control wurde nicht ausgeführt. Er
  liegt außerhalb dieses lokalen Source-Deduplizierungskandidaten und wird
  nicht aus Source-Checks abgeleitet.
- Eine erfolgreiche C17-Kompilierung wurde nicht ausgeführt: Der exakte
  Parent/Framework-Overlay-Control wurde versucht, ist aber wegen fehlender
  NGINX-Header/Source blocked_external_dependency, mit Script-Exit 77 und
  make-Exit 2.
- Gehostete SonarQube Cloud, GitHub Actions, Review- und Pull-Request-Checks
  wurden nicht ausgeführt, weil noch kein Commit, Push oder Pull Request
  existiert.
- Repository-weite Bilingual-/Link-Validierung wird hier nicht als bestanden
  behauptet. Root führt die spätere Exact-Overlay-Validierung aus; ein
  Kandidaten-Checkout ohne Parent-gepinntes Framework-Material gilt nicht als
  Dokumentationsdefekt.

## Bekannte Einschränkungen

Die Zahl von 36 Zeilen ist ein aktuelles Source-/Assessment-Ziel, kein neuer
gehosteter SonarQube-Cloud-Wert. Nur ein exakter Kandidaten-PR-Head kann
New-Code-Duplizierung, Quality Gate, Check- oder Issue-Closure-Status
feststellen.

Dem C17-Control fehlt derzeit eine Host-NGINX-Header/Source-Voraussetzung. Sein
blockiertes Ergebnis ist eine External-Dependency-Einschränkung, weder ein
Source-Compile-Fehler noch Evidence für einen erfolgreichen Build.
Source-Contract-Validierung baut oder linkt das NGINX-Modul nicht.

## Verbleibende Risiken

Native NGINX-Integration könnte noch eine Lifecycle-, Allocation- oder Host-
Header-Interaktion zeigen, die der Source-Contract nicht ausführt. Erhaltene
Guards, Caller-lokale Zustandsübergänge, feste Warnungen und das nicht fatale
Helper-Interface begrenzen dieses Risiko; sie ersetzen keine native Runtime
oder erfolgreiche C17-Kompilierung.

Es existiert noch keine Delivery oder gehostete Analyse. Das lokale Ergebnis
behauptet deshalb weder, die globale Projekt-Duplikatdichte zu reduzieren, noch
ein SonarQube-Cloud-Issue zu schließen oder ein Quality Gate zu erfüllen.

## Finaler Diff- und Review-Status

Der Source-Review bestätigt, dass der Kandidat einen internen void-Mapper-
Helper mit Compile-Time-Diagnostic-Discriminator hat und die Body/Header-
Lifecycle-Unterschiede in den Callern bleiben. Dieser deutsche Record, seine
englische Begleitfassung und die gepaarten Indizes bestanden ihre eingeschränkte
Whitespace-/Paired-Structure-Prüfung.

Zum Zeitpunkt der Record-Erstellung existieren kein task-eigener Commit, Push,
Pull Request, gehostete Analyse, gehosteter Abschluss, Review-Ergebnis oder
Merge. Die exakte C17-Einschränkung und fehlende Host-Runtime-Evidence bleiben
offen und werden nicht als erfolgreiche Ergebnisse dargestellt.
