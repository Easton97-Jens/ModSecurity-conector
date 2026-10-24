# Change Record: CR-20261008-native-first-byte-shell-environment

**Sprache:** [English](CR-20261008-native-first-byte-shell-environment.md) | Deutsch

Begrenzter First-Byte-Shell-Follow-up; keine native Runtime-Aussage.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-native-first-byte-shell-environment |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `8c19e31a21f0388b7b1417f0d25bb6530f496fae` |

## Motivation und Problemstellung

Nach der Baseline-Korrektur meldete die gemeinsame Lifecycle-ShellCheck-Prüfung noch sieben SC1007/SC2097/SC2098-Warnungen im First-Byte-Helper. Leerer CDPATH und caller-expandierte Kindprozess-Zuweisungen waren implizit.

## Akzeptanzkriterien

Warnungen ohne Unterdrückung beheben; echte Helper-/Harnesspfade, Aufruferumgebung, quotierte Argumente, Fehlerexit, Safe-Modus, frische Projektion und Evidence-Ablehnung bewahren. Bestehende Baseline- und Routingtests erhalten.

## Implementierungsentscheidung und Begründung

Den leeren CDPATH explizit als CDPATH='' schreiben. Nur ein explizites env vor der äußeren Zuweisungsliste ergänzen; rechte Seiten und Wrapper-/Harnesspfade expandieren weiterhin in der aufrufenden Shell. Keine Defaults, Guards, Evidence-Anforderungen oder native Auswahl ändern.

## Geänderte Dateien

ci/runtime/lifecycle/run-native-first-byte.sh (Zweizeilenkorrektur); neue tests/test_native_first_byte_shell_environment.py; dieses generierte EN/DE-Paar. Keine Änderungen an Baseline, Framework, MRTS, Katalog oder Schema.

## Ausgeführte Befehle

RTK-gewrapptes Parent-Python unittest -v prüfte tests.test_native_first_byte_shell_environment, tests.test_no_crs_baseline_shell_environment, tests.test_no_crs_native_authority_wiring und tests.test_nginx_selected_configtest_wiring. RTK shellcheck -S warning prüfte run-no-crs-baseline.sh, run-connector-stage.sh und run-native-first-byte.sh gemeinsam; RTK sh -n prüfte jede Datei einzeln. Generatorarchiv- und Git-Whitespace-Prüfungen folgten. Neutraler externer TMPDIR: /var/tmp/codex/ModSecurity-conector/runs/dv-Hm965b; Bytecode/User-Site deaktiviert.

## Security-Auswirkung

Keine Unterdrückung oder Gate-Abschwächung. Recording-Doubles belegen konkrete quotierte Wrapperargumente und Umgebungen für Apache/NGINX, Exit 23, Safe-Modus und einen frischen, nicht vorab angelegten NGINX-Projektionsnamen. Negative Kontrollen bewahren BLOCKED bei fehlendem Helper, unbekanntem Connector, Validatorfehler und fehlendem Log/Barrier.

## Runtime-Evidence

Keine. Unit-Doubles starten keine nativen Hosts. Der Recording-Validator belegt keine echte Pfadautorität; separate vorhandene Pfadsicherheitstests bleiben erforderlich. Dummy-Logbytes sind ausdrücklich keine nativen Events und erzeugen keinen Result-Receipt.

## Bekannte Einschränkungen

Diese Prüfungen belegen nur Shell-Orchestrierung und statische/Syntax-Gültigkeit, nicht natives Streaming, Engine-Verhalten oder Protected-/kanonische Evidence.

## Verbleibende Risiken

Der Koordinator muss integrieren und echte finale Runtime-Prüfungen gegen das saubere gepinnte Source-/Build-/Authority-Tupel durchführen.

## Nicht ausgeführte Prüfungen mit Begründung

Build, native Runtime, Installation, Remote-CI und Sonar lagen außerhalb des Auftrags. ShellCheck war installiert und wurde ausgeführt; keine SKIPs.

## Finaler Diff- und Review-Status

RED reproduzierte alle sieben Warnungen, während vier Verhaltenskontrollen schon vor der Änderung bestanden. Finale Suite: 37 PASS in 21,182 Sekunden, keine SKIPs. Gemeinsames ShellCheck auf Warnungsebene und alle drei Syntaxprüfungen Exit 0. Diff nur mit freigegebenem Skript, neuem Test und Recordpaar; kein Dependency-Replay und keine Statuspromotion.
