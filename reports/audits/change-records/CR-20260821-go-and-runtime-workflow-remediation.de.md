# Change Record: Go- und Runtime-Workflow-Remediation

**Sprache:** [English](CR-20260821-go-and-runtime-workflow-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260821-go-and-runtime-workflow-remediation |
| Datum (UTC) | 2026-08-21 |
| Basis-Revision | `57187eb210ab96b7e1eed22221fa367671d01820` |
| Delivery-Status | Ein Parent-only-Task-Branch und Draft-PR sind autorisiert. Initiale Hosted-Evidence wurde auf `a0c527cdb57ec97c663e983c4fbe195a6f2361b0` erhoben; der finale Code-Head `bf21d726f3d998a333ce57dc935efa2d8782a75c` bestand die anwendbaren PR-Checks und sein Successor-No-CRS-Lauf validierte jeden Diagnostic-Capture-/Upload-Schritt. Ein Merge ist nicht autorisiert. |

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

## Security-Auswirkung

Diese Änderung berührt GitHub-Actions-Runtime-Pfade, Artefakt-Evidence und
einen Update-Contract. Sie bewahrt gepinnte Actions, read-only-Berechtigungen,
deaktivierte Checkout-Credential-Persistenz, fail-closed-Evidence-Aggregation
und den ModSecurity-v3-Provenance-Guard. Ein fokussierter Diff-Review fand,
dass der erste Open-Connectors-Patch eine nicht gesetzte Shell-Variable
`BUILD_ROOT` referenzierte; die Korrektur bindet den Wert an den vertrauenswür-
digen geprüften Root und die verstärkte Regression reproduziert die `set -eu`-
Kontrolle. Der abschließende fokussierte Review fand kein verbleibendes
berichtspflichtiges Security-Kandidatenfinding.

## Geänderte Dateien

- `.github/workflows/open-connectors-smoke.yml`
- `.github/workflows/reusable-five-connectors-profile.yml`
- `.github/workflows/test-full-smoke-sequential.yml`
- `ci/checks/common/check-go-version-contract.py`
- `tests/test_all_connectors_no_crs_workflow_contract.py`
- `tests/test_full_smoke_workflow_contract.py`
- `tests/test_go_version_contract.py`
- `tests/test_runtime_path_policy.py`
- dieses gekoppelte Change-Record-Paar und die gekoppelten Archivindizes

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

## Nicht ausgeführte Prüfungen mit Begründung

`actionlint` und `zizmor` sind in der verfügbaren Umgebung nicht installiert.
Framework-abhängige Aggregatprüfungen können nicht laufen, weil der
Task-Worktree einen nicht initialisierten Framework-Gitlink enthält; er wird
absichtlich weder initialisiert noch verändert. Die Final-Code-Head-No-CRS-
Ausführung und die anwendbaren PR-Checks sind abgeschlossen; kein Merge ist
autorisiert.

## Bekannte Einschränkungen

Die Five-Connector- und ModSecurity-v3-Findings gelten durch die neue
Diagnostik allein nicht als behoben. Ihre historischen direkten Job-Logs sind
nicht verfügbar und der Provenance-Guard ist Framework-eigen. Die nächsten
korrigierten Hosted-Läufe müssen zuerst die Connector-Fehler klassifizieren und
den Component-Report bereitstellen, bevor eine zugrundeliegende Connector- oder
Framework-Ursache repariert werden kann.

## Verbleibende Risiken

Diagnose-Artefakte enthalten begrenzte Runtime-/Log-/Report-Evidence und
müssen frei von Secrets bleiben. Die aktuellen Workflows übergeben keine
Repository-Secrets, behalten `contents: read` und trennen das Diagnoseartefakt
vom kanonischen Erfolgsaggregat. Der Hosted Runner bleibt die notwendige finale
Ausführungsgrenze für das korrigierte Workflowverhalten.

## Finaler Diff- und Review-Status

Die Parent-only-Source-Änderung liegt in Draft-PR #313. Die drei ersetzten
Dependabot-PRs sind geschlossen, ihre Branches bleiben erhalten. Keine neue
Master-Integration, Branch-Löschung, Framework-/MRTS-Modifikation oder NGINX-
Konsolidierung ist autorisiert oder wird behauptet.
