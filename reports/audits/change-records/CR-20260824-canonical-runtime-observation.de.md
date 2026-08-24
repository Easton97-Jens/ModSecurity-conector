# Change Record CR-20260824: Canonical Runtime-Observation-Vertrag

**Sprache:** [English](CR-20260824-canonical-runtime-observation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260824-canonical-runtime-observation` |
| Datum (UTC) | `2026-08-24` |
| Basis-Revision | `232b020cac23d5edc0e18adaf502468bb3012237` |
| Source-Implementation-Revision | `ebb1aa565c0fd1e88efef454a5807640daf6adcd` |
| Scope | Parent-only versionierter Runtime-Observation-Vertrag, strikter Validator/CLI, Contract-Fixtures/-Tests, Envoy-/Lighttpd-/Traefik-Normalizer-Integration, Hardening des sicheren Raw-Evidence-Lesers und gekoppelte Traceability. Keine Framework-/MRTS-Source oder Gitlink, Workflow-, Berechtigungs-, NGINX-Broker-, HAProxy-Artifact-Upload-, Root-Runtime- oder Dependency-Änderung. |

## Motivation und Problemstellung

Connector-spezifische Runtime-Evidence hatte zuvor keinen gemeinsamen,
versionierten Vertrag, der eine strikte Entscheidung ohne Behandlung eines
erfolgreichen CI-Steps oder synthetischen Inputs als Live-Runtime-Proof treffen
kann. Diese Änderung führt ein Canonical-Observation-Schema und einen Validator
mit einem expliziten Evidence- und Provenance-Modell ein. Fehlende Apache- und
HAProxy-Live-Producer bleiben fail-closed, während die separate geschützte
NGINX-Grenze erhalten bleibt.

## Akzeptanzkriterien

- Versioniertes Schema, öffentliche `validate_runtime_observation()`-API und
  strikte CLI akzeptieren nur vollständige, identity-bound Observations.
- Eine Profil-Requirement-Matrix steuert alle vier CRS-/MRTS-Profile und
  promoted kein fehlendes `live_executed` zu PASS.
- Envoy-, Lighttpd- und Traefik-Structured-Evidence wird durch den gemeinsamen
  Validator adaptiert; Apache und HAProxy bleiben fixture/interface-only.
- Alle 32 angeforderten Contract-Cases sind abgedeckt, einschließlich Identity,
  Expected-versus-Observed-Verhalten, Cleanup, Profil, Provenance, JSON und
  Safe-File-Negative-Controls.
- Evidence-Processing lehnt Symlinks, unsichere Hardlinks und Berechtigungen,
  unsichere Owner, non-regular Objects, unsichere Component-Directories,
  übergroße Dateien, Duplicate-JSON-Keys und Replacement-Races ab.
- Kein Live-Six-Connector-by-Four-Profile-PASS wird ohne Host-Evidence behauptet.

## Implementierungsentscheidung und Begründung

- `ci/runtime/contracts/runtime-observation.schema.json` ist der versionierte
  Vertrag; `runtime_observation.py` stellt die gemeinsame API und das strikte
  Policy-Result-Vokabular bereit; `validate-runtime-observation.py` ist die CLI.
- Jedes Profil führt vollständige `parent_commit`-, `framework_commit`- und
  `mrts_commit`-Identity. No-MRTS-Isolation-Fakten bleiben false, während die
  gewählte MRTS-Revision Provenance bleibt.
- Die strikte Policy berechnet digest-bound relative Evidence unter einer
  privaten Evidence-Root neu. `fixture`-Evidence ist explizit getrennt und
  kann nicht in einen strikten Live-Claim eingeschleust werden.
- `runtime_observation_adapters.py` enthält nur Envoy-, Lighttpd- und Traefik-
  Live-Adapter. Apache und HAProxy haben Canonical-Fixtures, aber keinen Lite-
  Live-Adapter; NGINX wird als `protected-separate` ohne Broker-Änderung
  abgebildet.
- Der vorhandene No-MRTS-Normalizer behält connector-spezifische Korrelation,
  erzeugt und validiert dann die Canonical Observation. Sein Raw-Reader nutzt
  nun descriptor-relative no-follow traversal, Owner-/Mode-/Link-Count-Checks,
  `O_NONBLOCK`, begrenzte Reads und Before-/After-State-Checks.

## Security-Auswirkung

Die Änderung verarbeitet Connector-produziertes JSON und Filesystem-Evidence,
deshalb ergänzt sie No-Follow-, Regular-File-, Owner-, Writable-Mode-, Link-
Count-, Size-, Duplicate-Key-, Non-Finite-JSON- und Exchange-Race-Abwehr.
`FND-PARENT-0228` hält eine validierte Pre-Fix-Raw-Reader-Lücke und ihre
fokussierte lokale Remediation fest. Der strikte Validator behandelt weder ein
Test-Fixture noch Command-Success oder Raw-Log als Live-Runtime-PASS-Evidence;
die Same-UID-Trusted-Runner-Einschränkung für ansonsten selbstkonsistente Daten
ist unten dokumentiert.

Der fokussierte Workflow-Security-Gleichheitscontrol schlägt für zwei vorhandene
vertrauenswürdige Workflows außerhalb des Workflow-Scopes dieses Tasks
fail-closed fehl; dies bleibt als `FND-PARENT-0111` erhalten und wird hier
weder remediated noch suppressed.

## Geänderte Dateien

- `ci/runtime/contracts/__init__.py`
- `ci/runtime/contracts/runtime-observation.schema.json`
- `ci/runtime/contracts/runtime_observation.py`
- `ci/runtime/contracts/runtime_observation_adapters.py`
- `ci/runtime/contracts/validate-runtime-observation.py`
- `ci/runtime/contracts/README.md` und `ci/runtime/contracts/README.de.md`
- `ci/runtime/lifecycle/normalize-with-crs-no-mrts.py`
- `ci/README.md` und `ci/README.de.md`
- `tests/test_runtime_observation_contract.py`
- `tests/test_with_crs_no_mrts_runtime.py`
- `tests/fixtures/runtime-observation/apache-no-crs-no-mrts.json`
- `tests/fixtures/runtime-observation/haproxy-no-crs-no-mrts.json`
- Dieser Change Record, sein deutscher Companion und beide Change-Record-Indizes.

## Ausgeführte Befehle

Die folgenden Befehle verwenden den konfigurierten Projekt-Python-Interpreter
über RTK; ihre beobachteten Ergebnisse werden aufbewahrt statt aus einem
CI-Step abgeleitet.

## Tests und tatsächliche Ergebnisse

| Check | Tatsächliches Ergebnis |
| --- | --- |
| `tests.test_runtime_observation_contract` + `tests.test_with_crs_no_mrts_runtime` | Bestanden: `107 tests in 35.534s`. |
| Fokussierte Raw-Reader-Hardlink-/Owner-/Mode-/FIFO-/Nonblocking- und Replacement-Controls | Bestanden: `7 tests`. |
| `tests.test_with_crs_no_mrts_runtime` Legitimate-Control-Suite | Bestanden: `54 tests in 27.829s`. |
| `py_compile` für alle sieben geänderten Python-Dateien | Bestanden: Exit `0`. |
| `tests.test_runtime_path_security` | Bestanden: `21 tests in 2.230s`. |
| `tests.test_evidence_output_security` | Bestanden: `9 tests in 0.237s`. |
| `tests.test_bilingual_docs` | Bestanden: `22 tests in 0.288s`. |
| Bestehende CI-Security-Baseline | Bestanden: `1 test in 70.580s`. |
| Workflow-Security Exact Equality Control | Fail-closed für zwei pre-existing ausgelassene Workflow-Pfade; als `FND-PARENT-0111` getrackt, keine Workflow-Source geändert. |
| `git diff --check` für die Working Change | Bestanden. |
| `make check-bilingual-docs` und `make check-doc-links` | Task-eigene Change-Record-Validierung bestanden; beide Targets bleiben nur durch vorhandene Links in das absichtlich nicht initialisierte Framework-Submodul blockiert. |

## Runtime-Evidence

Die aufgezeichneten Tests validieren Schema, API, Adapter, Provenance und
sichere Dateiverarbeitung. Sie sind keine Live-Host-Runtime-Evidence. Keine
vollständige Six-Connector-by-Four-Profile-Matrix wurde ausgeführt, und dieser
Record behauptet keinen solchen PASS. Envoy-, Lighttpd- und Traefik-Normalizer-
Tests verwenden structured host-shaped Evidence; Apache und HAProxy behalten
nur Canonical-Fixtures, bis reale Producer existieren.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine Live-Six-Connector-by-Four-Profile-Host-Matrix wurde nicht ausgeführt;
  erforderliche Connector-Hosts, Provenance und legitime Runtime-Evidence sind
  in diesem lokalen Contract-Task nicht vorhanden.
- `make check-bilingual-docs` und `make check-doc-links` liefen, können in
  diesem Task-Worktree aber nicht bestehen, weil vorhandene Repository-
  Dokumente in das absichtlich nicht initialisierte Framework-Submodul linken.
  Framework-Initialisierung oder -Änderung liegt außerhalb der Task-Autorität;
  kein Link- oder Source-Control wurde geschwächt.
- Der terminale Security-Diff-Report steht bei Record-Erstellung noch aus.

## Bekannte Einschränkungen

Der gemeinsame Validator kann einen privaten, digest-bound Evidence-Vertrag
prüfen, aber keinen Prozess kryptographisch attestieren, der bereits dieselbe
lokale UID- und Private-Evidence-Root-Autorität hat. Er erhält daher die
vorhandene Trusted-Runner-Grenze, statt einen nicht erreichbaren Proof der
Producer-Identity zu behaupten. Apache- und HAProxy-Live-Producer bleiben
explizit abwesend und fail-closed.

## Verbleibende Risiken

`FND-PARENT-0111` bleibt ein P1-Workflow-Governance-Blocker außerhalb des
autorisierten Scopes. Seine zwei exakten Workflow-Pfade erfordern eine
separate, eng autorisierte Reparatur, die die endliche Allowlist und den
Fail-Closed-Negative-Control erhält. Die aktuelle Implementierung ergänzt
keinen Workaround, Path-Exclusion, Permission-Change oder geschwächten
Security-Control.

## Finaler Diff- und Review-Status

Für Source-Implementation und Raw-Reader-Remediation liegen fokussierte
Regression-, vollständige Changed-Python-Compilation-, task-eigene Bilingual-
Record-, CI-Security- und Working-Diff-Evidence vor. Der finale Delivery-Review
muss noch den terminalen Security-Diff-Workflow versiegeln und exakten Draft-
PR-Delivery-Preflight durchführen. Kein Hosted-Result oder Merge wird vorab
behauptet.

## Delivery-Status

Der Benutzer autorisiert einen unabhängigen Draft PR von
`codex/canonical-runtime-observation` gegen `master` nach finaler Validierung.
Kein Ready-for-Review-Übergang, Merge, Auto-Merge, Rebase, Force-Push,
Default-Branch-Push, Framework-/MRTS-Änderung oder Gitlink-Update ist durch
diesen Record autorisiert.
