# Change Record: Phase-4-Evidence-Identitätsbindung

**Sprache:** [English](CR-20260718-phase4-evidence-identity-binding.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-phase4-evidence-identity-binding` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Finding | `FND-PARENT-0027` |
| Grenze | Nur Parent-Phase-4-Evidence-Validator und Parent-Tests; Framework und MRTS unverändert. |

## Motivation und Problemstellung

`matching_events` akzeptierte ein Phase-4-Event, wenn nur `rule_id` und
`phase` übereinstimmten. Ein kopiertes oder vorab platziertes Event konnte
damit einen PASS-Fall für First-Byte oder No-Full-Buffering erfüllen, obwohl
es zu einem anderen Run, Connector, ausgewählten nativen Profil (über dessen
kanonischen Event-seitigen Integrationsmodus) oder einer anderen Transaktion
gehörte.

## Akzeptanzkriterien

- Das kanonische Resultat und ein für eine Promotion verwendetes Phase-4-Event
  müssen mit ausgewähltem Connector, `run_id`, kanonischem nativem
  Profil/Integrationsmodus, `rule_id`, Phase und den `transaction_ids` des
  Resultatfalls übereinstimmen.
- Fehlende Identitätsmetadaten schlagen geschlossen fehl.
- Fixtures mit fremdem Run, kopiertem Connector, kopiertem nativen
  Integrationsmodus eines anderen ausgewählten Profils, beliebigem falschem
  Integrationsmodus und fremder Transaktion werden sowohl für First-Byte- als
  auch No-Full-Buffer-Prüfungen abgelehnt.
- Ein nativer Apache-Kontrollfall desselben Runs bleibt akzeptiert.
- Englische/deutsche Change Records und ihre README-Links nennen nur
  beobachtete lokale Evidence; es erfolgen keine Framework-, MRTS-, Git- oder
  Delivery-Aktionen.

## Implementierungsentscheidung und Begründung

Der Parent-Checker leitet die erwartete native Identität jetzt aus
`FULL_LIFECYCLE_IDENTITIES` ab, bindet das kanonische Resultat an ausgewählten
Connector und CLI-Run-ID und verlangt `transaction_ids`, die bereits vom
kanonischen Resultatfall getragen werden. Der Matcher lehnt jedes Event ab,
das in einem dieser Felder fehlt oder abweicht. Dies nutzt das Identitätsmodell
des bestehenden Parent-Six-Connector-Core-Checkers und ändert weder einen
Framework-Producer-Vertrag noch das Evidence-Schema.
`host_profile` ist Metadatum auf Resultat-Ebene und wird vor diesem Matcher
validiert; das Event-Schema führt den kanonischen `integration_mode`, auf den
das ausgewählte native Profil abgebildet wird.

## Security-Auswirkung

Die korrigierte Trust Boundary verhindert, dass ein Rule-und-Phase-Lookalike
als Phase-4-Runtime-Evidence des aktuell ausgewählten Hosts promoted wird. Die
Resultatgrenze validiert das ausgewählte `host_profile`; die Event-Grenze
validiert seinen kanonischen nativen `integration_mode`. Sie schließt den
validierten Parent-Matching-Bypass für `FND-PARENT-0027` und behält für
unvollständige Identitätsmetadaten ein geschlossenes Fehlverhalten bei.

## Geänderte Dateien

- `ci/checks/evidence/check-full-lifecycle-evidence.py`
- `tests/test_full_lifecycle_evidence.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260718-phase4-evidence-identity-binding.md`
- `reports/audits/change-records/CR-20260718-phase4-evidence-identity-binding.de.md`

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_full_lifecycle_evidence` vor der Matcher-Korrektur | Erwarteter Fehlschlag: Die fünf verlangten Spoofing-Klassen und die alternative Klasse fremde Transaktion wurden akzeptiert; der legitime Apache-Kontrollfall bestand. |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_full_lifecycle_evidence` nach der Matcher-Korrektur | bestanden: 17 Tests einschließlich aller negativen Fixtures und des legitimen Apache-Kontrollfalls. |
| `rtk env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_full_lifecycle_evidence tests.test_six_connector_core_completion` | bestanden: 19 fokussierte Parent-Tests. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -c '<check_change_record_pair(...)>'` gegen dieses englische/deutsche Paar | bestanden: erforderliche Überschriften, Identitätsmetadaten und bilinguale Paarinvarianten. |
| `rtk env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHON=/root/git/ModSecurity-conector/.venv/bin/python make check-bilingual-docs` | durch fehlende Framework-Dokumentationsziele in diesem dedizierten Worktree blockiert; nach der Korrektur der Record-Überschriften meldete die Ausgabe keinen Fehler in diesem Change-Record-Paar. |
| `rtk git diff --check` | bestanden. |

## Runtime-Evidence

Nicht ausgeführt. Die verifizierte Evidence ist ein fokussierter
Parent-Unit-/Contract-Test der Validator-Grenze; sie ist keine Connector-
Runtime- oder Traffic-Behauptung.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Connector-Build, kein Runtime-Harness, keine CRS/MRTS-Matrix, kein
CodeQL, kein SonarQube Cloud, keine GitHub Action, kein Commit, Push,
Pull-Request oder Merge wurde ausgeführt. Diese benötigen einen separaten
autorisierten Delivery- oder Runtime-Scope und gegebenenfalls einen exakten
Pull-Request-Head-SHA. `make check-doc-links` wurde nicht ausgeführt, weil
sein Target den Framework-Dokumentationschecker aufruft; die aktuelle Aufgabe
schließt Framework-Arbeit aus und dieser Worktree enthält keine befüllten
Framework-Dokumentationsziele. Der umfassende `security-diff-scan`-
Worker-Workflow wurde nicht ausgeführt, weil alle verfügbaren
Delegations-Slots bereits belegt waren; sein Capability-Preflight lieferte
`ready`.

## Bekannte Einschränkungen

Diese Korrektur validiert Identitätsfelder, die bereits im kanonischen
Parent-Eventmodell vorhanden sind. Sie erstellt, signiert oder verändert
bewusst keinen Framework-Producer-Vertrag. Ein Runtime-Producer, der ein
erforderliches Feld auslässt, schlägt nun geschlossen fehl und benötigt eine
separat begrenzte Producer-Remediation, falls dies in einem tatsächlichen
Harness-Run auftritt.

## Verbleibende Risiken

Diese Änderung liefert keine Signatur oder unveränderliche Manifestkette für
einen bösartigen Producer oder eine Resultatdatei; das sind getrennte
Evidence-Authentizitätsgrenzen. Sie stellt sicher, dass dieser Validator eine
übereinstimmende `rule_id` und Phase nicht mehr als ausreichende
Identitäts-Evidence behandelt.

## Finaler Diff- und Review-Status

Fokussierte Post-Fix-Tests, Change-Record-Paarvalidierung und finale
Whitespace-Diff-Validierung bestanden. Das vollständige Bilingual-Target ist
nur durch fehlende Framework-Linkziele in diesem Worktree extern blockiert.
Delivery-Status ist nur lokal: kein Staging, Commit, Push, Pull-Request oder
Merge erfolgte.
