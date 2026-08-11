# Change Record

**Sprache:** [English](CR-20260811-trusted-nginx-broker-crs-placeholder-worker-directory-repair.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260811-trusted-nginx-broker-crs-placeholder-worker-directory-repair |
| Datum (UTC) | 2026-08-11 |
| Basis-Revision | `4749c02c6dd5e285c4309b4e69b0bb28ae459e48` |
| Findings | FND-PARENT-0120, FND-PARENT-0121 |
| Failure-Evidence | GitHub-Actions-Run `31421851336` |

## Motivation und Problemstellung

Diese Parent-only-Reparatur dokumentiert die enge Behandlung des gepinnten
Zero-Byte-CRS-Placeholders und der vom Worker beschreibbaren Broker-Runtime-
Verzeichnisse. Run `31421851336` ist ausschließlich Failure-Evidence; er
belegt kein Hosted-Lifecycle-Ergebnis.

## Akzeptanzkriterien

Der Broker-Vertrag bindet das exakte CRS-Repository, Release-Tag, Commit, den
Gitblob des leeren Placeholders und SHA-256, akzeptiert keine andere leere
CRS-Datei und bewahrt fail-closed-Metadaten- und Provenance-Prüfungen. Nur
Broker-erzeugte Logs-, State- und CRS-Audit-Verzeichnisse dürfen Root-Ownership,
die zugelassene Worker-Gruppe und exakt Modus `0730` verwenden. Die EN/DE-
Dokumente und Records nennen dieselben Fakten ohne Behauptungen zu Hosted, PR,
Runtime, Lifecycle, Evidence-Readback oder Cleanup-Erfolg.

## Implementierungsentscheidung und Begründung

Das CRS-Tupel bleibt `https://github.com/coreruleset/coreruleset.git`,
`v4.28.0` und `55b09f5acfd16413e7b31041100711ceb7adc89c`. Das einzige
zugelassene leere Leaf ist `plugins/empty-after.conf`, gebunden an Gitblob
`e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` und SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Nur Logs, State und das CRS-Audit-Verzeichnis sind root-owned, verwenden die
zugelassene Worker-GID, fordern exakt `0730` und nicht-symlinkende Pfade.
Andere Directory-Metadata- und Broker-Sicherheitskontrollen bleiben unverändert.

## Security-Auswirkung

Das benannte gepinnte Leaf ist keine allgemeine Ausnahme für leere Dateien.
Die Worker-Write-Erlaubnis fügt weder ein breites beschreibbares Verzeichnis
noch einen Caller-vorgegebenen Pfad, Command, Executable, Manifestfeld oder
Permission hinzu.

## Geänderte Dateien

- `ci/runtime/broker/nginx_root_broker.py`
- `tests/test_nginx_root_broker.py`
- `tests/test_nginx_root_broker_crs_profile.py`
- `docs/security/trusted-nginx-root-broker.md`
- `docs/security/trusted-nginx-root-broker.de.md`
- dieser Change Record und seine deutsche Begleitfassung

Framework-Source/Gitlink, MRTS und PR-#240-Produktänderungen sind außerhalb
des Scopes. Dieser Record wurde vor der Delivery verfasst. Der aktuelle User
autorisiert genau einen separaten Parent-Commit, Push und Draft-PR; jeder Merge,
einschließlich desjenigen von PR #240, bleibt außerhalb des Scopes.

## Tests und tatsächliche Ergebnisse

- In-Memory-Compile: bestanden.
- `tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile`:
  bestanden, 55 Tests in 11.750 Sekunden.
- `tests.test_nginx_root_broker_workflow tests.test_protected_nginx_broker_caller tests.test_ci_security_workflows tests.test_python_version_contract`:
  bestanden, 72 Tests in 1.384 Sekunden.
- `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract`:
  bestanden, 26 Tests plus validate-only actionlint/zizmor/gitleaks.
- Aggregierte Auswahl einschließlich Snapshot-Contract: 81 bestanden und 1
  Fehler, weil dem isolierten Worktree
  `modules/ModSecurity-test-Framework/ci/lib/common.sh` fehlt; dies wird nicht
  als Source-Regression dargestellt.

## Ausgeführte Befehle

Die oben genannten Testauswahlen und der CI-Security-Contract wurden mit den
genannten Ergebnissen ausgeführt. `git diff --check` bestand. Scopierte
Dokumentationsprüfungen werden nach ihrer Ausführung im finalen Review erfasst.

## Runtime-Evidence

Es gibt keine erfolgreiche Hosted-, PR-, Root-, Worker-, NGINX-, CRS-, Audit-,
Evidence-Readback-, Cleanup- oder Lifecycle-Evidence. Run `31421851336`
bleibt ausschließlich Failure-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

Direktes `py_compile` war blockiert, weil das Worktree kein `__pycache__`
erstellen kann. Direktes `check-python-version-contract.py --json` endet
sowohl auf clean base/master `4749c02c6dd5e285c4309b4e69b0bb28ae459e48` als
auch auf diesem Task-Diff mit Exit 1 wegen unabhängiger bestehender Workflow-
Inventory-Verletzungen; dies ist unveränderte Baseline-Evidence, kein
Reparaturergebnis. Kein Hosted-Workflow, keine Root-Action, kein NGINX-Start,
CRS-Fetch, Audit, Evidence-Readback, Cleanup, PR oder Delivery-Action wurde
ausgeführt.

## Bekannte Einschränkungen

Die Evidence besteht nur aus lokalen Source-/Static-Ergebnissen. Sie validiert
weder einen beschreibbaren Hosted-Runner noch GitHub-Actions-Kontext, echtes
Root-/Master-Worker-Verhalten oder einen geschützten resulting-master-Lifecycle.

## Verbleibende Risiken

Ein zukünftiger geschützter resulting-master-Run muss `no-crs` und
`owasp-crs`, Evidence-Readback und Cleanup unabhängig nachweisen. PR #240
wird durch diesen Record nicht entsperrt.

## Finaler Review-Status

Der scopierte Parity-Review für kritische Literale, Überschriften und
wechselseitige Links bestand; `git diff --check` bestand ebenfalls. `make
check-bilingual-docs` endete mit Exit 1, weil dem isolierten Worktree von
bereits vorhandenen Repository-Dokumenten referenzierte Framework-Pfade fehlen;
seine gemeldeten fehlenden Ziele liegen außerhalb der zugewiesenen Dateien und
dieser Parent-only-Reparatur. Es wird kein Delivery-Status behauptet.

## Finaler Diff- und Review-Status

Dieser Record ist auf die Parent-Reparatur auf Basis von
`4749c02c6dd5e285c4309b4e69b0bb28ae459e48` beschränkt; er behauptet keinen
Commit, veröffentlichten Head, PR, Hosted Check, Review, Lifecycle oder Merge.
