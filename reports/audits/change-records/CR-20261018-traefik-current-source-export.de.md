# Change Record: CR-20261018-traefik-current-source-export

**Sprache:** [English](CR-20261018-traefik-current-source-export.md) | Deutsch

Nur eine Vorlage. Alle offenen Abschnitte mit tatsächlichen Fakten ausfüllen; keine Validierung wird behauptet.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-traefik-current-source-export |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `95691eb24d53c1d9b4b7a089b96e5776be8b2fcd` |

## Motivation und Problemstellung

Unvollständiges/historisches Quell-Staging durch vollständige authentifizierte aktuelle Parent-Quell-Exporte für vorhandene Traefik-Capture-Varianten ersetzen.

## Akzeptanzkriterien

Jede committete reguläre Parent-Datei mit exaktem Modus und SHA256 exportieren; HEAD-Commit, Baum und Gitlink-Revisionen binden; fremde Gitlink-Inhalte, Links, Git-Metadaten und nicht committete Producer ausschließen. Frische private konfigurierte externe Ziele verlangen und Fixture-Änderungen separat binden.

## Implementierungsentscheidung und Begründung

git ls-tree und cat-file gegen den unveränderlich aufgelösten Commit verwenden, jede Git-Blob-Identität prüfen und das vollständige v2-Inventar vor zentraler Capture-Anwendung einfrieren. Native- und forwardAuth-Preparer verwenden die vorhandenen zentralen Varianten und erhalten ursprüngliche Schutzprüfungen. Die Quellrevision im nativen Build-Manifest stammt jetzt aus dem tatsächlich exportierten Inventar.

## Geänderte Dateien

`connectors/traefik/harness/i12/source_export.py`; `connectors/traefik/harness/i12/native/prepare.py`; `connectors/traefik/harness/i12_auth/prepare.py`; the corresponding native/auth README EN/DE pairs; `tests/test_traefik_i12_source_export.py`; this Change Record pair.

## Ausgeführte Befehle

`rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_traefik_i12_source_export tests.test_traefik_i12_auth tests.test_traefik_i12_native_measurements tests.test_traefik_i12_quality_controls tests.test_traefik_i12_ledger`: bestanden, 45 Tests, Exit 0. Root-Beleg: `checks/root-traefik-export-integrated-20261018.json` im Lauf `i12-traefik-acceptance-20261015`; stderr-SHA256 `235363f05352d02bf9faddb52e8f10e3b5b9312065bbd1d397d80037890cf588`. Gezielte Exporter-Kontrollen: 5 bestanden. Der frühere kombinierte Test erhielt eine Zurückweisung des veralteten Manifests vor regulärer gemeinsamer Capture-Integration; die integrierte Wiederholung bestand.

## Security-Auswirkung

Ungültigen Speicher, Links, bestehende Ziele, nicht unterstützte Git-Einträge und beschädigte Blob-Antworten sicher zurückweisen. SHA1 dient ausschließlich der Git-Objektidentitätsprüfung mit usedforsecurity=False; SHA256 bindet das Evidence-Inventar. Keine Admission-, Peer-, Namespace-, UID-, Capability-, Read-only- oder Ressourcenprüfung wird abgeschwächt.

## Runtime-Evidence

Diese Änderung startete keinen Host. Reine Quellproben exportierten erfolgreich 2138 reguläre Dateien aus Commit `0f174e0e4eb0316abb3e8662eba04eaf2c820e8c`, Baum `21519c3215a70b202b29b27f9cb77c63851d769f`, und wendeten beide vorhandenen zentralen Varianten an. Temporäre Kopien wurden entfernt. Dies belegt ausschließlich Quellanwendung.

## Bekannte Einschränkungen

Nicht committete Abnahme-Producer sind aus der Identität committeter Quellen ausgeschlossen und müssen separat als Fixtures/Instrumentierung exportiert und gehasht werden. Aktuelle Quellanwendung belegt weder einen Build noch die Identität geladener Artefakte.

## Verbleibende Risiken

Neue integrierte Builds, tatsächliche Hostbeobachtungen und Original-ID-Qualifikation bleiben im Hauptauftrag erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Hosttests und finale gehostete CI/Sonar wurden in dieser Quellexport-Teilaufgabe nicht ausgeführt. Die zuständige Abnahmearbeit folgt der committeten Integration.

## Finaler Diff- und Review-Status

Root prüfte den Exporter-/Preparer-Diff und wiederholte die 45 integrierten Tests erfolgreich. Die Quellarbeit ist für einen normalen Commit bereit; dieser Worker führte weder Git-Delivery noch Hostausführung durch.
