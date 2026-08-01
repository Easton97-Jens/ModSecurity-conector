# Finding FND-SONAR-0021: Inneres Sonar-S131-Issue von PR #177 auf Master remediiert und verifiziert

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
| Candidate-Integration-Blocker | `false` |
| Profil | Historische Baseline `d0cd2970-18e5-4a3b-ad84-eb4f91a13855` für `fda62539…`; exakte Master-Analyse `a9e18381-2f71-4627-a750-731ceb8dd1c3` für `a1c8394e…` |

## Geschlossene Disposition — 2026-07-29T22:41:32Z

Der finale PR-#177-Head `da4dc5d77c0695182b58b116d55a285156992c15` ergänzte den fail-closed-Default an der tatsächlichen inneren S131-Grenze und wurde per SHA-gebundenem Squash als Master `a1c8394e528bfcd7b54bc3e0aac4cdf3430d1345` integriert. Der resultierende Master-Tree entspricht exakt diesem Kandidaten. Alle vierzehn beobachteten Master-Workflows endeten erfolgreich.

Die neueste SonarCloud-Analyse `a9e18381-2f71-4627-a750-731ceb8dd1c3` erfasst genau diese Master-Revision; die ursprüngliche Abfrage ungelöster `shelldre:S131`-Issues liefert jetzt null Issues. Die frische aufbewahrte Evidence ist extern versiegelt (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-postmerge-20260729T223327Z/manifest.md`). Es wurden weder `NOSONAR`, Suppression, Rule, Quality Gate, Exclusion, Bypass noch ein direkter Master-Push verwendet. Das verbleibende Projekt-Quality-Gate `ERROR` gehört ausschließlich zur separat akzeptierten FND-SONAR-0001-Security-Rating-/Hotspot-Baseline und wird diesem geschlossenen S131-Finding nicht zugerechnet.

## Historische Zusammenfassung und beobachtetes Verhalten

Der aufbewahrte SonarQube-Cloud-Issue-Readback meldet einen OPEN-
`shelldre:S131`-`CODE_SMELL`, Key `AZ7uz_BiBV84XD89pXti`, in
`common/scripts/run_blocked_runtime_smoke.sh:119`.

Die exakte Analyzer-Meldung lautet:

> Add a default case (*) to handle unexpected values.

Sonar markiert die Rule als `CRITICAL` und ihren Maintainability-Impact als
`HIGH`. Dieser lokale Record ist dennoch nicht sicherheitsrelevant
(`severity: not_applicable`): Es wird kein Angreifer-zu-Runtime-Security-Pfad
behauptet.

Die Issue-Response enthält `lastChangeAnalysisUuid`
`833494ef-5342-4c6e-8bcb-c92cb3e665e0`. Separat listet der Projektanalysen-
Readback `d0cd2970-18e5-4a3b-ad84-eb4f91a13855`, datiert
`2026-07-29T20:43:20+0000`, für Revision
`fda62539b6f0a710865707e3003b73ed4469f20e`; dieser Record behauptet nicht,
dass die unterschiedlichen UUIDs identisch sind.

Der PR-#177-Kandidat `8a95d22db11576d337743c8131af65a08a9449a8` ändert nur den
äußeren `case`-Default in Zeilen 184–194. Das bestätigte Issue betrifft den
unveränderten inneren `case` in Zeile 119, daher ist der Kandidat für die
Integration als behauptete S131-Remediation blockiert.

## Historisches erwartetes Verhalten und Impact

Der tatsächliche innere `case` an der gemeldeten Stelle muss einen expliziten
fail-closed-`*)`-Zweig für unerwartete Werte haben. Fokussierte Regression-
Coverage und das englische/deutsche Tracking müssen diesen inneren Zweig statt
des äußeren Defaults als S131-Remediation identifizieren.

Dies ist kein Release-Blocker, aber ein Candidate-Integration-Blocker. Der
Kandidat kann nicht wahrheitsgemäß als Remediation für `AZ7uz_BiBV84XD89pXti`
anerkannt oder ausgeliefert werden, bevor der tatsächliche innere case
korrigiert ist und ein frischer Exact-Head-Scan sowie gehostete SonarQube-
Cloud-Evidence vorliegen. Ändere keine Sonar-Rule, kein Quality Gate, keine
Exclusion, kein `NOSONAR`, keine Suppression und keine Risikoakzeptanz.

## Betroffener Scope und Preconditions

- Betroffene Datei: `common/scripts/run_blocked_runtime_smoke.sh`
- Betroffenes Symbol / Grenze: innerer `case`-Statement in Zeile `119`
- Kandidatenvergleich: der äußere Default liegt in Zeilen `184`–`194` von
  `8a95d22db11576d337743c8131af65a08a9449a8`
- Preconditions: Die aufbewahrte Issue-Abfrage liefert das OPEN-S131-Issue;
  die aufbewahrte Analyse-Abfrage listet Revision `fda62539b6f0a710865707e3003b73ed4469f20e`;
  und die Outer-only-Änderung des Kandidaten bleibt von der gemeldeten inneren
  Stelle getrennt.

## Reproduktion und Evidence

Run-ID: `20260729T204320Z-fnd-sonar-0021-blocked-smoke-s131`. Die gelieferten
read-only Commands liefen aus `/root/git/ModSecurity-conector` mit Exit `0`.
Die erfasste Zeit ist das gelieferte Sonar-Analyse-Datum, keine Behauptung
einer neuen Netzabfrage während dieses Tracking-Updates.

| Artefakt | SHA-256 | Command / Ergebnis |
| --- | --- | --- |
| `issue.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-blocked-smoke-s131/evidence/issue.json`) | `854c3a863b37013cbfa4ebc918e650fcbb3a3eefb0d0383f4e5ba79cfe29708e` | `rtk curl -fsS 'https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&rules=shelldre%3AS131&resolved=false&ps=500'`; ein OPEN-`shelldre:S131` in `common/scripts/run_blocked_runtime_smoke.sh:119`. |
| `analysis.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-blocked-smoke-s131/evidence/analysis.json`) | `462ee987c4213297fa0e0ff1ffa3714e97b14a25ce471e5682ea629cbffaa32a` | `rtk curl -fsS 'https://sonarcloud.io/api/project_analyses/search?project=Easton97-Jens_ModSecurity-conector&ps=3'`; Analyse `d0cd2970-18e5-4a3b-ad84-eb4f91a13855` hat Revision `fda62539b6f0a710865707e3003b73ed4469f20e`. |
| `receipt.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-blocked-smoke-s131/evidence/receipt.md`) | `9bd53db9f102c827469f81400cccc34117d2e3f390823189e6ab241cf5e601bd` | Begrenzter Receipt für Command, Kandidatenvergleich, Nicht-Duplikation und Candidate-Integration-Blocker. |

Das secret-freie Inventar ist in
`manifest.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-blocked-smoke-s131/manifest.md`)
und `SHA256SUMS` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-blocked-smoke-s131/SHA256SUMS`)
versiegelt.

## Root Cause und vorgeschlagene Remediation

Der in PR #177 erfasste äußere case-Default ist eine andere Kontrollflussgrenze
als der von Sonar gemeldete innere case. Der Kandidat lässt daher die
tatsächliche S131-Stelle ohne Default und das bisherige Issue-zu-Remediation-
Mapping war unvollständig.

Füge einen fail-closed-`*)`-Zweig zum tatsächlichen inneren `case` hinzu,
aktualisiere fokussierte Regression-Coverage für diesen inneren Unexpected-
Value-Pfad und gleiche das englische/deutsche Tracking ab. Hole anschließend
einen frischen Exact-Head-Scan und gehostete SonarQube-Cloud-Evidence ein.
Unterdrücke die Rule nicht und ändere keine SonarQube-Cloud-Konfiguration.

## Akzeptanzkriterien und Validierungsplan

1. Der tatsächliche innere case in
   `common/scripts/run_blocked_runtime_smoke.sh:119` hat einen expliziten
   fail-closed-`*)`-Zweig.
2. Fokussierte strukturelle Regression-Coverage prüft den tatsächlichen
   inneren Unexpected-Value-Default, während gültige benannte innere
   case-Source-Pfade erhalten bleiben.
3. Die englischen und deutschen Tracking-Records zitieren dasselbe Issue,
   dieselbe Stelle, denselben tatsächlichen Remediation-Zweig und dieselbe
   Validierungseinschränkung.
4. Es wird keine `NOSONAR`-, Suppression-, Rule-, Quality-Gate-, Exclusion-
   oder Risikoakzeptanz-Änderung eingeführt.
5. Ein frischer exakter PR-#177-Head-Scan und gehostete SonarQube-Cloud-
   Evidence zeigen die Disposition von `AZ7uz_BiBV84XD89pXti`, bevor die
   Candidate-Integration erneut betrachtet wird.

## Geschlossene Disposition, verwandte Findings und Restrisiko

Für dieses geschlossene Finding bestehen keine Abhängigkeiten oder Blocker mehr. Der fokussierte strukturelle Test prüft wahrheitsgemäß den tatsächlichen inneren Default; ein unabhängiger Outer-Default-Test und die erfolgreichen Exact-Master-Controls bewahren das legitime kontrollierte Skip-Verhalten. Die ursprüngliche Sonar-Reproduktion tritt nicht mehr auf.

Historisch benötigte die Reparatur eine task-owned fokussierte Parent-PR-#177-
Änderung und frische Exact-Head-Hosted-/SonarQube-Cloud-Evidence. Diese
Bedingungen waren vor der SHA-gebundenen Integration erfüllt und bleiben unten
nur als Chronologie erhalten.

- `FND-SONAR-0001` ist verwandter aktueller Quality-Gate-Kontext, kein
  Duplikat: Es besitzt die begrenzte akzeptierte Security-Hotspot-Baseline.
- `FND-SONAR-0016` ist verwandter aggregierter Draft-PR-Kontext, kein
  Duplikat.
- `FND-SONAR-0020` ist ein separater, nun geschlossener Event-Serializer-
  Cognitive-Complexity-Befund, kein Duplikat.

Es verbleibt kein FND-SONAR-0021-spezifisches Integrationsrisiko. Dieser Abschluss erweitert, ersetzt oder akzeptiert FND-SONAR-0001 nicht erneut.

## Historie

- `2026-07-29T20:43:20Z` — stabile ID `FND-SONAR-0021` nach aufbewahrten Daten
  für das unabhängig behebbare OPEN-inner-case-S131-Issue und den
  PR-#177-Candidate-Integration-Blocker alloziert.
- `2026-07-29T22:19:19Z` — exakter PR-#177-Head `da4dc5d…` korrigierte den tatsächlichen Inner-Case-Default, bestand den vollständigen versiegelten Security-Diff-Scan und die exakte gehostete SonarCloud-Evidence.
- `2026-07-29T22:41:32Z` — resultierender Master `a1c8394e…` wurde als tree-identisch zu `da4dc5d…` bestätigt; vierzehn Master-Workflows bestanden, die neueste SonarCloud-Analyse band an diesen SHA und die ursprüngliche Abfrage ungelöster S131-Issues lieferte null. Der Status ist daher `closed`.

## Aktuelle Abgleichbestätigung — 2026-08-01

[PR #177](https://github.com/Easton97-Jens/ModSecurity-conector/pull/177)
wurde normal als `a1c8394e528bfcd7b54bc3e0aac4cdf3430d1345` gemergt und ist vom
aktuellen `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c` erreichbar.
Der aktuelle SonarCloud-API-Readback für `AZ7uz_BiBV84XD89pXti` bleibt
`CLOSED` / `FIXED`; der aktuelle innere Case behält seinen Default-Branch und
die exakten PR-Checks melden 33 bestanden und 0 fehlgeschlagen.
