# Change Record

**Sprache:** [English](CR-20260811-protected-nginx-broker-caller-repin-v5.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260811-protected-nginx-broker-caller-repin-v5 |
| Datum (UTC) | 2026-08-11 |
| Basis-Revision | `49c40779a7b6de9f699391bcd524ea069787df42` |
| Vorheriger geschützter Broker-SHA | `7a9240d35e50475cc1a381fa103b0bb5cca2bee3` |
| Aktiver geschützter Broker-SHA | `49c40779a7b6de9f699391bcd524ea069787df42` |
| Broker-Framework-Gitlink | `03880bf66b3905940466ff10b3a431a27ecc6b26` |
| Zugehörige Findings | FND-PARENT-0120, FND-PARENT-0121 |

## Motivation und Problemstellung

PR #275 mergte Broker-Commit `49c40779a7b6de9f699391bcd524ea069787df42`,
der die enge FND-PARENT-0120/FND-PARENT-0121-Reparatur enthält. Der aktuelle
geschützte Caller wählte weiterhin den vorherigen Broker-Commit
`7a9240d35e50475cc1a381fa103b0bb5cca2bee3`. Diese getrennte Parent-only-
Änderung repinnt den Caller auf die verfügbare unveränderliche Broker-Revision,
bevor irgendein neuer geschützter resulting-master-Lifecycle betrachtet wird.

## Akzeptanzkriterien

Beide benannten Caller-Jobs verwenden denselben vollständigen unveränderlichen
`uses`-SHA und passenden `protected_broker_sha`; beide `framework_sha`-Inputs
entsprechen dem mode-`160000`-Gitlink, der durch Broker
`49c40779a7b6de9f699391bcd524ea069787df42` aufgezeichnet ist. Helper,
Manifest-/Evidence-Validierung, Result-Summary, statische Contract-Tests und
die gepaarten Guides verwenden dasselbe Tupel. Keine Permission, kein Trigger,
kein Gate, Profil, Schema, Root-Command, Framework-Gitlink, Framework-/MRTS-
Source, APR-util oder PR-#240-Produktänderung ist enthalten.

## Implementierungsentscheidung und Begründung

Der Framework-Wert wurde ausschließlich aus dem Parent-Gitobjekt abgeleitet:
`git ls-tree 49c40779a7b6de9f699391bcd524ea069787df42 -- modules/ModSecurity-test-Framework`
lieferte mode `160000` und Commit
`03880bf66b3905940466ff10b3a431a27ecc6b26`. Die Caller-Änderungen betreffen
nur das unveränderliche Auswahl-Tupel; sie ermöglichen weder einen mutable Ref,
einen Caller-ausgewählten Codepfad noch eine neue privilegierte Fähigkeit.
Historische Change Records bleiben unverändert.

## Security-Auswirkung

Die unveränderliche Caller-zu-Broker-Auswahl bleibt fail-closed. Statische Tests
weisen weiterhin mutable Refs, nicht passende Tupel-Inputs, veränderte Job-
Gates, zusätzliche Jobs oder Inputs, erhöhte Permissions, geerbte Secrets und
die Nutzung nicht vertrauenswürdigen Caller-Codes an der Root-Grenze ab. Dieser
Record ist keine geschützte Lifecycle-Evidence.

## Geänderte Dateien

- `.github/workflows/run-protected-nginx-root-broker.yml`
- `ci/runtime/broker/protected_nginx_broker_caller.py`
- `ci/checks/common/check-python-version-contract.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_nginx_root_broker.py`
- `docs/security/trusted-nginx-root-broker.md`
- `docs/security/trusted-nginx-root-broker.de.md`
- dieser Change Record und seine deutsche Begleitfassung

Framework-Source/Gitlink, MRTS, Framework-PR #74, APR-util-Remediation sowie
PR-#240-Änderungen oder -Merge sind außerhalb des Scopes.

## Tests und tatsächliche Ergebnisse

- Die fokussierte Parent-Caller-/Broker-Suite bestand: 127 Tests in 11.605 Sekunden.
- Die breitere ausgewählte Suite führte 137 Tests aus; 136 bestanden und einer
  schlug fehl, weil dem isolierten Worktree das bestehende Framework-Gitlink-
  Ziel `modules/ModSecurity-test-Framework/ci/lib/common.sh` fehlt. Die
  fehlschlagende Snapshot-Integration ist kein Repin-Source-Fehler und es
  wurde keine Framework-Materialisierung vorgenommen.
- `make check-ci-security-contract` bestand: 26 Tests plus validate-only
  actionlint-, zizmor- und gitleaks-Lock-Prüfungen.
- Der checksum-verifizierte actionlint `1.7.12`-Lauf mit ShellCheck bestand.
- Der checksum-verifizierte zizmor-`1.29.0`-Offline-Workflow-Scan bestand;
  beide sicheren Fixtures bestanden und beide unsicheren Fixtures wurden wie
  erwartet abgewiesen.
- Die In-Memory-Syntax-Kompilierung der vier geänderten Python-Dateien bestand.

## Ausgeführte Befehle

- `PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 "$PARENT_PYTHON" -m unittest -v tests.test_protected_nginx_broker_caller tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile tests.test_nginx_root_broker_workflow tests.test_ci_security_workflows tests.test_python_version_contract` — PASS, 127 Tests.
- `make PYTHON="$PARENT_PYTHON" check-ci-security-contract` — PASS.
- `actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml ci/fixtures/workflow-permission-contract/*.yml` — PASS mit der checksum-verifizierten task-lokalen `1.7.12`-Binary.
- `zizmor --offline .github/workflows` — PASS mit der checksum-verifizierten task-lokalen `1.29.0`-Binary; sichere Fixtures bestanden und die unsicheren Fixtures lieferten die erwartete Nonzero-Abweisung.
- `make PYTHON="$PARENT_PYTHON" check-python-version-contract` — Exit 2 wegen bestehender unabhängiger Workflow-Inventory-Verletzungen; es wurde keine geschützte Caller-Tupelverletzung gemeldet.

`$PARENT_PYTHON` bezeichnet den policy-ausgewählten Parent-
Virtual-Environment-Interpreter. Seine lokal verfügbare Version war `3.14.4`;
`.python-version` erklärt CI-Lane `3.14.6`.

## Runtime-Evidence

Zum Zeitpunkt dieses Records hat kein neuer geschützter Workflow-Dispatch,
keine Root-Action, kein NGINX-Start, CRS-Fetch, Evidence-Readback,
Prozess-/Socket-/PID-/Listener-Cleanup, Pull-Request-Check oder Merge
stattgefunden. Die früheren Fehlschläge bleiben ausschließlich historische
Failure-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

Hosted-Pull-Request-Checks, CodeQL, SonarQube Cloud, Review-/Conversation-
Auflösung, SHA-gebundener Squash-Merge, resulting-master-Checks und der
geschützte No-CRS-/OWASP-CRS-Lifecycle warten auf den getrennten autorisierten
Draft-PR und seinen exakten finalen Head. Keine lokale Root-Runtime ersetzt
diese. Die breiten Dokumentationsprüfungen sind in diesem isolierten Worktree
durch bestehende fehlende Framework-Gitlink-Ziele blockiert; die gepaarten
geänderten Dokumente erhalten einen fokussierten Parity- und Link-Review.

## Bekannte Einschränkungen

Die ausgewählte lokale Parent-venv ist `3.14.4`, nicht die erklärte CI-Lane
`3.14.6`. Sie ist nützliche lokale Test-Evidence, ersetzt aber keine exakte
Hosted-Python-Lane-Evidence. Der isolierte Worktree materialisiert den
Framework-Gitlink absichtlich nicht, daher kann die eine breite Snapshot-
Integration hier nicht laufen.

## Verbleibende Risiken

FND-PARENT-0120 und FND-PARENT-0121 bleiben unverified, bis ein erfolgreicher
resulting-master-Lifecycle beide Profile, Evidence-Readback und Prozess-/
Socket-/PID-/Listener-Cleanup belegt. Der APR-util-HTTP-404 bleibt ein
getrennter Framework-owned Blocker; PR #240 bleibt auch bei später erfolgreichem
Caller-Lifecycle merge-blocked.

## Finaler Review-Status

Pre-Commit-Scope- und Security-Review warten auf die finale Diff-Validierung.
Dieser Record behauptet keinen Commit, Push, Pull Request, Hosted-Check,
Review, Merge oder Runtime-Erfolg.

## Finaler Diff- und Review-Status

Der beabsichtigte Scope sind die neun oben gelisteten Dateien. Die finale
Validierung des exakten committen Caller-Blobs, PR-Head-Checks und der
resulting-master-Lifecycle stehen noch aus.
