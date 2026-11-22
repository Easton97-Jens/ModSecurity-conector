# Change Record: CR-20261119-verified-cppcheck-findings-connector-hardening

**Sprache:** [English](CR-20261119-verified-cppcheck-findings-connector-hardening.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261119-verified-cppcheck-findings-connector-hardening |
| Datum (UTC) | 2026-11-19 |
| Basis-Revision | `b79c3d93efbb8330f121caf8fb7c1a7874195e57` |

## Motivation und Problemstellung

Ein Cppcheck-2.22.0-Scan des gesamten Checkouts meldete rund 1.800 Diagnosen. Jede
priorisierte Diagnose im Parent-Produktcode wurde gegen den realen Kontrollfluss und die
reale Compiler-Konfiguration geprüft. Die meisten waren Analyseartefakte: Der Scan definierte
`__linux__` nicht, parste keine System- oder Host-Header und vermischte Framework-Test-Stubs
mit der übersetzungseinheitenübergreifenden Analyse von `common/runtime/`. Zwei
Parent-Defekte wurden bestätigt:

1. `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`,
   `phase4_common_event_write()`: Das vorzeichenbehaftete `int`-Feld `decision->rule_id`
   wurde mit `%u` formatiert. Ein negativer Wert ist für diese Konvertierung undefiniertes
   Verhalten und erschien als große vorzeichenlose Zahl (`-7` wurde zu `4294967289`), und
   „keine Regel“ (`0`) erschien als `"0"`. Das kanonische HAProxy-Binding
   (`haproxy_modsecurity_binding.c`) gibt nur positive IDs aus und lässt „keine Regel“ leer.
2. `connectors/nginx/src/ngx_http_modsecurity_module.c`: Die Analyse ohne NGINX-Header
   meldete Syntaxfehler bei drei Aufrufen von `ngx_http_set_ctx(...)`. NGINX 1.31.8 liefert
   das abschließende Semikolon in der Makrodefinition. Die zunächst ergänzten Semikola
   erzeugten drei SonarCloud-Befunde `c:S1116` zu leeren Anweisungen und wurden im Review
   entfernt. Die statische Analyse benötigt die konfigurierten NGINX-Header.

## Akzeptanzkriterien

- SPOP-Phase-4-Common-Events geben positive Regel-IDs unverändert aus und geben `0` sowie
  negative Werte als leere `rule_id` aus.
- Die NGINX-Aufrufe verwenden das abschließende Semikolon aus dem konfigurierten Makro
  und kompilieren mit der erfassten C17-Konfiguration.
- Die nativen C17-Prüfungen für HAProxy, Apache, NGINX und die übrigen Connectoren bestehen.
- Ein realistischer Cppcheck-Lauf über alle Parent-Produkt-Übersetzungseinheiten meldet
  keinen verbleibenden bestätigten Defekt; verbleibende Diagnosen sind disponiert.

## Implementierungsentscheidung und Begründung

- `haproxy_spop_diagnostic_runtime.c`: Formatierung mit `%d` nur bei `rule_id > 0`, sonst
  leerer String. Damit wird die vorhandene kanonische Binding-Regel wiederverwendet statt
  eine neue Konvention einzuführen. Die Änderung ist identisch mit der bereits vorhandenen,
  nicht committeten Änderung im Arbeitsbaum des Maintainers, sodass eine spätere Integration
  nicht kollidiert.
- `ngx_http_modsecurity_module.c`: Die drei ursprünglichen Makroaufrufe bleiben erhalten.
  Die Definition aus NGINX 1.31.8 liefert das abschließende Semikolon, sodass ein weiteres
  Semikolon eine leere Anweisung erzeugt. Parserdiagnosen ohne Header benötigen korrigierte
  Präprozessor-Eingaben.
- Keine weitere Parent-Quelle wurde geändert. Fail-open-/Fail-closed-Richtlinie, API, ABI
  und Wire-Protokoll bleiben unverändert.
- Der Framework-Gitlink wird durch diesen Record nicht geändert. Die Regressionstests für
  beide Fixes und der NDEBUG-Testhygiene-Fix liegen im separaten Framework-Repository und
  werden über einen eigenen Framework-Pull-Request geliefert.

## Geänderte Dateien

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `reports/audits/change-records/CR-20261119-verified-cppcheck-findings-connector-hardening.md`
- `reports/audits/change-records/CR-20261119-verified-cppcheck-findings-connector-hardening.de.md`

## Ausgeführte Befehle

Alle Befehle liefen über RTK in einem Task-Worktree; Build-, Temporär- und Logausgaben lagen
im task-eigenen externen Run-Root `cppcheck-audit-20261119T095825Z`.

| Befehl | Ergebnis |
| --- | --- |
| `rtk bypass make check-haproxy-c17` (mit Bear erfasst) | Exit 0, `PASS: haproxy_c_standards c17 compile completed` |
| `rtk bypass make check-apache-c17` (mit Bear erfasst) | Exit 0, `PASS: apache_c_standards c17 compile` |
| `rtk bypass make check-nginx-c17` (mit Bear erfasst, konfigurierte NGINX-1.31.8-Header) | Exit 0, `PASS: nginx_c_standards c17 compile completed` |
| `rtk bypass make check-remaining-connectors-c17` (mit Bear erfasst) | Exit 0, `PASS: remaining connectors C standard check (c17)` |
| `rtk bypass cppcheck --project=<Bear-Compile-Datenbank> --enable=all --inconclusive --std=c17 --library=posix -D__linux__ ...` über 105 Parent-Produkt-Übersetzungseinheiten | Exit 0; jede Parent-Diagnose disponiert (siehe Bekannte Einschränkungen) |
| Framework-On-Demand-Test `test_haproxy_spop_event_sink_failures...test_phase4_event_renders_only_positive_signed_rule_ids` | Basis-Revision: 2 Fehlschläge (`'0' != ''`, `'4294967289' != ''`); diese Änderung: OK |
| Framework-On-Demand-Modul `test_nginx_upstream_security_contract` bei der ersten PR-Veröffentlichung | einziger Statuswechsel: `test_context_creation_returns_only_context_or_null` auf der Basis ERROR, mit den später entfernten redundanten Semikola ok; die übrigen 7 nicht bestandenen Fälle sind auf Basis und Änderung identisch |
| Framework-On-Demand-Modul `test_haproxy_spop_event_sink_failures`, auch mit `CC="gcc -fsanitize=address,undefined"` | alle Fälle OK, keine Sanitizer-Meldung |
| `rtk make check-active-inventory` | Exit 0, `active_case_count` 100 von `hard_limit` 100 |

## Security-Auswirkung

Der SPOP-Fix beseitigt undefiniertes Verhalten bei der Event-Formatierung und hält
Audit-Events konsistent mit dem kanonischen Regel-ID-Vertrag, sodass eine fehlende oder
ungültige Regel-ID in Phase-4-Evidence nicht mehr als erfundene große Regelnummer erscheinen
kann. Keine Durchsetzungsentscheidung, kein Statuscode, kein Fail-Modus und kein
Transportverhalten ändert sich. Das NGINX-Review erhält die ursprünglichen Makroaufrufe
und dokumentiert die für die statische Analyse benötigten konfigurierten Header.

## Runtime-Evidence

Keine. Es wurde kein HAProxy- oder NGINX-Host gestartet. Die Evidence beschränkt sich auf
Kompilierung, den SPOP-Harness mit extrahierten Funktionen, Quelltext-Vertragstests und
statische Analyse.

## Bekannte Einschränkungen

- Die verbleibenden Parent-Cppcheck-Diagnosen wurden geprüft und sind keine Defekte:
  `__linux__`- und Fehlende-Header-Artefakte, übersetzungseinheitenübergreifende
  Kontamination durch Framework-Test-Stubs (getrennte Scans vermeiden sie),
  Längenabfragen `snprintf(NULL, 0, ...)`, `fdopen()`-Fehlerpfade, die den Deskriptor
  korrekt schließen, `NULL`-Attribute für `pthread_*_init`, `apr_pstrcat(..., NULL)` in C
  mit glibc sowie redundante Defensivbedingungen.
- Das lighttpd-Modul wurde ohne lighttpd-Header analysiert (lokal nicht verfügbar).

## Verbleibende Risiken

Gering. Konsumenten, die sich auf die bisherige Regel-ID `"0"` in SPOP-Phase-4-Events
verlassen haben, erhalten nun einen leeren Wert, passend zu den HAProxy-Binding-Events.

## Nicht ausgeführte Prüfungen mit Begründung

- Host-Runtime- und Lifecycle-Tests für HAProxy SPOE/SPOP und NGINX: nicht Teil dieses
  Bugfix-Umfangs; lokal sind keine Host-Binärdateien installiert.
- `make test` und `make quick-check`: nicht vollständig ausgeführt; stattdessen wurden
  gezielte native Prüfungen und die betroffenen Framework-On-Demand-Tests ausgewählt.
- Cloud Quality Gate: CI-eigen; Ergebnisse gehören zum Pull-Request-Head.

## Finaler Diff- und Review-Status

Die finale Produktänderung umfasst die HAProxy-Regel-ID-Korrektur plus dieses Record-Paar.
Die NGINX-Quelle entspricht den ursprünglichen Makroaufrufen. Am 2026-11-22 kompilierte
die tatsächliche NGINX-Modul-Übersetzungseinheit mit der erfassten GCC-15-C17-Konfiguration,
NGINX-1.31.8-Headern und `-Wall -Wextra -Werror` erfolgreich. Der aufgabeneigene Adapter
`nginx455-compile.py` leitet ausschließlich Checkout-Pfade und Objekt-/Abhängigkeitspfade
aus der vorhandenen Compile-Datenbank um. `git diff --check` bestand.

Der gezielte Framework-Test `test_context_creation_returns_only_context_or_null` verlangt
in Zeile 49 weiterhin ein am Aufruf geschriebenes Semikolon und scheiterte nach der
Makrokorrektur mit `ValueError: substring not found`. Seine Quelltextprüfung benötigt
eine Framework-Nacharbeit, die das vom gepinnten Makro gelieferte Semikolon berücksichtigt.
