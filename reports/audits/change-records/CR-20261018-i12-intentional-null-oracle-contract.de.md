# Change Record: CR-20261018-i12-intentional-null-oracle-contract

**Sprache:** [English](CR-20261018-i12-intentional-null-oracle-contract.md) | Deutsch

Reine Quellvertragsprüfung; keine Hostqualifikation.
## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-intentional-null-oracle-contract |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `a2d545ac7ec4abce23595e1c033f094104617201` |

## Motivation und Problemstellung

Das ursprüngliche kanonische `phase2_over_limit` hat `visible_status: null` ohne Unresolved-Grund. Die bisherige Prüfung lehnte diesen definierten, host-/konfigurationsabhängigen Vertrag als fehlende Erwartung ab.

## Akzeptanzkriterien

Nur unverändertes, ausdrücklich vorhandenes ursprüngliches `visible_status: null` mit separater Root-Interpretation und hash-/revisionsgebundenem unabhängigen Primärbeleg akzeptieren. Unbekannte Originale, andere fehlende Felder, geänderte Erwartungen und ersetzte Belege ablehnen; keine Ausführung oder Hostqualifikation vergeben.

## Implementierungsentscheidung und Begründung

Die bestehende Review-API erhält `intentional_null_fields.visible_status`. Der Primärbeleg muss dieselbe unabhängige Pfad-/Hash-/Kind-/Revisionsbindung haben und von Implementierungsbytes getrennt bleiben. Die vollständigen kanonischen Hashes des effektiven und ursprünglichen Oracles müssen übereinstimmen; Korrekturen und Ersatzerwartungen dürfen diese Erklärung nicht nutzen. `native_result`, `phase` und der Statusschlüssel bleiben verpflichtend. Ursprüngliche ID-/Vertragshashes bleiben unverändert.

## Geänderte Dateien

- `ci/evidence/reports/generate-pr382-i12-oracle-reconciliation.py`
- `tests/test_i12_oracle_reconciliation.py`
- `ci/runtime/lifecycle/i12/README.md`
- `ci/runtime/lifecycle/i12/README.de.md`
- `reports/audits/change-records/CR-20261018-i12-intentional-null-oracle-contract.md`
- `reports/audits/change-records/CR-20261018-i12-intentional-null-oracle-contract.de.md`

## Ausgeführte Befehle

```sh
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -B -m pytest -q tests/test_i12_oracle_reconciliation.py tests/test_i12_lifecycle_ledger.py
rtk proxy make check-bilingual-docs PYTHON=/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python
rtk proxy make check-doc-links PYTHON=/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework
rtk proxy git diff --check
```

Python 3.14.7: 41 Tests und 76 Subtests bestanden. Bilinguale Dokumentations- und Linkprüfungen sowie Whitespaceprüfung bestanden. Der Vorher-Probelauf mit echter Originalzeile lehnte visible_status erwartungsgemäß ab. Exakte Befehle, Exits, Originalzeilen-/Primär-YAML-Hashes und Ausgabehashes liegen in externer Task-Evidence.

## Security-Auswirkung

Die Änderung verhindert eine Verwechslung eines beabsichtigt unbestimmten Werts mit fehlender Evidence. Sie erlaubt keine fehlenden Beobachtungen, entfernt keine Hostmessung, akzeptiert kein unaufgelöstes Original und behandelt Implementierungs-/Probeausgaben nicht als unabhängigen Primärbeleg.

## Runtime-Evidence

Kein Host wurde gestartet. Die reine Quellprüfung liefert weiterhin `full_lifecycle_qualified=false` ohne Retest. Der echte ursprüngliche Auswahlhash lautet `98f5423f9cf2a019997a8c751429c43956d3211488452b1e323b6099d10f847d`; der Framework-Primär-YAML-Hash lautet `83e1bc8c6292e90f01acc84617f05113d2dbe625c88d7c4278f5327a6c121cfd`. Die acht neuen Testmethoden enthalten diesen gepinnten kanonischen Vertrag sowie Negativkontrollen.

## Bekannte Einschränkungen

Diese Ausnahme betrifft ausschließlich ein bereits definiertes visible_status-null. Sie löst keinen der ursprünglich 596 unbekannten Oracle-Records und wählt keinen Clientstatus für eine neue Fixture. Historische Ledger, Reconciliation und zentrale Matrix wurden nicht neu erzeugt.

## Verbleibende Risiken

Root muss die Primärquelleninterpretation weiterhin beurteilen und jedes frische echte Hostpaket separat prüfen. Die Erklärung selbst beweist weder physischen Clientstatus noch nativen Lifecycle oder vollständige Abnahme.

## Nicht ausgeführte Prüfungen mit Begründung

Host-/Buildtests, CI und Sonar wurden für diese begrenzte Quellvertragsänderung nicht ausgeführt. Bestehende Lifecycle-/Oracle-Tests und vollständige Dokumentationsprüfungen wurden ausgeführt; Root verantwortet anschließende Integrations-/Lieferprüfung.

## Finaler Diff- und Review-Status

Umfang geprüft: bestehende Oracle-API, Regressionstests, zweisprachiges API-README und dieser zweisprachige Change Record. Keine Produkt-, Capture-Objekt-, Framework-/MRTS-Gitlink- oder historischen Evidence-Änderungen. Kein Commit, Push oder Hostlauf durch diesen Worker.
