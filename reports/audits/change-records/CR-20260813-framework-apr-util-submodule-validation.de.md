# Change Record: Framework-APR-util-Provenance und Submodule-Candidate-Validierung

**Sprache:** [English](CR-20260813-framework-apr-util-submodule-validation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260813-framework-apr-util-submodule-validation |
| Datum (UTC) | 2026-08-13 |
| Basis-Revision | `33973d094b3f0aeb47605f08ced16a4043f643a0` |
| Delivery-Status | Parent-PR [#280](https://github.com/Easton97-Jens/ModSecurity-conector/pull/280) wurde in `master` unter SHA `7e057a27b5ea068cae073b48f0fc8de6b33083b5` gemergt. Der geschützte `master`-`validate_only`-Run [31777704809](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31777704809) bestand mit Candidate `a65eb889dc663d9940215bc4f18f52e56587d8a6`; das Publizieren wurde übersprungen. Der normale Updater-Run [31777868704](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31777868704) erzeugte den unveränderten Draft-PR [#281](https://github.com/Easton97-Jens/ModSecurity-conector/pull/281) auf `9dd5d6a0ea5bedce7318eca941227b32d5aefe76` und schlug danach fail-closed fehl, weil die GitHub CLI JSON-`null` aus `.auto_merge` als leeren Shell-Wert ausgab. PR #281 wurde anschließend extern am `2026-08-14T07:14:48Z` mit Merge/Master-SHA `8d416239ea8920c45f07ce2c39daab5f4e44fe5e` gemergt. Korrektur-PR [#282](https://github.com/Easton97-Jens/ModSecurity-conector/pull/282) wurde danach am `2026-08-14T07:41:07Z` von Head `634a1dc1e3636bc628400952da2f73d602c7c813` in `master` `790eac0a875a9ed0148e78d656cfdd30c3104ca6` squash-gemergt; seine erforderlichen Checks einschließlich SonarCloud-PR-API `total:0` bestanden nach einem erfolgreichen Wiederholungslauf eines transienten Traefik-Fuzz-Timeouts. Alle beobachteten Master-Push-Workflows bestanden. Der finale Updater-Run `31781092484` auf `790eac0a875a9ed0148e78d656cfdd30c3104ca6` bestand mit `changed=false`; Validator und Publisher wurden übersprungen, ohne Branch-, Commit- oder PR-Mutation. Die offene Updater-PR-Liste war leer; der bestehende Chore-Branch blieb auf `9dd5d6a0ea5bedce7318eca941227b32d5aefe76`. |

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

- Produktive Parent-APR-util-Konfiguration weist direkte `APR_UTIL_*`-Overrides
  ab. Ein vollständiges kanonisches Tupel darf nur intern zwischen Parent und
  Child nach einem unabhängigen Vergleich mit dem ausgecheckten Framework
  weitergegeben werden; partielle, leere, abweichende oder alternative Tupel
  schlagen vor Cache- oder Build-Nutzung fehlgeschlossen fehl. Parent besitzt
  keine APR-util-Version oder SHA-256.
- Cache-Identitäten enthalten die autoritativen APR-util-Provenance-Eingaben.
- Der Updater akzeptiert einen unveränderten Candidate als No-op und einen
  gültigen vorwärts gerichteten Descendant, weist aber fehlerhafte,
  Ref-falsche, nicht-descendente oder historisch fehlerhafte
  Gitlink-Candidates ab.
- Candidate-State-Validierung erlaubt nur den erwarteten Framework-Candidate-
  Checkout-Übergang und scheitert fail-closed bei Parent-, Framework- oder
  initialisierten Nested-Submodule-Mutationen und bei unsicheren Metadatenpfaden.
- Der Candidate-Validator läuft in einer privaten `tmpfs`-`chroot`-Allowlist:
  `/source` ist read-only, `/external` ist der einzige für den Validator
  beschreibbare Pfad, `/guard` ist nicht beschreibbar, der Jail-Root ist
  read-only, und geerbte nicht-standardmäßige Deskriptoren werden vor dem
  Identitäts-Drop geschlossen. Die Host-Aliasse `/tmp`, `/var`, `/home`,
  `/root`, `/run`, `/sys` und `/dev/shm` sind nicht vorhanden.
- Englische und deutsche Reader-Dokumentation sowie Change Records beschreiben
  dasselbe Verhalten. Framework- und MRTS-Source, der Parent-Gitlink und jeder
  Merge bleiben außerhalb des Scopes.

## Implementierungsentscheidung und Begründung

`ci/tools/print-framework-apr-util-env.sh` ist eine feste `/bin/sh`-Bridge. Sie
erfasst und entfernt geerbten `APR_UTIL_*`-Zustand, sourct das ausgecheckte
Framework `ci/lib/common.sh`, ruft die Framework-Provenance-Guards auf und gibt
nur die vier shell-quotierten APR-util-Assignments aus. Der Parent-Python-Loader
ruft diese feste Bridge über vertrauenswürdige Host-Executables auf, bereinigt
Shell-Hooks und `PATH`, parst ein vollständiges kanonisches Tupel strikt und
vergleicht die erfasste Eingabe unabhängig mit dem Ergebnis des ausgecheckten
Frameworks. Nur eine fehlende Eingabe oder ein passendes nichtleeres
vollständiges Tupel darf intern zwischen Parent und Child weitergegeben werden;
partielle, leere, abweichende oder alternative Tupel schlagen fehlgeschlossen
fehl. Die kanonische HTTPS-Downloadform und 64-stellige SHA-256 werden vor der
Nutzung erneut validiert. Runtime-Component-Preparation, Inventory und
Cache-Wrapper führen denselben Guard vor Cache-Roots oder Build-Arbeit aus.
Parent besitzt keine APR-util-Version oder SHA-256 und stellt keinen statischen
Fallback-Pin wieder her.

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

Die abgeschlossene lokale `GITHUB_ENV`-Containment-Härtung im
Remediation-Commit `646eec7edf3165c1bc8b82273c1fd5490738fc11` behandelt den Pfad
vom Workflow-Argument `--github-env "$GITHUB_ENV"` über
`capture_parent_baseline`, `_open_github_environment_file` und den finalen
Baseline-Write mit `os.fdopen(..., "a")`. Bevor der Sink geöffnet wird,
verlangt der Helper ein normalisiertes absolutes Ziel strikt unterhalb von
`RUNNER_TEMP`, durchläuft jedes Verzeichnis über mit `O_NOFOLLOW` geöffnete
Deskriptoren und verlangt für jedes Verzeichnis Eigentum des effektiven Users
und keine Gruppen- oder Weltbeschreibbarkeit. Das finale Ziel muss eine
reguläre Datei mit einem Link, Eigentum des effektiven Users und ohne Gruppen-
oder Weltbeschreibbarkeit sein und wird relativ zum verifizierten
Verzeichnisdeskriptor mit `O_NOFOLLOW | O_NONBLOCK` zum Anhängen geöffnet.
`O_NONBLOCK` verhindert, dass ein FIFO den Schreibpfad blockiert, während die
Regular-File-Prüfung ihn abweist. Bei jeder verletzten Invariante gibt der
Helper vor dem Baseline-Write `GITHUB_ENV_INVALID` zurück.

## Security-Auswirkung

Die Änderung stärkt zwei sicherheitsrelevante Grenzen. APR-util-Provenance wird
jetzt vom autoritativen Framework-Guard statt von duplizierten Parent-Pins
bezogen, und feindlicher geerbter Shell-Zustand kann das ausgewählte Tupel nicht
still überschreiben. Ein vollständiges kanonisches Tupel darf die interne
Parent-/Child-Grenze nur nach einem unabhängigen Framework-Vergleich passieren;
partielle, leere, abweichende und alternative Tupel schlagen fehlgeschlossen
fehl. Strikte Archiv- und Digest-Validierung bindet die Cache-Identität an die
geschützte Provenance.

Candidate-Validierung behandelt den Framework-Candidate weiterhin als nicht
vertrauenswürdig. Sie verlangt vollständige SHA-Werte, weist unsichere
Metadatenpfade vor ihrer Nutzung ab und meldet begrenzte JSON-escaped
Diagnostik nur im Fehlerfall. Sie erweitert weder Publisher-Berechtigungen,
Gitlink-Staging-Scope, Source-Write-Autorität noch die bestehende isolierte
Validator-Grenze.

`FND-PARENT-0122` behebt die frühere Exposition geerbter Host-Mounts. Nach dem
Eintritt in einen privaten Mount- und PID-Namespace erstellt vertrauenswürdiges
Setup ein privates `tmpfs`-Jail und verwendet `chroot` vor der Candidate-
Ausführung. Die Jail-Allowlist enthält read-only `/source`, ein für den
Validator beschreibbares `/external`, nicht beschreibbares `/guard`, die
read-only-Runtime-Verzeichnisse `/usr`, `/bin`, `/sbin`, `/lib`, `/lib64` sowie
nur die exakte `actions/setup-python`-Runtime unter
`/opt/hostedtoolcache/Python/<version>/<architecture>` und minimales
read-only-`/etc`-Material. Der Launcher akzeptiert nur den aufgelösten
nicht-symlinkten `<version>/x64`-Unterbaum und bind-mountet genau diesen
Unterbaum vor dem Start von Candidate-Code read-only. Das Hosted-Runner-
Quellverzeichnis darf permissive Host-Rechte haben, doch weder Host-`/opt`
noch ein anderer Host-Alias sind im Jail vorhanden. Sein Root wird read-only
remountet; ein frisches
gehärtetes read-only-`proc` wird bei `/proc` gemountet,
und privates `/dev` enthält nur `null` und `urandom`. Vor dem Drop auf
`modsecurity-validator` schließt der Launcher geerbte Deskriptoren außer
Standard-Input, -Output und -Error. Das verhindert Hostpfad-Aliasse und
Escapes über vorgeöffnete Deskriptoren zu `/tmp`, `/var`, `/home`, `/root`,
`/run`, `/sys` oder `/dev/shm`.

Der Launcher löst seine festen Pfade `/usr/bin/gcc` und `/usr/bin/g++` erst
auf, nachdem `/usr` im Jail bereits read-only bereitgestellt ist. Er akzeptiert
ihre finalen Targets nur als ausführbare reguläre Dateien, die weiterhin unter
`/usr` aufgelöst werden, und übergibt die aufgelösten Pfade über die expliziten
Umgebungsvariablen `CC` und `CXX`. `/etc/alternatives` fehlt absichtlich im
Jail, sodass der Candidate keinen Compiler über den Host-Alternatives-
Mechanismus auswählen kann.

Netzwerkzugriff bleibt absichtlich verfügbar, weil hash-pinned `pip`-
Installation für das Funktionieren des Validators erforderlich ist. Diese
Remediation behauptet keine Egress-Isolation. Die unten genannte begrenzte
Hosted-`validate_only`-Evidence belegt weder SonarQube noch einen PR-Merge oder
den Abschluss von `FND-PARENT-0122`; das Finding bleibt offen. Nach diesem
Nachweis wurde die temporäre Validation-Admission entfernt: Die permanente
Policy erlaubt nur den Reparatur-Branch und geschütztes `master`.

Auf PR-#280-Head `3fbba306ddedf86acd3d01929a077cee33f66ed7` meldete das
task-eigene SonarCloud-Ergebnis S8707 für diesen `GITHUB_ENV`-Schreibpfad.
Dieser Record klassifiziert das Ergebnis weder als False Positive noch
beansprucht er eine Suppression. Die Containment-Implementierung ist lokal
abgeschlossen; frische Hosted-Sonar-Analyse steht erst nach dem Follow-up-
Commit für dessen neuen PR-Head aus.

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
- Submodule-Candidate-Validierung und ihre Dateisystemgrenze:
  `ci/tools/validate-submodule-candidate-state.py` und
  `ci/tools/run-readonly-submodule-validation-namespace.py`;
- erzeugte Source- und Reader-Dokumentation:
  `scripts/generate_compiler_guides.py`, `docs/build/compilers/apache.md`,
  `docs/build/compilers/apache.de.md`, `docs/build/README.md`,
  `docs/build/README.de.md`, `docs/reference/variables.md` und
  `docs/reference/variables.de.md`;
- Tests und Fixtures: `tests/test_ci_security_workflows.py`,
  `tests/test_collect_no_crs_source.py`,
  `tests/test_runtime_env_snapshot_contract.py`,
  `tests/test_apr_util_static_contract.py`,
  `tests/test_framework_apr_util_provenance.py`,
  `tests/test_update_submodules_local_git.py`,
  `tests/test_validate_submodule_candidate_state.py`,
  `tests/test_run_readonly_submodule_validation_namespace.py` und
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
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_validate_submodule_candidate_state tests.test_update_submodules_local_git` — bestanden: 13 Tests nach der abgeschlossenen lokalen Containment-Härtung.
- `rtk make check-ci-security-contract` — bestanden: 77 Tests und drei
  erwartete Skips nach der abgeschlossenen lokalen Containment-Härtung.
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

### SonarCloud-Follow-up

- Der Task-Owner beobachtete ein S8707-Ergebnis für den `GITHUB_ENV`-
  Schreibpfad auf PR #280 mit Head `3fbba306ddedf86acd3d01929a077cee33f66ed7`.
  Die Deskriptor-Containment-Implementierung ist lokal abgeschlossen und die
  zwei oben genannten lokalen Befehle bestanden danach. Für den späteren
  PR-Head, den dieser Follow-up-Commit erzeugt, wurde keine frische
  Hosted-Sonar-Analyse ausgeführt oder beobachtet. Dieser Record erhebt daher
  keinen Resolved-, Clean-, False-Positive- oder Suppression-Claim.
- Lokale Regressionsabdeckung für die Containment-Invariante liegt in
  `ValidateSubmoduleCandidateStateTests.test_capture_rejects_github_env_outside_runner_temp_or_via_symlink` und
  `ValidateSubmoduleCandidateStateTests.test_capture_rejects_missing_runner_temp_and_accepts_runner_file`.
  Die Fälle weisen ein Ziel außerhalb, lexikalisches Traversal, ein Symlink-
  Ziel, einen Hard Link, ein Symlink-Verzeichnis sowie fehlendes oder unsicheres
  `RUNNER_TEMP` ab und akzeptieren eine reguläre runner-eigene Datei. Der
  abgeschlossene Pfad öffnet außerdem mit `O_NONBLOCK`, wodurch FIFO-Blocking
  verhindert wird, während die Regular-File-Invariante FIFO-Ziele abweist.

## Runtime-Evidence

Kein Component-Build, keine Cache-Population, keine Connector-Runtime und keine
Hosted-Updater-Ausführung wurden als Nachweis für diese Änderung verwendet. Die
unten genannte begrenzte Hosted-Validator-Evidence beansprucht keines dieser
weitergehenden Runtime-Ergebnisse.

### Hosted-`validate_only`-Evidence

Der GitHub-hosted-`workflow_dispatch`-`validate_only`-Run
[`31776302498`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31776302498)
lief auf dem exakten Head `c7bbc70bcf729d148a7d87f45ca352ae7247416b`.
Validator-`make quick-check`, Postverification und Enforcement waren
erfolgreich. Der Publisher wurde übersprungen und erzeugte keinen Output-Pull-
Request, Commit oder Branch. Dies ist begrenzte funktionale Evidence für diesen
Run und Head; sie belegt kein SonarQube-Ergebnis, keinen PR-Merge und keinen
Abschluss von `FND-PARENT-0122`.

## Nicht ausgeführte Prüfungen mit Begründung

- `FND-PARENT-0122` bleibt offen. Run `31776302498` liefert die oben
  beschriebene begrenzte Exact-Head-Validator-Evidence; ein Finding-Abschluss
  wird nicht behauptet.
- Frische GitHub-hosted-Updater-Validierung und PR-Checks für den späteren
  exakten PR-Head stehen nach der Local-Git-Fixture-Identity-Reparatur aus.
- S8707 wurde auf `3fbba306ddedf86acd3d01929a077cee33f66ed7` beobachtet.
  Frische SonarCloud-Analyse steht nach diesem Follow-up-Commit für einen
  späteren PR-Head aus. Bis diese Analyse beobachtet wurde, wird kein
  Hosted-Resolved-, Hosted-Clean-, False-Positive- oder Suppression-Claim
  erhoben.
- Zum historischen Zeitpunkt des früheren Follow-ups wurden Review, Merge,
  resulting-`master`-Validierung und Workspace-Restoration nicht behauptet;
  der Benutzer hatte nur einen Draft-PR autorisiert. Der spätere Merge und
  die Validierung sind unten im aktuellen Delivery-Update dokumentiert.
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
unverändert. Direkte Parent-`APR_UTIL_*`-Overrides schlagen absichtlich früh
fehl, statt ein Framework-owned-Provenance-Tupel zu verändern. Parent besitzt
keine APR-util-Version oder SHA-256; das intern weitergegebene Tupel bleibt nur
nach seinem unabhängigen Vergleich mit dem ausgecheckten Framework gültig.

Die `GITHUB_ENV`-Containment-Härtung ist lokal abgeschlossen und hat lokale
Regressionsabdeckung, benötigt aber weiterhin frische Hosted-Sonar-Analyse
nach dem Follow-up-Commit, um den Hosted-Status von S8707 für dessen späteren
PR-Head festzustellen.

Das `FND-PARENT-0122`-Jail begrenzt Dateisystem- und geerbte Deskriptor-
Oberfläche des Candidate, nicht Netzwerk-Egress oder vollständige Host-/Kernel-
Isolation. Netzwerkzugriff bleibt nur für hash-pinned `pip`-Installation
erhalten. Hosted-Exact-Head-Validator-Validierung wurde in Run `31776302498`
beobachtet; der Finding-Abschluss bleibt ausstehend.

## Verbleibende Risiken

Der finale exakte PR-Head benötigt weiterhin seine anwendbaren Hosted-Checks,
Review- und Protected-Branch-Policy-Auswertung. Korrekte APR-util-Werte bleiben
vom ausgecheckten Framework-Guard abhängig, was das beabsichtigte Ownership-
Modell ist. Der ausstehende Hosted-S8707-Status für den späteren PR-Head ist
ein zusätzliches Delivery-Risiko. Dieser Record behauptet absichtlich keinen
SonarQube-, Merge- oder Cross-Repository-Erfolg; er behauptet nur die oben
genannte begrenzte Hosted-Validator-Evidence.

## Finaler Diff- und Review-Status

Die eingeschränkte Parent-Implementierung, fokussierte lokale Tests,
Security-Review und Whitespace-Prüfungen wurden vor Delivery beobachtet. Der
Draft-Parent-PR [#280](https://github.com/Easton97-Jens/ModSecurity-conector/pull/280)
ist gegen `master` offen; sein exakter neuer Head und Hosted-Check-Status
müssen nach diesem Follow-up-Record-Commit erneut abgefragt werden. Das
beobachtete S8707-Ergebnis gehört zum früheren Head
`3fbba306ddedf86acd3d01929a077cee33f66ed7`; frische Hosted-Sonar-Analyse ist
weiterhin für den späteren Follow-up-Head erforderlich. Kein Review, Merge
oder Parent-Gitlink-Update wird behauptet.

## Lokales SonarCloud-New-Issues-Follow-up

Dieses Follow-up behebt sechs SonarCloud New Issues in den lokalen
Parent-Änderungen. Es aktualisiert nur die folgenden Implementierungs- und
fokussierten Testpfade:

- `ci/provisioning/components/prepare-runtime-components.py`: Der relevante
  reguläre Ausdruck verwendet mit `re.ASCII` explizit ASCII, und die
  Loader-Helper wurden ohne Änderung ihres Fail-closed-Verhaltens refaktoriert.
- `ci/tools/print-framework-apr-util-env.sh`: Ein Shell-Quote-Arity-Guard weist
  ein ungültiges Quoting-Ergebnis vor dessen Ausgabe ab.
- `ci/tools/validate-submodule-candidate-state.py`: Die Hook-Inventory-Logik
  wurde in einen Helper aufgeteilt, und der `.gitmodules`-Pfad wird durch eine
  Konstante dargestellt.
- `tests/test_framework_apr_util_provenance.py` und
  `tests/test_validate_submodule_candidate_state.py`: Fokussierte Coverage
  wurde für diese Änderungen hinzugefügt oder aktualisiert.

Für dieses Follow-up wurde folgende lokale Validierung beobachtet:

- die ausgewählten Validator-Tests bestanden: 11 Tests;
- die ausgewählten APR-util/Cache-Tests bestanden: 13 Tests;
- `rtk make check-ci-security-contract` bestand: 78 Tests mit drei erwarteten
  Skips;
- `sh -n ci/tools/print-framework-apr-util-env.sh` bestand; und
- ein versiegelter lokaler Security-Diff-Scan fand 0 berichtspflichtige
  Findings über die fünf geänderten Code-/Testpfade.

Dies sind ausschließlich lokale Ergebnisse. Für den Follow-up-Head wurde noch
kein frisches Hosted-SonarCloud-Ergebnis beobachtet; die Hosted-Analyse bleibt
bis nach Commit und Push des Follow-ups ausstehend.

## Hosted-Delivery-Ergebnis (vor diesem reinen Dokumentations-Follow-up-Commit beobachtet)

Dieser Abschnitt korrigiert den früheren Status einer ausstehenden
Hosted-Analyse. Der Source-Remediation-Commit
`2a962b43615b8ff078a00828b1fb3338ce441abd` ist der exakte von SonarCloud am
`2026-08-13T15:51:30+0000` analysierte PR-Head: Das Quality Gate meldete `OK`,
`codeSmells` war `0`, und die API-Abfrage meldete insgesamt `0` offene New
Issues. Die GitHub-Checksuite für diesen exakten Head war terminal, ohne
ausstehende oder erfolglose Checks. Draft-Parent-PR
[#280](https://github.com/Easton97-Jens/ModSecurity-conector/pull/280) war zu
diesem historischen Zeitpunkt gegen `master` offen; sein späterer Merge ist
unten dokumentiert.

Diese Fakten gehen diesem reinen Dokumentations-Follow-up-Commit voraus, der
keine selbstreferenzielle finale SHA beansprucht. Zu diesem historischen
Zeitpunkt waren weder Merge noch Auto-Merge, Parent-Gitlink-Update oder
Framework/MRTS-Delivery erfolgt oder behauptet.

## Aktueller Delivery-Update nach #280

Die vorstehenden Delivery-Angaben sind historisch, soweit sie PR #280 als
offen beschreiben. PR #280 wurde in den geschützten `master` unter
`7e057a27b5ea068cae073b48f0fc8de6b33083b5` gemergt. Die resultierenden
Master-Checks liefen erfolgreich durch. Der geschützte `master`-
`validate_only`-Run
[`31777704809`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31777704809)
bestand ebenfalls: Der Validator wählte Candidate
`a65eb889dc663d9940215bc4f18f52e56587d8a6`, während das Publizieren
übersprungen wurde.

Der anschließende normale Updater-Run
[`31777868704`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31777868704)
löste denselben Candidate auf und validierte ihn. Sein Publisher erzeugte
sicher den unveränderten Draft-PR [#281](https://github.com/Easton97-Jens/ModSecurity-conector/pull/281)
mit Head `9dd5d6a0ea5bedce7318eca941227b32d5aefe76` und schlug anschließend
bei der Identitätsprüfung fail-closed fehl. Ursache war, dass
`gh api --jq '.auto_merge'` JSON-`null` als leeren Shell-Wert ausgab und die
Prüfung auf deaktiviertes Auto-Merge dadurch fälschlich fehlschlug. PR #281
wurde anschließend extern am `2026-08-14T07:14:48Z` mit Head
`9dd5d6a0ea5bedce7318eca941227b32d5aefe76` und Merge/Master-SHA
`8d416239ea8920c45f07ce2c39daab5f4e44fe5e` gemergt. Alle PR-Checks
einschließlich SonarCloud sowie die aufgeführten Master-Push-Workflows
bestanden.

Die lokale Korrektur normalisiert die `.auto_merge`-Abfrage in allen drei
Updater-Identitätsprüfungen: `update-submodules.yml`,
`update-python-version.yml` und `update-go-version.yml`. Die finale Abfrage
akzeptiert ausschließlich vorhandenes JSON-`null`:
`if (has("auto_merge") and (.auto_merge == null)) then "null" else
"auto-merge-present" end`. Ein fehlendes Feld, `false`, der String `"null"`,
ein Objekt oder jeder andere Wert wird abgelehnt. Die lokale Validierung
bestand mit 28 fokussierten CI-Security-Tests sowie
`make check-ci-security-contract` (90 bestanden, 4 erwartete
Capability-Skips). `/usr/bin/jq`-Vektoren ergaben einmal `null` und viermal
`auto-merge-present` für die abgelehnten Fälle; die reale PR-#281-Abfrage mit
dem finalen Ausdruck ergab `null`. Das abschließende eingeschränkte
`git diff --check` bestand.

Die Korrektur wurde über PR [#282](https://github.com/Easton97-Jens/ModSecurity-conector/pull/282)
ausgeliefert, der am `2026-08-14T07:41:07Z` von Head
`634a1dc1e3636bc628400952da2f73d602c7c813` in Master
`790eac0a875a9ed0148e78d656cfdd30c3104ca6` squash-gemergt wurde. Seine
erforderlichen Checks einschließlich SonarCloud-PR-API `total:0` bestanden;
ein transienter Traefik-Fuzz-Timeout wurde durch einen erfolgreichen
Wiederholungslauf behoben. Alle beobachteten Master-Push-Workflows,
einschließlich Security-Workflow-Lint und CodeQL, bestanden.

Der finale normale Updater-Run `31781092484` auf
`790eac0a875a9ed0148e78d656cfdd30c3104ca6` bestand mit Candidate/Current
`a65eb889dc663d9940215bc4f18f52e56587d8a6`, `changed=false`; Validator und
Publisher wurden übersprungen. Es erfolgte keine Branch-, Commit- oder
PR-Mutation; die offene Updater-PR-Liste war leer und der bestehende
Chore-Branch blieb auf `9dd5d6a0ea5bedce7318eca941227b32d5aefe76`.

`FND-PARENT-0122` ist nun anhand seiner retained Exact-Head- und
Resulting-Master-Evidence geschlossen: PR #280, Hosted-Runs `31776302498` und
`31777704809`, lokale Security-/Namespace-Regressionen und finaler No-op
`31781092484`. Die fünf masterweiten `cpp:S5945`-Issues in
`common/scripts/modsecurity_targeted_eval.cc` stammen aus der Zeit vor PR
#280 und sind von dieser Änderung unabhängig; dieser Record behauptet weder
ihre Behebung noch eine Reduktion der masterweiten Sonar-Issue-Anzahl auf null.
