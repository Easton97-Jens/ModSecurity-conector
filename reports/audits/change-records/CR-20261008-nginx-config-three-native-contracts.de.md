# Change Record: CR-20261008-nginx-config-three-native-contracts

**Sprache:** [English](CR-20261008-nginx-config-three-native-contracts.md) | Deutsch

Fokussierte Parent-Konfigurationsorchestrierung.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-config-three-native-contracts |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `45754c0a0f0ae3dbd04f63a028d342bdac61220a` |

## Motivation und Problemstellung

Drei geschlossene native Konfigurationsablehnungen registrieren: invalid_status und die beiden entfernten modsecurity_phase4_content_types_file-Fälle. Ablehnung der entfernten API darf nicht als Engine-MIME-Parsing gelten.

## Akzeptanzkriterien

Exakte Ablehnungsfragmente, Exitcode, erhaltene Konfigurationszeile und byteidentische kontrollierte reguläre Fixtures verlangen; fremde Konfigurationspfade oder veränderte Fixture-Bytes ablehnen. Bestehende Configtest-Operationen erhalten.

## Implementierungsentscheidung und Begründung

Inline modsecurity_rules durch JSON-Escaping quotieren. Begrenzte reguläre MIME-Fixtures mit 0600 und einem Hardlink samt SHA256 nur für die zwei ausdrücklichen Removed-API-Fälle erhalten. Collector übernimmt geschlossene Fixture-Felder und verlangt erhaltene Fixture-Artefakte.

## Geänderte Dateien

ci/runtime/lifecycle/run-nginx-configtest.py; ci/runtime/lifecycle/collect-no-crs-source.py; tests/test_nginx_migration_driver.py; tests/test_nginx_migration_collection.py; this EN/DE record pair.

## Ausgeführte Befehle

RTK-gekapselte Parent-.venv-Unittests von tests.test_nginx_configtest_driver, tests.test_nginx_migration_driver, tests.test_nginx_configtest_collection und tests.test_nginx_migration_collection bestehen 83 Tests; externes Log stream-c-parent-config.log enthält das Ergebnis. In-Memory-Compile besteht alle vier geänderten Python-Dateien. ci/tools/new-change-record.py check, make check-bilingual-docs und make check-doc-links (expliziter aktueller Framework-Checkout) bestehen; Diff-Whitespace ist sauber.

## Security-Auswirkung

Kontrollen binden Parserdiagnosen an exakte erhaltene Eingaben; Fixture-Identität, Typ, Eigentümer, Rechte, Grenzen und Inhalt werden geprüft. Keine Validierung oder Quellautorität wird abgeschwächt.

## Runtime-Evidence

Für diese Lieferung wurde keine frische native Runtime ausgeführt. Kontrollierte Fake-Host-Unittests beweisen nur Orchestrierung und Ablehnungsklassifikation.

## Bekannte Einschränkungen

NGINX lehnt die entfernte Direktive ab, bevor es ihre Argumentdatei liest. Diese Fälle belegen weder Wildcard-MIME- noch Engine-Content-Type-Verhalten.

## Verbleibende Risiken

Frische integrierte Konfigurations-/Runtime- und Canonical-Evidenz bleiben Koordinator-Verantwortung. Erhaltene Unit-Receipts allein beweisen keine Runtime-Abdeckung.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Build, native Runtime, E2E, Remote-CI, Sonar oder Push: durch diese begrenzte Integrationsaufgabe ausgeschlossen.

## Finaler Diff- und Review-Status

Fokussierten Config3-Slice und Negativkontrollen geprüft; separater Commit nur der vier Python-Dateien und des generierten zweisprachigen Records. Parallele Slices bleiben unstaged.
