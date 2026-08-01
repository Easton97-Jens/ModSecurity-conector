# FND-PARENT-0067 — Apache name_for_debug verwendet über den Konfigurations-Lifecycle hinweg eine nicht besessene strdup-Allocation

- Kategorie: `lifecycle_defect`
- Repository / Ownership: `parent` / `parent`
- Priorität / Schweregrad / Konfidenz: `P2` / `not_applicable` / `validated`
- Status / Machbarkeit: `validated` / `feasible_now`
- Release-Blocker / Sicherheitsrelevanz: `false` / `false`
- Sicherheitsbewertung: `not_applicable_trusted_apache_configuration_lifecycle_no_attacker_boundary`
- Connector / Protokoll / Profil: `apache` / `Apache configuration-pool lifecycle and graceful restart` / `Private Apache graceful-restart Memcheck control`

## Zusammenfassung

Ein privater Apache-Graceful-Restart-Memcheck-Lauf validiert einen getrennten Parent-Lifecycle-Leak. Parent-master weist `strdup(path)` an `name_for_debug` in `msc_hook_create_config_directory` bei `connectors/apache/src/msc_config.c:416` zu. Der aufbewahrte Log meldet `66` definitiv verlorene Bytes in `3` Blöcken; beide Allocation-Stacks laufen über `strdup` und die Connector-DSO-Adresse `0x53D1BEB`.

Der Log enthält keine Invalid-free/read/write- oder Use-After-Free-Diagnose. Der Memcheck-Command endet mit `99`, weil er definite Leaks bewusst als Fehler behandelt. Dies ist ein P2-Defekt im vertrauenswürdigen Konfigurations-Lifecycle, kein Sicherheitsbefund und kein Release-Blocker. Er ist unabhängig vom RulesSet-Cleanup aus `FND-PARENT-0064`, und die aktuelle Aufgabe enthält keine Source-Reparatur.

## Beobachtetes und erwartetes Verhalten

Auf Parent-master `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` verwendet der Nicht-Null-`path`-Zweig:

```c
cnf->name_for_debug = strdup(path);
```

Der task-eigene private Apache-Graceful-Restart-Lauf meldet zwei Definitive-Leak-Kontexte: `22` Bytes in einem Block und `44` Bytes in zwei Blöcken. Beide Stacks enthalten `strdup`, Connector-DSO-Adresse `0x53D1BEB` und Apache-Konfigurationstraversierung. Die Diagnose summiert sich auf `66` Bytes in `3` Blöcken.

Debug-Name-Storage, der zu einer Konfigurationsgeneration gehört, muss einen expliziten Owner haben und bei Zerstörung dieser Generation freigegeben werden, während legitime Debug-Name-Reads während der normalen Lebenszeit dieser Generation gültig bleiben.

## Impact und Grenzbewertung

Der beobachtete private Lauf leakt `66` Bytes in `3` Blöcken. Wiederholte Konfigurationserzeugung und Graceful-Restarts können diese vertrauenswürdige Lifecycle-Allocation akkumulieren. Das Ergebnis belegt weder Angreiferkontrolle, externe Ausnutzbarkeit, Korruption, Invalid-Free, UAF, einen Release-Blocker noch einen Sicherheitsimpact.

## Betroffener Scope, Voraussetzungen und Reproduktion

- Datei: `connectors/apache/src/msc_config.c`.
- Symbole: `msc_hook_create_config_directory`, `msc_conf_t.name_for_debug` und `strdup`.
- Voraussetzungen: Der Parent-Apache-Connector ist privat geladen; Apache erzeugt Per-Directory-Konfigurationen mit Nicht-Null-Pfaden; der Prozess führt unter Memcheck einen `SIGUSR1`-Graceful-Restart und eine Terminierung aus.
- Aktuellen Master bei Zeilen `414`–`417` prüfen, dann den aufbewahrten privaten Memcheck-Control mit `--leak-check=full`, `--show-leak-kinds=definite`, `--errors-for-leak-kinds=definite` und `--error-exitcode=99` ausführen.
- `memcheck.8.log` meldet `22` plus `44` definitiv verlorene Bytes und keine Invalid-Memory-Access-Diagnose.

## Evidence

| Typ | Artefakt | SHA-256 | Exit | Ergebnis |
| --- | --- | --- | ---: | --- |
| Privater Graceful-Memcheck | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/graceful-memcheck/memcheck.8.log` | `a49ca3a72f06aef4f4e67bab0b57056fe785c95a1dfba2361a892fbbf497b931` | 99 | `66` definitiv verlorene Bytes in `3` Blöcken über `strdup` und `0x53D1BEB`; kein Invalid free/read/write oder UAF. |
| Privates Restart-Log | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/apache-runtime/error.log` | `d65d607196ecc06f09179a5db5cc11ffb5fa332185d0f4d5125a3f47923165b4` | 0 | `AH00493` dokumentiert SIGUSR1-Restart, `AH00489` Wiederaufnahme und `AH00491` saubere Terminierung. |

## Root Cause und Remediation-Richtung

Die Konfigurationsfabrik alloziert `name_for_debug` über libc-`strdup` statt über Storage, der dem APR-Konfigurationspool gehört, und der aktuelle Source hat keinen dedizierten Cleanup-Owner. Die Memcheck-Allocation-Stacks korrelieren diesen Pfad mit der Apache-Konfigurationstraversierung.

Vor einer Source-Änderung einen getrennten lifecycle-sicheren Ownership-Vertrag auswählen: bestimmen, ob der Debug-Name dem APR-Pool gehören oder einen engen Cleanup erhalten soll; Creation-, Merge-, Error-, Shutdown- und alle späteren Debug-Use-Pfade verifizieren; dann eine fokussierte Regression ergänzen und denselben privaten Memcheck-Control erneut ausführen. Die aktuelle Aufgabe enthält absichtlich keine Source-Reparatur für dieses Finding.

## Akzeptanzkriterien und Validierungsplan

1. Ein getrennt reviewtes Ownership-Design etabliert einen gültigen Cleanup-Owner, ohne eine legitime Debug-Name-Lebenszeit zu verkürzen.
2. Fokussierte Tests decken Nicht-Null-Creation, Merge-/Error-Pfade, Pool-Zerstörung und legitimen Debug-Name-Zugriff ab, soweit anwendbar.
3. Die private Apache-Graceful-Restart-Memcheck-Reproduktion meldet den `strdup`-basierten `66`-Byte-Definitive-Leak nicht mehr.
4. Die resultierende Änderung erhält fokussierte Lifecycle-/Security-Review und Exact-Head-Validierung vor `fixed` oder `verified`.

## Abhängigkeiten, verwandte Findings und Restrisiko

- Ein Follow-up benötigt einen task-eigenen Parent-Worktree sowie eine private Apache/APXS/APR/libmodsecurity/Valgrind-Umgebung.
- Verwandtes Finding: `FND-PARENT-0064`. Es besitzt RulesSet-Heap-Cleanup; dieses Finding besitzt `name_for_debug`-String-Storage. Beide Korrekturen müssen unabhängig sicher und unabhängig getestet bleiben.
- Restrisiko: Dieser P2-Leak bleibt auf Parent-master und im aktuellen RulesSet-Cleanup-Kandidaten. Er ist keine Security- oder Release-Blocker-Behauptung, und es wird keine Source-Reparatur, kein PR, kein Merge oder Master-Disposition behauptet.

## Historie

- `2026-07-29T09:04:55Z`: private Graceful-Restart-Memcheck-Evidence validierte den getrennten `strdup(path)`-Lifecycle-Leak und reservierte diese kanonische ID.
