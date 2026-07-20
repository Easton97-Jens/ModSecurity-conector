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
Die Parent-Consumer-Disposition von `FND-PARENT-0027` ist `fixed`, aber nicht
`verified` oder geschlossen. Die zuvor getrennte Framework-autoritative
Identitätslücke `FND-CROSS-0006` wurde unabhängig durch Framework-PR #34
remediert und auf Framework-Master
`3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` verifiziert. Der aktuelle
Parent-Master referenziert die spätere Framework-Master-Revision
`efdbcbd98afeed0f39f8912ce1140aaa5742f507`; PR #57 enthält keinen
Framework-Gitlink-Delta. Dieser Parent-Record behauptet weder eine
Framework-/MRTS-Aktion noch ändert er den separaten Default-Branch-
SonarQube-Backlog `FND-SONAR-0002`.

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

## Delivery-Evidence

### Historische Erstbeobachtung — 2026-07-18 UTC

- Die Implementierungs-Commits wurden auf
  `agent/harden-evidence-phase4-binding` gepusht:
  `8b7b13b294fe4043fb4002c1cb96ba3de72986f8`
  (`ci: bind phase4 evidence identity`) und
  `0124b0d685c69129d4aeace8eff75ccc288e7a8e`
  (`ci: wire phase4 identity checks into promotion gates`).
- Die anfängliche Draft-PR-Beobachtung war an
  `0124b0d685c69129d4aeace8eff75ccc288e7a8e` gebunden; sie ist nur
  historisch und keine Evidence für einen späteren PR-Head.

### Aktuelle Basis-Update-Beobachtung — 2026-07-20 UTC

- Die aktuelle Task-Anweisung autorisiert eine Parent-Master-Integration nur
  bedingt nach jeder Protection- und Exact-Head-Gate. Sie autorisiert keinen
  Framework-Master-Merge, keine MRTS-Aktion, keinen direkten Master-Write und
  keinen Bypass.
- GitHub aktualisierte Draft-PR
  [#57](https://github.com/Easton97-Jens/ModSecurity-conector/pull/57) regulär
  mit aktuellem Parent-Master `9ef0619b9c00729c16b7056943d7843785223095`.
  Der resultierende PR-Head ist der signierte reguläre Merge-Commit
  `7a36393797cc7ec7b1659e6823b74e0a58ec9f6e`; der Branch liegt fünf Commits
  vor und null hinter dieser Basis. Der task-eigene Worktree wurde danach
  sicher fast-forwarded, sodass lokales `HEAD`, Remote-Branch und PR-Head bei
  dieser Beobachtung übereinstimmten.
- An diesem exakten beobachteten Head waren alle 39 GitHub-Check-Runs terminal:
  33 bestanden, sechs waren scope-gestützte Skips, kein Run war fehlgeschlagen,
  abgebrochen oder ausstehend. Die sechs strikten Ruleset-Kontexte bestanden;
  CodeQL bestand mit null offenen Code-Scanning-Alerts, und SonarClouds Quality
  Gate bestand mit null neuen Issues und null Security Hotspots.
- GitHub meldete `OPEN`, `DRAFT`, `MERGEABLE` und `CLEAN`; es gab null
  eingereichte Reviews, Review-Threads, Inline-Kommentare und angeforderte
  Reviewer. Der aktuelle PR-Diff enthält nur acht Parent-Dateien. Er enthält
  keinen Framework-, MRTS- oder Gitlink-Pfad-Delta; sowohl Basis als auch Head
  referenzieren Framework `efdbcbd98afeed0f39f8912ce1140aaa5742f507`. Damit
  enthält er nicht den separaten Framework-Draft-PR #36.
- Diese Change-Record-Korrektur erzeugt beim Commit und Push absichtlich einen
  neuen PR-Head. Die vorhergehenden Exact-Head-Checks und das Review sind dann
  nur historische Evidence: Der neue Head benötigt vor einer Ready- oder
  Merge-Entscheidung wieder einen vollständigen Zyklus aus GitHub-Checks,
  CodeQL, SonarCloud, Review/Threads und finalem Diff. Es wurde kein Merge
  durchgeführt.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Connector-Build, kein Runtime-Harness, keine CRS/MRTS-Matrix und keine
Framework-Änderung wurden ausgeführt. Sie liegen weiter außerhalb des
Parent-Consumer-Validierungs-Scopes. `make check-doc-links` wurde nicht
ausgeführt, weil sein Target den Framework-Dokumentationschecker aufruft;
dieser dedizierte Worktree enthält keine befüllten
Framework-Dokumentationsziele. Der umfassende `security-diff-scan`-
Worker-Workflow wird für die aktuelle Basis-Update-Beobachtung nicht
behauptet; eine fokussierte unabhängige Diff-Review fand an
`7a36393797cc7ec7b1659e6823b74e0a58ec9f6e` keinen konkreten neuen Bypass.
Für den noch zu erzeugenden Dokumentations-Commit existiert kein Exact-Head-
Remote-Check; sein vollständiger frischer Delivery-Zyklus bleibt erforderlich.
Es erfolgte kein Merge.

## Bekannte Einschränkungen

Diese Korrektur validiert Identitätsfelder, die bereits im kanonischen
Parent-Eventmodell vorhanden sind. Sie erstellt, signiert oder verändert
bewusst keinen Framework-Producer-Vertrag. Ein Runtime-Producer, der ein
erforderliches Feld auslässt, schlägt nun geschlossen fehl und benötigt eine
separat begrenzte Producer-Remediation, falls dies in einem tatsächlichen
Harness-Run auftritt. `FND-CROSS-0006` ist jetzt unabhängig auf
Framework-Master verifiziert; dieser Parent-only PR schließt weder
`FND-PARENT-0027` noch bearbeitet er den separaten Framework-Default-Branch-
SonarQube-Backlog `FND-SONAR-0002`.

## Verbleibende Risiken

Diese Änderung liefert keine Signatur oder unveränderliche Manifestkette für
einen bösartigen Producer oder eine Resultatdatei; das sind getrennte
Evidence-Authentizitätsgrenzen. Sie stellt sicher, dass dieser Validator eine
übereinstimmende `rule_id` und Phase nicht mehr als ausreichende
Identitäts-Evidence behandelt. Die Framework-autoritative Checker-
Identitätsgrenze wurde separat durch Framework-PR #34 verifiziert; das
Restrisiko behauptet nicht, dass #57 oder dieser Record den separaten
Framework-Default-Branch-SonarQube-Backlog verändert.

## Finaler Diff- und Review-Status

Der erste Identity-Matcher-Commit verdrahtete die Parent-Checks noch nicht in
die tatsächlichen Make-Targets für First-Byte und Promotion; eine unabhängige
Security-Review identifizierte diese Reachability-Lücke. Dieser Change Record
enthält die Parent-Verdrahtungs-Remediation und ihren statischen Contract-Test
aus dem Follow-up-Commit `0124b0d685c69129d4aeace8eff75ccc288e7a8e`. Eine
fokussierte unabhängige Review des regulär aktualisierten Heads
`7a36393797cc7ec7b1659e6823b74e0a58ec9f6e` fand keinen konkreten neuen
Security-Bypass; die beobachtete Exact-Head-CI/CodeQL/Sonar-Evidence steht
oben. Diese Dokumentationskorrektur macht diesen Head historisch; nach eigenem
Commit und Push müssen ein frisches Exact-Head-Review und alle erforderlichen
Checks bestehen, bevor #57 Draft verlassen oder in den bedingten
Parent-Master-Integrationsablauf eintreten kann. Es wurde kein Merge
durchgeführt.
