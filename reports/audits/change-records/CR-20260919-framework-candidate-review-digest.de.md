# Change Record

**Sprache:** [English](CR-20260919-framework-candidate-review-digest.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260919-framework-candidate-review-digest |
| Datum (UTC) | 2026-09-19 |
| Basis-Revision | 6bb07fee268aa013268f9b0566176d6f94c4abf9 |

## Motivation und Problemstellung

GitHub Actions [Run 35449797036](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35449797036), Job `105914883572`, schlug in `Validate Framework component-pin data contract` fehl. Der aktuelle Parent-Framework-Gitlink war `d4f7b69dc264852eac74e1439c0887fcb9fbe372`; der aufgelöste, nachfolgende Framework-Kandidat war `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`. Die geprüften OpenSSL-, OSV-Scanner- und Ruff-Wartungs-Pins des Kandidaten änderten die absichtlich abgedeckte `common.sh`-Struktur, während Parent noch `609315092e5f5cdd793a33636f7d620445f2e4e802a383c23bc26a70d1bc7c75` erwartete.

Die angeforderte Parent-only-Remediation lässt nur die separat geprüfte Kandidatenstruktur zu. Sie verändert weder Framework-/MRTS-Source, einen Gitlink, NGINX, die generische Component-Synchronisierung, Workflow-Permissions, Quality Gates noch Delivery-Controls.

## Akzeptanzkriterien

- Der exakte Kandidat `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` besteht den Verifier, während die aktuelle statische Parent-Projektion `d4f7b69dc264852eac74e1439c0887fcb9fbe372` bleibt.
- Die Production-Review-Konstante entspricht `7ad268af3baa17d2c2e9b5857ced2138684fab70e5066ddddd6f3656e8baa6af`.
- Abgedeckte OpenSSL-, OSV-Scanner- und Ruff-Pin-Mutationen schlagen weiterhin vor der Parent-Projektion fehl; der vorhandene registrierte Generic-Source-Data-Control bleibt akzeptiert.
- Alle bestehenden begrenzten File-Read-, Closed-Mutable-Field-, NGINX-Handoff- und Shell-Mutation-Controls bleiben unverändert.

## Implementierungsentscheidung und Begründung

Die Änderung ersetzt einen einzelnen Review-Digest, nicht einen Old/New-Allowlist. Ein dauerhafter Allowlist würde die ältere abgedeckte Wartungs-Pin-Struktur weiter zulassen und die One-Reviewed-Structure-Invariante abschwächen. Die Test-Fixture hält das exakte neue Review-Literal fest und prüft repräsentative abgedeckte OpenSSL-, OSV-Scanner- und Ruff-Pin-Modifikationen, die an der Structure-Boundary fehlschlagen müssen. Der bereits gemergte Static-SHA-Projection-Flow bleibt unverändert: Er prüft die aktuelle statische Parent-SHA, projiziert die trusted Resolver-SHA in seiner geschlossenen Five-Slot-Registry und verifiziert erneut.

## Security-Auswirkung

Dies ist eine CI-/Supply-Chain-Integrity-Boundary. Kandidateninhalt wird aus einem exakten Framework-Git-Objekt extrahiert und als begrenzte Regular-File-Daten gelesen, bevor er einen späteren Sourcing- oder Publication-Pfad erreicht. Der Verifier hasht weiter jede nicht-generische Zeile, lehnt unsichere Shell-Formen ab und validiert NGINX getrennt gegen Parent-Projektionen. Der beobachtete Fehler ist ein Fail-closed-Stale-Review-Reliability-Defect, keine nachgewiesene Sicherheitsumgehung oder externe Vulnerability. Es werden keine Scanner-Suppression, Exclusion, Quality-Gate-Änderung, Permission-Expansion oder gelockerte Validierung eingeführt.

## Geänderte Dateien

- `ci/tools/verify-framework-candidate-contract.py`
- `tests/test_verify_framework_candidate_contract.py`
- `reports/audits/change-records/CR-20260919-framework-candidate-review-digest.md`
- `reports/audits/change-records/CR-20260919-framework-candidate-review-digest.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Keine Framework-/MRTS-Source, kein Gitlink, keine `.gitmodules`, kein Dependency-Manifest, kein Credential, kein Generated Artifact, keine Runtime-Source, keine Workflow-Permission und kein Quality Gate wurden verändert.

## Tests und tatsächliche Ergebnisse

- Vor dem Patch endete `python3 ci/tools/verify-framework-candidate-contract.py --repo-root . --candidate-sha cc36b37d0f6a0fbc3512f3878a691751e91c5fbb --framework-common /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/ci/lib/common.sh --expected-parent-framework-sha d4f7b69dc264852eac74e1439c0887fcb9fbe372` mit Exit `2` und `Framework common.sh differs from approved reviewed structure`.
- Nach dem Patch endete derselbe Befehl mit Exit `0` und JSON-Status `verified`, `nginx_release_tag` `release-1.31.5` sowie denselben Candidate/Current-SHA-Werten.
- `env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/fix-actions-run-35449797036/runtime python3 -m unittest -v tests.test_verify_framework_candidate_contract` bestand `27` Tests.
- Der ausgewählte Parent-Virtual-Environment-Interpreter wiederholte den Exact-Candidate-Verifier mit Exit `0` und das fokussierte Verifier-Modul mit `27` bestandenen Tests.

## Ausgeführte Befehle

- `env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/fix-actions-run-35449797036/runtime make check-ci-security-contract` bestand `155` Tests mit `5` erwarteten umgebungsabhängigen Skips.
- `PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/fix-actions-run-35449797036/bytecode python3 -m py_compile ci/tools/verify-framework-candidate-contract.py tests/test_verify_framework_candidate_contract.py` bestand.
- `/root/git/ModSecurity-conector/.venv/bin/python` wurde als Virtual-Environment-Interpreter verifiziert (`sys.prefix != sys.base_prefix`) und mit `PYTHONNOUSERSITE=1`, `PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1` und `PYTHONDONTWRITEBYTECODE=1` für finale fokussierte Verifier-Checks verwendet.

## Runtime-Evidence

Der autoritative beobachtete Fehler ist GitHub-Actions-Run `35449797036`, Job `105914883572`. Der lokale Exact-Candidate-Verifier ist der stärkste verfügbare deterministische Contract-Proof. Es wurde kein Runtime-Connector-, NGINX-, Framework- oder MRTS-Service gestartet oder verändert.

## Nicht ausgeführte Prüfungen mit Begründung

`make check-bilingual-docs` und `make check-doc-links` sind nicht sauber, weil dieser isolierte Worktree absichtlich kein initialisiertes Framework-Submodule hat; alle übrigen gemeldeten Targets liegen unter `modules/ModSecurity-test-Framework`. Die erforderlichen Überschriften des neuen Records wurden nach der ersten Checker-Ausgabe korrigiert; ein gepaartes Dokumentationsreview fand keinen Content- oder Link-Befund. Ruff und Pyright sind in diesem Parent-Worktree nicht konfiguriert und ihre Executables fehlen im ausgewählten Parent-Environment; keine External-Tool-Installation ist autorisiert. GitHub-Exact-Head-Checks, SonarQube-Cloud-Quality-Gate, Review-Status und Hosted-Updater-Run bleiben ausstehend. Kein Workflow-Dispatch oder Merge wird durch diesen Record autorisiert.

## Bekannte Einschränkungen

Die lokale Testumgebung kann GitHub-hosted Tokens, Scheduler-Verhalten, Branch Protection, konkurrierende Remote-Änderungen oder eine spätere Candidate-Publication nicht beweisen. Framework-Upstream-Release-Provenance bleibt Framework-owned; Parent-Acceptance ist an den unveränderlichen Candidate-Commit und den geprüften Structure-Digest gebunden.

## Verbleibende Risiken

Jede zukünftige abgedeckte `common.sh`-Pin- oder Executable-Structure-Änderung benötigt einen neuen expliziten Parent-Review-Digest. Ein malformed Candidate, eine unsafe Shell-Form, NGINX-Drift, eine invalid Parent-Projektion oder ein geänderter Resolver-State schlägt weiterhin fail closed fehl.

## Finaler Diff- und Review-Status

Die Implementierung ist Parent-only; die lokale Evidenz ist oben festgehalten. Unabhängige Dokumentations- und Post-Patch-Bypass-/Regression-Reviews fanden keinen Action- oder reportierbaren Befund. Normale Task-Branch-Delivery, Exact-PR-Head-Checks und SonarQube-Cloud-Evidenz sind noch ausstehend; dieser Record behauptet keinen Commit, Push, PR, Hosted-Rerun oder Merge.
