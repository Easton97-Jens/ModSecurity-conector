# FND-FRAMEWORK-0054 — Framework-ModSecurity-v3-Git-Wrapper bindet vor der Provenance-Validierung kein verifiziertes Host-Git-Programm

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0054` |
| Kategorie / Category | `security_candidate` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priorität / Priority | `P2` |
| Schweregrad / Severity | `medium` |
| Konfidenz / Confidence | `probable` |
| Status | `verified` |
| Machbarkeit / Feasibility | `feasible_now` |
| Release-Blocker / Release blocker | `true` |
| Security-Relevanz / Security relevance | `true` |

## Zusammenfassung / Summary

## Aktuelle Master-Verifikation vom 2026-07-26

Das Review der umgebenden PATH-Auflösung unten betrifft den historischen Master
`f98a8739cb13b583f23d646784b144e596b61441`. Der aktuelle Master von
Framework-PR #44 `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` bindet
freigegebenes Host-Git vor Provenance-Befehlen. Die fokussierten
Fake-PATH-Rejection- und Approved-Host-Legitimate-Controls bestehen zusammen
mit der FND-FRAMEWORK-0036-Containment-Suite; Source-Provenance- und
Quality-Controls bleiben fail-closed.

Der eigenständige Framework-ModSecurity-v3-Provenance-Wrapper bereinigt Git-
Konfigurations- und Transporteingaben, ruft aber vor der Source-Provenance-
Prüfung ein unqualifiziertes über den aufrufenden `PATH` aufgelöstes `git` auf.
Bestehende Regressionen ersetzen Git absichtlich über `PATH` durch ein Fake-
Git, um freigegebene Git-Argumente zu modellieren; sie belegen keine
verifizierte Host-Executable-Grenze.

## Beobachtetes Verhalten / Observed behavior

Auf dem exakten sauberen Framework-master
`f98a8739cb13b583f23d646784b144e596b61441` löscht
`ci_modsecurity_v3_git` geerbten Git-Zustand und führt anschließend nacktes
`git -c ... "$@"` aus. Es wählt weder ein absolutes Host-Git-Programm noch
setzt es `PATH` zurück. Die Provenance-Regression schreibt ein temporäres
`bin/git` und stellt dieses Verzeichnis `PATH` voran. Das ist ein legitimes
Modell-Git-Control, aber kein Nachweis der ausführbaren Programmidentität in
der Produktion.

## Erwartetes Verhalten / Expected behavior

Bevor ein eigenständiger Fresh-Fetch-, Checkout- oder rekursiver Submodule-
Befehl Git erreicht, muss das Framework ein freigegebenes Host-Git-Programm
unabhängig von einem aufruferkontrollierten `PATH` auflösen und binden, beim
Fehlen dieses Trust-Contracts fail closed enden und Regressionen behalten, die
Test-only-Fake-Git-Injektion von der Produktionsauswahl des Host-Tools trennen.

## Auswirkung und Scope-Grenze / Impact and scope boundary

Falls ein weniger vertrauenswürdiger Akteur `PATH` in einer unterstützten
eigenständigen Framework-Fetch-Invocation beeinflussen kann, kann ein
ersetztes Git-Programm mit der Framework-/CI-Identität vor der Source-
Provenance-Validierung laufen. Das statische Review hat nicht belegt, dass ein
unterstützter produktiver Aufrufer einem solchen Akteur `PATH`-Kontrolle gibt.
Es ist daher eine plausible `P2`/medium-Hardening-Lücke, kein validierter
Exploit und kein High-/Critical-Finding.

Die Parent-Invocation kann `PATH` separat binden. Dieses Finding ist auf den
eigenständigen Framework-Source-Provisioning-Pfad begrenzt und schwächt oder
ersetzt weder `FND-FRAMEWORK-0032`, `FND-FRAMEWORK-0034`,
`FND-FRAMEWORK-0035` noch `FND-FRAMEWORK-0036`.

## Betroffener Pfad / Affected path

- `ci/lib/common.sh` — `ci_modsecurity_v3_git` startet nacktes `git` an der
  Provenance-Grenze.
- `ci/provisioning/fetch-smoke-sources.sh` —
  `provision_fresh_modsecurity_v3` erreicht Init, Fetch, Checkout und
  rekursives Submodule-Handling über diesen Wrapper.
- `tests/security_regression/test_modsecurity_v3_git_ref_provenance.py` —
  injiziert absichtlich ein Fake-`git`, indem ein temporäres Verzeichnis
  `PATH` vorangestellt wird; das beweist Argument-/Provenance-Semantik, nicht
  die Host-Tool-Bindung.

## Evidence / Evidence

- Run-ID: `20260723T162517Z-fnd-cross-0001-runtime-evidence-bcda7d1d`
  - Exakte Framework-master-Quelle:
    `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/ci/lib/common.sh`
  - Typ: `exact_framework_master_static_host_git_resolution_review`
  - SHA-256: `de97949bf36a409f4520b462f73dbb11b0033d70392c329c39d20f2131ccac6a`
  - Statische RTK-umhüllte Revisions-/Status-, Wrapper-Kontext- und Hash-
    Inspektion endete `0` um `2026-07-23T17:31:41Z`.
- Gleiche Run-ID, exakte Framework-Regressionsquelle:
  `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/tests/security_regression/test_modsecurity_v3_git_ref_provenance.py`
  - Typ: `exact_framework_master_static_fake_git_regression_review`
  - SHA-256: `d7e07d63c8bffb5526d13cf36159aa73b478879f68803bc92c8a0b56db2a1050`
  - Statische RTK-umhüllte Fake-bin-/`PATH`- und Hash-Inspektion endete `0` um
    `2026-07-23T17:31:41Z`.

Es wurde keine Runtime-Command-Substitution und keine hostile produktive
`PATH`-Quelle ausgeführt. Der Fake-Git-Test bleibt ein legitimes Control, kein
Exploit-Nachweis.

## Vorgeschlagene Remediation / Proposed remediation

Den unterstützten Host-Tool-Trust-Contract definieren und vor der Grenze ein
vertrauenswürdiges absolutes Git-Programm ohne Vertrauen in den aufrufenden
`PATH` auflösen. Zulässigen Ort, Ownership oder andere freigegebene Provenance
prüfen und `ci_modsecurity_v3_git` bei nicht erfülltem Contract fail closed
machen. Fokussierte Controls ergänzen, die belegen, dass nicht freigegebenes
Git früher auf `PATH` nicht aufgerufen wird, während ein freigegebenes Host-Git
den legitimen gepinnten Fetch-/Checkout-Pfad abschließt. Die getrennte
Fresh-Root-Containment-Arbeit von `FND-FRAMEWORK-0036` erhalten.

## Akzeptanzkriterien / Acceptance criteria

- Der produktive eigenständige Wrapper kann Git nicht aus einem untrusted
  aufruferseitigen `PATH` auflösen.
- Das ausgewählte Git-Programm besitzt einen expliziten dokumentierten und
  fail-closed Host-Trust-Contract, bevor es Fetch-, Checkout- oder Submodule-
  Argumente erhält.
- Eine fokussierte Regression beweist, dass ein Fake-Git früher auf `PATH`
  nicht durch den Produktions-Wrapper aufgerufen wird.
- Ein freigegebenes Host-Git-Control behält den legitimen gepinnten Source-
  Graphen und alle bestehenden Provenance-/Fresh-Root-Controls.
- Exaktes Framework-PR-Head-Review, fokussierte Checks, relevante CI-/Sonar-
  Evidence und Resulting-Master-Verifikation bestehen ohne Controls zu
  schwächen.

## Validierungsplan / Validation plan

- Feststellen, ob ein unterstützter Framework- oder CI-Aufrufer `PATH` einem
  weniger vertrauenswürdigen Akteur aussetzt; vor dieser Evidence keine
  Exploitability folgern.
- Die Host-Git-Bindung nur in einem isolierten Framework-Task/PR implementieren
  und fokussierte Fake-PATH-Block- sowie Approved-Host-Git-Legitimate-Controls
  ausführen.
- Die FND-FRAMEWORK-0036-Fresh-Root-Worktree-, Attributes/Filter- und
  Recursive-Update-Regressionen erneut ausführen, weil beide Findings dieselbe
  Pre-Provenance-Git-Command-Grenze teilen.
- Exact-Head-Review-, CI-, Sonar- und Resulting-Master-Evidence vor einer
  `fixed`- oder `verified`-Disposition erfassen.

## Verwandte Findings / Related findings

- `FND-FRAMEWORK-0032`
- `FND-FRAMEWORK-0034`
- `FND-FRAMEWORK-0035`
- `FND-FRAMEWORK-0036`

## Restrisiko / Residual risk

Die eigenständige Framework-Bereitstellung behält eine umgebende Command-
Resolution-Annahme an einer sicherheitsrelevanten Pre-Provenance-Grenze, bis
Host-Git-Trust-Contract und fokussierte Controls verifiziert sind. Praktische
Exploitability ist unbelegt; keine Risikoakzeptanz ist erfasst. Die
Framework-PR-Verifikation für diesen Pfad bleibt bis Fix oder evidenzgemäßer
Disposition blockiert.

## Historie / History

- `2026-07-23T17:31:41Z`: `static_host_git_path_boundary_triaged` — exakter
  Framework-master ruft nacktes Git aus `PATH` auf; der absichtliche Fake-Git-
  Test beweist keinen produktiven untrusted Akteur. Dieser getrennte
  P2/medium/probable-Kandidat änderte keinen Produkt-Source, keinen
  Framework-Branch/PR, keinen Parent-Gitlink und keinen MRTS-Zustand.
