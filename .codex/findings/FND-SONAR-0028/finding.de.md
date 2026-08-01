# Finding FND-SONAR-0028: Common-Runtime enthält achtzehn aktuelle SonarQube-Cloud-Maintainability-Befunde

**Sprache:** Deutsch | [English](finding.md)

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `maintainability` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Severity / Confidence | `P2` / `not_applicable` / `confirmed` |
| Status / Feasibility | `verified` / `feasible_now` |
| Release-Blocker / Candidate-Integration-Blocker / sicherheitsrelevant | nein / nein / ja |
| Sonar-Inventar | Initial: 1 × `c:S1820`, 1 × `c:S107`, 2 × `c:S995`, 10 × `c:S5350`, 3 × `c:S3776`, 1 × `c:S1912`; finaler Resulting Master: null zurückbehaltene Befunde. |

## Zusammenfassung, Verhalten und Auswirkung

Auf Parent-master `979e50b9d7d9a914e102465814e7f2fd4cd853eb` besaß das
eingegrenzte Inventar `common/runtime/` 18 offene C-Code-Smells, null Bugs,
Vulnerabilities, Security-Hotspots und Duplikatzeilen. Die Runtime vereinte
Konfigurations-Dispatch, Lifecycle-Validierung, Decision-Event-Serialisierung
und Transaction-Start-Arbeit in wenigen langen Funktionen. Außerdem stellte
sie zusammenhängende private Transaction-Daten als viele unabhängige Felder dar
und verwendete veränderbare Pointer für schreibgeschütztes HTTP-Parsing.

PR #216 wurde anschließend normal als Parent-master
`63f6baed5ea6f650aeb5372e148b32aa062a326b` gemergt; sein Tree ist identisch
mit dem geprüften finalen Head `2c49e0de7aa163252e2105a916c3bfca530cc1a7`.
Der PR besitzt Quality Gate `OK`, null neue Issues, null New-Violations und
`0,0 %` / null New-Code-Duplikation. Eine direkte Resulting-Master-Abfrage
findet jedoch weiterhin historischen Befund `AZ9MwjLo-bUaKQ_zSGBC`
(`c:S3776`) in `load_runtime_config`; seine Erstellungs- und letzte
Aktualisierungsdaten liegen vor dieser Aufgabe. Der Befund ist kein neuer
PR-Code, aber damit ist der initiale 18-Befunde-Scope noch nicht vollständig
remediiert.

Dies ist keine belegte Security-Vulnerability. Der Code verarbeitet jedoch
HTTP-Eingaben und ModSecurity-Enforcement-State; deshalb unterliegt die
Remediation einem vollständigen Security-Diff-Review und einer Exact-Head-
Hosted-Verifikation.

## Scope, Remediation und Controls

- Der Scope umfasst die zwei genannten Parent-Common-Runtime-C-Sources, ihren
  direkten SDK-Source-Contract-Control, den zweisprachigen Change Record,
  gepaarte Indizes und lokale Finding-Evidence.
- Die C17-kompatible Remediation gruppiert zusammenhängenden privaten State,
  extrahiert eng benannte Lifecycle-Helper und macht schreibgeschütztes Parsing
  const-korrekt.
- Konfigurationssemantik, Body-Limits, native Phase-Reihenfolge,
  Request-/Response-Enforcement, Event-Felder, Integrity-Chaining und
  HTTP-Parsing-Verhalten bleiben unverändert.
- Sonar-Regeln, Quality Gates, Exclusions, Suppressions, `NOSONAR`, Framework,
  MRTS, Gitlinks, master und Security-Controls liegen außerhalb des Scopes und
  bleiben unverändert.

## Aufbewahrte Evidence

Run-ID: `common-runtime-sonar-maintainability-20260801`.

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| `evidence/sonar-current-runtime-inventory.md` | `b955ad65a2e36748344a39362178a2e46fd72297b7d18a1ddf55d42b0b6c962f` | 18 aktuelle offene Code-Smells; null Directory-Bugs, Vulnerabilities, Hotspots und Duplikatzeilen. |
| `security-diff-scan/report.md` | `72989b19f803956b284f04ce8fc24b6bb52f95d7413ddbeed26cdd226c10d01d` | Vollständige Source- und Direct-Control-Abdeckung; kein reportable diff-induced Security-Finding. |
| `security-diff-scan-amendment/report.md` | `a061e8aa74e838e2bbc9e7450b794f1944edf5ff9110d4c70f6bca6d87e4d8ea` | Finaler Const-Correctness-Delta reduziert Schreibfähigkeit und besitzt kein reportable Security-Finding. |
| `evidence/pr-216-exact-head-verification.md` | `36f9d8c1584b3e3f6506f2ca147829164ddb8b6720fbf355ad416f1659cd6185` | Exakter Draft-PR-#216-Head: Quality Gate OK, null PR-Issues/New-Violations/Duplikatzeilen, 0,0 % Duplikation, 33 bestandene Checks. |
| `evidence/pr-216-merge-master-verification.md` | `f3ba578d29e255b93342d79d6faaead84a49e66dc4a767f53d865d5b4ed34661` | Finaler PR-Head besitzt 33 Erfolge / sechs Scope-Skips; der Normal-Merge besitzt einen identischen Tree, 14 erfolgreiche Exact-Master-Workflows und einen zurückbehaltenen historischen `c:S3776`-Source-Befund. |
| `../../runs/parent-common-sonar-remediation-20260801/evidence/pr221-exact-head-verification.md` | `3420784833530d12802cebd9f98825eaa8e3cd45f584b6502ff3c22269db7efb` | Exakter Draft-PR-#221-Head besitzt null offene PR-Issues/New-Violations, `0,0 %` New-Code-Duplikation, alle anwendbaren Hosted-Checks bestanden und einen vollständigen Security-Diff-Review ohne Befund. |
| `../../runs/parent-common-sonar-remediation-20260801/evidence/pr221-merge-master-verification.md` | `c852730b467d505652414dd68124de553991efe9c46a8a67b45fbe9c1b014f17` | Exakter PR-#221-Head wurde normal als `3270ab5…` gemergt; alle 14 Master-Workflows bestehen und das Original-`c:S3776` ist `FIXED/CLOSED`. |

Die aufbewahrten Artefakte liegen unter
`/var/tmp/codex/ModSecurity-conector/runs/common-runtime-sonar-maintainability-20260801/`.
Sie enthalten kein Credential und ändern keinen Scanner-Control.

## Akzeptanz und aktueller Status

Die fokussierten lokalen C17-, Contract-, Security-, Memory-Safety-,
Flow-Integrity- und HTTP-Authorization-Controls bestehen. Auf finalem
[PR #216](https://github.com/Easton97-Jens/ModSecurity-conector/pull/216)-Head
`2c49e0de7aa163252e2105a916c3bfca530cc1a7` meldet SonarQube Cloud Quality
Gate `OK`, null OPEN/CONFIRMED-PR-Issues, null New-Violations und `0,0 %` /
null New-Code-Duplikation. Seine 39 terminalen GitHub-Check-Runs sind 33
Erfolge und sechs Scope-Skips bei null Fehlern. Der resultierende Master-Tree
des Normal-Merge ist identisch und alle 14 Master-SHA-Workflows bestehen.

GitHub mergte [PR #221](https://github.com/Easton97-Jens/ModSecurity-conector/pull/221)
normal an seinem exakten geprüften Head `dcfc64044d0f34b852a1b5cbc0cecd66cf6d1f9d`
und erzeugte Parent-master `3270ab5bdcc86ddab50e9be00db7611aae7fd937` um
`2026-08-01T13:36:33Z`. Alle 14 Push-Workflows für diese exakte Master-Revision
bestanden. Der direkte Resulting-Master-SonarQube-Cloud-Recheck um
`2026-08-01T13:39:56Z` meldet Originalbefund `AZ9MwjLo-bUaKQ_zSGBC` um
`2026-08-01T13:37:19Z` als `FIXED/CLOSED`.

Der Befund ist deshalb `verified`. Das globale Master-Quality-Gate bleibt
`ERROR`, weil die getrennte `FND-SONAR-0001`-New-Security-Rating-Baseline noch
`5` ist; keine Sonar-Policy und kein Security-Control änderten sich hier.

## Historie

- `2026-08-01T10:12:24Z`: aufbewahrte Current-Master-Evidence bestätigte die
  18 zusammenhängenden In-Scope-Maintainability-Befunde und allokierte dieses
  Parent-Finding. Remediation und lokale Validierung begannen; kein Scanner-
  Policy-, PR-, Merge- oder master-State änderte sich.
- `2026-08-01T10:29:10Z`: exakter Draft-PR-#216-Head
  `ad2f8e9a90af8981c060fe025b8ef5705556b9cf` für den Task-Scope verifiziert:
  33 bestandene / null fehlgeschlagene terminale GitHub-Checks, SonarQube-Cloud-
  Quality-Gate `OK`, null OPEN/CONFIRMED-PR-Issues, null New-Violations und
  `0,0 %` / null New-Code-Duplikation. Der nicht schreibende `header_end`-
  Const-Amendment beseitigte das einzige transiente `c:S5350`-Ergebnis. Es
  erfolgten kein Merge und keine master-Aktion.
- `2026-08-01T11:01:02Z`: PR #216 wurde normal als Parent-master
  `63f6baed5ea6f650aeb5372e148b32aa062a326b` gemergt; sein Tree ist identisch
  mit finalem Head `2c49e0de7aa163252e2105a916c3bfca530cc1a7`, und alle 14
  Master-SHA-Workflows bestanden. Das Zero-New-Sonar-Ergebnis des PR bleibt
  gültig, aber die direkte Resulting-Master-Source-Abfrage behält historischen
  `AZ9MwjLo-bUaKQ_zSGBC` / `c:S3776` in `load_runtime_config`; deshalb bleibt
  der Befund in progress. Das unabhängige globale Quality-Gate-Security-Rating
  bleibt unter `FND-SONAR-0001` aufbewahrt.
- `2026-08-01T13:12:18Z`: exakter Draft-PR-#221-Head
  `482ba035ed53b3668009b7158c656214d6924e6f` extrahiert den zurückbehaltenen
  Parser ohne Änderung seiner Validierungs- oder Close-Verträge. Anwendbare
  Hosted-Checks bestanden; SonarQube Cloud meldet null offene PR-Issues, null
  New-Violations und `0,0 %` New-Code-Duplikation; der vollständige
  Security-Diff-Review besitzt null reportable Befunde. Der Befund ist `fixed`
  und wartet vor `verified` oder `closed` auf autorisierten Merge und
  Resulting-Master-Reproduktion.
- `2026-08-01T13:39:56Z`: GitHub mergte exakten PR-#221-Head
  `dcfc64044d0f34b852a1b5cbc0cecd66cf6d1f9d` normal als Resulting Master
  `3270ab5bdcc86ddab50e9be00db7611aae7fd937`; alle 14 Exact-Master-Workflows
  bestanden. Der direkte SonarQube-Cloud-Recheck meldet Original-
  `AZ9MwjLo-bUaKQ_zSGBC` / `c:S3776` um `2026-08-01T13:37:19Z` als
  `FIXED/CLOSED`. Der Befund ist `verified`; die unabhängige globale
  Quality-Gate-Security-Rating-Baseline bleibt unter `FND-SONAR-0001`.
