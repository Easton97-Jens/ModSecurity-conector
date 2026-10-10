# Change Record: CR-20261009-nginx-body-buffer-event-scope

**Sprache:** [English](CR-20261009-nginx-body-buffer-event-scope.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-body-buffer-event-scope |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `dcbefad1144b38f1545399a9f72967fbb1b3d424` |

## Motivation und Problemstellung

Die Auswahl allein anhand URI vermischte Regelinterventions-Evidence mit legitimer Telemetrie desselben Requests: phase4_append, phase4_completion und transaction_cleanup. Die Append-Telemetrie zeigte diesen Defekt bereits vor dem Cleanup-Metadatenfix.

## Akzeptanzkriterien

Sechs legitime Kontrollen benötigen jeweils genau eine phase4_intervention in response_body mit rule_id 1250001 und exakt typisierter Body-/EOS-Bilanz. Reine Telemetrie, Abweichungen und Duplikate müssen scheitern.

## Implementierungsentscheidung und Begründung

Interventionskandidaten anhand URI und Event-Identität auswählen, danach Phase, Regel und sämtliche bestehenden Bilanzfelder strikt validieren. Andere Telemetrie bleibt unverändert im Originalprotokoll und kann den Nachweis nicht erfüllen.

## Geänderte Dateien

tests/run_nginx_body_buffer_fixture.py; tests/test_nginx_body_buffer_fixture.py; dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

Alle Befehle verwendeten rtk proxy. RED-Mixed-Telemetry-Regression: Exit 1, echte Bilanzierungsablehnung mit unverändertem Validator. GREEN-fokussierte Fixture-/Observation-Tests: Exit 0. Protokolle: extern analysis/nginx-all-required-20261008T124555Z/body-buffer-event-scope/{red,green}.log. Bestehender Parent-.venv-Interpreter mit PYTHONNOUSERSITE=1 und externem Bytecode-Cache. Ruff-Probe: Exit 1, No module named ruff. Syntaxprüfung durch bestehenden AST-Vertrag. Change-Record-Strukturprüfung: Exit 0.

## Security-Auswirkung

Evidence-Annahme bleibt für erforderliche Interventionsidentität, Regel, Phase, Body, EOS und Einmaligkeit fail-closed. Keine Produkt-, Framework-, MRTS- oder Selection-Änderungen.

## Runtime-Evidence

Dieser Worker führte keine gehostete Fixture und keinen Lifecycle aus. Unit-Zeilen sind Testeingaben, niemals Runtime-Evidence.

## Bekannte Einschränkungen

Fokussierte Verträge belegen nur Event-Auswahl und Bilanzierung; frische gehostete Requests bleiben erforderlich.

## Verbleibende Risiken

Unabhängige Prüfung und integrierte gehostete Ausführung stehen aus.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Build, E2E, Commit, Push, CI oder Sonar durch diesen Worker. Ruff fehlt in der bestehenden Umgebung; keine Dependency-Installation.

## Finaler Diff- und Review-Status

Nur vier zugewiesene Dateien; Prüfung durch den Koordinator steht aus. Kein Commit oder Push.
