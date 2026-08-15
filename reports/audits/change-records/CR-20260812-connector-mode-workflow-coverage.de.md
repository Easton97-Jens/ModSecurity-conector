# Change Record: Statische Connector-Mode-Workflow-Abdeckung

**Sprache:** [English](CR-20260812-connector-mode-workflow-coverage.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260812-connector-mode-workflow-coverage |
| Datum (UTC) | 2026-08-12, reconciled 2026-08-14 |
| Basis-Revision | `ea3b48abab7940de49997a371f9117b409c05a2a` |
| Delivery-Status | Draft-PR [#279](https://github.com/Easton97-Jens/ModSecurity-conector/pull/279) bleibt auf dem Remote-Head `63ad4f5ed359ba2be9abe955cb1c82e7dfcb3846`. Der lokale Task-Branch hat den aktuellen Master normal in `338985e5329076d42bb23cdeac8260f72b68b71d` gemergt und enthält darüber die lokal validierte Parent-CRS-Akquisitionsreparatur und Workflow-Korrekturen. Es wurde noch kein korrigierter Head gepusht und keine Ready-for-Review-Umstellung vorgenommen; Exact-Head-Hosted-Evidence steht weiterhin aus. |

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

With-MRTS-Runtime-Cells verwenden den bestehenden nativen Control
`action_allow_phase1_pass` und weisen ausdrücklich auf DetectionOnly-Semantik
hin; sie behaupten keine Enforcement-Wirkung. Die separaten No-MRTS-Runtime-
Cells behalten `action_deny_phase1`/HTTP `403` als Enforcement-Nachweis. Der
fokussierte No-CRS/With-MRTS-HAProxy-Zweig setzt vor seinem nativen
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
Source-Topologie. Danach vervollständigte die Runtime-Evidence im sauberen
Worktree alle acht Apache/HAProxy-Mode-Cells: Die vier No-MRTS-Enforcement-
Controls lieferten HTTP `403`, während die vier With-MRTS-DetectionOnly-
Controls `action_allow_phase1_pass` ausführten und HTTP `200` mit ausgeführtem
nativen Control, aber ohne Enforcement-Claim lieferten. Die HAProxy-Workflows
legen `BUILD_ROOT` nun unter `$cell_root/verified/build` und erfüllen damit
den bestehenden Verified-Root-Guard; ein `XDG_STATE_HOME`-Workaround wurde
nicht hinzugefügt. Diese lokale Acht-Mode-Evidence ist für den Task erhalten,
ersetzt aber keine Exact-Head-Hosted-Runs.

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

`FND-PARENT-0128` ist lokal behoben; die verbundene With-MRTS-Semantik- und
HAProxy-Root-Korrektur ist lokal ausgeführt, aber Release/Integration bleibt
blockiert, bis Exact-Head-Hosted-Cells bestehen. Framework/MRTS-Source und der
fail-closed Provenance-Guard bleiben unverändert. actionlint/zizmor, Required
Checks, Sonar-Disposition und die gesamte Hosted-Matrix-Evidence sind weiterhin
unverifiziert. Envoy-, Traefik- und lighttpd-MRTS-Cells bleiben ausdrücklich
unsupported, bis eine unabhängig autorisierte Capability- und Evidence-
Änderung existiert. Kein Fehler darf durch Abschwächung negativer,
statischer-Contract-, Cleanup- oder Security-Guards verdeckt werden.

## Nicht ausgeführte Prüfungen mit Begründung

- Lokale actionlint-, actionlint-vermittelte ShellCheck- und zizmor-Scans: ihre
  gepinnten Binaries fehlen; Tool-Fetch liegt außerhalb der lokalen
  Validierungsautorität dieses Tasks. Stattdessen sind Exact-Head-Hosted-Checks
  erforderlich.
- Exact-Head-Hosted-Connector-Matrix: Sie steht bis zu einem gepushten
  korrigierten Head aus; die vollständige Acht-Mode-Lokalserie im sauberen
  Worktree ist abgeschlossen, beweist aber kein Hosted-Runner-Verhalten.
- Corrected-Head-PR-Checks, SonarQube-Cloud-Anwendbarkeit und Ready-for-Review-
  Disposition: Es wurde kein korrigierter Commit gepusht; Merge und Auto-Merge
  bleiben ausdrücklich außerhalb des Scopes.

## Finaler Diff- und Review-Status

Dies bleibt ein lokaler Remediation-Record. Der normale Master-Merge behielt
den aktuellen Framework-Gitlink bei; es gibt keinen task-eigenen Gitlink-Diff.
Die Parent-CRS-Reparatur, ihre fokussierten Regressionen, die aktuelle
APR-util-Provenance, die HAProxy-Verified-Root-Korrektur und die vollständigen
sauberen Acht-Mode-Runtime-Controls bestanden lokal. Die finale Prüfung muss
weiterhin einen veröffentlichten exakten Commit-Head, Remote-Branch, PR-Head,
vier Hosted-Workflow-Runs, alle 20 Cells, actionlint, ShellCheck, zizmor,
Required Checks und die Sonar-Anwendbarkeit prüfen, bevor PR #279 auf Ready for
Review gesetzt wird. Kein Push, keine Ready-Umstellung, kein Merge und kein
Auto-Merge sind hier verzeichnet.

## Nachtrag vom 2026-08-15: Sonar-Duplizierung und Beibehaltung als Draft

### Motivation

Der vorherige PR-#279-Head zeigte `1.6%` New-Code-Duplizierung neben `0 New
issues`, `0 Security Hotspots` und `0.0% Coverage on New Code`. Der Nutzer
verlangte literal null angezeigte Werte, eine Aktualisierung vom aktuellen
`master` und die Beibehaltung als Draft, solange weitere Arbeit aussteht.

### Akzeptanzkriterien

- Nur die nachgewiesene task-eigene Duplizierung entfernen, ohne Sonar-
  Konfiguration, Exclusion, Suppression, `NOSONAR`, Testabschwächung oder
  Coverage-Abkürzung.
- `origin/master` `55e45726a39bebd3f33aea87807419a882cd3ea8` normal in den
  bestehenden Branch mergen, ohne Rebase, Force-Push, Default-Branch-Push,
  Merge oder Auto-Merge.
- PR #279 offen als Draft belassen und nach der Veröffentlichung ein neues
  Exact-Head-Sonar-Ergebnis einholen; eine lokale Berechnung ist kein Sonar-
  Ergebnis.

### Technische Entscheidungen

Sonar ordnete alle 32 duplizierten New-Code-Zeilen
`tests/test_runtime_component_cache_contract.py` zu: zwei lokale Git-Command-
Mocks waren äquivalent. Commit `f1f7bb615f89a8d17e0e1193d368ecae79d3a805`
extrahiert sie in `_local_component_runner`; jeder Test übergibt weiterhin
eigenen Upstream, gepinnten Commit, Branch, erwartete URL, ursprünglichen
Command-Runner und `clone_modes`-Receipt. `--no-recurse-submodules` und
`--recursive` werden daher weiterhin unabhängig geprüft.

Der normale Refresh-Merge ist `c6045f289b1b92d062732d552968c170f1c23a0f` mit
den Parents `dd92b27c4f5189abc4e0658df01ad1995a65209d` und
`55e45726a39bebd3f33aea87807419a882cd3ea8`. PR #279 wurde zu Draft
konvertiert. Framework- und MRTS-Source sowie Parent-Gitlinks bleiben außerhalb
dieses Follow-ups.

### Security-Auswirkung

Dieser test-only Maintainability-Refactor bewahrt Provenance-, Runtime-Root-,
Dependency-Lock-, CI-Permission-, Negative-Control- und Cache-Integrity-
Assertions. Kein Security-Control, keine Workflow-Permission, Download-Regel
oder Test-Erwartung wurde abgeschwächt.

### Geänderte Dateien

- `tests/test_runtime_component_cache_contract.py`
- `reports/audits/change-records/CR-20260812-connector-mode-workflow-coverage.md`
- `reports/audits/change-records/CR-20260812-connector-mode-workflow-coverage.de.md`

### Tests und tatsächliche Ergebnisse

`/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q
tests.test_runtime_component_cache_contract` bestand: 47 Tests in 39.718s.
`git diff --check` bestand vor den Dokumentationsänderungen. Sonars vorherige
exakte Messung waren 32 neue duplizierte Zeilen, `1.6129032258064515%`; die
nächste Hosted-Analyse muss `0.0%` für den neuen exakten PR-Head verifizieren.

### Runtime-Evidence

Für diesen test-only Refactor lief keine Connector-Runtime. Der Contract-Test
validiert gemockte Checkout-Pfade, nicht Hosted-Runner- oder Connector-Runtime-
Verhalten.

### Nicht ausgeführte Prüfungen

Neue Exact-Head-GitHub-Actions-, SonarQube-Cloud-, actionlint-,
actionlint-vermittelte-ShellCheck- und zizmor-Ergebnisse existieren bei diesem
Record-Update noch nicht und müssen nach dem normalen Branch-Push beobachtet
werden. Kein Package- oder Tool-Download ersetzte Hosted-Checks.

### Bekannte Einschränkungen

Die vorhandene `0.0%`-Coverage-Anzeige beruht auf keinem importierten New-Code-
Coverage-Report, nicht auf Runtime-Coverage. Nur die Exact-Head-Sonar-Analyse
nach dem Push kann die Remote-Duplication-Berechnung verifizieren.

### Restrisiken

Sonar kann den aktualisierten Source anders klassifizieren. Unabhängig von
bestandenen Checks bleibt PR #279 Draft, weil der Nutzer erklärt hat, dass vor
jeder Master-Integration weitere Arbeit erforderlich ist.

### Finaler Review-Status

Der Source-Refactor ist lokal committet, sein fokussierter Test besteht und der
normale Master-Merge ist lokal vorhanden. Veröffentlichung und Exact-Head-
Verifikation stehen aus; keine Ready-Umstellung, kein Merge und kein Auto-Merge
sind autorisiert.

## Zweiter Nachtrag vom 2026-08-15: Framework-Pin beim Master-Refresh

### Motivation

Der erste aktualisierte Head, `e0845a6e0f5ce37b713007640c7f68231b26c2fb`,
erreichte bei SonarQube Cloud Quality Gate `OK`, null neue duplizierte Zeilen,
`0.0%` Duplizierung, null neue Issues und null neue Security Hotspots. Seine
vier Connector-Mode-Matrizen und `actionlint` scheiterten dennoch vor der
Runtime: Der normale Master-Merge änderte den Parent-Framework-Gitlink auf
`01952978772995c054ba6a4cba86adc5d0cd1e7d`, während die PR-Workflows und ihr
Contract weiter `1260aaae411ecf88cf50dc480b80e2e20ac47901` erwarteten.

### Akzeptanzkriterien

- Die bestehenden exakten, fail-closed Parent-zu-Framework- und Framework-zu-
  MRTS-Revision-Checks bewahren.
- Alle Connector-Mode-Workflows und ihren Security-Contract ausschließlich mit
  dem bereits gemergten Parent-Gitlink abgleichen.
- Den lokalen Security-Contract erneut ausführen und nach der Korrektur neue
  Exact-Head-Hosted-Evidence erhalten; den PR als Draft belassen.

### Technische Entscheidungen

Commit `1855ed8bc9e6485d80ecdf373d33a6a0118b4646` ändert nur die vier
`EXPECTED_FRAMEWORK_SHA`-Werte und `CONNECTOR_MODE_FRAMEWORK_SHA` auf
`01952978772995c054ba6a4cba86adc5d0cd1e7d`. Der ausgecheckte Framework-Commit
hat den unveränderten verschachtelten MRTS-Gitlink
`615b13bacbd008562c17408246c41ab27dca3104`; daher bleibt
`EXPECTED_MRTS_SHA` exakt und unverändert. Dies ist keine Framework-, MRTS-
oder Parent-Gitlink-Source-Änderung.

### Security-Auswirkung

Die Korrektur stellt den immutablen Revision-Check wieder her, statt ihn zu
umgehen. Sie lässt PR-Trigger, read-only Permissions, exakten PR-Head-Checkout,
`persist-credentials: false`, SHA-gepinnte Actions und die No-Secret/No-Write-
Boundary unverändert.

### Geänderte Dateien

- `.github/workflows/test-connectors-no-crs-no-mrts.yml`
- `.github/workflows/test-connectors-no-crs-with-mrts.yml`
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `.github/workflows/test-connectors-with-crs-with-mrts.yml`
- `tests/test_ci_security_workflows.py`
- dieses englisch/deutsche Change-Record-Paar

### Tests und tatsächliche Ergebnisse

`/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q
tests.test_ci_security_workflows` bestand: 35 Tests in 2.631s.
`make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
check-ci-security-contract` bestand: 110 Tests in 34.308s mit vier erwarteten
Environment-Capability-Skips. Der Cache-Contract bestand ebenfalls: 47 Tests
in 34.140s. `git diff --check` bestand vor diesem Dokumentations-Update.

### Runtime-Evidence

Die fehlgeschlagenen ersten aktualisierten Matrix-Jobs erreichten keine
Connector-Runtime; die späteren fehlenden Evidence-Variablen waren Cascade-
Failures, nachdem die beabsichtigte Revision-Assertion das Setup stoppte. Der
korrigierte Head benötigt frische Hosted-Runtime-Evidence.

### Nicht ausgeführte Prüfungen

Die korrigierten Exact-Head-GitHub-Actions-, SonarQube-Cloud-,
actionlint/ShellCheck- und zizmor-Ergebnisse stehen bis zum normalen Branch-
Push aus. Das erste aktualisierte Sonar-Ergebnis ist Evidence für die
Duplication-Reparatur, nicht dafür, dass der korrigierte Framework-Pin alle
Hosted-Jobs abgeschlossen hat.

### Bekannte Einschränkungen

Sonars `new_coverage`-Measure bleibt nicht vorhanden; die angezeigte `0.0%`
Coverage ist kein Runtime-Coverage-Anspruch. Kein lokaler Check kann die
Hosted-Matrix- und Scanner-Ergebnisse des korrigierten Heads ersetzen.

### Restrisiken

Die gewählte Framework-Revision kann ein unabhängiges Runtime-
Kompatibilitätsproblem zeigen, nachdem die Revision-Verifikation besteht. Ein
solches Problem wird weder angenommen noch verborgen; PR #279 bleibt Draft,
während der Nutzer weitere Arbeit abschließt.

### Finaler Review-Status

Der Fehler hat eine exakte, security-reviewte Ursache und eine enge lokal
validierte Korrektur. Normale Veröffentlichung und neue Exact-Head-
Verifikation sind die verbleibenden Schritte; keine Ready-Umstellung, kein
Merge und kein Auto-Merge sind autorisiert.
