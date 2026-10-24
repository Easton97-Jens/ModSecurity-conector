# Change Record: CR-20261010-nginx-intervention-outcome-projection

**Sprache:** [English](CR-20261010-nginx-intervention-outcome-projection.md) | Deutsch

Gezielte Collector-Korrektur; frische Runtime-Bestätigung bleibt offen.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261010-nginx-intervention-outcome-projection |
| Datum (UTC) | 2026-10-10 |
| Basis-Revision | `dca17fd5690c2ec2b8806024d1061744db8c3ad8` |

## Motivation und Problemstellung

Der historische Full97 auf der Basis-Revision hatte 80 Case-PASS, neun FAIL und acht NOT_EXECUTED. Completion-/Cleanup-Defaults überschrieben beobachtete Interventionsfelder.

## Akzeptanzkriterien

Die passende transaktions-/regel-/phasengebundene Entscheidung bewahren; mehrdeutige Identitäten ablehnen und echte technische Störungen erhalten.

## Implementierungsentscheidung und Begründung

Interventionsentscheidungen werden getrennt vom späteren Lifecycle-Zustand projiziert. Nicht passende oder widersprüchliche Interventionen liefern keine Entscheidungswerte. Der erste belegte technische Fehler bleibt maßgeblich.

## Geänderte Dateien

`ci/runtime/lifecycle/collect-no-crs-source.py`, `tests/test_no_crs_outcome_projection.py`, this EN/DE record pair.

## Ausgeführte Befehle

`rtk proxy env PYTHONNOUSERSITE=1 /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python -m unittest -v tests.test_nginx_first_byte_binding tests.test_no_crs_outcome_projection tests.test_collect_no_crs_source_helpers tests.test_collect_no_crs_source tests.test_native_first_byte_shell_environment`: 86 Tests bestanden, Exit 0. Erster A-RED-Lauf mit Exit 1 reproduzierte 403→0 sowie Cross-TX-/Prioritätslücken; eine ungültige Allow-Action-Fixture wurde korrigiert.

## Security-Auswirkung


Validatoren, Datenschutz-Allowlist, Required-Scope und Produktsemantik nicht abgeschwächt. Der Receipt speichert keinen Response-Payload. MRTS unverändert.

## Runtime-Evidence

Historischer R13 unverändert. Offline-Fixtures sind kein neuer Runtime-Lauf. Frischer echter begrenzter Fokus und integrierte SHA-Evidence liegen beim Koordinator und werden hier noch nicht behauptet.

## Bekannte Einschränkungen

Unit-Regressionen sind kein Full97- oder Protected-Exact-Head-Nachweis. Tests liefen auf der uncommitted Sourceüberlagerung der Basis-Revision, nicht als Exact-Head-Runtime. Die aufgeführten Test-Payloads wurden in `rtk proxy bash -c` mit Log-/Exit-Erfassung ausgeführt. Python-Kompilierung, Shell-Syntax, Change-Record-Struktur und `git diff --check` bestanden. ShellCheck mit `--severity=warning` meldete auf Basis und geändertem Harness dieselben sieben bestehenden Warnungen, jeweils Exit 1; keine Unterdrückung.

## Verbleibende Risiken

Der unabhängige Review zeigte, dass ein globales technisches Fehlerveto positive generische Reset-/Timeout-/Resume-Verträge ablehnen würde. Die Folgekorrektur begrenzt das Veto auf die acht betroffenen normalen Interventions-/First-Byte-IDs; fünf positive Fault-Kontrollen reproduzieren die Regression vor der Korrektur. Eine Rule-ID allein unterscheidet normale und Fault-Verträge nicht ausreichend. Der ursprüngliche A-Commit wird nicht umgeschrieben.

Frischer Phase-3-Deny/Redirect- und Phase-4-Safe/Strict-Fokus muss Entscheidungen, Rollen und Cleanup prüfen.

## Nicht ausgeführte Prüfungen mit Begründung

Neuer Full97 nicht freigegeben. Protected-/Admin-Operationen außerhalb des Scopes. Vollständiger Lint, frisches CI/Sonar und Veröffentlichung werden durch diesen Worker nicht behauptet.

## Finaler Diff- und Review-Status

Gezielte Sourceänderungen für unabhängigen Review und separaten Commit vorbereitet. Dieser Worker führte keinen Commit, Push, Merge, Retarget oder Undraft aus.
