# Change Record: Parent-Common-Header-Validierung und NGINX-Strict-JSONL-Tail-Deduplizierung

**Sprache:** [English](CR-20260728-sonar-common-nginx-strict-jsonl-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-common-nginx-strict-jsonl-duplication |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8a3872e5e63f93e202bed24e0dcbad7bdf110ede |
| Grenze | Parent-Common- und NGINX-Quelltext, ihre direkten Source-Contract-Checks sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework/MRTS-Quelltext und Gitlinks, Workflows, Scanner-Konfiguration, Suppressions, Exclusions, Quality Gates und die Default-Branch-Integration bleiben unverändert. |
| Delivery-Status | Nur lokaler Kandidat zum Zeitpunkt der Record-Erstellung. Es existieren kein task-eigener Commit, Push, Pull Request, gehostete SonarQube-Cloud-Analyse, gehosteter Check-Abschluss, Merge oder Master-Integration. |

## Motivation und Problemstellung

Die aktuelle `master`-Bewertung identifiziert 630 ungelöste Projektzeilen und
`0.2%` Projektduplizierung. Auf `common/` und `connectors/` gefiltert verbleiben
285 offene Zeilen. Die größeren HAProxy-Duplikatkandidaten parsen
Protokolleingaben oder erzwingen Request-Body-Lifecycle-Regeln und werden
bewusst nicht in diesen ersten engen Batch aufgenommen.

Dieser Kandidat entfernt die identische private Header-Validator-Implementierung
aus den Common-Request- und Response-Helpern. Zudem entfernt er den
18-Zeilen-Phase-3- und 18-Zeilen-Phase-4-NGINX-JSONL-Serialisierungs-/Write-Tail.
Diese Pfade sind nicht mit dem vorhandenen warning-only-Request-Event-Writer
austauschbar: Serialisierungs-, Write- und Short-Write-Fehler müssen für den
Caller fatal bleiben.

Damit neben der Duplikatmetrik auch die Gesamtzahl der Issues sinkt, behebt der
Kandidat zusätzlich den bestehenden MAJOR-`c:S1854`-Befund in
`common/runtime/http_authorization_service.c`. `decision_name` wird auf jedem
Pfad gesetzt, der `send_response` erreicht; der einzige Pfad vor diesen
Zuweisungen kehrt zurück, nachdem er seine eigene Invalid-Request-Response
gesendet hat. Der initiale `"error"`-Store ist daher tot und wird entfernt,
ohne eine Authorization-Entscheidung oder Response zu ändern.

## Akzeptanzkriterien

- Beide Common-Validatoren verwenden eine private Implementierung, ohne ihre
  Request-spezifischen Method/URI- oder Response-spezifischen Status-Controls
  zu verändern.
- Ungültige Headernamen und ungültige Value/Size-Kombinationen bleiben
  abgelehnt; ein NULL-Value mit Größe null bleibt gültig.
- Phase 3 und Phase 4 teilen nur einen strikten begrenzten JSONL-Tail, der
  `NGX_ERROR` und die ausgegebenen Diagnosen erhält.
- Der warning-only-Request-Event-JSONL-Helper bleibt warning-only und wird
  nicht von den enforcement-relevanten Phase-3/4-Pfaden wiederverwendet.
- Das bestehende `c:S1854`-Initialisierungs-Issue wird entfernt, ohne ein
  erreichbares Authorization-Service-Ergebnis zu verändern.
- Die genaue PR-Head-Analyse muss `0 New issues`, `0.0% Duplication on New
  Code`, weniger Duplikatzeilen insgesamt und weniger offene Issues insgesamt
  als die aufgezeichnete `master`-Baseline ausweisen.
- Lokale Checks, Security-Diff-Review und der englisch/deutsche Record
  berichten beobachtete Ergebnisse und Einschränkungen wahrheitsgemäß.

## Implementierungsentscheidung und Begründung

`common/src/header_validation_internal.h` enthält einen privaten `static inline`
Validator. Er behält die bisherigen Prüfungen für einen nicht-NULL, nichtleeren
Namen, die Ablehnung von Space/Control/DEL/Colon mittels Unsigned-Byte-Vergleich
und die Regel NULL-Value-nur-bei-Größe-null exakt bei. Er ergänzt keine
öffentliche ABI. Request- und Response-Helper behalten ihre unterschiedlichen
umgebenden Validierungen.

`ngx_http_modsecurity_write_phase_event_jsonl` bleibt von
`ngx_http_modsecurity_write_event_jsonl` getrennt. Er serialisiert nur die
vorhandenen Metadaten in einen 4096-Byte-Stack-Buffer, schreibt auf denselben
konfigurierten Descriptor und gibt nach Serialisierungs-, Write- oder
Short-Write-Fehler `NGX_ERROR` zurück. Seine einzigen aktuellen Caller
übergeben die festen Literale `phase3` und `phase4`; `%s` ist ein Datenargument,
kein Caller-gesteuerter Format-String.

Der Control Flow des Authorization-Service bleibt bewusst unverändert. Alle
nicht zurückkehrenden Branches weisen `decision_name` vor `send_response` zu:
Request-Mapping-Fehler wählen `mapping_error`, Runtime-Begin/Finish-Fehler
wählen `runtime_error` und eine erfolgreiche Transaction leitet den
Action-Namen ab. Der tote Declaration-Initializer wird entfernt, nicht durch
eine Suppression oder einen Kommentar ersetzt.

## Geänderte Dateien

- common/src/header_validation_internal.h
- common/src/request_helpers.c
- common/src/response_helpers.c
- common/runtime/http_authorization_service.c
- connectors/nginx/src/ngx_http_modsecurity_common.h
- connectors/nginx/src/ngx_http_modsecurity_header_filter.c
- connectors/nginx/src/ngx_http_modsecurity_body_filter.c
- ci/checks/common/check-common-helpers.sh
- ci/checks/connectors/nginx/check-nginx-common-adoption.py
- dieses englisch/deutsche Change-Record-Paar und beide Indizes

Es werden kein Framework/MRTS-Quelltext oder Gitlink, Workflow, Makefile,
Scanner-Setting, Suppression, Exclusion, Quality Gate oder `master` geändert.

## Ausgeführte Befehle

| Command oder Verfahren | Ergebnis |
| --- | --- |
| `make check-nginx-common-adoption` | bestanden. Der Source-Contract prüft den erhaltenen warning-only-Helper, den separaten strikten Helper, einen begrenzten Serialisierungs-/Write-Tail, das Fehlen von Body-Daten darin, feste Phase-Caller und propagierte Phase-4-Fehlerbehandlung. |
| `make check-common-helpers` | bestanden mit C17, `-Wall -Wextra -Werror`; deckt den erhaltenen Common-Header-Validierungs-Contract ab. |
| `make check-common-sdk-contract`, `make check-common-security-contract` und `make check-common-flow-integrity` | bestanden. |
| `make check-common-memory-safety` | außerhalb der Sandbox bestanden. Der erste Sandbox-Versuch stoppte vor dem Test, weil LeakSanitizer unter dieser Tracing-Grenze nicht arbeiten kann. |
| `make check-http-authorization-service-timeout` | außerhalb der Sandbox bestanden mit C17, `-Wall -Wextra -Werror` sowie Configuration-Error-, Timeout- und Loopback-Service-Controls. Der erste Sandbox-Versuch konnte keinen Loopback-Port reservieren. |
| `make check-nginx-c-standard-wiring` | bestanden. |
| `make check-nginx-c17` | blocked_external_dependency: NGINX-Header/Source fehlen; der zugrunde liegende Control gibt 77 zurück. Es wird kein Compile-Erfolg behauptet. |
| `make check-bilingual-docs` | blocked_external_dependency im isolierten Worktree: Das nicht ausgecheckte Framework-Submodul macht bestehende Parent-Links unaufgelöst. Es wurde kein Documentation-Check geändert oder umgangen. Die eingeschränkte Paired-Record-/Link- und Whitespace-Validierung bestand. |

## Security-Auswirkung

Der fokussierte Diff-Review deckte eine HTTP-Header-Validierungsgrenze und eine
NGINX-Security-/Audit-Event-Write-Grenze ab. Der Common-Helper behält jede
bisherige Ablehnungsbedingung bei und fügt keinen öffentlichen Eintrittspunkt
hinzu. Der strikte NGINX-Helper verarbeitet keine Header- oder Body-Payloads,
ändert weder Ausgabedatei noch Descriptor, alloziert nicht und ändert keinen
Request/Response-Lifecycle-State. Entscheidend: Er wandelt keinen bisherigen
Fehler in eine Warnung um; alle drei Fehlerklassen geben weiter `NGX_ERROR`
zurück, während der unabhängige warning-only-Request-Event-Helper seine alte
Semantik behält.

Die Authorization-Service-Änderung liegt an einer Network-Authorization-Grenze
und wurde deshalb getrennt im Control Flow geprüft. Der einzige Pfad vor einer
Zuweisung sendet die Invalid-Request-Response und kehrt zurück; jeder Pfad zum
späteren Response-Sink weist `decision_name` zu. Das Entfernen des toten
Initialwerts ändert weder eine Default-Allow/Deny-Entscheidung noch führt es
einen erreichbaren uninitialisierten Wert ein.

Im geänderten Diff wurde kein neuer plausibler Security-Fund hoher oder
kritischer Auswirkung identifiziert. Dies ist fokussierte Source-Evidence, keine
Host-Runtime-Evidence.

## Runtime-Evidence

Es wurden keine native NGINX/libModSecurity-Host-Runtime, kein Connector-Load,
Request, Response, Transport, Service-Start oder Allocation-Fault-Szenario
ausgeführt. Der bestandene NGINX-Check ist ein Source-Contract-Control. Der
versuchte C17-Control konnte wegen fehlender externer NGINX-Source/Header nicht
mit der Kompilierung beginnen.

## Nicht ausgeführte Prüfungen mit Begründung

- Native NGINX/libModSecurity-Runtime-Tests wurden nicht ausgeführt, weil ihre
  Host-Voraussetzungen fehlen; sie werden nicht aus dem Source-Contract
  abgeleitet.
- Eine erfolgreiche NGINX-C17-Kompilierung wurde nicht ausgeführt: Der genaue
  Control ist wegen fehlender externer Header/Source blockiert, nicht wegen
  einer Source-Compile-Diagnose.
- Gehostete SonarQube Cloud- und GitHub-Actions-Checks wurden nicht ausgeführt,
  weil dieser Record vor Kandidaten-Commit, Push und Draft-PR entsteht.
- Die vollständige Repository-Bilingual-Link-Validierung kann in diesem
  isolierten Checkout erst bestehen, wenn sein externes Framework-Submodul
  vorhanden ist. Die eingeschränkte Paired-Record-/Link-Validierung ist
  schmalere Evidence, kein Ersatz.

## Bekannte Einschränkungen

Die 36 NGINX-Duplikatzeilen und der Common-Helper-Klon sind Source-Selection-
Evidence, kein neuer gehosteter SonarQube-Cloud-Wert. Nur der exakt gepushte
PR-Head kann New-Code-Duplizierung, Quality Gate oder Issue-Status belegen.

Der statische NGINX-Contract beweist die beabsichtigte Source-Form und
Fehlerpropagation, nicht jedoch Host-ABI-Kompatibilität oder Runtime-
Filterreihenfolge.

Die geforderten gehosteten Werte `0 New issues`, `0.0% Duplication on New Code`
und niedrigere projektweite Zähler sind Akzeptanz-Gates, noch keine beobachteten
Ergebnisse. Der Draft-PR muss offen bleiben, bis sein exakter Head diese
Evidence liefert.

## Verbleibende Risiken

Eine native NGINX-Integration könnte eine Host-ABI-, Descriptor- oder
Filter-Chain-Interaktion offenlegen, die der Source-Contract nicht ausführt.
Erhaltene Caller-Guards, ein begrenzter Metadata-only-Buffer, feste aktuelle
Phase-Literale und strikte Fehlerpropagation begrenzen dieses Risiko, ersetzen
aber keine native Tests.

Zum Zeitpunkt der Record-Erstellung gibt es keine gehostete Delivery oder
Analyse. Dieser Record behauptet daher keine globale Duplikatreduktion, keinen
Issue-Abschluss, keine niedrigere Issue-Zahl und keinen Quality-Gate-Erfolg.

## Finaler Diff- und Review-Status

Der lokale Diff zentralisiert nur die ausgewählten Klone. Der Common-Validator
behält die bisherigen Byte- und Size-Regeln; NGINX-Phase-3/4-Caller behalten
ihre Event-Erstellung und delegieren nur den strikten Write-Tail. Der
fokussierte Security-Diff-Review fand keinen geschwächten Control. Die oben
genannten lokalen Checks haben ihren beobachteten Status; die externe NGINX-
C17-Einschränkung bleibt offen. Zum Zeitpunkt der Record-Erstellung existieren
kein Commit, Push, Draft-PR, gehostete Analyse, Review, Merge oder Master-
Integration.
