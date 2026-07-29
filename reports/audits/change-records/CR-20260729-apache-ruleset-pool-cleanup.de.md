# Change Record: Apache-RulesSet-Konfigurationspool-Cleanup

**Sprache:** [English](CR-20260729-apache-ruleset-pool-cleanup.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-apache-ruleset-pool-cleanup` |
| Datum (UTC) | `2026-07-29` |
| Bewertungs-Baseline | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Grenze | Parent-Apache-Connector-Source, fokussierte Checks und Harnesses, Source-Provenance und dieses englisch/deutsche Change-Record-/Index-Paar. Framework und MRTS bleiben schreibgeschützter Build-Kontext; Repository, Gitlink, Abhängigkeit, CI-Policy und Runtime-Matrix werden nicht geändert. |
| Finding-Verknüpfung | `FND-PARENT-0064` (RulesSet-Lifecycle), `FND-PARENT-0008` (C17-Sentinel), `FND-PARENT-0068` (Runner-Output-Confinement), `FND-PARENT-0069` (geerbter aggregierter C17-Diagnosebefund), `FND-PARENT-0070` (APXS-Header-Materialisierung) und `FND-PARENT-0071` (isoliertes MIME-Artefakt-Layout). |
| Upstream-Referenz | Selektive Übernahme von `owasp-modsecurity/ModSecurity-apache` PR #94 Commit `5ea3fc9da876195706375cf35f321de2a1f35ce1`; keine andere Änderung aus Upstream PR #91–#94 ist enthalten. |

## Entscheidung und Umfang

Apache erstellt pro Per-Directory-Konfigurationsobjekt ein `RulesSet`. Vor dieser Änderung war ein erfolgreiches `msc_create_rules_set()`-Ergebnis nicht beim besitzenden APR-Konfigurationspool registriert. Die ausgewählte Upstream-Änderung #94A fügt den zugehörigen APR-Cleanup-Callback unmittelbar nach einer nicht-null Allokation ein. APR besitzt damit genau einen Cleanup für dieses Objekt; Request-, Merge- und globale Modul-Teardowns erhalten keinen konkurrierenden manuellen Cleanup-Pfad.

Der Vergleich mit dem aktuellen Parent schließt das übrige Upstream-Material aus:

- #91 ist eine inkompatible Handler-/Body-Architektur; Parent besitzt bereits eine eigene stärkere EOS-/Drain-Grenze.
- #92 ist Docker-/Compose-Build-Stack-Arbeit und hier nicht anwendbar.
- #93 ist eine mögliche spätere lokale Evidenzmethode, kein nachgewiesener Produktdelta.
- Der Intervention-String-Teil von #94 ist bereits durch Parents getrenntes request-eigenes Intervention-Cleanup abgedeckt.

Die Exact-Candidate-Validierung zeigte zusätzlich zwei unabhängige, geerbte Parent-Build-/Harness-Defekte, die den normalen Apache-Control sonst vor der Prüfung der ausgewählten Lifecycle-Änderung beenden. Ihre engen Reparaturen sind in dieser Parent-Auslieferung enthalten:

- Der APXS-Wrapper kopiert jetzt den festen privaten `header_validation_internal.h` neben die bestehenden Common-C-Sources. Ein frischer materialisierter Build kompiliert `request_helpers.c` sonst ohne seinen quoted sibling Header.
- Der isolierte Apache-Smoke-Harness erzeugt dieselbe generierte MIME-Datei jetzt sowohl unter `$ServerRoot/mime.types` als auch unter `$ServerRoot/conf/mime.types`. Das entspricht der unterstützten Apache-Standardauflösung, ohne Konfigurationstext, Regeln oder Request-Verhalten zu ändern.

Der Directive-Table-Terminator wird zum verhaltensgleichen Sentinel `{ .name = NULL }`. Dies ist nötig, damit die geänderte Translation Unit mit beiden vorhandenen Compilern die normale strikte C17-Kompilierung besteht; Apache-Directive-Dispatch wird nicht verändert.

## Akzeptanzkriterien

- Jede erfolgreiche Apache-`msc_create_rules_set()`-Allokation registriert genau einen Cleanup beim besitzenden APR-Konfigurationspool; eine Null-Allokation registriert keinen.
- Pool-Clear/-Destruction ruft `msc_rules_cleanup()` für jedes besessene nicht-null RulesSet genau einmal auf, einschließlich unabhängig erzeugter Merge-Konfigurationen und ihrer Fehlerpfade.
- In Request-, Merge- oder globale Modul-Teardown-Pfade wird kein manueller RulesSet-Cleanup eingefügt.
- Die geänderte Translation Unit besteht den realen APR-Harness unter GCC und Clang C17 mit `-Wall -Wextra -Werror` ohne Warnungsunterdrückung oder Änderung produktiver Compiler-Flags.
- Ein frisch materialisierter APXS-Build enthält den privaten Header, den gestagte Common-Sources benötigen, und erzeugt das Apache-DSO.
- Ein normaler isolierter Apache-HTTP/1.1-Control lädt genau dieses DSO, liefert für `phase2_args_block` das erwartete `403` und übersteht einen `SIGUSR1`-Graceful-Restart mit Readiness vor und nach dem Signal.
- Der fokussierte Runner behält seine Private-Output- und Unsafe-Parent-Schutzmaßnahmen; Workflow, Runtime-Matrix, Scanner, Quality Gate oder Branch-Protection-Control werden nicht geschwächt.

## Implementierung

`msc_config.c` definiert `msc_rules_set_cleanup()` und registriert ihn mit `apr_pool_cleanup_register()` nur nach erfolgreichem `msc_create_rules_set()`. Der APR-Harness verwendet reale APR-Pools und deterministische RulesSet-Stubs für normale Konstruktion, Null-Konstruktion, Pool-Clear, erfolgreichen Merge und jeden Merge-Fehlerpfad. Der Source-Contract schützt Callback-Platzierung und verbietet einen künftigen konkurrierenden manuellen Cleanup.

Der native Harness-Runner verwendet eine validierte temporäre Parent-Kette, `umask 077` und ein neues privates `mktemp -d`-Leaf. Er prüft Ownership und Modus vor der Kompilierung, ignoriert Legacy-caller-selected Output-Pfade und entfernt ausschließlich die exakte generierte Binärdatei und das Leaf-Verzeichnis nicht-rekursiv.

Die APXS-Wrapper-Korrektur ist eine Literal-Header-Staging-Änderung mit einer fokussierten Apache/Common-Strukturassertion. Die MIME-Korrektur kopiert oder erzeugt dasselbe Artefakt an beiden konventionellen Orten; sie führt keinen request-abgeleiteten Pfad, keine Shell-Auswertung, keine dynamische Konfigurationsdirektive und keinen neuen ausführbaren Input ein.

## Geänderte Dateien

- `connectors/apache/src/msc_config.c`
- `connectors/apache/SOURCE_MAP.json`
- `connectors/apache/build/apxs-wrapper.in`
- `connectors/apache/harness/run_apache_smoke.sh`
- `ci/checks/connectors/apache/apache_rules_set_cleanup.c`
- `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh`
- `ci/checks/connectors/apache/check-apache-common-adoption.py`
- `tests/test_apache_rules_set_cleanup.py`
- `tests/test_apache_smoke_mime_types.py`
- `Makefile`
- `reports/audits/change-records/README.md`, `README.de.md` und dieses gepaarte Change Record

## Validierungsevidenz

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Fokussierte Source-Contracts | bestanden: sechs Python-Tests decken RulesSet-Ownership, das benannte C17-Sentinel, privaten Runner-Output und beide MIME-Orte ab. |
| Shell-Syntax | bestanden für RulesSet-Runner, Apache-Smoke-Harness und APXS-Wrapper-Template. |
| Fokussierter Apache/Common-Strukturcheck | bestanden, einschließlich der Private-Header-Materialisierungsassertion. |
| GCC-C17-APR-Lifecycle-Harness | bestanden mit `-Wall -Wextra -Werror`. |
| Clang-C17-APR-Lifecycle-Harness | bestanden mit `-Wall -Wextra -Werror`. |
| `make check-apache-ruleset-cleanup-lint` | bestanden; der Statusbeleg meldet `apache_rules_set_cleanup` als `passed`. |
| Apache-C-Standard-Wiring und JSON-Source-Map-Validierung | bestanden. |
| Frische Materialisierung, Autotools-Konfiguration und APXS-DSO-Build | nach der Literal-Private-Header-Staging-Korrektur bestanden; das exakte Kandidaten-DSO wurde erzeugt. |
| Isolierter Apache-`phase2_args_block`-HTTP/1.1-Control | bestanden: Das exakte DSO lud und der konfigurierte Request lieferte `403`. |
| Isolierter Apache-Graceful-Restart-Control | bestanden: Readiness war vor und nach `SIGUSR1` erfolgreich. |
| Fokussierter Post-Scan-Security-Review von C17-Sentinel, APXS-Header-Staging und MIME-Korrektur | bestanden: kein neuer reportbarer Security-Befund. |
| Aggregiertes `make check-apache-c17` | auf der Bewertungs-Baseline und dem Kandidaten identisch in unverändertem `connectors/apache/src/mod_security3.c` fehlgeschlagen; separat als `FND-PARENT-0069` erfasst und nicht als bestandene Evidence behauptet. |

Der ursprüngliche Baseline-APR-Harness schlug erwartbar fehl, weil sein erstes nicht-null RulesSet keinen Pool-Cleanup hatte. Der ursprüngliche frisch materialisierte APXS-Tree enthielt den privaten Header nicht, und die ursprüngliche isolierte Runtime endete vor der Request-Verarbeitung, weil Apache die MIME-Datei im Root nicht auflösen konnte. Diese zurückgehaltenen Fehler sind die jeweilige Pre-Fix-Evidence der enthaltenen Reparaturen.

## Security-Auswirkung

Dies ist eine native C-Konfigurations-Lifecycle- und Availability-Remediation. Regeln sind vertrauenswürdige Apache-Operator-Konfiguration, nicht direkter nicht vertrauenswürdiger HTTP-Input. Der Cleanup-Callback wird nur nach erfolgreicher Allokation registriert, ruft seine passende native Cleanup-Funktion auf und vermeidet frühe oder doppelte Cleanup-Grenzen.

Der frühere Candidate-Security-Review liegt unter dem registrierten Task-Root. Ein fokussierter Follow-up-Review der drei späteren Deltas fand keinen neuen reportbaren Kandidaten: Das benannte Sentinel ist datenunabhängig, Header-Staging ist eine feste Literal-Kopie und das zweite MIME-Artefakt ist deterministisch unter dem bestehenden validierten Runtime-Root. Die funktionale Smoke-Ausführung ist getrennt in der Validierungsevidenz erfasst.

## Protokoll- und Runtime-Grenzen

Die Evidence belegt den betroffenen Apache-Konfigurationspool-Lifecycle, frische DSO-Materialisierung und einen normalen HTTP/1.1-Control. HTTP/2, HTTP/3, die vollständige Connector-Matrix und eine Valgrind-leak-free-Zertifizierung wurden nicht ausgeführt; sie ersetzen den spezifischen APR-Ownership-Nachweis nicht. Ein diagnostischer Valgrind-Lauf zeigte im ausgeübten Pfad kein Invalid-Free und kein Use-after-free, aber ein unabhängiger `name_for_debug`-Leak bleibt außerhalb dieser Delivery-Scope.

## Delivery-Status

Bei Aktualisierung dieses Records ist dies ein lokaler task-eigener Parent-Commit und sein Task-PR ist noch nicht veröffentlicht. Der aktuelle Nutzer autorisierte einen neuen Parent-PR und die geschützte `master`-Integration nach Exact-Head-Validierung. Parent PRs #123/#124 sind nur Source-Referenzen und werden nicht pauschal gemergt. Hosted Checks, SonarQube Cloud, Review-/Thread-Status, Mergeability, geschützte Integration und Resulting-Master-Verifikation dürfen erst nach tatsächlicher Beobachtung eingetragen werden.
