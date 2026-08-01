# Finding FND-SONAR-0024: Native-ModSecurity-Oracle-main überschreitet Sonars Grenze für kognitive Komplexität

**Sprache:** Deutsch | [English](finding.md)

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `maintainability` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schwere / Confidence | `P2` / `not_applicable` / `confirmed` |
| Status / Feasibility | `verified` / `feasible_now` |
| Release-Blocker / sicherheitsrelevant | nein / nein |
| Sonar-Inventar | `c:S3776`, `AZ7b3dgOcO69wzd-_jHu` |

## Zusammenfassung, Verhalten und Auswirkung

Der an das Inventar gebundene `c:S3776`-Code-Smell meldete Cognitive
Complexity `30`, wo `25` erlaubt sind, in Native-Oracle-`main`. Er ist nur
Maintainability und begründet selbst keine Security-Vulnerabilität. Der lokale
Task-Patch extrahiert die lineare Request-Phasen-Sequenz in `process_request`
und zentralisiert Resource-Teardown in `cleanup_oracle`, während CLI-Parsing,
Result-JSON, Phasenreihenfolge, Reason-Strings und Exit-States erhalten bleiben.

Geschützter Squash-PR #200 vom exakten Head
`5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` erzeugte Parent-Master
`13890da56ad19a105629243349f39ea8c084f396`. Die Native-Oracle- und
fokussierten Reliability-Test-Blobs entsprechen dem geprüften Kandidaten;
Compiler- und Real-LibModSecurity-Controls bewahren ausgeübtes Verhalten, alle
14 Master-Workflows bestanden, und Default-Branch-Analyse
`c1f32224-aa05-4202-9b10-65c15165ff35` meldet
`AZ7b3dgOcO69wzd-_jHu` nicht mehr. Das unabhängige nicht ignorierte globale
Quality Gate `ERROR` ist kein Akzeptanzkriterium für dieses nicht
sicherheitsrelevante Finding, daher ist sein Status `verified`, nicht `closed`.

## Scope, Reproduktion und Evidence

- Betroffene Dateien/Symbole: `ci/tools/native_modsecurity_oracle.c`,
  `tests/test_sonar_reliability_contract.py`, `main`, `process_request` und
  `cleanup_oracle`.
- Voraussetzungen: Die Inventar-Revision mit Complexity `30` wird analysiert
  und normale Request-Inputs/Rules/Expected-Status-Argumente werden übergeben.
- Durch Review von `c:S3776` Key `AZ7b3dgOcO69wzd-_jHu`, C17-GCC/Clang-
  Warning-as-Error-Builds und erlaubte-200-, Header-Blocked-403- und
  Setup-Error-Controls gegen echtes LibModSecurity reproduzieren.

Run-ID: `ci-tools-sonar-remediation-20260730`.

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| `.codex/plans/ci-tools-sonar-remediation.md` | `0029f0724d663e1d84408d56af69e71724a79f79dbb24c862aa0f628ffc0852c` | Erfasst `AZ7b3dgOcO69wzd-_jHu`, Complexity `30` und erforderliche Semantik-Erhaltung. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/security-diff-scan-20260730T100735Z/report.md` | `9d4b50736c29628147b053cd869e9253c1f95bf681e849174829929ec99b69d7` | Vollständiger fokussierter Review findet kein reportables diff-eingeführtes Security-Item und erfasst erhaltene Phasen/Resultate/Cleanup. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/runtime/native-final-clang-block-result.json` | `ae386940e02a5c12915ce68992b0ef64d562fc6b5fad0cfc4a80ea14fdc8d72e` | Realer 3.0.14-Request-Header-Control liefert pass, erwartet/tatsächlich `403`, `native_match: true`, Phase `request_headers`. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/runtime/native-final-gcc-missing-headers-result.json` | `4c4901048beaeb13e485761315a8d1f40ff3756d3616b29add1e257d80d994e0` | Der erwartete Setup-Error-Vertrag liefert Exit `2` und Reason `adding request headers failed`. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-exact-head-verification.md` | `42ba7a4ff8ff0172997a935f04a7fdf560b7b6ce9c70daab97fa24e69024f3be` | Exakter Draft-PR-#200-Head ist OPEN/Draft/CLEAN und MERGEABLE; erforderliche Checks und SonarQube-Cloud-Quality-Gate/Readbacks bestehen mit null PR-Issues, einschließlich ursprünglichem `c:S3776`-Key `AZ7b3dgOcO69wzd-_jHu`. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-66db7e3f-exact-head-verification.md` | `33cc911a5ee393fb44906c3e4dac76634df86d99fe07b3e105be9962148c840a` | Aufgefrischter Draft-PR-#200-Head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` gegen Master `726322b17d6423c7f9e3bba0e6affc051dbf94cd` ist OPEN/Draft/CLEAN und MERGEABLE; erforderliche Checks und SonarQube-Cloud-Quality-Gate/Readbacks bestehen mit null PR-Issues, einschließlich ursprünglichem `c:S3776`-Key `AZ7b3dgOcO69wzd-_jHu`. |

## Root Cause, Remediation und Controls

`main` vermischte Argument-Decoding, Rules-Setup, Request-Phasen-Fortschritt,
Result-Generierung und Cleanup in einer Control-Flow-Einheit. Der Task-Patch
extrahiert nur die lineare Phasensequenz und nutzt One-Owner-Cleanup; `main`
besitzt weiterhin CLI-Parsing, Setup, finale Result-Ausgabe und Exit-
Klassifikation. Keine Sonar-Rule, kein Quality Gate, keine Exclusion, kein
`NOSONAR` und keine Suppression werden geändert.

Akzeptanz ist auf exaktem resultierendem Master belegt: Das ursprüngliche Issue
und kein task-eigener Ersatz fehlen in der Default-Branch-Analyse; Request-/
JSON-/Reason-/Exit-/Cleanup-Semantik, C17-GCC/Clang-Controls, reale
200/403/Setup-Error-Controls und Hosted-Checks blieben ohne Bypass erhalten.
Regression:
`tests/test_sonar_reliability_contract.py`; legitime Controls sind die drei
Real-Library-Pfade.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

Exact-Draft-PR- und Resulting-Master-Hosted-Analysen sind erhalten.
Integration und Resulting-Master-Revalidierung sind abgeschlossen; für dieses
verifizierte Finding gibt es keinen technischen Blocker. `FND-SONAR-0016` ist
aggregierter Sonar-Kontext, `FND-SONAR-0023` ist die unabhängige Result-Writer-
Ursache und `FND-PARENT-0036` bleibt das getrennte historische Lifetime-
Finding. Die One-Owner-Cleanup-Verbesserung beweist nicht, dass natürlicher
Append-Failure reproduzierbar ist. Es erfolgte keine Risikoakzeptanz; die
geschützte Master-Integration ist als Evidence erfasst.

## Historie

- `2026-07-30T10:46:48Z`: als getrennte `c:S3776`-Source-Grenze alloziert;
  lokale Compiler-, Source-Contract- und Real-LibModSecurity-Controls bestehen,
  Hosted-Exact-Head-Sonar-Verifikation war zu diesem Zeitpunkt pending.
- `2026-07-30T11:07:21Z`: Exakter Draft-PR-#200-Head `2bc97ac058725fdba6a36ad93307487c160b1f05` bestand
  erforderliche GitHub-Checks und SonarQube-Cloud-Quality-Gate/Readbacks. Der
  ursprüngliche `c:S3776`-Key `AZ7b3dgOcO69wzd-_jHu` fehlt in der PR-Issue-Abfrage;
  Status bleibt `fixed` pending autorisierte Integration und Resulting-
  Master-Verifikation.
- `2026-07-30T11:33:48Z`: nachdem Master auf `726322b17d6423c7f9e3bba0e6affc051dbf94cd` vorrückte, bestand aufgefrischter exakter Draft-PR-#200-Head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` erforderliche GitHub-Checks und SonarQube-Cloud-Quality-Gate/Readbacks. Der ursprüngliche `c:S3776`-Key `AZ7b3dgOcO69wzd-_jHu` fehlt in der Null-Issue-PR-Abfrage; Status bleibt `fixed` pending autorisierte Integration und Resulting-Master-Verifikation.

## Resulting-Master-Disposition

Geschützter Squash-PR #200 vom exakten Head `5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` erzeugte Parent-
Master `13890da56ad19a105629243349f39ea8c084f396` am `2026-07-30T12:11:32Z`. Die Native-Oracle- und
fokussierten Reliability-Test-Blobs entsprechen dem geprüften Kandidaten; die
aufbewahrten Phase-, JSON-, Exit-State-, Compiler- und Real-LibModSecurity-
Controls gelten daher für diese exakte Quelle. Alle 14 Master-Workflows
bestanden, und die Default-Branch-Analyse `c1f32224-aa05-4202-9b10-65c15165ff35` meldet
`AZ7b3dgOcO69wzd-_jHu` nicht mehr.

Das projektweite Quality Gate bleibt für zurückgehaltene unabhängige
Bedingungen nicht ignoriert `ERROR`, ist aber kein Akzeptanzkriterium für
dieses nicht sicherheitsrelevante Maintainability-Finding. Der ursprüngliche
Key fehlt auf resultierendem Master bei bewahrten Controls; der Status steigt
daher auf `verified`, nicht `closed`. Das verwandte Lifetime-Finding
FND-PARENT-0036 bleibt `fixed`. Receipt-SHA-256: `69cdb1bbdc92c4faa82e2e722dd27d5eac32b3d33df50cc64fc7ed110d9da48a`.
