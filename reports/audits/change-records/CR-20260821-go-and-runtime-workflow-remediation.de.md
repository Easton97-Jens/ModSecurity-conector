# Change Record: Go- und Runtime-Workflow-Remediation

**Sprache:** [English](CR-20260821-go-and-runtime-workflow-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260821-go-and-runtime-workflow-remediation |
| Datum (UTC) | 2026-08-21 |
| Basis-Revision | `57187eb210ab96b7e1eed22221fa367671d01820` |
| Delivery-Status | Parent-Draft-PR #313 ist task-eigen. Vor dieser gekoppelten Record-Korrektur war sein exakter Head `d06528df0daca17c66c9771dad449b5e341ad986`; alle anwendbaren PR-Checks und SonarCloud bestanden, und der kontrollierte Five-Connector-No-CRS-Run `32582786272` endete. Der aktuelle Nutzer autorisiert ausdrücklich die geschützte Integration von PR #313 und akzeptiert nur das beschriebene Risiko des noch fehlenden r13-Hostnachweises von FND-PARENT-0148. Diese Dokumentationskorrektur erzeugt einen neuen PR-Head, der vor jedem Merge erneut geprüft werden muss; ein Merge wird hier nicht behauptet. |

## Motivation und Problemstellung

Der Workflow `Update Go version` stoppte vor seinem Resolver, weil der
gemeinsame Go-Version-Contract weiterhin einen veralteten Bash-Validator
erwartete, während CodeQL den geprüften Awk-Validator verwendet. Drei
unabhängig erfasste Runtime-Workflow-Fehler benötigen außerdem eine
Parent-only-Remediation: einen Report-Root im Source-Checkout, unvollständige
Five-Connector-Fehler-Evidence und nicht verfügbare Heavy-Smoke-Component-
Reports, nachdem der ModSecurity-v3-Provenance-Guard blockiert.

Die bereits bestätigten Pfade `update-submodules.yml`,
`update-python-version.yml` und `update-workflow-tools.yml` bleiben absichtlich
unverändert. NGINX bleibt ein separater Workflowpfad. Die Dependabot-PRs #306,
#307 und #308 wurden erst geschlossen, nachdem ihre CodeQL-v4.37.7-Änderungen
auf gemergtem PR #311 und aktuellem `master` bestätigt waren; ihre Remote-
Branches bleiben erhalten.

## Akzeptanzkriterien

- Der gemeinsame Go-Contract akzeptiert den exakt vertrauenswürdigen
  Awk-Validator des eingecheckten CodeQL-Workflows und weist ungültige
  Selektoren, Pins und Versionsdateien weiterhin fail-closed ab.
- `open-connectors-smoke.yml` schreibt Runtime-Reports nur unterhalb seines
  privaten geprüften Build-Roots, niemals unterhalb von `$GITHUB_WORKSPACE`,
  und sein Initialisierungsblock besteht unter `set -eu` ohne geerbtes
  `BUILD_ROOT`.
- Das Five-Connector-Profil bewahrt die kanonische Evidence-Validierung und
  behält gleichzeitig begrenzte, private, nur bei Fehlern erzeugte Diagnose-
  Artefakte außerhalb seines Erfolgsaggregats.
- Heavy Smoke bewahrt den ModSecurity-v3-Provenance-Guard und stellt seine
  privaten Component-Reports in bestehenden Smoke-Artefakten bereit; die
  Provenance wird nicht abgeschwächt und Framework/MRTS werden nicht geändert.
- Fokussierte Regressionen und Security-Contracts bestehen. Der Final-Head-
  No-CRS-Lauf validiert die Follow-up-Capture-Korrektur; die vollständige
  Baseline bleibt unabhängig durch die Framework-eigene Provenance-Konfiguration blockiert.

## Implementierungsentscheidung und Begründung

- Der Go-Checker hält den exakt geprüften Awk-Ausdruck in
  `TRUSTED_VERSION_VALIDATOR`; Tests decken den eingecheckten CodeQL-Workflow
  ab. `update-go-version.yml` selbst bleibt publisher-gated und unverändert.
- Die Open-Connectors-Initialisierung bindet
  `build_root="$verified_root/build"`, bevor sie sowohl `BUILD_ROOT` als auch
  `RUNTIME_REPORT_OUTPUT_ROOT` exportiert. Ihre Regression führt den
  extrahierten Shell-Block mit `bash --noprofile --norc -eu` und ohne
  umgebendes `BUILD_ROOT` aus.
- Das wiederverwendbare Five-Connector-Profil schreibt identitätsgebundene
  Diagnostik nur bei Fehlern unterhalb seines privaten geprüften Roots. Der
  Artefaktname liegt absichtlich außerhalb des kanonischen
  `five-no-crs-*`-Aggregatmusters.
- Der erste korrigierte No-CRS-Lauf belegte, dass der Capture-Schritt
  `$CONNECTOR` unter `set -u` ohne Step-lokale Bindung nutzte. Er erhält jetzt
  den geschlossenen Resolver-Matrixwert explizit; der Contract-Test begrenzt
  diese Assertion auf den Capture-Schritt.
- Heavy Smoke exportiert Runtime-Component-Reports unterhalb seines bestehenden
  privaten Build-Roots und lädt sie über den etablierten Diagnose-Artefaktpfad
  hoch. Der Framework-eigene Provenance-Guard bleibt fail-closed; es gibt keine
  Framework-, MRTS-, Gitlink-, Cleanup-, Root-Broker- oder NGINX-
  Workflowänderung.

### Fortsetzung 2026-08-22: target-spezifische NGINX-Isolierung

Nach dem normalen Base-Merge erreichte der kontrollierte Five-Connector-No-CRS-
Run `32577438675` auf `ec8cccc6211534e92eba7013cf76747c135d7a4a` die
Parent-Vorbereitungsgrenze, aber alle fünf ausgewählten Nicht-NGINX-Jobs
scheiterten an `nginx_pinned_provenance_ref_mismatch`. Das Framework-Tupel
liefert separat verwaltete `release-1.31.4`-Metadaten, während Parent sein
unabhängig geprüftes `release-1.31.3`-Tupel behält. NGINX wurde nicht
gestartet; daher ist Target-Isolierung statt eines NGINX-Repins die korrekte
Reparatur.

`required_runtime_component_sources` weist unbekannte Targets jetzt fail-closed
ab und verarbeitet NGINX-URL-, Provenance- und Protokoll-Metadaten nur für
`all` und `nginx`. Einen NGINX-Connector-Plan erstellt es ebenfalls nur für
diese Targets. Die bestehenden strikten NGINX-Repository-/Tag-/Ref-/Asset-/
SHA-256- und Protokoll-/TLS-Prüfungen bleiben für `all` und `nginx`
unverändert. Dies lässt NGINX separat, macht `shared`, `apache` und `haproxy`
unabhängig von ungenutzten NGINX-Metadaten und ändert weder Framework, MRTS,
einen Gitlink, einen NGINX-Pin, einen Publisher noch einen Cleanup-Workflow.

### Fortsetzung 2026-08-22: kanonische Hostruntime-Projektion und Lighttpd-Inventar

Der Exact-Head-Folgelauf `32579807096` auf
`679ae784db021d72343fdce693f3033969227960` passierte für alle fünf
ausgewählten Connectoren den früheren Nicht-NGINX-NGINX-Guard. Apache, Envoy
und HAProxy finalisierten jeweils ein erfolgreiches Runtime-Ergebnis, aber der
unveränderte Framework-Validator verwarf danach korrekt die beiden vom Parent
erzeugten Dateien `hostruntime-record.json` und `hostruntime-summary.md`: Sie
wurden erst nach der Finalisierung erzeugt und waren nicht im kanonischen
Manifest deklariert. Der Parent projiziert nur diese zwei festen relativen
Dateien jetzt mit SHA-256-Werten in beide Artefakt-Maps und aktualisiert die
bestehende Checksumme des Manifest-Result-Artefakts erst nach Prüfung ihrer
vorherigen Bindung. Fehlgeformte Maps,
unsichere Pfade, Symlinks, nicht reguläre Dateien, Checksum-Mismatches und
Schreibfehler bleiben fail-closed; der Framework-Validator bleibt unverändert.

Der gleiche Lauf zeigte, dass der Lighttpd-Smoke selbst seine zwei Requests
bestand, aber seine finale Evidence nicht bestehen konnte, weil das
Versionsinventar einen anderen Cache-Pfad nutzte. Für das generische Profil
akzeptiert der Runner jetzt nur den festen Stage-Pfad
`CONNECTOR_BUILD_ROOT/lighttpd-connector/bin/lighttpd`, falls er eine absolute,
reguläre, ausführbare und nicht verlinkte Datei ist. Jeder fehlende oder
unsichere Stage-Binary lässt die Version bei `not_provisioned`; geerbtes
`LIGHTTPD_BIN`, System- und Shared-Cache-Fallbacks werden nicht konsumiert.
Das Full-Lifecycle-Mapping bleibt unverändert. Traefik bleibt fail-closed und
außerhalb dieses Parent-only-Fixes, weil seine vom Framework bereitgestellte
Binary eine separate Trusted-Root-Kontrolle verletzt.

### Fortsetzung 2026-08-22: Delivery-Autorisierung und FND-PARENT-0148-Scope

Der aktuelle Nutzer autorisiert nun ausdrücklich die geschützte Parent-
`master`-Integration des task-eigenen PR #313 und akzeptiert das exakte
Restrisiko von FND-PARENT-0148 nur für diese Integration. Es existiert kein
erfolgreicher privater Traefik-`no-crs/with-mrts`-Host-Receipt: r10--r12
schlugen vor Hoststart fail-closed fehl, und der normale PR-#313-Run beobachtete
einen Trusted-Root-Containment-Block vor Requests erneut. Die Akzeptanz
verifiziert oder schließt den Finding nicht, lockert keinen Control und endet
mit dem ersten frischen r13-Ergebnis. Ein Fehler muss über einen neuen PR
behoben werden, niemals direkt auf `master`.

Der historische r13-Runner gehört nicht zu PR #313 und benötigt eine separate
Parent-Runtime-Aufgabe mit vorbereiteten read-only-Framework-/MRTS-Inputs. Er
kann weder als exakter PR-#313-Check beansprucht noch aus diesem PR-Checkout
gestartet werden. NGINX bleibt getrennt und wurde nicht gestartet.

## Security-Auswirkung

Diese Änderung berührt GitHub-Actions-Runtime-Pfade, Artefakt-Evidence und
einen Update-Contract. Sie bewahrt gepinnte Actions, read-only-Berechtigungen,
deaktivierte Checkout-Credential-Persistenz, fail-closed-Evidence-Aggregation
und den ModSecurity-v3-Provenance-Guard. Ein fokussierter Diff-Review fand,
dass der erste Open-Connectors-Patch eine nicht gesetzte Shell-Variable
`BUILD_ROOT` referenzierte; die Korrektur bindet den Wert an den
vertrauenswürdigen geprüften Root und die verstärkte Regression reproduziert die
`set -eu`-
Kontrolle. Der abschließende fokussierte Review fand kein verbleibendes
berichtspflichtiges Security-Kandidatenfinding.

## Geänderte Dateien

- `.github/workflows/open-connectors-smoke.yml`
- `.github/workflows/reusable-five-connectors-profile.yml`
- `.github/workflows/test-full-smoke-sequential.yml`
- `ci/checks/common/check-go-version-contract.py`
- `ci/provisioning/components/prepare-runtime-components.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `ci/runtime/lifecycle/resolve-lighttpd-host-binary.py`
- `ci/runtime/lifecycle/write-hostruntime-record.py`
- `tests/test_all_connectors_no_crs_workflow_contract.py`
- `tests/test_full_smoke_workflow_contract.py`
- `tests/test_go_version_contract.py`
- `tests/test_prepare_runtime_components.py`
- `tests/test_resolve_lighttpd_host_binary.py`
- `tests/test_hostruntime_record.py`
- `tests/test_runtime_env_snapshot_contract.py`
- `tests/test_runtime_path_policy.py`
- dieses gekoppelte Change-Record-Paar sowie
  `reports/audits/change-records/README.md` /
  `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Go-/Updater-, Five-Connector-, Heavy-Smoke- und Open-Connectors-Contracts | bestanden: 34 Tests |
| `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-go-version-contract` | bestanden |
| CI-Security- und Python-Version-Contracts | bestanden: 52 Tests |
| Follow-up-Five-Connector-Contracts nach Step-lokaler Matrix-Bindung | bestanden: 17 Tests |
| Follow-up-CI-Security-Contracts nach Step-lokaler Matrix-Bindung | bestanden: 28 Tests |
| `git diff --check` | bestanden |
| Fokussierte Open-Connectors-`set -eu`-Shell-Regression | bestanden: 1 Test; der private Report-Root wurde exakt exportiert |
| Fokussierter Security-Re-Review | bestanden: kein verbleibender Kandidat für den korrigierten Open-Connectors-Pfad |
| `python -m py_compile tests/test_prepare_runtime_components.py ci/provisioning/components/prepare-runtime-components.py` | bestanden |
| `python -m unittest -v tests.test_prepare_runtime_components` | bestanden: 43 Tests; 5 erwartete Skips, weil der Task-Worktree den Framework-Gitlink nicht initialisiert |
| `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract` | bestanden: 123 Tests; 5 erwartete Namespace-/Identity-Skips; `actionlint`-, `zizmor`- und `gitleaks`-Lock-Validierung bestanden |

## Runtime-Evidence

Die ursprünglichen Hosted-Fehler bleiben als Evidence erhalten: Go-Run
`32006247568`, Open-Connectors-Run `32485037344`, Five-Connector-No-CRS-Run
`32485072808` und Heavy-Smoke-Run `32485033800`. Auf dem Exact-Draft-PR-Head
`a0c527cdb57ec97c663e983c4fbe195a6f2361b0` bestanden der korrigierte Go-
Contract und die Pull-Request-Checks. Open-Connectors-Run `32494251838`
initialisierte seinen privaten Report-Root erfolgreich vor dem unabhängigen
Provenance-Blocker; Heavy-Smoke-Run `32494271540` bewahrte No-CRS- und
With-CRS-Reports auf und forderte kein Cleanup an. Die Aufgabe startet nur
sichere read-only-/no-cleanup-Workflows; Publisher, Artefakt-Löschung,
Root-Broker und Framework-/MRTS-Aktionen sind nicht enthalten.

Der erste korrigierte Five-Connector-No-CRS-Lauf `32494262558` bewahrte die
neuen privaten Diagnose-Artefakte auf und legte das nun korrigierte nicht
gesetzte `$CONNECTOR` im Capture-Schritt offen. Der Successor-Lauf des finalen
Code-Heads `32495576734` auf `bf21d726f3d998a333ce57dc935efa2d8782a75c`
schloss Capture und Upload bounded diagnostics für alle fünf Connectoren ab.
Sein Result-only-Aggregat scheiterte fail-closed, weil alle fünf weiterhin den
gemeinsamen Blocker `modsecurity_v3_provenance_configuration_failed` erreichten.

Der spätere kontrollierte Five-Connector-No-CRS-Run `32577438675` auf dem
Merged-Base-Head `ec8cccc6211534e92eba7013cf76747c135d7a4a` ist begrenzte
Evidence für einen separaten Parent-Target-Scope-Defekt: Apache, HAProxy,
Envoy, Traefik und Lighttpd stoppten alle an
`nginx_pinned_provenance_ref_mismatch`, bevor ihre eigenen Runtime-Stufen
erreicht wurden. Der wiederverwendbare Workflow wählte Apache/HAProxy oder
`shared` und startete NGINX nicht. Seine secret-free aufbewahrte
Diagnosezusammenfassung ist hash-gebunden im Task-Evidence-Manifest. Ein Rerun
auf dem nachfolgenden exakten PR-Head endete dann als `32582786272` auf
`d06528df0daca17c66c9771dad449b5e341ad986`: Apache, HAProxy, Envoy und
Lighttpd bestanden Runtime-Smoke, kanonische Evidence, Publish und Cleanup.
Traefik stoppte korrekt vor Requests an seiner separaten Trusted-Root-Kontrolle,
weil die gestagte Binary unter dem geforderten Shared-Cache-Root lag; das
Aggregat schlug daher fail-closed fehl. Für diese Fortsetzung wurde kein
NGINX-, Publisher-, Lösch-, Root-Broker-, Framework- oder MRTS-Workflow
gestartet.

## Nicht ausgeführte Prüfungen mit Begründung

`actionlint` und `zizmor` sind in der verfügbaren Umgebung nicht installiert.
Framework-abhängige Aggregatprüfungen können nicht laufen, weil der
Task-Worktree einen nicht initialisierten Framework-Gitlink enthält; er wird
absichtlich weder initialisiert noch verändert. Die kontrollierte Final-Code-
Head-No-CRS-Ausführung und die anwendbaren PR-Checks endeten vor dieser reinen
Dokumentationskorrektur; der neue Head benötigt vor dem Merge eigene
Exact-Head-Checks.

Der gewünschte r13-Nachweis wird hier nicht ausgeführt: Sein historischer
Runner fehlt in PR #313, liegt auf einem separaten historischen Parent-Branch
und benötigt separat autorisierten Runtime-Scope mit vorbereiteten read-only-
Framework-/MRTS-Inputs. Es wäre weder sicher noch wahrheitsgemäß, den normalen
No-CRS-Run zu ersetzen, einen verschachtelten Checkout zu initialisieren oder
ein historisches r13-Ergebnis als PR-#313-Evidence zu behandeln.

## Bekannte Einschränkungen

Die Five-Connector- und ModSecurity-v3-Findings gelten durch die neue
Diagnostik allein nicht als behoben. Ihre historischen direkten Job-Logs sind
nicht verfügbar und der Provenance-Guard ist Framework-eigen. Die nächsten
korrigierten Hosted-Läufe müssen zuerst die Connector-Fehler klassifizieren und
den Component-Report bereitstellen, bevor eine zugrundeliegende Connector- oder
Framework-Ursache repariert werden kann.

Das lokale Runtime-Path-Aggregat behält einen umgebungsblockierten Self-Test
und fünf Framework-Gitlink-abhängige HAProxy-Skips; der Task initialisiert,
aktualisiert oder verändert dieses Submodule absichtlich nicht. Sie decken die
neue Target-Scope-Regression nicht ab; dafür bestehen eigene fokussierte
Kontrollen und das vollständige Modul `tests.test_prepare_runtime_components`.

## Verbleibende Risiken

Diagnose-Artefakte enthalten begrenzte Runtime-/Log-/Report-Evidence und
müssen frei von Secrets bleiben. Die aktuellen Workflows übergeben keine
Repository-Secrets, behalten `contents: read` und trennen das Diagnoseartefakt
vom kanonischen Erfolgsaggregat. Der Hosted Runner bleibt die notwendige finale
Ausführungsgrenze für das korrigierte Workflowverhalten.

Für die geschützte Integration von PR #313 allein akzeptierte der aktuelle
Nutzer das oben beschriebene verbleibende FND-PARENT-0148-Risiko, während r13
aussteht. Es ist auf das Fehlen eines erfolgreichen privaten Traefik-
no-CRS/with-MRTS-Receipts begrenzt und kann einen späteren Fehler vor oder
während Transaktions-, Audit-/Receipt- oder Cleanup-Validation umfassen. Es
schwächt die fail-closed-Controls nicht und erstreckt sich nicht auf Framework,
MRTS, Gitlinks, NGINX, einen anderen PR oder einen direkten Master-Write.

## Finaler Diff- und Review-Status

Die Parent-only-Source-Änderung liegt in Draft-PR #313. Die drei ersetzten
Dependabot-PRs sind geschlossen, ihre Branches bleiben erhalten. Der aktuelle
Nutzer hat die geschützte Integration von PR #313 allein autorisiert,
vorbehaltlich frischer Exact-Head-PR-Verifikation nach dieser Record-
Aktualisierung. Keine Branch-Löschung, Framework-/MRTS-Modifikation, NGINX-
Konsolidierung, direkter Master-Write oder Control-Lockerung ist autorisiert
oder wird behauptet. Die Fortsetzungs-Source- und Regression-Änderung hat
einen zweiten fokussierten Security-Review ohne High-/Critical-Finding außer
dem ausdrücklich erfassten und scope-begrenzten Restrisiko FND-PARENT-0148.
