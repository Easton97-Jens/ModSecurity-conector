# Change Record: CR-20261022-pr410-ci-fixture-drift

**Sprache:** [English](CR-20261022-pr410-ci-fixture-drift.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261022-pr410-ci-fixture-drift |
| Datum (UTC) | 2026-10-22 |
| Basis-Revision | `afaf6305bd55646073c3b40632b52fc4e5edf714` |

## Motivation und Problemstellung

Der aktuelle #410-Head scheiterte in `scaffold-lint`, weil sein extrahiertes
Native-Callback-Fixture `request_partial_observed` nicht abbildete. Beide
HAProxy-Structure-Jobs scheiterten außerdem, weil die Fake-libModSecurity-API
der I10-Caller-Tests `msc_get_request_body_length` nicht deklarierte oder
implementierte, nachdem die Common-Runtime die aufbewahrte Request-Bodylänge
ausliest. Dies waren Test-Fixture-Abweichungen auf Basis-Revision
`afaf6305bd55646073c3b40632b52fc4e5edf714`, keine Produkt-Runtimefehler.

## Akzeptanzkriterien

- Das Native-Result-Fixture kompiliert den aktuellen Callback und belegt, dass
  ein partieller Request-Append über spätere erfolgreiche und leere Appends
  erhalten bleibt.
- Die HAProxy-I10-Fake-API modelliert transaktionslokal aufbewahrte Request-
  Bodylänge, begrenzte partielle Aufbewahrung, Append-Fehler und Reset bei einer
  neuen Transaktion.
- Fokussierte Tests und die vollständige Mutationsmatrix
  `check-i10-haproxy-callers` bestehen ohne Produktänderung oder Abschwächung
  einer Prüfung.

## Implementierungsentscheidung und Begründung

Das Callback-Preamble enthält nun denselben Partial-Marker wie die
Produkttransaktion. Assertions prüfen Anfangs-, Partial-, Sticky- und Leer-
Append-Zustand. Die Fake-libModSecurity-Transaktion speichert aufbewahrte Bytes
und stellt sie über die aktuelle C-API bereit. Jedes Direct-/SPOP-Caller-Fixture
führt vor seinen bestehenden Caller-/Mutationsassertions einen Selbsttest aus.
Damit wird die API-Bedeutung geprüft statt nur eine kompilierende Konstante
einzufügen.

## Geänderte Dateien

- `tests/test_native_result_event_protocol.py`
- `tests/test_haproxy_i10_binding_callers.py`
- `reports/audits/change-records/CR-20261022-pr410-ci-fixture-drift.md`
- `reports/audits/change-records/CR-20261022-pr410-ci-fixture-drift.de.md`

## Ausgeführte Befehle

- `rtk /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -B -m unittest -v tests.test_native_result_event_protocol tests.test_haproxy_i10_binding_callers` — Exit `0`; 26 Tests bestanden in 187,792 Sekunden.
- `rtk make PYTHON=/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python check-i10-haproxy-callers` — Exit `0`; 20 Tests bestanden in 251,011 Sekunden.
- `rtk git diff --check` — Exit `0`.
- `rtk make check-bilingual-docs` — Exit `2`; im isolierten Git-Worktree ist
  das Framework-Submodul nicht befüllt, daher meldete der repository-weite
  Checker nur bereits vorhandene fehlende Ziele unter
  `modules/ModSecurity-test-Framework/...`.
- `rtk make check-doc-links` — Exit `2` wegen desselben fehlenden Framework-
  Submoduls; kein Fehler verwies auf einen der neuen Change Records.
- `rtk --version`, `rtk which rtk` und `rtk gain` — RTK `1.0.1` unter `/root/.local/bin/rtk`; alle Befehle und Validierungen nutzten den vorgeschriebenen Proxy.

## Security-Auswirkung

Keine Produktions-Trust-Boundary ändert sich. Die Tests stärken das
fail-closed Body-Accounting, indem sie konstante Retained-Length-Werte,
aufbewahrte Bytes nach fehlgeschlagenem Append, Verlust eines Partial-Limits
und fehlenden Reset einer neuen Transaktion verwerfen. Keine Validierungs-,
Isolations-, Logging- oder Quality-Gate-Kontrolle wird abgeschaltet.

## Runtime-Evidence

Kein neuer Host-Runtimeclaim. Diese Prüfungen kompilieren und führen
extrahierte aktuelle C-Callbacks sowie HAProxy-Direct-/SPOP-Caller-Fixtures mit
einer semantisch korrekten Fake-Native-API aus. Bestehende Hostevidenz bleibt an
ihre aufgezeichneten Ausführungsrevisionen gebunden.

## Bekannte Einschränkungen

Die Änderung repariert nur die beiden bestätigten CI-Fixture-Abweichungen. Sie
ändert kein Common- oder Connector-Produktverhalten und kann für sich keinen
gehosteten Runtime-Lifecycle qualifizieren.

## Verbleibende Risiken

GitHub- und Sonar-Ergebnisse für den aktuellen Head müssen nach normaler
Lieferung auf den #410-Branch gelesen werden. Unabhängige #410-Quality-Gate-
Befunde bleiben von diesen beiden Kompilierungsfehlern getrennt.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Connectormatrix und kein privater Hostlauf wurden wiederholt,
weil die Änderung auf Kompilierungs-/Ausführungsfixtures begrenzt ist und keinen
ausgelieferten Runtimesource ändert. Repository-weite Tests wurden nicht als
Ersatz für die beiden fokussierten Suites und das vollständige betroffene
I10-Caller-Target verwendet. Die repository-weiten Zweisprachigkeits- und
Linkprüfungen konnten in diesem isolierten Worktree nicht vollständig laufen,
weil sein Framework-Submodul nicht befüllt ist; ihre Diagnosen nannten weder
einen geänderten Test noch einen der Change Records.

## Finaler Diff- und Review-Status

Der begrenzte Diff enthält zwei Testdateien und diesen zweisprachigen Change
Record. Beide fokussierten Validierungen und `git diff --check` bestehen. Das
Review fand keine Produkt-, Generator-, Matrix-, Connectorimplementierungs-
oder fremde Dateiänderung. Normaler Commit/Push und CI-Readback auf dem exakten
Head stehen aus; kein Merge und keine Masteränderung werden behauptet.
