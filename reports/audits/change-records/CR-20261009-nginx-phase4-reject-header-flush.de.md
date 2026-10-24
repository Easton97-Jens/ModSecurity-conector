# Change Record: CR-20261009-nginx-phase4-reject-header-flush

**Sprache:** [English](CR-20261009-nginx-phase4-reject-header-flush.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-phase4-reject-header-flush |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `75686a47ba971d33c46f4f40a844bbe53d7465f1` |
| Integrations-Parent-Revision | `af82baac81a5a51ed062507688494e72d6480eeb` |
| Framework-Revision | `4c6c21e8622840b4c218d8ea5520dd0b10b3fac9` |
| MRTS-Revision | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |

## Motivation und Problemstellung

Die echte R11-Invocation `phase4_body_reject` protokollierte intern `header_sent=true` und den bereits festgelegten Status 200, aber curl erhielt eine leere Antwort (Exit 52, HTTP 0). NGINX 1.31.6 verwendet standardmäßig `postpone_output 1460`; die kurzen Header waren noch zurückgehalten, als der unmittelbare Body Reject die Verbindung abbrach. Die interne Festlegung allein beweist keine Übertragung an den Client.

## Akzeptanzkriterien

Nur die exakte Invocation `phase4_body_reject` muss `postpone_output 0;` verwenden; die sieben anderen geschlossenen Phase-4-Fälle behalten ihre Konfiguration. Eingaben, Case-Identität, URI, Run-ID, Modus, Regeln, Required-Auswahl und Validatoren bleiben unverändert. Eine anschließende echte Root-Master/nobody-Worker-Probe muss HTTP-200-Header, curl-Exit 18 und null Body-Bytes behalten, bevor Runtime-Abschluss behauptet werden kann.

## Implementierungsentscheidung und Begründung

Der Parent-Driver ergänzt die nur als Keyword zulässige Option `flush_response_headers=False` und wählt sie über ein Konfigurationsfactory-Partial ausschließlich für `phase4_body_reject`. Die Direktive gilt in der exakten Location dieser Invocation. Dies ändert das Ausgabescheduling des Testhosts ohne Änderung der Produktquellen oder Binärsemantik. Regressionstests vergleichen die vollständige Konfiguration nach Entfernung der einen autorisierten Direktive und decken alle acht geschlossenen Fälle ab.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-nginx-phase4-cases.py`
- `tests/test_nginx_phase4_driver.py`
- `reports/audits/change-records/CR-20261009-nginx-phase4-reject-header-flush.md`
- `reports/audits/change-records/CR-20261009-nginx-phase4-reject-header-flush.de.md`

## Ausgeführte Befehle

Befehle liefen im Parent-Worktree über RTK. `${PARENT_PYTHON}` bezeichnet den gewählten Parent-Virtualenv-Interpreter; `${FRAMEWORK_ROOT}` bezeichnet den expliziten Framework-Worktree. Beide sind auf die entsprechenden lokalen Checkouts zu setzen. Diese portablen Befehle erhalten die ausgeführten Inhalte:

```sh
rtk proxy env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 "${PARENT_PYTHON}" -m unittest discover -s tests -p test_nginx_phase4_driver.py -v
rtk proxy env PYTHONNOUSERSITE=1 "${PARENT_PYTHON}" -m unittest discover -s tests -p 'test_nginx_phase4_*.py' -v
rtk proxy env PYTHONNOUSERSITE=1 "${PARENT_PYTHON}" -m unittest discover -s tests -p 'test_nginx_*driver.py' -v
rtk proxy env PYTHONNOUSERSITE=1 FRAMEWORK_ROOT="${FRAMEWORK_ROOT}" "${PARENT_PYTHON}" -m unittest tests.test_nginx_common_input_fault_driver.InputFaultDriverTest.test_source_bound_protocol_selection_retains_cleanup_and_raw tests.test_nginx_driver_contract_tables -v
rtk proxy env PYTHONNOUSERSITE=1 "${PARENT_PYTHON}" -c 'from pathlib import Path; [compile(Path(name).read_bytes(), name, "exec") for name in ("ci/runtime/lifecycle/run-nginx-phase4-cases.py", "tests/test_nginx_phase4_driver.py")]'
rtk git diff --check
```

Fokussiertes RED: 11 Tests, ein FAIL und ein ERROR, Exit 1. Fokussiertes GREEN: 11 Tests, Exit 0. Phase-4-Nachbarn: 46 Tests, Exit 0, keine Skips. Driver-Nachbarn: 138 Tests, Exit 0, ein Prerequisite-Skip wegen fehlendem explizitem Framework-Root. Die ausgelassene Kontrolle und die Vertragstabellen-Suite liefen anschließend mit explizitem `FRAMEWORK_ROOT`: acht Tests, Exit 0, keine Skips. Syntax- und Diff-Prüfungen: Exit 0. Auch der native Change-Record-Scaffold-Befehl endete mit Exit 0. Dies sind Unit-/Konfigurationsprüfungen, keine echte HTTP-Evidence.

Auch die Dokumentationsvalidierung bestand: `rtk proxy "${PARENT_PYTHON}" ci/tools/new-change-record.py check`, `rtk make check-bilingual-docs PYTHON="${PARENT_PYTHON}"` und `rtk make check-doc-links PYTHON="${PARENT_PYTHON}" FRAMEWORK_ROOT="${FRAMEWORK_ROOT}"`, alle Exit 0. Die Archivprüfung beweist ausschließlich die Struktur. Manuelles Review bestätigte faktische EN/DE-Parität; RTK-Version/Gain-Verifikation und `rtk git diff --check` endeten mit Exit 0.

## Security-Auswirkung

Keine Änderung an Autorisierung, Pfadautorität, Projection-Freshness, Root/nobody-Isolation, Framing-Validierung oder Required-Evidence-Kontrollen. Keine Framework- oder MRTS-Änderung gehört zu diesem Parent-Fix. Dieser Record speichert keine Secrets oder privaten Payloads.

## Runtime-Evidence

R11 bleibt FAIL; seine originale Beobachtung curl-Exit 52/HTTP 0 bleibt erhalten. Für diesen Record wurde noch kein korrigierter echter Request ausgeführt. Die erforderliche begrenzte Root-Master/nobody-Worker-Probe muss echte Raw-Header, HTTP 200, curl-Exit 18, null Body-Bytes und Cleanup erfassen. Unit-GREEN beweist kein Canonical PASS.

## Bekannte Einschränkungen

`header_sent` beschreibt die interne Festlegung in NGINX statt die Übertragung auf dem Wire. Die Direktive ist auf den unmittelbaren Body-Reject-Fall begrenzt. Andere unabhängige R11-Framework-Defekte und der vollständige Required-Lifecycle liegen außerhalb dieser isolierten Scheduling-Änderung.

## Verbleibende Risiken

Die echte Probe und ein frischer integrierter Required-Lauf müssen das clientseitig sichtbare Verhalten mit den tatsächlichen NGINX-1.31.6-Artefakten bestätigen. Bestehende fehlgeschlagene Evidence darf nicht als korrigierte Evidence umetikettiert werden.

## Nicht ausgeführte Prüfungen mit Begründung

Die korrigierte echte Probe, ein frischer Full97-Lauf, Canonical-Finalisierung, geschützter Workflow und CI-/Sonar-Delivery-Prüfungen des aktuellen Heads wurden für diese Änderung nicht ausgeführt. Sie erfordern Root-Integration nach den unabhängigen Fixes und der Source-Bindung. Die Dokumentationstask hat keinen Commit oder Push ausgeführt.

## Finaler Diff- und Review-Status

Der Source-Diff ist auf den Parent-Phase-4-Driver und seine Regressionen begrenzt, ergänzt durch dieses EN/DE-Paar. Produktbinärdateien, Framework-Validatoren und Required-Auswahl bleiben durch diesen Fix unverändert. Integrationsreview und Runtime-Abnahme stehen aus; PR #396 bleibt Draft.
