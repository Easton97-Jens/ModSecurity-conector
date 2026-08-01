# FND-FRAMEWORK-0005 — PCRE2-Archiv-Digest kann vor Framework-Extraction unset sein

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0005` |
| Title / Titel | `PCRE2-Archiv-Digest kann vor Framework-Extraction unset sein` |
| Category / Kategorie | `security_validated` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P2` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `validated` |
| Status | `fixed` |
| Final disposition / Finale Disposition | `fixed_pending_framework_pr_verification` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Der Framework-PCRE2-Source-Archive-Pfad akzeptierte zuvor einen leeren Digest und konnte unverifizierte Bytes extrahieren. Der Task-Branch verlangt nun vor dem realen Extraction-Sink ein geprüftes SHA-256-Literal und behält fokussierten lokalen Nachweis.

## Observed behavior / Beobachtetes Verhalten

Vor dem Fix waren `PCRE2_SHA256` und `PCRE2_SHA256_URL` standardmäßig leer und optionale Verifikations-Helper kehrten vor der Extraction erfolgreich zurück. Nach dem Fix enden leere, nur-Whitespace-, malformed und abweichende `PCRE2_SHA256`-Werte mit `77`, bevor das PCRE2-Archiv `tar` erreicht; das passende lokale Fixture erreicht den erwarteten Extraction-Pfad.

## Expected behavior / Erwartetes Verhalten

Kein PCRE2-Archiv darf Extraction oder weitere Verarbeitung erreichen, bevor ein nicht leerer, syntaktisch gültiger und exakt passender SHA-256-Digest verifiziert wurde.

## Impact / Auswirkung

Die implementierte Kontrolle schließt die zuvor optionale Archive-Integrity-Grenze im Framework-PCRE2-Provisioning-Pfad. Die PR-Verifikation des aktuellen Heads bleibt durch den unabhängigen common-structure-Fehler `FND-FRAMEWORK-0001` blockiert.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `modules/ModSecurity-test-Framework/ci/lib/common.sh`
- `modules/ModSecurity-test-Framework/ci/provisioning/prepare-apache-build.sh`
- `modules/ModSecurity-test-Framework/tests/security_regression/test_pcre2_archive_digest.py`
- `modules/ModSecurity-test-Framework/tests/fixtures/pcre2-digest/`

### Symbols / Symbole

- `PCRE2_SHA256`
- `verify_required_pcre2_sha256`
- `build_pcre2_from_source`
- `extract_tar_strip`

## Preconditions / Voraussetzungen

- Der Framework-Apache-PCRE2-Source-Build-Pfad wird aufgerufen.
- Ein Aufrufer liefert die PCRE2-Archivquelle und kann `PCRE2_SHA256` überschreiben.
- Die retained Assessment- und Task-Run-Evidence bleibt verfügbar.

## Reproduction / Reproduktion

- Vor dem Fix: Die optionalen Digest-Helper vor dem PCRE2-`extract_tar_strip`-Sink in der Framework-Basisrevision prüfen.
- Nach dem Fix: `tests.security_regression.test_pcre2_archive_digest` über den echten `prepare-apache-build.sh`-Entry-Point mit dem isolierten lokalen Archive-Fixture ausführen.

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:221-227,238-244`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '221,227p;238,244p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260718T092308Z-fnd-framework-0005-pcre2-digest-e064e1d8`
  - Artifact: `.codex/runs/20260718T092308Z-fnd-framework-0005-pcre2-digest-e064e1d8/validation.md`
  - Type: `security_fix_validation_receipt`; SHA-256: `7f8c99d3df6788a145f09de893ee990f2e04d3a0ecec077aa57121d54c3ec0db`
  - Command: fokussierte tatsächliche Preparation-Script-Regression, Framework-Lint-/Dokumentationschecks, Source-to-Sink-Review und Current-Head-PR-/CI-/Sonar-Inspektion
  - Working directory: `/var/tmp/codex/ModSecurity-test-Framework/worktrees/fw-pcre2-digest`; exit code: `0`
  - Observed at: `2026-07-18T10:01:20Z`; retention: `retained_local_hash_addressed`

## Root-cause analysis / Grundursachenanalyse

Der Apache-PCRE2-Provisioning-Pfad behandelte beide Digest-Quellen als optional: Seine Verifikations-Helper kehrten bei leerer Eingabe erfolgreich zurück und die Extraction folgte unmittelbar.

## Proposed remediation / Vorgeschlagene Remediation

Implementiert wurden ein geprüftes PCRE2-SHA-256-Default, das explizit leere Overrides erhält, ein PCRE2-spezifischer erforderlicher 64-Hex-Verifier, exaktes Archive-Hashing vor dem einzigen Extraction-Sink sowie isolierte Negative-/Kontrollregressionen mit `tar`-Instrumentierung.

## Acceptance criteria / Akzeptanzkriterien

- Ein leerer, nur aus Whitespace bestehender, syntaktisch ungültiger oder abweichender PCRE2-Digest schlägt vor Extraction oder weiterer Verarbeitung fehl.
- Jeder negative Fall beweist, dass das PCRE2-Archiv `tar` nicht erreicht hat.
- Ein syntaktisch gültiger exakt passender Digest erlaubt dem isolierten Fixture-Archiv, den erwarteten Extraction-Pfad zu erreichen.

## Validation plan / Validierungsplan

- Das tatsächliche Preparation-Script mit isolierten leeren, nur-Whitespace-, malformed und abweichenden Digest-Fixtures ausführen und `tar`-Instrumentierung erfassen.
- Die passende Digest-Kontrolle über dieselbe Script-Grenze ausführen.
- Fokussierte Framework-Regression, Syntax-, Dokumentations-, Lint-/Static-Analysis-, ShellCheck- und Source-to-Sink-Checks ausführen.

## Regression tests / Regressionstests

- `tests/security_regression/test_pcre2_archive_digest.py`: vier negative Digest-Fälle sowie eine passende Kontrolle über `ci/provisioning/prepare-apache-build.sh`.

## Legitimate control tests / Legitime Kontrolltests

- Eine korrekte SHA-256 für das deterministische lokale PCRE2-Fixture beendet sich mit `0`, erreicht genau einmal den PCRE2-`tar`-Marker und beendet den Fixture-`pcre2-config`-Pfad.

## Grundursachen-Triage / Root-cause triage

- Basis-Framework-SHA: `cdc91a398d6c156eaff927d742b23018a3817fb6`; Task-Head: `320627da979f5a3da607460d6e3b6bb0b9cb8c61`.
- Urteil: vor der Remediation `confirmed`; statische Confidence: `medium`. Die validierte Task-Kontrolle liegt bei `ci/provisioning/prepare-apache-build.sh:300-327,361-364`.
- Grundursachen-Gruppe: `RC-FW-003-pcre2-archive-digest-fail-closed`; Singleton. Mit `FND-FRAMEWORK-0006` besteht nur eine Archive-Integrity-Familie, kein gemeinsamer Patch oder Regression-Group.
- Source → Broken Control / Sink vor der Remediation: `PCRE2_SOURCE_URL`-Archivbytes mit leeren Defaults `PCRE2_SHA256` und `PCRE2_SHA256_URL` → optionale Verifikations-Helper akzeptierten leere Werte → `tar`-Extraction. Der korrigierte Pfad ruft `verify_required_pcre2_sha256` unmittelbar vor dem einzigen PCRE2-`extract_tar_strip`-Sink auf.
- Angreifervoraussetzungen vor der Remediation: Ein PCRE2-Source-Build lief mit leerem Digest und das externe Archiv wurde vor Consumption ersetzt. Kein ersetztes Upstream-Archiv wurde geladen oder ausgeführt.
- Gegenkontrolle nach der Remediation: Die no-colon-`PCRE2_SHA256`-Expansion erhält einen explizit leeren Override zur Zurückweisung; der Verifier verlangt exakt 64 Hex-Zeichen, normalisiert die Groß-/Kleinschreibung, hasht das Archiv, vergleicht exakt und `PCRE2_SHA256_URL` besitzt keine Extraction-Verifikations-Fallback-Rolle.
- Erforderliche Regression / legitimer Kontrollfall: leere, nur-Whitespace-, 64-Zeichen-nicht-Hex- und falsche 64-Hex-Digests schlagen vor `tar` fehl; der passende Fixture-Digest erreicht einen PCRE2-`tar`-Marker.
- Parent-Auswirkung: keine; ein späteres Framework-Delivery kann Parent nur über ein separat autorisiertes Gitlink-Update erreichen. MRTS-Auswirkung: keine; kein MRTS-Pfad ist beteiligt.
- Delivery-Grenze: ausschließlich Framework-Branch `codex/fix-framework-pcre2-digest` und Draft-PR [#22](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/22); Parent-Gitlink unverändert; MRTS unberührt. Das SonarQube-Cloud-Quality-Gate bestand mit null Security-Hotspots.
- Current-Head-Blocker: PR #22 `test-common` / `common-structure` schlägt mit `expected 141 YAML cases, found 179` fehl. Derselbe Zustand schlug am Basis-SHA fehl und wird unabhängig als `FND-FRAMEWORK-0001` verfolgt; er liegt außerhalb dieses Finding-only-Scopes.
- Nachweisgrenze: Kein realer Download oder vollständiger Apache-Build lief, weil das isolierte Fixture die tatsächliche Script-Enforcement-Grenze ausübte, wie im Task autorisiert.

## Remediation-Validierung / Remediation validation

- Die lokale Full-Script-Regression bestand drei Unittest-Methoden mit vier negativen Eingaben und einer passenden Kontrolle.
- Leere, nur-Whitespace-, malformed 64-Zeichen-nicht-Hex- und falsche 64-Hex-Digests endeten jeweils mit `77` und schrieben keinen PCRE2-Archiv-Eintrag in das Fake-`tar`-Log.
- Das passende deterministische lokale bzip2-Fixture endete mit `0`, schrieb genau einen PCRE2-`tar`-Marker und beendete den Fixture-`pcre2-config`-Pfad.
- Fixture-JSON-Syntax, `sh -n`, `bash -n`, `make check-documentation`, `make lint`, `git diff --check` und statisches Source-to-Sink-Review bestanden. ShellCheck 0.11.0 behielt dieselben 17 Basis-Diagnosen, keine im geänderten PCRE2-Control.
- SonarQube Cloud für PR #22 bestand sein Quality Gate; der PR meldet zwei neue Issues, null Security-Hotspots und null New-Code-Coverage/Duplikation.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- `FND-FRAMEWORK-0001`: Der Current-Head von PR #22 kann `verified_pr` nicht erreichen, solange `test-common` / `common-structure` mit `expected 141 YAML cases, found 179` fehlschlägt; derselbe Fehler besteht am Basis-SHA und liegt außerhalb dieses Finding-only-Scopes.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0006`

## Residual risk / Restrisiko

Der Task-Branch erzwingt die PCRE2-Archive-Digest-Grenze und besitzt lokalen Source-to-Sink-Nachweis. Der unabhängig verfolgte common-structure-Fehler `FND-FRAMEWORK-0001` verhindert `verified_pr` für den aktuellen Head; kein Risiko wurde akzeptiert und kein Merge erfolgte.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-18T08:09:21Z`: root_cause_triaged — Aktuelle statische Evidence bestätigte optionale PCRE2-Digest-Enforcement; sie bleibt vom NGINX-Consumer-/Control-Pfad getrennt.
- `2026-07-18T10:01:20Z`: local_fail_closed_remediation_validated — Der Task-Branch verlangt den PCRE2-Verifier unmittelbar vor der Extraction; die vier negativen Fälle erreichen nie `tar` und die passende Kontrolle besteht. Draft-PR #22 bleibt ungemergt; sein `verified_pr`-Status wird nur durch den vorbestehenden common-structure-Fehler `FND-FRAMEWORK-0001` blockiert, während das SonarQube-Cloud-Quality-Gate bestand.

## Direkte Stale-PR-Rückeinführungsgefahr vom 2026-07-19

Direkte Vergleiche vom aktuellen Framework-`master`
`9954b99a31fab0006cdf903ab477c8158c50fea8` zeigen, dass die veralteten
ungemergten Heads #24, #27 und #29 leere PCRE2-Digest-Defaults, optional-
erfolgreiche Verifikation und Extraction/Build nach der übersprungenen
Prüfung wiederherstellen. Die Source-to-Sink-Bedingung ist nur ein
Merge-Blocker: `master` bleibt `fixed`, und das Finding wird nicht wieder
geöffnet.

Zurückgehaltene Evidence: Run
`20260719T081017Z-framework-pr-resolution-20260719-840082e0`,
`analysis/direct-merge-hazards.md`, SHA-256
`d28d88c9b1f034e1798cfa805d3b4e7210e3e3742dc4014d19ef78238c5c2004`;
beobachtet am `2026-07-19T12:01:55Z` durch RTK-präfixierte Direct-Diff- und
statische PCRE2-Source-to-Sink-Review.
