# Finding FND-SONAR-0020: Event-JSON-Serializer-Cognitive-Complexity-Befund auf Master remediiert und verifiziert

**Sprache:** Deutsch | [English](finding.md)

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `sonarqube_finding` |
| Repository / Ownership | `parent` / `parent` |
| Priorität | `P2` |
| Security-Severity / -Relevanz | `not_applicable` / `false` |
| Konfidenz / Status | `confirmed` / `closed` |
| Feasibility | `already_fixed` |
| Release-Blocker | `false` |
| Profil | Historischer Master `a5901a3c…`; PR #197 wurde als Master `caddd86…` gesquasht und durch Analyse `43a50e20…` verifiziert |

## Zusammenfassung und beobachtetes Verhalten

Die historische Current-Master-Analyse
`f179066b-a8ed-4471-895e-342cebd8dc52` meldete einen OPEN-`c:S3776`
`CODE_SMELL`, Key `AZ9cRy9OHhV2CayPTP4Y`, in
`common/src/event.c:502`, Symbol `msconnector_event_write_json_ex`: Cognitive
Complexity `26`, wo `25` erlaubt waren.

PR #197 extrahierte den gemeinsamen begrenzten Optional-Event-JSON-Field-
Formatting-Pfad, ohne eine Sonar-Rule, ein Quality Gate, eine Exclusion,
`NOSONAR`, eine Suppression oder eine Risikodisposition zu ändern. Sein exakter
Delivery-Head `8a9036a7663f4170a02a0e3b7a677e306ddc6012` bestand fokussierte
lokale, Security-, Hosted- und PR-Sonar-Evidenz und wurde SHA-gebunden als
Master `caddd86d1eede95de53aa1bc971dd26d875df21c` gesquasht.

Die Current-Master-Analyse `43a50e20-8bdd-453a-bc44-549a7e3d7588` erfasst
diese exakte Revision und markiert `AZ9cRy9OHhV2CayPTP4Y` als `CLOSED` /
`FIXED`. Die ursprüngliche Reproduktion tritt damit auf Master nicht mehr auf.

## Erwartetes Verhalten und Impact

Die abgeschlossene Reparatur hält `msconnector_event_write_json_ex` an oder
unter der konfigurierten Grenze, ohne eine Sonar-Rule, ein Quality Gate, eine
Exclusion, `NOSONAR`, eine Suppression oder eine Risikodisposition zu ändern.
Sie bewahrt JSON-Serialisierungskompatibilität, Trunkierungs-/Failure-
Verhalten, Bounded-Transport-Token-Validierung und Raw-QUIC-Connection-ID-
Redaktion.

Dies war ein bestätigter nicht-sicherheitsrelevanter Maintainability-Befund
(`severity: not_applicable`) trotz Sonars historischer `CRITICAL` / `HIGH`-
Maintainability-Klassifikation. Das aktuelle Master-Quality-Gate bleibt nur
wegen der separaten akzeptierten FND-SONAR-0001-Baseline
`new_security_rating=5` und `new_security_hotspots_reviewed=0.0` auf `ERROR`;
`new_maintainability_rating=1` bleibt bestanden. Dieser geschlossene Befund
ändert oder erweitert diese Risikoakzeptanz nicht.

## Betroffener Scope, historische Preconditions und Closure-State

- Betroffene Datei: `common/src/event.c`
- Betroffenes Symbol: `msconnector_event_write_json_ex`
- Protokoll / Grenze: Event-JSON-Serialisierung
- Historische Preconditions: SonarQube Cloud analysierte Parent master
  `a5901a3c89528ec9a43ab9755da5755fdb01420d`; Issue
  `AZ9cRy9OHhV2CayPTP4Y` war an der genannten Stelle OPEN.
- Closure-State: PR-#197-Delivery-Head `8a9036a…` wurde SHA-gebunden als
  Master `caddd86…` gesquasht; die Current-Master-Analyse `43a50e20…`
  markiert das Issue als `CLOSED` / `FIXED`.

## Reproduktion und Evidence

Die historische Run-ID ist
`20260729T195549Z-fnd-sonar-0020-event-cognitive-complexity`. Ihre
Beobachtungen erfolgten aus `/root/git/ModSecurity-conector` um
`2026-07-29T19:55:49Z`. Die Closure-Run-ID ist
`20260730T135511Z-fnd-sonar-0020-postmerge-verification`; ihre aufbewahrte,
secret-freie Post-Merge-Zusammenfassung ist an Master `caddd86…` gebunden.

| Artefakt | SHA-256 | Command / Ergebnis |
| --- | --- | --- |
| `issue.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/evidence/issue.json`) | `69d6fa710a3e99b4a18151a13eb6bcf83e600a1c0d3188b0036b4115cb66c4ea` | `rtk proxy curl --fail --silent --show-error 'https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&issues=AZ9cRy9OHhV2CayPTP4Y&ps=10'`; liefert ein OPEN-`c:S3776`-Issue in `common/src/event.c:502`, Komplexität `26`, wo `25` erlaubt ist. |
| `analysis.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/evidence/analysis.json`) | `1c12b6c8e780a1282cdb8fdc154ddc2543bf5ca2901f267994a26c83ef8ba446` | `rtk proxy curl --fail --silent --show-error 'https://sonarcloud.io/api/project_analyses/search?project=Easton97-Jens_ModSecurity-conector&ps=1'`; bindet Analyse `f179066b-a8ed-4471-895e-342cebd8dc52` an master `a5901a3c89528ec9a43ab9755da5755fdb01420d`. |
| `quality-gate.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/evidence/quality-gate.json`) | `a65798fd40f5538e793d1734eb631235eb6809ae9107a2086acdc9a87b6e3689` | `rtk proxy curl --fail --silent --show-error 'https://sonarcloud.io/api/qualitygates/project_status?projectKey=Easton97-Jens_ModSecurity-conector'`; zeigt die separate Security-Hotspot-Baseline und `new_maintainability_rating=1`. |
| `receipt.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/evidence/receipt.md`) | `5790131a8e4b5b159001af9a60c9b316209d8ceca6fc66e2e1453f52c4b7cd8f` | Begrenzter Receipt für Command, Exit-Code, Source-Revision und Interpretation. |
| `sonar-master-readback.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-186-199-20260730T072658Z/fnd-sonar-0020-postmerge-verification-20260730T135511Z/evidence/sonar-master-readback.json`) | `1c1c704489e1d8bf4ea09f466b6a132dd9f5f36a0095a069c2cf9b6da93d86c3` | Read-only-Post-Merge-Sonar/GitHub-Monitor-Readback plus `rtk git rev-parse HEAD origin/master`; Analyse `43a50e20…` bindet an `caddd86…`, und `AZ9cRy9OHhV2CayPTP4Y` ist `CLOSED` / `FIXED`. |
| `Post-Merge-receipt.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-186-199-20260730T072658Z/fnd-sonar-0020-postmerge-verification-20260730T135511Z/evidence/receipt.md`) | `d0857f57980009e47ba469f143d91055c2e8b75d77ce155e27b6c25b12ad531d` | Hash-gebundener Receipt für die exakten wiederholbaren Read-only-Master-, Analyse-, Issue- und Quality-Gate-Readbacks. |

Das historische secret-freie Inventar ist in
`manifest.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/manifest.md`)
und `SHA256SUMS` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0020-event-cognitive-complexity/SHA256SUMS`)
versiegelt.
Das separate Closure-Run-Inventar ist in
`manifest.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-186-199-20260730T072658Z/fnd-sonar-0020-postmerge-verification-20260730T135511Z/manifest.md`)
und `SHA256SUMS` (`/var/tmp/codex/ModSecurity-conector/pr-integration-186-199-20260730T072658Z/fnd-sonar-0020-postmerge-verification-20260730T135511Z/SHA256SUMS`)
versiegelt.

## Root Cause und vorgeschlagene Remediation

Historisch kombinierte die Funktion zahlreiche unabhängige Validierungs-,
Redaktions-, Metadatenpräsenz-, Formatierungs- und Trunkierungszweige. PR #174
senkte die gemessene Komplexität von `32` auf `26`, ließ den Befund aber einen
Punkt über der Grenze.

Ohne Sonar-Konfigurationsänderung abgeschlossen: PR #197 extrahierte den
gemeinsamen begrenzten Optional-JSON-Field-Formatting-Pfad. Sein exakter Head
bestand C17- und ASan/UBSan-Common-Helper-Smokes, Common-SDK-/Security-/Flow-
Contracts, 22 Bilingual-Documentation-Tests, einen versiegelten Zero-Finding-
Security-Diff-Scan, alle erforderlichen Hosted-Gates und PR-Sonar-Quality-Gate
`OK` und wurde anschließend SHA-gebunden auf Master gesquasht.

## Akzeptanzkriterien und Validierungsplan

1. `AZ9cRy9OHhV2CayPTP4Y` ist in Current-Master-Analyse `43a50e20…`
   `CLOSED` / `FIXED`.
2. Es wurde keine `NOSONAR`-, Suppression-, Sonar-Rule-, Quality-Gate-,
   Exclusion- oder Risikoakzeptanz-Änderung verwendet.
3. Exact-Head-Common-C17-, ASan/UBSan-, SDK-/Security-/Flow-, Bilingual- und
   Diff-Checks bestanden.
4. Der versiegelte fokussierte Security-Diff-Review enthält null reportable
   Findings und bestätigt erhaltene Serialisierungs-, Trunkierungs-, Bounded-
   Token- und Raw-QUIC-CID-Redaktions-Controls.
5. Der exakte PR-Head bestand aktuelle Hosted-Checks, Reviews/Threads, CodeQL,
   Dependency-/Secret-Controls und SonarQube Cloud ohne Bypass.
6. Der SHA-gebundene Merge erzeugte `caddd86…`; seine Current-Master-Analyse
   führte den ursprünglichen Issue-Readback vor dem Closing dieses Befunds
   erfolgreich erneut aus.

## Dependencies, verwandte Findings und Restrisiko

Die fokussierte Parent-Remediation und der aktuelle SonarQube-Cloud-Exact-
Head-/Current-Master-Zugriff sind abgeschlossen. Es gibt keinen aktuellen
technischen Blocker.

- `FND-SONAR-0001` ist verwandter Current-Master-Quality-Gate-Kontext, kein
  Duplikat: Es besitzt die akzeptierte Drei-`python:S5332`-Security-Hotspot-
  Baseline.
- `FND-SONAR-0016` ist verwandter Scanner-Familien-Kontext, kein Duplikat: Es
  ist ein aggregierter Draft-PR-New-Code-/Duplication-Record.

Es bleibt kein FND-SONAR-0020-spezifisches Restrisiko. Der einzige verbleibende
Master-Quality-Gate-Fehler ist die separate, unveränderte und begrenzte
`FND-SONAR-0001`-Baseline; dieser Record ändert oder erweitert sie nicht.

## Historie

- `2026-07-29T19:55:49Z` — stabile ID `FND-SONAR-0020` nach Current-Master-
  Evidence für das unabhängig behebbare OPEN-Issue alloziert.
- `2026-07-30T13:41:13Z` — exakter PR-#197-Head `8a9036a…` reparierte die
  fokussierte Source-Grenze und bestand lokale, Security-, Hosted- und
  PR-Sonar-Evidenz.
- `2026-07-30T13:49:52Z` — resultierender Master `caddd86…` wurde durch
  Analyse `43a50e20…` verifiziert; das ursprüngliche Issue ist `CLOSED` /
  `FIXED`, daher ist der Befund geschlossen.

## Aktuelle Abgleichbestätigung — 2026-08-01

[PR #197](https://github.com/Easton97-Jens/ModSecurity-conector/pull/197)
wurde normal als `caddd86d1eede95de53aa1bc971dd26d875df21c` gemergt und ist vom
aktuellen `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c` erreichbar.
Der aktuelle SonarCloud-API-Readback für `AZ9cRy9OHhV2CayPTP4Y` bleibt
`CLOSED` / `FIXED`; die exakten PR-Checks melden 33 bestanden und 0
fehlgeschlagen. Das globale Master-Quality-Gate-ERROR wird separat als
`FND-SONAR-0001` verfolgt.
