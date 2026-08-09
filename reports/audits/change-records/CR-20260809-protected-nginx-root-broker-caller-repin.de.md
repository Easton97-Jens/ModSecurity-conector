# Change Record

**Sprache:** [English](CR-20260809-protected-nginx-root-broker-caller-repin.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260809-protected-nginx-root-broker-caller-repin |
| Datum (UTC) | 2026-08-09 |
| Basis-Revision | b71da9803484dacce7d3349ffdff4d1ccdcfe4d6 |

## Motivation und Problemstellung

Der geschützte Caller muss den reparierten wiederverwendbaren NGINX-Root-Broker
über dessen unveränderlichen resultierenden Protected-master-Merge-Commit
auswählen und nicht über den früheren Broker-Commit. Der getrennte Repin ist
nötig, weil ein Squash-Merge das Phase-A-Ergebnis während der Review der
Broker-Reparatur noch nicht verfügbar macht.

Die resultierende Broker-Revision ist
c2836f74510b9f72bae466d8b7d92a3f9f38c007. Ihr exakter Parent-Tree enthält den
Framework-Gitlink 4c9af1cee72caa0107fa011e59eef9e853338cf5 mit Modus 160000.
Die früheren Werte e06254ea9622d214a9030b9ba786756560ace417 und
c71e15db7b7517b237add9fa09b3493e7bc93627 bleiben historische Evidence für den
fehlgeschlagenen Lauf 31310183097 und sind keine ausführbaren Caller-Policy-Pins.

## Akzeptanzkriterien

Beide geschützten Caller-Jobs verwenden denselben literalen unveränderlichen
Broker-SHA in ihrer Reusable-Workflow-Referenz und ihrem Input
protected_broker_sha. Beide verwenden den Framework-Gitlink, den dieser
Broker-Commit aufzeichnet. Manifest-Helper, Evidence-Readback,
Python-Workflow-Vertrag, Workflow-Security-Tests, Broker-Tests und die
gepaarte Sicherheitsdokumentation führen dasselbe kanonische Tupel.

Der Caller bleibt master-only, dispatch-only, read-only, unprivilegiert und
datenorientiert. Dieser Repin ändert weder Broker-Logik, Berechtigungen,
Root-Aktionen, Manifest-Schema, Profilregeln, Framework-Source, MRTS-Source
noch einen Gitlink.

## Implementierungsentscheidung und Begründung

Die Revision ist ein separater Parent-only-Caller-PR. Die wiederverwendbare
Broker-Revision ist über Protected-master erreichbar; ihre Framework-Revision
wird aus ihrem exakten Git-Tree abgeleitet und nicht vom alten Pin kopiert.
Konstanten und Regressionsfixtures werden gemeinsam aktualisiert, sodass ein
gemischtes Broker-, Manifest-, Evidence- oder Framework-Tupel im bestehenden
Vertrag fehlschlägt, statt einen beweglichen Ref auszuwählen.
Der eingeschränkte Workflow-Tool-Publisher erhält den Caller als einen exakten
geprüften Pfad sowohl in seiner Source-Allowlist als auch in seiner passenden
Staging-Liste; dies stellt vollständige zentral gesperrte Action-Pin-Coverage
ohne ein breites Präfix wieder her. Dieselbe endliche Pfadkorrektur ist bereits
in der normal integrierten Basis
`b71da9803484dacce7d3349ffdff4d1ccdcfe4d6` enthalten; sie ist damit
Current-master-Control-Evidence und keine nur branch-spezifische Dateiänderung
dieses Repin-Range.

Es werden weder Branch, Tag, master-Referenz, lokaler Reusable-Pfad,
vom Caller gewählte Broker-Source, OIDC-Berechtigung, Write-Berechtigung,
Secret noch ein Root-Ausführungspfad hinzugefügt.

## Geänderte Dateien

- .github/workflows/run-protected-nginx-root-broker.yml
- ci/runtime/broker/protected_nginx_broker_caller.py
- ci/checks/common/check-python-version-contract.py
- tests/test_ci_security_workflows.py und tests/test_nginx_root_broker.py
- docs/security/trusted-nginx-root-broker.de.md und das englische Gegenstück
- dieser Change Record und sein englisches Gegenstück

## Ausgeführte Befehle

Der exakte Broker-SHA und der Framework-Gitlink wurden aus dem resultierenden
Protected-master-Tree geprüft. Der Branch mergte danach die aktuelle
geschützte `origin/master`-Revision
`cabf949553f40ef93c4d4add0bbca0f03372a259` normal und erzeugte dabei den
Post-Sync-Commit `5efc5187cbb4f68ded484656d060e7c7847a52e2`. Auf diesem
Post-Sync-Head wurden mit dem verfügbaren Parent-Virtual-Environment-Python
`3.14.4` folgende Source-/Static-Validierungen beobachtet:

- `PYTHONDONTWRITEBYTECODE=1 <Parent .venv>/bin/python -m unittest -v tests.test_nginx_root_broker tests.test_nginx_root_broker_workflow tests.test_protected_nginx_broker_caller tests.test_ci_security_workflows tests.test_python_version_contract tests.ci_security.test_update_workflow_tools tests.security_regression.test_workflow_security_contract` — PASS, 133 Tests.
- `make PYTHON=<Parent .venv>/bin/python check-ci-security-contract` — PASS,
  26 Tests plus read-only actionlint-, zizmor- und gitleaks-Lock-Validierung.
- `actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml` — PASS.
- `zizmor --offline .github/workflows` — PASS, keine Befunde.
- `python -I ci/runtime/broker/nginx_root_broker.py validate-caller-workflow --caller-sha 5efc5187cbb4f68ded484656d060e7c7847a52e2 --broker-sha c2836f74510b9f72bae466d8b7d92a3f9f38c007 --framework-sha 4c9af1cee72caa0107fa011e59eef9e853338cf5` — PASS; der Caller wurde aus seinem unveränderlichen committed Git-Blob gelesen.
- `git diff --check origin/master...HEAD` — PASS.

Die ursprüngliche endliche-allowlist-Reproduktion schlug vor der
Zwei-Pfad-Reparatur fehl; danach bestand die fokussierte
Updater-/Security-Contract-Suite mit dem legitimen Negative-Control für
unzulässige Workflows. Der eingehende master enthält bereits dieselbe
Zwei-Pfad-Korrektur. `make check-python-version-contract` schlug auf diesem
Branch und auf clean master mit denselben unveränderten Inventory-/Shape-
Diagnosen fehl; die Fehler nennen `verified-report-governance.yml`,
`ci-security-codeql.yml`, `test-apache.yml`, `test-haproxy.yml` und
`update-workflow-tools.yml`, nicht eine Caller-Repin-Datei. Der
repository-weite Bilingual-Target schlägt ebenso nur wegen fehlender
Framework-Submodule-Link-Targets fehl. Es wird kein Runtime-Lifecycle-Ergebnis
beansprucht.

Nach der späteren normalen Synchronisierung mit
`b71da9803484dacce7d3349ffdff4d1ccdcfe4d6` und dem Merge-Commit
`0f2605eeda78aaa80a895d91ab0baa71c7c12852` bestanden dieselbe fokussierte
133-Test-Suite, der 26-Test-CI-Security-Contract, actionlint mit ShellCheck,
offline zizmor, der Immutable-Blob-Caller-Validator und die gezielte EN/DE-
Pair-Prüfung erneut. Die globalen Python-Version- und repository-weiten
Bilingual-Targets behalten die oben aufgezeichneten identischen
Current-master-/Umgebungsblocker.

## Security-Auswirkung

Die unveränderliche Caller-zu-Broker-Bindung bleibt fail-closed. Deklarative
Caller-Inputs und Manifeste müssen mit dem gepinnten Broker- und
Framework-Tupel übereinstimmen, bevor der wiederverwendbare Broker Artefakte
admitten oder bestehende privilegierte Aktionen erreichen kann. Das Update
erweitert weder die vertrauenswürdige Source-Menge noch erlaubt es Caller- oder
PR-Code als root auszuführen.

## Runtime-Evidence

Noch wurde kein Post-Repin-Protected-master-Lifecycle beobachtet. Sobald dieser
getrennte Caller-PR normal gemergt ist, muss ein manueller
Protected-master-Dispatch beide no-crs- und with-crs-Profile, Broker-Binding,
Root- und Worker-Identität, gegebenenfalls CRS- und Audit-Evidence,
Evidence-Readback, Stop und Cleanup beweisen. Diese resulting-master-Evidence
ist erforderlich, bevor PR #240 fortgesetzt wird.

## Bekannte Einschränkungen

Dieser Record ersetzt weder GitHub-Hosted-Checks noch SonarQube Cloud oder die
privilegierte Runtime. Lokale Source- und Contract-Validierung kann weder den
GitHub-Reusable-Workflow-Kontext noch Artefakttransport, Runner-sudo-Verhalten
oder den vollständigen NGINX- und CRS-Lifecycle beweisen. Das verfügbare
Python `3.14.4` ist ein repository-erlaubter Source-/Static-Fallback, nicht
die konfigurierte CPython-`3.14.6`-CI-Baseline.

## Verbleibende Risiken

Ein Phase-B-Qualitäts-, Security-, Review- oder Branch-Protection-Fehler
blockiert den Caller-PR. Ein resulting-master-Lifecycle- oder
Evidence-Readback-Fehler blockiert die Verifikation von FND-PARENT-0113 und
die Fortsetzung von PR #240. Kein Ergebnis autorisiert einen beweglichen Ref,
eine direkte master-Änderung, einen Bypass oder synthetischen PASS.

## Nicht ausgeführte Prüfungen mit Begründung

`make check-python-version-contract` ist durch unveränderte Current-Master-
Workflow-Inventar-/Shape-Verletzungen in `verified-report-governance.yml`,
`ci-security-codeql.yml`, `test-apache.yml`, `test-haproxy.yml` und
`update-workflow-tools.yml` blockiert; clean master meldet identische
Diagnosen. Der repository-weite Bilingual-Checker und die exakte-Head-breite
Unit-Discovery sind durch das absichtlich nicht initialisierte
Framework-Submodule in diesem Task-Worktree blockiert; die Framework-Policy
verbietet automatische Initialisierung. Der Post-Merge-Lifecycle ist
absichtlich erst ausführbar, nachdem der separate Caller-Repin die
Current-Head-Gates bestanden hat und normal gemergt ist. Hosted-Checks,
CodeQL, SonarQube Cloud, Review- und Branch-Protection-Ergebnisse müssen für
den späteren PR-Head frisch beobachtet werden.

## Finaler Diff- und Review-Status

Dieser lokale Phase-B-Candidate ist normal mit der Protected-master-Revision
b71da9803484dacce7d3349ffdff4d1ccdcfe4d6 nach dem späteren normalen
Merge-Commit `0f2605eeda78aaa80a895d91ab0baa71c7c12852` synchronisiert.
Exact-Head-Validierung und ein erneuertes finales Security-Diff-Review bleiben
vor der Auslieferung erforderlich. Er beansprucht nicht, dass ein Push, Pull
Request, Merge, Hosted Check oder Lifecycle bereits abgeschlossen ist. Der
finale Range enthält nur Parent-eigene Caller-, Contract-, Test-,
Dokumentations- und Record-Änderungen; er enthält keine Framework- oder
MRTS-Source- oder Gitlink-Änderung.
