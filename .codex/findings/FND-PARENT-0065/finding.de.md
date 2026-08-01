# FND-PARENT-0065 — Body-Processor-Metadaten können über eine artefaktabgeleitete Case-ID einen Request-Body außerhalb der Safe Root lesen

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0065 |
| Kategorie | security_validated |
| Repository / Ownership | Parent / Parent |
| Priorität / Schweregrad / Konfidenz | P2 / low / validated |
| Status / Feasibility | fixed / feasible_now |
| Release-Blocker / Security-relevant | false / true |
| Connector / Profil | NGINX-Zweig validiert; Body-Processor-Analysis-Generated-Report |

## Zusammenfassung

Auf Parent-Source-Revision 9f23ae2c5fe908cef38f203be03f93fda75a8dd7
bewies ein kontrollierter Pre-Fix-NGINX-Probe, dass eine artefaktabgeleitete
case_id ../../../outside den generierten Request-Body-Kandidaten außerhalb der
konfigurierten Safe Root verschieben kann. request_body_bytes() las danach den
externen Sentinel conf/request-body.bin und gab dessen Vorschau sowie passende
SHA-256 aus, während die legitime In-Root-Kontrolle lesbar blieb. Der Probe
belegt keine externe Content-Offenlegung über generated_body_length().

## Beobachtetes und erwartetes Verhalten

generated_config_path() hängt entry["case_id"] an einen aus einer sicheren
Evidence-Datei abgeleiteten Pfad an. Im validierten NGINX-Zweig liest
request_body_bytes() danach config_path.parent / "request-body.bin" direkt,
ohne den abgeleiteten Pfad zuerst über safe_existing_file() zu führen; dies ist
der bestätigte Content-Read-/Offenlegungs-Sink. generated_body_length()
konstruiert den Kandidaten ebenfalls und führt eine ungeschützte is_file()-
Prüfung aus, aber sein späterer read_text()-Pfad wendet Safe-Root-Gating bereits
vor dem Content-Read an.

Die Safe-Root-Containment-Invariante muss nach Auflösung jedes
artefaktabgeleiteten Pfadsegments gelten. Ein externer abgeleiteter Body muss
abgewiesen werden und stattdessen das bereits unterstützte Request-Body-Fallback
verwenden. Die Reparatur darf Safe Roots nicht erweitern und die
Report-Path-Validierung nicht abschwächen.

## Impact, Source-to-Sink-Pfad und Voraussetzungen

    artifact record case_id -> generated_config_path -> config_path.parent /
    request-body.bin -> request_body_bytes() direct read_bytes() -> body preview / SHA-256

Der Dateiname ist fest auf conf/request-body.bin gesetzt; der Probe wählt über
die traversalhaltige case_id nur dessen Parent. Eine Partei muss einen solchen
Artefakt-Record liefern können, der gewählte Out-of-Root-Parent muss eine
reguläre lesbare Datei mit genau diesem Suffix enthalten, und case_metadata()
muss request_body_bytes() für den Record erreichen. Evidence- und Case-Pfade
blieben im Nachweis selbst innerhalb der konfigurierten Safe Root.

Dies ist eine begrenzte CI-Report-Read-Grenzenverletzung. Sie belegt keinen
normalen Hosted-CI-Angreiferpfad, keinen beliebigen Dateiread, keinen File-Write,
keine Codeausführung, keine Secret-Exposition und keine externe
Report-Veröffentlichung. Es werden weder Release-Blocker noch Risikoakzeptanz
beansprucht.

## Reproduktion und Baseline-Evidence

Der aufbewahrte kontrollierte Pre-Fix-Probe verwendete die Parent-.venv mit
PYTHONNOUSERSITE=1, PYTHONDONTWRITEBYTECODE=1, task-eigenem TMPDIR und
task-eigenem PYTHONPYCACHEPREFIX:

    rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 \
      TMPDIR=<task-tmp> PYTHONPYCACHEPREFIX=<task-pycache> \
      /root/git/ModSecurity-conector/.venv/bin/python -B \
      artifacts/03_validation/pre_fix_body_processor_path_probe.py

Er endete mit 0. Das aufbewahrte Ergebnis meldet
vulnerability_reproduced:true; traversal_preview ist outside-root-sentinel und
seine SHA-256 entspricht outside_sha256
(afeb199d897b997c4b32330b4fa18c6ae6694cd153edd9ddacabb6bcfbfa2c2b).
Die legitime Vorschau bleibt legitimate-in-root-body. Es wird kein roher
Request-Body aufbewahrt.

Die fokussierte Regression wurde absichtlich vor dem Source-Fix ausgeführt und
endete mit 1: Sie erwartete fallback-body, erhielt aber den Out-of-Root-Sentinel.
Dies beweist die reale case_metadata()-Report-Generation-Grenze, nicht nur ein
Helper-Level-Source-Pattern.

| Feld | Wert |
| --- | --- |
| Run | 20260729-parent-ci-sonar-remediation |
| Baseline-Source | 9f23ae2c5fe908cef38f203be03f93fda75a8dd7 |
| Pre-Fix-Ergebnis | /var/tmp/codex/ModSecurity-conector/runs/20260729-parent-ci-sonar-remediation/evidence/security-diff-ci-a-9f23ae2-20260729T074736Z/artifacts/03_validation/pre_fix_body_processor_path_probe.result.json |
| Pre-Fix-SHA-256 | 1ac99356e987dc8a95f5715ec508da16b1007cfbc93f31e4c48bdd2485cdc826 |
| Regressionsfehler | .../artifacts/03_validation/focused_regression_failure.md |
| Regressions-SHA-256 | 5deb32d93b42a4b71ec6fe7cb19e927c4c544a9d576685f61708c15b75512392 |

## Lokale Candidate-Evidence, absichtlich keine Statusänderung

Der lokale Candidate leitet den Body-Kandidaten durch safe_existing_file().
Sein aufbewahrter Post-Fix-Probe meldet vulnerability_reproduced:false; sowohl
Traversal- als auch Symlink-Varianten fallen auf fallback-body zurück, während
die legitime In-Root-Kontrolle lesbar bleibt. Seine Ergebnis-SHA-256 ist
1dcce56a4de6b03f63d1b459d865211eb39fc5a93fa3f2cda2d13a8dbb6a223a.

Die aufbewahrte finale lokale Diff-Review hat SHA-256
a2904a5561dca0fd7646f27b0987baf64ba84fc39dd4c33e74c86466fa86e5ad und meldet
keinen verbleibenden Changed-Path-Candidate. Dies ist nur lokale
Remediation-Evidence. Sie macht den Record weder fixed noch verified und belegt
weder PR, Hosted-Exact-Head, Merge noch Master-Evidence.

## Root Cause und Remediation-Richtung

Der Generator validiert Artefakt-Evidence und Case-Datei über
safe_existing_file(), behandelt die artefaktabgeleitete case_id jedoch als
Pfadkomponente und konstruiert danach den benachbarten Body-Kandidaten ohne
erneute Anwendung dieses Controls. request_body_bytes() liest diesen Kandidaten
direkt; generated_body_length() führt vor seinem separat gegateten
read_text()-Aufruf eine ungeschützte is_file()-Prüfung aus.

Sowohl generated_body_length() als auch request_body_bytes() müssen
config_path.parent / "request-body.bin" vor Prüfung oder Read über
safe_existing_file() auflösen. Fokussierte Negativ-Coverage für eine
traversalhaltige case_id und einen In-Root-request-body.bin-Symlink, der nach
außerhalb auflöst, sowie eine In-Root-Kontrolle und eine Fallback-Body-Kontrolle
ergänzen. Scanner-Regeln, Exclusions, Suppressions, Quality Gates,
Report-Output-Containment und Allowed-Root-Policy nicht ändern.

## Akzeptanzkriterien und Validierungsplan

1. Die ursprüngliche ../../../outside-Reproduktion liefert keine externe
   Vorschau oder SHA-256 mehr.
2. Eine traversalhaltige case_id und ein In-Root-request-body.bin-Symlink, der
   nach außerhalb auflöst, können request_body_bytes() keinen Content außerhalb
   konfigurierter Safe Roots offenlegen lassen; beide Body-Helper weisen den
   abgeleiteten Kandidaten konsistent ab.
3. Eine legitime In-Root-request-body.bin behält ihre bisherigen Metadaten.
4. Fehlende oder abgewiesene generierte Body-Dateien bewahren das
   Fallback-Request-Body-Verhalten.
5. Fokussierte Tests, Python-Kompilierung und eine Exact-Diff-Security-Review
   bestehen ohne Control-Abschwächung.

Die nächste Verifikation muss den ursprünglichen Nachweis (oder einen
gleichwertigen fokussierten Test) gegen den reparierten Source und danach seine
legitime In-Root- sowie In-Root-Symlink-der-nach-außen-auflöst-Kontrollen durch
dieselbe case_metadata()-Grenze ausführen.

## Abhängigkeiten, Deduplizierung und Restrisiko

Es gibt keine externen Abhängigkeiten oder Blocker für eine Parent-only-
Reparatur. FND-PARENT-0026 ist verwandt, aber getrennt: Es betrifft breite
caller-kontrollierte Runtime-Roots. Das archivierte FND-PARENT-0034 ist ebenfalls
getrennt: Es betrifft Report-Publication-Writes und Symlink-Clobber, nicht diesen
begrenzten Read-Pfad.

Bis eine Reparatur verifiziert ist, erlaubt die Baseline den oben beschriebenen
begrenzten externen Read. Dieser Record beansprucht weder normale Hosted-CI-
Angreiferreichweite noch Secret-Exposition, Risikoakzeptanz, PR, Delivery,
Merge oder Master-Ergebnis.

## Historie

- 2026-07-29T08:11:35Z: Kontrollierter Pre-Fix-Safe-Root-Bypass reproduziert.
- 2026-07-29T08:11:35Z: Lokale Candidate-Kontrolle und finale Diff-Review
  aufbewahrt, ohne das Finding von validated zu ändern.
