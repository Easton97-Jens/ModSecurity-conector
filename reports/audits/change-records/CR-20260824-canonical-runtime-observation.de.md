# Change Record CR-20260824: Abschluss des kanonischen Runtime-Observation-Vertrags

**Sprache:** [English](CR-20260824-canonical-runtime-observation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260824-canonical-runtime-observation` |
| Datum (UTC) | `2026-08-24` |
| Basis-Revision | `e776ab75a4e2689955b9c42df6e962e06598c70b` |
| Repository / Scope | Parent-only Runtime-Observation-Contract-Abschluss für Draft PR #338; keine Framework- oder MRTS-Source, kein Gitlink, Workflow-, Pin-, Berechtigungs-, Coverage-Transfer-, NGINX-Broker-, HAProxy-Artifact-Upload-, Dependency- oder Root-Runtime-Change. |
| Vorheriger verifizierter PR-Head | `e776ab75a4e2689955b9c42df6e962e06598c70b` |
| Finale Source-Revision | Ausstehend bis zum autorisierten normalen, nicht umschreibenden Commit und Push zu `codex/canonical-runtime-observation`. Der finale SHA wird bewusst im PR statt in einer selbstreferenziellen Commit-Schleife festgehalten. |
| Delivery-Disposition | PR #338 bleibt Draft. Kein neuer Branch/PR, Merge, Auto-Merge, Ready-for-review-Übergang, Rebase, Force-Push oder Default-Branch-Aktion ist autorisiert. |

## Motivation und Problemstellung

Der bisherige Parent-Vertrag schloss Adapter-Identitätstupel nicht vollständig,
wies nicht jede öffentliche Framework-Erwartungsform direkt nach und konnte
Host-Runtime-Ergebnisse mit Framework-Case-Kardinalität vermischen. Die
Korrektur muss die bestehenden Connector-Trust-Boundaries bewahren und jede
PASS-relevante Tatsache explizit und prüfbar machen.

## Akzeptanzkriterien

Die gemeinsamen Runtime-Observation-Lücken ohne Framework-Source-Import
schließen:

- `identity.adapter_id` verpflichtend machen und ein geschlossenes
  Connector-/Adapter-/Integration-Tupel validieren;
- die öffentliche 14-Arten-Framework-Erwartungsunion mit begrenzter,
  geschlossener rekursiver `compound`-Semantik und ohne öffentlichen
  `rule_id`-Output spiegeln;
- explizite typisierte Host-Fakten für jede PASS-relevante Assertion verlangen;
- Producer, Raw-Logs, Digests, Fixtures, Step-Success und nachgelagerte
  Kompatibilitätschecks daran hindern, Runtime- oder Framework-PASS zu
  erzeugen;
- ein Run-Aggregat mit eindeutigen Framework-Cases und geprüften
  Kardinalitätsgleichungen verwenden; und
- korrekte zweisprachige Traceability, lokale Security-Evidence und Exact-
  Head-Delivery-Evidence aufbewahren.

## Implementierungsentscheidung und Begründung

Der geschlossene Katalog ist:

| Connector | `adapter_id` | `integration_mode` |
| --- | --- | --- |
| Apache | `apache-native-httpd-module` | `native-httpd-module` |
| Envoy | `envoy-ext-proc-service` | `ext_proc` |
| Lighttpd | `lighttpd-patched-native-module` | `patched-native-lighttpd` |
| Traefik | `traefik-native-middleware` | `native-traefik-middleware` |
| NGINX | `native-nginx-http-module` | `native-nginx-http-module` |
| HAProxy SPOE/SPOP | `haproxy-spoe-spop-agent` | `spoe-spop-agent` |
| HAProxy native HTX | `haproxy-native-htx-filter` | `native-htx-filter` |

Der generische Live-Adapter bleibt auf Envoy, Lighttpd und Traefik begrenzt.
Apache und beide HAProxy-Pfade haben nur kanonische Fixtures und schlagen für
Live-Claims geschlossen fehl; die geschützte NGINX-Broker-Grenze bleibt
unverändert. Getrennte HAProxy-Fixtures verhindern Evidence-Crossing zwischen
SPOE/SPOP und native HTX.

Die öffentliche Erwartungsunion ist exakt `http_status`, `intervention`,
`action`, `rule_match`, `event`, `request_headers`, `response_headers`,
`request_body`, `response_body`, `transport`, `lifecycle`, `cleanup`,
`compound` und `not_applicable`. Legacy-`rule_id` wird nur an der
Kompatibilitätsgrenze zu `rule_match` normalisiert. Schema-`oneOf` und
`additionalProperties: false` formen die Union; Python bleibt der maßgebliche
semantische Validator. `compound` begrenzt die Tiefe auf vier und Bedingungen
auf 2–16, weist leere/doppelte/unbekannte/unsichere Members, Raw-Payloads/-Logs
und absolute Pfade zurück.

`StructuredObservationInput` erhält jetzt benannte Konfigurations-, Start-,
Reachability-, Expected-/Observed-Status-, Action-, Trigger-, Intervention-,
Framework- und Cleanup-Fakten. Fehlende Fakten bleiben `PARTIAL` oder
`VALIDATION_FAILED`; Abweichungen bleiben failed. Digests binden Dateien, aber
ersetzen nie eine Observation.

Für den ausgewählten CRS-Smoke leitet der Parent-Normalizer einen
`crs_sqli_anomaly_block`-Case erst ab, nachdem er die typisierten Live-
Host-Fakten separat validiert hat. Er kopiert keinen Framework-Status aus einem
Producer, und das spätere öffentliche Framework-Kommando `validate` ist nur
kompatibilitäts-only: Es kann kein Parent-Ergebnis hochstufen und keine
Framework-Source-/Runner-Execution behaupten. Das Run-Aggregat prüft
`selected = executed + unsupported + not_applicable + not_executed` und
`executed = passed + failed + cancelled`; die Framework-Szenariokategorie
bleibt Framework-Metadata statt einer profilabgeleiteten Parent-Kategorie.

Der Validator schlägt zusätzlich für nicht hashbare geschlossene Literale sowie
übermäßiges/zyklisches Metadata geschlossen fehl. Envoy und Lighttpd leiten
CRS-Intervention-IDs aus validierten strukturierten Final-Events statt aus
Summary-Literalen ab; der Normalizer prüft sie erneut. `FND-PARENT-0307`
bleibt mit ausstehender finaler Exact-Head-Evidence fixed. Die erste exakte
Runtime-Beobachtung eröffnete `FND-PARENT-0308` und `FND-PARENT-0309` erneut
als `in_progress`, statt einen lokal bestandenen Unit-Test als Host-Runtime-
Nachweis zu behandeln.

SonarQube Cloud meldete danach auf dem exakten Head
`245503cdf75ae58f1077ed4c5679f9640c12ce4a` acht task-eigene
Maintainability-Issues: sechs Cognitive-Complexity-Findings und einen
verschachtelten Ausdruck im Contract-Validator sowie ein
Cognitive-Complexity-Finding im Normalizer. Der normale Successor
`a7b8cc199e01f6403616792c598068d24ff645ee` extrahierte ausschließlich die
vorhandene Metadata-Traversierung, Expectation-Normalisierung,
Case-/Aggregate-Validierung und das Framework-Execution-Predicate in private
Helper. Sein exakter Check `97619927966` bestand das Quality Gate, meldete aber
noch drei task-eigene Issues: Metadata- und Expectation-Dispatch-Komplexität
sowie einen unbenutzten privaten Case-Parameter. Der zweite enge Successor
`ee7585250f2d7af6279a5fd1b847b76a87a15c99` teilte diese verbleibenden privaten
Pfade auf und entfernte den unbenutzten Parameter, ohne den geschlossenen
Katalog, Evidence-Reads, PASS-Regeln oder Trust-Boundaries zu ändern. Sein
exakter SonarQube-Cloud-Check `97624800934` bestand mit null New Issues. Der
terminale Runtime-Workflow offenbarte danach zwei separate Parent-only-
Integrationsfehler: Common emittiert Envoy-`rule_id` als kanonischen JSON-Text,
während der Harness nur Python-Integer akzeptierte; und das Legacy-externe
`event.json` leakte das interne `framework_case`-Aggregat in eine strikte
Framework-Kompatibilitätsform. Der dritte enge Successor
`efc2505b76734c19a0ca5766dabb268678dabc12` akzeptiert nur kanonischen
begrenzten Decimal-Text (oder einen Integer), bewahrt die exakte
`949110`-Prüfung und hält das Aggregat ausschließlich in der kanonischen
Runtime-Observation. Sein exakter SonarQube-Cloud-Check `97632932827` hatte
erneut null New Issues, doch sein terminaler Runtime-Workflow `32791114544`
offenbarte eine weitere externe Shape-Inkompatibilität: Nachdem Envoy,
Lighttpd und Traefik jeweils erfolgreiche Host-Runtime und Parent-
Normalisierung gemeldet hatten, wies der strikte Consumer
`event.host_configuration.reachability_status` zurück. Apache und HAProxy
bestanden. Diese vierte enge Parent-only-Korrektur bewahrt Reachability nur im
Raw-Host-Log und in der kanonischen Runtime-Observation und lässt sie aus dem
Legacy-externen Event aus. `FND-SONAR-0060` bleibt verfolgt, bis der neue
exakte gepushte Head erneut null New Issues ohne Suppression oder Scanner-
Control-Änderung nachweist.

## Geänderte Dateien

- `ci/runtime/contracts/README.md` und `ci/runtime/contracts/README.de.md`
- `ci/runtime/contracts/runtime-observation.schema.json`
- `ci/runtime/contracts/runtime_observation.py`
- `ci/runtime/contracts/runtime_observation_adapters.py`
- `ci/runtime/contracts/validate-runtime-observation.py`
- `ci/runtime/lifecycle/normalize-with-crs-no-mrts.py`
- `ci/runtime/lifecycle/run-with-crs-no-mrts.sh`
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh`
- `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `tests/fixtures/runtime-observation/apache-no-crs-no-mrts.json`
- gelöscht `tests/fixtures/runtime-observation/haproxy-no-crs-no-mrts.json`
- hinzugefügt `tests/fixtures/runtime-observation/haproxy-spoe-spop-no-crs-no-mrts.json`
- hinzugefügt `tests/fixtures/runtime-observation/haproxy-native-htx-no-crs-no-mrts.json`
- `tests/test_runtime_observation_contract.py`
- `tests/test_with_crs_no_mrts_runtime.py`
- dieser Change Record und sein deutscher Companion.

## Ausgeführte Befehle

| Check | Tatsächliches Ergebnis |
| --- | --- |
| `python3 -m unittest -q tests.test_runtime_observation_contract tests.test_with_crs_no_mrts_runtime` | Nach dem vierten Runtime-Follow-up bestanden: `126 tests in 92.700s`. Dies deckt die verlangten Identity-, Union-, Compound-, Explicit-Fact-, Aggregate-, HAProxy-, NGINX-, Path-/Evidence- und No-Fabricated-PASS-Regressionen ab. |
| Fokussierte Runtime-Follow-up-Regression (`test_envoy_intervention_rule_id_accepts_only_canonical_json_values` plus All-Connector-Normalizer-Realisation) | Bestanden: `2 tests in 8.541s`. Sie führt den exakten Envoy-Inline-Parser mit der produktiven JSON-Text-Form aus und weist nichtkanonische oder unbegrenzte Formen ab; außerdem bestätigt sie, dass das externe Event `framework_case` auslässt, während das kanonische Aggregat gültig bleibt. |
| Fokussierte vierte Runtime-Follow-up-Regression (All-Connector-Normalizer-Realisation und exakte External-Event-Records) | Bestanden: `2 tests in 10.843s`. Sie bestätigt, dass die kanonische Runtime-Observation `reachability.observed == {"status": "PASS"}` behält, während das externe `event.host_configuration` `reachability_status` auslässt. |
| Benutzergeforderter kombinierter Verbose-Befehl mit `tests.test_ci_security_workflows` | Die `126` Contract-/Normalizer-Cases bestanden; der Befehl führte `127` Einträge in `41.392s` aus, wobei das letzte Modul wegen des fehlenden lokalen `PyYAML`-Imports als ein Fehler gemeldet wurde. Keine Dependency wurde installiert oder geändert. |
| `tests.test_runtime_path_security`, `tests.test_evidence_output_security`, `tests.test_bilingual_docs` und `tests.test_envoy_transport_hardening_contract` | Nach dem vierten Runtime-Follow-up bestanden: `70 tests in 10.468s`. |
| Direkte `tests.test_bilingual_docs`-Bestätigung | Nach der finalen Change-Record-Aktualisierung erneut bestanden: `22 tests in 0.288s`. |
| Shell-Syntax des CRS/no-MRTS-Runner- und Envoy-Harness-Skripts | Bestanden. |
| Erforderliche `py_compile`-Dateien | Bestanden: Exit `0`. |
| `python3 -m json.tool ci/runtime/contracts/runtime-observation.schema.json /dev/null` | Bestanden. |
| `git diff --check` | Bestanden. |
| Security-Diff-Review | Der versiegelte Scan für `a7b8cc19` endete mit null reportable Findings. Nachfolgende fokussierte Delta-Reviews des verbleibenden semantischen Refactors und des dritten Parser-/Kompatibilitäts-Follow-ups fanden ebenfalls kein reportable Finding. Der frische Review dieser vierten External-Field-Auslassung fand weder ein reportable Finding noch einen False-PASS-Pfad: kanonische Reachability, Raw-Evidence, Digest-Binding und fail-closed Validation bleiben intakt. Der Same-UID-Private-Runner-Writer ist eine explizite Trusted-Runner-Boundary-Einschränkung, kein stillschweigend unterdrücktes Finding. |

Die genaue lokale `PyYAML`-Import-Einschränkung ist eine Umgebungs-Evidence-
Lücke, kein Produkt-Erfolg und kein Grund, den CI-Security-Test zu schwächen.

## Nicht ausgeführte Prüfungen mit Begründung

`tests.test_ci_security_workflows` wurde über den benutzergeforderten
kombinierten Befehl aufgerufen, konnte in diesem lokalen Interpreter wegen des
fehlenden `PyYAML` jedoch nicht importieren. Kein Dependency-Setup war
autorisiert; dies bleibt eine ehrliche lokale Grenze statt eines übersprungenen
oder gelockerten Tests. Exact-Head-GitHub-Actions, SonarQube Cloud und der
terminale Connector-Runtime-Workflow müssen nach jedem normalen Push erneut
geprüft werden.

`make check-doc-links` wurde ebenfalls ausgeführt und meldet nur die sechzehn
bereits bestehenden Links in den absichtlich nicht initialisierten Framework-
Gitlink; ein task-eigener Change-Record-Defekt wird nicht gemeldet. Dieses
separate Repository zu initialisieren oder zu ändern liegt außerhalb des
Parent-only-Tasks.

## SonarQube Cloud und Coverage

Der exakte Head `245503cdf75ae58f1077ed4c5679f9640c12ce4a` bestand sein
Quality Gate, meldete aber im SonarQube-Cloud-Check `97609857745` acht New
Issues. Der erste normale Successor
`a7b8cc199e01f6403616792c598068d24ff645ee` reduzierte sie im exakten Check
`97619927966` bei weiter bestandenem Quality Gate auf drei. Der zweite enge
Successor `ee7585250f2d7af6279a5fd1b847b76a87a15c99` bestand den exakten Check
`97624800934` mit null New Issues. Der dritte enge Successor
`efc2505b76734c19a0ca5766dabb268678dabc12` bestand den exakten Check
`97632932827` mit null New Issues und null Annotations. Dieses Ergebnis beweist
nicht diesen vierten korrektiven Successor: Sein eigenes Exact-Head-Sonar-
Ergebnis muss erneut null New Issues zeigen, bevor die Delivery verifiziert ist.
Es wurde keine Suppression, kein `NOSONAR`, keine Exclusion, Acceptance,
Quality-Gate-Änderung oder Coverage-Workflow-Änderung vorgenommen.

```text
No Python coverage report is supplied to SonarCloud.
0.0% is not treated as measured test coverage.
```

## Runtime-Evidence

Die lokalen Tests validieren Contracts, strukturiertes Normalizer-Verhalten,
Fixture-Identity und File-Safety-Controls. Sie sind kein Live-Host-Runtime-
Ergebnis.
Der exakte Workflow `32788272062` für `ee758525` endete nach erfolgreichen
Apache- und HAProxy-Läufen terminal fehlgeschlagen: Envoy wies den gültigen
strukturierten String `"949110"` ab; Lighttpd und Traefik schlossen ihre
Host-Pfade ab, aber der strikte Kompatibilitäts-Consumer wies den zusätzlichen
externen `framework_case`-Key zurück. Dies sind aus Logs abgeleitete Ursachen,
keine wiederholten oder inferierten Fehler.

Der exakte Successor-Workflow `32791114544` für `efc2505b` endete ebenfalls
ohne Retry terminal fehlgeschlagen. Apache und HAProxy bestanden; Envoy,
Lighttpd und Traefik meldeten jeweils erfolgreiche Host-Runtime und Parent-
Normalisierung, bevor derselbe strikte Kompatibilitäts-Consumer das schema-
verbotene externe Feld `host_configuration.reachability_status` zurückwies.
Dies ist ein Downstream-External-Event-Shape-Defekt, kein Nachweis einer
fehlgeschlagenen Reachability oder eines fabrizierten PASS.

## Bekannte Einschränkungen

Es wurden weder Apache- noch HAProxy-Live-Producer implementiert, keine
Live-Six-Connector-by-Four-Profile-Matrix behauptet und Framework/MRTS nicht
initialisiert oder verändert. Die vierte Parent-only-Reparatur erfordert jetzt
einen neuen normalen Push sowie frische Exact-Head-GitHub-Workflow-, SonarQube-
Cloud- und anwendbare PR-Check-Evidence. Jeder Fehler erfordert Log-basierte
Diagnose vor einem weiteren Commit.

## Security-Auswirkung

Der versiegelte lokale Scan für `a7b8cc19` verwendete Threat Model, Candidate
Discovery, Validation, Attack-Path-Analyse, fokussierte Regressionen und einen
unabhängigen Read-only-Review; er fand null reportable Findings. Der spätere
fokussierte Delta-Review des verbleibenden semantischen Refactors fand ebenfalls
kein reportable Finding. Ein fokussierter Review des Parser- und
Kompatibilitätsform-Follow-ups fand ebenfalls kein reportable Security-Finding
oder False-PASS-Bypass. Der frische Review dieser vierten External-Field-
Auslassung fand ebenfalls weder ein reportable Finding noch einen False-PASS-
Pfad; kanonische Reachability, Raw-Evidence, Digest-Binding und fail-closed
Validation bleiben aktiv. Keine Security-Control oder Trust-Boundary wurde für
diese Änderung gelockert.

## Verbleibende Risiken

Die dokumentierte Same-UID-Private-Root-Einschränkung bleibt, weil ein bereits
innerhalb dieses Roots autorisierter Akteur im Trusted-Runner-Modell liegt;
Attestation/Signatures wären ein separater Scope.

## Finaler Diff- und Review-Status

Der erste Task-Commit `f2fcb71f47e69f33d888dd89e1b871656e02fc38` wurde normal
zum bestehenden PR-#338-Branch gepusht. Sein Exact-Head-`lint`-Run meldete die
fehlenden erforderlichen Template-Abschnitte dieses Change Records; die
fokussierte Dokumentationskorrektur
`245503cdf75ae58f1077ed4c5679f9640c12ce4a` war die daraus folgende
Remediation und kein blinder Rerun. Dieser Head bestand lint, aber SonarQube
Cloud fand acht Maintainability-Issues. Die normalen Successors `a7b8cc19`
und `ee758525` reduzierten sie auf drei und dann null. Der terminale Runtime-
Fehler des letzteren wurde aus den exakten Envoy-, Lighttpd- und Traefik-Logs
diagnostiziert; die dritte enge Parent-only-Korrektur erreichte null Exact-Head-
Sonar-Issues, doch ihr eigener terminaler Runtime-Fehler wurde erneut aus den
exakten Envoy-, Lighttpd- und Traefik-Logs diagnostiziert. Diese vierte enge
Parent-only-Korrektur geht dem nächsten normalen Follow-up-Commit/-Push voraus.
Danach müssen alle Exact-Head-Checks, SonarQube Cloud und `Connector runtime
with CRS and no MRTS` erneut beobachtet werden. PR #338 bleibt Draft; Merge,
Auto-Merge, Ready-Übergang, Rebase und Force-Push sind weder behauptet noch
autorisiert.
