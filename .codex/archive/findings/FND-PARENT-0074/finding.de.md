# FND-PARENT-0074 — Case-Runner akzeptierten verlinkte verifizierte Runtime-Roots vor Artefakt-Schreibvorgängen und nativer Oracle-Ausführung

## Klassifikation

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0074 |
| Kategorie | security_validated |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P3 / low / validated (0.78) |
| Status / Machbarkeit | closed / already_fixed |
| Release-Blocker / Candidate-Integration-Blocker / Sicherheitsrelevanz | false / false / true |
| Protokoll / Profil | local/shared-host CI and test-runner verified-artifact-root filesystem boundary / verifizierter Parent-Ersatz-PR #213 mit frischer Historie wurde bei `f335965fd5f7b9640fc39a1dd7873d46d7c989c5` nach `master` gemergt |

## Zusammenfassung

Vor dem lokalen Kandidaten wendeten beide Lifecycle-Case-Runner
`Path(...).resolve()` auf den ausgewählten CLI-/Environment-/Default-
`VERIFIED_RUN_ROOT` an, bevor Artefakt-Verzeichnisse erzeugt wurden. Ein
niedriger privilegierter Akteur mit einem gemeinsamen sticky Temporary-Parent
konnte einen finalen oder Parent-Symlink vorab erzeugen und runner-eigene
Schreibvorgänge umleiten; der Native-Runner kompilierte oder verwendete danach
ein Oracle mit festem Namen unter diesem umgeleiteten Baum wieder und führte es
aus.

Der lokale Kandidat wählt `CLI > VERIFIED_RUN_ROOT > historical fallback` über
`prepare_verified_runtime_artifact_root()`. Er normalisiert nur lexikalisch,
delegiert an den bestehenden Descriptor-basierten No-Follow-Owner-/Mode-
Validator, schlägt mit Exit `77` fail-closed fehl und validiert runner-erzeugte
Case-/Log-/Oracle-Verzeichnisse. Fokussierte Negative- und Legitimate-Controls
bestehen auf dem Tree, der mit aktuellem `master` identisch nachgewiesen ist;
frische Exact-Head-Hosted-Validierung und Post-Merge-Master-Checks sind
erfolgreich abgeschlossen.

## Beobachtetes und erwartetes Verhalten

Die Pre-Remediation-Root-Selection in beiden Case-Runnern folgte mit
`Path(...).resolve()` einem vom Caller kontrollierten bestehenden Symlink vor
`mkdir`, Artefakt-Schreibvorgängen, Compiler-Output,
Native-Oracle-Wiederverwendung/-Ausführung oder einem Child-Harness. Der
vorhersagbare historische Fallback ist
`/var/tmp/ModSecurity-conector-verified`. Dies ist eine lokale/shared-host-
Dateisystem-Integritätsgrenze, keine GitHub-Pull-Request-Token-, Secret-,
Netzwerk- oder Connector-Request-Grenze.

Bevor einer der Case-Runner unter `VERIFIED_RUN_ROOT` Artefakte schreibt,
kompiliert, wiederverwendet, ausführt oder einen Child-Harness startet, müssen
der ausgewählte Root und jeder erzeugte runner-eigene Descendant privat, dem
aktuellen Benutzer zugeordnet, nicht verlinkt und ohne Link-Following
traversiert sein. Die Runner bewahren die Präzedenz
`CLI > VERIFIED_RUN_ROOT > historical fallback` und weisen unsichere, breite,
fremdbesitzte, group/world-writable, final-verlinkte oder parent-verlinkte
Roots zurück. Explain-only-Verhalten darf keinen Runtime-Root materialisieren.

## Impact, Source-to-Sink-Pfad und Voraussetzungen

```text
niedriger privilegierter lokaler/shared-host-Akteur -> finaler oder Parent-Symlink unter sticky /var/tmp -> Path(...).resolve() folgt ihm -> runner-eigener Artefakt-/Compiler-/Oracle-/Harness-Pfad unter umgeleitetem Baum -> mögliche Opferidentitäts-Artefaktumleitung oder Fixed-Name-Oracle-Ausführung
```

Ein erfolgreicher Preseed konnte Evidence-Artefakte umleiten und auf dem
nativen Pfad einen vertrauenswürdigen Developer oder Runner dazu bringen, ein
ersetztes Oracle mit festem Namen wiederzuverwenden oder auszuführen. Der
Effekt benötigt eine lokale/shared-host-Timing- und Dateisystem-Voraussetzung,
daher ist dies low/P3. Es gibt keine Evidence für Remote-Reachability,
Public-Endpoint-Exposition, GitHub-External-PR-/Token-Eskalation,
Secret-Zugriff, Connector-Request-Processing-Impact oder einen normalen
Hosted-CI-Angreiferpfad.

Voraussetzungen sind ein niedriger privilegierter Akteur mit gemeinsamem Host
oder Self-Hosted-Runner, die Auswahl des historischen Fallbacks oder eines
vom Caller gelieferten final-/parent-verlinkten Roots und runner-eigene
Artefakterzeugung. Der native Impact benötigt zusätzlich Compiler-/Oracle-
Voraussetzungen und den nativen Ausführungspfad.

## Betroffener Scope und Evidence

- `ci/lib/runtime_path_utils.py`: `prepare_verified_runtime_artifact_root`,
  `verified_runtime_artifact_root` und `ensure_safe_runtime_directory`.
- `ci/runtime/lifecycle/run-native-case-comparison.py`:
  `run-native-case-comparison.main`, `run_native_case` und `compile_oracle`.
- `ci/runtime/lifecycle/run-verified-case.py`: `run-verified-case.main`.
- `tests/test_runtime_artifact_utils.py` und
  `tests/test_runtime_path_security.py`.

| Evidence | SHA-256 | Ergebnis |
| --- | --- | --- |
| Local case-runner hardening receipt | `ee818da377f476f02852ea5286dcf20b508d14dc85d4b91d0fb51e72357c32e1` | External-root-Syntax, fokussierte Runtime-Artefakt-/Path-/Report-Tests, Terminal-Status-Kompatibilität und Diff-Hygiene bestanden; finale-/Parent-Symlink-Fälle liefern `77` vor beobachteter Victim-/Output-Mutation. |
| Sealed Codex Security diff scan | `f25310a5fd1b2c074d8be405895549c6c3c30f0acd242ace818b16dc1eef463a` | Alle acht geänderten Source-/Test-Zeilen wurden vollständig geprüft; kein reportable diff-introduced Security-Finding überlebte Discovery. |
| Draft-PR-#202-Initial-Delivery-Receipt | `624874cf47b387a05e3572085ba7e775e55a7bf57b186f9cdab11d47c6b69d03` | Draft PR #202 ist offen; lokaler, Origin- und GitHub-Head entsprechen `c846c2c6716c5e321b8743c1d191bfc8193163ca`, Basis ist `caddd86d1eede95de53aa1bc971dd26d875df21c`, und terminale Hosted-Checks/Sonar bleiben ausstehend. |

Die zurückgehaltenen Artefakte sind:

- `/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/evidence/case-runner-root-hardening-local.md`
- `/var/tmp/codex/ModSecurity-conector/codex-security-scans/ModSecurity-conector/caddd86d1eede95de53aa1bc971dd26d875df21c_20260730T142059Z/scan-manifest.json`
- `/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/evidence/pr-202-initial-delivery.md`

## Root Cause und Remediation

Die Runner behandelten die Auflösung eines absolut aussehenden Pfadnamens als
ausreichende Autorität. `Path.resolve()` folgt einem vom Angreifer angelegten
Link, bevor die bestehenden No-Follow-, Ownership- und Mode-Controls ihn
prüfen können. Der dadurch umgeleitete Baum wird Parent von vorhersagbaren
Artefakt- und Native-Oracle-Pfaden.

Die Reparatur zentralisiert die Selection in
`prepare_verified_runtime_artifact_root()`: Sie bewahrt
`CLI > VERIFIED_RUN_ROOT > historical fallback`, absolutisiert ohne
Link-Resolution lexikalisch, delegiert an den bestehenden No-Follow-
Private-Root-Validator, liefert bei `ValueError` vor runner-eigenen
Schreibvorgängen oder Children `77` und erzeugt runner-eigene Case-/Log-/
Oracle-Verzeichnisse mit `ensure_safe_runtime_directory()`. Workflow-
Berechtigungen, Sonar-Regeln, Quality Gates, Test-Controls oder separate
Root-Verträge nicht abschwächen.

## Akzeptanzkriterien und Validierungsplan

1. Beide Runner bewahren `CLI > VERIFIED_RUN_ROOT > historical fallback` und
   liefern `77` vor Schreibvorgängen oder Child-Process-Start bei unsicherem
   Root.
2. Finale Roots und Parent-Komponenten mit Symlink können Target oder native
   Summary-Output über keine Runner-Schnittstelle mutieren.
3. Ein legitimer privater Root wird mit sicheren Modes erzeugt; relative
   Eingabe wird lexikalisch normalisiert und `--explain` materialisiert keinen
   Runtime-Root.
4. Fokussierte Source-/Test-/Security-Diff-Controls bestehen auf dem
   committeten Kandidaten ohne Framework/MRTS-Aktion, Suppression oder
   Quality-Gate-Änderung.
5. Nach dem Push besitzt der exakte PR-Head frische Hosted-GitHub-/Sonar-
   Evidence vor jeder Disposition `verified` oder `closed`.

Die beiden Receipts aufbewahren, nach finalen Dokumentations-/Commit-
Änderungen `py_compile`, die fokussierten Runtime-Artefakt-/Path-/Report-
Tests, Terminal-Status-Kompatibilität und `git diff --check` erneut laufen
lassen. Die Framework-abhängigen `tests.test_collect_no_crs_source` und die
Runtime-Environment-Suite als `blocked_missing_local_checkout` behalten;
Framework/MRTS nicht initialisieren oder ändern, um sie bestehen zu lassen.
Nach dem Push lokalen, Remote- und PR-SHA vergleichen und exakten Head-
GitHub- und SonarQube-Cloud-Status prüfen.

## Abhängigkeiten, Restrisiko und Historie

Der historische PR-#202-Eintrag besaß einen task-eigenen Commit und normalen
Push auf exaktem Head `c846c2c6716c5e321b8743c1d191bfc8193163ca`; seine damals
ausstehenden Checks bleiben unten nur als Historie erhalten. Er ist mit
`FND-PARENT-0068` verwandt, aber kein Duplikat: Die lokale/shared-host-
Schwächenfamilie besitzt eigene
Lifecycle-Case-Runner-Root-Selection, Sinks, Tests und Remediation.
`FND-SONAR-0016` bleibt die aggregierte Sonar-Beobachtung dieses Tasks.

Die Reparatur deckt nur Verified-Run-Root-Selection und runner-erzeugte
Descendants ab. Sie beansprucht keine Sicherheit für separate caller-eigene
`--build-root`, `--tmp-root`, native `--output-dir`, Connector-/Framework-
Roots oder einen Same-UID-Akteur, der einen bereits privaten Root verändern
kann. Es wurden kein Live-Cross-User-Race, Connector-Host oder Framework-
Checkout eingeführt. Die fokussierten Security-Controls, Exact-Head-Hosted-
Checks, der geschützte Merge und die Post-Merge-Master-Checks wurden beobachtet.

- `2026-07-30T14:33:26Z`: Nach Deduplizierung gegen `FND-PARENT-0068`
  angelegt. Lokale Source-to-Sink-, Negative-Symlink-, Legitimate-Control- und
  sealed Security-Diff-Evidence stützen `fixed`; Commit-/Push-/PR-/Hosted-
  Evidence bleibt ausstehend.
- `2026-07-30T15:10:00Z`: Normaler Push erstellte Draft PR #202 gegen
  `master`. Sein lokaler, Origin- und GitHub-Head entsprechen
  `c846c2c6716c5e321b8743c1d191bfc8193163ca`; die Basis entspricht
  `caddd86d1eede95de53aa1bc971dd26d875df21c`. Initiale Checks sind unvollständig,
  daher wird kein Quality-Gate-, Zero-New-Issue-/Duplication-, `verified`-,
  `closed`- oder Merge-Claim erhoben.

### Finale Verifikation und Schließung

Die datierten PR-#202-Einträge oben bleiben nur historische Evidence. Der vom
aktuellen Benutzer autorisierte Ersatz-PR #213 mit frischer Historie bestand
sein exaktes `pull-request-range` Secret Scanning, die erforderlichen GitHub-
Kontexte und das SonarQube-Cloud-Quality-Gate mit null OPEN/CONFIRMED-Issues
und `0.0%` New-Code-Duplizierung. Er wurde über den geschützten
SHA-gebundenen Squash-Pfad nach `master` bei
`f335965fd5f7b9640fc39a1dd7873d46d7c989c5` gemergt; der Branch-Tree ist mit
diesem Master-Tree byte-identisch, die fokussierten Root-Security-Module
bestehen 26 Tests und die Post-Merge-Master-Checks bestanden.

Damit wird dieses Finding geschlossen: Die ursprünglichen Symlink-Root-
Regression-Controls bestehen jetzt auf dem resultierenden Master-Tree. Die
separate historische PR-#202-Scanner-Beobachtung bleibt in
`FND-PARENT-0075` als `not_applicable` erhalten; sie wurde nicht
unterdrückt, umgeschrieben oder als bestandener Scan behandelt.

## Aktuelle Abgleichbestätigung — 2026-08-01

[PR #213](https://github.com/Easton97-Jens/ModSecurity-conector/pull/213) wurde
normal als `f335965fd5f7b9640fc39a1dd7873d46d7c989c5` gemergt und ist vom
aktuellen `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c` erreichbar.
Nach späteren Runner-Änderungen wurde die aktuelle Root-/Symlink-Control-Suite
mit `python3 -B -m unittest tests.test_runtime_artifact_utils
tests.test_runtime_path_security tests.test_generated_report_evidence_integrity`
wiederholt: 107 Tests bestanden. Diese Bestätigung ergänzt, ersetzt aber nicht
die aufbewahrte 26-Test- und Exact-Range-Secret-Scanning-Evidence. Die Suite
wurde nach dem test-only-PR-#229-Update auf
`59aba762f2d852fd917079ca8519e4ea7f49169c` erneut ausgeführt und bestand
wieder mit 107 Tests.
