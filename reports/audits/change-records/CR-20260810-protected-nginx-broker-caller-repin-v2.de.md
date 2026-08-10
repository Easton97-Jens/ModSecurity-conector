# Change Record

**Sprache:** [English](CR-20260810-protected-nginx-broker-caller-repin-v2.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260810-protected-nginx-broker-caller-repin-v2 |
| Datum (UTC) | 2026-08-10 |
| Basis-Revision | 1df2fcbd0c764c52253348a29034ff9e9b1bf7e2 |
| Geschützter Broker-SHA | 1df2fcbd0c764c52253348a29034ff9e9b1bf7e2 |
| Broker-Framework-Gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |

## Motivation und Problemstellung

Der geschützte Caller wählte noch das vorherige unveränderliche Broker-/Framework-Tupel. Dieses Tupel kann die spätere, bereits als 1df2fcbd0c764c52253348a29034ff9e9b1bf7e2 gemergte Broker-Runtime-Snapshot-Reparatur nicht ausführen. Der Caller muss beide Reusable-Jobs, ihr Eingabetupel, seinen Manifest-/Evidence-Helper und die statischen Verträge an den exakten Broker-Commit und den exakten Modus-160000-Framework-Gitlink binden, die dieser Broker-Tree enthält.

## Akzeptanzkriterien

Beide festen Caller-Jobs verwenden denselben vollständigen unveränderlichen Broker-SHA, übergeben ihn als protected_broker_sha und übergeben Framework-SHA 03880bf66b3905940466ff10b3a431a27ecc6b26. Der Caller behält seinen dispatch-only-, kanonisches-Repository-, non-fork-, refs/heads/master- und contents: read-Vertrag. Er darf weder eine bewegliche Referenz, ein drittes Profil, Secret-Inheritance, Write-Permissions, Target-Checkout/-Ausführung, einen Root-Command, Framework-/MRTS-Source-Änderungen noch ein Parent-Gitlink-Update hinzufügen.

Der unveränderliche Broker muss den committed Phase-C-Caller-Blob für dieses Tupel akzeptieren und ein absichtlich falsches Tupel vor Artefakt-, Build-, Candidate- oder Root-Aktivität ablehnen. Die gepaarte Sicherheitsdokumentation und dieser Change Record müssen dieselben aktiven Literale in Englisch und Deutsch bewahren; ältere Records behalten ihr historisches Tupel.

## Technische Entscheidungen

Der Repin ist eine datenorientierte Parent-Caller-Änderung. Der neue Broker-SHA ist weder Branch noch Tag und kann nicht durch Caller-Eingaben gewählt werden. Der Framework-SHA kommt aus dem eigenen Gitlink des Broker-Trees und nicht aus einem späteren Parent-Stand. Die beiden Profilaufrufe bleiben explizit und symmetrisch, sodass weder Matrix, Profil, Pfad noch Command durch den Caller wählbar werden.

## Implementierungsentscheidung und Begründung

Die zwei uses-Werte, beide protected_broker_sha-Eingaben, beide framework_sha-Eingaben und die Lifecycle-Ergebnislabels nennen nun das neue Tupel. protected_nginx_broker_caller.py, der Python-Workflow-Version-Vertrag und die Caller-/Blob-Vertragstests verwenden dasselbe Paar. Parser, Schema, Root-Aktion, Permission, Trigger, Artefaktpfad und Cleanup-Verhalten ändern sich nicht.

Der englische/deutsche Trusted-Broker-Guide beschreibt den geschützten Snapshot-Vertrag jetzt als über diese Broker-Revision aktiv. Der Phase-B-Record und ältere Caller-Repin-Records sind historische Evidenz und werden absichtlich nicht umgeschrieben.

## Geänderte Dateien

- .github/workflows/run-protected-nginx-root-broker.yml
- ci/runtime/broker/protected_nginx_broker_caller.py
- ci/checks/common/check-python-version-contract.py
- tests/test_ci_security_workflows.py
- tests/test_nginx_root_broker.py
- docs/security/trusted-nginx-root-broker.md und docs/security/trusted-nginx-root-broker.de.md
- dieser Change Record und CR-20260810-protected-nginx-broker-caller-repin-v2.md

## Tests und tatsächliche Ergebnisse

Die fokussierte Parent-Caller-/Broker-/Security-/Snapshot-/Python-Contract-Suite bestand 120 Tests, nachdem das exakt gepinnte Framework-Gitlink nicht-rekursiv im task-eigenen Validierungs-Worktree materialisiert worden war. Der erste Lauf hatte einen rein umgebungsbedingten Fehler, weil diesem Worktree absichtlich modules/ModSecurity-test-Framework/ci/lib/common.sh fehlte; der gezielte Test und der vollständige Wiederholungslauf bestanden nach Checkout von exakt 03880bf66b3905940466ff10b3a431a27ecc6b26. Verschachteltes MRTS blieb uninitialisiert und unverändert.

## Ausgeführte Befehle

- PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-owned external directory> <Parent .venv>/bin/python -m unittest -v tests.test_protected_nginx_broker_caller tests.test_nginx_root_broker tests.test_nginx_root_broker_workflow tests.test_nginx_root_broker_crs_profile tests.test_ci_security_workflows tests.test_runtime_env_snapshot_contract tests.test_python_version_contract — PASS, 120 Tests nach exakter Framework-Materialisierung; der vorherige Versuch ist oben als rein umgebungsbedingt erfasst.
- PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-owned external directory> <Parent .venv>/bin/python -m py_compile ci/runtime/broker/protected_nginx_broker_caller.py ci/checks/common/check-python-version-contract.py tests/test_ci_security_workflows.py tests/test_nginx_root_broker.py — PASS.
- PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-owned external directory> make PYTHON=<Parent .venv>/bin/python check-ci-security-contract — PASS, 26 Workflow-Security-Tests plus read-only Tool-Lock-Validierung.
- PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-owned external directory> make PYTHON=<Parent .venv>/bin/python check-python-version-contract — BLOCKED, Exit 2 wegen bestehender unveränderter Workflow-Inventarfehler. Die Ausgabe nennt keine Verletzung für run-protected-nginx-root-broker.yml; dieser Repin maskiert oder repariert diese separate Baseline nicht.
- actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml — PASS mit actionlint 1.7.12 und ShellCheck 0.11.0.
- zizmor --offline .github/workflows — PASS, keine Findings; 94 bestehende Suppressions wurden gemeldet.
- make PYTHON=<Parent .venv>/bin/python check-bilingual-docs — PASS.
- make PYTHON=<Parent .venv>/bin/python check-doc-links — PASS.
- git diff --check — PASS.

## Security-Auswirkung

Die betroffene Grenze ist die Deklaration des unveränderlichen privilegierten Reusable-Workflows. Caller-kontrollierte Dispatch-Daten bleiben deklarativ, und der Caller erhält keine Autorität zur Auswahl von Broker-Source, Framework-Source, Root-Aktion, Manifestpfad, Executable, Profil, Permission oder Secret. Bestehende negative Verträge lehnen weiterhin bewegliche/lokale Referenzen, falsche oder gemischte Tupelwerte, doppelte YAML-/Input-Werte, geschwächte Master-Gates, PR-/Fork-Kontexte, Write-Permissions, Secrets, sudo, Target-Ausführung, unsichere Artefakte und Maskierung fehlgeschlagener Ergebnisse ab.

## Runtime-Evidence

Für diesen Kandidaten lief kein resultierender-master-geschützter Lifecycle. Der frühere Phase-C-Versuch 31328046595 bleibt ein fail-closed Fehler vor Root und ist keine Evidenz für den reparierten Broker. Ein neuer master-only Dispatch muss beide No-CRS- und OWASP-CRS-Profile, Identity-Bindings, Root-Master- und Non-Root-Worker-Verhalten, CRS-/Audit-Evidence, Evidence-Readback, Stop und Cleanup erst separat beweisen, nachdem dieser Caller-Repin-PR normal gemergt wurde.

## Bekannte Einschränkungen

Das lokale Parent-Virtualenv stellt CPython 3.14.4 bereit, während .python-version CPython 3.14.6 verlangt. Lokale Ergebnisse sind daher Source-/Static-Evidence und keine CI-äquivalente Interpreter-Evidence. Das exakte Framework-Submodule wurde nur für einen Parent-Contract-Test materialisiert; weder Framework- noch MRTS-Source, Branch, Gitlink, Commit, Push oder PR wurden geändert.

## Verbleibende Risiken

Jedes PR-spezifische Review-, Branch-Protection-, CodeQL-, SonarQube-Cloud- oder resultierender-master-Lifecycle-Problem blockiert die Delivery. Dieser Record autorisiert weder eine bewegliche Ref, direkten Master-Push, History-Rewrite, Check-Bypass, automatischen Merge, Framework-/MRTS-Modifikation, Phase-D-Dispatch, FND-PARENT-0113-Schließung noch die Fortsetzung von PR #240.

## Nicht ausgeführte Prüfungen mit Begründung

Der resultierende-master-Lifecycle, Root-Admission, NGINX-Start, Worker-Proof, CRS-Netzwerk-Fetch, Audit-Evidence, Artefakttransport, Evidence-Readback und Cleanup sind keine lokalen Prüfungen. Sie benötigen den späteren geschützten GitHub-hosted-Workflow nach Exact-Head-PR-Validierung und Master-Integration. Hosted GitHub Actions, CodeQL, SonarQube Cloud, Review- und Branch-Protection-Evidence bleiben für den finalen PR-Head unbestätigt.

## Finaler Review-Status

Dieser Record hält die lokale Pre-Commit-Validierung und die anfängliche normale Veröffentlichung fest. Der Draft-Parent-PR [#270](https://github.com/Easton97-Jens/ModSecurity-conector/pull/270) wurde von `fix/ci-repin-nginx-broker-runtime-snapshot` nach `master` mit initialem Head `5e290bb228a47331a53038da258970b6d792ed2f` eröffnet; er ist nicht review-bereit und hat keinen Auto-Merge-Request. Die Committed-Blob-Validierung bestand; Hosted Exact-Head-, Review-, Branch-Protection-, Merge- und Lifecycle-Evidence bleiben Delivery-Gates. Dafür wird keine Erfolgsbehauptung getroffen.

## Finaler Diff- und Review-Status

Der Diff dieses Records ist auf die neun Parent-Pfade oben begrenzt. Er bewahrt das bestehende Parent-Framework-Gitlink 03880bf66b3905940466ff10b3a431a27ecc6b26 und nimmt keine MRTS-Änderung vor. Historische Referenzen auf das vorherige Tupel bleiben nur in älteren Change Records als historische Evidenz.
