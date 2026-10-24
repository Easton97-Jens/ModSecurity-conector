# Change Record: CR-20261009-nginx-upstream-header-reader

**Sprache:** [English](CR-20261009-nginx-upstream-header-reader.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-upstream-header-reader |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `c57e6b0a930161e83cb59bf5905a6db00311dc91` |

## Motivation und Problemstellung

Das aktuelle Sonar-Finding `AaEhok3w0iUkTaK5Ajv2` meldet für `_Handler.handle` eine kognitive Komplexität von 19 bei unverändertem Grenzwert 15. Die Parent-Fixture benötigt eine verhaltenserhaltende Extraktion, keine Abschwächung des Gates.

## Akzeptanzkriterien

Die kognitive Komplexität pro Funktion reduzieren, ohne Veröffentlichungsreihenfolge, initiale Write-/Flush-Fehler, Suffix-Fehler, Timeout oder Verhalten bei fehlerhaften/abgeschnittenen Requests zu ändern. Required-Scope, Framework und MRTS erhalten.

## Implementierungsentscheidung und Begründung

Nur die vorhandene, pro Zeile begrenzte Request-Head-Schleife nach `read_request_head()` extrahieren. Ein fehlender oder abgewiesener Head liefert `None`; die Antwortmethode kehrt vor Parsing oder Schreiben zurück. Das 4096-Byte-Zeilenlimit, EOF-Verhalten und Request-Parsing bleiben unverändert. Die Veröffentlichung bleibt vor dem ungepufferten Write; initiale Fehler löschen sie weiterhin. Kein neues Gesamtheaderlimit und keine Parsing-Policy werden eingeführt.

## Geänderte Dateien

- `ci/runtime/lifecycle/nginx_sequence_upstream.py`
- `tests/test_nginx_sequence_upstream_barrier.py`
- `reports/audits/change-records/CR-20261009-nginx-upstream-header-reader.md`
- `reports/audits/change-records/CR-20261009-nginx-upstream-header-reader.de.md`

## Ausgeführte Befehle

```sh
rtk run -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_sequence_upstream_barrier
rtk run -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest discover -s tests -p 'test_nginx_sequence_*py' -v
rtk run -- /usr/local/bin/sonar-with-env api get '/api/rules/show?key=python:S3776'
```

Die neuen Kontrollen an der echten Handler-Methode bestanden vor der Extraktion: 12/12 Tests, Exit 0. Dieser verhaltenserhaltende Refactor hat deshalb Baseline GREEN, kein behauptetes RED. Nach der Extraktion bestand die benachbarte Sequence-Suite mit 53/53, Exit 0. Die Sonar-Regelabfrage über den kanonischen Wrapper lieferte API 400, Exit 1; die Regelbewertung nutzt den bekannten Cognitive-Complexity-Vertrag, keine behauptete erfolgreiche Serverabfrage.

Weitere Befehle liefen über RTK: `ci/tools/new-change-record.py check`, Python-Kompilation im Speicher und `git diff --check` bestanden mit Exit 0. `make check-bilingual-docs` und `make check-doc-links` mit dem Parent-Interpreter lieferten Exit 2, weil dieser isolierte Worktree ein nicht initialisiertes Framework-Submodul hat und vorhandene Repository-Links nicht aufgelöst werden können; keine Links wurden abgeschwächt. Die Dokumentationsprüfung im Integrationsworktree bleibt erforderlich. RTK-Version, Gain und Prüfung des ausführbaren Pfads bestanden. Das vollständige Sequence-Log liegt unter `/var/tmp/codex/ModSecurity-conector/analysis/nginx-r12-race-followup-20261009T172437Z/complexity-tests/sequence-tests.log`.

## Security-Auswirkung

Keine Guardrail, Validierung, Autorisierung, Timeout-, Fehlerklassifikation oder Evidence-Erwartung wird abgeschwächt. EOF und übergroße Request-Zeilen können die Veröffentlichung nicht aktivieren. Ein vollständig eingelesener fehlerhafter Request behält den vorhandenen `IndexError` vor Ausgabe; diese Änderung ergänzt keine Parserfähigkeit.

## Runtime-Evidence

Dieser isolierte Refactor führt keinen NGINX-Runtime-Lauf aus. Unit-Ergebnisse sind keine Runtime- oder Canonical-Evidence und ändern den ursprünglichen R12-Status nicht.

## Bekannte Einschränkungen

Der Request-Reader behält seine vorhandene Zeilengrenze und ergänzt weder eine Gesamtbytezählung noch eine Socket-Deadline. Die Ausnahme bei vollständig eingelesenem fehlerhaftem Request bleibt unverändert.

## Verbleibende Risiken

Eine frische serverseitige Sonar-Analyse muss die Metrik am integrierten Commit bestätigen. Jede Runtime-Aussage erfordert echte, separat aufbewahrte Root/nobody-Beobachtungen.

## Nicht ausgeführte Prüfungen mit Begründung

In diesem Writer-Worktree erfolgen kein Full97, geschützter Workflow, nativer Build oder frischer serverseitiger Sonar-Scan. Der Koordinator bleibt für integrierte Validierung und Veröffentlichung verantwortlich.

## Finaler Diff- und Review-Status

Der Diff ist auf die Parent-Request-Head-Extraktion, zwei Regressionstests an der echten Handler-Methode und diesen zweisprachigen Change Record begrenzt. Dieser Worker führt keinen Git-Commit, Push oder Schreibzugriff auf den Integrationsworktree aus.
