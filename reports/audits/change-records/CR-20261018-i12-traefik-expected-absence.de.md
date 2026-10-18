# Change Record: CR-20261018-i12-traefik-expected-absence

**Sprache:** [English](CR-20261018-i12-traefik-expected-absence.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-traefik-expected-absence |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `08ed2bd4a37223ba58dc0a46c9aa9787c6f42839` |

## Motivation und Problemstellung

Einige Traefik-Parser- und abnormale Transportfälle besitzen laut Quelle keine native Entscheidung, native Phase oder vollständigen HTTP-Status. Die bisherige Reconciliation wies jedes null zurück. Dadurch ließ sich eine unabhängig geprüfte Abwesenheitserwartung ohne erfundenen Wert nicht ausdrücken.

## Akzeptanzkriterien

Nur separat von Root geprüfte typisierte Abwesenheit für die exakte ursprüngliche Traefik-ID und ihre Vertragshashes zulassen. Literal null, ursprüngliche Erwartungen und physische Belegpflichten erhalten. Ausgelassene Werte, veraltete oder routenfremde Freigaben, unbekannte Abwesenheitstypen, fehlende Primärquellen und manipulierte Quellbytes zurückweisen. Quellauflösung darf niemals eine Hostausführung qualifizieren.

## Implementierungsentscheidung und Begründung

Die optionale expected_absence-Prüfung bindet die kanonischen Hashes der ausgewählten Anforderung und des ursprünglichen Oracles. Ihre Feldmenge muss exakt den literal-null-Erwartungsfeldern entsprechen. Jedes Feld benötigt eine Begründung und unabhängig gebundene offizielle Host- und Protokollquellen; Messwerte allein dürfen die Erwartung nicht definieren. Vollständige bestehende Erwartungen verwenden unverändert den bisherigen Pfad.

## Geänderte Dateien

Das zentrale Oracle-Reconciliation-Skript, tests/test_i12_traefik_absence_oracles.py und dieses EN/DE-Nachweispaar. Keine Änderung an zentraler Matrix, ursprünglichem Inventar, Produkt, Framework oder MRTS.

## Ausgeführte Befehle

Die fünf neuen Abwesenheitskontrollen bestanden mit RTK-umhüllter unittest-Ausführung in der Parent-venv. Sie reproduzierten vor der Änderung die bisherige Zurückweisung; kombinierte bestehende Oracle-/Ledger-Regressionen bestanden danach. Belege liegen im checks-Verzeichnis des Task-Laufs als absence-before/absence-after. Das unabhängige schreibgeschützte Review wiederholte die fünf Kontrollen erfolgreich.

## Security-Auswirkung

Fehlende Belege bleiben fehlend. Freigaben gelten nur für die drei Traefik-Routen und die unveränderliche ursprüngliche Identität. Eine Worker-Behauptung, fremder Beleg oder gemessener Status erlaubt keine neue Erwartung. Keine Änderung an Runtime-Admission oder Sicherheitsgrenzen.

## Runtime-Evidence

Für diese Quellvertragsänderung wurde kein Host gestartet. full_lifecycle_qualified bleibt false; Tests und Quellreviews stufen keine ursprüngliche ID hoch.

## Bekannte Einschränkungen

Hashes authentifizieren die geprüften Quellen, nicht ihre Interpretation. Root muss jede tatsächliche Primärquelle vor einer Freigabe weiterhin prüfen; eine synthetische Testfixture ist kein Produkt-Oracle.

## Verbleibende Risiken

Anwendbare Host-Lifecycle-, Client-, Backend-, Native-Observer- und Cleanup-Belege bleiben nach dem jeweiligen Qualifier-Vertrag separat verpflichtend.

## Nicht ausgeführte Prüfungen mit Begründung

Gehostete CI und Sonar stehen für den integrierten veröffentlichten Head aus. Tatsächliche Traefik-Hostausführungen gehören den Abnahme-Producern und werden hier nicht behauptet.

## Finaler Diff- und Review-Status

Root und unabhängiges schreibgeschütztes Review fanden keinen verbleibenden konkreten Fehler im begrenzten Diff. Gezielte Tests bestanden; integrierte Abschlussprüfungen und Gates des veröffentlichten Heads bleiben erforderlich.
