# Finding FND-SONAR-0030: Provisioning-Remediation für achtunddreißig SonarQube-Cloud-Befunde und zwei Duplikatblöcke

**Sprache:** [English](finding.md) | Deutsch

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `maintainability` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Severity / Confidence | `P2` / `not_applicable` / `confirmed` |
| Status / Feasibility | `fixed` / `requires_user_decision` |
| Release-Blocker / Candidate-Integration-Blocker / sicherheitsrelevant | nein / nein / ja |
| Finale Disposition | `exact_draft_pr_226_head_b08bc69278570a02af5c0367bffb2dea47d37d7c_verified_fixed_pending_explicit_master_authorization_and_resulting_master_reproduction` |
| Anfängliches Sonar-Inventar | 21 `python:S3776`, 10 `python:S1192`, 3 `pythonsecurity:S6549`, 2 `python:S3358`, 1 `python:S1066` und 1 `python:S8786`; zwei Duplikatblöcke umfassen zusammen 25 Zeilen. |

## Zusammenfassung und Scope

Das aufbewahrte anfängliche Current-Master-Inventar bindet den
`ci/provisioning/`-Scope an Parent-Revision
`6b4aca18d390363764b96d85cd31969b9bb114a1`. Es identifizierte 38
SonarQube-Cloud-Zeilen in
`ci/provisioning/components/prepare-runtime-components.py` und zwei
provisioning-seitige Duplikatblöcke zwischen `markdown_report()` und
`ci/evidence/reports/update-runtime-reports.py`.

GitHub mergte den exakten PR-#220-Head
`5378ed0c29f91df7e508f13b9d860c548f882468` normal als Resulting Master
`caabf33c11d6002f9a1661f215ed195d6e141253`. Alle vierzehn Resulting-Master-
Workflows bestanden, und die Resulting-Master-Sonar-Analyse ist an diese SHA
gebunden. Sie meldet null Duplikatzeilen und `0,0 %` Duplikation, aber vier
offene Source-Zeilen in der ursprünglichen Komponente bleiben; jede wurde vor
dem aufbewahrten Inventar erzeugt. Das saubere PR-/New-Code-Ergebnis beweist
daher nicht, dass alle 38 Old-Master-Zeilen behoben wurden. Keine Scanner-Rule,
kein Quality Gate, keine Exclusion, Suppression, kein `NOSONAR`, Workflow,
Framework-/MRTS-Source, Gitlink oder Bypass wurde geändert.

Exakter Draft-PR-#224-Head
`0da588ecd068f35e27ae404139906e2bebc89e14` implementierte Source-Refactors
für die vier erhaltenen historischen Ursachen: die drei Cognitive-Complexity-Zeilen in
`prepare_nginx_runtime()`, `prepare_apache_httpd()` und `BuildLock.__enter__()`
sowie die Nested-Condition-Zeile in `remove_incomplete_connector_cache_entry()`.
Sein fokussiertes 94-Test-Aggregat, die lokalen Controls, alle anwendbaren
GitHub-Checks und das SonarQube-Cloud-Quality-Gate bestehen. Sonar meldet null
offene PR-Issues, `new_violations=0`, null Security-Hotspots und `0,0 %`
New-Code-Duplikation. Dieses Exact-Head-Ergebnis rechtfertigte nur eine
vorläufige `fixed`-Disposition bis zur nachstehenden Resulting-Master-
Reproduktion.

## Resulting-Master-Ergebnis

GitHub mergte exakten PR-#224-Head
`0da588ecd068f35e27ae404139906e2bebc89e14` normal als Resulting Master
`7016a66f3702523098811b45139133c77dee88fb`. Alle 14 Workflows für diese
exakte Master-SHA bestanden, und die SonarQube-Cloud-Master-Analyse ist daran
gebunden. Der Nested-Condition-Key `AZ9cRyj3HhV2CayPTPys` und der BuildLock-
Key `AZ9cRyj3HhV2CayPTPy2` sind `CLOSED/FIXED`. Die zwei Cognitive-Complexity-
Keys `AZ9cRyj3HhV2CayPTPzB` (`prepare_apache_httpd()`) und
`AZ9cRyj3HhV2CayPTPzC` (`prepare_nginx_runtime()`) bleiben `OPEN`.

Das Master-Projekt-Quality-Gate ist `ERROR`; dieser Eintrag schreibt keine
unabhängigen bestehenden Projekt-Befunde PR #224 zu. Die Original-Issue-
Reproduktion öffnete die zwei verbleibenden Source-Ursachen; eine direkte
Master-Korrektur ist nicht zulässig.

## Ergebnis des aktuellen PR #226

Der exakte Draft-PR-#226-Head
`b08bc69278570a02af5c0367bffb2dea47d37d7c` zentralisiert die unveränderte
Apache-/NGINX-Keyed-Plan-Staging-Entscheidung in
`prepare_connector_with_optional_staging()` und bewahrt die öffentlichen
Einstiegspunkte als dünne Wrapper über ihren privaten Per-Plan-Kontrollfluss.
Seine 34 fokussierten Cache-Contract-Tests und Python-Kompilierung bestehen;
der fokussierte Security-Control-Review fand keinen plausiblen diff-induzierten
reportierbaren Befund.

Der exakte lokale, Remote- und GitHub-Head ist identisch. Der PR ist `OPEN`,
Draft und `CLEAN`, ohne eingereichten Review oder Review-Entscheidung. Alle 33
abgeschlossenen GitHub-Checks bestanden und sechs kontextgerechte Checks wurden
übersprungen. SonarQube Cloud meldet Quality Gate `OK`, null OPEN/CONFIRMED
PR-Issues, `new_violations=0`, `new_security_hotspots=0`,
`new_duplicated_lines_density=0.0` und `new_duplicated_lines=0`. Das Finding
ist daher `fixed`, nicht `verified` oder `closed`: ein explizit autorisierter
Merge und Resulting-Master-Reproduktion bleiben erforderlich.

## Beobachtetes und erwartetes Verhalten

Das anfängliche Inventar konzentrierte kognitive Komplexität, wiederholte
Literale, verschachtelten bedingten Ablauf, eine Regex-Performance-Beobachtung,
Path-Construction-Scanner-Leads und zwei Report-Rendering-Duplikatblöcke. Der
eingegrenzte Code enthält Cache-, Download-, Path-, Provenance- und
Subprocess-nahe Abläufe.

Provisioning bewahrt validierte Managed-Root-Containment, Provenance-Prüfungen,
atomare Veröffentlichung und Argument-Vector-Ausführung, während begrenzte
Helper, zentralisierte reine Datenliterale, geklärter bedingter Ablauf und eine
unterschiedene Report-Repräsentation die Maintainability-Ursachen ohne
Änderung des Report-Vertrags beheben.

## Auswirkung und Security-Bewertung

Eine unvorsichtige Maintainability-Remediation könnte eine Containment- oder
Provenance-Invariante schwächen. Der aufbewahrte Baseline-Review enthält null
reportierbare Security-Befunde, aber seine Runtime-Snapshot-Wrapper-Caller-
Reachability-Abdeckung bleibt ausdrücklich zurückgestellt. Der versiegelte
Exact-Head-Post-Change-Review für
`904a8fca64b35cd287348722b4bdc2260b4f64b3...cb500e3a84efe94565b7a6665dea4b94ec719501`
besitzt vollständige Abdeckung und null reportierbare Befunde.

Der exakte PR-#226-Head bestand außerdem fokussierte lokale Controls und alle
anwendbaren GitHub-Actions-Checks. Die verbleibenden historischen
Source-Ursachen wurden remediert, ohne die Cache-, Provenance-, Path- oder
Subprocess-Controls zu schwächen. Das Finding ist `fixed`, nicht `verified`
oder `closed`, bis Integration und Resulting-Master-Reproduktion beobachtet
sind.

## Betroffene Dateien und Symbole

Dateien:

- `ci/provisioning/components/prepare-runtime-components.py`
- `ci/evidence/reports/update-runtime-reports.py`
- `tests/test_prepare_runtime_components.py`
- `tests/test_runtime_component_cache_contract.py`

Symbole:

- `validated_cache_manifest_for_entry`, `prepare_git_component`,
  `prepare_archive`, `resolve_nginx_archive`, `hash_input_paths`,
  `prepare_expat_managed_overrides`, `prepare_expat`,
  `modsecurity_build_inputs`, `prepare_shared_modsecurity`, `connector_plan`,
  `prepare_go_tool`, `rebase_apache_install_text_paths_for_publish`,
  `connector_cache_entry_complete`,
  `reuse_connector_cache_entry_if_only_commit_changed`,
  `prepare_connector_transactionally`, `prepare_apache_httpd`,
  `prepare_nginx_runtime`, `prepare_haproxy_runtime`,
  `remove_incomplete_connector_cache_entry`, `BuildLock.__enter__`,
  `known_tool_source`, `markdown_report`, `main` und
  `map_expat_build_failure`.

## Voraussetzungen und Reproduktion

Voraussetzungen:

- Das anfängliche Inventar bleibt an Parent-Revision
  `6b4aca18d390363764b96d85cd31969b9bb114a1` gebunden.
- Der Task bleibt auf Parent-Provisioning-Remediation, direkt notwendige
  Parent-Tests, versionierte Change Records und lokale Control-Plane-Evidence
  begrenzt.
- Keine SonarQube-Cloud-Rule, kein Quality Gate, keine Exclusion, Suppression,
  kein `NOSONAR`, Workflow, Framework-/MRTS-Source, Gitlink oder direkter
  master-Change wird verwendet.

Die Exact-PR-Head-New-Code-Analyse war ohne Änderung von Analyse-Controls
sauber. GitHub mergte danach den exakten Head
`5378ed0c29f91df7e508f13b9d860c548f882468` normal als Resulting Master
`caabf33c11d6002f9a1661f215ed195d6e141253`; alle vierzehn Resulting-Master-
Workflows bestanden. Die Master-Sonar-Analyse ist an diese SHA gebunden und
hat null Duplikatzeilen sowie `0,0 %` Duplikation. Sie bewahrt außerdem vier
OPEN-Zeilen: `AZ9cRyj3HhV2CayPTPzC` (`python:S3776`,
`prepare_nginx_runtime()`), `AZ9cRyj3HhV2CayPTPzB` (`python:S3776`,
`prepare_apache_httpd()`), `AZ9cRyj3HhV2CayPTPys` (`python:S1066`,
`remove_incomplete_connector_cache_entry()`) und
`AZ9cRyj3HhV2CayPTPy2` (`python:S3776`, `BuildLock.__enter__()`). Ihre
Erzeugungsdaten liegen vor dem aufbewahrten Inventar. PR #224 schloss die
beiden letzteren Keys, aber die Apache- und NGINX-Cognitive-Complexity-Keys
bleiben auf Resulting Master offen; diese zwei Source-Ursachen beheben und die
ursprüngliche Reproduktion erneut ausführen, bevor `fixed` oder `verified`
gesetzt wird.

## Aufbewahrte Evidence

- Historischer Pfad des anfänglichen Current-Master-Sonar-Inventars und
  Task-Plans `.codex/plans/ci-provisioning-sonar-remediation-20260801.md`
  (nicht in diesem Reconciliation-Checkout verteilt)
  — SHA-256 `4cab13eaecb863922524318c350a85baeb57f72db6a32cd86cbcae3bd9005274`;
  read-only Inventar; Exit `0`; beobachtet `2026-08-01T11:08:22Z`.
- Versiegelter eingegrenzter Baseline-Security-Review (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-sonar-remediation-20260801/security-scan-6b4aca18-20260801/report.md`)
  — SHA-256 `d4eb095bd927350ea1a1a9c349750abd3bba0e1960721cd83fa6446e0aaa8503`;
  partielle Baseline-Abdeckung, null reportierbare Befunde und eine
  zurückgestellte Caller-Reachability-Frage; Exit `0`; beobachtet
  `2026-08-01T10:25:41Z`.
- Versiegelter Exact-Head-Security-Review (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-sonar-remediation-20260801/security-diff-904a8fca-cb500e3a-20260801/report.md`)
  — SHA-256 `6b9ce34f771a3b7f8799b0ba9addcbc5e649005efeb932955cd7734a4f64bd6a`;
  vollständige Abdeckung und null reportierbare Befunde; Exit `0`; beobachtet
  `2026-08-01T13:10:39Z`.
- Exact-Head-Hosted-Verification-Receipt (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-sonar-remediation-20260801/hosted-verification-pr-220-cb500e3a.md`)
  — SHA-256 `d129af2ad25db78f85623c8b1d14149ad03192257a7fa70c7d4be4b223bd1d8f`;
  exakte PR-#220-Head-, GitHub-Actions- und SonarQube-Cloud-Evidence; Exit
  `0`; beobachtet `2026-08-01T13:20:09Z`.
- Resulting-Master-Integration und Sonar-Reproduktions-Receipt (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-sonar-remediation-20260801/master-integration-verification-caabf33c-20260801.md`)
  — SHA-256 `351639d5a70189bf776063414c8ea8b23060dc863b6177cea2638415f450a55d`;
  normaler Merge, Tree-Identität, vierzehn erfolgreiche Master-Workflows und
  die exakte Resulting-Master-Sonar-Reproduktion; Exit `0`; beobachtet
  `2026-08-01T14:13:10Z`.
- PR-#224-Exact-Head-Hosted-Verification-Receipt (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-four-sonar-followup-20260801/hosted-verification-pr-224.md`)
  — SHA-256 `975675e0ae13027d05f7a219c884b24428ff03eb0f82f43d64b4f97073f69647`;
  Draft-PR-#224-Exact-Head-, GitHub-Check-, Review- und SonarQube-Cloud-
  Evidence; Exit `0`; beobachtet `2026-08-01T15:46:12Z`.
- PR-#224-Resulting-Master-Verification-Receipt (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-four-sonar-followup-20260801/master-integration-verification-7016a66f.md`)
  — SHA-256 `44324bf23b19bebd8523056dbd6834d77eea9e2113ddc96e96cdf525328688bd`;
  normaler Merge, Exact-Master-Workflows und Original-Issue-SonarQube-Cloud-
  Reproduktion; Exit `0`; beobachtet `2026-08-01T16:03:41Z`.

## Root Cause und Remediation

Provisioning-Cache-, Acquisition-, Component-, Reporting- und CLI-
Verantwortlichkeiten sammelten sich in einem primären Modul. Dies erzeugte
hochkomplexen Kontrollfluss, wiederholte Literale, lokale verschachtelte
Branches und eine duplizierte Report-Rendering-Repräsentation.

Die abgeschlossene Remediation einschließlich PR #224 bewahrt Cache-, Path-,
Provenance- und Subprocess-Sicherheitsverträge, während begrenzte Helper
extrahiert, reine Datenliterale zentralisiert, ausgewählter Ablauf vereinfacht,
`pythonsecurity:S6549`-Controls bewahrt und die provisioning-seitige
Markdown-Repräsentation unterschieden wurden. PR #224 reduziert die kognitive
Komplexität von `prepare_nginx_runtime()`, `prepare_apache_httpd()` und
`BuildLock.__enter__()` und vereinfacht die verschachtelte Bedingung in
`remove_incomplete_connector_cache_entry()`, ohne Scanner-Controls zu ändern
oder Code nur zur Metrikveränderung zu verschieben.

## Akzeptanzkriterien und Validierungsplan

Abgeschlossene Teilremediations-Evidence:

- Die 91 fokussierten Parent-Provisioner-/Cache-/Environment-/Artifact-/Path-
  Policy-Tests bestanden zusammen mit Python-Kompilierung,
  `make check-runtime-path-policy`, bilingualer Dokumentation,
  Documentation-Links und `git diff --check`.
- Managed-Expat-Mark-Child-Akzeptanz und External-Path-, Canonical-Traversal-
  und Symlink-Escape-Rejection-Controls bestanden vor Cache-Filesystem- oder
  Build-Sinks. Der Silent-Nonzero-Git-Submodule-Failure- und der begrenzte
  NGINX-Profile-Propagation-Control bestanden ebenfalls.
- Der versiegelte Exact-Head-Security-Review besitzt vollständige Abdeckung
  und null reportierbare Befunde.
- Auf dem exakten PR-Head bestanden alle genannten erforderlichen GitHub-
  Actions-Checks, und SonarQube Cloud meldete Quality Gate `OK`, null offene
  PR-Issues, `new_violations=0`, `new_security_hotspots=0`,
  `new_duplicated_lines_density=0.0` und `duplicated_lines_density=0.0`.
- GitHub mergte exakten Head `5378ed0c29f91df7e508f13b9d860c548f882468`
  normal als `caabf33c11d6002f9a1661f215ed195d6e141253`; alle vierzehn
  Exact-Master-Workflows bestanden, und die Resulting-Master-Sonar-Analyse hat
  null Duplikatzeilen sowie `0,0 %` Duplikation.

Abgeschlossene Follow-up-Bedingung: PR #224 remediert die Nested-Condition-
und BuildLock-Ursachen. Das fokussierte 94-Test-Aggregat, Python-Kompilierung,
`make check-runtime-path-policy`, bilinguale Dokumentation, Documentation-Links
und `git diff --check` bestehen; die Exact-Head-GitHub-Checks bestehen, und
SonarQube Cloud meldet Quality Gate `OK`, null PR-Issues und `0,0 %`
New-Code-Duplikation.

Resulting-Master-Verifikation abgeschlossen: Alle 14 Workflows bestehen, aber
die Original-Keys `AZ9cRyj3HhV2CayPTPzB` und `AZ9cRyj3HhV2CayPTPzC` bleiben
offen. Der exakte Draft-PR #226 zentralisiert nun ihre unveränderte Keyed-Plan-
Staging-Entscheidung in `prepare_connector_with_optional_staging()` und bewahrt
den Apache-/NGINX-Per-Plan-Kontrollfluss. Python-Kompilierung und 34
fokussierte Cache-Contract-Tests bestehen; der fokussierte Source-/Control-
Review fand keinen plausiblen diff-induzierten reportierbaren Security-Befund.
Sein Exact Head ist verifiziert; nur Resulting-Master-Reproduktion bleibt vor
`verified` oder `closed` erforderlich.

## Abhängigkeiten, Blocker und verwandte Findings

- Abhängigkeit: eine explizite aktuelle Nutzerautorisierung für die `master`-
  Integration, gefolgt von Resulting-Master-Reproduktion der zwei Original-Keys.
- Blocker: Source-Arbeit ist abgeschlossen; Delivery benötigt die Nutzerentscheidung.
- Duplikate: keine.
- Verwandte Findings: `FND-SONAR-0016`, `FND-SONAR-0029`.
- Source-Runs: `ci-provisioning-sonar-remediation-20260801`,
  `ci-provisioning-four-sonar-followup-20260801` und
  `ci-provisioning-two-cognitive-sonar-remediation-20260801`.

## Restrisiko

Der Baseline-Review bewahrt eine zurückgestellte Runtime-Snapshot-Wrapper-
Caller-Reachability-Frage, obwohl der fokussierte PR-#226-Review keinen
reportierbaren diff-induzierten Security-Befund fand. Zwei Maintainability-
Ursachen vor dem Inventar sind `CLOSED/FIXED`; die letzten zwei sind im exakten
Draft-PR #226 fixed, bleiben aber auf aktuellem Master offen. Das Finding ist
`fixed`, nicht `verified` oder `closed`.

## Historie

- `2026-08-01T11:08:22Z`: nach dem revisionsgebundenen anfänglichen Inventar
  allokiert, das 38 aktuelle `ci/provisioning`-Zeilen und zwei
  provisioning-seitige Duplikatblöcke identifizierte. Kein Code-Abschluss,
  Commit, PR, Merge, Scanner-Control-, Framework-/MRTS-, Gitlink- oder master-
  Change wurde behauptet.
- `2026-08-01T11:36:00Z`: ein versiegelter Working-Tree-Post-Change-Review
  endete mit vollständiger Abdeckung und null reportierbaren Befunden. Dies war
  nur lokale Evidence und beanspruchte keinen Commit, PR, Merge, Hosted-
  Analyse oder Abschluss.
- `2026-08-01T13:20:09Z`: Exact-Draft-PR-#220-Head-Verifikation abgeschlossen.
  Basis ist `904a8fca64b35cd287348722b4bdc2260b4f64b3`; übereinstimmender
  lokaler, Remote- und GitHub-Head ist
  `cb500e3a84efe94565b7a6665dea4b94ec719501`. Der finale Security-Review
  besitzt vollständige Abdeckung und null reportierbare Befunde, 91 fokussierte
  lokale Tests und Controls bestehen, erforderliche Exact-Head-GitHub-Actions
  sind erfolgreich mit `quick-framework-check` erwartbar `skipped`, und
  SonarQube Cloud meldet Quality Gate `OK` mit null offenen PR-Issues und
  `0.0` Duplizierung. Kein Master-Merge wurde autorisiert oder versucht, daher
  ist der Lifecycle-Übergang `fixed`, nicht `verified` oder `closed`.
- `2026-08-01T14:13:10Z`: GitHub mergte exakten PR-#220-Head
  `5378ed0c29f91df7e508f13b9d860c548f882468` normal als Resulting Master
  `caabf33c11d6002f9a1661f215ed195d6e141253`. Alle vierzehn Resulting-Master-
  Workflows bestanden, und die Master-Sonar-Analyse ist an diese SHA gebunden
  mit null Duplikatzeilen und `0,0 %` Duplikation. Die ursprüngliche
  Reproduktion bewahrt außerdem vier OPEN-Zeilen vor dem Inventar:
  `AZ9cRyj3HhV2CayPTPzC`, `AZ9cRyj3HhV2CayPTPzB`,
  `AZ9cRyj3HhV2CayPTPys` und `AZ9cRyj3HhV2CayPTPy2`. Die frühere saubere
  PR-/New-Code-Evidence belegt daher keine vollständige historische
  Remediation; der kanonische Status wird zu `in_progress` korrigiert. Keine
  Scanner-Control, Framework-/MRTS-Source, Gitlink, kein Bypass oder direkter
  Master-Write wurde verwendet.
- `2026-08-01T15:46:12Z`: exakter Draft-PR-#224-Head
  `0da588ecd068f35e27ae404139906e2bebc89e14` wurde gegen Basis
  `62f7e13f35edd3f73661f724fd5208dcf1584d18` verifiziert. Er remediert die
  vier erhaltenen historischen Source-Ursachen. Das fokussierte 94-Test-
  Aggregat und die lokalen Checks bestanden; alle anwendbaren Exact-Head-
  GitHub-Checks bestanden; SonarQube Cloud meldet Quality Gate `OK`, null
  offene PR-Issues, `new_violations=0`, null Security-Hotspots und `0,0 %`
  New-Code-Duplikation. Der einzige Issue-Kommentar ist die erfolgreiche
  Sonar-Bot-Benachrichtigung; Review-Kommentare oder eingereichte Reviews
  bleiben aus. Kein Merge wurde autorisiert oder versucht. Der Status ist
  `fixed` bis nutzerautorisierte Integration und Resulting-Master-Reproduktion
  erfolgen.
- `2026-08-01T16:03:41Z`: GitHub mergte exakten PR-#224-Head
  `0da588ecd068f35e27ae404139906e2bebc89e14` normal als Resulting Master
  `7016a66f3702523098811b45139133c77dee88fb`. Alle 14 Workflows für diese
  exakte Master-SHA bestanden. Die Sonar-Master-Analyse ist an diese SHA
  gebunden: `AZ9cRyj3HhV2CayPTPys` und `AZ9cRyj3HhV2CayPTPy2` sind
  `CLOSED/FIXED`, aber `AZ9cRyj3HhV2CayPTPzB` und
  `AZ9cRyj3HhV2CayPTPzC` bleiben `OPEN`. Das Projekt-Quality-Gate ist `ERROR`;
  kein unabhängiger Projekt-Befund wird diesem PR zugeschrieben. Die Original-
  Issue-Reproduktion setzt den Status auf `in_progress` zurück.
- `2026-08-01T16:33:12Z`: Eine frische read-only SonarQube-Cloud-Abfrage
  bestätigt exakt die zwei verbleibenden Current-Master-Keys,
  `AZ9cRyj3HhV2CayPTPzB` und `AZ9cRyj3HhV2CayPTPzC`, beide `python:S3776` bei
  kognitiver Komplexität 16, obwohl 15 erlaubt ist. Der task-eigene Parent-
  Branch zentralisiert die unveränderte Keyed-Plan-Entscheidung für den
  transaktionalen Einstieg in `prepare_connector_with_optional_staging()`;
  öffentliche Apache-/NGINX-Wrapper bewahren den privaten Per-Plan-
  Kontrollfluss. Python-Kompilierung und 34 fokussierte Cache-Contract-Tests
  bestehen, und der fokussierte Review findet keinen plausiblen diff-induzierten
  reportierbaren Security-Befund. Kein Commit, Push, PR, Hosted-Analyse,
  Scanner-Control-Change, Framework-/MRTS-Source, Gitlink oder Master-Action
  wird behauptet.
- `2026-08-01T16:59:29Z`: Exakter Draft-PR-#226-Head
  `b08bc69278570a02af5c0367bffb2dea47d37d7c` ist lokal, remote und auf GitHub
  identisch. Er ist offen, Draft und `CLEAN`, ohne eingereichten Review oder
  Review-Entscheidung. Alle 33 abgeschlossenen GitHub-Checks bestehen und sechs
  erwartete Checks sind übersprungen. SonarQube Cloud meldet Quality Gate `OK`,
  null OPEN/CONFIRMED PR-Issues, `new_violations=0`,
  `new_security_hotspots=0` und null New-Code-Duplikation. Das Finding ist
  `fixed` bis zu expliziter Master-Autorisierung und Resulting-Master-
  Reproduktion; kein Merge oder Scanner-Control-Change erfolgte.

## Neueste aufbewahrte Evidence

- PR-#226-Exact-Head-Hosted-Verification-Receipt (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-two-cognitive-sonar-remediation-20260801/hosted-verification-pr-226-b08bc692.md`)
  — SHA-256 `92cee447f5fb36bfa536681b85c8d6a04d9b9d7f74c2f79db0bfa3e8666b2e5a`;
  übereinstimmender Exact Head, vollständige GitHub-Check-Disposition und
  SonarQube-Cloud-PR-Evidence; beobachtet `2026-08-01T16:59:29Z`.
