# Change Record: HAProxy-Master-Recovery für Common-Adoption und SPOP-Grenzen

**Sprache:** [English](CR-20260906-haproxy-master-recovery.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260906-haproxy-master-recovery |
| Datum (UTC) | 2026-09-06 |
| Basis-Revision | 9925ef647b5fb49d21aebd658a658d4fdb649c58 |
| Delivery-Status | Lokale Implementierung und Validierung auf einem isolierten Branch ausgehend von der genannten Revision. Ein normaler Push und separater Draft PR sind erst nach einem frischen Delivery-Preflight autorisiert. Kein Merge, direkter `master`-Push, Force-Push, Rebase oder Branch-Löschen ist autorisiert. |

## Motivation und Problemstellung

Fünf Resulting-Master-Actions-Jobs (`quick-framework-check`, `lint`,
`test-apache`, `test-nginx` und `test-common`) stoppten an derselben veralteten
HAProxy-Common-Adoption-Assertion. Der alte Checker verlangte sowohl einen von
Host abgeleiteten Hostnamen als auch den obsoleten Fallback
`out->request.hostname = src->server_ip`. Der aktuelle Mapper weist fehlenden
oder doppelten Host vor der Owned-Header-Allokation zurück, weist leeren Host
nach dem Lookup mit Cleanup zurück, mappt `server_ip` nur auf
`request.server.address` und leitet `hostname` aus dem validierten Host-Header
ab.

Die exakte Master-SonarQube-Cloud-Analyse
`1878d424-279f-4452-8b32-b7d9c05e724a` für die genannte Basis meldete zudem
`AaBwK2W4SQwNCdYHcQVm` / `c:S3519` beim direkten SPOP-NOTIFY-
Argumentzählbyte-Zugriff. Dies ist ein bestätigter Analyzer- und
Delivery-Blocker, kein reproduzierter Runtime-Out-of-Bounds-Fehler: Begrenzter
Frame-Empfang und `read_string_ref()` weisen die gemeldete abgeschnittene
Message-Name-Form bereits zurück.

PR-#346-Head `5432cf5607ac0f105579651bb24eca9f57b99e1d` ist ausschließlich
Read-only-Referenz. Seine relevante Sequenz ist `139030d2`, `1c32bbac` und
`5432cf56`; kein PR-#346-Branch, keine Datei, kein Gitlink und kein
Delivery-Status werden hier geändert.

## Akzeptanzkriterien

- Der globale Checker beweist, dass der aktive Request-Mapper genau einen Host
  vor der Owned-Header-Allokation validiert, leeren Host mit Cleanup verwirft,
  `hostname` aus Host ableitet, `server_ip` nur als Serveradresse behält und
  beide Common-Request-Validation-Returns korrekt auswertet.
- Comment-only- und Foreign-function-Dekoys können die aktiven Host-,
  Request-/Response-Common-Validation- oder Engine-Config-Merge/Validate-
  Assertions nicht erfüllen; entfernte oder ignorierte Host-Ablehnung, ein
  erneut eingeführter Hostname-Fallback und invertierte Return-Behandlung
  werden durch fokussierte Mutationstests verworfen.
- `read_byte()` verwirft Null-Input-/Cursor-/Output-Pointer, Input-Ende,
  Cursor-außerhalb-der-Länge und `SIZE_MAX`-Cursor vor einem Bytezugriff;
  fehlgeschlagene Reads bewahren Caller-Cursor und Output-Wert.
- `parse_notify_message_header()` behält die rohe Ein-Byte-Count-Semantik,
  verwirft ein fehlendes Count-Byte, akzeptiert einen vollständigen
  Zero-Count-Parser-Control und macht aus Parser-Akzeptanz keine
  Request-Autorisierung.
- Leerer Input, abgeschnittener Message-Name, vollständiger Name ohne Count,
  gültiger Zero-Count-Control, malformed-then-legitimate-Sequenz, Cleanup,
  C17, ASan/UBSan und der Repository-Runtime-Selbsttest haben aktuelle lokale
  Evidence.
- Enthalten sind keine Workflow-, Governance-, Quality-Gate-, Suppression-,
  Exclusion-, Source-Lock-, Gitlink-, Framework-, MRTS-, PR-#346- oder
  fremden Connector-Source-Änderungen.

## Implementierungsentscheidung und Begründung

Der Checker maskiert jetzt Kommentare und extrahiert die konkreten
Funktionsrümpfe des Request-Mappers, Response-Mappers, Header-Validators und
der Engine-Erzeugung, bevor er ihre geordneten fail-closed-Formen prüft. Dies
bindet Host-Admission-Guard, Request-/Response-Validation-/Cleanup-Returns und
den Common-Config-Merge/Validate-Guard an ihre aktiven Funktionen. Es ist
absichtlich ein enger Function-Boundary-Contract statt eines breiten Neubaus
des globalen Checkers oder einer Wiederherstellung des verbotenen
`server_ip`-Hostname-Fallbacks.

Der SPOP-Transfer ist die kleinste abhängigkeitvollständige Teilmenge der drei
referenzierten PR-#346-Commits: `read_byte()` besitzt seinen lokalen Cursor,
validiert Pointer-Eingaben, verwendet `cursor > len || len - cursor <
sizeof(*value)` vor dem Zugriff, liest ein rohes Byte und schreibt den
Caller-Cursor erst nach Erfolg fort. `parse_notify_message_header()` führt
eigene Pointer-/Cursor-Validierung aus, parst den Message-Namen, liest den
rohen Count über den Helper und behält die bestehenden Valid-Message- und
Response-Role-Regeln. Es werden keine breiteren PR-#346-Runtime-, Worker-,
Cache-, Socket- oder Lifecycle-Änderungen übertragen.

## Geänderte Dateien

- `ci/checks/connectors/haproxy/check-haproxy-common-adoption.py`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `tests/test_haproxy_common_adoption.py`
- `tests/test_haproxy_header_validation_contract.py`
- `tests/test_sonar_reliability_contract.py`
- `reports/audits/change-records/CR-20260906-haproxy-master-recovery.md`
- `reports/audits/change-records/CR-20260906-haproxy-master-recovery.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Pre-Patch direkter Checker und `make check-haproxy-common-adoption` | Die veraltete Host/`server_ip`-Fallback-Assertion auf der genannten Basis reproduziert. |
| Pre-Patch `make lint` und `make quick-check` mit isolierten Output-Roots | Beide erreichten und scheiterten an derselben veralteten HAProxy-Assertion. |
| Fokussierte Checker-Mutation-, Mapper/Header-, native Host- und Sonar-Contract-Tests | Bestanden: 37 Tests; Negativ-Controls decken entfernte oder ignorierte Pre-Allocation-Host-Ablehnung, entfernten Empty-Host-Cleanup, `server_ip`-Hostname-Fallback, invertierte Request-/Response-Common-Returns und invertierten Config-Merge trotz Comment- und Foreign-function-Dekoys ab. |
| `make check-haproxy-common-adoption` | Bestanden. |
| `make check-haproxy-c17` | Bestanden. |
| `tests.test_sonar_reliability_contract` mit `-fsanitize=address,undefined` | Bestanden: 15 Tests; sein HAProxy-C-Harness deckt Empty/Truncated/Missing-Count/Zero-Count, Cursor-Grenzen, Pointer und Cleanup ab. |
| `make -C connectors/haproxy self-test-spoa-runtime` | Bestanden: Der Repository-SPOP-Protocol-Selftest wurde abgeschlossen. |
| `make -C connectors/haproxy self-test-spoa` | Scheiterte vor der SPOP-Parser-Ausführung: Das bestehende Starter-Target lässt `common/src/block_statuses.c` aus und kann `msconnector_block_status_is_allowed` nicht linken; keine Makefile-Änderung liegt im Scope. |
| Valgrind auf dem gebauten Runtime-Selftest | Bestanden mit null Fehlern, null definitiven/indirekten/möglichen Leaks und keinen Retained Allocations des Parent-Prozesses. |
| Direkter `clang --analyze` der geänderten SPOP-Translation-Unit | Bestanden ohne Diagnostic-Output. |
| `make check-analysis-tools` und `make check-clang-analysis-tools` | Bestanden. |
| Post-Patch `make lint` und `make quick-check` | Beide bestanden den reparierten globalen Checker und HAProxy C17 und stoppten danach an vier bereits bestehenden HTX-Overlay-Assertions außerhalb dieses Scopes. |

## Security-Auswirkung

Der Mapper-Source-to-Sink-Pfad ist empfangene HAProxy-Header →
`haproxy_validate_source_headers()` → Owned-Common-Header → Host-Lookup →
Common-Mapper-Validation → Transaction-Admission. Der reparierte Checker
bindet seine Assertions jetzt an diesen aktiven Pfad: fehlender, leerer und
doppelter Host bleiben fail-closed; eine gemappte Allokation wird beim
Empty-Host-Fehler bereinigt; Endpoint-Metadaten können Authority nicht still
ersetzen.

Der SPOP-Source-to-Sink-Pfad ist Peer-Frame → `recv_frame()` →
`handle_connection()` → `handle_notify_frame()` → `parse_notify_payload()` →
`parse_notify_message_header()` → Typed-Argument-Parser → Endpoint-Admission
und Transaction-Owner-Handling. Die Änderung bewahrt Frame-Limits, exakten
Payload-Consumption, Duplicate-Argument-Rejection, begrenzte Header-/Body-
Pfade und fail-closed-Missing-Endpoint-Verhalten. Eine parsergültige
Zero-Count-Nachricht durchläuft weiterhin die späteren Host- und
Endpoint-Admission-Controls; sie ist keine Autorisierungsfreigabe.

## Runtime-Evidence

Der direkt kompilierte HAProxy-Harness führt die Parser-Controls unter
AddressSanitizer und UndefinedBehaviorSanitizer aus. Der gebaute
SPOP-Runtime-Selftest des Repositorys bestand ebenfalls unter Valgrind. Dies
ist nur begrenzte lokale Protocol-Evidence, keine Behauptung vollständiger
HAProxy-Host-Runtime-, P1–P4- oder 17×10-Matrix-Abnahme.

## Bekannte Einschränkungen

Der Checker ist ein absichtlich enger Source-Contract, kein vollständiger
C-Parser oder Beweis beliebiger Macro-/Control-Flow-Reachability. Das
Sonar-Signal wurde nicht unabhängig als Runtime-Overflow reproduziert; der
source-native Bounds-Proof und die Regressionen adressieren die vom Analyzer
gemeldete Byte-Access-Form, ohne diese nicht belegte Behauptung aufzustellen.
Die begrenzten Kommentar- und Foreign-function-Dekoy-Fälle sind abgedeckt;
dies behauptet keine beliebige C-Semantikgleichheit.

## Verbleibende Risiken

Die fünf anderen Exact-Master-Sonar-Issues sind unabhängig und unverändert:
`AaBjSjUps3vKd0hpl5pP` ist Apache-Checker-Duplizierung; drei NGINX-Shell-Issues
sind unabhängig; und `AaA34UWlbqrRc02noCI3` gehört zum Framework-Gitlink-Pfad.
Es gibt keinen weiteren aktuellen HAProxy-Befund im Six-Issue-Inventar. Die
Post-Patch-Aggregatketten zeigen vier HTX-Overlay-Contract-Fehler; sie sind ein
separater HAProxy-Follow-up und werden durch diese Änderung weder verborgen
noch behoben.

## Nicht ausgeführte Prüfungen mit Begründung

`tests/test_haproxy_transaction_contract_binding.py` konnte nicht gesammelt
werden, weil die isolierte Python-Umgebung kein `pytest`-Modul hat; es wurde
keine Abhängigkeit nur zur Veränderung dieses Ergebnisses installiert. Die
repositoryweite `clang-analyzer-baseline` war blockiert, weil keine
HAProxy-Compilation-Database verfügbar war. Das Starter-Target `self-test-spoa`
hat eine unabhängige bestehende Link-Auslassung und stoppt deshalb vor der
Parser-Ausführung. Es gibt kein repository-natives HAProxy-ThreadSanitizer-
Target. Es wird keine vollständige native HAProxy-Runtime-, P1–P4- oder 17×10-
Matrix-Abnahme behauptet.

## Finaler Diff- und Review-Status

Die finale Allowlist ist auf die neun oben genannten Pfade begrenzt. Das erste
unabhängige Review reproduzierte drei Checker-Integrity-False-Negatives, die
danach mit begrenzten Copied-Source-Controls geschlossen wurden; ein frisches
unabhängiges Read-only-Recheck fand keinen zusätzlichen validierten Bypass oder
keine Parser-Regression. Die generierte Analyzer-Plist wurde entfernt und ist
nicht Teil des Diffs. Ein finaler Exact-Delivery-Preflight bleibt vor Delivery
erforderlich. Dieser Record behauptet absichtlich keinen Commit-SHA, Push-Head,
Draft-PR-Nummer, Hosted-Checks, Sonar-Ergebnis, Ready-Status oder Merge; diese
Fakten müssen nach der Delivery unabhängig beobachtet werden.
