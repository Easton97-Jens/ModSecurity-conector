# FND-CROSS-0001 — Evidence-Freshness-Manifest enthält veraltete Einträge und SHA-Abweichungen

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-CROSS-0001` |
| Title / Titel | `Evidence-Freshness-Manifest enthält veraltete Einträge und SHA-Abweichungen` |
| Category / Kategorie | `evidence_gap` |
| Repository / Repository | `parent_and_framework` |
| Ownership / Ownership | `cross_repository` |
| Priority / Priorität | `P0` |
| Severity / Severity | `low` |
| Confidence / Confidence | `confirmed` |
| Status | `validated` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Die Bestandsaufnahme dokumentiert 58 veraltete Einträge und 9 SHA-Abweichungen in der Freshness-Evidence.

Aktueller Stand (`2026-07-26T18:27:22Z`): Parent-PR #74 benötigt eine neu
gehostete, descriptor-gestagte, payload-sichere aufbewahrte maschinenlesbare
Kette, bevor dieses P0-Finding fortschreiten kann. Der Producer vor der
Retention besaß keinen Artifact-Upload. Sein erster veröffentlichter
Nachfolger (`881a6bccf0a324ead467ced47b64514164b00981`) wurde nicht
akzeptiert, weil Pfadnamenprüfungen die spätere Upload-Action nicht banden;
seine zwei Läufe wurden vor dem Upload abgebrochen und erzeugten kein Artifact.

## Observed behavior / Beobachtetes Verhalten

Die Bestandsaufnahme dokumentiert 58 veraltete Einträge und 9 SHA-Abweichungen
in der Freshness-Evidence. Der ursprüngliche gehostete Parent-PR-#74-Workflow
erzeugte die strukturierte Kette, bewahrte sie nach Runner-Teardown aber nicht
auf. Der erste Retention-Nachfolger konnte außerdem einem später ersetzten Pfad
außerhalb seiner beabsichtigten Allowlist folgen.

## Expected behavior / Erwartetes Verhalten

Die aktuelle Evidence muss gegen bekannte Parent- und Framework-Revisionen
erneut ausgeführt, durch eine descriptor-sichere gestagte Allowlist kopiert, an
das finale strikte Gate gebunden und als payload-sicheres maschinenlesbares
Artifact aufbewahrt werden, bevor dieses Finding über `validated` hinaus
fortschreiten kann.

## Impact / Auswirkung

Release- und Assurance-Aussagen bleiben durch die dokumentierte Evidence
begrenzt. Ein ungebundener Pfadnamen-Upload könnte zusätzlich Inhalte außerhalb
der beabsichtigten strukturierten Allowlist aufbewahren und die erforderliche
Freshness-Kette nicht etablieren.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`
- `.github/workflows/verified-report-governance.yml`
- `ci/checks/common/check-python-version-contract.py`
- `ci/evidence/reports/stage-verified-full-matrix-evidence.py`
- `ci/lib/verified_full_matrix_receipt.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_generated_report_evidence_integrity.py`
- `tests/test_python_version_contract.py`

### Symbols / Symbole

- None / Keine

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '204,230p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:204-230`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '204,230p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run-ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/pr_delivery_status.json`
  - Typ: `strict_runtime_evidence_gate_failure`; SHA-256:
    `70aa1c1c9048027f02da2bad4f097165d267e70befeb965eec735b512dc1c366`
  - Kommando: `rtk gh pr checks 55 --repo Easton97-Jens/ModSecurity-conector`
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `1`
  - Beobachtet am `2026-07-18T11:13:55Z`; Aufbewahrung:
    `retained_task_evidence`
- Run-ID: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-current-master-transfer-revalidation.md`
  - Typ: `framework_current_master_validation_prerequisite_blocker`; SHA-256:
    `067db2ef9c429fa405737d193aa7a7fa5751c158b4d0ffdddbc6667918ce3ed6`
  - Kommando: `rtk proxy test -x /var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/tmp/framework-current-master-worktree/.venv/bin/python`
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `1`
  - Beobachtet am `2026-07-20T22:18:23Z`; Aufbewahrung:
    `retained_task_evidence`
- Run-ID: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-current-master-python-environment-preflight.md`
  - Typ: `framework_ci_python_and_dependency_contract_blocker`; SHA-256:
    `7491f9abd99c80e0c2c16b2ba2d3ef4ec5a21e4e93ea7ea272bb0d6b4e6f5082`
  - Kommando: `rtk proxy /usr/bin/python3.14 --version`
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`
  - Beobachtet am `2026-07-21T04:22:56Z`; Aufbewahrung:
    `retained_task_evidence`

- Run-ID: 20260721T055738Z-framework-pr39-delivery-followup-416b152c
  - Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/evidence/framework-pr39-cpython313-validation.md
  - Typ: framework_pr39_cpython31314_local_qualification; SHA-256:
    2825f5278dcf241dcdb8e501fccb85b9f9fc710e5b24406259a396af7cd3ee30
  - Kommando: Framework PR #39 CPython 3.13.14 qualification receipt: hash-locked PyYAML-6.0.3 installation and pip check; 30 direct affected tests; make test-ci-security-contract (89 tests); make check-python-version; make check-github-actions-workflows; make test-workflow-security-contract (7 tests); make check-documentation; python -m compileall -q ci tests; worktree-scoped response-body guard; make lint.
  - Arbeitsverzeichnis: framework-python-updater; Exit-Code: 0
  - Beobachtet am 2026-07-21T06:13:56Z; Aufbewahrung: retained

Dieser Receipt ersetzt nur die lokale CPython-Umgebungsprämisse von PR #39. Er
führt die ursprünglichen 58 veralteten Einträge und 9 SHA-Abweichungen nicht
erneut aus und gleicht sie nicht ab.

- Run-ID: `20260726T171724Z-pr74-hosted-evidence-retention`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260726T171724Z-pr74-hosted-evidence-retention/evidence/pr74-hosted-evidence-retention-preflight.md`
  - Typ: `hosted_runtime_evidence_retention_gap_preflight`; SHA-256:
    `3e5c1580b2e7765782cc83dae6122318aac97a26b7ac7b8c32d8d55f007bbcf3`
  - Kommando: Artifact-Inventar-Readback für die gehosteten PR-/Push-Runs
    `30210885288` und `30210883722` sowie Exact-Head-Readback für
    `30210885288`
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`
  - Beobachtet am `2026-07-26T17:17:24Z`; Aufbewahrung:
    `retained_task_evidence`
  - Beide aktiven Exact-Head-Runs meldeten einen Artifact-Count von `0`.
- Run-ID: `20260726T171724Z-pr74-hosted-evidence-retention`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260726T171724Z-pr74-hosted-evidence-retention/evidence/pr74-artifact-retention-security-correction.md`
  - Typ: `payload_safe_artifact_retention_security_correction`; SHA-256:
    `1c980e2b3de51b08144ae33fd534f882264780bc5fd4b22ce15689bb640bae5a`
  - Kommando: fokussierte Descriptor-Staging-, Workflow-Sicherheits- und
    Python-Contract-Validierung des lokalen Nachfolgers zum veröffentlichten
    PR-#74-Head `881a6bccf0a324ead467ced47b64514164b00981`
  - Arbeitsverzeichnis:
    `/var/tmp/codex/worktrees/parent/migrate-pr55-pr74-master-V27zuA/pr74`;
    Exit-Code: `0`
  - Beobachtet am `2026-07-26T18:27:22Z`; Aufbewahrung:
    `retained_task_evidence`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.
Das strikte Parent-Report-Gate weist die ungelöste veraltete oder abweichende
Runtime-Evidence korrekt zurück, statt Governance-Validierung in
Runtime-Nachweis umzuwandeln.

Der gehostete Producer benötigte außerdem einen expliziten payload-sicheren
Export: Seine generierten Manifeste und Receipts sind nur im ephemeren Runner
gültig, wenn der Workflow nicht nach dem strikten Gate ein allowlisted
Structured-Artifact aufbewahrt. Der erste Exportversuch verwendete
Pfadnamenprüfungen, aber diese banden `actions/upload-artifact` nicht an die
geprüften Source-Objekte.

## Proposed remediation / Vorgeschlagene Remediation

Revisionsgebundene Evidence neu erzeugen und abgleichen, eine descriptor-
gestagte maschinenlesbare Manifestkette aufbewahren und das strikte Report-Gate
bei ungelöster SHA-Abweichung oder einer geänderten gestagten Source geschlossen
fehlschlagen lassen.

Der Nachfolge-Workflow darf nur die drei Manifest-JSON-Dateien, die Command- /
Aggregate-Receipts des aktuellen Runs, den rohen Matrix-Index und zwölf Job-
JSON-Records aufbewahren; Build-Trees, Logs, `run.log`, Result-JSONL,
Request-/Response-Payloads, Header und Cookies müssen ausgeschlossen bleiben.

## Acceptance criteria / Akzeptanzkriterien

- Every retained assessment claim is tied to the current Parent and Framework revisions.
- The freshness manifest reports no unexplained stale entry or SHA mismatch.
- Der exakte Hosted-Upload enthält nur die feste 18-Dateien-Staging-Allowlist
  und ihre finale Byte-/Digest-Bindung an das Strict-Gate-Source-Set.

## Validation plan / Validierungsplan

- Regenerate the freshness manifest at the target revisions.
- Verify each report/reference SHA and retain the raw machine-readable result.
- Das Exact-Head-Success-only-Artifact herunterladen und eine übereinstimmende
  Run-ID, Parent-/Framework-Revisionen, deklarierte Hashes und alle zwölf
  strukturierten Full-Matrix-Job-Records sowie das exakte Pfad-Set der
  gestagten Allowlist prüfen.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.
- `tests.test_ci_security_workflows` muss eine Post-Gate-, SHA/run-gebundene,
  payload-sichere gestagte Artifact-Allowlist verlangen und Log-/Result-Payload-Pfade
  ablehnen.
- `tests.test_generated_report_evidence_integrity` muss Intermediate-/Final-
  Source-Symlinks, Source-Mutation/-Ersetzung, unsichere Staging-Parents,
  wiederverwendete Staging-Wurzeln und Post-Staging-Source-Änderungen ablehnen,
  während der legitime 18-Dateien-Control erhalten bleibt.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.
- Ein erfolgreicher Exact-Head-Strict-Producer muss die gestagten allowlisted Structured-
  Records hochladen, ohne Workflow-Permissions auszuweiten oder Runtime-
  Payloads aufzubewahren.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- Frische Parent- und Framework-Evidence sowie ein regeneriertes Freshness-
  Manifest wurden nicht erzeugt; die ursprünglichen 58 veralteten Einträge und
  9 SHA-Abweichungen bleiben ungelöst.
- Der zurückgehaltene `2026-07-21T04:22:56Z`-Current-master-Candidate-Preflight
  bleibt Evidence für diesen getrennten Candidate, aber der
  `2026-07-21T06:13:56Z`-Framework-PR-#39-CPython-3.13.14-Receipt revalidiert
  diesen Candidate nicht und erzeugt nicht die frische Parent-Runtime-Evidence,
  die dieses Finding erfordert.
- Der exakte Parent-PR-#74-Head `77bd39e64194cf5e6d221d874d9c6924549711eb`
  hatte gehostete Producer vor der Retention ohne Artifact-Inventar. Der
  veröffentlichte Nachfolger `881a6bccf0a324ead467ced47b64514164b00981` war
  unsicher und beide seiner Läufe wurden vor dem Upload abgebrochen. Der
  uncommitted Descriptor-Staging-Nachfolger muss committed werden, den strikten
  Producer bestehen und seine gebundene Structured-Evidence aufbewahren, bevor
  Freshness abgeglichen werden kann.

## Related findings / Verwandte Findings

- `FND-CROSS-0002`
- `FND-CROSS-0005`
- `FND-PARENT-0037`

## Residual risk / Restrisiko

Der Zustand bleibt offen. PR 55 exact head
`42b31f1c84c0c915a5cb65119714613fbf3e0c40` scheitert korrekt am
strikten Runtime-Evidence-Gate, weil dieser Freshness-Zustand ungelöst bleibt.
Der aktuelle Benutzer hat kein Risiko akzeptiert.

Der Current-master-Candidate-Transfer ist retained und seine statischen
Checks bestanden, aber es wurden keine frische Parent-Runtime-Evidence und
kein regeneriertes Freshness-Manifest erzeugt. Der spätere Framework-PR-#39-
Receipt beweist nur seine eigene Framework-spezifische lokale CPython-3.13.14-
Qualifikation; er revalidiert den getrennten Current-master-Candidate nicht
und löst die ursprünglichen 58 veralteten Einträge oder 9 SHA-Abweichungen
nicht. Es wird kein Risiko akzeptiert.

Die Parent-PR-#74-Producer vor der Retention schließen dieses Finding nicht,
weil keiner eine rohe Artifact-Kette aufbewahrt. Der veröffentlichte Nachfolger
`881a6bccf0a324ead467ced47b64514164b00981` wurde vor dem Upload abgebrochen,
weil Pfadnamenprüfungen ihn nicht sicher banden. Der descriptor-gestagte
Snapshot schützt die normale Runner-Grenze, kann aber einen beliebigen
weiterlaufenden Same-UID-Prozess nicht daran hindern, nach dem finalen Vergleich
einen Runner-Pfad zu ändern; eine getrennte Identität oder ein
Descriptor-/Stream-konsumierender Uploader wäre stärker. Der Nachfolger muss
veröffentlicht werden, bestehen und sein Artifact muss abgeglichen werden,
bevor sich `validated` oder `release_blocker: true` ändern kann. Es wird kein
Risiko akzeptiert.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-18T11:13:55Z`:
  `strict_report_gate_correctly_rejected_stale_runtime_evidence` — Parent PR 55
  head `42b31f1c84c0c915a5cb65119714613fbf3e0c40` scheiterte wie
  vorgesehen am strikten Runtime-Evidence-Gate und bewahrt dieses Finding als
  `validated`, statt Governance-only-Runtime-Evidence zu erzeugen.
- `2026-07-20T22:18:23Z`:
  `current_framework_master_prerequisite_blocked_before_parent_runtime_rerun`
  — der private Current-master-Candidate
  `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b` erhielt den geprüften
  Prerequisite-Patch ohne Pfadüberlappung und bestand Diff-/Shell-Checks; der
  SHA-256 des retained Reports lautet
  `067db2ef9c429fa405737d193aa7a7fa5751c158b4d0ffdddbc6667918ce3ed6`.
  Seine erforderliche Framework-`.venv/bin/python` fehlt; daher erfolgten
  keine System-/Parent-Python-Substitution, kein Framework-PR, keine frische
  Parent-Runtime-Evidence und kein geschützter Merge.
- `2026-07-21T04:22:56Z`:
  `authorized_framework_environment_preflight_remains_blocked_on_ci_contract`
  — der Benutzer autorisierte eine Framework-eigene Repository-Umgebung und
  Abhängigkeitsinstallation. Framework-`master` und der Candidate blieben
  `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b`, MRTS blieb unverändert und der
  Storage-Preflight erlaubte das geschätzte zusätzliche GiB. Der retained
  Preflight SHA-256
  `7491f9abd99c80e0c2c16b2ba2d3ef4ec5a21e4e93ea7ea272bb0d6b4e6f5082` zeigte,
  dass alle Framework-CI-Workflows und `requirements-ci.lock` CPython
  `3.13.14` erfordern, der lokal nicht verfügbar ist; gefunden wurde nur
  CPython `3.14.4`. `requirements-dev.txt` bleibt `PyYAML>=6,<7` und sein
  Bootstrap aktualisiert Pip. Es wurden keine `.venv`, kein Paketdownload,
  kein Framework-PR, keine frische Parent-Runtime-Evidence und kein
  geschützter Merge durchgeführt.
- 2026-07-21T06:13:56Z:
  framework_pr39_environment_blocker_superseded_without_freshness_resolution
  — der zurückgehaltene Receipt
  20260721T055738Z-framework-pr39-delivery-followup-416b152c, SHA-256
  2825f5278dcf241dcdb8e501fccb85b9f9fc710e5b24406259a396af7cd3ee30,
  etabliert die lokale Framework-PR-#39-CPython-3.13.14-Qualifikation mit
  hash-locked PyYAML-6.0.3, pip check, 30 direkten betroffenen Tests, 89 make
  test-ci-security-contract Tests, Workflow- und Dokumentations-Checks, python
  -m compileall -q ci tests, dem Response-Body-Guard und make lint. Er ersetzt
  nur den lokalen PR-#39-CPython-Umgebungsblocker; er führt die ursprünglichen
  58 veralteten Einträge und 9 SHA-Abweichungen nicht erneut aus und gleicht
  sie nicht ab, daher bleibt der Status `validated`.
- `2026-07-26T17:17:24Z`:
  `hosted_evidence_retention_gap_confirmed_and_remediation_prepared` — der
  exakte Parent-PR-#74-Head `77bd39e64194cf5e6d221d874d9c6924549711eb` hatte
  aktive Pull-Request- und Push-Producer mit Artifact-Count `0`. Die
  Parent-only-Remediation ergänzt eine Success-only-, SHA/run-gebundene,
  payload-sichere Allowlist nach dem unveränderten strikten Gate. Der
  Nachfolge-Exact-Head muss dieses Artifact veröffentlichen und abgleichen,
  bevor dieser P0-Release-Blocker fortschreiten kann.
- `2026-07-26T18:27:22Z`:
  `unbound_artifact_upload_corrected_with_descriptor_staging_and_fast_preflight`
  — unabhängiges Review des veröffentlichten PR-#74-Heads
  `881a6bccf0a324ead467ced47b64514164b00981` fand eine low/P3-Pfadnamen-
  TOCTOU-Exposure; seine zwei Läufe wurden vor dem Upload abgebrochen und
  erzeugten keine Evidence. Der lokale Parent-only-Nachfolger staged alle 18
  allowlisted Records über descriptor-relative No-Follow-Traversal, exklusive
  private Staging-Writes und eine finale Strict-Gate-Source-Bindung. Er ergänzt
  außerdem einen 15-Minuten-Read-only-Contract-Preflight und bricht nur
  überholte PR/ref-Läufe ab, während der vollständige Producer erhalten bleibt.
  Die lokale Validierung bestand; Exact-Head-Hosted-Artifact-, Sonar- und
  Protection-Evidence bleiben erforderlich.
