# Change Record: Integrität des CI-Statuskanals

**Sprache:** [English](CR-20260718-status-channel-integrity.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-status-channel-integrity` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Finding | `FND-PARENT-0025` |
| Grenze | Nur Parent-CI-Statusrunner, Apache-Lint-Wiring, Tests und Dokumentation; Framework und MRTS bleiben unverändert. |

## Motivation und Problemstellung

`ci/tools/run-check-status.py` hat zuvor eine `CHECK_STATUS_REASON`-Zeile aus
kombiniertem Child-`stdout` und Child-`stderr` geparst. Ein Child mit Exit `77`
konnte daher den erlaubten Apache-Prerequisite-String ausgeben und aus einem
erlaubten Lint-Ergebnis Erfolg machen. Der Ausgabestream fungierte damit als
nicht authentifizierter Statuskanal.

## Akzeptanzkriterien

- Ein vom Child erzeugter erlaubter Marker in `stdout` oder `stderr` kann kein
  Blocked-Ergebnis autorisieren.
- Die fehlende Apache-Entwicklungs-Prerequisite bleibt nur dann eine erlaubte,
  strukturierte Lint-Disposition, wenn der Parent-Runner sie vor dem Start des
  Childs erkennt.
- Ein Kontrollpfad mit nutzbarem APXS/Header startet das Child weiterhin und
  bewahrt Erfolgs- oder Fehlersemantik.
- Direkte, nicht klassifizierte Exit-`77`-Ergebnisse bleiben nichtnull.
- Parent-Regressionstests und zweisprachige Dokumentation beschreiben die
  resultierende Kontrollgrenze wahrheitsgemäß.

## Implementierungsentscheidung und Begründung

Der Runner parst keinen Child-Text mehr als Grund. Er persistiert einen
Version-2-Datensatz mit `status_source`; nur sein
`--blocked-if-missing-apache-development`-Preflight kann die erlaubte
`apache_development_prerequisite`-Disposition ausgeben. Dieser Preflight löst
`APXS_BIN`, `APXS`, `CI_APXS_BIN_CANDIDATES` oder `apxs`/`apxs2` auf und
verlangt dann ein ausführbares APXS, dessen Ergebnis von `-q INCLUDEDIR`
absolut ist und `httpd.h` enthält. Bei Erfolg läuft das Child normal; jeder
spätere Child-Exit `77` bleibt nicht klassifiziert und nichtnull. Das
Apache-Child-Skript gibt keinen Status-Steuerungsmarker mehr aus.

Der SonarQube-Cloud-Follow-up lässt diese Entscheidungsgrenze unverändert. Er
weist die aufgelösten APXS-Kandidaten genau einem explizit typisierten
`tuple[str, ...]`-Wert zu und gibt ihn einmal zurück. Damit bleiben bestehende
Priorität und das Verhalten bei fehlerhafter Konfiguration erhalten, ohne
einen zweiten Statuskanal hinzuzufügen.

## Security-Auswirkung

Die kontrollierten Eingaben sind direktes Child-`stdout`, Child-`stderr` und
der Exit-Status. Das Schutzobjekt ist die CI-Entscheidung, einen optionalen
Apache-Prerequisite-Block zu erlauben. Der Parent-Runner besitzt diese
Autorisierung jetzt über einen separaten persistierten Datensatz und einen
Parent-Preflight. Child-Ausgabe bleibt nur diagnostisch. Dieser Patch ändert
weder Runtime-Host-Evidence noch Report-Governance, Framework-Verhalten, MRTS
oder einen Connector-Runtime-Claim.

## Geänderte Dateien

- `ci/tools/run-check-status.py`
- `Makefile`
- `ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh`
- `tests/test_optional_prerequisite_status.py`
- `ci/README.md` und `ci/README.de.md`
- dieses englische/deutsche Change-Record-Paar und seine README-Indexlinks

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 CODEX_TEMP_ROOT=<task-owned-build-root> /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_optional_prerequisite_status` vor dem Source-Fix | erwartungsgemäß fehlgeschlagen: Die neue Suite der Nachbedingung meldete fünf Failures und sechs Errors, einschließlich beider vom alten Runner fälschlich erlaubten gefälschten Marker-Fälle. |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 CODEX_TEMP_ROOT=<task-owned-build-root> make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-optional-prerequisite-status` nach dem Source-Fix | bestanden: 18 fokussierte Tests, einschließlich gefälschter `stdout`-/`stderr`-Marker, eines nicht erlaubten Markers, eines echten Missing-APXS/Header-Preflights, eines nutzbaren-APXS-Kontrollfalls, rekursivem Make und des tatsächlichen Apache-Lint-Targets. |
| Retained original stderr and stdout spoof probes durch den gepatchten Runner | bestanden: Jede Probe lieferte `77` mit `allowed_by_contract: false`, `reason: "unclassified direct blocked exit code 77"` und `status_source: "child_exit_code"`. |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -c '<compile selected files>'` | bestanden: `ci/tools/run-check-status.py` und `tests/test_optional_prerequisite_status.py` wurden ohne Checkout-Bytecode-Ausgabe im Speicher kompiliert. |
| `rtk shellcheck -x ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh` | fehlgeschlagen an bestehenden Diagnosen in den Zeilen 4 und 86–87 (`SC1007` und `SC2086`); diese Änderung entfernt nur den Statusmarker in Zeile 31 und ändert diese nicht zugehörigen Command-Construction-Zeilen nicht. |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs` | fehlgeschlagen, weil dieser Sparse-Worktree verlinkte Framework-Dokumentation nicht materialisiert; nach Korrektur der Change-Record-Überschriften meldete die Prüfung keinen Fehler für dieses Change-Record-Paar oder seine README-Links. |
| `rtk git diff --check` | bestanden. |
| `rtk env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 CODEX_TEMP_ROOT=/var/tmp/codex/ModSecurity-conector /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_optional_prerequisite_status` | bestanden: 20 fokussierte Tests. Der SonarQube-Cloud-`python:S8495`-Follow-up bewahrt die Priorität `APXS_BIN` → `APXS` → `CI_APXS_BIN_CANDIDATES` → Fallback, besitzt genau einen Kandidaten-Rückgabepfad und prüft ein absolutes konfiguriertes APXS bei leerem `PATH`. |

## Runtime-Evidence

Nicht anwendbar. Dies ist eine Korrektur des CI-Statuskanals. Sie startet
weder einen Connector-Host noch etabliert sie HTTP-, CRS-, MRTS- oder
Lifecycle-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

`rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile ci/tools/run-check-status.py tests/test_optional_prerequisite_status.py` war blockiert, weil `py_compile` trotz `PYTHONDONTWRITEBYTECODE=1` versucht, Checkout-lokale `__pycache__` zu erzeugen, und dieser Worktree diese Schreiboperation korrekt zurückweist. Die fokussierten Import- und Ausführungstests oben bestanden ohne Bytecode-Ausgabe.

Vollständiges Linting, Connector-Builds, Runtime-Harnesses und Generator-/Report-
Tests wurden in diesem isolierten Remediation-Worktree nicht ausgeführt. Dem
ursprünglichen Draft-PR-#56-Head `63f4c9694f3f1c1372ce6db86ea1f88a38f01a92`
folgte der exakte Head `6195e177fa159654e6c30ef732cc7211b1a1385b`, der 33
bestandene GitHub-Checks mit bestandenem CodeQL und SonarQube-Cloud-Quality-Gate
erhielt. Der SonarQube-Cloud-Follow-up für `python:S8495` bewahrte die
APXS-Priorität und den kanonischen Rückgabepfad; das aktuelle PR-Quality-Gate
meldet null neue Issues, null akzeptierte Issues und null Security Hotspots.

Nach dem normalen Merge von Parent-Master
`63819e416984294792bbbe68aa5d84503791baab` erzeugte der
Synchronisations-Commit `35d21bffcde4cf97ab2970b36d42dff2f7d4a128` einen neuen
Delivery-Stand. Seine lokalen fokussierten Status- und
Workflow-Permission-Controls bestehen, aber seine künftige Exact-Head-CI-,
CodeQL-, SonarQube-Cloud- und Review-Evidence muss vor einer `verified_pr`-
Behauptung über das PR-Delivery-Gate beobachtet werden. Dieser Record behauptet
keinen Live-PR-Status und autorisiert keinen Merge ohne diese Evidence.

## Bekannte Einschränkungen

Der Apache-Preflight deckt absichtlich nur diese Lint-Erlaubnis ab. Andere
Status-Wrapper-Aufrufer sind separate Root Causes und werden hier nicht
geändert.

## Verbleibende Risiken

Der Preflight vertraut den konfigurierten APXS-Kandidaten des Jobs,
vertraut jedoch nie einem Child-Ergebnis zur Autorisierung eines Blocks. Ein
nutzbares APXS kann weiterhin zu einem späteren echten Child-Fehler oder einem
nicht klassifizierten `77` führen, das rot bleibt.

## Finaler Diff- und Review-Status

Fokussierte Regression-Coverage, In-Memory-Syntaxvalidierung und `git diff
--check` bestanden. Verpflichtende Change-Record-Überschriften,
wechselseitige Sprachlinks und beide README-Indexlinks wurden manuell
validiert. Das zweisprachige Target schlägt weiterhin nur fehl, weil diesem
Sparse-Worktree verlinkte Framework-Dokumentation fehlt; es meldet keinen
Fehler für dieses Change-Record-Paar. Der historische exakte Head
`6195e177fa159654e6c30ef732cc7211b1a1385b` ist validiert; der aktuelle
Post-Master-Sync-Delivery-Head benötigt eigene Evidence und wird hier bewusst
nicht behauptet. Es wurde kein Runtime-Evidence-Claim erzeugt.
