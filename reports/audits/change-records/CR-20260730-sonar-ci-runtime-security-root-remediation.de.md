# Change Record: Parent-CI-Runtime-SonarQube-Cloud-Remediation und Verified-Root-Hardening

**Sprache:** [English](CR-20260730-sonar-ci-runtime-security-root-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260730-sonar-ci-runtime-security-root-remediation` |
| Datum (UTC) | `2026-07-30` |
| Basis-Revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | Ausgewählte aktuelle SonarQube-Cloud-Code-Smell-Keys: `AZ9cRyd3HhV2CayPTPxL`, `AZ9cRyd3HhV2CayPTPxM`, `AZ7b3dfYcO69wzd-_jHf`, `AZ7b3dfYcO69wzd-_jHg`, `AZ9cRydQHhV2CayPTPxF`, `AZ7b3diDcO69wzd-_jHy`, `AZ7TenozHrNUCHtbhYSE`, `AZ7RRan5GxvN3xmvwZcC`, `AZ7RRan5GxvN3xmvwZcE`, `AZ7RRan5GxvN3xmvwZcD` und `AZ7RRan5GxvN3xmvwZcB`; Security-Remediation `FND-PARENT-0074`; aggregiertes Sonar-Tracking `FND-SONAR-0016`. |
| Grenze | Ausschließlich Parent `ci/runtime/**`, gemeinsames Parent `ci/lib/runtime_path_utils.py`, direkte Parent-Tests, dieses englische/deutsche Change-Record-Paar und gepaarte Change-Record-Indizes. Keine `.github/`, keine `scripts/`, kein Framework, kein MRTS, kein Gitlink, keine Scanner-Konfiguration, kein Quality Gate, keine Exclusion, keine Suppression, kein `NOSONAR`, kein Workflow und keine `master`-Änderung sind enthalten. |

## Motivation und Problemstellung

Die aktuelle Master-Analyse `43a50e20-8bdd-453a-bc44-549a7e3d7588` ist an
`caddd86d1eede95de53aa1bc971dd26d875df21c` gebunden und meldet 78 offene
Befunde unter `ci/runtime`: drei scanner-gelabelte Anker in `common` und 75 in
`lifecycle`. Dieses Record behebt bewusst nur die oben genannten 11 aktuellen,
niedrigriskanten source-applicable Code-Smell-Keys. Die scanner-gelabelten
`common`-Anker sind already-safe Rule-Leads, höher riskante Orchestrierungs-
Kandidaten haben keinen sicheren One-PR-Beweis, und ein aktiver unabhängiger PR
besitzt `AZ9cRycZHhV2CayPTPw4`; keiner wird unterdrückt, als False Positive
markiert oder hier als fixed beansprucht.

Die Source-to-Sink-Prüfung stellte außerdem fest, dass beide Lifecycle-Case-
Runner `Path(...).resolve()` auf ausgewählten `VERIFIED_RUN_ROOT`-Input
anwenden, bevor Artefaktverzeichnisse erzeugt werden. Ein niedriger
privilegierter Akteur, der einen sticky Temporary-Parent teilt, konnte einen
finalen oder Ancestor-Symlink vorbelegen und runner-eigene Schreibvorgänge
umleiten. Der Native-Case-Runner konnte danach ein Oracle mit festem Namen
unter dem umgeleiteten Baum kompilieren, wiederverwenden oder ausführen. Dieser
begrenzte lokale Dateisystem-Integritätsdefekt wird getrennt als
`FND-PARENT-0074` verfolgt.

## Akzeptanzkriterien

- Die ausgewählten 11 Code-Smell-Keys erhalten die kleinsten
  verhaltenerhaltenden Source-Änderungen; kein anderer aktueller
  `ci/runtime`-Befund wird als remediiert beansprucht.
- Case-Runner bewahren die Präzedenz `CLI > VERIFIED_RUN_ROOT > fallback` und
  weisen unsichere Roots vor runner-eigenen Schreibvorgängen, Compiler-Output,
  Native-Oracle-Wiederverwendung/-Ausführung oder Child-Harness-Start zurück.
- Finale Root- und Parent-Component-Symlink-Controls beenden mit Exit `77`,
  ohne ein Target zu verändern; ein legitimer privater Root, relative
  lexikalische Normalisierung und `--explain`-Nichtmaterialisierung bleiben
  gültig.
- Bestehendes Report-Layout, Full-Matrix-Command-Klassifikation,
  Timestamp-Parsing, Case-Result-Dateiname, Terminal-Statuses und Native-
  Case-Metadaten behalten ihre bisherige Semantik.
- Der exakte PR-Head muss null neue SonarQube-Cloud-Issues, null neue
  duplizierte Zeilen und `0.0%` New-Code-Duplizierung erhalten, ohne einen
  Scanner-, Quality-Gate-, Test- oder Security-Control abzuschwächen.

## Implementierungsentscheidung und Begründung

`prepare_verified_runtime_artifact_root()` zentralisiert die Selection in
`ci/lib/runtime_path_utils.py`. Sie macht einen Pfad ohne Auflösung eines
input-kontrollierten Links lexikalisch absolut und delegiert dann an den
bestehenden Descriptor-basierten No-Follow-Owner-/Mode-Validator. Beide Case-
Runner rufen ihn vor Directory-Materialisierung oder Child-Arbeit auf, schlagen
bei `ValueError` mit Exit `77` fail-closed fehl und erzeugen runner-eigene
Case-, Log- und Native-Oracle-Verzeichnisse mit
`ensure_safe_runtime_directory()`.

Die engen Sonar-Änderungen geben wiederholten unveränderlichen Strings nur
private Owner oder flachen die exakte Terminal-Status-Conditional ab. Sie
bewahren Original-Bytes, Reihenfolge, Command-Konstruktion, Report-Tabellen,
Timestamps und Return-Mapping.

## Betrachtete Alternativen

Die Auflösung eines ausgewählten Roots vor der Validierung wurde abgelehnt,
weil sie einem vorbelegten Symlink vor der No-Follow-Inspection folgt. Ein
lexikalischer Check allein wurde abgelehnt, weil er keinen bestehenden finalen
oder Ancestor-Symlink schließen kann. Suppressions, `NOSONAR`, Quality-Gate-/
Rule-Änderungen und externe False-Positive-Aktionen wurden abgelehnt, weil sie
die Source-Grenze nicht reparieren oder das erforderliche Exact-Head-
Qualitätsergebnis belegen.

Höher riskante Complexity-, Unicode-, Regular-Expression- und Runner-
Orchestrierungsbefunde bleiben unverändert, weil eine verhaltenerhaltende
One-PR-Remediation nicht bewiesen war. Der unabhängige Active-PR-Key
`AZ9cRycZHhV2CayPTPw4` liegt außerhalb dieses Diffs.

## Geänderte Dateien

- `ci/lib/runtime_path_utils.py`
- `ci/runtime/lifecycle/collect-no-crs-source.py`
- `ci/runtime/lifecycle/run-native-case-comparison.py`
- `ci/runtime/lifecycle/run-verified-case.py`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `tests/test_collect_no_crs_source.py`
- `tests/test_runtime_artifact_utils.py`
- `tests/test_runtime_path_security.py`
- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-security-root-remediation.md`
- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-security-root-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Manuelle revisionsgebundene SonarQube-Cloud-API-Inventar-Prozedur im Task-Plan aufbewahrt | bestanden: Analyse `43a50e20-8bdd-453a-bc44-549a7e3d7588` entspricht Basis `caddd86d1eede95de53aa1bc971dd26d875df21c`; die ausgewählten 11 Keys und der unabhängige Active-PR-Key wurden festgehalten. |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile ci/lib/runtime_path_utils.py ci/runtime/lifecycle/collect-no-crs-source.py ci/runtime/lifecycle/run-native-case-comparison.py ci/runtime/lifecycle/run-verified-case.py ci/runtime/lifecycle/run-verified-report-run.py tests/test_collect_no_crs_source.py tests/test_runtime_artifact_utils.py tests/test_runtime_path_security.py` | bestanden: die fünf geänderten Production-Dateien und drei geänderten Tests kompilieren. |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_runtime_artifact_utils tests.test_runtime_path_security tests.test_generated_report_evidence_integrity` | bestanden: 102 Tests in 15.050s. |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_runtime_artifact_utils tests.test_runtime_path_security` | bestanden: 26 Tests in 2.440s nach der finalen legitimen Broad-Root-Rejection-Regression. |
| Manuelle Terminal-Status-JSONL-Prozedur in der lokalen `FND-PARENT-0074`-Receipt aufbewahrt | bestanden: `NOT_EXECUTABLE`, `SKIPPED`, `BLOCKED`, `UNSUPPORTED`, `NOT_APPLICABLE`, `NOT_EXECUTED` und `PASS` enden jeweils mit Exit `0`. |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_collect_no_crs_source.CollectNoCrsSourceTest.test_explicit_terminal_statuses_keep_their_existing_precedence` | `blocked_missing_local_checkout`: der Import stoppt bei fehlendem `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`; Framework/MRTS wurde nicht initialisiert oder geändert. |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_runtime_path_security.RuntimePathSecurityTest.test_case_runners_reject_symlinked_verified_roots_before_runtime_actions tests.test_runtime_path_security.RuntimePathSecurityTest.test_precreated_verified_runtime_root_symlink_is_rejected tests.test_runtime_path_security.RuntimePathSecurityTest.test_verified_case_explain_does_not_materialize_a_runtime_root` | bestanden: 3 Tests in 0.090s; Final-Root- und Parent-Component-Controls enden mit Exit `77` vor beobachteter Target-Mutation, Artefakt-Output, Compiler-Output oder Harness-Start. |
| Manuelle Codex-Security-`security-diff-scan`-Prozedur, Report-Range `caddd86d1eede95de53aa1bc971dd26d875df21c...working-tree`, unter `FND-PARENT-0074` aufbewahrt | bestanden: alle acht geänderten Source-/Test-Zeilen wurden vollständig geprüft; kein reportable diff-introduced Security-Finding blieb bestehen. |
| `rtk proxy -- make check-bilingual-docs` | `blocked_missing_local_checkout`: das neue Change-Record-Paar wurde nicht gemeldet; die Diagnostik betrifft die nicht initialisierten Framework-Link-Targets sowie das task-eigene ungetrackte `cleanup-manifest.md` ohne deutschen Companion. |
| `rtk proxy -- make check-doc-links` | `blocked_missing_local_checkout`: die Diagnostik betrifft nur die nicht initialisierten Framework-Link-Targets; kein neuer Change-Record-Link wird gemeldet. |
| `rtk proxy -- env VERIFIED_RUN_ROOT=/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/build PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make lint` | `blocked_missing_local_checkout`: POSIX-/Bash-Syntax und die Kompilierung aller `ci/*.py` bestanden, bevor `check-no-crs-source-normalization` die fehlende Framework-Datei importiert. |
| `rtk proxy -- git diff --check` nach dem finalen Change-Record-Update | bestanden. |

### Details der manuellen Prozeduren

Die öffentliche SonarQube-Cloud-Inventar-Prozedur ruft zuerst
`https://sonarcloud.io/api/project_analyses/search?project=Easton97-Jens_ModSecurity-conector&branch=master` ab, wählt die Analyse
`43a50e20-8bdd-453a-bc44-549a7e3d7588` und bestätigt, dass ihre Revision
`caddd86d1eede95de53aa1bc971dd26d875df21c` entspricht. Anschließend ruft sie
`https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&branch=master&statuses=OPEN,CONFIRMED,REOPENED&ps=500` ab, filtert Pfade unter `ci/runtime/` und vergleicht die zurückgegebenen Keys mit den elf Tracking-Keys und `AZ9cRycZHhV2CayPTPw4`. Die Prozedur ist read-only und verwendet keine Credentials, Issue-Mutation, Suppression oder Quality-Gate-Änderung.

Für die Terminal-Status-Prozedur enthält ein task-eigenes `cases.jsonl` pro
`SOURCE_STATUS` in `NOT_EXECUTABLE`, `SKIPPED`, `BLOCKED`, `UNSUPPORTED`,
`NOT_APPLICABLE`, `NOT_EXECUTED` und `PASS` eine
`{"case_id":"allow_without_marker","status":SOURCE_STATUS,"actual_status":200,"live_executed":SOURCE_STATUS=="PASS"}`-Zeile. Die Prozedur ruft
`case_observations([source], "nginx", "1100001", {"allow_without_marker": (200, None)})` auf und vergleicht den zurückgegebenen Status jeweils mit `NOT_EXECUTED`, `NOT_EXECUTED`, `BLOCKED`, `UNSUPPORTED`, `NOT_APPLICABLE`, `NOT_EXECUTED` und `PASS`. Diese exakte Source-Contract-Prozedur ist in der `FND-PARENT-0074`-Evidence-Receipt aufbewahrt; ihr gewöhnlicher Module-Test kann in diesem Worktree nicht importieren, solange der Framework-Gitlink absichtlich nicht initialisiert ist.

Der manuelle Loader erzeugt `source` und `collector`, ohne das Framework-
abhängige Testmodul zu importieren:

```python
import importlib.util
import json
from pathlib import Path

source = Path("cases.jsonl")
source.write_text(json.dumps({"case_id": "allow_without_marker", "status": SOURCE_STATUS, "actual_status": 200, "live_executed": SOURCE_STATUS == "PASS"}) + "\n", encoding="utf-8")
spec = importlib.util.spec_from_file_location("collect_no_crs_source", Path("ci/runtime/lifecycle/collect-no-crs-source.py"))
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
cases, _ = collector.case_observations([source], "nginx", "1100001", {"allow_without_marker": (200, None)})
```

Die Prozedur wiederholt die Zeilen `source.write_text(...)` und
`collector.case_observations(...)` einmal für jeden aufgeführten
`SOURCE_STATUS`.

Für die Codex-Security-Prüfung verwendet der Scan die Basis
`caddd86d1eede95de53aa1bc971dd26d875df21c`, stellt nach dem Ausschluss von
`ci/` und `tests/` durch die generische Worklist die exakte Git-Diff-Menge
`ci/lib/runtime_path_utils.py`, `ci/runtime/lifecycle/collect-no-crs-source.py`,
`ci/runtime/lifecycle/run-native-case-comparison.py`,
`ci/runtime/lifecycle/run-verified-case.py`,
`ci/runtime/lifecycle/run-verified-report-run.py`,
`tests/test_collect_no_crs_source.py`, `tests/test_runtime_artifact_utils.py`
und `tests/test_runtime_path_security.py` wieder her und führt für jede Zeile
eine vollständige Source-/Control-/Sink- und Bypass-Prüfung durch. Seine
versiegelte Manifest-SHA-256 lautet
`f25310a5fd1b2c074d8be405895549c6c3c30f0acd242ace818b16dc1eef463a`; sie
zeichnet vollständige Acht-Zeilen-Coverage und null reportable
diff-introduced Findings auf.

## Tests und tatsächliche Ergebnisse

Die fokussierten Controls decken den gemeinsamen Selection-Helper und beide
direkten Runner-Interfaces ab. Expliziter CLI-Input hat Vorrang vor
`VERIFIED_RUN_ROOT`, das Vorrang vor dem historischen Fallback hat; ein
privater Root bleibt verwendbar und relativer Input wird ohne Link-Auflösung
normalisiert. Die Runner weisen finale Root- und Parent-Component-Symlinks vor
beobachteten Schreibvorgängen oder Children zurück. `--explain` kehrt zurück,
ohne einen Root zu materialisieren.

Die Report-Evidence-Suite bestätigt, dass extrahierte statische Strings
bestehende Report-Bytes und Full-Matrix-Command-Semantik bewahren. Der direkte
`collect-no-crs-source.py`-JSONL-Control bestätigt jedes beibehaltene
Terminal-Status-Mapping. Dies sind fokussierte lokale Source-/Contract-
Controls, keine Connector-Matrix oder Hosted-CI-Ergebnisse.

## Security-Auswirkung

Die Verified-Root-Änderung repariert eine validierte lokale/shared-host-
Dateisystemgrenze. Die Voraussetzung ist ein niedriger privilegierter Akteur,
der einen finalen oder Ancestor-Symlink unter einem geteilten sticky
Temporary-Parent erzeugen kann, bevor das private Runner-Child angelegt wird.
Die Reparatur nutzt repository-native Descriptor-Traversal-, No-Follow-,
Ownership- und Mode-Checks vor Artefakt-, Compiler-, Executable- oder
Harness-Sinks.

Sie beansprucht keine Sicherheit für unabhängige caller-eigene `--build-root`,
`--tmp-root`, native `--output-dir`, Connector-/Framework-Roots oder einen
Same-UID-Akteur, der einen bereits privaten Root verändern kann. Es wurde kein
Live-Cross-User-Race, Connector-Host, Remote-Endpoint, GitHub-Token, Secret
oder External-PR-Execution-Pfad ausgeführt. Die versiegelte Security-Prüfung
fand keinen neuen diff-introduced Security-Candidate.

## Dokumentationsstatus

Dieses englische/deutsche Paar hält Sonar-Grenze, ausgewählte Repair-Keys,
Verified-Root-Entscheidung, Security-Finding, fokussierte Controls und
Delivery-Limits fest. Beide Change-Record-Indizes sind aktualisiert.
`FND-PARENT-0074` ist ein lokaler Control-Plane-Record und wird nicht als
versionierte Product-Dokumentation gestaged.

## Runtime-Evidence

Keine Connector-Runtime-Matrix, keine networked Preparation, keine Package-
Installation, kein Generated-Report-Refresh und kein Production-Deployment
wurden ausgeführt. Die deterministischen Symlink-Controls üben reale Runner-
Entry-Points in task-eigenem Temporary-Storage aus; sie sind lokale
Dateisystem-Integritäts-Controls, keine Live-Multi-User-Race- oder Production-
Connector-Ergebnisse.

## Kompatibilität und generierte Artefakte

Kein generiertes Artefakt wird committed. Die Literalextraktionen bewahren
Report- und Native-Case-String-Werte, Result-Dateiname, Full-Matrix-Prefix,
UTC-Konvertierung, Tabellenstruktur, Status-Mapping und Command-Konstruktion.
Die absichtliche Kompatibilitätsänderung weist unsichere/verlinkte Roots zurück
statt sie aufzulösen; vertrauenswürdige private absolute Roots und die
dokumentierte Präzedenz bleiben verwendbar.

## Bekannte Einschränkungen

Der absichtlich nicht initialisierte Framework-Gitlink blockiert
`tests.test_collect_no_crs_source` und die Runtime-Environment-Suite in diesem
isolierten Parent-Worktree. Framework/MRTS zu initialisieren oder zu ändern,
um ein Passing-Result zu erhalten, liegt außerhalb des Scopes und wurde nicht
versucht. Die lokalen Tests beweisen Cross-User-Race-Resistenz über
deterministische Symlink-Controls und Descriptor-basierte Implementierungs-
Prüfung hinaus nicht.

## Verbleibende Risiken

Die anderen 67 aktuellen `ci/runtime`-Befunde bleiben außerhalb der begrenzten
Remediation-Menge dieses PR. Die Security-Reparatur wartet auf task-eigenen
Commit, normalen Push, Draft-PR und frische Exact-Head-GitHub-/SonarQube-
Cloud-Evidence, bevor `FND-PARENT-0074` `verified` oder `closed` werden kann.

## Nicht ausgeführte Prüfungen mit Begründung

- Die vollständige Connector-/Runtime-Matrix, Host-Preparation, networked
  Checks, Package-Installation, Generated-Report-Refresh und ein Live-
  Cross-User-Race wurden nicht ausgeführt: Sie würden den fokussierten Parent-
  Source-/Contract-Scope erweitern.
- Framework/MRTS-Source, Gitlinks, Workflows, `.github/`, `scripts/`, Scanner-
  Konfiguration, Suppressions, Exclusions, Quality Gates, externer Sonar-
  Issue-Status und `master` blieben unverändert/nicht ausgeführt.
- Hosted-GitHub-Actions, PR-Review, SonarQube-Cloud-PR-Analyse und Merge-
  Evidence benötigen den späteren exakten Draft-PR-Head und werden nicht lokal
  hergeleitet.

## Finaler Diff- und Review-Status

Der lokale Scoped-Diff enthält Verified-Root-Hardening, elf enge
Sonar-orientierte Maintainability-Repairs, direkte Regression-Controls und
dieses bilinguale Traceability-Paar. Der fokussierte Security-Diff-Scan hat
null reportable diff-introduced Findings. Zum Authoring-Zeitpunkt gibt es
keinen Task-Commit, Push, Draft-PR, Hosted-Check, Review, Exact-Head-
SonarQube-Cloud-Ergebnis oder `master`-Integration-Claim; diese Fakten müssen
erst nach Beobachtung ergänzt werden.
