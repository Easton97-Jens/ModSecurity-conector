# Change Record: Statische Connector-Mode-Workflow-Abdeckung

**Sprache:** [English](CR-20260812-connector-mode-workflow-coverage.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260812-connector-mode-workflow-coverage |
| Datum (UTC) | 2026-08-12, reconciled 2026-08-14 |
| Basis-Revision | `ea3b48abab7940de49997a371f9117b409c05a2a` |
| Delivery-Status | Draft-PR [#279](https://github.com/Easton97-Jens/ModSecurity-conector/pull/279) bleibt auf dem Remote-Head `63ad4f5ed359ba2be9abe955cb1c82e7dfcb3846`. Der lokale Task-Branch hat den aktuellen Master normal in `4e224b23c5973c34be3ef4f336b7772a0b13c094` gemergt und enthält darüber die lokal validierte Parent-CRS-Akquisitionsreparatur. Es wurde noch kein korrigierter Head gepusht und keine Ready-for-Review-Umstellung vorgenommen; die verbleibenden Clean-Worktree-Runtime-Controls und jede Exact-Head-Hosted-Evidence stehen noch aus. |

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
  `1260aaae411ecf88cf50dc480b80e2e20ac47901` beziehungsweise
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

Alle vier Pfadfilter enthalten jetzt ihre direkten Interpreter-, Provisioning-,
Provenance-, Report-Helper- und `.gitmodules`-Abhängigkeiten. Der fokussierte
Contract verlangt in jedem Workflow dasselbe geschlossene Trigger-Set; NGINX
bleibt ausgeschlossen.

Die drei Workflows, die `verified-haproxy-case` direkt aufrufen, leiten
`haproxy_source_root="$CACHE_ROOT/shared/sources"` ab, weisen einen Root
außerhalb von `$CACHE_ROOT` zurück und übergeben ihn nur an dieses Make-Target.
Damit entspricht der Aufrufer dem `SOURCE_ROOT`- und `CRS_SOURCE_DIR`-Pfad des
Component-Snapshots; der separate No-CRS/No-MRTS-HAProxy-Pfad und der
Framework-Containment-Guard bleiben unverändert.

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

Der Parent-Component-Preparer zeichnet jetzt auf, ob eine Git-Quelle rekursiv
akquiriert wurde. Nur `coreruleset` wählt `--no-recurse-submodules`; alle
generischen Git-Komponenten behalten ihren bestehenden rekursiven Clone- und
Submodule-Update-Pfad. Die CRS-Cache-Identität enthält den nichtrekursiven
Mode, sodass ein alter rekursiver CRS-Checkout nicht wiederverwendet werden
kann. Frische und wiederverwendete nichtrekursive CRS-Checkouts schlagen
fail-closed fehl, wenn nullterminierte lokale `submodule.*`-Metadaten oder eine
`.git/modules`-Registry vorliegen. Das verhindert den Zustand an der Quelle;
es löscht keine Konfiguration nach der Akquisition und ändert nicht den
Framework-Provenance-Guard.

## Geänderte Dateien

- Vier `test-connectors-*.yml`-Workflows.
- `ci/provisioning/components/prepare-runtime-components.py` sowie
  fokussierte Workflow-/Python-/Cache-Contract-Tests einschließlich
  `tests/test_runtime_component_cache_contract.py`.
- Dieses englische/deutsche Change-Record-Paar und seine Archiv-Indizes.

Kein Connector-Source, Capability-Manifest, Lifecycle-Runner, Framework/MRTS-
Source, Gitlink, Dependency-Lock, Ruleset oder NGINX-Workflow ist Teil dieser
Änderung.

## Ausgeführte Befehle

- `ConnectorModeWorkflowContractTest` plus `PythonVersionContractTest`
  bestanden: `31` Tests. Sie prüfen die geschlossene 20-Cell-Topologie, die
  aktuellen Gitlinks, den hash-gesperrten Installationspfad, die direkten
  Trigger und den HAProxy-Snapshot-Source-Root-Guard.
- APR-util-/Provenance-/Static-/Snapshot-Controls bestanden: `43` Tests.
- `RuntimeComponentCacheContractTest` bestand: `47` Tests. Die fokussierte
  Preparation-Suite bestand: `41` Tests. Sie decken die nur-für-CRS geltende
  nichtrekursive Akquisition, die nullsichere lokale Config-Prüfung, die exakt
  gepinnte Revision, Wiederholung/Wiederverwendung, den Rebuild eines
  kontaminierten Legacy-Caches, fehlgeschlagenes Staging-Cleanup und ein echt
  rekursives Generic-Component-Control ab.
- `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
  check-ci-security-contract` bestand: `97` Tests und `4` erwartete
  Environment-Capability-Skips; die Tool-Lock-Prüfung ist validate-only.
- Python-Kompilierung und `git diff --check` bestanden.
- PyYAML parste alle vier Workflows. ShellCheck erhielt alle `42` literalen
  Bash-`run:`-Blöcke über stdin; jeder endete mit `0`. Blöcke mit
  GitHub-Ausdrücken bleiben ausschließlich unter Hosted-actionlint autoritativ.
- Eine frische private virtuelle Umgebung installierte die Framework-
  `requirements-ci.lock` mit `--require-hashes` und `--only-binary=:all:`, lud
  PyYAML `6.0.3` und bestand `python -m pip check`.

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
erzeugten keinen Build-Root. Der Framework-Contract bleibt statische Evidence.

Die frische All-Target-Component-Vorbereitung wurde in einem neuen privaten
Build-/Source-/Cache-Root ausgeführt. Framework
`1260aaae411ecf88cf50dc480b80e2e20ac47901` wählte APR-util `1.6.5`; der
frische Archiv-SHA-256 lautet
`96de1dd6f6a0476d2d2e7964926d8c1ddc3bb0e210e1b1812d3ba5a454a392e2`.
Apache/No-CRS/No-MRTS `action_deny_phase1` bestand anschließend mit HTTP
`403`. Der alte APR-util-`1.6.4`-HTTP-`404`-Fehler des PR-Heads ist damit durch
aktuelle Master-Evidence überholt; `FND-FRAMEWORK-0067` wird durch diesen
Parent-Task nicht verändert.

Die vorhergehende rekursive CRS-Akquisition wurde gegen die freigegebene
Revision `55b09f5acfd16413e7b31041100711ceb7adc89c` reproduziert: Sie erzeugte
lokal `submodule.active .`, und der unveränderte Framework-Guard wies den
Checkout korrekt mit Exit `77` ab. Der neue nur-für-CRS geltende
nichtrekursive Pfad erreicht denselben freigegebenen Commit, liefert
`recursive_submodules=false`, lässt
`git config --local --null --get-regexp '^submodule\\.'` leer (Git-Exit `1`),
erzeugt keine `.git/modules` und wird vom unveränderten Framework-
`prepare-crs.sh`-Guard akzeptiert. Die absichtlich kontaminierte negative
Fixture liefert weiterhin Exit `77`; generische Komponenten, die Submodules
benötigen, bleiben rekursiv. Dies ist die lokale Reparatur für
`FND-PARENT-0128`, kein Guard-Bypass.

Die fokussierten `action_deny_phase1`-Controls für Apache und HAProxy mit
`with-crs/no-mrts` bestanden jeweils mit HTTP `403` unter der reparierten
Source-Topologie. Ein erster kanonischer Apache-No-CRS-Lauf führte beide
legitimen Fälle aus, aber sein Evidence-Finalizer verweigerte korrekt `PASS`,
weil der Source-Worktree dirty war. Er ist nur diagnostisch; die vollständige
frische Acht-Mode-Serie im sauberen Worktree bleibt vor der Veröffentlichung
erforderlich.

### Diagnose der alten Hosted-Runs

| Alter Run | Jobs / erster kausaler Schritt | Einordnung auf aktuellem Master |
| --- | --- | --- |
| `31616687887` | Apache `94181133426`, Provision host component: APR-util `1.6.4` HTTP `404` | durch aktuelle Framework-APR-util-`1.6.5`-Vorbereitung und Apache-Runtime-Nachweis überholt |
| `31616687903` | Apache/HAProxy: APR-util `1.6.4` HTTP `404`; Envoy/Traefik/lighttpd: `ModuleNotFoundError: No module named 'yaml'` | APR-Fehler überholt; YAML-Pfad lokal durch hash-gesperrte `requirements-ci.lock` behoben |
| `31616687995` | Apache/HAProxy: APR-util `1.6.4` HTTP `404` | überholt; der reparierte lokale CRS-Pfad ermöglicht einen erforderlichen frischen Exact-Head-Rerun |
| `31616688052` | Apache/HAProxy: APR-util `1.6.4` HTTP `404` | überholt; der reparierte lokale CRS-Pfad ermöglicht einen erforderlichen frischen Exact-Head-Rerun |

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

Die frischen lokalen Controls verwendeten CPython `3.14.4`; die Hosted-
Workflows erwarten `3.14.6`. Daher behauptet dieser Record keine exakte
Interpreter-Äquivalenz.

## Verbleibende Risiken

`FND-PARENT-0128` ist lokal behoben, bleibt aber ein Release-/Integration-
Blocker, bis die Acht-Mode-Runtime-Serie im sauberen Worktree und alle
Exact-Head-Hosted-Cells bestehen. Framework/MRTS-Source und der fail-closed
Provenance-Guard bleiben unverändert. actionlint/zizmor, Required Checks,
Sonar-Disposition und die gesamte Hosted-Matrix-Evidence sind weiterhin
unverifiziert. Envoy-, Traefik- und lighttpd-MRTS-Cells bleiben ausdrücklich
unsupported, bis eine unabhängig autorisierte Capability- und Evidence-
Änderung existiert. Kein Fehler darf durch Abschwächung negativer,
statischer-Contract-, Cleanup- oder Security-Guards verdeckt werden.

## Nicht ausgeführte Prüfungen mit Begründung

- Lokale actionlint-, actionlint-vermittelte ShellCheck- und zizmor-Scans: ihre
  gepinnten Binaries fehlen; Tool-Fetch liegt außerhalb der lokalen
  Validierungsautorität dieses Tasks. Stattdessen sind Exact-Head-Hosted-Checks
  erforderlich.
- Vollständige Acht-Mode-Lokalserie im sauberen Worktree und Exact-Head-
  Hosted-Connector-Matrix: Beide stehen bis zum fokussierten lokalen Commit
  aus, den der native No-CRS-Evidence-Finalizer benötigt, bevor er einen
  sauberen Checkout attestieren kann.
- Corrected-Head-PR-Checks, SonarQube-Cloud-Anwendbarkeit und Ready-for-Review-
  Disposition: Es wurde kein korrigierter Commit gepusht; Merge und Auto-Merge
  bleiben ausdrücklich außerhalb des Scopes.

## Finaler Diff- und Review-Status

Dies ist ein laufender lokaler Remediation-Record. Der normale Master-Merge
behielt den aktuellen Framework-Gitlink bei; es gibt keinen task-eigenen
Gitlink-Diff. Die Parent-CRS-Reparatur, ihre fokussierten Regressionen, die
aktuelle APR-util-Provenance und die ersten reparierten fokussierten Controls
bestanden lokal. Eine spätere finale Prüfung muss die Runtime-Serie im sauberen
Worktree, einen veröffentlichten exakten Commit-Head, Remote-Branch, PR-Head,
vier Workflow-Runs, alle 20 Cells, actionlint, ShellCheck, zizmor, Required
Checks und die Sonar-Anwendbarkeit prüfen, bevor PR #279 auf Ready for Review
gesetzt wird. Kein Push, keine Ready-Umstellung, kein Merge und kein
Auto-Merge sind hier verzeichnet.
