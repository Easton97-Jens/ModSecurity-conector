# Change Record: Parent-Common-Runtime-Smoke-Result-Objekt-Refaktorierung

**Sprache:** [English](CR-20260729-sonar-common-runtime-result.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-common-runtime-result |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc |
| Grenze | Parent-`common/`-Runtime-Smoke-Quelltext, direkte Parent-Regressionstests und dieses englisch/deutsche Change-Record-Paar mit Indizes. Framework/MRTS, Gitlinks, Workflows, SonarQube-Cloud-Konfiguration, Exclusions, Suppressions, Quality Gates und `master` bleiben unverändert. |
| Delivery-Status | Lokaler Kandidat zum Zeitpunkt der Record-Erstellung. Kein task-eigener Commit, Push, Pull Request, gehostete Analyse, Review, Merge oder `master`-Integration wird behauptet. |

## Motivation und Problemstellung

Der aktuelle `master` hat 623 ungelöste SonarQube-Cloud-Zeilen und 1.057 Duplikatzeilen (0,2 %). SonarQube Cloud identifiziert zwei `python:S107`-Zeilen an den 26-Parameter-Signaturen `writer_args` und `write_result` in `common/scripts/run_local_runtime_smoke.py`. Das Paar ist zugleich der einzige Common-CPD-Block dieser Datei: Zeilen 1428 und 1610 mit jeweils 26 Zeilen, also 52 Duplikatzeilen.

Der Runner gibt Evidence für die lokale Runtime-Smoke-Automation aus. Jede Option, jeder Wert, jeder Default, jeder PASS/BLOCKED-Status und jeder Missing-Dependency-Eintrag an `write_smoke_result.py` muss erhalten bleiben.

## Akzeptanzkriterien

- Ergebnisdaten werden durch einen typisierten unveränderlichen Wert statt durch doppelte lange Funktionssignaturen getragen.
- `writer_args` erzeugt für ein CRS-gestütztes blockiertes Runtime-Ergebnis dieselbe Option/Wert-Evidence einschließlich Status, Request-Status, Regelidentität, Security-Evidence, Pfaden und Missing Dependencies.
- Die Runtime-Output-Containment-, CRS-Source-, Request-Body-Framing- und Finite-Socket-Controls bleiben bestanden.
- Der genaue Draft-PR-Head muss 0 New Issues, 0,0 % Duplication on New Code, ein bestandenes Quality Gate und weniger Duplikatzeilen insgesamt als die aufgezeichnete `master`-Baseline ausweisen.

## Implementierungsentscheidung und Begründung

`SmokeResult` ist eine eingefrorene Dataclass mit den zuvor positionalen Evidence-Feldern. `writer_args` und `write_result` nehmen diesen einen Wert. Alle Call Sites konstruieren benannte Felder; damit sind Status und Evidence-Ownership explizit und es gibt keine positional geordnete Feldliste mehr zwischen beiden Funktionen. Der Writer nutzt weiterhin dasselbe Command-Line-Protokoll und denselben `write_smoke_result.py`-Entry-Point.

## Security-Auswirkung

Die Änderung berührt die Runtime-Evidence-Grenze, ändert jedoch weder Request-Parsing, URL-/Pfad-Validierung, Process-Execution, Output-Root-Validierung noch das Writer-Programm. Der direkte Regressionstest prüft die Werte eines repräsentativen blockierten CRS-Ergebnisses. Die vorhandenen Security-Tests behalten abgelehnte Symlinks, unsichere Roots, schreibbare CRS-Inputs, fehlerhaftes Body-Framing und Oversize-Body-Controls. Der fokussierte Diff-Review fand keinen geschwächten Control und keinen neuen plausiblen Fund hoher oder kritischer Auswirkung.

## Geänderte Dateien

- common/scripts/run_local_runtime_smoke.py
- tests/test_common_runtime_smoke_crs_source_security.py
- dieses englisch/deutsche Change-Record-Paar und beide Indizes

## Tests und tatsächliche Ergebnisse

| Command oder Verfahren | Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests/test_common_runtime_smoke_crs_source_security.py tests/test_local_runtime_smoke_request_body.py` | außerhalb der Sandbox bestanden: 37 Tests, einschließlich des neuen Writer-Result-Argument-Regressionstests und der HTTP-Request-Body-Controls. |
| Dieselbe Suite innerhalb der Sandbox | durch die Loopback-Socket-Restriktion der Sandbox blockiert (`PermissionError: [Errno 1] Operation not permitted`), nachdem die nicht socketbasierten CRS-/Pfad-Tests bestanden. Der Outside-Sandbox-Lauf ist das aufgezeichnete vollständige Ergebnis. |
| `git diff --check` vor Record-Erstellung | bestanden. |

## Ausgeführte Befehle

Der oben genannte Test-Command und `git diff --check` sind die vollständigen
vor der Record-Erstellung ausgeführten Befehle. Es wird kein gehosteter oder
Connector-Host-Command als lokale Evidence dargestellt.

## Runtime-Evidence

Die fokussierten Tests verwenden nur lokale Loopback-HTTP-Handler. Sie prüfen Request-Body-Framing und begrenzte Reads, starten aber keinen Envoy-, Traefik-, Lighttpd- oder libModSecurity-Host-Runtime. Sie sind Regression-Evidence für die geänderte Writer-Grenze, keine Connector-Host-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Host-Connector-Runtime- oder libModSecurity-Integration-Lauf wurde ausgewählt: Diese Refaktorierung ändert kein Host-Protokoll oder Adapter-Verhalten.
- Gehostete SonarQube-Cloud- und GitHub-Actions-Ergebnisse existieren zum Zeitpunkt der Record-Erstellung nicht; sie müssen am genauen gepushten Draft-PR-Head erneut geprüft werden.
- `make check-bilingual-docs` ist durch 20 vorbestehende Links in das nicht populierte Framework-Submodul blockiert. Nach der Korrektur der erforderlichen Record-Überschriften meldet er keinen Fehler für dieses Record-Paar; der breite Check kann erst nach Auschecken dieser externen Voraussetzung bestehen.

## Bekannte Einschränkungen

Nur die genaue gehostete PR-Analyse kann eine niedrigere globale Duplikatzeilenmetrik, den Abschluss der zwei Basis-`python:S107`-Zeilen und das New-Code-Quality-Gate nachweisen. Der typisierte Wert hält Felder flach unveränderlich; seine Tuple-`missing`-Collection verhindert mutable Dependency-Einträge, während die `argparse.Namespace`-Quelle die bestehende mutable Input-Grenze bleibt.

## Verbleibende Risiken

Die bestehenden Runtime-Smoke-Caller-Pfade sind durch die fokussierten Result-
Argument- und Boundary-Tests abgedeckt, Connector-Host-Verhalten liegt jedoch
außerhalb der Evidence dieser Source-only-Refaktorierung. Die gehostete
SonarQube-Cloud-Analyse bleibt die erforderliche Messung für die globalen
Zählkriterien.

## Finaler Diff- und Review-Status

Der Diff beschränkt sich auf den Common-Runtime-Smoke-Writer-Contract, seinen direkten Regressionstest und erforderliche zweisprachige Traceability. Es sind weder Framework- oder MRTS-Quelltext/Gitlink noch Workflow, Scanner-Control, Suppression oder Default-Branch enthalten. Die lokale Validierung bestand; gehostete Delivery-Evidence steht nach Task-Branch-Commit, Push und Draft PR noch aus.
