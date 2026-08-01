# Finding FND-SONAR-0025: Lighttpd-Lifecycle-Fixture-Input besitzt keine verifizierte Runtime-Root-Begrenzung

**Sprache:** [English](finding.md) | Deutsch

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `security_candidate` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schwere / Confidence | `P2` / `low` / `validated` |
| Status / Feasibility | `verified` / `feasible_now` |
| Release-Blocker / sicherheitsrelevant | nein / ja |
| Sonar-Inventar | `pythonsecurity:S8707`, `AZ9cRymfHhV2CayPTPzM` |

## Zusammenfassung, Verhalten und Auswirkung

SonarQube Cloud meldete, dass `--entity-fixture-result` `Path.read_text()`
erreichte, ohne zu beweisen, dass die ausgewählte Datei zum verifizierten
privaten Runtime-Root gehört. Der kanonische Runner schreibt das Fixture
normalerweise unter sein privates Smoke-Verzeichnis, ein direkter
Lifecycle-Helper-Aufrufer konnte jedoch einen unabhängigen lesbaren Pfad
wählen. Für die übrigen datenführenden Lifecycle-CLI-Inputs fehlte dieselbe
Containment-Voraussetzung.

Der Patch wendet den bestehenden Parent-Control für private Root, absolute
Pfade, reguläre Dateien und keine Symlinks auf alle sechs Dateninputs an. Er
ändert den Fixture-Read auf den bestehenden descriptor-relativen
`O_NOFOLLOW`-Leser. Dies ist eine validierte lokale
Developer/CI/Operator-CLI-Artefaktgrenze. Es ist keine Evidence für einen
Remote-Lighttpd-HTTP-Arbitrary-File-Read-Exploit, daher ist die kalibrierte
Schwere `low` statt Sonars generischem HIGH-Impact-Label.

## Scope, Voraussetzungen und Reproduktion

- Betroffene Dateien/Symbole: `safe_runtime_output.py`,
  `write_patched_lifecycle_results.py`, `safe_input_path`,
  `read_runtime_input_text`, `load_fixture_result` und `main`.
- Ein direkter Aufrufer muss dem historischen Helper einen gewählten absoluten
  `--entity-fixture-result`-Pfad übergeben. Für eine materielle
  Cross-Privilege-Auswirkung wäre zusätzlich ein vom Private-Root-Owner
  getrennter Akteur nötig; die Repository-Evidence belegt keinen solchen.
- Die fokussierte Lifecycle-Suite übergibt für alle sechs datenführenden
  Optionen Outside-Root- und Symlink-Pfade und verlangt Ablehnung vor
  Resultat-, Projection- oder Summary-Publikation. Sie erhält außerdem den
  gültigen In-Root-Lifecycle-Control.

## Evidence

Run-ID: `lighttpd-sonar-security-20260728`.

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| `sonarqube-cloud-issue-AZ9cRymfHhV2CayPTPzM.json` | `81891db472788897c2f98e78dca90bc1ad3422f8bb296190b906bd97a7cfd45d` | Ein offenes in-scope `pythonsecurity:S8707`-Issue am Fixture-Reader. |
| `test-patched-event-validation.log` | `ce229433d6e29eec70abd1e41fb09656f335146304be8054068362ce787cc4ad` | Acht fokussierte Hostile-Path- und Legitimate-Control-Tests bestanden. |
| `test-patched-host-contract.log` | `00ea1ddd907f040d93ead44b04b4d917cbe1b93d9b23f108ce6b7c4a3f48c6c6` | Siebzehn Lighttpd-Host-Contract-Tests bestanden. |
| `security-diff-scan/report.md` | `a5e3bcfb9bbd2ce405602b0a61a9f4a5278c64b784b494865873667bd6614ae0` | Versiegelter vollständiger Review beider geänderten Source-Dateien fand keinen diff-eingeführten reportbaren Kandidaten. |

Alle Artefakte sind unter
`/var/tmp/codex/ModSecurity-conector/runs/lighttpd-sonar-security-20260728/`
aufbewahrt.

## Root Cause, Remediation und Akzeptanz

`load_fixture_result()` verwendete ein einfaches `Path.read_text()` für einen
CLI-ausgewählten Fixture-Pfad, und die Hauptfunktion übergab weitere CLI-Pfade
an Leser, ohne sie vorher an die verifizierte Root zu binden.
`safe_input_path()` delegiert nun für jeden Input an
`runtime_artifact_path(..., must_exist=True)`. Fixture-Inhalt fließt danach
durch `read_runtime_artifact_text()`, das mit No-Follow-Descriptor-Semantik
öffnet und eine reguläre Datei verifiziert.

Die Akzeptanz verlangt, dass Escape-Pfade, Symlinks, fehlende Dateien und
nicht-reguläre Fixture-Inputs vor der Publikation fehlschlagen, gültige
Lifecycle-Daten kompatibel bleiben, fokussierte Tests und der versiegelte
Diff-Review bestehen und ein exakter PR-Head das ursprüngliche Key mit null New
Issues und null New-Code-Duplikation als abwesend beweist. Draft-PR #201
erfüllt das Hosted-Exact-Head-Kriterium. Keine Sonar-Policy, Exclusion,
Suppression, `NOSONAR`, Framework-, MRTS- oder Gitlink-Änderung ist erlaubt.

## Abhängigkeiten, Controls, verwandte Findings und Restrisiko

Der exakte Head von Draft-PR #201 hat GitHub-Actions und SonarQube-Cloud-
Verifikation abgeschlossen: alle ausgeführten GitHub-Checks bestanden; das
Quality Gate ist `OK`; die OPEN/CONFIRMED-PR-Issue-Abfrage,
`new_violations` und neue Duplikatzeilen sind null; und die New-Code-
Duplikationsdichte ist `0.0`. Die relevanten Regression-Suiten sind
`test_patched_event_validation.py` und `test_patched_host_contract.py`; der
legitime Lifecycle-Control bleibt explizit erhalten.

`FND-SONAR-0001` und `FND-SONAR-0016` sind verwandter Sonar-Kontext, keine
Duplikate. Ein zukünftiger Defense-in-Depth-Change könnte JSONL-Event-Leser
auf denselben descriptor-begrenzten Leser umstellen. Innerhalb einer privaten
current-user-owned, nicht group/world-writable Root ist das verbleibende
Normal-Read-Intervall Same-Identity-Hardening statt eines belegten
Lower-Privilege-Angriffspfads.

Draft-Parent-PR [#201](https://github.com/Easton97-Jens/ModSecurity-conector/pull/201)
ist gegen `master` offen. Sein GitHub-Head, Remote-Branch und lokaler
Task-Head lösen alle auf `620ce4b8f731ee2e01fd3b9cf21abc4bc38511e6` auf.
Hosted-Checks und der Exact-Head-Sonar-Readback sind verifiziert; dieser Record
beansprucht keinen Merge und kein `master`-Ergebnis.

## Historie

- `2026-07-30T13:52:50Z`: exaktes Sonar-Issue und lokale CLI-Grenze
  revalidiert; fokussierter Patch und Regressionen abgeschlossen.
- `2026-07-30T14:12:09Z`: vollständiger Security-Diff-Report versiegelt; er
  fand keinen neu eingeführten reportbaren Security-Kandidaten.
- `2026-07-30T14:12:09Z`: Status auf `fixed` gesetzt, Exact-Draft-PR-Hosted-
  Verifikation steht aus. Kein Merge und keine `master`-Änderung erfolgten.
- `2026-07-30T14:31:00Z`: Draft-Parent-PR #201 erstellt und exakter Head über
  lokales Git, Remote-Branch und GitHub verifiziert; Hosted-Checks und Sonar
  stehen aus.
- `2026-07-30T14:32:00Z`: alle ausgeführten GitHub-Checks bestanden und die
  Exact-Head-SonarQube-Cloud-Verifikation ergab Quality Gate `OK`, null offene
  PR-Issues, null neue Violations und `0.0` / null New-Code-Duplikation. Status
  auf `verified` angehoben; kein Merge und keine `master`-Änderung erfolgten.
