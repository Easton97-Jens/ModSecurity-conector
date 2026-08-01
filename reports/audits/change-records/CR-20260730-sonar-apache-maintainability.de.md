# Change Record: Parent-Apache-Maintainability-Remediation

**Sprache:** [English](CR-20260730-sonar-apache-maintainability.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260730-sonar-apache-maintainability` |
| Datum (UTC) | 2026-07-30 |
| Basis-Revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | `FND-SONAR-0027`; 13 offene SonarQube-Cloud-`CODE_SMELL`-Befunde in `connectors/apache/src`. |
| Grenze | Nur Parent `connectors/apache/`, fokussierte Apache-Validierung, Regression-Contracts und dieses gepaarte Change-Record-/Index-Paar. |

## Motivation und Problemstellung

Das aktuelle SonarQube-Cloud-Inventar für `connectors/apache/src` meldet 13
Maintainability-Befunde: zwei überlange Parameterlisten, drei Cognitive-
Complexity-Befunde, sechs verschachtelte bedingte Ausdrücke, eine zu große
Runtime-State-Struktur und einen unbenutzten variadischen Helper. Im Inventar
gibt es keine offenen Apache-Security-, Reliability- oder Duplikatbefunde.

## Akzeptanzkriterien

- Jeder aufgezeichnete Sonar-Issue-Key wird durch eine Source-Remediation,
  nicht durch Suppression, Exclusion oder eine Scanner-/Quality-Gate-Änderung
  entfernt.
- Apache-Request-/Response-Event-Metadaten, Header-Snapshots, Phase-4-EOS-
  Containment, Directory-Config-Merge-Precedence und APR-Cleanup-Ownership
  behalten ihre bestehenden Contracts.
- Geänderte Apache-C-Units kompilieren unter C17 mit `-Wall -Wextra -Werror`;
  die fokussierten nativen Harnesses und Python-Regression-Contracts bestehen.
- Eine frische Exact-Head-Hosted-SonarQube-Cloud-Analyse bestätigt vor jeder
  Integration, dass die 13 Original-Keys und task-eigene Ersatzbefunde fehlen.
- Dieselbe Analyse meldet null neue Duplikatzeilen und null New-Code-
  Duplikatdichte; ein bestehendes Quality Gate genügt allein nicht.

## Implementierungsentscheidung und Begründung

Das Intervention-Event besitzt jetzt ein typisiertes Input-Objekt anstelle von
zwei breiten Funktionen und verschachtelter Auswahl. Request-, Response-
Snapshot-, Response-Gate- und Intervention-Felder werden nach Lifecycle-
Verantwortung gruppiert, ohne Lifetime oder Default-Zero-Initialisierung zu
ändern. Filter-Phasen und Directory-Merge sind in private, einzelne Helper
geteilt. Die unbenutzte File-Writing-Variadic-Funktion entfällt. Der native
Cleanup-Harness linkt nun APR-util, das `apr_brigade_cleanup` besitzt.

Während der Exact-Head-Hosted-Verifikation identifizierte SonarQube Cloud 18
neue Duplikatzeilen in den zwei Phase-1-Intervention-Pfaden von
`mod_security3.c`. Diese Pfade rufen nun einen privaten Event-Emission-Helper
mit denselben zwei Reason-Strings und dem ursprünglichen Intervention-Status
auf. Der Helper behält typisierte Event-Felder, Phase, Redirect-/Deny-
Entscheidung und den begrenzten Common-Event-Writer unverändert bei und
entfernt zugleich den Duplikatblock.

## Geänderte Dateien

- `connectors/apache/src/mod_security3.c`
- `connectors/apache/src/mod_security3.h`
- `connectors/apache/src/msc_config.c`
- `connectors/apache/src/msc_filters.c`
- `connectors/apache/src/msc_utils.c`
- `connectors/apache/src/msc_utils.h`
- `ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh`
- fokussierte Apache-Regression-Contract-Tests und dieses gepaarte Change-
  Record-/Index-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Fokussierter Intervention-Cleanup-Contract | bestanden (5 Tests). |
| Fokussierte Phase-4- und Synchronized-Upstream-Contracts | bestanden (17 Tests). |
| `make check-apache-request-transaction-cleanup` | bestanden; nativer APR-Lifecycle-Harness besteht nach APR-util-Linking des Runners. |
| `make check-apache-ruleset-cleanup` | bestanden; nativer RulesSet-APR-Lifecycle-Harness besteht. |
| Direkte Changed-Unit-C17-Kompilierung | bestanden für `msc_config.c`, `msc_filters.c` und `msc_utils.c` mit `-Wall -Wextra -Werror`. |
| Direkte Mapper-C17-Kompilierung | bestanden mit der gruppierten State-Definition. |
| Phase-1-Event-Emission-Regression-Contract | bestanden (7 Tests); beide ursprünglichen Reason-Strings laufen durch den einen begrenzten Writer. |
| Vollständiges `make check-apache-c17` | durch bestehende Current-Master-Diagnosen in `mod_security3.c` und `msc_config.h` blockiert, getrennt als `FND-PARENT-0069` getrackt; der C17-Compiler erreicht die geänderte Unit und meldet bis zum Baseline-Stopp keine Helper-spezifische Diagnose. |
| `git diff --check` | nach der Duplikat-Remediation bestanden; läuft erneut vor Delivery. |

## Security-Auswirkung

Der Refaktor bewahrt die Request-/Response-Trust-Boundary: Response-Bodies
bleiben bis EOS set aside, Phase-4-Fehler bleiben fail-closed und Intervention-
Records bewahren die begrenzte Common-Event-Serialisierung. Keine
Authentifizierung, Autorisierung, Input-Validation, Logging-Policy, Sonar-
Kontrolle, Framework-, MRTS-, Gitlink- oder Workflow-Permission wird
abgeschwächt oder geändert.

Die Phase-1-Extraktion ändert weder Intervention-Entscheidung noch Request-
Pfad: Originalstatus und beide Reasons bleiben explizite Caller-Argumente,
und das Event wird weiterhin erzeugt, bevor dasselbe Intervention-Ergebnis an
Apache zurückgeht.

## Runtime-Evidence

Die realen APR-Harnesses prüfen Request-Transaction-Cleanup und Directory-
RulesSet-Ownership. Phase-4-Regression-Contracts bewahren Assertions für
normal, deny, log-only, ErrorDocument, fragmentierte Buckets und Terminal-
Output.

## Bekannte Einschränkungen

Kein Live-Apache/httpd-Prozess, CRS oder vollständige Connector-Matrix lief
lokal. Die vollständige C17-Aggregation kann erst bestehen, wenn die
unabhängigen Current-Master-Diagnosen aus `FND-PARENT-0069` behoben sind.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Live-Host-Matrix oder vollständiger Repository-Security-Scan lief, weil
dies ein fokussierter Maintainability-Refaktor einer bereits abgedeckten nativen
Filter-Boundary ist. Hosted Actions, Review und Exact-Head-SonarQube-Cloud-
Evidence stehen bis zur Draft-PR-Delivery aus.

## Verbleibende Risiken

SonarQube Cloud ist die Autorität für die Original-Keys. Lokale Kompilierung
und fokussierte Tests können weder deren endgültige Entfernung noch neue Issues
beweisen; keine Integration wird bis zu einer frischen grünen Exact-Head-
Hosted-Analyse beansprucht.

## Finaler Diff- und Review-Status

Der Kandidat ist Source-lokal, soweit die aktuelle Baseline es erlaubt C17-
geprüft und mit Traceability gepaart. Delivery und Exact-Head-Verifikation
stehen aus; kein Merge oder `master`-Change wird beansprucht.

## Delivery-Autorisierung

Der aktuelle Nutzer autorisierte die Parent-Integration ausdrücklich mit:
`bringe das pr 205 in den master`. Diese Autorisierung gilt nur für PR #205
und nur nachdem sein aktueller Head die vollständige frische Integrations-
Prüfung einschließlich null neuer Issues und null New-Code-Duplikation
bestanden hat. Sie autorisiert weder einen direkten `master`-Push noch einen
Bypass, eine Framework-/MRTS-Änderung oder ein Gitlink-Update. Bei dieser
Record-Revision ist kein Merge erfolgt.
