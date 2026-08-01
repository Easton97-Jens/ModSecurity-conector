# FND-GITHUB-0003 — Framework-CodeQL-Klartext-Logging-Alert #1 ist ein False Positive des statischen Checkers

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-GITHUB-0003` |
| Kategorie | `static_analysis_finding` |
| Repository | `framework` |
| Ownership | `external_tool` |
| Priorität | `P2` |
| Severity | `not_applicable` |
| Confidence | `validated` |
| Status | `not_applicable` |
| Release-Blocker | `false` |
| Security-Relevanz | `true` |

## Zusammenfassung

Nach dem Merge von PR #23 eröffnete GitHub CodeQL den High-Severity-Alert #1 (`py/clear-text-logging-sensitive-data`) auf dem Framework-Master-Commit `e482549b93d95ba85830a208e99a2ba0331ec351`. Die exakte Source-to-Sink-Triage beweist, dass CodeQL die statische Detector-Pattern-Liste in Zeile 8 bis zum Error-Printer in Zeile 32 verfolgt. Der Checker liest Fixtures nur für Prädikate und gibt weder einen Fixture-Treffer noch Dateiinhalte aus: Seine Diagnostic-Strings enthalten ausschließlich feste Required-Pfade, feste Phrasen, Detector-Pattern-Literale oder allow-gelistete Feldnamen. Der Alert wurde autoritativ als `false positive` dismissed; es gab keine Änderung an Framework-Source, Parent-Gitlink, MRTS-Status, PR, Berechtigungen oder Branch-Protection.

## Beobachtetes und erwartetes Verhalten

Unmittelbar vor dem autorisierten PATCH zeigte GitHub Alert #1 als offen auf dem exakten Master `e482549b93d95ba85830a208e99a2ba0331ec351`, mit Source `ci/checks/security/check-security-data-flow-cases.py:8:17-8:102` und Sink `:32:15-32:32`. Die statische Inspektion des identischen Blobs `8d8e273d48bd4cfcd6b59fff99222cb5df12f217` zeigt, dass `text = p.read_text()` ausschließlich boolesche Validierungen beeinflusst. Alle `errors.append(...)`-Werte werden aus einem festen Pfad, einer festen Phrase, einem Detector-Pattern-Literal oder einem allow-gelisteten Feldnamen gebildet. Der einzige Sink gibt `"\\n".join(errors)` nach stderr aus. GitHub meldete unmittelbar danach den Status `dismissed`, Grund `false positive` und `fixed_at: null` zurück.

Der Checker darf ein ungültiges Fixture identifizieren, ohne Fixture-Inhalte, gematchtes Secret-Material, Request-Bodies oder Credentials in CI-Output zu schreiben. CodeQL-Findings bleiben offen, sofern nicht eine exakte aktuelle Source-to-Sink-Analyse einen nicht ausnutzbaren False Positive belegt oder ein Fix verifiziert ist.

## Auswirkung und Grundursachenanalyse

Kein Klartext-Credential und kein sensibler Fixture-Inhalt erreicht im abgegrenzten Source den gemeldeten Sink. Eine Source-Code-Änderung nur zum Unterdrücken des Alerts würde den Control nicht verbessern und könnte seine Diagnostik schwächen. Die evidenzbasierte GitHub-Disposition entfernt diesen reinen Scanner-Master-Integrationsblocker; der unabhängige Master-SonarQube-Blocker bleibt unverändert.

Die generische CodeQL-Query für Klartext-Logging behandelt die feste Detector-Pattern-Liste als sensible Daten, wenn der Checker das aktuell gewählte Pattern in eine statische Validation-Diagnostik aufnimmt. Die Query unterscheidet ein Pattern-Literal nicht von einem gematchten Credential und modelliert nicht, dass der Fixture-Text nie ausgegeben wird.

## Betroffene Dateien und Symbole

- `ci/checks/security/check-security-data-flow-cases.py:8`
- `ci/checks/security/check-security-data-flow-cases.py:18-32`
- `Makefile:116,124-125`
- `py/clear-text-logging-sensitive-data`, `SECRET_PATTERNS`, `errors`, `check-security-data-flow-cases`, GitHub Code Scanning alert #1

## Voraussetzungen und Reproduktion

- Source-Blob: `8d8e273d48bd4cfcd6b59fff99222cb5df12f217`; master: `e482549b93d95ba85830a208e99a2ba0331ec351`.
- Die Alert-Source bleibt Zeile 8 und der gemeldete Sink bleibt Zeile 32 von `ci/checks/security/check-security-data-flow-cases.py`.
- Der Checker ist ein statischer `make lint` / `check-security-data-flow-cases`-Control, keine unterstützte Request-Processing-Surface.

```text
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/code-scanning/alerts/1
rtk sed -n '1,40p' ci/checks/security/check-security-data-flow-cases.py
rtk rg -n -C 3 'check-security-data-flow-cases\.py|security-data-flow' Makefile .github ci tests --glob '!tests/mrts/**'
```

## Evidenz

- Run `20260718T192214Z-framework-pr-resolution-20260718-b30403da`
  - Statische Triage: `/var/tmp/codex/ModSecurity-conector/runs/20260718T192214Z-framework-pr-resolution-20260718-b30403da/evidence/codeql-alert-1-triage.json`
  - SHA-256: `c8e8c052add0c6d1d54b152f2ebacf9141d1009aa0e4df8cc95636b0ef664b1b`
  - Typ: `static_codeql_source_to_sink_triage`; Befehl: GitHub-Alert-Metadaten/Instances plus statischer Source- und Source-Blob-Equality-Readback; Arbeitsverzeichnis: `/var/tmp/codex/worktrees/framework-common-structure`; Exit-Code: `0`; beobachtet: `2026-07-18T19:42:18Z`.
- Run `20260718T192214Z-framework-pr-resolution-20260718-b30403da`
  - Dismissal-Receipt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T192214Z-framework-pr-resolution-20260718-b30403da/evidence/codeql-alert-1-dismissal-receipt.json`
  - SHA-256: `74882ca084034fb5f9b96949734143d7ec9f30a3927ddc5056dac186cff1f449`
  - Typ: `github_code_scanning_alert_pre_patch_and_post_patch_receipt`; Befehl: GitHub `GET/PATCH/GET` Alert #1 mit exaktem Master-SHA-, Source- und Sink-Readback; Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`; beobachtet: `2026-07-18T19:45:12Z`.

## Remediation, Akzeptanzkriterien und Validierung

Keine Framework-Code-Remediation ist erforderlich. Checker und Secret-Pattern-Control bewahren, die exakte statische Triage und den GitHub-Receipt aufbewahren und Alert #1 nur mit Grund `false positive` plus Source-to-Sink-Begründung dismissen. Wieder öffnen/triagieren, falls sich analysierter SHA, Source-/Sink-Koordinaten oder ausgegebener Datenfluss des Alerts ändern.

- Der exakte Source-Blob und die Alert-Koordinaten stimmen mit der retained Triage überein.
- Fixture-Text, Match-Objekte, Request-Bodies und Credential-Werte gelangen nie in `errors` oder den Printer.
- GitHub Alert #1 liest als `dismissed` mit Grund `false positive`, exaktem SHA `e482549b93d95ba85830a208e99a2ba0331ec351` und `fixed_at: null` zurück.
- Keine Source-, Parent-Gitlink-, MRTS-, Branch-, PR-, Permission-, Rule- oder Security-Control-Änderung erlangt die Disposition.

Bei einer späteren Source-Änderung SHA/Source/Sink mit dieser Evidenz vergleichen, jedes `errors.append(...)` und den Printer erneut inspizieren, danach den GitHub-Alert auslesen. Die bestehende `make lint`-Invocation bleibt der Regression-Control. Ein sicheres Fixture-Set gibt nur den begrenzten Count aus; ein Verstoß gibt seinen festen Pfad und die feste Diagnostic-Kategorie aus, nicht gematchten Fixture-Text.

## Abhängigkeiten, Blocker, verwandtes Finding und Restrisiko

Es gibt keine Abhängigkeiten oder Blocker. Verwandtes Finding: `FND-SONAR-0002` bleibt der nicht zusammenhängende blockierte Framework-Master-SonarQube-Quality-Gate-Fehler.

Der abgegrenzte Checker kann einen festen Workspace-Pfad, ein Detector-Pattern-Literal oder einen allow-gelisteten Feldnamen in CI-Diagnostik offenlegen, aber keinen gematchten Fixture-Inhalt und kein Credential. Eine zukünftige Codeänderung, die `text`, ein Match-Objekt oder einen nicht vertrauenswürdigen Pfad an `errors` anhängt, macht diese Disposition ungültig und erfordert eine frische Triage.

## Aktueller GitHub-Abgleich für das Archiv — 2026-07-26

Der nur lesende GitHub-Abgleich um 2026-07-26T13:29:40Z meldet
Code-Scanning-Alert #1 als `dismissed`, Grund `false positive`; seine aktuelle
Instance bleibt auf dem Master-Checker-Pfad in Zeile 32. Die aktuelle
Framework-Source hält SECRET_PATTERNS weiterhin als statisches Tuple, verwendet
Fixture-Text nur für Validierungsprädikate, konstruiert Diagnostik nur aus
begrenzten Pfaden, festen Phrasen, statischen Patterns oder allow-gelisteten
Feldnamen und gibt nur diese begrenzte Diagnostikliste nach stderr aus.

In diesem Abgleich wurden weder Framework-Source, Workflow, Gitlink,
Parent-Source, Permission noch Security-Control geändert. Dies bleibt ein
validierter Scanner-False-Positive, kein Code-Fix. Der kanonische Status bleibt
`not_applicable`; das erhaltene EN/DE/JSON-Tripel wird archiviert. Vor einer
Wiederverwendung erneut öffnen und triagieren, falls Fixture-Text, ein
Match-Objekt oder ein nicht vertrauenswürdiger Pfad die Diagnostikliste oder
ihren Output-Sink erreichen kann.

## GitHub-Disposition und Historie

GitHub Code Scanning Alert #1 ist um `2026-07-18T19:45:12Z` von `Easton97-Jens` mit Grund `false positive` dismissed; `fixed_at: null`. Der dokumentierte Dismissal-Kommentar lautet: `Exact master e482549b93d95ba85830a208e99a2ba0331ec351: source is a hard-coded detector-pattern list. Diagnostics emit fixed paths, pattern literals, and allow-listed names--never fixture matches or content. Static source-to-sink triage: false positive.`

- `2026-07-18T19:15:30Z` — GitHub CodeQL eröffnete High-Severity-Alert #1 für `py/clear-text-logging-sensitive-data` auf Master `e482549b93d95ba85830a208e99a2ba0331ec351`; er war ein Master-Integrationsblocker bis zur Validierung.
- `2026-07-18T19:42:18Z` — Die exakte statische Source-to-Sink-Triage fand, dass nur feste Pfade, Phrasen, Detector-Pattern-Literale und allow-gelistete Feldnamen den Printer erreichen können. Verdict: `not_actionable`, hohe Confidence.
- `2026-07-18T19:45:12Z` — GitHub dismisste den passenden offenen Alert als `false positive`; `fixed_at` bleibt null. Keine Framework-/Parent-/MRTS-Source-, Gitlink-, Branch-, PR-, Permission-, Rule- oder Security-Control-Änderung erfolgte.
