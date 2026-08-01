# Finding FND-SONAR-0022: Block-Status-Generator erlaubt, dass CLI-ausgewählte Ausgabe ihre gewählte Root verlässt

**Sprache:** Deutsch | [English](finding.md)

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `security_validated` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schwere / Confidence | `P1` / `medium` / `confirmed` |
| Status / Feasibility | `fixed` / `feasible_now` |
| Release-Blocker / sicherheitsrelevant | ja / ja |
| Sonar-Inventar | `pythonsecurity:S8707`, `AZ8d8_sBE36x1qGA4xhY` |

## Zusammenfassung, Verhalten und Auswirkung

Die an das Inventar gebundene SonarQube-Cloud-Vulnerabilität
`pythonsecurity:S8707`, Key `AZ8d8_sBE36x1qGA4xhY`, betrifft die
CLI-ausgewählte Ausgabegrenze des Parent-Block-Status-Generators. Der
historische Generator akzeptierte
`--out-dir ../generator-outside/baseline-escape` und erzeugte generierte
Dateien außerhalb der vom Aufrufer gewählten Current-Working-Directory-Root.

Erwartetes Verhalten akzeptiert nur einen relativen Nachkommen des bewusst
gewählten aktuellen Arbeitsverzeichnisses. Absolute Pfade, Parent-Traversal,
Intermediate-Symlink-Escape und ein Final-Generated-File-Symlink dürfen kein
externes Ziel ändern; gewöhnliche verschachtelte Ausgabe innerhalb der Root
bleibt gültig. Geschützter Squash-PR #200 vom exakten Head
`5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` ist nun Parent-Master
`13890da56ad19a105629243349f39ea8c084f396`. Seine Generator- und Checker-
Blobs entsprechen dem geprüften Kandidaten; ursprüngliche Containment- und
legitime Output-Controls, fokussierte Reliability-Suite, Bilingual-Suite und
alle 14 Master-Workflows bestanden. Default-Branch-Analyse
`c1f32224-aa05-4202-9b10-65c15165ff35` meldet den ursprünglichen Key nicht
mehr. Das Finding bleibt ausschließlich wegen des nicht ignorierten
Default-Branch-Quality-Gate `ERROR` `fixed` statt `verified`; es ist nicht
risikoakzeptiert.

## Scope, Voraussetzungen und Reproduktion

- Betroffene Dateien/Symbole: `ci/tools/generate-block-status-config.py`,
  `ci/checks/common/check-block-status-generator.py`, `generate`,
  `resolve_output_dir`, `open_output_dir` und `write_generated_file`.
- Voraussetzungen: Ein Aufrufer kontrolliert `--out-dir`; ein beschreibbarer
  Sibling oder extern auflösender Pfadeintrag steht bereit; die historische
  Implementierung wird verwendet.
- Die Baseline aus einem task-eigenen aktuellen Arbeitsverzeichnis mit
  `--out-dir ../generator-outside/baseline-escape` reproduzieren; generierte
  Dateien erscheinen außerhalb der gewählten Root. Danach den fokussierten
  Checker ausführen: verschachtelte In-Root-Ausgabe besteht, während
  Traversal-, Absolute-, Intermediate-Symlink- und Final-File-Symlink-Controls
  kein externes Ziel ändern können.

## Evidence

Run-ID: `ci-tools-sonar-remediation-20260730`.

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| `.codex/plans/ci-tools-sonar-remediation.md` | `0029f0724d663e1d84408d56af69e71724a79f79dbb24c862aa0f628ffc0852c` | Das Inventar erfasst Analyse `00fc69e7-8a50-4c44-9eae-abaf077610f5`, Issue `AZ8d8_sBE36x1qGA4xhY` und die Baseline-Traversal-Reproduktion. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/security-diff-scan-20260730T100735Z/report.md` | `9d4b50736c29628147b053cd869e9253c1f95bf681e849174829929ec99b69d7` | Der vollständige fokussierte Security-Diff-Review hat null diff-eingeführte Findings; alle fokussierten Hostile-Path-Controls bestehen lokal. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/security-diff-scan-20260730T100735Z/artifacts/05_findings/attack_path_analysis_report.md` | `9cb84a91230740f9ca22f10e64c98cf1900edc6ab9fe581d5dd8dc2c14d30d92` | Der finale Patch weist Absolute-/Traversal-Inputs zurück, nutzt No-Follow-Directory-Descriptors und ersetzt nur feste generierte Namen atomar. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-exact-head-verification.md` | `42ba7a4ff8ff0172997a935f04a7fdf560b7b6ce9c70daab97fa24e69024f3be` | Exakter Draft-PR-#200-Head ist OPEN/Draft/CLEAN und MERGEABLE; erforderliche Checks und SonarQube-Cloud-Readbacks bestehen mit null PR-Issues, null neuen Violations und `0.0%` New-Code-Duplikation. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-66db7e3f-exact-head-verification.md` | `33cc911a5ee393fb44906c3e4dac76634df86d99fe07b3e105be9962148c840a` | Aufgefrischter Draft-PR-#200-Head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` gegen Master `726322b17d6423c7f9e3bba0e6affc051dbf94cd` ist OPEN/Draft/CLEAN und MERGEABLE; erforderliche Checks und SonarQube-Cloud-Readbacks bestehen mit null PR-Issues, null neuen Violations und `0.0%` New-Code-Duplikation. |

Alle Beobachtungen liegen im Parent-Scope; Framework, MRTS, Gitlinks,
Scanner-Regeln, Quality Gates, Exclusions, `NOSONAR` und Suppressions bleiben
unverändert.

## Root Cause, Remediation und Akzeptanz

Der historische Code verband ein vom Aufrufer kontrolliertes Directory mit
generierten Dateinamen durch gewöhnliche Pfadoperationen, ohne
Containment-Vertrag oder descriptor-verankerte No-Follow-Traversal. Der
Task-Patch weist Absolute- und Parent-Traversal-Werte zurück, verlangt einen
relativen In-Root-Nachkommen, öffnet jede Directory-Komponente mit
No-Follow-Semantik und nutzt eine exklusive temporäre Datei plus
descriptor-relative atomare Ersetzung für feste generierte Namen.

Akzeptanz und Validierung umfassen die fokussierten Generator- und
Sonar-Reliability-Contracts, den byte-kompatiblen `501,403`-Output-Control,
den versiegelten Security-Review und die Default-Branch-Analyse auf exaktem
Master `13890da56ad19a105629243349f39ea8c084f396`, die
`AZ8d8_sBE36x1qGA4xhY` ohne Scanner-Control-Änderung nicht mehr meldet. Eine
Promotion zu `verified` oder `closed` erfordert zusätzlich ein nicht
ignoriertes Default-Branch-Quality-Gate `OK`; diese Bedingung bleibt unerfüllt.

## Abhängigkeiten, Controls, verwandte Findings und Restrisiko

Exact-Draft-PR- und Resulting-Master-SonarQube-Cloud-Evidence sind erhalten;
autorisierte Integration und Resulting-Master-Revalidierung sind erfolgt.
Regression-Controls sind
`ci/checks/common/check-block-status-generator.py` und
`tests/test_sonar_reliability_contract.py`; der legitime Control ist
verschachtelte In-Root-Ausgabe mit byte-kompatibler generierter Ausgabe. Die
verbleibende Bedingung ist das nicht ignorierte Default-Branch-Quality-Gate
`ERROR`, das eine Security-Promotion blockiert, aber nicht gelockert wird.

`FND-SONAR-0001` und `FND-SONAR-0016` sind verwandter Sonar-Kontext, keine
Duplikate; `FND-PARENT-0036` ist eine getrennte Native-Lifetime-Grenze. Die
gewählte Current-Working-Directory-Root bleibt eine Annahme über einen
vertrauenswürdigen, exklusiven Aufrufer/Umgebung. Es erfolgte keine
Risikoakzeptanz; die geschützte Master-Integration ist als Evidence erhalten.

## Historie

- `2026-07-30T10:46:48Z`: nach Inventar und Baseline-Traversal-Reproduktion
  alloziert, die die unabhängig behebbare CLI-zu-Dateisystem-Grenze belegten;
  lokaler Patch und Security-Review bestanden, Exact-PR-Head-Verifikation war
  zu diesem Zeitpunkt pending.
- `2026-07-30T11:07:21Z`: Exakter Draft-PR-#200-Head `2bc97ac058725fdba6a36ad93307487c160b1f05` bestand
  erforderliche GitHub-Checks und SonarQube-Cloud-Quality-Gate/Readbacks:
  null PR-Issues, null neue Violations und `0.0%` New-Code-Duplikation. Das
  Finding ist auf dem Kandidaten `fixed`, bleibt aber auf aktuellem Master
  Release-Blocker bis autorisierte Integration und Resulting-Master-
  Revalidierung.
- `2026-07-30T11:33:48Z`: nachdem Master auf `726322b17d6423c7f9e3bba0e6affc051dbf94cd` vorrückte, behielt normaler Merge-Commit `66db7e3f2de324c960d8db36b4b6760d958cd7e1` beide Change-Record-Index-Einträge. Der aufgefrischte Draft-PR ist CLEAN/MERGEABLE; erforderliche Checks und SonarQube-Cloud-Quality-Gate/Readbacks bestehen mit null PR-Issues, null neuen Violations und `0.0%` New-Code-Duplikation. Status bleibt `fixed` pending autorisierte Integration und Resulting-Master-Revalidierung.

## Resulting-Master-Disposition

PR #200 wurde vom exakten Head
`5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` am `2026-07-30T12:11:32Z`
geschützt per Squash als Parent-Master
`13890da56ad19a105629243349f39ea8c084f396` gemergt. Die Master-Generator-
und Checker-Blobs entsprechen dem geprüften Kandidaten; `make check-block-status-generator`, die 12-Test-Reliability-Suite, die 22-Test-
Bilingual-Suite, `git diff --check` und alle 14 Master-Workflows bestanden.
Die exakte Default-Branch-Sonar-Analyse
`c1f32224-aa05-4202-9b10-65c15165ff35` meldet
`AZ8d8_sBE36x1qGA4xhY` nicht mehr; in den zwei geänderten `ci/tools`-
Source-Pfaden ist keine Vulnerability/kein Bug offen.

Das projektweite Default-Branch-Quality-Gate ist dennoch nicht ignoriert
`ERROR`, weil zurückgehaltene unabhängige Security-Rating-/Hotspot-
Bedingungen bestehen. Die Security-Verifikationsregel verlangt Quality Gate
`OK` vor einer Promotion über `fixed`; dieses P1-Release-Blocker-Finding ist
daher nicht risikoakzeptiert und bleibt `fixed`, nicht `verified` oder
`closed`. Das aufbewahrte Receipt ist `pr200-master-integration-13890da5.md`,
SHA-256 `69cdb1bbdc92c4faa82e2e722dd27d5eac32b3d33df50cc64fc7ed110d9da48a`.
