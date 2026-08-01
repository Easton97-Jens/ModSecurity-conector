# FND-FRAMEWORK-0049 — Framework-PR #42: Python-Quality-Gate scheitert an fünf Pyright-Typdiagnosen

- Kategorie: `ci_failure`
- Repository / Ownership: `framework` / `framework`
- Priorität / Schweregrad / Konfidenz: `P1` / `not_applicable` / `validated`
- Status / Feasibility: `verified` / `already_fixed`
- Release-Blocker / Sicherheitsrelevanz: `false` / `true`

## Zusammenfassung

Der exakte Head
`22747d460a9f7be02760edf05c311be376492457` von Framework-PR #42 scheitert im
erforderlichen Check `python-ci-security-quality` des GitHub-Actions-Runs
`29942429850`. Hosted Pyright meldet fünf Typdiagnosen: Wiederholte,
als `Any | None` typisierte `dict.get()`-Werte erreichen `re.fullmatch` in
`ci/tools/fetch-security-tool.py`, und ein statisch als `object` typisierter
Lock-Fixture-Wert wird in `tests/ci_security/test_update_workflow_tools.py`
indiziert.

Der Kandidaten-Commit `1fd3b362e0fed9766c6920e3c7bd1939535850f2` grenzt die
dynamischen Werte ein und korrigiert die Fixture-Annotation. Seine begrenzte
lokale Validierung und sein frischer Hosted-Pyright-Result bestanden: GitHub-
Actions-Run `29943112344`, Job `89001693819`, SUCCESS um
`2026-07-22T17:37:28Z`. Alle nicht übersprungenen PR-Checks und das PR-Sonar-
Quality-Gate sind grün. PR #42 wurde danach um `2026-07-23T07:41:13Z` als
Framework-Master `935cf14c676a24672be5c336e92cd13457cc35c8` aus Vorgänger
`f73f8842f45318e2df8aff1d31855eeb7c20a22f` und gemergtem Head
`dc6cf411e78b3f37f1e4be52edef59894560b1ae` normal integriert; der
resultierende Tree entspricht dem geprüften PR-Head-Tree. Das SHA-256-gebundene
Postmerge-Receipt
`0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1`
erfasst den Erfolg des exakten Master-CI-security-Python-quality-Workflows
`29989195066` und der übrigen sieben exakten Master-GitHub-Actions-Workflows.
Die Source-Remediation ist `verified`, nicht `closed`.

## Beobachtetes und erwartetes Verhalten

Der gehostete Check `python-ci-security-quality` scheitert während der
deterministischen Pyright-Analyse mit fünf Fehlern. Die zitierten Stellen sind
`ci/tools/fetch-security-tool.py:161` und `:166`, wo `Any | None`
`re.fullmatch` erreicht, sowie `tests/ci_security/test_update_workflow_tools.py:49`,
wo ein als `object` typisierter Wert indiziert wird.

Der erforderliche Quality-Job muss ohne Pyright-Suppression oder geschwächten
Scope erfolgreich enden. Dynamische Mapping-Werte müssen vor dem Matching
eingegrenzt werden, und die verschachtelte YAML-abgeleitete Lock-Fixture muss
vor dem Indizieren einen korrekten Typvertrag tragen. Bestehendes Download-
Host-, Release-Identity-, Action-Lock-, Workflow-Permission-, Publisher-,
Checkout- und Ref-Validation-Verhalten muss unverändert bleiben.

## Auswirkung, Grenzen und Voraussetzungen

Der ursprüngliche Head war ein P1-Release-Blocker, weil er einen erforderlichen
CI-Gate nicht erfüllen konnte. Der exakte Kandidaten-Head
`1fd3b362e0fed9766c6920e3c7bd1939535850f2` erfüllt diesen Gate und alle nicht
übersprungenen PR-Checks jetzt. Der normale Merge und der erfolgreiche exakte
Master-CI-security-Python-quality-Workflow liefern die erforderliche Delivery-
Evidence; daher ist dies kein Release-Blocker mehr. Dies ist kein Nachweis
eines Runtime-Defekts oder einer validierten Vulnerability. Der betroffene
Helper nimmt an einem Security-Quality- und Provenance-Workflow teil; seine
bestehenden Controls blieben erhalten.

Der Fehler setzt Framework-PR #42 am exakten Head
`22747d460a9f7be02760edf05c311be376492457`, die Ausführung des gehosteten
Jobs `python-ci-security-quality` und dessen deterministischen Pyright-Step
voraus. Kein attacker-controlled Source-to-Sink-Pfad und kein gebrochener
Runtime-Security-Control wird durch diese Typdiagnosen belegt.

## Betroffene Dateien und technische Ursache

- `ci/tools/fetch-security-tool.py:161` — `re.fullmatch` erhält einen
  wiederholten dynamischen `dict.get()`-Wert vom Typ `Any | None`.
- `ci/tools/fetch-security-tool.py:166` — dieselbe Typgrenze tritt beim
  zweiten `re.fullmatch`-Aufruf auf.
- `tests/ci_security/test_update_workflow_tools.py:49` — ein verschachtelter
  Lock-Fixture-Wert vom Typ `object` wird indiziert.

Der ursprüngliche Source behielt `Any | None` über die Matching-Grenzen bei,
und die Test-Fixture deklarierte eine flache `object`-Map, obwohl sie als
verschachtelte dynamische YAML-abgeleitete Daten indiziert wird. Dies beschreibt
einen statischen Typvertragsfehler; falsches Runtime-Verhalten wird nicht
behauptet.

## Evidence und Reproduktion

- Externer Hosted-Fehler: Framework-PR #42, Run `29942429850`, Check
  `python-ci-security-quality`, exakter Head
  `22747d460a9f7be02760edf05c311be376492457`, Exit `1`. Das Live-GitHub-Log
  wird in dieser Parent-lokalen Aufgabe nicht aufbewahrt.
- Aufbewahrtes Follow-up-Receipt:
  `evidence/ci-remediation/pr42-pyright-followup-commit-receipt.md`, SHA-256
  `5ccf2bd636101b2feea10e80c89852dbcf9c5f5e94e4b27decfbe0f5311ab790` im Run
  `20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e`.
- Aufbewahrter gepaarter Framework-Change-Record:
  `reports/audits/change-records/20260722-01-consolidate-framework-pr-39-41.md`,
  SHA-256
  `faad4f2e542bac431c0a0f7f3b348cc3192ace933cf3c38944ee3beb7fa7ee93`.
- Aufbewahrtes Exact-Head-Hosted-Verification-Receipt:
  `evidence/delivery/pr42-exact-head-hosted-verification.md`, SHA-256
  `07d30f93ab9bda5fb03fb22b20b9755aba2b8567b67678a34ec3ff7927bcb853`.
- Aufbewahrtes Resulting-Master-Verification-Receipt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md`,
  SHA-256
  `0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1`.
  Es bindet den normalen PR-#42-Merge an den resultierenden Master
  `935cf14c676a24672be5c336e92cd13457cc35c8` und erfasst den erfolgreichen
  exakten Master-CI-security-Python-quality-Workflow `29989195066`.

Das aufbewahrte Receipt bindet den ursprünglichen Fehler an den Kandidaten-
Commit `1fd3b362e0fed9766c6920e3c7bd1939535850f2` (Parent
`22747d460a9f7be02760edf05c311be376492457`) und dokumentiert das lokale
Ergebnis.

## Kandidaten-Remediation und lokale Validierung

Der Kandidat speichert `upstream_release` und `asset_url` einmal, prüft und
grenzt ihren String-Typ vor dem Matching ein und typisiert die verschachtelte
Lock-Fixture als verschachtelte `Any`-Daten. Er ändert weder Download-Host,
Release-Identity, Action-Lock, Workflow-Permissions, Publisher, Checkout noch
Ref-Validation.

Das aufbewahrte Receipt dokumentiert diese lokalen Ergebnisse für den
Kandidaten:

- Fokussierte Fetcher/Updater-Unit-Tests: 39 bestanden.
- CI-Security-Contract: bestanden.
- Dokumentations- und Change-Record-Contracts: bestanden.
- Prüfsummenverifizierter Ruff-Check und Format-Check für beide berührten
  Python-Dateien: bestanden.
- Native `make lint`: bestanden.
- Clean Worktree und `git diff --check` für die vollständige Base-to-Head-
  Range: bestanden.

Darauf folgte Exact-Head-Hosted-Verifikation: Run `29943112344`, Job
`89001693819` bestand `python-ci-security-quality`, einschließlich
deterministischem Pyright, um `2026-07-22T17:37:28Z`. Alle nicht
übersprungenen PR-Checks und das PR-Sonar-Quality-Gate bestanden. PR #42 ist
offen, nicht Draft, `MERGEABLE` und `CLEAN`, ohne Review oder actionable
Thread.

## Akzeptanz und Validierung

Die Source-Remediation-Kriterien sind am exakten Head
`1fd3b362e0fed9766c6920e3c7bd1939535850f2` erfüllt; der normale Merge und die
Resulting-Master-Evidence stützen nun `verified`, aber nicht `closed`:

1. Ein geprüfter Kandidat muss die begrenzte Type-Narrowing- und Fixture-
   Typisierung ohne Lockerung der aufgeführten Provenance- und Workflow-
   Security-Controls beibehalten.
2. Die fokussierten Tests sowie die aufgezeichneten lokalen Contract-,
   Dokumentations-, Ruff-, Lint-, Clean-Worktree- und Whitespace-Checks müssen
   für den Kandidaten bestehen.
3. Ein unterschiedlicher exakter PR-Head mit der Remediation bestand
   `python-ci-security-quality`, einschließlich Pyright: Run `29943112344`,
   Job `89001693819`, SUCCESS um `2026-07-22T17:37:28Z`. Ein Result für
   `22747d460a9f7be02760edf05c311be376492457` ist kein Ersatznachweis.
4. Erfüllt: alle nicht übersprungenen Hosted-PR-Checks, das PR-Sonar-Quality-
   Gate und die PR-Review-/Thread-Controls wurden für genau diesen Head
   beobachtet; PR #42 wurde normal als
   `935cf14c676a24672be5c336e92cd13457cc35c8` integriert, mit erfolgreichem
   exakten Master-CI-security-Python-quality-Workflow `29989195066`.

Legitime Controls verlangen, dass akzeptiertes Release-/Provenance-Matching
und bestehendes Updater-Lock-Fixture-Verhalten erhalten bleiben, während
fehlende oder ungültige dynamische Werte die bestehenden Checks nicht umgehen
dürfen.

## Abhängigkeiten, Delivery-Limitierungen und Restrisiko

Für diese verifizierte Source-Reparatur gibt es keine offene Remediation-
Abhängigkeit oder keinen Blocker. Das ursprüngliche externe Log wird hier
nicht aufbewahrt, und die Typfehler allein beweisen keinen Security-Exploit.
Der normale Merge und die Resulting-Master-Evidence erfüllen den erforderlichen
Lifecycle-Nachweis.

`FND-SONAR-0002` (Resulting-Master-Security-Rating C) und
`FND-GITHUB-0007` (gequeue-te Cloudflare-Suite) sind getrennte, vom Nutzer für
PR #42 begrenzte Delivery-Limitierungen. Ihre globalen Findings bleiben
unabhängig getrackt; keine der beiden Bedingungen reproduziert, blockiert oder
öffnet diese verifizierte Pyright-Reparatur erneut. Es gab keine Parent-
Gitlink- oder MRTS-Aktion. Das Finding ist absichtlich `verified`, nicht
`closed`.

## Verwandte Findings

- `FND-FRAMEWORK-0020` ist eine frühere, getrennte Pyright-Typfehlerursache.
- `FND-FRAMEWORK-0046`, `FND-FRAMEWORK-0047` und `FND-FRAMEWORK-0048` sind
  getrennte Framework-Konsolidierungs-Findings; keines wird durch diesen Record
  geändert.
- `FND-SONAR-0002` und `FND-GITHUB-0007` sind getrennte begrenzte Delivery-
  Limitierungen, keine Abhängigkeiten dieses reparierten Source-Defekts.

## Historie

- 2026-07-23T07:51:09Z: `verified_after_pr42_normal_merge_and_resulting_master`
  — PR #42 wurde um 2026-07-23T07:41:13Z normal als Framework-Master
  `935cf14c676a24672be5c336e92cd13457cc35c8` aus Vorgänger
  `f73f8842f45318e2df8aff1d31855eeb7c20a22f` und gemergtem Head
  `dc6cf411e78b3f37f1e4be52edef59894560b1ae` integriert. Das aufbewahrte
  Postmerge-Receipt SHA-256
  `0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1`
  erfasst den erfolgreichen exakten Master-CI-security-Python-quality-Workflow
  `29989195066` und sieben weitere exakte Master-GitHub-Actions-Workflows. Mit
  dem vorherigen direkten Pyright-Erfolg wechselt die Source-Reparatur von
  fixed zu verified, nicht closed. FND-SONAR-0002 und FND-GITHUB-0007 bleiben
  getrennte begrenzte Delivery-Limitierungen, keine Blocker dieser Reparatur.
- 2026-07-22T17:35:19Z: Hosted-Fehler auf PR-#42-Exact-Head
  `22747d460a9f7be02760edf05c311be376492457`, GitHub-Actions-Run
  `29942429850`, Check `python-ci-security-quality` aufgezeichnet.
- 2026-07-22T17:35:19Z: lokaler Kandidat
  `1fd3b362e0fed9766c6920e3c7bd1939535850f2` und dessen bestandene begrenzte
  lokale Validierung aufgezeichnet. Hosted Pyright und Required Checks bleiben
  unbeobachtet.
- 2026-07-22T17:37:28Z: exakter Head
  `1fd3b362e0fed9766c6920e3c7bd1939535850f2` bestand GitHub-Actions-Run
  `29943112344`, Job `89001693819`, einschließlich
  `python-ci-security-quality` / deterministischem Pyright, allen nicht
  übersprungenen PR-Checks und dem PR-Sonar-Quality-Gate. PR #42 ist nicht
  Draft, `MERGEABLE` und `CLEAN`, ohne Reviews oder actionable Threads. Die
  Source-Remediation ist fixed/open; kein normaler Master-Merge oder
  Resulting-Master-Rerun erfolgte, weil `FND-SONAR-0002` ihn unabhängig
  blockiert.
