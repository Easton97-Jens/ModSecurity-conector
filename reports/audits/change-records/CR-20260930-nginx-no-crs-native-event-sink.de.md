# Nativer NGINX-No-CRS-Event-Sink

**Sprache:** [English](CR-20260930-nginx-no-crs-native-event-sink.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-nginx-no-crs-native-event-sink |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | `3de8043c2482b52debc6f6e2d9ca609adf257eab` |
| Framework | `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` |
| MRTS | `615b13bacbd008562c17408246c41ab27dca3104` |

## Motivation und Problemstellung

Generische NGINX-No-CRS-Cases erzeugten echte HTTP- und Native-Result-
Records, aber kein natives JSONL-Event: Der Lifecycle-Caller wählte keinen
Sink-Scope, und der direkte Harness-Default erzeugte für diese portablen Cases
keine `modsecurity_phase4_log`-Direktive. Bei einem leeren Modul-Sink kehrten
P1/P2/P3-Emitter vor der Event-Erzeugung zurück. Ein gepinnter Kontrolllauf
mit Root-Master/`nobody`-Worker und explizitem bestehendem Sink erzeugte das
erwartete Event. Der Audit-Artefaktpfad ist ein separater Collection-Defekt
und wird hier nicht geändert.

## Akzeptanzkriterien

Für jeden generischen No-CRS-Case genau einen case-lokalen nativen Location-
Sink unter `LOG_DIR/phase4.log` rendern; connector-spezifische Fixture-eigene
Direktiven einzeln belassen und direktes Harness-/First-Byte-Verhalten
erhalten. Echte P1/P2/P3-Requests müssen eigene Regel-, Phasen-, Transaktions-
und Message-IDs ohne Body-Payload liefern. Bestehende Containment-, No-Follow-/
Private-File-, Root-/Worker- und Projection-Prüfungen bleiben aktiv. Aus
isolierten Cases wird kein vollständiger Canonical-PASS abgeleitet.

## Implementierungsentscheidung und Begründung

Nur der Parent-Caller `nginx:no_crs_baseline` wählt
`NGINX_PHASE4_LOG_SCOPE=location_if_missing`. Nach der Framework-
Materialisierung prüft der Parent-Harness das erzeugte Location-Include auf
eine vorhandene Direktive und rendert sonst genau eine Direktive in den
bestehenden Location-Platzhalter. Er nutzt den bereits validierten
case-lokalen Pfad `LOG_DIR/phase4.log`, den der Collector liest. `server`
allein würde in eine andere Datei schreiben; ein bedingungsloses
`server_with_location_override` würde die connector-spezifische Phase-4-
Fixture-Direktive duplizieren. Keine Änderungen an nativem C-Code, Common-
Protokoll, Framework, MRTS, Schema, Regeln oder Canonical-Erwartungen.

## Security-Auswirkung

Der Root-NGINX-Master öffnet den Sink über die bestehenden No-Follow-,
Regular-File-, Eigentümer- und Modusprüfungen; der `nobody`-Worker nutzt den
geerbten Deskriptor. In den isolierten Kontrollen ist das Leaf `root:root`
im Modus `0600` unter dem validierten privaten case-lokalen Log-Root. Der
Worker erhält keinen Zugriff auf private Config-, Rules- oder Harness-Logs.
Pfadautorität und Docroot-Projection-Freshness bleiben unverändert; die
Runtime nutzt `PrivateNetwork=yes`, keinen Build und keinen Download.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-connector-stage.sh`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_no_crs_event_sink.py`
- `connectors/nginx/README.md` und `connectors/nginx/README.de.md`
- Dieses Change-Record-Paar.

## Ausgeführte Befehle

Der erhaltene externe RED-Test reproduzierte Default-P1 mit HTTP `403`,
Native-Result und null Events; seine bestehenden Sink- und Matched-Rule-
Kontrollen bestanden. Die neue dynamische Config-Render-Regression war vor
dem Sourcefix RED und danach GREEN. Ein Parent-Lauf mit 19 Modulen führte
306 Tests aus: 305 bestanden; ein Worker-Ownership-Test konnte in der
Standard-Sandbox kein `chown` ausführen (`EINVAL`); exakt dieser Test bestand
bei der Wiederholung mit Host-Rechten. Shell-Syntax bestand. ShellCheck
behielt genau die Diagnosen der Basisrevision bei, ohne neue Diagnosen. Ein
abschließender fokussierter Lauf mit fünf Modulen bestand 81/81 Tests.
Gepinnte Bilingual-, Repository-Pfad-, Doc-Link- und No-CRS-Konsistenzprüfungen
bestanden. `git diff --check` bestand vor dem Commit.

```sh
rtk run -c 'TMPDIR=/var/tmp/codex/ModSecurity-conector/analysis PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest tests.test_nginx_no_crs_event_sink tests.test_nginx_synchronized_phase4_policy tests.test_nginx_native_security_contract tests.test_nginx_harness_path_authority tests.test_collect_no_crs_source'
rtk run -c 'sh -n connectors/nginx/harness/run_nginx_smoke.sh && sh -n ci/runtime/lifecycle/run-connector-stage.sh'
rtk run -c 'bash /var/tmp/codex/ModSecurity-conector/analysis/run-nginx-sink-fix-isolated.sh p1'
rtk run -c 'bash /var/tmp/codex/ModSecurity-conector/analysis/run-nginx-sink-fix-isolated.sh p2'
rtk run -c 'bash /var/tmp/codex/ModSecurity-conector/analysis/run-nginx-sink-fix-isolated.sh p3'
rtk run -c 'make FRAMEWORK_ROOT=/var/tmp/codex/worktrees/pr382-nginx-source-map-phase4-header/modules/ModSecurity-test-Framework check-bilingual-docs check-doc-links check-no-crs-doc-consistency'
```

## Runtime-Evidence

Drei frische Cache-only-Einzelcase-Services nutzten getrennte direkte
Projection-Kinder und echte Requests mit Root-Master/`nobody`-Worker. P1
lieferte HTTP `403` und `engine_decision`, `MSCONN_EVENT_ENGINE_DECISION`,
Regel `1100001`, `request_headers`, Transaktion
`nginx-deny_header_marker_403-2-1`; P2 lieferte HTTP `403` mit demselben
Event-/Message-Typ, Regel `1100101`, `request_body`, Transaktion
`nginx-deny_request_body_marker_403-2-1`. Beide Harness-Exits waren `0`.
P3 lieferte HTTP `403` und `phase3_intervention`,
`MSCONN_EVENT_RESPONSE_BLOCKED`, Regel `1100201`, `response_headers`, Transaktion
`nginx-phase3_deny_before_commit-2-1`. Nativer Case und Collector-Case
bestanden, aber der Harness-Exit war `1`, weil Cleanup nach dem Ende von
Master und Workern `port=19783 result=still_bound` meldete. Jeder Collector
sah ein Event; alle drei gesammelten Records bestanden den gepinnten
Framework-Event-Validator mit null Fehlern. Die umfassendere Profil-Summary
jedes isolierten Collectors blieb `FAIL`, weil nur ein Case ausgewählt war.
Kein isoliertes Ergebnis ist ein Canonical-Full-Lifecycle-PASS.

## Nicht ausgeführte Prüfungen mit Begründung

Der neue Exact-Head-Full-E2E folgt erst nach diesem separaten Commit. Kein
neuer C-Build, keine MRTS-Matrix, Framework-Änderung, Remote-CI, Push, PR
oder Merge gehört zu diesem Sourcefix.

## Bekannte Einschränkungen

Der unabhängige Audit-Artefakt-Collection-Pfad, die P3-Cleanup-Port-
Beobachtung, der Redirect-Transport und andere Canonical-Fehler werden hier
nicht behoben. Für einen gewöhnlichen unmatched Allow-Case wird kein
künstliches generisches Allow-Event erfunden.

## Verbleibende Risiken

Die Prüfung des erzeugten Includes erkennt eine eigenständige Location-
Direktive, wie sie die gepinnten connector-spezifischen Fixtures benutzen;
verschachtelte Includes werden nicht geparst. Keine gepinnte Fixture verwendet
einen solchen verschachtelten Sink. Vollständiger Canonical-Status und
verbleibende unabhängige Fehlerklassen erfordern den neuen Exact-Head-Lauf.

## Finaler Diff- und Review-Status

Die Änderung betrifft nur den Parent und schreibt keine Historie um. Vor dem
neuen Exact-Head-Lauf müssen Pre-Commit-Diff, Dokumentationsprüfungen und
separater Folge-Commit verifiziert werden; dieser Record behauptet keinen
gesamten E2E-PASS.
