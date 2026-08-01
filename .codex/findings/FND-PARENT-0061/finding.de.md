# FND-PARENT-0061 — Worker-Wrapper-Abbruch vor FIFO-Completion kann den Full-Matrix-Scheduler blockieren

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0061 |
| Kategorie | lifecycle_defect |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / validated |
| Status / Machbarkeit | fixed / feasible_now |
| Release-Blocker / sicherheitsrelevant | ja / nein |
| Scope | Parent-Full-Matrix-Worker-Completion-FIFO-Watchdog-Grenze |

## Lokal behobenes Verhalten, Scope und Non-Security-Klassifikation

Vor der lokalen Watchdog-Remediation ließ ein Worker-Wrapper, der nach dem
Start von Fake Make, aber vor dem Emittieren seines FIFO-Completion-Token
beendet wurde, den Parent-Scheduler unbegrenzt auf read <&8 blockiert. Der
Wrapper konnte Completion nicht mehr melden, während der Parent keinen
begrenzten Fehlerpfad für den fehlenden Token hatte.

Der lokale Fix begrenzt diesen Fehlerpfad. Mit
VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=1 führt ein Wrapper-Abbruch vor
FIFO-Completion zu Runner-Exit 77 statt zu unbegrenztem Warten. Nachdem das
Child endet, wird der FD-9-Full-Matrix-Lock wiederverwendbar. Dies ist ein
Lifecycle-/Reliability-Defekt, kein Security-Finding, und lokal fixed, aber
nicht hosted verified oder closed.

Betroffene Dateien und Symbole sind:

- ci/runtime/lifecycle/run-full-matrix-parallel.sh — Worker-Wrapper, FIFO-
  Completion-Token, read <&8, Timeout und FD-9-Lock-Reuse; und
- tests/test_full_matrix_parallel_scheduler.py — die fokussierte Wrapper-
  Death-Lifecycle-Regression.

## Evidenz und Reproduktion

Der Parent bestätigte, dass der folgende fokussierte Test besteht:

    tests.test_full_matrix_parallel_scheduler.test_scheduler_times_out_when_a_job_wrapper_dies_before_completion

Er startet Fake Make, beendet den Wrapper vor FIFO-Completion, setzt
VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=1 und beobachtet Runner-Exit 77.
Nachdem das Child endet, beobachtet er außerdem, dass FD 9 wiederverwendbar
ist. Dies ist nur vom Parent bereitgestellte Task-Konversations-Evidence; es
wurden keine Filesystem-Receipt und kein Hosted-Successor-Ergebnis geliefert.

Der ursprüngliche Zustand wird reproduziert, indem Fake Make gestartet, der
Worker-Wrapper vor seinem FIFO-Completion-Token beendet und der Pre-Watchdog-
Parent unbegrenzt auf read <&8 blockiert beobachtet wird. Das lokal behobene
Verhalten endet stattdessen über den begrenzten Timeout-Pfad und gibt den
geerbten Lock erst frei, nachdem das Child endet.

## Auswirkung, Ursache und Remediation

Ein fehlgeschlagener Worker-Wrapper konnte einen Full-Matrix-Lauf unbegrenzt
anhalten, Release-Evidence verzögern oder verhindern und den Scheduler für
Folgearbeit nicht verfügbar machen. Dies ist deshalb ein P1-Lifecycle- /
Reliability-Release-Blocker.

Die Ursache war die Abhängigkeit von einem FIFO-Completion-Token ohne
begrenzten Fehlerpfad. Starb der Worker-Wrapper nach dem Start von Fake Make,
aber vor Token-Emission, hatte read <&8 keinen zu konsumierenden Token und der
Parent wartete unbegrenzt.

Die lokale Watchdog-Remediation begrenzt das Warten auf den fehlenden Token und
meldet den kontrollierten Fehler mit Exit 77. Sie behält die fokussierte
Wrapper-Death-Regression und den FD-9-Reuse-Control bei. Frische
Hosted-Successor-Evidence ist vor verified oder closed erforderlich; es werden
weder Hosted-Verifikation noch Closure oder Delivery-Disposition behauptet.

## Akzeptanz und Validierung

Akzeptanz erfordert:

- ein Wrapper-Abbruch nach Start von Fake Make und vor FIFO-Completion lässt
  den Scheduler nicht unbegrenzt auf read <&8 blockiert;
- mit VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=1 endet der Runner mit 77;
- nachdem das Child endet, ist der FD-9-Lock wiederverwendbar;
- die fokussierte Worker-Wrapper-Lifecycle-Regression besteht; und
- Scheduler-Cap-, FND-PARENT-0058-Port-Plan-, FND-PARENT-0059-Lock-,
  Manifest- und Result-Policy-Controls bleiben wirksam.

Eine exakte lokale Receipt für den fokussierten Test aufbewahren und die
anwendbaren kombinierten Scheduler-Controls erneut ausführen. Frische
Hosted-Successor-Full-Matrix- und Protected-Integration-Evidence vor verified
oder closed beschaffen. Das lokale bestandene Ergebnis stützt nur fixed.

## Abhängigkeiten, Restrisiko und Historie

Die lokale Watchdog-Remediation hängt davon ab, die fokussierte Regression und
den FND-PARENT-0059-FD-9-Lock-Reuse-Control zu erhalten. FND-PARENT-0058-
Port-Allokation und FND-PARENT-0060-Work-Conserving-Refill bleiben getrennte
Lifecycle-Controls; FND-SONAR-0016 bleibt der aggregierte Quality-Gate-Record.

Die lokale Remediation ist nur vom Parent bestätigte Task-Konversations-
Evidence. Es wurden keine aufbewahrte Filesystem-Receipt und kein
Hosted-Successor-Ergebnis geliefert. Deshalb ist das Finding P1 fixed /
feasible_now und ein Release-Blocker, nicht verified, closed, deferred oder
risk accepted.

Erfasst 2026-07-26T21:23:07Z als
local_watchdog_remediation_validated_hosted_successor_pending.
