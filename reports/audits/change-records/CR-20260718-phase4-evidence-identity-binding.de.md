# Change Record: Phase-4-Evidence-Identitätsbindung

**Sprache:** [English](CR-20260718-phase4-evidence-identity-binding.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-phase4-evidence-identity-binding` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Finding | `FND-PARENT-0027` |
| Grenze | Parent-Phase-4-Evidence-Validator, Parent-Makefile-Promotion-Verdrahtung und Parent-Tests; Framework und MRTS unverändert. |

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
- Die tatsächlichen Parent-Targets für First-Byte, No-Full-Buffering und
  Promotion rufen zusätzlich zum Framework-Check die entsprechenden
  Parent-Identitätsprüfungen auf.
- Englische/deutsche Change Records und ihre README-Links nennen nur
  beobachtete lokale und Delivery-Evidence; sie behaupten keine Framework- oder
  MRTS-Aktion und keinen Merge.

## Implementierungsentscheidung und Begründung

Der Parent-Checker leitet die erwartete native Identität aus
`FULL_LIFECYCLE_IDENTITIES` ab, bindet das kanonische Resultat an ausgewählten
Connector und CLI-Run-ID und verlangt `transaction_ids`, die bereits vom
kanonischen Resultatfall getragen werden. Der Matcher lehnt jedes Event ab,
das in einem dieser Felder fehlt oder abweicht. Dies nutzt das Identitätsmodell
des bestehenden Parent-Six-Connector-Core-Checkers und ändert weder einen
Framework-Producer-Vertrag noch das Evidence-Schema. Ein dedizierter
Parent-Makefile-Helper führt den Profil-Check für jedes strikte Gate aus und
führt zusätzlich für das entsprechende Target den passenden First-Byte-,
No-Full-Buffer- oder Promotion-Check aus. `host_profile` ist Metadatum auf
Resultat-Ebene und wird vor diesem Matcher validiert; das Event-Schema führt
den kanonischen `integration_mode`, auf den das ausgewählte native Profil
abgebildet wird.

## Security-Auswirkung

Die korrigierte Parent-Trust-Boundary verhindert, dass ein Rule-und-Phase-
Lookalike durch ein Parent-Target für First-Byte, No-Full-Buffer oder
Promotion als Phase-4-Runtime-Evidence des aktuell ausgewählten Hosts
promoted wird. Die Resultatgrenze validiert das ausgewählte `host_profile`;
die Event-Grenze validiert seinen kanonischen nativen `integration_mode`.
Die Parent-Consumer-Disposition von `FND-PARENT-0027` ist `fixed`; dieser
Record behauptet keinen Cross-Repository-Abschluss, weil der
Framework-autoritative Checker die separate Framework-eigene
Identitätsbindungs-Remediation `FND-CROSS-0006` benötigt.

## Geänderte Dateien

- `Makefile`
- `ci/checks/evidence/check-full-lifecycle-evidence.py`
- `tests/test_full_lifecycle_evidence.py`
- `tests/test_full_lifecycle_gate_wiring.py`
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
| `rtk env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_full_lifecycle_gate_wiring tests.test_full_lifecycle_evidence tests.test_six_connector_core_completion` | bestanden: 20 fokussierte Parent-Tests einschließlich des statischen Makefile-Contracts, der die Parent-Checks für First-Byte, No-Full-Buffer und Promotion erreicht. |
| `rtk make -n check-first-byte-before-response-end check-no-full-response-buffering check-full-lifecycle-promotion NO_CRS_RUN_ID=phase4-wiring-control ...` | bestanden: gab den Parent-Profil-Check sowie die target-spezifischen Parent-Kommandos für First-Byte, No-Full-Buffer und Promotion aus. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -c '<check_change_record_pair(...)>'` gegen dieses englische/deutsche Paar | bestanden: erforderliche Überschriften, Identitätsmetadaten und bilinguale Paarinvarianten. |
| `rtk env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHON=/root/git/ModSecurity-conector/.venv/bin/python make check-bilingual-docs` | durch fehlende Framework-Dokumentationsziele in diesem dedizierten Worktree blockiert; nach der Korrektur der Record-Überschriften meldete die Ausgabe keinen Fehler in diesem Change-Record-Paar. |
| `rtk git diff --check` | bestanden. |

## Runtime-Evidence

Nicht ausgeführt. Die verifizierte Evidence ist ein fokussierter
Parent-Unit-/Contract-Test der Validator-Grenze; sie ist keine Connector-
Runtime- oder Traffic-Behauptung.

## Delivery-Evidence (beobachtet am 2026-07-18 UTC)

- Die Implementierungs-Commits wurden auf
  `agent/harden-evidence-phase4-binding` gepusht:
  `8b7b13b294fe4043fb4002c1cb96ba3de72986f8`
  (`ci: bind phase4 evidence identity`) und
  `0124b0d685c69129d4aeace8eff75ccc288e7a8e`
  (`ci: wire phase4 identity checks into promotion gates`).
- Draft-PR [#57](https://github.com/Easton97-Jens/ModSecurity-conector/pull/57)
  war zum Beobachtungszeitpunkt gegen `master` `OPEN`. Zu dieser Beobachtung lösten lokales `HEAD`,
  `origin/agent/harden-evidence-phase4-binding` und der PR-Head alle auf
  `0124b0d685c69129d4aeace8eff75ccc288e7a8e` auf.
- Die PR-Check-Zusammenfassung zu dieser Beobachtung meldete 33 bestandene und 0
  fehlgeschlagene Checks. CodeQL war erfolgreich (Check-Run `88073814250`);
  SonarCloud Code Analysis war erfolgreich (Check-Run `88073815941`, Quality
  Gate bestanden mit 0 neuen Issues und 0 Security Hotspots).
- Die Delivery-Disposition am beobachteten Head war
  `verified_pr_parent_consumer_scope`: Der Parent-Consumer-PR-Head ist
  verifiziert, dieses eingegrenzte Ergebnis ist aber kein
  repository-weites `verified_pr`, solange das hohe, Framework-eigene
  `FND-CROSS-0006` `validated` bleibt. GitHub meldet keine
  Review-Entscheidung, und kein Merge ist autorisiert oder ausgeführt.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Connector-Build, kein Runtime-Harness, keine CRS/MRTS-Matrix und keine
Framework-Änderung wurden ausgeführt. Sie liegen weiter außerhalb des
Parent-Consumer-Validierungs-Scopes. `make check-doc-links` wurde nicht
ausgeführt, weil sein Target den Framework-Dokumentationschecker aufruft; die
aktuelle Aufgabe schließt Framework-Arbeit aus und dieser Worktree enthält
keine befüllten Framework-Dokumentationsziele. Der umfassende
`security-diff-scan`-Worker-Workflow wurde nicht ausgeführt, weil alle
verfügbaren Delegations-Slots bereits belegt waren; sein Capability-Preflight
lieferte `ready`. Die aktuellen Fakten zu CodeQL, SonarCloud, GitHub Actions,
Commit, Push und Draft-PR sind oben für den beobachteten exakten PR-Head-SHA
festgehalten; kein Merge erfolgte.

## Bekannte Einschränkungen

Diese Korrektur validiert Identitätsfelder, die bereits im kanonischen
Parent-Eventmodell vorhanden sind. Sie erstellt, signiert oder verändert
bewusst keinen Framework-Producer-Vertrag. Ein Runtime-Producer, der ein
erforderliches Feld auslässt, schlägt nun geschlossen fehl und benötigt eine
separat begrenzte Producer-Remediation, falls dies in einem tatsächlichen
Harness-Run auftritt. `FND-CROSS-0006` (`Framework authoritative Phase-4
checker does not bind promoted events to selected workload identity`) bleibt
ein hohes, `validated`, Framework-eigenes Finding und verhindert eine
Cross-Repository-Abschlussbehauptung.

## Verbleibende Risiken

Diese Änderung liefert keine Signatur oder unveränderliche Manifestkette für
einen bösartigen Producer oder eine Resultatdatei; das sind getrennte
Evidence-Authentizitätsgrenzen. Sie stellt sicher, dass dieser Validator eine
übereinstimmende `rule_id` und Phase nicht mehr als ausreichende
Identitäts-Evidence behandelt. Der Framework-autoritative Checker bleibt eine
getrennte High-Risk-Boundary, bis `FND-CROSS-0006` im owning Repository
remediert und verifiziert ist.

## Finaler Diff- und Review-Status

Der erste Identity-Matcher-Commit verdrahtete die Parent-Checks noch nicht in
die tatsächlichen Make-Targets für First-Byte und Promotion; eine unabhängige
Security-Review identifizierte diese Reachability-Lücke. Dieser Change Record
enthält die Parent-Verdrahtungs-Remediation und ihren statischen Contract-Test
aus dem Follow-up-Commit `0124b0d685c69129d4aeace8eff75ccc288e7a8e`. Die
Exact-Head-Delivery-Evidence steht oben: Das Parent-Consumer-Ergebnis ist
`verified_pr_parent_consumer_scope`, während `FND-CROSS-0006` eine
repository-weite Abschlussbehauptung verhindert. Der PR blieb zu dieser
Beobachtung Draft; diese Dokumentationskorrektur benötigt vor einer neuen
Delivery-Behauptung einen frischen Exact-Head-Review. Kein Merge ist autorisiert
oder ausgeführt.
