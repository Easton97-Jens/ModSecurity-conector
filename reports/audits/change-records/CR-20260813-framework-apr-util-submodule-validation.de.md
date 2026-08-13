# Change Record: Framework-APR-util-Provenance und Submodule-Candidate-Validierung

**Sprache:** [English](CR-20260813-framework-apr-util-submodule-validation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260813-framework-apr-util-submodule-validation |
| Datum (UTC) | 2026-08-13 |
| Basis-Revision | `33973d094b3f0aeb47605f08ced16a4043f643a0` |
| Delivery-Status | Draft-Parent-PR [#280](https://github.com/Easton97-Jens/ModSecurity-conector/pull/280) ist gegen `master` offen. Lokale Validierung ist unten aufgezeichnet; Hosted-Exact-Head-Checks, Review, Merge und Cross-Repository-Delivery werden nicht behauptet. |

## Motivation und Problemstellung

Parent duplizierte eine statische APR-util-Version, Archiv-URL, SHA-256 und
Checksum-URL, obwohl das ausgecheckte Framework die genehmigte APR-util-
Provenance besitzt. Diese Duplizierung konnte vom autoritativen Framework-
Tupel abweichen, und geerbte `APR_UTIL_*`-Umgebungswerte konnten die
Ownership-Grenze verwischen.

Der Submodule-Updater-Validator behandelte außerdem seinen beabsichtigten
Checkout einer Framework-Candidate-SHA als Parent-Source-Mutation. Zu diesem
Zeitpunkt enthält der Parent-Index korrekt weiterhin den aktuellen Gitlink,
während der Framework-Worktree beabsichtigt auf die Candidate-SHA ausgecheckt
ist. Eine
parentweite Status-Prüfung wies deshalb gültige Candidate-Validierung ab, bevor
die spätere Source-Inventar-Baseline den erwarteten Übergang von einer
tatsächlichen Mutation unterscheiden konnte.

## Akzeptanzkriterien

- Produktive Parent-APR-util-Konfiguration verwendet das geschützte
  Provenance-Tupel des ausgecheckten Frameworks, weist direkte
  `APR_UTIL_*`-Overrides ab und validiert ausgewähltes Archiv, Checksum-URL und
  SHA-256 vor Cache- oder Build-Nutzung.
- Cache-Identitäten enthalten die autoritativen APR-util-Provenance-Eingaben.
- Der Updater akzeptiert einen unveränderten Candidate als No-op und einen
  gültigen vorwärts gerichteten Descendant, weist aber fehlerhafte,
  Ref-falsche, nicht-descendente oder historisch fehlerhafte
  Gitlink-Candidates ab.
- Candidate-State-Validierung erlaubt nur den erwarteten Framework-Candidate-
  Checkout-Übergang und scheitert fail-closed bei Parent-, Framework- oder
  initialisierten Nested-Submodule-Mutationen und bei unsicheren Metadatenpfaden.
- Englische und deutsche Reader-Dokumentation sowie Change Records beschreiben
  dasselbe Verhalten. Framework- und MRTS-Source, der Parent-Gitlink und jeder
  Merge bleiben außerhalb des Scopes.

## Implementierungsentscheidung und Begründung

`ci/tools/print-framework-apr-util-env.sh` ist eine feste `/bin/sh`-Bridge. Sie
weist jeden geerbten `APR_UTIL_*`-Wert ab, sourct das ausgecheckte Framework
`ci/lib/common.sh`, ruft die Framework-Provenance-Guards auf und gibt nur die
vier shell-quotierten APR-util-Assignments aus. Der Parent-Python-Loader ruft
diese feste Bridge über vertrauenswürdige Host-Executables auf, bereinigt
Shell-Hooks und `PATH`, parst das ausgewählte Tupel strikt und prüft seine
kanonische HTTPS-Downloadform und 64-stellige SHA-256. Runtime-Component-
Preparation, Inventory und Cache-Wrapper führen denselben Guard vor Cache-
Roots oder Build-Arbeit aus. Parent stellt keinen statischen Fallback-Pin
wieder her.

`ci/tools/validate-submodule-candidate-state.py` erfasst eine deterministische
Parent-Baseline vor Candidate-Checkout und validiert anschließend den exakten
Candidate-Zustand. Es validiert vollständige unveränderliche Revisionen,
Parent-HEAD, Hooks- und `.gitmodules`-Fingerprints, den aufgezeichneten
Framework-Gitlink, getrackten, gestagten und ungetrackten Zustand außerhalb des
Framework-Worktrees, Framework-Cleanliness und rekursiv initialisierten
Nested-Submodule-Zustand. Unsichere absolute, Traversal- oder Pathspec-Magic-
Metadaten werden vor Git- oder Pfadoperationen abgewiesen. Der Workflow ruft
diesen Helper um den bestehenden isolierten Validator auf, sodass die erwartete
Candidate-Worktree-/Gitlink-Differenz keine False Mutation mehr ist, während
alle anderen Mutationen fail-closed bleiben.

## Security-Auswirkung

Die Änderung stärkt zwei sicherheitsrelevante Grenzen. APR-util-Provenance wird
jetzt vom autoritativen Framework-Guard statt von duplizierten Parent-Pins
bezogen, und feindlicher geerbter Shell-Zustand kann das ausgewählte Tupel nicht
still überschreiben. Strikte Archiv- und Digest-Validierung bindet die Cache-
Identität an die geschützte Provenance.

Candidate-Validierung behandelt den Framework-Candidate weiterhin als nicht
vertrauenswürdig. Sie verlangt vollständige SHA-Werte, weist unsichere
Metadatenpfade vor ihrer Nutzung ab und meldet begrenzte JSON-escaped
Diagnostik nur im Fehlerfall. Sie erweitert weder Publisher-Berechtigungen,
Gitlink-Staging-Scope, Source-Write-Autorität noch die bestehende isolierte
Validator-Grenze.

## Geänderte Dateien

Die Parent-Änderungen sind:

- Workflow-/Build-Integration: `.github/workflows/ci-security-workflow-lint.yml`,
  `.github/workflows/update-submodules.yml`, `Makefile` und
  `ci/tools/update-workflow-tools.py`;
- APR-util-Provenance- und Cache-Flow:
  `ci/tools/print-framework-apr-util-env.sh`,
  `ci/provisioning/components/prepare-runtime-components.py`,
  `ci/provisioning/components/prepare-runtime-components.sh`,
  `ci/provisioning/cache/runtime-components-inventory.sh` und
  `ci/provisioning/cache/with-runtime-components.sh`;
- Submodule-Candidate-Validierung:
  `ci/tools/validate-submodule-candidate-state.py`;
- erzeugte Source- und Reader-Dokumentation:
  `scripts/generate_compiler_guides.py`, `docs/build/compilers/apache.md`,
  `docs/build/compilers/apache.de.md`, `docs/reference/variables.md` und
  `docs/reference/variables.de.md`;
- Tests und Fixtures: `tests/test_ci_security_workflows.py`,
  `tests/test_collect_no_crs_source.py`,
  `tests/test_runtime_env_snapshot_contract.py`,
  `tests/test_apr_util_static_contract.py`,
  `tests/test_framework_apr_util_provenance.py`,
  `tests/test_update_submodules_local_git.py`,
  `tests/test_validate_submodule_candidate_state.py` und
  `tests/fixtures/apr-util-static-allowlist.txt`; sowie
- dieses Change-Record-Paar und seine zweisprachigen Archive-Index-Einträge.

Keine Framework- oder MRTS-Source, kein Parent-Gitlink, kein erzeugter
Runtime-Report, Secret oder Cache-Artefakt ist enthalten.

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned temporary directory> .venv/bin/python -m unittest -v tests.test_ci_security_workflows tests.test_validate_submodule_candidate_state tests.test_update_submodules_local_git tests.test_apr_util_static_contract tests.test_framework_apr_util_provenance tests.test_runtime_env_snapshot_contract tests.test_runtime_component_cache_identity tests.test_prepare_runtime_components` — bestanden: 116 Tests im Shared-Checkout mit dem vorhandenen ausgecheckten Framework. Die kopierten Produktdateien wurden byteweise mit dem externen PR-Worktree verglichen.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_apr_util_static_contract` — bestanden: 5 Tests im externen PR-Worktree, einschließlich Clean-Checkout-Scan-Coverage.
- `rtk make check-ci-security-contract` — bestanden: 74 Tests und drei
  erwartete Capability-Skips; das Target validierte außerdem gepinnte
  Security-Tool-Lock-Records.
- Der initiale Hosted-Security-Workflow-Lint-Run
  [31710687331](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31710687331)
  auf PR-Head `905555264c46da1742d27110cef05b908c910c4f` scheiterte in drei
  Local-Git-Candidate-State-Tests, weil das geklonte Fixture-Submodule keine
  Git-Identität erbte. Das Fixture konfiguriert diesen lokalen Clone jetzt
  explizit; der externe PR-Worktree führte
  `rtk make check-ci-security-contract` erfolgreich erneut aus (74 Tests,
  drei erwartete Capability-Skips). Ein frisches Hosted-Exact-Head-Ergebnis
  steht noch aus.
- `rtk make lint` — bestanden. Sein eingeschränktes `PATH` fand actionlint
  nicht; der separate checksum-verifizierte actionlint-Aufruf mit
  `-shellcheck=/usr/bin/shellcheck` bestand für Workflows und Fixtures.
- `rtk make check-compiler-guides`, `rtk make check-variable-documentation`
  und `rtk make check-bilingual-docs` — bestanden in der früheren Content-
  Validation-Runde. Der externe PR-Worktree bestand zusätzlich
  `check-variable-documentation`; seine aktuelle Ausführung von
  `check-bilingual-docs` und `check-doc-links` erreichte den neuen Change
  Record ohne Record-Fehler, blieb aber wegen fehlender Framework-Link-Targets
  blockiert, da dieser Worktree bewusst kein initialisiertes Submodule enthält.
  Shell-Syntax-Prüfungen, ShellCheck für die neue Bridge, Python-Kompilierung
  und `git diff --check` bestanden ebenfalls.

Dies sind lokale Source-, Contract-, Lint- und Fixture-Ergebnisse. Sie sind
keine Runtime-Evidence.

## Runtime-Evidence

Es wurde keine Runtime-Evidence erhoben oder beansprucht. Kein Component-Build,
keine Cache-Population, keine Connector-Runtime und keine Hosted-Updater-
Ausführung wurden als Nachweis für diese Änderung verwendet.

## Nicht ausgeführte Prüfungen mit Begründung

- Frische GitHub-hosted-Updater-Validierung und PR-Checks für den späteren
  exakten PR-Head stehen nach der Local-Git-Fixture-Identity-Reparatur aus.
- SonarQube Cloud, Review, Merge, resulting-`master`-Validierung und
  Workspace-Restoration werden nicht behauptet; der Benutzer hat nur einen
  Draft-PR autorisiert.
- Vollständige Component-Builds und Connector-Runtime-Matrizen wurden nicht
  ausgeführt, weil ihre Downloads und Runtime-Umgebungen weiter reichen als die
  hier geänderten Provenance- und Workflow-Contracts.
- Die finalen `check-bilingual-docs` und `check-doc-links` im externen Worktree
  bleiben durch bewusst nicht initialisierte Framework-Links blockiert. Die
  Framework-Richtlinie verbietet, dieses externe Submodule in dieser
  Parent-only-Delivery automatisch zu initialisieren oder zu ändern.

## Bekannte Einschränkungen

Die lokalen Git-Fixtures prüfen Resolver- und Candidate-State-Verhalten,
beweisen aber kein GitHub-hosted-Runner-Verhalten. Die Bridge benötigt ein
ausgechecktes Framework-`common.sh`; dieses Framework bleibt extern owned und
unverändert. Direkte Parent-`APR_UTIL_*`-Overrides schlagen jetzt absichtlich
früh fehl, statt ein Framework-owned-Provenance-Tupel zu verändern.

## Verbleibende Risiken

Der finale exakte PR-Head benötigt weiterhin seine anwendbaren Hosted-Checks,
Review- und Protected-Branch-Policy-Auswertung. Korrekte APR-util-Werte bleiben
vom ausgecheckten Framework-Guard abhängig, was das beabsichtigte Ownership-
Modell ist. Dieser Record behauptet absichtlich keinen Security-Scan-, Hosted-,
Merge- oder Cross-Repository-Erfolg.

## Finaler Diff- und Review-Status

Die eingeschränkte Parent-Implementierung, fokussierte lokale Tests,
Security-Review und Whitespace-Prüfungen wurden vor Delivery beobachtet. Der
Draft-Parent-PR [#280](https://github.com/Easton97-Jens/ModSecurity-conector/pull/280)
ist gegen `master` offen; sein aktueller exakter Head und Hosted-Check-Status
müssen nach diesem Follow-up-Record-Commit erneut abgefragt werden. Kein
Review, Merge oder Parent-Gitlink-Update wird behauptet.
