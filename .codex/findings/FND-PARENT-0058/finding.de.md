# FND-PARENT-0058 — Full-Matrix-Parallel-Jobs überlappen Response-Header-Backend-Portbereiche

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0058 |
| Kategorie | test_failure |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / validated |
| Status / Machbarkeit | fixed / feasible_now |
| Release-Blocker | ja |
| Scope | Loopback-Full-Matrix-Runtime, FORCE_ALL_CASES=1 mit globaler CPU-Parallelität |

## Validiertes Verhalten, Scope und Auswirkung

Der Parent-Runner startet Apache, NGINX und HAProxy parallel mit nominellen
Main-Port-Offsets 0, +1000 und +2000 vom Variant-Base-Port. Apache und NGINX
verwenden beide eine PORT+1000-Response-Header-Backend-Auswahl. Dadurch kann
ein Apache-Backend mit dem NGINX-Main-Range kollidieren und ein NGINX-Backend
mit dem HAProxy-Main-Range. Unabhängige Free-Port-Checks haben ein Check-then-
Bind-(TOCTOU-)Fenster; sie sind keine globalen Reservierungen.

Betroffener Code ist ci/runtime/lifecycle/run-full-matrix-parallel.sh
(variant_base_port, connector_offset, run_batch, run_job und
PORT_SEARCH_LIMIT) sowie die Apache-/NGINX-Implementierungen von
start_response_header_backend. Die Kollision ist möglich, wenn parallele
Apache-, NGINX- und HAProxy-Jobs unter FORCE_ALL_CASES=1 Response-Header-Cases
ausführen.

Die resultierende Full-Matrix-Evidence kann aus Scheduler-Gründen statt wegen
eines Connector-Ergebnisses fehlschlagen, blockieren, an einen falschen
Listener binden oder nichtdeterministisch werden. Dies ist ein validierter
P1-Test-/Runtime-Evidence-Reliability-Blocker. Er ist bewusst getrennt von
der plausiblen Workflow-Template-Injection-/S8707-Trust-Boundary-Korrektur in
FND-PARENT-0057 und vom aggregierten Quality-Gate-Status in FND-SONAR-0016.

## Evidenz und Reproduktion

Der retained Task-Receipt ist
/var/tmp/codex/ModSecurity-conector/runs/20260726T185607Z-pr74-fast-validation-hosted-followup/evidence/hosted-observation.md
(Run 20260726T185607Z-pr74-fast-validation-hosted-followup, SHA-256
5c64b4fe03ed670b0d2c25c58c2f770b59ae53bab10851ced35bd9012117d956,
2.978 Bytes). Er verankert das exakte Draft-PR-#74-Follow-up; die validierte
Port-Arithmetik wird aus den aktuellen Parent-Runner- und Harness-Quellen
reproduziert. Der read-only Receipt-Command endete mit 0. PR #74 bleibt Draft;
es werden weder Framework-/MRTS-, Gitlink-, Close-, Merge- noch
Delivery-Aktionen behauptet.

Zur Reproduktion die 0/+1000/+2000-Anordnung des Runners mit Apache
run_apache_smoke.sh:1924 und NGINX run_nginx_smoke.sh:1260 vergleichen und
danach eine anwendbare parallele Full-Matrix-Variante mit FORCE_ALL_CASES=1
ausführen. Bestätigen, dass die Auxiliary-Auswahl nicht gegen den Main- oder
Auxiliary-Range eines anderen parallelen Jobs reserviert ist.

## Remediation, Akzeptanz und Validierung

Die in Arbeit befindliche Parent-Runner-/Test-Korrektur muss disjunkte
dynamische Port-Reservierungen für jeden Main- und Auxiliary-Service
allozieren, jede Reservierung über die Lebensdauer ihres Jobs halten und einen
begrenzten globalen CPU-Scheduler verwenden. Sie muss Per-Job-Isolation,
sichtbare Busy-Port-Fehler, vollständige Coverage und FORCE_ALL_CASES erhalten;
das Wegserialisieren von Coverage ist keine Remediation.

Die aktuelle lokale Implementierung ergänzt
ci/runtime/lifecycle/plan_full_matrix_ports.py. Sie validiert jeden möglichen
Case-/Search-Intervall im fail-closed Bereich 1024..65000
(1024 ist der erste unprivilegierte Port), weist malformed oder
unpackable Pläne vor make ab, serialisiert die Vorbereitung und startet global
begrenzte Runtime-Arbeit erst, wenn Artefakte bereit sind. Diese
Implementationseigenschaften sind noch keine finale Full-Suite- oder
Hosted-Validierungsevidence.

Akzeptanz erfordert:

- paarweise disjunkte Apache-, NGINX- und HAProxy-Main- und
  Response-Header-Ports für jede unterstützte parallele Variante;
- einen fokussierten Allocation-Regressionstest, der beweist, dass kein
  Auxiliary-Port einem aktiven Main- oder Auxiliary-Port eines anderen Jobs
  entspricht;
- einen fokussierten Port-Plan-Control, der beweist, dass jeder mögliche
  Case-/Search-Intervall in 1024..65000 einschließlich des vollständigen
  Zwölf-Job-Zwei-Search-Window-Plans validiert und ein malformed oder
  unpackable Plan vor make abgewiesen wird;
- einen intentionalen Busy-Port-Negativtest, der klar fehlschlägt, ohne sich
  an den Listener eines anderen Jobs zu hängen;
- serialisierte Vorbereitung und globale CPU-Admission erst, wenn die
  erforderlichen Artefakte bereit sind;
- einen legitimen parallelen All-Cases-Control, der innerhalb des
  konfigurierten globalen CPU-Bounds erfolgreich ist und
  Reservierungen/Prozesse aufräumt; und
- frische retained Full-Matrix-Evidence sowie ein erneutes Lesen des
  ursprünglichen Kollisionspfads vor jeder fixed- oder verified-Disposition.

## Abhängigkeiten, Restrisiko und Historie

Dieser Record hängt von der Behandlung der Successor-Evidence in
FND-CROSS-0001 sowie von finaler fokussierter, Full-Suite- und Hosted-Evidence
für den exakten Successor-Parent-Runner-/Test-Patch ab. Bis lokale
Plan-Validierung, Malformed-Plan-Ablehnung, serialisierte Vorbereitung,
Ready-Artifact-Scheduler-Admission und Full-Matrix-Verhalten erneut ausgeführt
sind, kann parallele All-Cases-Runtime-Evidence nichtdeterministisch sein oder
an einen unbeabsichtigten Loopback-Listener binden.

Erfasst am 2026-07-26T18:56:07Z als
full_matrix_parallel_port_range_overlap_validated. Der Status bleibt
in_progress / feasible_now; es werden keine Remediation-Validierung oder
Delivery-Outcome behauptet. Die lokale Plan-/Scheduler-Implementierung wurde
zusätzlich am 2026-07-26T19:46:59Z erfasst; finale Full-Suite- und Hosted-
Validierung bleiben ausstehend.
