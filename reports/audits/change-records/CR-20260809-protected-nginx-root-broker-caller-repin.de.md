# Change Record

**Sprache:** [English](CR-20260809-protected-nginx-root-broker-caller-repin.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260809-protected-nginx-root-broker-caller-repin |
| Datum (UTC) | 2026-08-09 |
| Basis-Revision | c2836f74510b9f72bae466d8b7d92a3f9f38c007 |

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
ohne ein breites Präfix wieder her.

Es werden weder Branch, Tag, master-Referenz, lokaler Reusable-Pfad,
vom Caller gewählte Broker-Source, OIDC-Berechtigung, Write-Berechtigung,
Secret noch ein Root-Ausführungspfad hinzugefügt.

## Geänderte Dateien

- .github/workflows/run-protected-nginx-root-broker.yml
- .github/workflows/update-workflow-tools.yml
- ci/tools/update-workflow-tools.py
- ci/runtime/broker/protected_nginx_broker_caller.py
- ci/checks/common/check-python-version-contract.py
- tests/test_ci_security_workflows.py und tests/test_nginx_root_broker.py
- docs/security/trusted-nginx-root-broker.de.md und das englische Gegenstück
- dieser Change Record und sein englisches Gegenstück

## Ausgeführte Befehle

Die exakte Phase-B-Basis, der Broker-SHA und der Framework-Gitlink wurden aus
dem resultierenden Protected-master-Tree geprüft. Vor dem späteren
`origin/master`-Sync wurden mit dem verfügbaren Parent-Virtual-Environment-
Python `3.14.4` folgende Source-/Static-Validierungen beobachtet:

- `PYTHONDONTWRITEBYTECODE=1 <Parent .venv>/bin/python -m unittest -v tests.test_nginx_root_broker tests.test_nginx_root_broker_workflow tests.test_protected_nginx_broker_caller tests.test_ci_security_workflows tests.test_python_version_contract tests.ci_security.test_update_workflow_tools tests.security_regression.test_workflow_security_contract` — PASS, 133 Tests.
- `make PYTHON=<Parent .venv>/bin/python check-ci-security-contract` — PASS,
  26 Tests plus read-only actionlint-, zizmor- und gitleaks-Lock-Validierung.
- `actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml` — PASS.
- `zizmor --offline .github/workflows` — PASS, keine Befunde.
- `git diff --check c2836f74510b9f72bae466d8b7d92a3f9f38c007` — PASS.

Die ursprüngliche endliche-allowlist-Reproduktion schlug vor der
Zwei-Pfad-Reparatur fehl; danach bestand die fokussierte
Updater-/Security-Contract-Suite mit dem legitimen Negative-Control für
unzulässige Workflows. Der finale Phase-B-Range, die Validierung und das
Security-Diff-Review müssen nach dem normalen `origin/master`-Sync erneut
ausgeführt werden. Es wird kein Runtime-Lifecycle-Ergebnis beansprucht.

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
`test-apache.yml`, `test-haproxy.yml` und `update-workflow-tools.yml`
blockiert; es meldet keine Caller-Repin-spezifische Verletzung. Der
repository-weite Bilingual-Checker und die breite 897-Test-Unit-Discovery sind
durch das absichtlich nicht initialisierte Framework-Submodule in diesem
Task-Worktree blockiert; die Framework-Policy verbietet automatische
Initialisierung. Der Post-Merge-Lifecycle ist absichtlich erst ausführbar,
nachdem der separate Caller-Repin die Current-Head-Gates bestanden hat und
normal gemergt ist. Hosted-Checks, CodeQL, SonarQube Cloud, Review- und
Branch-Protection-Ergebnisse müssen für den späteren PR-Head frisch beobachtet
werden.

## Finaler Diff- und Review-Status

Dies ist ein uncommitteter lokaler Phase-B-Candidate auf Grundlage der
Protected-master-Revision c2836f74510b9f72bae466d8b7d92a3f9f38c007. Während
des Reviews wurde ein neuerer `origin/master` entdeckt, der vor der
Auslieferung normal integriert werden muss; danach werden finale Basis, Range
und Validierungsergebnisse dieses Records abgeglichen. Er beansprucht nicht,
dass ein Push, Pull Request, Merge, Hosted Check oder Lifecycle bereits
abgeschlossen ist. Der finale Range darf nur Parent-eigene Caller-, Contract-,
Test-, Dokumentations- und Record-Änderungen enthalten; er darf keine
Framework- oder MRTS-Source- oder Gitlink-Änderung enthalten.
