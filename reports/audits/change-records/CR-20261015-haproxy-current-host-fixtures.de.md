# Change Record: CR-20261015-haproxy-current-host-fixtures

**Sprache:** [English](CR-20261015-haproxy-current-host-fixtures.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-haproxy-current-host-fixtures |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `1b4e1dc041a9080cd84cd8c70ba053cd77c3fa3f` |

## Motivation und Problemstellung

Frische HAProxy-Abnahmefixtures nach Produktintegration vorbereiten und dabei jede ursprüngliche Anforderung und jedes historische Ergebnis erhalten. Die durch die aktuelle Sonar-Analyse erkannten HAProxy-Harnesspfade vereinfachen und härten; lokale Änderungen belegen keinen serverseitigen Befundabschluss.

## Akzeptanzkriterien

Alle 278 ursprünglichen HAProxy-IDs und ausgewählten Verträge an unveränderliche Snapshothashes binden; 80 native und 49 Companion-Fixtures für Captures vorbereiten und ausdrückliche Lücken erhalten. Beobachtungs-/Qualifikationsgrenzen und bestehende Capture-Definitionen bewahren. Gezielte Regressionstests ausführen; keine neuen Host- oder Lifecycle-PASS-Aussagen.

## Implementierungsentscheidung und Begründung

Quellgebundene native und Companion-Fixtureplaner ergänzen; gezielte Hilfsfunktionen aus komplexen Harnesspfaden extrahieren. Zugelassene physische Pfade validieren und Symlink-/Traversaleingaben ablehnen; tatsächliche Relayweiterleitung und terminale Zustände erfassen. Quell-Oracle-Werte, tatsächliche Messungen und Qualifikation getrennt halten. Keine Änderung an Produkt, gemeinsamen Captures, zentraler Matrix, Generatoren, Framework/MRTS oder anderen Connectoren.

Die Fortsetzung am 2026-10-18 gleicht das Fixtureverhalten von nativem v6 und Companion v5 ab: Negative Regeln, beschädigtes Framing, Client-Cancel und MRC-Fehler betreffen ausschließlich die Haupttransaktion; gesunde Nachbarn behalten saubere kleine Responses. Vergleicher verlangen tatsächliches Content-Length-Framing und unabhängige Transportabbruchbeobachtungen; ein Timeout oder unvollständiger Body allein belegt keinen Reset. Die MRC-Wire-Protokollversion `2` wird gegen den maßgeblichen C-Header des Produkts geprüft, und Clienttransport-Aliase bewahren dieselben gemessenen Fakten. Frühere v3-/v4-Versuche, die vor Hostausführung scheiterten, bleiben als `HARNESS_DEFECT` erfasst.

## Geänderte Dateien

`connectors/haproxy/harness/i12_companion_host.py`, `i12_native_cases.py`, `i12_native_observe.py`, `i12_spop_host.py`, `i12_spop_wire.py`; neu `connectors/haproxy/harness/i12_companion_cases.py` und `i12_native_contracts.py`; `tests/test_haproxy_i12_companion_host.py`, `tests/test_haproxy_i12_native_cases.py`, `tests/test_haproxy_i12_spop_wire.py`; dieses EN/DE-Change-Record-Paar. Die getrennten Arbeiten unter `i12_current_capture.py`, `i12_request_scope_observer.c`, `test_haproxy_i12_current_capture.py` und neue Oracle-Artefakte sind von diesem ersten Harness-Commit ausgeschlossen.

## Ausgeführte Befehle

Worker-Evidence meldet 45 bestandene gezielte Unittests unter CPython 3.14.4. Lokale Sonar-Remediation-Regressionsevidence meldet 28 bestandene Tests; dies sind überlappende gezielte Suiten, keine zusätzlichen Hostläufe. Historische Evidence der Hauptaufgabe wiederholte die frühere gezielte Harness-Suite unabhängig unter CPython 3.14.7: 45 Tests und 41 Subtests bestanden, Exit 0. Ältere Receipts mit 45/53 Tests bleiben historische Evidence und validieren nicht die neuesten Änderungen. Exakte argv, cwd und Ausgabehashes liegen im externen Lauf `i12-haproxy-415-acceptance-20261015/commands/current-haproxy-harness-pytest-v1.json` und dessen stdout. Der frische kombinierte CPython-3.14.7-Lauf der Hauptaufgabe am 2026-10-18 besteht 55 Tests und 56 Subtests, Exit 0. Exakte umhüllte argv, cwd, Zeiten und Ausgabehashes liegen in `i12-haproxy-415-acceptance-20261015/commands/current-haproxy-harness-20261018-v1.json`; dessen stdout-SHA-256 ist `4bb12b1d51dfbcfea2713684101f77b80ed6f4ef127fc98ea8d1ffc2a64e2c96`. Dies ist Harness-Regressionsevidence, keine Hostabnahme. Record-Erstellung erfolgte mit `rtk proxy python3 ci/tools/new-change-record.py create --name haproxy-current-host-fixtures --base-revision 1b4e1dc041a9080cd84cd8c70ba053cd77c3fa3f --date 2026-10-15`.

## Security-Auswirkung

Keine Änderung produktiver Sicherheitskontrollen. Physische Pfadannahme, Quellidentitätsbindung, Relayabschaltung und Behandlung beschädigter Frames bleiben auf ihrer geprüften Harnessebene fail-closed. Fixtures erlauben kein Bestehen bei fehlender Sink-, Timeout-, nativer File-API- oder Hostfehler-Evidence.

## Runtime-Evidence

Diese Fixture-/Remediation-Änderung beansprucht keine neue Hostausführung und kein Lifecycle-PASS. Die 80 nativen und 49 Companion-Fixtures sind ausschließlich für Captures vorbereitete Artefakte. Unabhängige integrierte Builds, native Engine-Mappings, physische Sinklogs, Wire-/Client-/Backendmessungen und Hauptqualifikation bleiben erforderlich. Historische Ergebnisse bleiben unverändert.

## Bekannte Einschränkungen

Ursprüngliche Anforderungen ohne ausführbare quellgebundene Verträge bleiben ausdrückliche Lücken. Der vollständige 278-ID-Snapshot ist unveränderlich, einschließlich unaufgelöster ursprünglicher Erwartungen. Capture-Bereitschaft schließt weder Oracle noch Transportprüfung oder Lifecycle ab.

## Verbleibende Risiken

Tatsächliches Hostverhalten nach Produktneubau und alle verbleibenden Evidencelücken erfordern separate Ausführung. Die Sonar-Serveranalyse meldet 41 Basisbefunde; sie wurde für diese lokalen Änderungen nicht wiederholt, daher wird weder ein neues Server-Quality-Gate noch eine Befundauflösung behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Frische private Hostabnahme und finale serverseitige Sonar-Analyse gehören nicht zu dieser lokalen Fixturevalidierung. Das CPython-3.14.7-Ergebnis der Hauptaufgabe ist separate receiptbelegte Evidence, nicht aus Worker-Ergebnissen abgeleitet.

## Finaler Diff- und Review-Status

Dieser Record beschreibt ausschließlich Harness-/Test-/Fixturevorbereitung und lokale Remediation. Es werden weder finale I12-Abnahme noch vollständig grünes Sonar-Ergebnis oder Liefer-/Mergeergebnis behauptet. Englischer und deutscher Record bewahren denselben Umfang, dieselben Anzahlen und Grenzen.
