# Change Record: Framework-zentrale Synchronisation des Version-Updaters

**Sprache:** [English](CR-20260815-framework-version-pin-updater-sync.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260815-framework-version-pin-updater-sync |
| Datum (UTC) | 2026-08-15 |
| Basis-Revision | `29a2a8bcab57e936c5274f8fe64a15c6fee879bd` |
| Delivery-Status | Draft-[PR #291](https://github.com/Easton97-Jens/ModSecurity-conector/pull/291) zielt auf `master`. Sein initialer Head `f804ed598d2515fc972b8f8308678d95a5584fb7` zeigte ShellCheck `SC2006`, behoben in `52c25c08ac309ecbe7edb72baeeabb0841ddba30`. Dieser Head zeigte danach einen Hosted-Defekt der verschachtelten-Submodule-Fixture-Identität und 18 task-eigene SonarQube-Cloud-New-Issues. Das Follow-up enthält quellnative Root-, Symlink-, Argument-, Komplexitäts- und Contract-Bereinigungen. Sein erster Hosted-`actionlint`-Recheck zeigte, dass die Updater-Testfixture temporäre Dateien unter `/tmp` statt unter GitHubs `RUNNER_TEMP` anlegte; das finale Fixture-Update folgt nun diesem Runner-Root. Ein weiteres reines Updater-Follow-up ersetzt einen mehrdeutig backtrackenden Assignment-Matcher durch begrenztes lineares Parsing, deklariert den Value-Rendering-Callback-Contract und kanonisiert den validierten Pfad direkt an der Lesegrenze bei beibehaltenen No-Follow-Prüfungen. Frische Hosted-Validierung ist erforderlich. Eine `master`-Integration wird durch diesen Record nicht autorisiert. |

## Motivation und Problemstellung

Das Framework `ci/lib/common.sh` ist die zentrale Versionsautorität. Das
Parent-Repository enthielt semantisch entsprechende Komponenten-Pins und
Contracts, die beim Update des Framework-Submoduls auseinanderlaufen konnten.
Der geschützte Framework-Update-Workflow muss daher die freigegebenen
Framework-Versionstupel atomar ins Parent übernehmen und bei ungültiger Quelle
oder ungültigem Ziel fehlgeschlossen abbrechen.

## Akzeptanzkriterien

- Framework-Deklarationen für Envoy, lighttpd, HAProxy, NGINX/QUIC und CRS sind
  jedem entsprechenden Parent-eigenen Pin oder Contract zugeordnet.
- Ein Framework-Update extrahiert das exakte `common.sh`-Objekt des Kandidaten
  als Daten, synchronisiert die registrierten Parent-Ziele, prüft sie erneut
  und staged nur die explizite Allowlist sowie erzeugte Compiler-Guides.
- Der Updater sourced oder evaluiert keine Framework-Shell-Eingabe und weist
  fehlende, doppelte, fehlerhafte, unbekannte, symbolische oder spezielle
  Dateien zurück, ohne unbeabsichtigten Teil-Write.
- Aktuelle Framework-Werte sind ein stabiler No-op; gültige geänderte Werte
  aktualisieren alle registrierten Ziele; fokussierte Regressionstests decken
  Rollback- und Fehlerfälle ab.
- Framework-Quelle, MRTS und der Parent-Framework-Gitlink bleiben unverändert.

## Implementierungsentscheidung und Begründung

`ci/tools/sync-framework-component-versions.py` implementiert einen begrenzten
Literal-Parser und eine explizite Zielregistry. Er validiert die vollständigen
Framework-Versionstupel, erhält Zielmodi, verwendet Containment- und
Dateitypprüfungen und rollt bereits abgeschlossene Ersetzungen zurück, wenn
eine spätere Ersetzung fehlschlägt. Der Publisher in
`.github/workflows/update-submodules.yml` initialisiert nur das vertrauenswürdige
Framework der obersten Ebene, liest das exakte Git-Objekt
`ci/lib/common.sh` des Kandidaten, führt `--validate`, `--sync` und `--check`
aus, erzeugt Compiler-Guides neu und weist Pfade außerhalb seiner expliziten
Allowlist zurück.

Die registrierten Zuordnungen umfassen Envoy `1.39.0`, lighttpd `1.4.85` samt
Quellmetadaten, HAProxy `3.2.22` samt HTX-Contract, den NGINX-Release-Tupel
`release-1.31.3`, NGINX-QUIC-TLS `4.0.1` samt Digests und CRS `v4.28.0` mit
Commit `55b09f5acfd16413e7b31041100711ceb7adc89c`, wie sie in der beibehaltenen Framework-Eingabe enthalten
sind. Lighttpd- und HAProxy-Build-/Lifecycle-Verbraucher leiten Werte jetzt aus
ihren Contracts ab. Compiler-Guides lesen begrenzte Parent-Contracts statt
Framework-Shell auszuführen.

## Security-Auswirkung

Diese Änderung schützt eine Grenze für Dependency-Updates und
Codeausführung. Der Updater behandelt Framework-Shell als nicht auszuführende
Daten, führt sie nicht aus, begrenzt Writes auf registrierte Parent-Dateien,
validiert URLs, Referenzen, Digests und Tupelkonsistenz, weist symbolische und
spezielle Dateien zurück und bietet atomisches Rollback. Der Workflow
initialisiert keine vom Kandidaten kontrollierten verschachtelten Submodule
mehr rekursiv. Es wurden keine Berechtigungen, Scanner, Tests oder
Quality-Gates abgeschwächt.

Das Follow-up begrenzt zusätzlich extrahierte Framework-Daten auf den
Runner-kontrollierten temporären Root, validiert jeden Git-Subprozess-Root und
Argumentvektor und begrenzt den HAProxy-Contract-Reader mit No-Follow-Regular-
File-Zugriff auf seinen festen Overlay-Root. Die Nested-Submodule-
Regression-Fixture konfiguriert ihre lokale Commit-Identität explizit für
Hosted Runner. Die Updater-Regression-Fixture erzeugt ihr temporäres
Repository außerdem unterhalb von `RUNNER_TEMP`, wenn dieser GitHub-Runner-Root
bereitgestellt wird, sodass ihre Testdaten demselben Root-Contract wie der
Produktionsaufruf folgen.
Der Reader kanonisiert sowohl den geprüften Kandidaten als auch seinen
freigegebenen Root an der Dateisystemgrenze, weist jede Symlink-Auflösung ab und
behält anschließend Komponenten-Walk, No-Follow-Descriptor-Öffnung,
Regular-File-Prüfung und Größenbegrenzung bei.

## Geänderte Dateien

Der task-eigene Parent-Diff ist nachfolgend gruppiert; die englische und die
deutsche Fassung beschreiben dieselbe Abdeckung.

- Update- und CI-Orchestrierung: `.github/workflows/ci-security-workflow-lint.yml`,
  `.github/workflows/nginx-root-broker.yml`,
  `.github/workflows/update-submodules.yml`, `Makefile`.
- Synchronizer und Validierung: `ci/tools/sync-framework-component-versions.py`,
  `ci/checks/connectors/all/check-remaining-connectors-common-adoption.py`,
  `ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py`,
  `ci/checks/evidence/check-runtime-producer-readiness.py`,
  `ci/provisioning/components/prepare-runtime-components.py`,
  `ci/runtime/broker/nginx_root_broker.py`,
  `ci/runtime/broker/protected_nginx_broker_caller.py`,
  `ci/runtime/lifecycle/resolve-full-lifecycle-profile.py`,
  `ci/tools/validate-submodule-candidate-state.py`.
- Connector-Contracts und Verbraucher: `connectors/envoy/ext_proc/README.md`,
  `connectors/envoy/ext_proc/README.de.md`, die geänderten HAProxy-Dateien
  unter `connectors/haproxy/` einschließlich
  `htx-overlay/haproxy-makefile.patch`, `htx-overlay/version-contract.json`
  und `htx-overlay/version_contract.py`, die geänderten lighttpd-Dateien
  unter `connectors/lighttpd/` einschließlich `build/read_version.sh`,
  `lighttpd-version.contract` und
  `patches/0001-lighttpd-msconnector-stream-hooks.patch` sowie die geänderten
  NGINX-README-Dateien unter `connectors/nginx/`.
- Dokumentation und erzeugte Evidenz: geänderte Dateien unter
  `docs/build/compilers/`, `docs/reference/variables.*`,
  `docs/security/trusted-nginx-root-broker.*`, geänderte lighttpd-Beispiel-
  READMEs und `examples/lighttpd/safe/lighttpd-http1-identity.conf`,
  `scripts/generate_compiler_guides.py` sowie die drei erzeugten Dateien unter
  `reports/testing/generated/canonical/connector-capabilities.generated.*`.
- Regression: `tests/test_ci_security_workflows.py`,
  `tests/test_full_lifecycle_profiles.py`,
  `tests/test_haproxy_modsecurity_resolver.py`,
  `tests/test_validate_submodule_candidate_state.py` und
  `tests/test_update_framework_versions.py`.

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| `python3 ci/tools/sync-framework-component-versions.py --validate --repo-root . --framework-common <beibehaltenes Framework-common.sh-Blob>` | bestanden; gab `{"changed": [], "mode": "validate"}` zurück |
| `python3 ci/tools/sync-framework-component-versions.py --check --repo-root . --framework-common <beibehaltenes Framework-common.sh-Blob>` | bestanden; gab `{"changed": [], "mode": "check"}` zurück |
| Fokussierte Unittest-Suite für Updater/Workflow/Compiler/Lifecycle/HAProxy/Submodul | bestanden; 87 Tests |
| Lighttpd-Patched-Host-Contract-Tests | bestanden; 26 Tests |
| NGINX-Root-/Protected-Broker-Tests | bestanden; 64 Tests |
| Workflow-/Submodul-/Updater-Unittest-Suite nach `actionlint`-Remediation | bestanden; 52 Tests |
| Aktuelles Sonar-/actionlint-Remediation-Aggregat | bestanden; 140 Tests mit 4 erwarteten Capability-Skips unter einer task-eigenen schreibbaren `RUNNER_TEMP`-Simulation |
| Connector-, Shell-Syntax-, Variablen-Dokumentations-, No-CRS-Dokumentations- und Evidence-Output-Security-Prüfungen | bestanden |
| `python3 -m py_compile` für geänderte relevante Python-Dateien | bestanden |
| `git diff --check 29a2a8bcab57e936c5274f8fe64a15c6fee879bd` | bestanden |
| Finalisierter Security-Diff-Scan | bestanden; 0 meldungswürdige Findings |

Die exakte Framework-Eingabe war das beibehaltene
`ci/lib/common.sh`-Objekt für den Gitlink
`1260aaae411ecf88cf50dc480b80e2e20ac47901`. Der Security-Scan-Report ist am
task-eigenen externen Evidenzpfad unter
`/var/tmp/codex/ModSecurity-conector/tasks/framework-version-pin-updater-sync-20260815/security-diff-scan/report.md`
aufbewahrt.

## Runtime-Evidence

Die Evidenz besteht aus lokaler statischer Validierung, Contract-Tests,
Parser-Tests und Upstream-Patch-Kompatibilitätsprüfungen. Keine vollständige
Runtime-Matrix, Produktions-Runtime oder GitHub-Hosted-Runner-Ausführung wurde
durchgeführt oder behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

- Frische GitHub Actions, SonarQube Cloud und Hosted-Review-Checks wurden für
  den ausstehenden Sonar-/actionlint-Remediation-Head noch nicht beobachtet.
- `actionlint` wurde nicht ausgeführt, weil es in der Umgebung nicht
  installiert ist.
- Eine vollständige Framework-abhängige Integration-/Runtime-Validierung wurde
  nicht ausgeführt, weil der exakte Framework-Submodule-Checkout im
  Task-Worktree absichtlich fehlt.
- `make check-bilingual-docs` konnte wegen desselben fehlenden Submoduls die
  bestehenden lokalen Framework-Link-Prüfungen nicht vollständig ausführen;
  ein Paritätsfehler in den geänderten Dokumenten blieb nicht bestehen.

## Bekannte Einschränkungen

Der exakte Framework-Submodule-Checkout war im Task-Worktree nicht verfügbar;
deshalb konnten die vollständige Framework-Integration und der
Framework-Archiv-zu-Quelle-Extraktionspfad nicht erneut ausgeführt werden. Die
unabhängige Security-Prüfung erfasste dies als partielle Abdeckung einer
bereits bestehenden Integrations-Evidenzlücke, nicht als neues meldungswürdiges
Finding. Die lokalen Prüfungen können kein Hosted-Runner-Image, keine
Netzwerkbedingung, keinen Cache-Zustand und kein aktuelles Remote-PR-Ergebnis
beweisen.

## Verbleibende Risiken

Der Updater bricht bewusst fehlgeschlossen ab, wenn Framework-Deklarationen oder
zugeordnete Parent-Ziele den begrenzten Contract nicht erfüllen. Das
verbleibende Risiko ist der unbeobachtete Framework-seitige Nachweis der
Archivextraktion sowie die noch erforderliche Beobachtung des exakt
gepushten PR-Heads in GitHub, bevor die Auslieferung als verifiziert gelten
kann.

## Finaler Diff- und Review-Status

Die lokale finale Diff-Prüfung fand nur task-eigene Parent-Änderungen; die
Framework-Quelle, MRTS und der Parent-Gitlink blieben unverändert. Die
erforderliche lokale Validierung und der Security-Diff-Review bestanden wie
oben aufgeführt. PR #291 ist bereits offen und Draft; dieser Record behauptet
keine bestandenen Hosted-Checks, kein SonarQube-Ergebnis, keinen
Ready-for-Review-Status und keinen Merge vor direkter Beobachtung.
