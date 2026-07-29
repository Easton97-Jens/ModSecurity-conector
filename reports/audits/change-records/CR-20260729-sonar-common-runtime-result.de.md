# Change Record: Parent-Common-Runtime-Smoke-Result-Objekt-Refaktorierung

**Sprache:** [English](CR-20260729-sonar-common-runtime-result.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-common-runtime-result |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc |
| Grenze | Parent-`common/`-Runtime-Smoke-Quelltext, direkte Parent-Regressionstests und dieses englisch/deutsche Change-Record-Paar mit Indizes. Framework/MRTS, Gitlinks, Workflows, SonarQube-Cloud-Konfiguration, Exclusions, Suppressions, Quality Gates und `master` bleiben unverändert. |
| Delivery-Status | Draft-PR [#164](https://github.com/Easton97-Jens/ModSecurity-conector/pull/164) existiert. Sein erster Head `265e3e90debb0c33546cbd6aa4c32dc4a1bf4fb3` bestand alle anwendbaren GitHub Actions, scheiterte jedoch am SonarQube-Cloud-New-Code-Gate. Der Source-Follow-up-Head `9ea886a6fd4a8e8b27b1e0c3d7c5102c6d4e3278` bestand anschließend seine anwendbaren GitHub Actions und das SonarQube-Cloud-Quality-Gate mit 0 New Issues und 0,0 % New-Code-Duplizierung. Diese additive Dokumentationskorrektur benötigt vor dem Ready-Setzen des Drafts einen frischen Exact-Head-Gate; es wird kein Merge oder `master`-Integration behauptet. |

## Motivation und Problemstellung

Der aktuelle `master` hat 623 ungelöste SonarQube-Cloud-Zeilen und 1.057 Duplikatzeilen (0,2 %). SonarQube Cloud identifiziert zwei `python:S107`-Zeilen an den 26-Parameter-Signaturen `writer_args` und `write_result` in `common/scripts/run_local_runtime_smoke.py`. Das Paar ist zugleich der einzige Common-CPD-Block dieser Datei: Zeilen 1428 und 1610 mit jeweils 26 Zeilen, also 52 Duplikatzeilen.

Der Runner gibt Evidence für die lokale Runtime-Smoke-Automation aus. Jede Option, jeder Wert, jeder Default, jeder PASS/BLOCKED-Status und jeder Missing-Dependency-Eintrag an `write_smoke_result.py` muss erhalten bleiben.

## Akzeptanzkriterien

- Ergebnisdaten werden durch einen typisierten unveränderlichen Wert statt durch doppelte lange Funktionssignaturen getragen.
- `writer_args` erzeugt für ein CRS-gestütztes blockiertes Runtime-Ergebnis dieselbe Option/Wert-Evidence einschließlich Status, Request-Status, Regelidentität, Security-Evidence, Pfaden und Missing Dependencies.
- Die Runtime-Output-Containment-, CRS-Source-, Request-Body-Framing- und Finite-Socket-Controls bleiben bestanden.
- Der genaue Draft-PR-Head muss 0 New Issues, 0,0 % Duplication on New Code, ein bestandenes Quality Gate und weniger Duplikatzeilen insgesamt als die aufgezeichnete `master`-Baseline ausweisen.

## Implementierungsentscheidung und Begründung

`SmokeResult` ist eine eingefrorene Dataclass mit den zuvor positionalen Evidence-Feldern. `writer_args` und `write_result` nehmen diesen einen Wert. Die erste gehostete Analyse zeigte ein neues `python:S3776` bei `writer_args` und neue Duplikatblöcke in der Result-Konstruktion. Der Follow-up extrahiert unveränderliche `BackendEvidence`, leitet `SmokeWriterValues` getrennt ab und baut jedes Ergebnis über `smoke_result`. Damit bleiben Status und Evidence-Ownership explizit, ohne wiederholte positionale Feldreihenfolge oder Result-Blöcke. Der Writer nutzt weiterhin dasselbe Command-Line-Protokoll und denselben `write_smoke_result.py`-Entry-Point.

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
| Derselbe Command nach dem Sonar-Remediation-Follow-up | außerhalb der Sandbox bestanden: 39 Tests, einschließlich direkter `BackendEvidence`-/Pfad-Komposition, Erhalt des CRS-Werts im Simple-Backend sowie der bisherigen Writer-Result- und Request-Body-Controls. |
| Derselbe Command im sauberen Integrations-Clone vor dieser Dokumentationskorrektur | bestanden: 39 Tests, einschließlich Result-/Evidence-Komposition, Erhalt des CRS-Werts im Simple-Backend, Runtime-Pfad- und Request-Body-Controls. |
| Dieselbe Suite innerhalb der Sandbox | durch die Loopback-Socket-Restriktion der Sandbox blockiert (`PermissionError: [Errno 1] Operation not permitted`), nachdem die nicht socketbasierten CRS-/Pfad-Tests bestanden. Der Outside-Sandbox-Lauf ist das aufgezeichnete vollständige Ergebnis. |
| `python -m py_compile common/scripts/run_local_runtime_smoke.py tests/test_common_runtime_smoke_crs_source_security.py` im sauberen Integrations-Clone | mit task-eigenem Bytecode-Cache bestanden. |
| `git diff --check` | nach dem Follow-up erneut bestanden. |

## Ausgeführte Befehle

Der oben genannte Test-Command, die Kompilierung und `git diff --check` sind
die bisher aufgezeichneten lokalen Validierungsbefehle. Der erste exakte
PR-Head bestand anwendbare GitHub Actions, scheiterte jedoch an den New-Code-
Sonar-Kriterien; der Source-Follow-up-Head
`9ea886a6fd4a8e8b27b1e0c3d7c5102c6d4e3278` bestand die anwendbaren GitHub
Actions und die erfolgreiche Sonar-Analyse. Es wird kein Connector-Host-
Command als lokale Evidence dargestellt. Diese Source-Head-Evidence belegt
keinen späteren rein dokumentarischen PR-Head.

## Runtime-Evidence

Die fokussierten Tests verwenden nur lokale Loopback-HTTP-Handler. Sie prüfen Request-Body-Framing und begrenzte Reads, starten aber keinen Envoy-, Traefik-, Lighttpd- oder libModSecurity-Host-Runtime. Sie sind Regression-Evidence für die geänderte Writer-Grenze, keine Connector-Host-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Host-Connector-Runtime- oder libModSecurity-Integration-Lauf wurde ausgewählt: Diese Refaktorierung ändert kein Host-Protokoll oder Adapter-Verhalten.
- Der erste exakte PR-Head bestand alle anwendbaren GitHub Actions, SonarQube
  Cloud meldete jedoch ein neues `python:S3776`, 58 neue Duplikatzeilen
  (23,9 %) und 1.094 Duplikatzeilen insgesamt. Diese nicht erfüllten
  Akzeptanzkriterien lösten die Follow-up-Extraktion aus. Der Source-Follow-
  up-Head `9ea886a6fd4a8e8b27b1e0c3d7c5102c6d4e3278` bestand anschließend
  seine anwendbaren GitHub Actions und das SonarQube-Cloud-Quality-Gate mit
  0 New Issues und 0,0 % New-Code-Duplizierung. Ein späterer rein
  dokumentarischer Head benötigt weiterhin seinen normalen Exact-Head-Gate.
- `make check-bilingual-docs` ist durch 20 vorbestehende Links in das nicht populierte Framework-Submodul blockiert. Nach der Korrektur der erforderlichen Record-Überschriften meldet er keinen Fehler für dieses Record-Paar; der breite Check kann erst nach Auschecken dieser externen Voraussetzung bestehen.

## Bekannte Einschränkungen

Die genaue gehostete Source-Follow-up-Analyse bei
`9ea886a6fd4a8e8b27b1e0c3d7c5102c6d4e3278` belegte eine niedrigere globale
Duplikatzeilenmetrik, das Fehlen der neuen `python:S3776`-Zeile und das
erforderliche New-Code-Quality-Gate. Die typisierten Werte halten Felder flach
unveränderlich; ihre Tuple-`missing`-Collection verhindert mutable
Dependency-Einträge, während die `argparse.Namespace`-Quelle die bestehende
mutable Input-Grenze bleibt. Ein rein dokumentarischer Nachfolger benötigt
vor dem Merge weiterhin seinen eigenen geschützten Exact-Head-Gate.

## Verbleibende Risiken

Die bestehenden Runtime-Smoke-Caller-Pfade sind durch die fokussierten Result-
Argument- und Boundary-Tests abgedeckt, Connector-Host-Verhalten liegt jedoch
außerhalb der Evidence dieser Source-only-Refaktorierung. Der Source-Follow-
up besitzt gehostete SonarQube-Cloud-Evidence; jeder Nachfolger-Head muss den
normalen geschützten PR-Gate wiederholen.

## Finaler Diff- und Review-Status

Der Diff beschränkt sich auf den Common-Runtime-Smoke-Writer-Contract, seine
direkten Regressionstests und erforderliche zweisprachige Traceability. Es
sind weder Framework- oder MRTS-Quelltext/Gitlink noch Workflow,
Scanner-Control, Suppression oder Default-Branch enthalten. Der Source-
Follow-up ist gepusht und besitzt die aufgezeichnete bestandene Exact-Head-
Hosted-Analyse. Der Draft bleibt offen, und diese Dokumentationskorrektur
benötigt vor Ready-Transition oder geschützter Übergabe frische Exact-Head-
Checks.
