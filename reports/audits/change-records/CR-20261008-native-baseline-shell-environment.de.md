# Change Record: CR-20261008-native-baseline-shell-environment

**Sprache:** [English](CR-20261008-native-baseline-shell-environment.md) | Deutsch

Begrenzte Shell-Grenzkorrektur; keine Aussage über native Runtime.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-native-baseline-shell-environment |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `461bcd62a3cb2159ec9750db6ad64f0ab6053cc3` |

## Motivation und Problemstellung

ShellCheck meldete acht SC2097/SC2098/SC2034-Warnungen. Die Zuweisungspräfixe für Stage und First-Byte expandieren absichtlich Werte des Aufrufers; die statische Analyse erkannte diese Absicht nicht eindeutig. Der letzte VERIFIED_COMPONENT_CACHE-Reset hatte keinen späteren Verbraucher.

## Akzeptanzkriterien

ShellCheck auf Warnungsebene ohne Unterdrückung bestehen; Kindprozess-Umgebung, quotierte Argumente, Exitstatus und Elternscope erhalten. Kanonische Cache- und Authority-Prüfungen, Required-Auswahl und bisherige Routing-Regression bewahren.

## Implementierungsentscheidung und Begründung

Beide Zuweisungslisten verwenden explizit env: rechte Seiten und Programmpfade expandieren weiterhin in der aufrufenden Shell. Die Stage-Umgebung konsumiert den initial aufgelösten VERIFIED_COMPONENT_CACHE mit demselben kanonischen Wert. Nur dessen letzte tote Zuweisung entfällt; der aktive CONNECTOR_COMPONENT_CACHE-Inventarreset bleibt. Kein sonst ungenutzter Export wird ergänzt.

## Geänderte Dateien

ci/runtime/lifecycle/run-no-crs-baseline.sh; neue tests/test_no_crs_baseline_shell_environment.py; dieses generierte EN/DE-Recordpaar. Keine Änderungen an Framework, MRTS, Katalog, Schema oder Fixtures.

## Ausgeführte Befehle

Alle Befehle liefen über RTK. Parent-Python führte unittest -v für tests.test_no_crs_baseline_shell_environment, tests.test_no_crs_native_authority_wiring und tests.test_nginx_selected_configtest_wiring aus. sh -n und shellcheck -S warning prüften die Baseline. new-change-record.py erzeugte dieses Paar und prüfte das Archiv; git diff --check prüfte Whitespace. TMPDIR war der neutrale externe Taskpfad /var/tmp/codex/ModSecurity-conector/runs/dv-Hm965b; Python-Bytecode und User-Site waren deaktiviert.

## Security-Auswirkung

Kein Bypass, keine Unterdrückung und keine abgeschwächte Auswahl. Tests prüfen echte Shell-Prozessgrenzen mit aufzeichnenden Unit-Doubles, Pfaden mit Leerzeichen, kanonischen Cachewerten und Kind-Exitstatus 23. Keine der beiden Befehlsgrenzen verändert Elternvariablen.

## Runtime-Evidence

Keine. Aufzeichnende Prozesse liefern ausschließlich Unit-Evidence. Kein NGINX-Host, nativer Traffic, Build oder Protected-Gate wurde ausgeführt.

## Bekannte Einschränkungen

Ein breiterer Versuch mit 24 Tests hatte zwei fehlgeschlagene Subtests der Apache-Fixture-Existenzprüfung: OwnPs uninitialisiertes Framework-Submodul enthält beide späten Phase4-Apache-YAML-Fixtures nicht. Das sind unabhängige, fest verdrahtete Dateiexistenzprüfungen, keine Shell-Regressionen. Keine Fixture und kein Test wurde zum Verbergen der Fehler verändert.

## Verbleibende Risiken

Koordinator-Integration und vollständige native beziehungsweise kanonische Runtime bleiben separate Prüfungen. Diese Lieferung belegt nur Shell-Wiring.

## Nicht ausgeführte Prüfungen mit Begründung

Native Runtime/Build, Installation, Remote-CI und Sonar lagen außerhalb dieser begrenzten Aufgabe. Die ShellCheck-Regression überspringt nur bei fehlendem Programm; hier war es installiert und wurde tatsächlich ausgeführt.

## Finaler Diff- und Review-Status

Der gezielte RED reproduzierte alle acht Warnungen, während beide Befehlsgrenz-Charakterisierungen bereits bestanden. Finale fokussierte Suite: 30 Tests PASS in 15,585 Sekunden, keine SKIPs. Syntax und ShellCheck auf Warnungsebene bestehen. Der Diff erhält initiale Cachezuweisung und aktiven Inventarreset, ändert nur freigegebene Dateien und ergänzt weder Unterdrückungen noch native PASS-Behauptungen.
