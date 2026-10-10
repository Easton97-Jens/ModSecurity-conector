# Change Record: CR-20261008-harness-explicit-content-type-omission

**Sprache:** [English](CR-20261008-harness-explicit-content-type-omission.md) | Deutsch

Nur ausdrückliche opt-in-Fixture-Metadaten.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-harness-explicit-content-type-omission |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `5788ba5ced597106911785a5407b2024c68bbaf2` |

## Motivation und Problemstellung

Die ausdrücklich angeforderte Fixture ohne Content-Type durch Harness-Metadaten erhalten, statt ihre Omission-Anweisung still zu verlieren.

## Akzeptanzkriterien

Nur validiertes opt-in omit_headers weitergeben. Default-Fixture-Form erhalten; Framing-Header-Omission und Konflikte mit konfiguriertem Content-Type einschließlich leerer Werte ablehnen.

## Implementierungsentscheidung und Begründung

Vor Übergabe von omit_headers an das Backend den bestehenden geschlossenen response_fixture_omission-Validator nutzen. Omission bleibt [] oder genau ['Content-Type']; keine allgemeine Header-Unterdrückung.

## Geänderte Dateien

ci/runtime/common/harness-case-metadata.py; tests/test_harness_omission_metadata.py; this EN/DE pair.

## Ausgeführte Befehle

RTK-gekapselte Parent-.venv-Unittests tests.test_case_metadata_utils tests.test_harness_omission_metadata tests.test_response_fixture_omission tests.test_response_header_backend tests.test_change_record bestehen 40 Tests (stream-c-parent-metadata.log). Drei fokussierte Omission-Kontrollen bestehen auch zusammen mit drei Raw-Driver-Kontrollen. In-Memory-Syntax beider Python-Dateien, ci/tools/new-change-record.py check, make check-bilingual-docs und make check-doc-links (expliziter aktueller Framework-Checkout) bestehen.

## Security-Auswirkung

Keine Framing- oder Security-Header-Omission wird erlaubt. Ungültige oder widersprüchliche Omission-Metadaten scheitern vor Backend-Verwendung; Default-Verhalten bleibt unverändert.

## Runtime-Evidence

Nur kontrollierte Unit-Fixtures; keine frische NGINX- oder andere native Host-Runtime.

## Bekannte Einschränkungen

Diese Änderung gibt Fixture-Metadaten weiter; sie belegt weder tatsächliche Wire-Omission noch Engine-MIME-Entscheidungen.

## Verbleibende Risiken

Frische hostgebundene Response-Header- und Canonical-Beobachtungen bleiben Koordinator-Verantwortung.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Build, native Runtime, E2E, Remote-CI, Sonar oder Push im Rahmen dieser Aufgabe.

## Finaler Diff- und Review-Status

Engen opt-in-Seam und Positiv-/Default-/Negativkontrollen geprüft. Separater Vier-Dateien-Commit einschließlich beider generierter Records; parallele Root-Arbeit erhalten.
