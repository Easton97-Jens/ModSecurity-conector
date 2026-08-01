# FND-PARENT-0062 — Python-Workflow-Inventarvertrag referenziert einen entfernten Verified-Report-Governance-Job

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0062 |
| Kategorie | ci_failure |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / confirmed |
| Status / Machbarkeit | validated / feasible_now |
| Release-Blocker / sicherheitsrelevant | ja / nein |
| Scope | Parent-Python-Workflow-Inventar und Verified-Report-Governance-Job-Identitäten |

## Beobachtung, erwartetes Verhalten und Auswirkung

Auf Parent-master `dd175053b3d7f509286af87646d6eb093a49d578` endet der Befehl
`rtk proxy make check-python-version-contract` mit `2`. Sein explizites
Normal-Job-Inventar verlangt weiterhin
`verified-report-governance.yml:verified-report-contract-preflight`, während
`.github/workflows/verified-report-governance.yml` diesen Job nicht mehr
definiert.

Der Beleg beweist unabhängig, dass Workflow-, Checker- und Makefile-Scope mit
`origin/master` identisch sind und nicht durch PR #138 verändert werden:

```text
git diff --quiet origin/master -- .github/workflows/verified-report-governance.yml ci/checks/common/check-python-version-contract.py Makefile
exit 0
```

Das unveränderte fehlgeschlagene Ergebnis ist:

```text
python-version-contract: expected normal Python job is absent: verified-report-governance.yml:verified-report-contract-preflight
make: *** [Makefile:1276: check-python-version-contract] Error 1
```

Das explizite Inventar und die eingecheckten Workflows müssen stattdessen
denselben aktuellen Vertrag beschreiben, damit das Make-Target auf aktuellem
Parent-master mit `0` endet und für einen tatsächlich fehlenden erforderlichen
Python-Job weiter fail-closed bleibt. Der aktuelle Fehler blockiert
vertrauenswürdige CI-Validierung und kann sinnvolle Inventar-Drift hinter einer
dauerhaft fehlgeschlagenen Baseline verbergen. Er ist ein P1-CI-Release-Blocker,
kein Security-Finding.

## Evidenz und Reproduktion

Die aufbewahrte Evidence gehört zum Source-Run
`merge-prs-129-149-master-20260728`:

`/var/tmp/codex/ModSecurity-conector/runs/merge-prs-129-149-master-20260728/evidence/fnd-parent-0062-python-workflow-contract-drift.md`

SHA-256:
`17ae8b2b76e65e4f9db7625122b56f5d74c171bed69912f6ba2a68198b3b283e`

Die Evidence wurde am `2026-07-28T07:03:58Z` erfasst. Aus
`/var/tmp/codex/ModSecurity-conector/worktrees/parent/sonar-report-conditionals-20260727`
endete der Scope-Equivalence-Control mit `0`, danach endete `rtk proxy make
check-python-version-contract` mit `2`. Beim Sammeln des Belegs wurden weder
Workflow, Scanner, Suppression, Framework, MRTS, Gitlink noch Delivery-Status
verändert.

Zur Reproduktion denselben Scope-Equivalence-Control bestätigen, das
Make-Target ausführen und die oben genannte exakt fehlende Identität beobachten.

## Ursache und begrenzte Remediation

`ci/checks/common/check-python-version-contract.py` behält
`JobIdentity("verified-report-governance.yml", "verified-report-contract-preflight")`
in `EXPECTED_NORMAL_PYTHON_JOBS`, aber
`.github/workflows/verified-report-governance.yml` definiert diesen Job nicht
mehr. Daher gibt `inventory_violations` den Missing-Job-Fehler aus.

Die Remediation ist ein getrennter fokussierter Parent-Workflow-/Checker-
Alignment-PR. Er muss das kanonische Python-Setup und die bestehenden
Workflow-Trust-Controls bewahren, eine wahrheitsgemäße exakte
Inventar-/Workflow-Beziehung wiederherstellen, einen Regressionstest ergänzen
und Hosted-Proof einholen. Er darf nicht stillschweigend in PR #138 gefaltet
werden.

## Akzeptanz und Validierung

Akzeptanz erfordert alle folgenden Punkte:

- das exakte Inventar und die definierten Verified-Report-Governance-Jobs sind
  auf dem korrigierenden PR-Head ausgerichtet, ohne kanonisches Python-Setup
  oder Trust-Controls abzuschwächen;
- `rtk proxy make check-python-version-contract` endet auf diesem
  ausgerichteten Tree mit `0`;
- fokussierte Coverage in `tests/test_python_version_contract.py` beweist das
  gewählte Alignment und einen unabhängigen Missing-Job-Negativ-Control;
- das Inventar bleibt explizit, statt zu einem breiten Dateinamen- oder
  Jobnamen-Pattern zu werden;
- relevante Workflow-Syntax- und CI-Contract-Checks bestehen; und
- der exakte korrigierende Head besitzt Hosted-Proof, gefolgt von einem
  Original-Target-Rerun auf resultierendem Parent-master, bevor das Finding
  verified oder closed wird.

Die legitimen Controls bewahren das kanonische `.python-version`-Setup und den
Verifier-Vertrag, halten einen absichtlich fehlenden anderen erforderlichen Job
über `inventory_violations` fail-closed und erhalten die bestehende
Least-Privilege-/Trust-Control-Topologie des Verified-Report-Governance-
Workflows.

## Abhängigkeiten, Restrisiko und Historie

Abhängigkeiten sind ein getrennter fokussierter Parent-Alignment-PR,
fokussierte Python-Inventar-Regression-Coverage und Exact-Head-Hosted- sowie
Resulting-Master-Proof. Es gibt keine aktuellen Blocker für die Implementierung
dieser fokussierten Reparatur.

Bis die Reparatur und ihr Resulting-Master-Rerun vorliegen, kann der
verpflichtende Python-Workflow-Inventarvertrag nicht als bestehender
Master-Control bestehen. Es sind keine Abschwächung eines Trust-Controls,
Scanner-Änderung, Suppression, Framework-/MRTS-Aktion, Gitlink-Update oder
Risikoakzeptanz erfasst.

- `2026-07-28T07:03:58Z` — Auf Current-Master-Equivalent-Scope mit dem oben
  genannten aufbewahrten Receipt-Hash validiert. Dieser Record bleibt bewusst
  von PR #138 getrennt, weil seine Workflow-/Checker-Alignment-Ursache und
  Remediation-Grenze unabhängig sind.
