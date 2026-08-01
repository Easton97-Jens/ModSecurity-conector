# FND-FRAMEWORK-0033 — Framework-Python-Wartungsvertrag erlaubt künftige Token- und Secret-Exposition außerhalb seines überprüften Publisher-Inputs

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0033 |
| Kategorie | security_hardening |
| Repository / Ownership | framework / framework |
| Priorität / Severity | P2 / low |
| Konfidenz / Status | validated / fixed |
| Feasibility | feasible_now |
| Release-Blocker | nein |
| Sicherheitsrelevant | ja |

## Zusammenfassung, betroffener Pfad und Auswirkung

Vor der Remediation war der nicht commitete CPython-3.13-Wartungsworkflow als
Ganzes von der generischen GitHub-Token-Referenzregel ausgenommen. Seine
wartungsspezifische Prüfung suchte nur nach dem Literal `github.token` in
`resolve` und `candidate-validate` und prüfte `publish` nicht. Eine zukünftige
Workflow-Änderung könnte daher `${{ github['token'] }}`,
`${{ secrets.GITHUB_TOKEN }}`, einen anderen `${{ secrets.* }}`-Ausdruck oder
eine Token-Referenz in einer Publisher-Shell oder -Action verwenden, ohne dass
der lokale CI-Security-Contract sie zurückweist.

Die Quelle ist eine vorgeschlagene Änderung an
`.github/workflows/check-python-version.yml`; mögliche Senken sind ein
Action- oder Bash-Kontext in einem Reader-Job oder der schreibfähige Publisher.
Der aktuelle Quelltext enthält keine dieser unsicheren Referenzen: Das einzige
explizite Token ist der überprüfte Input
`create-pull-request.with.token: ${{ github.token }}`. Die Veröffentlichung
ist nur per Schedule/Manual zulässig und auf Default-Branch/Repository
eingeschränkt. Es handelt sich daher um ein P2/low-Härtungsfinding für künftige
Regressionen, nicht um eine aktuelle Offenlegung, untrusted-PR-Ausführung oder
ein Finding mit breiterem Repository-Write.

`actions/checkout` kann intern GitHubs automatisches Job-Token mit
read-Scopes verwenden. Dieses gehostete Default ist etwas anderes als eine
explizite YAML-Secret-Deklaration; der Workflow behält für Reader
`contents: read` und `persist-credentials: false`, damit Credentials nicht für
nachfolgende Git-Kommandos persistiert werden.

## Evidenz und Reproduktion

Aufbewahrte Evidenz:

- Run-ID: `20260720T180337Z-framework-python-313-updater-f3349a7e`
- Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260720T180337Z-framework-python-313-updater-f3349a7e/analysis/codex-security-scans/ModSecurity-test-Framework/9dab40c2_20260720T185431Z/05_findings/FND-FRAMEWORK-0033-pre-fix-validation.md`
- SHA-256: `8a0a0cb5ac7fa15a76de01c5210d596bc2ceac1933e40380eb6d49869bb71495`
- Befehl: RTK-umhüllte fokussierte Python-Version- und CI-Security-Contract-Testmodule
- Arbeitsverzeichnis: `/var/tmp/codex/ModSecurity-test-Framework/worktrees/framework-python-updater`
- Exit-Code: `1` (beabsichtigte Pre-fix-Regression)
- Beobachtet um: `2026-07-20T19:12:21Z`
- Retention: `retained_task_evidence`

Der Test kopierte den geparsten Workflow, setzte den literalen nicht geheimen
Testausdruck `${{ secrets.GITHUB_TOKEN }}` in `resolve.env` und erwartete eine
Zurückweisung durch `python_version_maintenance_errors`. Vor der Remediation
gab der Checker keinen Fehler zurück. Der aufbewahrte Run bewies auch die
unabhängige Basename-only-Exception des Kandidatenworkflows; diese
verschachtelte Konfiguration wird von GitHub Actions nicht ausgeführt, aber in
derselben engen Änderung repariert.

Es wurde kein echtes Secret erzeugt, offengelegt oder aufbewahrt. Eine
bösartige Änderung müsste weiterhin auf den vertrauenswürdigen Branch
akzeptiert werden; die Evidenz behauptet keinen aktuellen Exploit.

## Root Cause, Remediation und Akzeptanzkriterien

Eine file-weite Allow-List wurde genutzt, obwohl eine geparste,
ortsgebundene Ausnahme nötig war. Der Spezialmatcher ließ indexiertes
`github['token']`, `secrets.*`- und Shell-`${GITHUB_TOKEN}`-Formen aus und
prüfte Publisher-Felder außerhalb der create-pull-request-Token-Option nicht.

Die Reparatur erkennt rekursiv `github.token`, `github['token']`,
`secrets.<name>`, geklammerte `secrets[...]`- und Shell-
`${GITHUB_TOKEN}`-Formen. Sie weist jede explizite Referenz in `resolve` und
`candidate-validate` zurück. In `publish` erlaubt sie nur den `with.token`-
Skalar `${{ github.token }}` der eindeutigen überprüften
`peter-evans/create-pull-request`-Action. Fokussierte Mutationen weisen
Reader-Env/with/uses/run-Referenzen, Publisher-Shell/Env/nicht freigegebene
Action-Referenzen und eine zweite PR-Erzeugungs-Action zurück; der aktuelle
legitime Workflow bleibt akzeptiert.

## Validierungsevidenz, Abhängigkeiten, Blocker und Restrisiko

Die fokussierte Mutationssuite, die Python-Version- und CI-Security-Contract-
Suiten, vollständiges Framework-Lint, Dokumentations-/Change-Record-Prüfungen,
`git diff --check` und ein versiegelter vollständiger Security-Diff-Review
bestanden. Der Scan-Report ist am Evidenzpfad im JSON-Record mit SHA-256
`f4c1ec2c78aeb33745fada8f1a9795cc5eba576e11be1f1cc24130ee9e4de56a` und
null reportable Findings aufbewahrt. Der Bypass-Review deckt punkt- und
indexierte GitHub-Token-Syntax, generische und geklammerte Secrets, Shell-
`${GITHUB_TOKEN}`, Publisher-Positionen und doppelte PR-Actions ab. Es gibt
keine externe Abhängigkeit, keinen Blocker und kein Duplikat.

Die lokale Reparatur ist fixed, aber Exact-Head-GitHub-Actions-, Reviewer- und
SonarQube-Evidenz auf dem autorisierten Draft-PR steht noch aus. Der aktuelle
Quelltext bleibt durch Reader-`contents: read`, nicht persistierte Checkout-
Credentials, Publisher-only-Write-Berechtigungen, exakte Candidate-Gates und
Draft-only-Veröffentlichung begrenzt. Kein Parent-Gitlink- oder MRTS-Wechsel
ist autorisiert oder durchgeführt.

## Historie

- 2026-07-20T19:12:21Z — ein task-eigener Pre-fix-Mutationstest validierte,
  dass der Resolver einen expliziten `${{ secrets.GITHUB_TOKEN }}`-Ausdruck
  akzeptierte; dieses P2/low-Framework-Härtungsfinding wurde vor der Delivery
  angelegt.
- 2026-07-20T19:55:25Z — die ortsgebundene rekursive Parser-Reparatur,
  einschließlich `${{ github['token'] }}`, bestand fokussierte
  Mutationsregressionen, natives vollständiges Lint und den versiegelten
  Security-Diff-Scan. Das Finding ist `fixed`; Exact-Head-Draft-PR-Validierung
  steht noch aus.

## Follow-up für serialisierte Kontexte

Die frühere Reparatur für direkte Referenzen klassifizierte keine nackten
Kontextobjekte innerhalb von GitHub-Expression-Funktionen. Eine sichere
Literal-Mutation mit `${{ toJSON(secrets) }}` in einem Reader-Shell-Step ließ
den fokussierten Test fehlschlagen, weil der Wartungscontract keinen Fehler
meldete; eine Publisher-Mutation mit `${{ toJSON(github) }}` wurde ebenfalls
akzeptiert. Es wurde kein Secret aufgelöst, ausgegeben, übertragen oder
aufbewahrt; eine bösartige Source-Änderung müsste weiterhin auf dem
vertrauenswürdigen Branch akzeptiert werden.

Die aktive enge Reparatur parst `${{ ... }}`-Ausdruckskörper. Sie weist
`secrets` überall im Ausdruck, `github.token`, jede `github[...]`-Form,
nackte GitHub-Kontext-Serialisierung und Shell-`${GITHUB_TOKEN}` außerhalb des
einen überprüften Inputs
`create-pull-request.with.token: ${{ github.token }}` zurück. Die legitimen
Kontrollen `github.sha` und `github.repository` bleiben gültig. Die
aufbewahrte sichere Evidenz ist
`evidence/fnd-framework-0033-serialized-context.md` im Task-Run
`20260720T180337Z-framework-python-313-updater-f3349a7e`; die Post-fix-
fokussierte Suite bestand 12 Tests. Die erneuerte 36-Test-Fokussuite, 85
CI-Security-Tests, native Workflow-/Dokumentations-/vollständige-Lint-Gates und
der versiegelte 11-Dateien-Follow-up-Security-Diff-Scan bestanden alle mit null
reportable Findings. Seine Report-SHA-256 lautet
`be92a7e65c3c81e72140b5441494eb4461df4417ee361c344bd3d0cf56775a5c`.

- 2026-07-20T20:54:02Z — als `in_progress` wiedereröffnet, nachdem der
  Bypass serialisierter Kontexte mit literalen Testausdrücken reproduziert
  wurde.
- 2026-07-20T21:12:33Z — nach expression-aware Regressions-Coverage, dem
  vollständigen lokalen Validierungssatz und dem versiegelten Follow-up-Scan
  wieder auf `fixed` gesetzt. Der remediierte Framework-Commit sowie
  Exact-Current-Head-Actions-, Review- und SonarQube-Evidenz stehen noch aus;
  kein Merge, Parent-Gitlink-Update oder MRTS-Aktion ist autorisiert.
