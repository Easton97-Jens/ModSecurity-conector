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
2. `connectors/nginx/src/ngx_http_modsecurity_module.c`: Drei Aufrufe von
   `ngx_http_set_ctx(...)` hatten kein abschließendes Semikolon und verließen sich darauf,
   dass das NGINX-Makro es liefert. Ohne NGINX-Header melden Analysewerkzeuge einen
   Syntaxfehler und überspringen die gesamte Übersetzungseinheit; der Framework-Vertragstest
   `test_context_creation_returns_only_context_or_null` sucht die abgeschlossene Anweisung
   und schlug mit `ValueError: substring not found` fehl.

## Akzeptanzkriterien

- SPOP-Phase-4-Common-Events geben positive Regel-IDs unverändert aus und geben `0` sowie
  negative Werte als leere `rule_id` aus.
- Die Anweisungsform im NGINX-Modul ist abgeschlossen, und der vorhandene Vertragstest
  besteht.
- Die nativen C17-Prüfungen für HAProxy, Apache, NGINX und die übrigen Connectoren bestehen.
- Ein realistischer Cppcheck-Lauf über alle Parent-Produkt-Übersetzungseinheiten meldet
  keinen verbleibenden bestätigten Defekt; verbleibende Diagnosen sind disponiert.

## Implementierungsentscheidung und Begründung

- `haproxy_spop_diagnostic_runtime.c`: Formatierung mit `%d` nur bei `rule_id > 0`, sonst
  leerer String. Damit wird die vorhandene kanonische Binding-Regel wiederverwendet statt
  eine neue Konvention einzuführen. Die Änderung ist identisch mit der bereits vorhandenen,
  nicht committeten Änderung im Arbeitsbaum des Maintainers, sodass eine spätere Integration
  nicht kollidiert.
- `ngx_http_modsecurity_module.c`: `;` nach den drei Aufrufen ergänzt. Mit dem echten
  NGINX-Makro entsteht nur eine leere Anweisung in einem Block mit geschweiften Klammern;
  erzeugter Code und Verhalten bleiben unverändert.
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
| Framework-On-Demand-Modul `test_nginx_upstream_security_contract` | einziger Statuswechsel: `test_context_creation_returns_only_context_or_null` auf der Basis ERROR, mit dieser Änderung ok; die übrigen 7 nicht bestandenen Fälle sind auf Basis und Änderung identisch |
| Framework-On-Demand-Modul `test_haproxy_spop_event_sink_failures`, auch mit `CC="gcc -fsanitize=address,undefined"` | alle Fälle OK, keine Sanitizer-Meldung |
| `rtk make check-active-inventory` | Exit 0, `active_case_count` 100 von `hard_limit` 100 |

## Security-Auswirkung

Der SPOP-Fix beseitigt undefiniertes Verhalten bei der Event-Formatierung und hält
Audit-Events konsistent mit dem kanonischen Regel-ID-Vertrag, sodass eine fehlende oder
ungültige Regel-ID in Phase-4-Evidence nicht mehr als erfundene große Regelnummer erscheinen
kann. Keine Durchsetzungsentscheidung, kein Statuscode, kein Fail-Modus und kein
Transportverhalten ändert sich. Die NGINX-Änderung hat keine Laufzeit-Security-Wirkung; sie
stellt die vollständige statische Analyse des Moduls wieder her.

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

Zwei Produktdateien mit minimalen Änderungen plus dieses Record-Paar. Der Diff wurde auf
Umfang und Whitespace geprüft (`git diff --check`).
