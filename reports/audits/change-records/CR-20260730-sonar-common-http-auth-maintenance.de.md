# Change Record: Parent-Common HTTP-Autorisierungsservice-Const-Korrektheit

**Sprache:** [English](CR-20260730-sonar-common-http-auth-maintenance.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260730-sonar-common-http-auth-maintenance` |
| Datum (UTC) | 2026-07-30 |
| Basis-Revision | `fe4840a0a72449bbdb8f7b2f77f09922c9e66a9f` |
| Tracking | Aktuelle SonarQube-Cloud-Issues in `common/runtime/http_authorization_service.c`: `AZ9MwjL6-bUaKQ_zSGBP`, `AZ9MwjL6-bUaKQ_zSGBQ`, `AZ9MwjL6-bUaKQ_zSGBT`, `AZ9MwjL6-bUaKQ_zSGBU`, `AZ9MwjL6-bUaKQ_zSGBV`, `AZ9MwjL6-bUaKQ_zSGBW`, `AZ9MwjL6-bUaKQ_zSGBX`, `AZ9MwjL6-bUaKQ_zSGBY` und `AZ9MwjL6-bUaKQ_zSGBa` (`c:S5350`, `c:S995` und `c:S1066`). |
| Grenze | Parent-Common-HTTP-Autorisierungsservice, gepaarte Change-Record-/Index-Dokumente und keine Framework-/MRTS-/Gitlink-/Workflow-/Sonar-Konfigurationsänderung. |

## Motivation und Problemstellung

Die aktuelle Common-Basis enthält acht Stellen, an denen der HTTP-Parser oder
eine Runtime-Sicht einen schreibbaren Pointer behält, obwohl nur lesend über
ihn zugegriffen wird, sowie eine verschachtelte Transaction-Finish-Bedingung.
Der Parser muss seine eigenen Request-Buffer an den beabsichtigten Delimitern
weiter mutieren; die Korrektur darf diese Mutationsstellen nicht versehentlich
immutable machen oder Request-, Timeout-, Transaction- oder Response-Semantik
ändern.

## Akzeptanzkriterien

- Die acht Sonar-Const-Korrektheitsbefunde nutzen `const` nur an
  Read-only-Pointer-Grenzen, während Parser-eigene Delimiter-Schreibzugriffe
  gültig bleiben.
- Das Transaction-Finish-Ergebnis wird weiterhin nur bei existierender
  Transaction ausgewertet, mit demselben Fehlerstatus, Decision-Namen und
  Success-Ergebnis.
- Der C-Quelltext kompiliert und der reale Timeout-Service-Smoke erhält
  fehlerhafte CLI-, Timeout-, Request- und Response-Control-Verhalten im
  expliziten C17-Modus mit beiden verfügbaren Compilern.
- Keine Security-Control, Sonar-Regel, Quality Gate, Suppression oder
  Runtime-Abhängigkeit wird geändert.

## Implementierungsentscheidung und Begründung

Read-only-Parser-Cursor, Header-Bereichsgrenzen, Header-Werte und die
Runtime-Sicht sind nun als `const` deklariert. Der eine mutable Parsing-Cursor
wird aus dem eigenen Request-Buffer und der Read-only-First-Line-Grenze
rekonstruiert; die vorhandene NUL-Terminierung der Header-Delimiter bleibt
damit explizit und gültig. Der Transaction-Finish-Branch nutzt nun eine
Short-Circuit-Konjunktion; C garantiert, dass der Finish-Aufruf nicht bei
einer Null-Transaction erfolgt, und bewahrt den bisherigen verschachtelten
Kontrollfluss.

## Geänderte Dateien

- `common/runtime/http_authorization_service.c`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260730-sonar-common-http-auth-maintenance.md`
- `reports/audits/change-records/CR-20260730-sonar-common-http-auth-maintenance.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Tatsächliches Ergebnis |
| --- | --- |
| `BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260730-common-sonar-remediation/build/http-auth-gcc VERIFIED_RUN_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260730-common-sonar-remediation/runtime/http-auth-gcc CC=gcc make check-http-authorization-service-timeout` | bestanden mit `-std=c17 -Wall -Wextra -Werror`; der Smoke schloss fehlerhafte CLI- und Timeout-Controls sowie drei Loopback-Request-/Response-Service-Controls ab. |
| Derselbe Befehl mit `CC=clang` und den getrennten externen `http-auth-clang`-Roots | bestanden mit demselben expliziten C17-Warnvertrag und Smoke-Controls. |
| `git diff --check` | vor Hinzufügen dieses Records bestanden; wird für den finalen Delivery-Kandidaten erneut ausgeführt. |

## Security-Auswirkung

Dies ist eine reine Maintainability-C-Typ-/Kontrollflusskorrektur in einer
HTTP-Autorisierungsgrenze. Sie verändert weder Header-Syntaxvalidierung,
Body-Size-Limits, Peer-/Local-Endpoint-Konvertierung, Transaction-Erzeugung,
Response-Serialisierung noch Timeout-Behandlung. Die Short-Circuit-Bedingung
behält den Null-Transaction-Guard bei, und kein Validierungs- oder Fehlerpfad
wurde gelockert.

## Runtime-Evidence

Der vorhandene `check-http-authorization-service-timeout`-Smoke kompiliert den
Service mit seinen realen Common-Abhängigkeiten und prüft ungültige CLI-Formen,
begrenzten Socket-Service-Start, Timeout-Verhalten und gültige HTTP-Request-
Verarbeitung. Dies ist fokussierte Service-Evidence, keine vollständige
Connector- oder libmodsecurity-Matrix.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine vollständige Connector-/CRS-/MRTS-Matrix lief: Der Patch ändert nur
  Common-Parser-Typqualifier und einen Short-Circuit-Ausdruck, nicht
  Connector-Integration oder Rule-Ausführung.
- Kein vollständiger Repository-Security-Scan lief: Die Source-Änderung
  enthält keinen neuen kontrollierten Input, Sink, Policy oder Security-
  Control; der fokussierte C-Smoke prüft die geänderte Service-Grenze.
- Hosted GitHub Actions, Current-Head-SonarQube-Cloud-Analyse und
  Review-Status liegen noch nicht vor, weil der Task-Branch noch nicht
  geliefert wurde. Sie sind erforderlich, bevor der Draft-PR als verifiziert
  gilt.

## Verbleibende Risiken

SonarQube Cloud bleibt die Autorität, um zu bestätigen, dass alle neun
ausgewählten Baseline-Code-Smells im PR-Vergleich verschwinden. Jeder spätere
Source- oder Dokumentationscommit erfordert eine frische Exact-Head-Hosted-
Verifikationsrunde.

## Finaler Diff- und Review-Status

Der Kandidat ist auf den ausgewählten Common-Service, erforderliche bilinguale
Traceability und keine Nested-Repository- oder Scanner-Konfigurationsdatei
beschränkt. Draft-PR [#196](https://github.com/Easton97-Jens/ModSecurity-conector/pull/196)
wurde vom Task-Branch erstellt. Dieser reine Record-Follow-up erfordert eine
frische Current-Head-GitHub-Actions-, SonarQube-Cloud- und Review-
Verifikationsrunde; kein Merge oder `master`-Change wird behauptet.
