# Change Record: NGINX-Konfigurations-Receipt-Collection

**Sprache:** [English](CR-20261001-nginx-configtest-collection.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261001-nginx-configtest-collection` |
| Datum (UTC) | `2026-10-01` |
| Basis-Revision | `794d16d7d387512213bc2e8d8b2f3199e5dbc6ce` |

## Motivation und Problemstellung

Der Source-Collector erhielt den neuen expliziten Konfigurations-Receipt und
seine Retained-Artifact-Referenz nicht. Eine reine Konfigurationsoperation darf
nicht allein wegen eines rohen Case-Records als Request-Ausführung gelten.

## Akzeptanzkriterien

Begrenzte allowlistete Receipt-/Run-Felder und eine autorisierte vorhandene
Referenz auf das Bundle aus fünf Dateien erhalten. Fehlende Authority,
externe oder relative Pfade, Symlinks, fehlende Dateien und unerwartete
Artefaktschlüssel abweisen. Konfigurationsrecords dürfen keine Rule-/
Transaction-Events erzeugen und keine Host-Starts oder Requests behaupten.
Vorhandene HTTP-Evidence muss ihre bisherige Bedeutung behalten.

## Implementierungsentscheidung und Begründung

Konfigurations-Receipt durch `collect-no-crs-source.py` erhalten, ohne
Evidence zu erzeugen oder FAIL zu ersetzen. `artifacts.configtest_dir` nur
innerhalb des explizit autorisierten Source-Roots und mit den geschlossenen
Dateien `nginx-binary`, `nginx-module.so`, `nginx.conf`, `stdout.log` und
`stderr.log` akzeptieren. Das begleitende Framework validiert Receipt-
Semantik und hasht verwaltete Artefakte erneut. Die separate Treiber-/Wiring-
Änderung besitzt tatsächliche Konfigurations-Invocation und Selected-Case-
Dispatch.

## Security-Auswirkung

Der Collector ist Consumer, kein Event-Produzent. Er erhält Containment,
Symlink-Abweisung, begrenzte Metadaten und Payload-Ausschlüsse. Ein Phase-0-
Receipt kann einen Request-Record nicht zu Konfigurationsnachweis machen.
Eine reine Config-Source behält `started=false` und `requests_sent=false`;
ein echter HTTP-Case zählt weiterhin als Request-Ausführung. Weder fehlende
Required-Cases noch nicht zugehörige Modulfehler werden zu PASS befördert.

## Geänderte Dateien

- `ci/runtime/lifecycle/collect-no-crs-source.py`
- `tests/test_nginx_configtest_collection.py`
- Dieser EN/DE-Change-Record und das Archivindex-Paar

## Ausgeführte Befehle

Alle Shell-Befehle verwenden RTK. Der Task-Koordinator beobachtete 6
bestandene Collector-Tests und einen breiteren Parent-Fokus mit 186
bestandenen Tests in 57.106 Sekunden. Der finale kombinierte Fokus-Befehl
verwendet den vorhandenen Framework-Interpreter:
`rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/.venv/bin/python -m unittest tests.test_nginx_configtest_driver tests.test_nginx_configtest_collection -v`.
Der finale kombinierte Rerun besteht 18 Tests in 12.304 Sekunden.
Der fokussierte Rerun besteht alle 6 Tests in 0.190 Sekunden. RTK-gekapseltes
`make PYTHON=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/.venv/bin/python check-bilingual-docs check-doc-links` besteht mit externen
Task-`TMPDIR`/`BUILD_ROOT` und unverändertem physischem Parent-Framework-Pin.
Die eingefrorene Framework-No-CRS-Suite besteht 159 Tests in 112.402 Sekunden,
Exit 0; vollständiges `make lint` endet mit Exit 0 (Session 8526). Framework-
Fokus besteht 27 Tests in 3.144 Sekunden und 3.651 Sekunden beim unabhängigen
Review. Kein unbeobachteter Check wird behauptet.

## Runtime-Evidence

Die echte Retained-Diagnose `runs/diagnosis/nginx-configtest-retained-jaYdBrvH`
erzeugt kanonischen `invalid_boolean`-PASS nur für Exit 1 mit exakter Boolean-
Ablehnung. Tatsächliches NGINX mit einem kontrollierten Non-ELF-Modul endet
ebenfalls mit Exit 1, erzeugt aber Case-FAIL mit `unexpected_config_error`.
Framework-Finalisierung erhält fünf verwaltete Artefakte je Kontrolle und
hasht sie erneut. Beide erzeugen null Native-Events, keine Starts und keine
Requests; Source-/Canonical-Aggregate bleiben FAIL, weil andere Required-
Requests absichtlich ausgelassen wurden. Der strikte Checker für
`analysis/nginx-configtest-retained-check-20261001.json` endet mit Exit 0.
Dies sind Retained-Build-Diagnosen, kein Exact-Head-E2E-PASS.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Full-E2E, Push, PR-Eingriff, Protokolllauf, Gitlink-Update oder Merge.
Required-Coverage bleibt unvollständig. Der Framework-spezifische Change-
Record-Checker ist für Parent-Templates nicht anwendbar; native Parent-
Bilingual-/Pfad-/Link-Checks gelten, ohne nicht zugehörige historische Records
oder Validatoren zu verändern.

## Bekannte Einschränkungen

Receipt-Semantik liegt beim Framework; bloßes Erhalten einer Referenz belegt
keinen gültigen kanonischen PASS. Dieser Slice ruft keine Cases auf. Neun
weitere konfigurationsbezogene Required-Records bleiben außerhalb der
initialen `invalid_boolean`-Implementierung.

## Verbleibende Risiken

Retained-Artifact-Bytes und vom Aufrufer übergebene Source-Identitäten
benötigen eigene Verifikation. Die Diagnose verwendet einen gecachten
C-Build und belegt daher keinen Build aus dem aktuellen Parent-Exact-Head.

## Finaler Diff- und Review-Status

Diese unabhängige Collector-Änderung wird bei vollständiger Validierung
getrennt von Treiber/Wiring geprüft und committet. Beim Verfassen des Records
wird kein Commit, Push oder Merge behauptet. Vorbereitete Protokollarbeit und
alle Gitlinks bleiben außerhalb dieser Änderung.
