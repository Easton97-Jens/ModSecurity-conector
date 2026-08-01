# Änderungsnachweis: Bereinigung der verbleibenden SonarQube-Cloud-Befunde in Parent-CI-Checks

**Sprache:** [English](CR-20260801-sonar-ci-checks-followup-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-sonar-ci-checks-followup-remediation` |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `caabf33c11d6002f9a1661f215ed195d6e141253` |
| Tracking | Aktuelles Parent-`ci/checks/`-Inventar: 4 Vulnerabilities, 5 Maintainability-Befunde, 0 Security Hotspots und 0 duplizierte Zeilen. |
| Grenze | Parent-`ci/checks/`, direkt erforderliche Parent-Tests und dieses englisch/deutsche Change-Record-/Index-Paar. Framework, MRTS, Gitlinks, Workflows, Scanner-Einstellungen, Suppressions und `master` bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle Master-Analyse enthält neun ungelöste Source-Zeilen unterhalb von `ci/checks/`: einmal `pythonsecurity:S2083`, dreimal `python:S5443`, einmal `python:S108` und viermal `python:S3776`. Sie betreffen einen Test-Matrix-Report-Writer, Runtime-Policy-Fixtures, einen leeren Lifecycle-Branch sowie Parsing-/Default-/Metadaten-Dispatch der Konfigurationsreferenz. Die Bereinigung bewahrt die fail-closed-Dateisystem- und Runtime-Path-Verträge der Checker und behandelt jede Source-Ursache ohne SonarQube-Cloud-Einstellung, Suppression, Exclusion, Quality-Gate-Workaround oder `NOSONAR`-Marker.

## Implementierungsentscheidung und Begründung

Der Language-Switch-Generator schreibt nur Pfade aus seiner eingecheckten Report-Registry, nachdem reguläre Datei, aufgelöster Pfad im Checkout und Symlink-Ausschluss geprüft sind. Seine Texttransformation ist ein reiner Helper mit expliziten Negativ-Controls. Der Runtime-Policy-Selbsttest übergibt dem Kindprozess die Verified-Run-Root als temporäre Pfadvariable und verwendet einen Kindpfad davon als Non-System-Control-Fixture; breite `/tmp`-Fixtures werden nicht mehr gesetzt.

Der Lifecycle-Checker stellt die Auswahl `profile` durch seine bereits leere Fehlerliste dar statt durch einen leeren Kontrollfluss-Branch. Die Konfigurationsreferenz bewahrt die Bytes des generierten Inventars, während YAML-Line-/Stack-/Inline-Field-Behandlung, Source-Default-Prüfungen, Envoy-Listener-Selektionskontext und Traefik-Middleware-/Router-Beschreibungen in fokussierte Helper ausgegliedert werden. Damit bleibt der dokumentierte Connector-Metadaten-Vertrag unverändert.

## Akzeptanzkriterien

- Alle neun aktuellen Parent-`ci/checks/`-SonarQube-Cloud-Zeilen erhalten eine Source-Level-Behebung ohne Änderung der Scanner-Controls.
- Report-Schreibvorgänge bleiben auf ausgewählte reguläre Nicht-Symlink-Dateien unterhalb des Checkouts begrenzt, und der Verified-Runtime-Root-Control bleibt akzeptiert.
- Der exakte Draft-PR-Head muss null offene Scoped-Issues, null neue Issues und 0,0 % New-Code-Duplizierung zeigen.

## Geänderte Dateien

- `ci/checks/documentation/connector_config_reference.py`
- `ci/checks/documentation/ensure-test-matrix-language-switches.py`
- `ci/checks/evidence/check-full-lifecycle-evidence.py`
- `ci/checks/security/check-runtime-path-policy.py`
- `tests/test_ensure_test_matrix_language_switches.py`
- `tests/test_runtime_path_policy.py`
- `reports/audits/change-records/README.md`, das deutsche Gegenstück und dieses englisch/deutsche Change-Record-Paar.

## Security-Auswirkung

Der Report-Updater weist weiterhin symbolische Links, nicht reguläre Dateien und aufgelöste Pfade außerhalb des Checkouts zurück, bevor ein Schreibversuch erfolgt. Der neue Registry-besessene Schreibpfad entfernt das generische, vom Caller übergebene Write-Ziel. Der Runtime-Policy-Selbsttest weist weiter System- und breite mutable Pfade zurück; die Verwendung seiner Verified-Run-Root für `RUNNER_TEMP` und `TMPDIR` begrenzt die Kindprozessumgebung statt sie zu erweitern. Credential-, Netzwerk-, Workflow-Permission-, Scanner- und Quality-Control-Grenzen ändern sich nicht.

## Validierung

| Befehl | Ergebnis |
| --- | --- |
| `/root/git/ModSecurity-conector/.venv/bin/python -m pip check` | bestanden: keine defekten Requirements; ausgewählter Parent-Interpreter ist Python 3.14.4. |
| Fokussierte `unittest`-Auswahl für Report-Switches, Runtime-Path-Controls, Lifecycle-Evidence und Connector-Konfigurationsreferenz | bestanden: 33 Tests. |
| `python ci/checks/documentation/check-connector-config-reference.py` | bestanden: alle acht Inventare. |
| `python ci/checks/documentation/ensure-test-matrix-language-switches.py` | bestanden: `ok`, ohne Generated-File-Drift. |

## Ausgeführte Befehle

Die Befehle in **Validierung** wurden im isolierten Parent-Worktree beobachtet.
`git diff --check`, finale Dokumentationsvalidierung, Security-Diff-Review und
SHA-gebundene Hosted-Validierung bleiben getrennte finale Meilensteine.

## Runtime-Evidence

Nicht anwendbar. Die Änderung betrifft statische Parent-CI-Checker und Dokumentationsgenerierung. Die In-Tree-Regular-File- sowie die abgewiesenen Symlink-/Traversal-Controls sind Dateisystem-Grenz-Evidence, keine Connector-Runtime-Behauptung.

## Nicht ausgeführte Prüfungen mit Begründung

- Der eine direkte Subprocess-Control `RuntimePathPolicyTest.test_default_policy_selftest_ignores_caller_cache_overrides` kann im isolierten Parent-Worktree nicht laufen, weil das Parent-gebundene Framework-Gitlink-Ziel dort absichtlich nicht materialisiert ist. Er scheitert vor der geänderten Parent-Logik, wenn der erforderliche Pfad `modules/ModSecurity-test-Framework/ci/lib/common.sh` fehlt. Eine Framework-Materialisierung oder -Änderung liegt außerhalb der Autorität dieses Tasks.
- Vollständige Connector-Builds, Runtime-Matrizen sowie Framework-/MRTS-Checks wurden nicht ausgeführt, weil keine Connector-Produktsource, Framework-Source, MRTS-Source oder Gitlink im Scope liegt.
- SHA-gebundene GitHub Actions, Review-Status und SonarQube-Cloud-Ergebnisse benötigen den nachfolgenden Draft-PR und werden durch diesen lokalen Record nicht behauptet.

## Bekannte Einschränkungen und nächste Evidence

Der exakte Task-PR-Head muss eine frische SonarQube-Cloud-Analyse erhalten, bevor die neun Source-Zeilen als `fixed` markiert werden können. Der PR muss null offene Scoped-Issues, null neue Issues und 0,0 % New-Code-Duplizierung zeigen. Erforderliche GitHub Actions müssen für denselben Head gelesen werden. Dieser Record autorisiert und behauptet keinen Merge.

## Verbleibende Risiken

Strukturelle Dokumentationsrefactorings können außerhalb der fokussierten
Fixtures eine ungewöhnliche Template-Path-Diagnoseabweichung zeigen. Die
sicherheitsrelevanten Schreib- und Runtime-Root-Grenzen haben direkte negative
und legitime Controls, aber der exakte PR-Head benötigt weiterhin unabhängige
Hosted-/Sonar-Verifikation.

## Finaler Diff- und Review-Status

Zum Zeitpunkt dieses Records ist der Kandidat auf Parent-`ci/checks/`,
fokussierte Parent-Tests und bilinguale Traceability-Dateien begrenzt. Es gibt
keine Framework-/MRTS-/Gitlink-, Workflow-, Dependency-, Scanner-
Konfigurations-, Suppression- oder `master`-Änderung. Finaler Scoped-Review
und Delivery werden noch nicht behauptet.
