# FND-PARENT-0060 — Full-Matrix-Batch-Scheduler schöpft seine Parallelitätsgrenze nicht work-conserving aus

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0060 |
| Kategorie | lifecycle_defect |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / validated |
| Status / Machbarkeit | fixed / feasible_now |
| Release-Blocker / sicherheitsrelevant | ja / nein |
| Scope | Parent-Full-Matrix-Completion-Scheduling und Capacity-Refill |

## Lokal behobenes Verhalten, Scope und Non-Security-Klassifikation

Der frühere Full-Matrix-Scheduler war bei seiner konfigurierten
Parallelitätsgrenze nicht work-conserving. Sein Batch-Scheduler füllte einen
Batch und wartete auf den gesamten Batch, statt beim Ende eines einzelnen Child
den nächsten wartenden Job zuzulassen. Bei cap=2 konnte ein schneller Job enden
und einen Kern freigeben, während sein langsamer Sibling noch lief; ein dritter
wartender Job konnte dann erst starten, nachdem der langsame Sibling endete.

Die erwartete Invariante ist completion-gesteuerte Zulassung: Ein beendetes
Child gibt einen Slot frei, und der nächste wartende Job startet zeitnah,
während die Anzahl aktiver Jobs die Grenze nicht überschreitet. Die lokale
completion-gesteuerte Remediation und ihre fokussierte Regression sind vom
Parent als bestanden bestätigt. Dies ist ein Lifecycle-/Reliability-Defekt,
kein Security-Finding. Er bleibt unabhängig von der Port-Allokationsgrenze aus
FND-PARENT-0058 und der FD-9-Lock-Admission-Grenze aus FND-PARENT-0059 und ist
lokal fixed, aber nicht hosted verified oder closed.

Betroffene Dateien und Symbole sind:

- ci/runtime/lifecycle/run-full-matrix-parallel.sh — run_planned_jobs und sein
  batch-weites wait;
- tests/test_full_matrix_parallel_scheduler.py —
  test_parallel_scheduler_refills_a_freed_slot_before_a_slow_sibling_exits;
  und
- die Full-Matrix-Parallelitätsgrenze.

## Evidenz und Reproduktion

Der Parent stellte einen Static-Review in der Task-Konversation für
ci/runtime/lifecycle/run-full-matrix-parallel.sh, run_planned_jobs, bereit,
zitiert als Zeilen 680-732. Der Review folgert, dass cap=2 auf den gesamten
gestarteten Batch wartet: Das Ende eines schnellen Child vor einem langsamen
Sibling führt nicht zum Start des dritten wartenden Jobs.

Der frühere Reviewer-Befehl lieferte Exit 0 mit acht bestandenen Tests:

    PYTHONDONTWRITEBYTECODE=1 python3 -B tests/test_full_matrix_parallel_scheduler.py

Dieses historische Ergebnis legte den Defekt nicht offen: Seine acht Tests
deckten nicht drei Jobs mit unterschiedlicher Dauer bei cap=2 ab. Der Parent
bestätigt nun, dass
test_parallel_scheduler_refills_a_freed_slot_before_a_slow_sibling_exits
besteht und ein kombinierter 107-Test-Scheduler-Run bestand. Diese lokalen
Ergebnisse validieren die Remediation, sind aber nur Task-Konversations-
Evidence; es wurden keine Filesystem-Receipt und kein Hosted-Successor-
Ergebnis geliefert.

Zur Reproduktion cap=2 konfigurieren und einen langsamen Job, einen schnellen
Job und einen dritten wartenden Job übergeben. Sobald der schnelle Job endet,
während der langsame Job noch aktiv ist, bleibt der dritte Job wartend. Der
lokal behobene Scheduler startet diesen dritten Job dagegen, bevor der langsame
Sibling endet.

## Auswirkung, Ursache und Remediation

Der Scheduler kann konfigurierte Kapazität ungenutzt lassen, einen
Full-Matrix-Lauf verlängern und trotz wartender Arbeit die Wahrscheinlichkeit
von Timeouts oder verzögerter Release-Evidence erhöhen. Der Defekt ist deshalb
ein P1-Lifecycle-/Reliability-Release-Blocker.

Die Ursache ist Whole-Batch-Synchronisierung in run_planned_jobs. Der Scheduler
benutzt das Ende des langsamsten Child als Admission-Grenze, statt einzelne
Children zu reapen und den freigewordenen Slot aufzufüllen.

Die lokale Remediation ist completion-gesteuert: Sie trackt und reapet
einzelne Child-Completion, lässt den nächsten wartenden Job bei jedem freien
Slot zu und erhält die konfigurierte Grenze. Die deterministische cap=2-/
Drei-ungleiche-Jobs-Regression besteht nun lokal. FND-PARENT-0058-Port-Plan-
Controls, FND-PARENT-0059-Live-Lock- und geerbte-FD-9-Controls sowie
Manifest-/Result-Controls müssen erhalten bleiben. Frische Hosted-Successor-
Evidence ist vor verified oder closed erforderlich.

## Akzeptanz und Validierung

Akzeptanz erfordert:

- bei cap=2 und drei Jobs mit unterschiedlicher Dauer startet der dritte
  wartende Job, nachdem der schnelle Sibling endet und bevor der langsame
  Sibling endet;
- der Scheduler überschreitet niemals zwei aktive Jobs;
- FND-PARENT-0058-Port-Allokations-Controls bleiben wirksam;
- FND-PARENT-0059-Live-Lock- und geerbte-FD-9-Controls bleiben wirksam;
- Manifest- und Result-Policy-Controls bleiben wirksam; und
- test_parallel_scheduler_refills_a_freed_slot_before_a_slow_sibling_exits
  legt das frühere batch-weite wait offen und besteht mit der lokalen
  Remediation.

Die lokale fokussierte Regression und der vom Parent bestätigte kombinierte
107-Test-Scheduler-Run stützen fixed. Exakte lokale Receipts aufbewahren und
die Cap-, Port-, Lock-, Manifest- und Result-Policy-Controls ausführen.
Frische Exact-Successor-Full-Matrix- und Hosted-Evidence sind vor verified oder
closed erforderlich. Der frühere Acht-Test-Reviewer-Befehl bleibt eine
historische Coverage-Gap-Beobachtung, nicht der Beweis für den lokalen Fix.

## Abhängigkeiten, Restrisiko und Historie

Abhängigkeiten sind die beizubehaltende Parent-Scheduler-Remediation und ihre
deterministische Regression, während FND-PARENT-0058, FND-PARENT-0059 und
FND-PARENT-0061 unabhängige, zu erhaltende Controls bleiben. FND-SONAR-0016
bleibt der aggregierte Quality-Gate-Record.

Die lokale Remediation, die genannte Regression und der 107-Test-kombinierte
Run sind nur vom Parent bestätigte Task-Konversations-Evidence; es wurden keine
aufbewahrte Filesystem-Receipt und keine Hosted-Successor-Evidence geliefert.
Deshalb ist das Finding P1 fixed / feasible_now und ein Release-Blocker, nicht
verified, closed, deferred oder risk accepted.

Erfasst 2026-07-26T20:48:02Z als
validated_non_work_conserving_batch_scheduler_allocated.
Aktualisiert 2026-07-26T21:23:07Z als
local_completion_driven_refill_validated_hosted_successor_pending.
