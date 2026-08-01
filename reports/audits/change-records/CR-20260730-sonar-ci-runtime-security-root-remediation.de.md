# Change Record: Parent-CI-Runtime-SonarQube-Cloud-Remediation und Verified-Root-Hardening

**Sprache:** [English](CR-20260730-sonar-ci-runtime-security-root-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260730-sonar-ci-runtime-security-root-remediation` |
| Datum (UTC) | `2026-08-01` |
| Basis-Revision | `30f7f58097d8b9659e27c64afde1c394c2f5f308` |
| Ziel | Die geprüfte CI-Runtime-Remediation in einer frischen Parent-Historie bewahren, die gegen den aktuellen `master` verifiziert werden kann, ohne eine frühere Delivery-Historie erneut abzuspielen. |
| Grenze | Nur Parent `ci/runtime/**`, gemeinsames Parent `ci/lib/runtime_path_utils.py`, direkte Parent-Tests, dieses englische/deutsche Change-Record-Paar und seine Indizes. Kein Framework, MRTS, Gitlink, keine Scanner-Konfiguration, kein Quality Gate, keine Exclusion, Suppression, `NOSONAR`, kein Workflow und keine direkte `master`-Änderung sind enthalten. |

## Motivation und Problemstellung

Die Remediation wählte elf historische, risikoarme source-applicable
CI-Runtime-Code-Smell-Repairs und eine Filesystem-Härtung des Verified-Runtime-
Root aus. Die historische Auswahl beruhte auf einer früheren Master-Analyse;
dieser Ersatz behauptet weder diese Analyse noch ihre Issue-Zahl oder ein
Hosted-Ergebnis als aktuelle Evidence. Der Ersatz muss gegen seinen eigenen
exakten Head inventarisiert und verifiziert werden.

Zuvor lösten beide Lifecycle-Case-Runner einen ausgewählten
`VERIFIED_RUN_ROOT` vor der deskriptorbasierten Validierung auf und erstellten
anschließend runner-eigene Artefakte darunter. Ein niedrig privilegierter Akteur
mit Zugriff auf einen gemeinsamen temporären Parent konnte einen finalen oder
Ancestor-Symlink vorab anlegen, so dass Writes, Native-Oracle-Output oder
Child-Harness-Arbeit an einem unbeabsichtigten Ort erfolgen konnten.

Eine frühere Delivery-Historie bleibt separat erhalten. Sie wird hier bewusst
nicht erneut abgespielt: Der Pull-Request-Range-Security-Control bewertet die
Commit-Historie ebenso wie den Endbaum. Dieser Ersatz enthält nur den geprüften
Endinhalt auf der aktuellen Parent-Basis und behauptet keine geerbten CI-,
Review-, SonarQube-Cloud- oder Delivery-Ergebnisse.

## Akzeptanzkriterien

- Die ausgewählten historischen Code-Smell-Repairs bleiben auf die geprüften
  Source-Pfade begrenzt; kein breiteres aktuelles `ci/runtime`-Inventar wird
  als behoben behauptet.
- Case-Runner bewahren die Präzedenz `CLI > VERIFIED_RUN_ROOT > fallback`,
  weisen aber unsichere Roots vor runner-eigenen Writes, Compiler-Output,
  Native-Oracle-Wiederverwendung oder -Ausführung sowie Child-Harness-Start
  zurück.
- Final-Root- und Ancestor-Component-Symlink-Controls beenden mit `77`, bevor
  ein Ziel mutiert wird; ein legitimer privater Root, lexikalische relative
  Normalisierung und `--explain` ohne Materialisierung bleiben gültig.
- Report-Layout, Command-Klassifikation, Timestamp-Konvertierung,
  Result-Dateiname, Terminal-Status-Semantik und Native-Case-Metadaten
  behalten ihr vorheriges Verhalten.
- Der exakte Ersatz-PR-Head muss null neue SonarQube-Cloud-Issues, null neue
  Duplikatzeilen und `0.0%` New-Code-Duplikation ohne Abschwächung eines
  Scanners, Tests, Quality Gates oder Security-Controls aufweisen.
- Der exakte Ersatz-Commit-Range muss den normalen redigierten Pull-Request-
  Secret-Scanning-Control des Repositorys bestehen.

## Implementierungsentscheidung und Begründung

`prepare_verified_runtime_artifact_root()` wählt den angeforderten Root zentral
aus und macht ihn lexikalisch absolut, ohne einen eingabegesteuerten Link
aufzulösen. Anschließend delegiert er an den vorhandenen deskriptorbasierten
No-Follow-Owner/Mode-Validator. Der native und der verified Case-Runner rufen
diesen Control vor der Materialisierung eines Run-Verzeichnisses oder Child-
Arbeit auf, schlagen bei `ValueError` mit Exit `77` fail-closed fehl und
verwenden `ensure_safe_runtime_directory()` für runner-eigene Descendants.

Die schmalen Maintainability-Änderungen geben wiederholten unveränderlichen
Strings private Owner oder glätten die exakte Terminal-Status-Bedingung. Sie
bewahren Bytes, Reihenfolge, Command-Konstruktion, Report-Tabellen, Timestamps
und Return-Mapping.

## Alternativen

Das Wiederholen des früheren Branch, das Auflösen von Eingabepfaden vor der
Validierung, Suppression, `NOSONAR`, Quality-Gate-Änderungen oder Scanner-
Änderungen wurden verworfen. Sie würden entweder den alten historiengebundenen
Control-Fehler bewahren, einem vorab angelegten Link folgen oder eine Reparatur
durch eine unverifizierte Ausnahme ersetzen.

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

| Befehl oder Control | Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <repository-venv>/bin/python -m py_compile` für die fünf geänderten Production-Dateien und drei geänderten Tests | bestanden. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-root>/tmp <repository-venv>/bin/python -m unittest -q tests.test_runtime_artifact_utils tests.test_runtime_path_security` | bestanden: 26 Tests in 2.395s. |
| Fokussierte `importlib`-Terminal-Status-Prozedur für `collect-no-crs-source.py` mit sieben JSONL-Source-Status | bestanden: Alle sieben behielten ihren erwarteten kanonischen Status. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-root>/tmp <repository-venv>/bin/python -m unittest -q tests.test_collect_no_crs_source` | `blocked_missing_local_checkout`: Der Import benötigt die absichtlich fehlende Parent-gebundene Framework-Datei `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`; Framework/MRTS wurde nicht initialisiert oder geändert. |
| `rtk proxy -- git diff --check` und exakter Content-Vergleich der acht Source/Test-Pfade mit dem geprüften finalen Remediation-Baum | bestanden. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <repository-venv>/bin/python ci/checks/documentation/check-bilingual-docs.py` | `blocked_missing_local_checkout`: Kein neuer Change-Record- oder Changed-File-Diagnose; nur vorbestehende Links in den absichtlich fehlenden Parent-gebundenen Framework-Checkout fehlen. |
| Exakte Ersatz-Head-GitHub-Actions, Pull-Request-Secret-Scanning, Review, SonarQube Cloud und Master-Integration | nicht ausgeführt: Bei Erstellung dieses Records existiert kein Ersatz-PR. |

## Security-Auswirkung

Die geänderte Grenze akzeptiert ein CLI-Argument oder eine
`VERIFIED_RUN_ROOT`-Environment-Variable und kontrolliert runner-eigene
Verzeichnisse, Logs, kompilierten Native-Oracle-Output, JSON-Artefakte und
Child-Harness-Arbeit. Die deskriptorbasierten No-Follow-, Owner- und Mode-
Checks sind der nächste Control vor diesen Sinks. Die direkten Negativ-Controls
müssen zeigen, dass ein finaler oder Ancestor-Symlink vor Seiteneffekten
zurückgewiesen wird, während ein privater legitimer Root nutzbar bleibt.

Der Ersatz ändert weder den Secret-Scanning-Workflow noch Gitleaks-
Provisioning/Lock-Record, Quality Gate, Exclusions, Suppressions oder eine
Credential. Ein erfolgreicher Exact-Range-Scan ist vor der Integration
erforderlich; Scanner-Output, Detector-Match oder secret-like Wert werden hier
nicht aufgezeichnet.

Diese Änderung behauptet keine Absicherung unabhängiger caller-eigener
`--build-root`, `--tmp-root`, nativer `--output-dir`, Connector-/Framework-
Roots, eines Same-UID-Angreifers mit Änderungsmöglichkeit eines bereits privaten
Roots oder eines Live-Cross-User-Race.

## Kompatibilität und generierte Artefakte

Kein generiertes Artefakt wird committed. Die beabsichtigte
Kompatibilitätsänderung besteht darin, unsichere oder symlinked Verified-Roots
zurückzuweisen statt sie aufzulösen; vertrauenswürdige private absolute Roots
und die dokumentierte Präzedenz bleiben nutzbar.

## Dokumentationsstatus

Das gepaarte englische/deutsche Change Record und die Indizes bewahren den
Navigationseintrag. Die bilinguale Dokumentationsprüfung fand keinen neuen
Change-Record- oder Changed-File-Diagnose; sie ist nur durch Links in den
absichtlich fehlenden Parent-gebundenen Framework-Checkout blockiert.

## Runtime-Evidence

Keine Connector-Matrix, Host-Vorbereitung, Paketinstallation, Generated-Report-
Refresh, netzwerkgebundene Vorbereitung, Produktionsdeployment oder Live-Cross-
User-Race wird behauptet. Fokussierte Runtime-Evidence wird erst berichtet,
nachdem die Ersatzbefehle gelaufen sind.

## Bekannte Einschränkungen

Framework/MRTS-Source, Gitlinks, Workflows, Scanner-Konfiguration, externer
Sonar-Issue-Status und `master` liegen außerhalb des Source-Scopes. Ein
Framework-abhängiger Test oder repositoryweiter Documentation-Target kann durch
den absichtlich nicht initialisierten Parent-gebundenen Framework-Checkout
blockiert bleiben; dieser Status wurde für das vollständige Collector-Modul
reproduziert und ist oben aufgezeichnet.

## Verbleibende Risiken

Der Ersatz bewahrt einen begrenzten ausgewählten Repair-Satz; er behauptet
nicht, das breitere aktuelle `ci/runtime`-SonarQube-Cloud-Inventar zu
eliminieren. Der frische Range-Secret-Scan, Exact-Head-Hosted-Checks, Review,
SonarQube-Cloud-Ergebnis und Mergeability bleiben unabhängige Delivery-Gates.

## Nicht ausgeführte Prüfungen mit Begründung

- Das vollständige Framework-abhängige Collector-Modul kann nicht importieren,
  bis der Parent-gebundene Framework-Checkout vorhanden ist; seine
  Initialisierung oder Änderung liegt außerhalb des autorisierten Parent-only
  Scopes.
- Die vollständige Connector-/Runtime-Matrix, Host-Vorbereitung,
  Paketinstallation, Generated-Report-Refresh, netzwerkgebundene Checks und
  ein Live-Cross-User-Race wurden nicht ausgeführt, weil sie den fokussierten
  Source-/Contract-Scope überschreiten.
- Hosted-Checks, Review, SonarQube Cloud, Pull-Request-Secret-Scanning und
  Integration erfordern den späteren exakten Ersatz-PR-Head und werden nicht
  lokal hergeleitet.

## Delivery-Status

Bei Erstellung basiert der frische lokale Branch auf
`30f7f58097d8b9659e27c64afde1c394c2f5f308`. Es werden kein gehosteter Check,
kein Review, keine SonarQube-Cloud-Analyse und keine Master-Integration des
Ersatz-PR behauptet. Vor einem geschützten Merge müssen finaler lokaler,
Remote- und PR-Head übereinstimmen; erforderliche Checks, frischer Range-Secret-
Scan, Review-Status, SonarQube-Cloud-Ergebnis und Mergeability müssen für genau
diesen Head beobachtet werden.

## Finaler Diff- und Review-Status

Der beabsichtigte Ersatz-Diff ist der final geprüfte Runtime-Root-Hardening-
und begrenzte Maintainability-Repair-Baum, der auf dem aktuellen `master`
rekonstruiert statt als historische Commits kopiert wurde. Er benötigt einen
frischen fokussierten Security-Review, lokale Regression-Evidence,
Dokumentationsvalidierung und Hosted-Exact-Head-Verifikation, bevor ein
Delivery-Anspruch erhoben werden kann.
