# Finding FND-SONAR-0023: Native-ModSecurity-Oracle-Result-Writer überschreitet Sonars Parameteranzahlgrenze

**Sprache:** Deutsch | [English](finding.md)

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `maintainability` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schwere / Confidence | `P2` / `not_applicable` / `confirmed` |
| Status / Feasibility | `verified` / `feasible_now` |
| Release-Blocker / sicherheitsrelevant | nein / nein |
| Sonar-Inventar | `c:S107`, `AZ7b3dgOcO69wzd-_jHt` |

## Zusammenfassung, Verhalten und Auswirkung

Der an das Inventar gebundene `c:S107`-Code-Smell meldete die achtargumentige
Funktion `write_result` in `ci/tools/native_modsecurity_oracle.c`. Es ist ein
Maintainability-Finding, kein validierter angriffssteuerbarer Security-Pfad.
Der Task-Patch gruppiert zusammengehörige Ergebnisdaten in privaten
`struct result_context` und nutzt diesen Context für Ergebnisserialisierung,
ohne öffentliche CLI, JSON-Felder/-Reihenfolge, Reason-Strings oder den
Exit-State-Vertrag zu ändern.

Geschützter Squash-PR #200 vom exakten Head
`5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` erzeugte Parent-Master
`13890da56ad19a105629243349f39ea8c084f396`. Die Native-Oracle- und
fokussierten Reliability-Test-Blobs entsprechen dem geprüften Kandidaten; alle
14 Master-Workflows bestanden, und Default-Branch-Analyse
`c1f32224-aa05-4202-9b10-65c15165ff35` meldet
`AZ7b3dgOcO69wzd-_jHt` nicht mehr. Das unabhängige nicht ignorierte globale
Quality Gate `ERROR` ist kein Akzeptanzkriterium für dieses nicht
sicherheitsrelevante Finding, daher ist sein Status `verified`, nicht `closed`.

## Scope, Reproduktion und Evidence

- Betroffene Dateien/Symbole: `ci/tools/native_modsecurity_oracle.c`,
  `tests/test_sonar_reliability_contract.py`, `write_result` und
  `struct result_context`.
- Voraussetzungen: SonarQube Cloud analysiert die Inventar-Revision mit der
  achtargumentigen Definition; das Oracle wird mit unterstützten C17-
  Toolchains kompiliert.
- Durch Review von `c:S107` Key `AZ7b3dgOcO69wzd-_jHt`, Kompilieren des Patches
  mit GCC und Clang unter `-std=c17 -Wall -Wextra -Werror` und Ausführen des
  fokussierten Source-Contracts plus Real-LibModSecurity-200/403/Setup-Error-
  Controls reproduzieren.

Run-ID: `ci-tools-sonar-remediation-20260730`.

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| `.codex/plans/ci-tools-sonar-remediation.md` | `0029f0724d663e1d84408d56af69e71724a79f79dbb24c862aa0f628ffc0852c` | Erfasst `AZ7b3dgOcO69wzd-_jHt` und das kompakte Result-Context-Design. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/security-diff-scan-20260730T100735Z/report.md` | `9d4b50736c29628147b053cd869e9253c1f95bf681e849174829929ec99b69d7` | C17-GCC/Clang- und Real-LibModSecurity-200/403/Setup-Error-Controls bestehen; Phasen- und Result-Semantik bleiben erhalten. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/runtime/native-final-gcc-allow-result.json` | `ad1ed3ba88d88b8eb03683083a103461d2efb28e46135ace7365d297eaa80843` | Der erlaubte Real-LibModSecurity-3.0.14-Control liefert pass mit erwartetem/tatsächlichem Status `200`. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-exact-head-verification.md` | `42ba7a4ff8ff0172997a935f04a7fdf560b7b6ce9c70daab97fa24e69024f3be` | Exakter Draft-PR-#200-Head ist OPEN/Draft/CLEAN und MERGEABLE; erforderliche Checks und SonarQube-Cloud-Quality-Gate/Readbacks bestehen mit null PR-Issues, einschließlich ursprünglichem `c:S107`-Key `AZ7b3dgOcO69wzd-_jHt`. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-66db7e3f-exact-head-verification.md` | `33cc911a5ee393fb44906c3e4dac76634df86d99fe07b3e105be9962148c840a` | Aufgefrischter Draft-PR-#200-Head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` gegen Master `726322b17d6423c7f9e3bba0e6affc051dbf94cd` ist OPEN/Draft/CLEAN und MERGEABLE; erforderliche Checks und SonarQube-Cloud-Quality-Gate/Readbacks bestehen mit null PR-Issues, einschließlich ursprünglichem `c:S107`-Key `AZ7b3dgOcO69wzd-_jHt`. |

## Root Cause, Remediation und Controls

`write_result` vermischte eine stabile Ausgaberepräsentation mit zu vielen
unabhängigen Ergebniswerten. Die Reparatur erhält private Request-/Result-
Contexts, übergibt Result-Context plus Status/Reason an den Writer und bewahrt
die bestehende Serialisierungssemantik. Keine Sonar-Rule, kein Quality Gate,
keine Exclusion, kein `NOSONAR` und keine Suppression werden geändert.

Akzeptanz ist auf exaktem resultierendem Master belegt: Die Default-Branch-
Analyse meldet den ursprünglichen `c:S107`-Key nicht mehr, öffentliche JSON-/
CLI-Semantik ist erhalten, GCC/Clang-Warning-as-Error-Builds und Real-Library-
Controls bestehen, und Hosted-Checks endeten ohne Bypass. Regression:
`tests/test_sonar_reliability_contract.py`. Legitime Controls: reale 200-,
403- und Setup-Error-Result-Pfade.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

Exact-Draft-PR- und Resulting-Master-Hosted-Analysen sind erhalten.
Integration und Resulting-Master-Revalidierung sind abgeschlossen; für dieses
verifizierte Finding gibt es keinen technischen Blocker. `FND-SONAR-0016` ist
aggregierter Sonar-Kontext; `FND-SONAR-0024` ist die getrennte
Komplexitätsursache; `FND-PARENT-0036` ist das getrennte Native-Lifetime-
Finding. Es erfolgte keine Risikoakzeptanz; die geschützte Master-Integration
ist als Evidence erfasst.

## Historie

- `2026-07-30T10:46:48Z`: als getrennte `c:S107`-Source-Grenze alloziert;
  lokale Compiler-, Source-Contract- und Real-LibModSecurity-Controls bestehen,
  Hosted-Exact-Head-Sonar-Verifikation war zu diesem Zeitpunkt pending.
- `2026-07-30T11:07:21Z`: Exakter Draft-PR-#200-Head `2bc97ac058725fdba6a36ad93307487c160b1f05` bestand
  erforderliche GitHub-Checks und SonarQube-Cloud-Quality-Gate/Readbacks. Der
  ursprüngliche `c:S107`-Key `AZ7b3dgOcO69wzd-_jHt` fehlt in der PR-Issue-Abfrage;
  Status bleibt `fixed` pending autorisierte Integration und Resulting-
  Master-Verifikation.
- `2026-07-30T11:33:48Z`: nachdem Master auf `726322b17d6423c7f9e3bba0e6affc051dbf94cd` vorrückte, bestand aufgefrischter exakter Draft-PR-#200-Head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` erforderliche GitHub-Checks und SonarQube-Cloud-Quality-Gate/Readbacks. Der ursprüngliche `c:S107`-Key `AZ7b3dgOcO69wzd-_jHt` fehlt in der Null-Issue-PR-Abfrage; Status bleibt `fixed` pending autorisierte Integration und Resulting-Master-Verifikation.

## Resulting-Master-Disposition

Geschützter Squash-PR #200 vom exakten Head `5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` erzeugte Parent-
Master `13890da56ad19a105629243349f39ea8c084f396` am `2026-07-30T12:11:32Z`. Die Native-Oracle- und
fokussierten Reliability-Test-Blobs entsprechen dem geprüften Kandidaten;
seine direkten Semantik-, Compiler- und Real-LibModSecurity-Controls gelten
daher für diese exakte Quelle. Alle 14 Master-Workflows bestanden, und die
Default-Branch-Analyse `c1f32224-aa05-4202-9b10-65c15165ff35` meldet
`AZ7b3dgOcO69wzd-_jHt` nicht mehr.

Das projektweite Quality Gate bleibt für zurückgehaltene unabhängige
Bedingungen nicht ignoriert `ERROR`, ist aber kein Akzeptanzkriterium für
dieses nicht sicherheitsrelevante Maintainability-Finding. Der ursprüngliche
Key fehlt auf resultierendem Master bei bewahrten Controls; der Status steigt
daher auf `verified`, nicht `closed`. Receipt-SHA-256: `69cdb1bbdc92c4faa82e2e722dd27d5eac32b3d33df50cc64fc7ed110d9da48a`.
