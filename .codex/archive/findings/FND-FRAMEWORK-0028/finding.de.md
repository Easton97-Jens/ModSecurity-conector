# FND-FRAMEWORK-0028 — Framework-Autoupdater für ModSecurity v3 kann eine unvollständige Provenance-Identitätsänderung planen

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0028 |
| Kategorie | security_hardening |
| Repository / Ownership | framework / framework |
| Priorität / Severity | P2 / medium |
| Konfidenz / Status | validated / verified |
| Feasibility | feasible_now |
| Release-Blocker | false |
| Sicherheitsrelevant | true |

## Zusammenfassung, Beobachtung, erwartetes Verhalten und Auswirkung

Nachdem die Parser-Reparatur die freigegebenen ModSecurity-v3-Literale sichtbar
macht, meldet ein Live-Check v3.0.15 als veraltet und plant nur die Änderung von
MODSECURITY_V3_GIT_REF auf Zeile 184 zu v3.0.16. Der geplante privilegierte
Workflow schreibt common.sh und erstellt einen Pull Request, kann aber nicht
gleichzeitig die geprüfte Release-Tag-zu-Immutable-Commit-Identität etablieren.

Der Autoupdater darf keine partielle ModSecurity-v3-Identität schreiben. Ein
neues Release muss ein expliziter Review-Punkt bleiben, solange der Updater
nicht Release-Tag, Repository-Identität und freigegebenen Immutable-Commit
atomar prüfen und ändern kann.

Die Runtime-Provenance-Validierung weist den inkonsistenten Alias fail-closed
ab; dies ist daher kein bestätigter Supply-Chain-Bypass. Der privilegierte
geplante Workflow könnte jedoch unbrauchbare Update-Pull-Requests erzeugen und
einen Operator zur Abschwächung eines Provenance-Controls drängen. Das
Verhindern partieller Automation bewahrt die freigegebene Tag-zu-Commit-Grenze.

## Scope, Voraussetzungen, Reproduktion und Evidence

Betroffene Framework-Pfade sind ci/tools/check-common-versions.py,
.github/workflows/check-common-versions.yml und ci/lib/common.sh. Relevante
Symbole sind check_github_release_ref, check_all, MODSECURITY_V3_GIT_REF,
MODSECURITY_V3_RELEASE_TAG, MODSECURITY_V3_APPROVED_COMMIT und
ci_require_approved_modsecurity_v3_provenance.

Das Problem erfordert aufgelöste freigegebene Literale, ein neueres GitHub-
ModSecurity-v3-Release und die Ausführung des geplanten Workflows mit --update
und contents-/pull-requests-Schreibrechten.

1. python3 ci/tools/check-common-versions.py --check --json --timeout 20
   ausführen.
2. Eine veraltete ModSecurity-v3-Komponente und einen Update-Plan nur für
   MODSECURITY_V3_GIT_REF beobachten.
3. Den Write-Modus des geplanten Workflows und die Runtime-Provenance-Invariante
   inspizieren.
4. Bestätigen, dass der Plan MODSECURITY_V3_RELEASE_TAG oder
   MODSECURITY_V3_APPROVED_COMMIT nicht atomar aktualisiert.

Aufbewahrte Evidence:

- Run: 20260720T080314Z-parent-pr55-57-59-framework-update-3443af13
- Artifact:
  /var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/framework-common-version-parser/modsecurity-v3-auto-update-plan.json
- Typ: framework_modsecurity_v3_partial_auto_update_plan
- SHA-256: 93f14b78781506a54f7d04f36067b50f47d95c1f94eb9147e309eb7435597368
- Command: python3 ci/tools/check-common-versions.py --check --json --timeout 20;
  Source- und Scheduled-Workflow-Review
- Working directory: /var/tmp/codex/worktrees/framework-common-version-parser
- Exit-Code: 1
- Beobachtet: 2026-07-20T09:01:13Z
- Retention: retained
- Ergebnis: Nur MODSECURITY_V3_GIT_REF ist von seinem Release-Tag-Alias auf
  v3.0.16 zur Änderung geplant.

## Ursachenanalyse und vorgeschlagene Remediation

check_all ruft den generischen check_github_release_ref mit dem
Kompatibilitätsalias MODSECURITY_V3_GIT_REF als ref_var auf. Der generische
Updater kann einen Release-Tag nicht an seinen Immutable-Commit binden oder die
gekoppelte freigegebene Identität atomar aktualisieren.

ModSecurity v3 nach dem bestehenden CRS-Provenance-Pfad modellieren: das
freigegebene Repository/den Release-Tag prüfen, ein neueres Release als
unknown/manual review melden und automatische Updates leeren. Eine fokussierte
Regression ergänzen, die beweist, dass ein veraltetes ModSecurity-v3-Release den
Kompatibilitätsalias nicht allein ändern kann.

## Akzeptanzkriterien und Validierungsplan

- [x] Ein veraltetes ModSecurity-v3-Release erzeugt kein automatisches Update
  für MODSECURITY_V3_GIT_REF.
- [x] Die Komponente meldet einen review-pflichtigen unknown/manual-review-
  Zustand statt eines partiellen Updates.
- [x] Das Kandidaten-Komponentenergebnis liefert Exit zero, wenn nur
  review-pflichtige unknown-Zustände verbleiben.
- [x] Die Runtime-Prüfungen für Exact-Commit und Alias-Gleichheit bleiben
  unverändert.
- [x] Keine Parent-Datei, kein Sonar-Control und keine MRTS-Datei ändern sich.

Fokussierte In-Memory-Release-Client-Abdeckung ergänzen, die fokussierte
Common-Version-Provenance-Suite und den ModSecurity-v3-Provenance-Contract
ausführen und die leere Update-Liste des Kandidaten reviewen. Update-Modus darf
nie gegen kanonisches common.sh laufen; bei keinem anzuwendenden ModSecurity-
v3-Update ist auch kein Fixture-Write erforderlich. Den exakten Diff reviewen
und Exact-Head-Framework-PR-Checks sammeln.

## Lokale Remediation und beobachtete Validierung

Der gleiche isolierte Framework-Task-Branch ergänzt
`check_modsecurity_v3_release_provenance`. Er prüft das freigegebene Repository
und den geprüften Release-Tag-Anker, meldet ein neueres Release als `unknown` /
manuelle Review und leert alle Update-Anweisungen. Die Kompatibilitätsaliase
können daher vom geplanten Writer nicht allein geändert werden.

Die In-Memory-Regression für ein neueres Release prüft `STATUS_UNKNOWN`, eine
leere Update-Liste, den exakten Review-Grund und `exit_code([result]) == 0`.
Die fokussierte Suite bestand 15 Tests; der bestehende 10-Test-ModSecurity-v3-
Provenance-Contract, die Dokumentationsprüfungen und Framework-Lint bestanden
ebenfalls. Unabhängige Source-Security-Review und Folgeprüfung fanden keinen
Bypass, keine Berechtigungserweiterung und keine MRTS-Änderung.

Der kanonische schreibende Update-Befehl wurde bewusst nicht ausgeführt.
Statische Review und die leere Update-Liste zeigen, dass sein Update-Applikator
keinen ModSecurity-v3-Write ausführen kann.

Framework-Draft-PR [#36](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/36)
liefert nun Exact-Head-gehostete Evidence für
`2bf862e1a5f262251043ec421447f6e4db11e17d` gegen Basis
`efdbcbd98afeed0f39f8912ce1140aaa5742f507`: Er ist offen, Draft und
mergeable `CLEAN`. Alle 14 terminalen Checks sind aktuell: 11 bestanden
(einschließlich CodeQL Actions/Python/C++, SonarCloud Code Analysis,
PR-Head/Range, scaffold-lint und common-structure); 3 Advisory-Checks sind
erwartete Skips; keiner schlug fehl, wurde abgebrochen oder ist noch pending.
Es wurden keine Reviews oder ungelösten Review-Threads beobachtet.

Post-Merge-Lifecycle-/Evidence-Ereignis vom `2026-07-20T13:10:07Z`: PR #36
wurde am `2026-07-20T13:06:39Z` normal als Framework-master
`784977615acfc55567e37b863309abc4a38ac877` gemergt. Der aktualisierte PR-Head
`1608352912a755f0f8639eddfa2350436446067e` ist ein Vorfahr und sein Tree ist
identisch mit diesem Master. Frische gehostete Evidence für genau diesen Head
bestand: CodeQL Actions, Python und C++; OSV; OpenSSF; Secret Scanning; lint;
test-common; und das PR-SonarQube-Cloud-Quality-Gate mit 0 neuen Issues, 0
Security Hotspots und 0.0% Duplikation. Es wurden keine menschlichen Reviews,
Review Requests oder ungelösten Review-Threads beobachtet. Resultierende
Master-CodeQL-Actions-/Python-/C++-, lint-, test-common- und OpenSSF-Checks
bestanden ebenfalls. Der getrennte Master-Sonar-Check scheiterte nur mit
geerbtem FND-SONAR-0002 Security E unter der abgegrenzten master-only-
Akzeptanz des aktuellen Nutzers; diesem Finding wird keine Kausalität
zugeschrieben.

Das aufbewahrte isolierte Exact-Master-Original-Reproduktionsartefakt
`analysis/pr36-master-common-version-original-reproduction.json`
(SHA-256 `4d2311ab1287b3943633b5f9d5243451ad697d66726d6a6d57012b3fae7eb1ab`)
erfasst Exit-Code 0 für `--check --json --timeout 20`: ModSecurity v3.0.15
gegenüber v3.0.16 bleibt `unknown` / manuelle Review mit leerer Update-Liste,
während `missing_required` leer ist und alle freigegebenen Anker und Aliase
auflösen. Der Befehl verwendete nur `--check` und führte weder `--update`,
`--markdown` noch `--write-files` aus. Die früheren lokalen Parser-15/15-,
Provenance-Contract-10/10-, `py_compile`-, Bilingual-/Documentation- und
Diff-Checks bleiben Teil der Exact-Head-Evidence. Die getrennte
FND-SONAR-0002-Akzeptanz hebt keinen frischen PR-Head-Check, kein PR-Sonar-
Gate, Review-, Berechtigungs- oder Security-Control auf.

## Regressions- und Legitimate-Control-Tests

Regressionstests:

- tests/security_regression/test_common_versions_sonar_provenance.py
- make test-modsecurity-v3-provenance-contract

Legitimate Controls:

- Das aktuelle freigegebene ModSecurity-v3-Release bleibt ohne Update current.
- Ein neueres Release bleibt für manuelle Review sichtbar, ohne common.sh zu
  ändern.
- Runtime-Provenance weist abweichende Aliase oder Immutable-Commits weiterhin
  ab.

## Abhängigkeiten, Grenzen, verwandte Findings und Restrisiko

Die historischen Exact-Head- und aktuellen Exact-Master-Controls erfüllen nun
die Source-Validierungsabhängigkeit dieses Findings; GitHub-Releases-API-
Verfügbarkeit bleibt eine legitime Runtime-Abhängigkeit des Checkers. Dies ist
kein Duplikat von FND-FRAMEWORK-0027: Dieses Finding besitzt fehlende Literal-
Auflösung, während das vorliegende partielle automatische Updates nach
Auflösung der Literale besitzt.

Die normale Framework-Master-Delivery erfolgte ohne Parent-Datei oder
Parent-Gitlink-Update und ohne MRTS-Inhalts- oder Git-Aktion. Update-Modus
wurde nicht gegen kanonisches common.sh ausgeführt, um Source-Mutation zu
vermeiden. Das Runtime-Control weist das inkonsistente Ergebnis weiterhin ab;
ein erfolgreicher bösartiger Dependency-Update wurde nicht reproduziert.

Manuelle ModSecurity-v3-Release-Maintenance bleibt nötig, bis ein sicherer
Tag-zu-Immutable-Commit-Resolver entwickelt und geprüft ist. Diese Reparatur
bewahrt bewusst manuelle Review, statt einen Commit-Pin aus einem ungeprüften
Release-Tag zu synthetisieren.

## Aktuelle Delivery-Disposition

Dieses Finding ist `verified`, nicht `closed` oder risikoakzeptiert. PR #36
wurde normal als exakter Framework-master
`784977615acfc55567e37b863309abc4a38ac877` gemergt; sein Tree entspricht dem
aktualisierten Head `1608352912a755f0f8639eddfa2350436446067e`, und die
ursprüngliche Partial-Auto-Update-Reproduktion sowie Legitimate Controls
bestanden auf diesem Master. FND-SONAR-0002 bleibt ein separates blocked
Framework-Master-Issue mit abgegrenzter master-only-Akzeptanz; es verändert
weder den verified-Status dieses Findings noch hebt es seine PR-Controls auf.
Es erfolgte keine Parent-Gitlink- oder MRTS-Aktion.

## Historie

- 2026-07-20T09:01:13Z — confirmed_during_fnd_framework_0027_security_review:
  Der Live-Check plante nur MODSECURITY_V3_GIT_REF=v3.0.16. Die
  Sicherheitsreview bestätigte fail-closed Runtime, aber der privilegierte
  geplante Updater könnte sonst einen inkonsistenten Pull Request erzeugen.
- 2026-07-20T09:36:58Z — local_remediation_validated: Der Provenance-Wrapper
  macht aus einem neueren ModSecurity-v3-Release ein Manual-Review-Ergebnis mit
  leerem Update, und die fokussierten Contract-, Dokumentations-, Lint- und
  unabhängigen Security-Checks bestanden. Exact-Head-Draft-PR-Evidence bleibt
  ausstehend; es gab keine Framework-Master-, Parent- oder MRTS-Git-Aktion.
- 2026-07-20T10:14:31Z — fixed_on_framework_pr_36_exact_head_validated:
  Draft-PR #36 Exact Head `2bf862e1a5f262251043ec421447f6e4db11e17d`, basierend
  auf `efdbcbd98afeed0f39f8912ce1140aaa5742f507`, ist mergeable CLEAN mit 11
  erfolgreichen und 3 expected-skipped terminalen Checks sowie ohne
  fehlgeschlagenen/pending Check, Review oder ungelösten Review-Thread.
  Master-Merge, Current-Master-Reproduktion, Parent-Gitlink und MRTS-Aktionen
  bleiben out of scope.
- 2026-07-20T13:10:07Z — verified_on_framework_master_after_pr_36_normal_merge:
  PR #36 wurde am `2026-07-20T13:06:39Z` normal als Framework-master
  `784977615acfc55567e37b863309abc4a38ac877` gemergt; exakter Head
  `1608352912a755f0f8639eddfa2350436446067e` ist ein Vorfahr mit einem zu
  Master identischen Tree. Frische PR-Head-Controls und resultierende
  Master-CodeQL-Actions-/Python-/C++-, lint-, test-common- und OpenSSF-Checks
  bestanden. Das aufbewahrte Exact-Master-Artefakt
  `analysis/pr36-master-common-version-original-reproduction.json` (SHA-256
  `4d2311ab1287b3943633b5f9d5243451ad697d66726d6a6d57012b3fae7eb1ab`) erfasst
  Exit 0, v3.0.15 gegenüber v3.0.16 als `unknown` / manuelle Review und eine
  leere Update-Liste. Das Master-Sonar Security E ist das getrennte geerbte
  FND-SONAR-0002-Gate unter einer abgegrenzten Akzeptanz, keine kausale
  Disposition dieses Findings; es erfolgte keine Parent-Gitlink- oder
  MRTS-Aktion.
