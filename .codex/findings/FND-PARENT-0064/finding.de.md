# FND-PARENT-0064 — Der Apache-RulesSet-Allocation fehlt eine APR-Config-Pool-Cleanup-Bindung

- Kategorie: `lifecycle_defect`
- Repository / Ownership: `parent` / `parent`
- Priorität / Schweregrad / Konfidenz: `P1` / `not_applicable` / `validated`
- Status / Machbarkeit: `verified` / `feasible_now`
- Release-Blocker / Sicherheitsrelevanz: `false` / `true`
- Sicherheitsbewertung: `validated_lifecycle_ownership_defect_no_attacker_controlled_boundary_established`
- Connector / Protokoll / Profil: `apache` / `Apache configuration-pool lifecycle and graceful restart` / `resulting master 154ee724eba4653fa6378fc3c8729ae433e65697, tree-identical to final PR #183 head 4e4dfb36e1b05f7eda38450fd3710e3a04905118`

## Zusammenfassung

**Aktuelle Resulting-Master-Disposition — 2026-07-29T11:27:25Z.** PR #183
mergte als Parent-master `154ee724eba4653fa6378fc3c8729ae433e65697`; sein Tree
`c4d08e66d9b1929f4a56c81f3d5a021ea6ce4ef0` entspricht finalem Head
`4e4dfb36e1b05f7eda38450fd3710e3a04905118`. Alle 14 Master-SHA-GitHub-Actions-
Workflows waren erfolgreich. Ein detached Exact-Master-Worktree bestand
`make check-apache-ruleset-cleanup` (fünf Python-Contracts plus nativer GCC-
APR-Harness), daher ist die ursprüngliche APR-Fehler-/Control-Grenze
`verified`. Historische Kandidat-only-Formulierungen unten bleiben Chronologie
und werden durch diese Disposition ersetzt. Es ist nicht `closed`: Die breitere
Live-Apache-Konfigurations-/Readiness-/Phase-2-/`SIGUSR1`-Sequenz wurde nicht
auf Resulting Master erneut ausgeführt.

Parent-master erzeugt ein Per-Directory-`RulesSet`, ohne diese Allocation an die
Zerstörung des APR-Konfigurationspools zu binden. Der aufbewahrte
Baseline-APR-Harness bricht mit Exit `134` bei
`ci/checks/connectors/apache/apache_rules_set_cleanup.c:205` ab, weil er
keinen Cleanup beobachtet, obwohl `native_cleanup_calls == 1` erwartet wird.
Der noch nicht committete Task-Kandidat registriert einen Cleanup nur nach
erfolgreicher RulesSet-Erzeugung, und sein GCC-Harness besteht.

Der task-eigene private Apache-Build lädt zudem die Konfiguration, bedient den
HTTP/1.1-Readiness-Control, liefert die erwartete Phase-2-`403`-Sperre,
führt einen `SIGUSR1`-Graceful-Restart durch und beendet sich sauber. Der
Kandidat ist nicht committet, nicht reviewed, nicht hosted-validiert und nicht
gemergt; deshalb lautet der Status `in_progress`, nicht `fixed`, `verified`
oder `closed`.

## Beobachtetes und erwartetes Verhalten

Auf Parent-master `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` erzeugt
`msc_hook_create_config_directory` in `connectors/apache/src/msc_config.c`
bei Zeile `402` `cnf->rules_set` mit `msc_create_rules_set()`, registriert aber
keinen RulesSet-spezifischen `apr_pool_cleanup_register`-Callback. Der gegen
diesen Source kompilierte Baseline-APR-Harness endet bei Zeile `205` mit Exit
`134`, während `native_cleanup_calls == 1` erwartet wird.

Der Kandidat ergänzt `msc_rules_set_cleanup()` und registriert ihn unmittelbar
nach dem erfolgreichen Non-Null-RulesSet-Guard. Sein GCC-Harness besteht die
Pfade für Exactly-Once-Ownership, Null-RulesSet, Pool-Clear, Successful-Merge
und Merge-Failure.

Ein für eine Apache-Konfigurationsgeneration erzeugtes RulesSet muss genau
einmal freigegeben werden, wenn der APR-Konfigurationspool dieser Generation
zerstört wird, während konfigurierte Regeln während der normalen Lebenszeit
dieser Generation nutzbar bleiben.

## Impact und Grenzbewertung

Ohne die Pool-Bindung können ausgemusterte Konfigurationsgenerationen
RulesSets über Graceful-Restarts hinweg zurückhalten und zu
Prozessspeicherwachstum oder Verfügbarkeitsbeeinträchtigung beitragen. Der
Source-/Lifecycle-Defekt ist durch das Baseline-/Kandidaten-APR-Harness-Paar
und die privaten Apache-Lifecycle-Controls validiert.

Die relevante Quelle ist vertrauenswürdige Apache-Operator-Konfiguration und
Prozess-Lifecycle. Weder eine von Angreifern kontrollierte Quelle noch eine
unterstützte angreiferexponierte Grenze, extern ausnutzbare Memory-Safety-
Bedingung oder ein Release-Blocker wurden belegt. Es bleibt dennoch
sicherheitsrelevante Lifecycle-/Ownership-Arbeit und benötigt vor der
Integration eine fokussierte Ownership-Review.

## Betroffener Scope, Voraussetzungen und Reproduktion

- Datei: `connectors/apache/src/msc_config.c`.
- Symbole: `msc_hook_create_config_directory`, `msc_create_rules_set`,
  `msc_rules_cleanup` und `apr_pool_cleanup_register`.
- Voraussetzungen: Der Parent-Apache-Connector ist geladen; ein nicht
  nullwertiges RulesSet wird für eine Per-Directory-Konfiguration erzeugt;
  Apache leert oder zerstört später den Konfigurationspool, auch bei einem
  Graceful-Restart.
- Die Baseline mit dem aufbewahrten APR-Cleanup-Harness reproduzieren. Er endet
  mit Exit `134` bei `apache_rules_set_cleanup.c:205`, weil der Master-Source
  `native_cleanup_calls` bei null belässt.
- Kandidaten-Harness und privaten Apache-Control im selben aufbewahrten
  Task-Root ausführen. Die Kandidaten-Ownership-Controls bestehen; der
  Runtime-Control belegt Konfigurationsladen, HTTP/1.1-Readiness,
  Phase-2-Sperre, Graceful-Restart und sauberen Shutdown.

## Evidence

| Typ | Artefakt | SHA-256 | Exit | Ergebnis |
| --- | --- | --- | ---: | --- |
| Statischer Vergleich | `.codex/runs/merge-pr171-apache-pr91-94-comparison-20260729/evidence/fnd-parent-0064-static-triage.md` | `acd1923243fb4b46894959c5b9b08cf99f9d7478aa524e07fe008ecdf0357b59` | 0 | Parent-Allocation und Upstream-#94A-Cleanup-Richtung stimmen statisch überein. |
| Baseline-APR-Harness | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/baseline-apr/apache-rules-set-cleanup` | `030144bc518ad0ab9549858fbcc3cb8fdecb380b46d95822a4cea183f233c2df` | 134 | Fehlschlag bei `apache_rules_set_cleanup.c:205`: `native_cleanup_calls == 1`. |
| Kandidaten-GCC-APR-Harness | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/ruleset-gcc/apache-rules-set-cleanup` | `6b1dfd3ab32b36cf2efa74c08fde14237b87bcc6949a2efe8a5e2998d0ff7415` | 0 | Exactly-Once-, Null-, Pool-Clear-, Merge- und Failure-Path-Controls bestehen. |
| Privater Apache-HTTP/1.1-Control | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/apache-runtime/result.json` | `4b56897c87aa87b4b10d6a56bcc36b7fa60e91cd938a76cd1eb22d5ad7d83bf5` | 0 | Readiness ist HTTP `200`; konfigurierte Phase-2-Sperre ist HTTP `403`. |
| Restart-/Shutdown-Log | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/apache-runtime/error.log` | `d65d607196ecc06f09179a5db5cc11ffb5fa332185d0f4d5125a3f47923165b4` | 0 | `AH00493`-SIGUSR1-Restart, später `AH00489`-Normalbetrieb, PID-Entfernung und `AH00491`-sauberer-SIGTERM-Shutdown. |
| Memcheck-Diagnose | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/graceful-memcheck/memcheck.8.log` | `a49ca3a72f06aef4f4e67bab0b57056fe785c95a1dfba2361a892fbbf497b931` | 99 | Keine Invalid-free/read/write- oder UAF-Diagnose; Exit `99` stammt vom getrennten `strdup`-Leak in `FND-PARENT-0067`. |
| Resulting-Master-Verifikation | Parent-gelieferte PR-#183-Resulting-Master-Delivery- und fokussierte Cleanup-Zusammenfassung | n/a | 0 | Master `154ee724eba4653fa6378fc3c8729ae433e65697` ist tree-identisch zu finalem Head `4e4dfb36e1b05f7eda38450fd3710e3a04905118`; alle 14 Workflows und die fokussierte APR-Regression bestehen. Kein breiter Live-Apache-Rerun wird behauptet. |

Die Upstream-Quellen bleiben [PR #94](https://github.com/owasp-modsecurity/ModSecurity-apache/pull/94),
[Commit `5ea3fc9`](https://github.com/owasp-modsecurity/ModSecurity-apache/commit/5ea3fc9da876195706375cf35f321de2a1f35ce1)
und [Issue #82](https://github.com/owasp-modsecurity/ModSecurity-apache/issues/82).

## Root Cause und Remediation-Richtung

Der adaptereigene Parent-Source spiegelt weiterhin eine Baseline vor
Upstream-Commit `5ea3fc9da876195706375cf35f321de2a1f35ce1`. Er erzeugt ein
RulesSet, bindet den Cleanup aber nicht an den APR-Konfigurationspool. Der
aktuelle Kandidat ergänzt nur einen Callback, der `msc_rules_cleanup()` aufruft,
und seine Registrierung nach dem erfolgreichen Non-Null-Allocation-Guard.

Nur diese fokussierte Korrektur und ihr Regressions-Harness committen und
reviewen. Danach APR-Harness, fokussierte C-Checks, private Apache-
Konfigurations-/Request-/Restart-Controls, Security-Diff-Review und
Exact-Head-Hosted-Checks erneut ausführen. Die stale Parent-PRs #123 oder
#124 nicht vollständig mergen. Den getrennten `name_for_debug`-Leak nicht
ohne eine eigene lifecycle-sichere Ownership-Entscheidung in diese Korrektur
aufnehmen; er ist `FND-PARENT-0067`.

## Akzeptanzkriterien und Validierungsplan

1. Der Cleanup wird nur nach erfolgreichem nicht nullwertigem
   `msc_create_rules_set()` registriert und ruft `msc_rules_cleanup()` genau
   einmal pro ausgemusterter Konfigurationsgeneration auf.
2. Die fokussierte APR-Ownership-Regression besteht auf dem committen
   Kandidaten.
3. Privates Apache-Konfigurationsladen, HTTP/1.1-Readiness, Phase-2-Sperre,
   Graceful-Restart und sauberer Shutdown bestehen auf dem committen Kandidaten.
4. Die fokussierte Security-Review findet keinen Double-Free, vorzeitigen
   Cleanup, Stale-Pool oder Error-Path-Ownership-Regressionsfehler.
5. Frische Exact-Head-Hosted-CI-, Review- und SonarQube-Cloud-Evidence liegt
   vor jedem Status `fixed`, `verified` oder `closed` vor.

## Abhängigkeiten, verwandte Findings und Restrisiko

Aktuelles Restrisiko: Eine kontrollierte Resulting-Master-Apache/APXS-, APR-,
libmodsecurity- und Valgrind-Umgebung muss die breitere Live-Apache-
Konfigurations-/Readiness-/Phase-2-/`SIGUSR1`-Sequenz vor dem Status `closed`
erneut ausführen. Die historische Kandidat-only-Restrisikoformulierung unten
ist ersetzt.

- Abhängigkeiten: task-eigener Kandidaten-Worktree; lokale Apache/APXS-, APR-,
  libmodsecurity-, GCC- und Valgrind-Voraussetzungen; frische Hosted-
  Exact-Head-Evidence nach Commit/Publish.
- Verwandte Findings: `FND-PARENT-0055` und der unabhängige
  `FND-PARENT-0067`-`name_for_debug`-Leak.
- Parent-PR #123 und #124 sind stale conflicting Source-Inputs, keine
  Merge-Ziele. Upstream-Apache-PR #94 liefert die selektiv revalidierte
  Cleanup-Richtung.
- Restrisiko: Parent-master besitzt die Cleanup-Bindung weiterhin nicht. Der
  Kandidat ist nur lokal und ungemergt; es wird keine Fixed-/Verified-/Master-
  Behauptung aufgestellt.

## Historie

- `2026-07-29T07:53:18Z`: Statischer Upstream-/Parent-Vergleich triagiert.
- `2026-07-29T09:04:55Z`: Baseline-APR-Fehlschlag, Kandidaten-GCC-Erfolg und
  private Apache-Lifecycle-Evidence erfasst; der unabhängige `strdup`-Leak
  erhielt `FND-PARENT-0067`.
- `2026-07-29T11:27:25Z`: Resulting Master
  `154ee724eba4653fa6378fc3c8729ae433e65697` wurde als tree-identisch zu
  finalem Head `4e4dfb36e1b05f7eda38450fd3710e3a04905118` bestätigt; alle 14
  Workflows und die fokussierte APR-Regression bestanden. Das Finding ist
  `verified`, nicht `closed`.
