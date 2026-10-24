# Change Record: CR-20261008-nginx-protocol-fixture-executor-contract

**Sprache:** [English](CR-20261008-nginx-protocol-fixture-executor-contract.md) | Deutsch

Testfixture-Korrektur; keine Protokollimplementierung oder Runtime-Erfolg wird behauptet.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-protocol-fixture-executor-contract |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `708e15aa4623b2b039d333e8f654753a027a554d` |

## Motivation und Problemstellung

Die bisherige Maximal-Capability-Fixture stufte unabhängige zukünftige
Capabilities falsch hoch. Die echte Auswahl lehnte selektierte Cases ohne
Ausführungsdeskriptoren korrekt ab; drei Fehler im Parent-Fokuslauf mit 546 Tests
waren die Folge.

## Akzeptanzkriterien

H1 behält alle 97 selektierten Records und schließt H2/H3-only-Cases aus.
Explizite H2/H3-Eingaben erreichen die echte Auswahl, aber fehlende Required-
Executors blockieren die Initialisierung. Das Hochstufen unabhängiger
Capabilities darf keine Ausführungsdeskriptoren erfinden.

## Implementierungsentscheidung und Begründung

Nur die sechs Protokoll-Capabilities in der positiven Sichtbarkeitsfixture
hochstufen. Eine separate Maximal-Capability-Negativkontrolle bleibt erhalten.
Für H2/H3 die tatsächliche Missing-Executor-Diagnose, ausschließlich einen
Selection-Aufruf und keine initialisierte Evidence verlangen. Produkt-
Capabilities, Auswahl, Validatoren und Dispatch bleiben unverändert.

## Geänderte Dateien

`tests/test_nginx_full_lifecycle_protocol_wiring.py` und dieses EN/DE-Record-Paar.

## Ausgeführte Befehle

Über RTK: `python -m unittest -v tests.test_nginx_full_lifecycle_protocol_wiring`
mit kurzem, Connector-neutralem externem `TMPDIR` und `RUNNER_TEMP`: 10 Tests,
31.976s, Exit 0. Der ursprüngliche vollständige Parent-Fokus bleibt bei 546 Tests,
16 Fehlern und Exit 1; acht Fehler waren Aufrufpfadprobleme, fünf generische
Native-Fixture-Discovery-Fehler benötigen die unabhängige Framework-Korrektur.
`make check-bilingual-docs check-doc-links`, die Change-Record-Archivprüfung und
`git diff --check` bestanden mit Exit 0. Ein früherer Dokumentationsaufruf hängte
das nicht vorhandene `check-doc-commands` an und endete nach erfolgreichen
gültigen Prüfungen mit Exit 2; der Wiederholungslauf nutzte ohne Sourceänderung
ausschließlich die aktuellen nativen Targets.

## Security-Auswirkung

Keine Authority-, Containment-, Freshness-, Protokoll- oder Evidence-Prüfung wird
abgeschwächt. Fehlende Required-Executors lassen die Auswahl weiterhin scheitern.
Diese Tests führen keinen Runtime- oder geschützten Root-Launcher aus.

## Runtime-Evidence

Keine. Dies sind native Make-Aufrufer- und Selection/Init-Tests, keine HTTP-
Requests. Die 45 finalen Runtime-Lücken und das ursprüngliche Canonical
NOT_EXECUTED bleiben unverändert.

## Bekannte Einschränkungen

Diese Änderung implementiert keine H2/H3-Ausführungsdeskriptoren. Sichtbarkeit
ist keine Protokollausführung; die Negativtests dürfen nicht als H2/H3 PASS gelten.

## Verbleibende Risiken

Der vollständige Parent-Fokus muss am finalen Framework-Pin mit geeigneten
temporären Pfaden erneut laufen. Echte NGINX-Requests mit aktuellen Artefakten
und kanonische Validierung bleiben vor jeder E2E-Erfolgsmeldung erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Full-E2E, geschützter Workflow und frische Remote-Analyse liefen für diese
reine Teständerung nicht. Der vollständige Framework-Lint läuft noch; Ruff ist
nicht verfügbar.

## Finaler Diff- und Review-Status

Die unabhängige Read-only-Prüfung fand keine belegte Regression. Der Diff ist
auf die Protokoll-Testfixture und ihr Record-Paar begrenzt; keine Produktquelle,
kein Gitlink, MRTS oder geschützter Workflow wird geändert.
