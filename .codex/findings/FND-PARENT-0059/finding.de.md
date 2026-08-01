# FND-PARENT-0059 — Legacy-Stale-Full-Matrix-Lock kann Scheduler-Service verweigern

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0059 |
| Kategorie | security_validated |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / medium / validated |
| Status / Machbarkeit | fixed / feasible_now |
| Release-Blocker / sicherheitsrelevant | ja / ja |
| Scope | Lokale Full-Matrix-Scheduler-Lock- und Descriptor-Vererbungsgrenze |

## Validiertes Verhalten, Scope und Sicherheitsinvariante

Der frühere Full-Matrix-Scheduler verwendete ein mkdir-Lock-Verzeichnis. Wurde
sein Owner vor dem Cleanup mit SIGKILL beendet, blieb dieses Verzeichnis
bestehen. Ein späterer Scheduler behandelte den verwaisten Pfad als lebenden
Owner und konnte dadurch dauerhaft keinen Service erhalten.

Die Invariante ist, dass ein lebender Scheduler einen regulären Non-Symlink-
.full-matrix-run.lock unter privatem MATRIX_ROOT auf FD 9 öffnet, flock -n 9
erwirbt und diese FD über seine gesamte Laufzeit hält. Ein konkurrierender
Scheduler kann nicht eintreten, releasen, ersetzen oder einen Live-Lock
umgehen. FD 9 wird an laufende Job-/Make-Nachfahren vererbt. Deshalb gibt
SIGKILL des Scheduler-Parents den Lock absichtlich nicht frei, solange ein
solcher Nachfahr läuft; erst wenn der letzte Holder endet, gibt der Kernel ihn
frei und derselbe Lockpfad kann wiederverwendet werden. Es gibt keinen
sekundären Ownership-State und kein Release-Interface.

Die finale lokale Remediation ist direkt in
ci/runtime/lifecycle/run-full-matrix-parallel.sh implementiert. Sie verwendet
eine POSIX-Shell-FD 9 und flock -n 9 auf der privaten regulären Lock-Datei über
die gesamte Scheduler-Laufzeit und für ihre geerbten Job-/Make-Nachfahren.

## Evidenz und Reproduktion

Der finale Current-Task-Security-Review des Parents bestätigt den
veralteten-mkdir-Lock-Zustand und die lokale Remediation. Der exakt vom Parent
bestätigte lokale Befehl war:

PYTHONDONTWRITEBYTECODE=1 python3 -W error::ResourceWarning -m unittest -v tests.test_full_matrix_parallel_scheduler

Er endete mit 0; acht Scheduler-Tests bestanden, darunter:

- test_scheduler_rejects_a_live_full_matrix_lock_owner
- test_scheduler_lock_outlives_a_sigkilled_parent_until_its_job_descendant_exits

Diese Evidence ist nur in der Task-Konversation aufbewahrt; für dieses Finding
wurde kein Filesystem-Receipt und kein Hosted-Exact-Successor-Receipt
geliefert. Zur Reproduktion des ursprünglichen Zustands den früheren
mkdir-Lock erwerben, seinen Owner vor Cleanup mit SIGKILL beenden und einen
zweiten Scheduler starten. Danach die finale Implementierung für
Live-Owner-Contention sowie dafür ausführen, dass geerbte FD 9 den Lock nach
SIGKILL des Scheduler-Parents aktiv hält, bis der letzte Job-/Make-Nachfahr
endet.

## Auswirkung, Ursache und Remediation

Ein verwaister Lock kann spätere Full-Matrix-Runs verweigern und
Release-Evidence ungültig machen. Ein separater Lock-Control-Pfad könnte
außerdem einem konkurrierenden Prozess
Release-Impersonation gegen einen lebenden Owner ermöglichen. Dies ist eine
validierte P1-Availability-/Security-Grenze und ein Release-Blocker.

Die Ursache war, einen dauerhaften mkdir-Pfad als Liveness-Beweis zu
behandeln. Der Release-Impersonation-Review verwarf ein separates
Lock-Control-Design. Die finale Remediation hält Ownership in der laufenden
Shell und ihren laufenden Job-/Make-Nachfahren: FD 9 hält flock -n 9, bis der
letzte geerbte Descriptor schließt. SIGKILL nur des Scheduler-Parents umgeht
diese Ownership nicht; der Kernel gibt den Lock erst frei, nachdem der letzte
Holder endet. Sie muss die fokussierten Tests und die vollständige
Scheduler-Isolation erhalten.

## Akzeptanz und Validierung

Akzeptanz erfordert:

- ein lebender Owner mit FD 9 und flock -n 9 weist einen konkurrierenden
  Scheduler ohne Release, Ersetzung oder Umgehung ab;
- SIGKILL des Scheduler-Parents hält den Kernel-Lock aktiv, solange ein
  Job-/Make-Nachfahr geerbte FD 9 behält; nachdem der letzte Nachfahr endet,
  gibt der Kernel den Lock frei und ein späterer Scheduler kann denselben Pfad
  erwerben;
- die Lock-Datei ist regulär und Non-Symlink unter privatem MATRIX_ROOT;
- nur der Shell-gehaltene-FD-9-Ownership-Pfad bleibt, ohne sekundären
  Control-Pfad oder Release-Interface;
- alle acht Scheduler-Tests einschließlich der zwei genannten Regressionen
  bestehen; und
- frische Hosted-Exact-Successor-Evidence bestätigt das Verhalten ohne
  Lockerung von Isolation oder Result-Policy.

Den genannten Unittest-Befehl mit einem aufbewahrten lokalen Receipt erneut
ausführen, Live-Owner-Contention und den SIGKILL-Parent-/geerbte-Nachfahr-
Control ausführen und danach frische Hosted-Exact-Successor-Full-Matrix-,
Producer-, Review- und Protected-Integration-Evidence vor einer fixed- oder
verified-Disposition beschaffen.

## Abhängigkeiten, Restrisiko und Historie

Dieses Finding ist mit FND-PARENT-0058 verwandt, aber kein Duplikat: 0058
besitzt Port-Range-Allokation und Ready-Artifact-Scheduler-Reliability,
während dieser Record die Shell-gehaltene-Kernel-Lock- und
Descriptor-Vererbungs-Preservation-Grenze besitzt.
FND-SONAR-0016 bleibt der aggregierte Quality-Gate-Record.

Das Acht-Test-Ergebnis ist nur vom Parent bestätigte Task-Konversations-
Evidence. Bis ein lokaler Receipt und ein Hosted-Exact-Successor-Ergebnis
aufbewahrt sind, bleibt das Finding P1 in_progress / feasible_now und ein
Release-Blocker. Es werden weder Risikoakzeptanz, Suppression,
Framework-/MRTS-Aktion, Gitlink-Update, Close, Merge noch Delivery behauptet.

Erfasst 2026-07-26T20:14:08Z als
stale_full_matrix_lock_dos_validated_and_local_guarded_remediation_recorded.
Aktualisiert 2026-07-26T20:37:23Z: SIGKILL nur des Scheduler-Parents gibt
geerbte FD 9 nicht frei; der Kernel gibt den Lock erst frei, nachdem der letzte
Job-/Make-Nachfahr endet.
