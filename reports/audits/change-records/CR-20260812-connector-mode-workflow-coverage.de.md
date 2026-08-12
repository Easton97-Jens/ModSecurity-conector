# Change Record: Statische Connector-Mode-Workflow-Abdeckung

**Sprache:** [English](CR-20260812-connector-mode-workflow-coverage.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260812-connector-mode-workflow-coverage |
| Datum (UTC) | 2026-08-12 |
| Basis-Revision | `33973d094b3f0aeb47605f08ced16a4043f643a0` |
| Delivery-Status | Draft-PR [#279](https://github.com/Easton97-Jens/ModSecurity-conector/pull/279) existiert auf seinem ursprünglichen Head; lokal validierte Korrektur-Commits warten auf genehmigte Veröffentlichung. Ready for Review bleibt durch die unten beschriebene Apache-Runtime-Abhängigkeit blockiert. |

## Motivation und Problemstellung

Der aktuelle Connector-Zustand benötigt eine explizite, wahrheitsgetreue
Workflow-Oberfläche für die vier CRS/MRTS-Mode-Kombinationen, ohne nicht
implementierte Fähigkeiten zu behaupten. Apache und HAProxy besitzen native
Runtime-Pfade für alle vier Modes. Envoy, Traefik und lighttpd haben einen
No-CRS/No-MRTS-Runtime-Pfad, einen statischen Framework-Contract für
With-CRS/No-MRTS und keinen unterstützten MRTS-Full-Matrix-Route. NGINX ist
bewusst ausgeschlossen, weil sein geschützter Broker eine separate
Trust-Grenze hat.

## Akzeptanzkriterien

- Vier benannte Top-Level-Workflows enthalten jeweils genau eine direkte,
  statische `strategy.matrix.include` mit fünf Zeilen und bilden gemeinsam die
  geforderten zwanzig Cells ohne NGINX- oder `_template`-Zeilen ab.
- Runtime-Cells rufen vorhandene native Controls auf und bewahren Cleanup und
  Exit-Status. Contract-Cells führen den bestehenden statischen Framework-
  Contract aus und behalten seine Unterscheidung
  `CONTRACT_VALIDATED`/`UNATTESTED` bei.
- Expected-unsupported-Cells rufen den realen Full-Matrix-Runner für den
  selektierten Connector, `unknown` und `_template` auf; jeder Aufruf muss mit
  Exit `2`, der Invalid-Choice-Diagnose und ohne Build-Root abweisen.
- Die Workflow-Sicherheit bleibt read-only und fail-closed: immutable
  Action-Pins, keine Secrets oder Write-Tokens, keine persistierten Checkout-
  Credentials, kein `pull_request_target`, kein Cache, keine Privilege-
  Escalation und keine breiten Artifact-Veröffentlichungen.
- Jede Framework-Python-Dependency-Installation in den neuen Workflows
  verwendet `requirements-ci.lock` mit `--require-hashes` und
  `--only-binary=:all:`; keine ruft `make setup-dev`,
  `bootstrap-python.sh`, `requirements-dev.txt` oder ein ungepinntes Pip-
  Upgrade auf.
- Bei einem Pull Request verwenden Checkout und die aufgezeichnete Parent-
  Revision die unveränderliche Event-Head-SHA; `github.sha` ist nur der
  Fallback für manuellen Dispatch.
- Parent- und Framework/MRTS-Gitlinks bleiben bei
  `209389022c942d83113f6be88bf31d25637352f0` beziehungsweise
  `615b13bacbd008562c17408246c41ab27dca3104` fest.

## Implementierungsentscheidung und Begründung

Die vier Workflows verwenden genau die fünf Nicht-NGINX-Connectors: `apache`,
`envoy`, `haproxy`, `lighttpd` und `traefik`. Ihr statisches Mapping lautet:

| Connector | no-crs/no-mrts | with-crs/no-mrts | no-crs/with-mrts | with-crs/with-mrts |
| --- | --- | --- | --- | --- |
| apache | runtime | runtime | runtime | runtime |
| haproxy | runtime | runtime | runtime | runtime |
| envoy | runtime | contract | expected_unsupported | expected_unsupported |
| traefik | runtime | contract | expected_unsupported | expected_unsupported |
| lighttpd | runtime | contract | expected_unsupported | expected_unsupported |

Die Implementierung verwendet ausschließlich vorhandene Parent-Entrypoints.
Sie fügt keine Connector-Fähigkeit hinzu, ändert weder die Full-Matrix-
Allowlist noch Framework- oder MRTS-Source und verändert weder den bestehenden
Workflow-Tool-Updater noch seinen Workflow. Dessen nicht zusammenhängende
All-Workflow-Inventurregression scheitert bereits im sauberen Basisstand an
einem action-freien lokalen Reusable-Caller; dieser Task schwächt oder ändert
dieses Testorakel nicht.

Die elf Runtime-Cells und die drei statischen Framework-Contract-Cells
installieren ihre erforderliche Python-Dependency aus der hash-gesperrten
Framework-`requirements-ci.lock`. Jede verwendet `--require-hashes`,
`--only-binary=:all:` und `pip check` statt `make setup-dev`, des Framework-
Development-Bootstraps oder eines veränderlichen Dependency-Pfads. Die
ausgecheckten Parent-, Framework- und MRTS-Revisionen werden vor dem Lesen
dieser Lockdatei gegen die aufgezeichneten immutable SHAs verifiziert. Dies
vermeidet das zuvor identifizierte, in `FND-PARENT-0052` verfolgte
Mutable-Pip-Muster, ohne einen Dependency-Lock oder Framework-Source zu ändern.

Der fokussierte No-CRS/With-MRTS-HAProxy-Zweig setzt vor seinem nativen
Case-Target den vorhandenen literalen Selektor
`RUNTIME_COMPONENT_TARGET=haproxy`. Dieser Zweig benötigt kein CRS und kann
deshalb das nicht zugehörige Apache-Archiv vermeiden, ohne seinen realen
HAProxy-Runtime-Pfad zu ändern. Die beiden With-CRS-HAProxy-Zweige behalten
bewusst die vorhandene All-Components-Vorbereitung: Der aktuelle Runtime-
Snapshot bindet ihre CRS-Quelle an diesen Preparation-Cache, und ein separater
frischer CRS-Fetch würde nicht Teil des zielgerichteten Snapshots. Apache
bleibt bewusst auf seinem regulären nativen Pfad, der weiterhin sein geprüftes
APR-util-Tupel benötigt.

## Geänderte Dateien

- Vier `test-connectors-*.yml`-Workflows.
- Fokussierte Workflow- und Python-Version-Contract-Tests/-Checker.
- Dieses englische/deutsche Change-Record-Paar und seine Archiv-Indizes.

Kein Connector-Source, Capability-Manifest, Lifecycle-Runner, Framework/MRTS-
Source, Gitlink, Dependency-Lock, Ruleset oder NGINX-Workflow ist Teil dieser
Änderung.

## Ausgeführte Befehle

- Der gepinnte statische Framework-Five-Connector-CRS-Contract und die CRS-
  Provenance-Regression bestanden beide.
- `tests.test_ci_security_workflows`, `tests.test_python_version_contract`,
  `tests.test_runtime_component_cache_contract` und
  `tests.test_runtime_env_snapshot_contract` bestanden: 120 Tests. Der
  fokussierte Connector-Mode-Contract weist eine Rückkehr zu `make setup-dev`,
  `bootstrap-python.sh`, `requirements-dev.txt` oder einem ungepinnten Pip-
  Upgrade zurück.
- `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
  check-ci-security-contract` bestand: 70 Tests, drei erwartete Environment-
  Capability-Skips und validate-only actionlint/zizmor/gitleaks-Lock-Checks.
- PyYAML lud alle vier Workflows, und ShellCheck bestand für jedes extrahierte
  GitHub-hosted-Bash-`run:`-Skript mit Warning-Severity.
- Der direkte Python-Workflow-Contract-Checker meldet dieselben 24 bereits
  vorhandenen Inventur-/Setup-Diagnosen im sauberen Basis- und Task-Worktree.
  Er meldet keine durch diese vier Workflows verursachte Diagnose.

## Security-Auswirkung

Die Workflows sind PR-sicher aufgebaut: top-level `permissions: contents:
read`, immutable Full-SHA-Action-Pins, rekursiver Checkout mit
`persist-credentials: false` und kein user-kontrollierter Ref in einem Shell-
Befehl. Die Event-Head-SHA wird ausschließlich als deklarativer Checkout- und
Revision-Gleichheitswert verwendet und nie in einen Shell-Body interpoliert.
Unsupported-Routen führen nur eine Parser-Abweisung unter dem privaten
Runner-Temp-Root aus; ein Rejection-Log ist ausschließlich diagnostisch und
kein Build-/Evidence-Artifact wird hochgeladen. Statische Contract-Routen
geben sich nicht als Host-Runtime-Evidence aus. Jede der elf Runtime-Cells und
drei Contract-Cells verwendet die hash-gesperrten CI-Requirements des
Frameworks und scheitert nach der Prüfung der unveränderlichen Gitlink-
Revisionen bei einem ungültigen Dependency-Set fail-closed. Keine neue
Workflow-Route ruft den veränderlichen Development-Bootstrap auf.

## Runtime-Evidence

Vor der Implementierung wiesen alle 18 ausgewählten/`unknown`/`_template`
negativen Runner-Versuche für die sechs unsupported Cells mit Exit `2` ab und
erzeugten keinen Build-Root. Die Framework-Contract- und Provenance-Tests sind
nur statische Evidence. Kein lokaler Connector-Build oder Host-Runtime wurde
ausgeführt; die vier neuen Hosted-Workflows müssen ihre eigene Exact-Head-
Runtime-Evidence liefern.

Die ursprünglichen Hosted-Runs belegten einen aktuellen externen Blocker, noch
bevor ein fokussierter Apache- oder HAProxy-Case ausgeführt wurde: Die gepinnte
Framework-APR-util-1.6.4-Archiv-URL lieferte während der All-Components-
Vorbereitung HTTP 404. Der eingegrenzte No-CRS/With-MRTS-HAProxy-Selektor
entfernt dieses nicht zugehörige Archiv aus diesem einen HAProxy-Pfad. Apache
und die With-CRS-HAProxy-Pfade bleiben fail-closed, bis das Framework sein
geprüftes Provenance-Tupel unabhängig aktualisiert.

## Bekannte Einschränkungen

Lokale `actionlint`- und `zizmor`-Binaries sind nicht verfügbar und wurden
nicht heruntergeladen oder installiert. Das installierte ShellCheck-Binary
kann die Workflow-/YAML-Analyse von actionlint nicht ersetzen. Ein lokales
statisches Ergebnis beweist weder GitHub-Hosted-Runner-Verhalten noch
Connector-Runtime-Erfolg oder Exact-PR-Head-Sicherheitsdurchsetzung.

Die bereits vorhandene Updater-Exact-Inventory-Regression bleibt außerhalb der
autorisierten Pfadliste: Ihre Korrektur würde eine nicht zusammenhängende
Testorakel-Änderung und Änderungen an einem bestehenden Updater-Workflow/-Tool
erfordern.

## Verbleibende Risiken

Apache-Runtime-Cells und die beiden With-CRS-HAProxy-Cells sind derzeit durch
das fehlende geprüfte APR-util-1.6.4-Provider-Asset im gepinnten Framework
blockiert; erforderlich sind ein Framework-eigenes Provenance-Update und
danach ein unabhängig autorisiertes Parent-Gitlink-Update. Die No-CRS-
HAProxy-Pfade und die offenen Connectoren hängen weiterhin von ihren Hosted-
Runner-Voraussetzungen ab. Envoy-, Traefik- und lighttpd-MRTS-Cells bleiben
ausdrücklich unsupported, bis eine unabhängig autorisierte Capability- und
Evidence-Änderung existiert. Kein Fehler darf durch eine Abschwächung der
negativen, statischen Contract-, Cleanup- oder Security-Guards verdeckt werden.

## Nicht ausgeführte Prüfungen mit Begründung

- Lokale actionlint-, actionlint-vermittelte ShellCheck- und zizmor-Scans: ihre
  gepinnten Binaries fehlen; Tool-Fetch liegt außerhalb der lokalen
  Validierungsautorität dieses Tasks. Stattdessen sind Exact-Head-Hosted-Checks
  erforderlich.
- Lokale Connector-Runtime-/Build-Matrix: Der Task ist workflow-/test-only und
  die Hosted-Workflows sind der angeforderte Runtime-Evidence-Pfad.
- Corrected-Head-PR-Checks, SonarQube-Cloud-Anwendbarkeit und Ready-for-Review-
  Disposition: Die Veröffentlichung des lokalen Korrektur-Heads ist nicht
  genehmigt, und der Apache-Runtime-Nachweis kann bis zur separaten Framework-
  Provenance-Remediation nicht bestehen. Ein Merge ist ausdrücklich außerhalb
  des Scopes.

## Finaler Diff- und Review-Status

Dies ist ein Partial-Delivery-Record. Lokale eingeschränkte Contracts bestehen
mit Ausnahme der separat reproduzierten bereits vorhandenen globalen Python-
Inventurdiagnosen. Die finale Prüfung muss einen veröffentlichten exakten
Commit-Head, Remote-Branch, PR-Head, vier Workflow-Runs,
actionlint/ShellCheck/zizmor, Required Checks und die Sonar-Anwendbarkeit
verifizieren, bevor der PR auf Ready for Review gesetzt wird; der aktuelle
Apache-Blocker verhindert diese Disposition innerhalb dieses Parent-only-Tasks.
